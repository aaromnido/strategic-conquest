/**
 * Canvas renderer for hexagonal map
 */

class HexRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');

        // Disable image smoothing for pixel art
        this.ctx.imageSmoothingEnabled = false;

        this.hexSize = 25;
        this.offsetX = 50;
        this.offsetY = 50;

        this.gameState = null;
        this.selectedHex = null;
        this.highlightedHexes = [];
    }

    /**
     * Convert axial hex coordinates to pixel coordinates
     */
    hexToPixel(q, r) {
        const x = this.hexSize * (3/2 * q);
        const y = this.hexSize * (Math.sqrt(3)/2 * q + Math.sqrt(3) * r);
        return {
            x: x + this.offsetX + this.canvas.width / 2,
            y: y + this.offsetY + this.canvas.height / 2
        };
    }

    /**
     * Convert pixel coordinates to axial hex coordinates
     */
    pixelToHex(x, y) {
        const relX = x - this.offsetX - this.canvas.width / 2;
        const relY = y - this.offsetY - this.canvas.height / 2;

        const q = (2/3 * relX) / this.hexSize;
        const r = (-1/3 * relX + Math.sqrt(3)/3 * relY) / this.hexSize;

        return this.hexRound(q, r);
    }

    /**
     * Round fractional hex coordinates
     */
    hexRound(q, r) {
        const s = -q - r;

        let rq = Math.round(q);
        let rr = Math.round(r);
        let rs = Math.round(s);

        const qDiff = Math.abs(rq - q);
        const rDiff = Math.abs(rr - r);
        const sDiff = Math.abs(rs - s);

        if (qDiff > rDiff && qDiff > sDiff) {
            rq = -rr - rs;
        } else if (rDiff > sDiff) {
            rr = -rq - rs;
        }

        return {q: rq, r: rr};
    }

    /**
     * Update game state and render
     */
    update(gameState) {
        this.gameState = gameState;
        this.render();
    }

    /**
     * Main render function
     */
    render() {
        if (!this.gameState) return;

        // Clear canvas
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Create hex lookup for quick access
        const hexMap = {};
        this.gameState.map.hexes.forEach(hex => {
            hexMap[`${hex.q},${hex.r}`] = hex;
        });

        // Draw hexes (terrain)
        this.gameState.map.hexes.forEach(hex => {
            const pixel = this.hexToPixel(hex.q, hex.r);

            // Draw terrain
            spriteManager.drawTerrain(this.ctx, hex.terrain, pixel.x, pixel.y, this.hexSize);

            // Draw grid
            spriteManager.drawHexOutline(this.ctx, pixel.x, pixel.y, this.hexSize);
        });

        // Draw highlighted hexes
        this.highlightedHexes.forEach(({q, r, color}) => {
            const pixel = this.hexToPixel(q, r);
            spriteManager.drawHexOutline(this.ctx, pixel.x, pixel.y, this.hexSize, color, 3);
        });

        // Draw cities
        this.gameState.cities.forEach(city => {
            const pixel = this.hexToPixel(city.position[0], city.position[1]);
            spriteManager.drawCity(this.ctx, city.owner, pixel.x, pixel.y, this.hexSize);
        });

        // Draw units
        this.gameState.units.forEach(unit => {
            const pixel = this.hexToPixel(unit.position[0], unit.position[1]);
            spriteManager.drawUnit(this.ctx, unit.type, unit.owner, pixel.x, pixel.y, this.hexSize);

            // Draw health bar
            this.drawHealthBar(pixel.x, pixel.y, unit.health, unit.stats.max_health);
        });

        // Draw selection
        if (this.selectedHex) {
            const pixel = this.hexToPixel(this.selectedHex.q, this.selectedHex.r);
            spriteManager.drawHexOutline(this.ctx, pixel.x, pixel.y, this.hexSize, '#FFFF00', 4);
        }
    }

    /**
     * Draw health bar above unit
     */
    drawHealthBar(x, y, health, maxHealth) {
        const barWidth = 30;
        const barHeight = 4;
        const barY = y - this.hexSize - 5;

        // Background
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(x - barWidth / 2, barY, barWidth, barHeight);

        // Health
        const healthPercent = health / maxHealth;
        const healthColor = healthPercent > 0.5 ? '#00FF00' : healthPercent > 0.25 ? '#FFFF00' : '#FF0000';

        this.ctx.fillStyle = healthColor;
        this.ctx.fillRect(x - barWidth / 2, barY, barWidth * healthPercent, barHeight);

        // Border
        this.ctx.strokeStyle = '#FFFFFF';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(x - barWidth / 2, barY, barWidth, barHeight);
    }

    /**
     * Set selected hex
     */
    selectHex(q, r) {
        this.selectedHex = {q, r};
    }

    /**
     * Clear selection
     */
    clearSelection() {
        this.selectedHex = null;
        this.highlightedHexes = [];
    }

    /**
     * Highlight hexes
     */
    highlightHexes(hexes, color = '#00FF00') {
        this.highlightedHexes = hexes.map(hex => ({...hex, color}));
    }
}
