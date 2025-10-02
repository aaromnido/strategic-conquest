/**
 * Main game application
 */

class Game {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.renderer = new HexRenderer(this.canvas);
        this.inputHandler = new InputHandler(this.canvas, this.renderer, this);

        this.gameState = null;

        this.setupUI();
        this.startNewGame();
    }

    setupUI() {
        // New game button
        document.getElementById('new-game-btn').addEventListener('click', () => {
            if (confirm('Start a new game? Current progress will be lost.')) {
                this.startNewGame();
            }
        });

        // End turn button
        document.getElementById('end-turn-btn').addEventListener('click', () => {
            this.endTurn();
        });

        // Save game button
        document.getElementById('save-game-btn').addEventListener('click', () => {
            const filename = prompt('Enter save name:', 'savegame');
            if (filename) {
                this.saveGame(filename);
            }
        });

        // Load game button
        document.getElementById('load-game-btn').addEventListener('click', () => {
            const filename = prompt('Enter save filename:');
            if (filename) {
                this.loadGame(filename);
            }
        });
    }

    async startNewGame() {
        try {
            this.addLog('Starting new game...', 'neutral');

            const response = await gameAPI.newGame(30, 20);

            if (response.success) {
                this.gameState = response.state;
                this.renderer.update(this.gameState);
                this.updateUI();
                this.addLog('New game started!', 'victory');
            } else {
                this.addLog(`Error: ${response.error}`, 'error');
            }
        } catch (error) {
            this.addLog(`Failed to start game: ${error.message}`, 'error');
            console.error(error);
        }
    }

    async refreshState() {
        try {
            const response = await gameAPI.getState();

            if (response.success) {
                this.gameState = response.state;
                this.renderer.update(this.gameState);
                this.updateUI();

                // Check for game over
                if (this.gameState.game_over) {
                    this.showGameOver();
                }
            }
        } catch (error) {
            console.error('Failed to refresh state:', error);
        }
    }

    async moveUnit(unitId, targetHex) {
        const response = await gameAPI.moveUnit(unitId, targetHex);
        return response;
    }

    async attack(attackerId, defenderId) {
        const response = await gameAPI.attack(attackerId, defenderId);
        return response;
    }

    async produceUnit(cityId, unitType) {
        const response = await gameAPI.produceUnit(cityId, unitType);
        return response;
    }

    async endTurn() {
        try {
            this.addLog('Ending turn...', 'neutral');

            const response = await gameAPI.endTurn();

            if (response.success) {
                this.gameState = response.state;
                this.renderer.update(this.gameState);
                this.updateUI();
                this.addLog(`Turn ${this.gameState.turn} - Your turn`, 'neutral');

                // Check for game over
                if (this.gameState.game_over) {
                    this.showGameOver();
                }
            }
        } catch (error) {
            this.addLog(`Failed to end turn: ${error.message}`, 'error');
            console.error(error);
        }
    }

    async saveGame(filename) {
        try {
            const response = await gameAPI.saveGame(filename);

            if (response.success) {
                this.addLog(`Game saved: ${filename}`, 'production');
            } else {
                this.addLog(`Save failed: ${response.error}`, 'error');
            }
        } catch (error) {
            this.addLog(`Save error: ${error.message}`, 'error');
        }
    }

    async loadGame(filename) {
        try {
            const response = await gameAPI.loadGame(filename);

            if (response.success) {
                this.gameState = response.state;
                this.renderer.update(this.gameState);
                this.updateUI();
                this.addLog('Game loaded successfully', 'production');
            } else {
                this.addLog(`Load failed: ${response.error}`, 'error');
            }
        } catch (error) {
            this.addLog(`Load error: ${error.message}`, 'error');
        }
    }

    updateUI() {
        if (!this.gameState) return;

        // Update top bar
        document.getElementById('turn-number').textContent = `Turn: ${this.gameState.turn}`;

        const playerName = this.gameState.current_player === 'player1' ? 'HUMAN' : 'AI';
        document.getElementById('current-player').textContent = `Player: ${playerName}`;

        const resources = this.gameState.resources[this.gameState.current_player] || 0;
        document.getElementById('player-resources').textContent = `Resources: ${resources}`;
    }

    showUnitInfo(unit) {
        document.getElementById('unit-info').style.display = 'block';
        document.getElementById('city-info').style.display = 'none';

        document.getElementById('unit-type').textContent = unit.type;
        document.getElementById('unit-health').textContent = `${unit.health}/${unit.stats.max_health}`;
        document.getElementById('unit-movement').textContent = unit.movement_remaining;
        document.getElementById('unit-attack').textContent = unit.stats.attack;
        document.getElementById('unit-defense').textContent = unit.stats.defense;
    }

    showCityInfo(city) {
        document.getElementById('city-info').style.display = 'block';
        document.getElementById('unit-info').style.display = 'none';

        document.getElementById('city-name').textContent = city.name;
        document.getElementById('city-owner').textContent = city.owner || 'Neutral';

        if (city.current_production) {
            document.getElementById('city-production').textContent =
                `${city.current_production} (${city.production_progress}/${this.getUnitCost(city.current_production)})`;
        } else {
            document.getElementById('city-production').textContent = 'None';
        }
    }

    hideSelectionInfo() {
        document.getElementById('unit-info').style.display = 'none';
        document.getElementById('city-info').style.display = 'none';
    }

    getUnitCost(unitType) {
        const costs = {
            'infantry': 50,
            'tank': 100,
            'fighter': 80,
            'bomber': 120,
            'transport': 70,
            'destroyer': 90
        };
        return costs[unitType] || 100;
    }

    addLog(message, type = 'neutral') {
        const logDiv = document.getElementById('log-messages');
        const p = document.createElement('p');
        p.textContent = message;
        p.className = `log-${type}`;

        logDiv.appendChild(p);

        // Scroll to bottom
        logDiv.scrollTop = logDiv.scrollHeight;

        // Keep only last 50 messages
        while (logDiv.children.length > 50) {
            logDiv.removeChild(logDiv.firstChild);
        }
    }

    showGameOver() {
        const modal = document.getElementById('modal');
        const title = document.getElementById('modal-title');
        const message = document.getElementById('modal-message');

        if (this.gameState.winner === 'player1') {
            title.textContent = 'VICTORY!';
            message.textContent = 'You have conquered all enemy cities! You win!';
        } else {
            title.textContent = 'DEFEAT';
            message.textContent = 'All your cities have been captured. Better luck next time!';
        }

        modal.style.display = 'flex';

        document.getElementById('modal-close').onclick = () => {
            modal.style.display = 'none';
        };
    }

    // Helper methods for InputHandler
    isValidHex(q, r) {
        if (!this.gameState) return false;
        return this.gameState.map.hexes.some(hex => hex.q === q && hex.r === r);
    }

    getUnitAt(q, r) {
        if (!this.gameState) return null;
        return this.gameState.units.find(unit =>
            unit.position[0] === q && unit.position[1] === r
        );
    }

    getCityAt(q, r) {
        if (!this.gameState) return null;
        return this.gameState.cities.find(city =>
            city.position[0] === q && city.position[1] === r
        );
    }

    getCityById(cityId) {
        if (!this.gameState) return null;
        return this.gameState.cities.find(city => city.id === cityId);
    }
}

// Initialize game when page loads
window.addEventListener('DOMContentLoaded', () => {
    console.log('Strategic Conquest - Starting...');
    const game = new Game();
    window.game = game; // For debugging
});
