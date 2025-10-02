/**
 * Input handler for user interactions
 */

class InputHandler {
    constructor(canvas, renderer, game) {
        this.canvas = canvas;
        this.renderer = renderer;
        this.game = game;

        this.selectedUnit = null;
        this.selectedCity = null;
        this.mode = 'select'; // 'select', 'move', 'attack'

        this.setupEventListeners();
    }

    setupEventListeners() {
        this.canvas.addEventListener('click', (e) => this.handleClick(e));

        // Build buttons
        document.querySelectorAll('.build-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleBuildClick(e));
        });
    }

    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const hex = this.renderer.pixelToHex(x, y);

        if (!this.game.isValidHex(hex.q, hex.r)) {
            return;
        }

        const clickedUnit = this.game.getUnitAt(hex.q, hex.r);
        const clickedCity = this.game.getCityAt(hex.q, hex.r);

        // Handle different modes
        if (this.mode === 'select') {
            this.handleSelectMode(hex, clickedUnit, clickedCity);
        } else if (this.mode === 'move' && this.selectedUnit) {
            this.handleMoveMode(hex);
        } else if (this.mode === 'attack' && this.selectedUnit) {
            this.handleAttackMode(clickedUnit);
        }
    }

    handleSelectMode(hex, unit, city) {
        const currentPlayer = this.game.gameState.current_player;

        // Select unit
        if (unit && unit.owner === currentPlayer) {
            this.selectedUnit = unit;
            this.selectedCity = null;
            this.renderer.selectHex(hex.q, hex.r);
            this.game.showUnitInfo(unit);

            // Highlight possible moves and attacks
            this.highlightOptions(unit);
        }
        // Select city
        else if (city && city.owner === currentPlayer) {
            this.selectedCity = city;
            this.selectedUnit = null;
            this.renderer.selectHex(hex.q, hex.r);
            this.game.showCityInfo(city);
        }
        // Deselect
        else {
            this.clearSelection();
        }
    }

    async handleMoveMode(hex) {
        if (!this.selectedUnit) return;

        const result = await this.game.moveUnit(this.selectedUnit.id, hex);

        if (result.success) {
            this.game.addLog(`${this.selectedUnit.type} moved`);

            if (result.captured_city) {
                this.game.addLog(`Captured city!`, 'victory');
            }

            await this.game.refreshState();
        } else {
            this.game.addLog(`Cannot move: ${result.message}`, 'error');
        }

        this.clearSelection();
        this.mode = 'select';
    }

    async handleAttackMode(targetUnit) {
        if (!this.selectedUnit || !targetUnit) return;

        if (targetUnit.owner === this.selectedUnit.owner) {
            this.game.addLog('Cannot attack own units', 'error');
            return;
        }

        const result = await this.game.attack(this.selectedUnit.id, targetUnit.id);

        if (result.success) {
            this.game.addLog(
                `${this.selectedUnit.type} attacks ${targetUnit.type}! ` +
                `Damage: ${result.damage_to_defender}`,
                'combat'
            );

            if (result.defender_destroyed) {
                this.game.addLog(`${targetUnit.type} destroyed!`, 'combat');
            }

            await this.game.refreshState();
        } else {
            this.game.addLog(`Cannot attack: ${result.message}`, 'error');
        }

        this.clearSelection();
        this.mode = 'select';
    }

    async handleBuildClick(e) {
        if (!this.selectedCity) return;

        const unitType = e.target.dataset.unit;
        const result = await this.game.produceUnit(this.selectedCity.id, unitType);

        if (result.success) {
            this.game.addLog(`Started producing ${unitType}`, 'production');
            await this.game.refreshState();

            // Refresh city info
            const city = this.game.getCityById(this.selectedCity.id);
            if (city) {
                this.game.showCityInfo(city);
            }
        } else {
            this.game.addLog(`Cannot build: ${result.message}`, 'error');
        }
    }

    highlightOptions(unit) {
        const highlighted = [];
        const currentPlayer = this.game.gameState.current_player;

        // Get all hexes and units
        this.game.gameState.map.hexes.forEach(hex => {
            const distance = this.manhattanDistance(
                unit.position[0], unit.position[1],
                hex.q, hex.r
            );

            // Highlight move targets (green)
            if (distance <= unit.movement_remaining && distance > 0) {
                const targetUnit = this.game.getUnitAt(hex.q, hex.r);
                if (!targetUnit) {
                    highlighted.push({q: hex.q, r: hex.r, color: '#00FF00'});
                }
            }
        });

        // Highlight attack targets (red)
        this.game.gameState.units.forEach(target => {
            if (target.owner !== currentPlayer) {
                const distance = this.manhattanDistance(
                    unit.position[0], unit.position[1],
                    target.position[0], target.position[1]
                );

                if (distance <= unit.stats.range) {
                    highlighted.push({
                        q: target.position[0],
                        r: target.position[1],
                        color: '#FF0000'
                    });
                }
            }
        });

        this.renderer.highlightHexes(highlighted);
    }

    manhattanDistance(q1, r1, q2, r2) {
        return (Math.abs(q1 - q2) + Math.abs(q1 + r1 - q2 - r2) + Math.abs(r1 - r2)) / 2;
    }

    clearSelection() {
        this.selectedUnit = null;
        this.selectedCity = null;
        this.renderer.clearSelection();
        this.game.hideSelectionInfo();
    }
}
