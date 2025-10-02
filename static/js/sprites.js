/**
 * Sprite manager for game graphics
 */

class SpriteManager {
    constructor() {
        this.sprites = {};
        this.loaded = false;
    }

    /**
     * Draw terrain hex
     */
    drawTerrain(ctx, terrain, x, y, size) {
        const colors = {
            'water': '#0080FF',
            'land': '#00FF00',
            'forest': '#008800',
            'mountain': '#A0A0A0'
        };

        ctx.fillStyle = colors[terrain] || '#00FF00';
        this.drawHexagon(ctx, x, y, size);
    }

    /**
     * Draw unit sprite
     */
    drawUnit(ctx, unitType, owner, x, y, size) {
        const playerColors = {
            'player1': '#0000FF',
            'player2': '#FF0000'
        };

        ctx.fillStyle = playerColors[owner] || '#808080';

        // Simple geometric representation
        const symbolSize = size * 0.6;

        switch (unitType) {
            case 'infantry':
                // Triangle (soldier)
                ctx.beginPath();
                ctx.moveTo(x, y - symbolSize / 2);
                ctx.lineTo(x - symbolSize / 2, y + symbolSize / 2);
                ctx.lineTo(x + symbolSize / 2, y + symbolSize / 2);
                ctx.closePath();
                ctx.fill();
                break;

            case 'tank':
                // Rectangle (tank)
                ctx.fillRect(x - symbolSize / 2, y - symbolSize / 2, symbolSize, symbolSize);
                break;

            case 'fighter':
                // Diamond (aircraft)
                ctx.beginPath();
                ctx.moveTo(x, y - symbolSize / 2);
                ctx.lineTo(x + symbolSize / 2, y);
                ctx.lineTo(x, y + symbolSize / 2);
                ctx.lineTo(x - symbolSize / 2, y);
                ctx.closePath();
                ctx.fill();
                break;

            case 'bomber':
                // Larger diamond
                ctx.beginPath();
                ctx.moveTo(x, y - symbolSize * 0.6);
                ctx.lineTo(x + symbolSize * 0.6, y);
                ctx.lineTo(x, y + symbolSize * 0.6);
                ctx.lineTo(x - symbolSize * 0.6, y);
                ctx.closePath();
                ctx.fill();
                break;

            case 'transport':
            case 'destroyer':
                // Ship (trapezoid)
                ctx.beginPath();
                ctx.moveTo(x - symbolSize / 3, y - symbolSize / 2);
                ctx.lineTo(x + symbolSize / 3, y - symbolSize / 2);
                ctx.lineTo(x + symbolSize / 2, y + symbolSize / 2);
                ctx.lineTo(x - symbolSize / 2, y + symbolSize / 2);
                ctx.closePath();
                ctx.fill();
                break;

            default:
                // Circle
                ctx.beginPath();
                ctx.arc(x, y, symbolSize / 2, 0, Math.PI * 2);
                ctx.fill();
        }

        // Add border
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    /**
     * Draw city sprite
     */
    drawCity(ctx, owner, x, y, size) {
        const playerColors = {
            'player1': '#0000FF',
            'player2': '#FF0000',
            'null': '#808080'
        };

        // Building (yellow base)
        ctx.fillStyle = '#FFFF00';
        const buildingSize = size * 0.8;
        ctx.fillRect(x - buildingSize / 2, y - buildingSize / 2, buildingSize, buildingSize);

        // Owner flag on top
        if (owner) {
            ctx.fillStyle = playerColors[owner] || '#808080';
            ctx.fillRect(x - buildingSize / 4, y - buildingSize * 0.7, buildingSize / 2, buildingSize / 4);
        }

        // Border
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.strokeRect(x - buildingSize / 2, y - buildingSize / 2, buildingSize, buildingSize);
    }

    /**
     * Draw hexagon shape
     */
    drawHexagon(ctx, x, y, size) {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 2;
            const hx = x + size * Math.cos(angle);
            const hy = y + size * Math.sin(angle);

            if (i === 0) {
                ctx.moveTo(hx, hy);
            } else {
                ctx.lineTo(hx, hy);
            }
        }
        ctx.closePath();
        ctx.fill();
    }

    /**
     * Draw hex outline
     */
    drawHexOutline(ctx, x, y, size, color = '#4a4a4a', lineWidth = 1) {
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.beginPath();

        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 2;
            const hx = x + size * Math.cos(angle);
            const hy = y + size * Math.sin(angle);

            if (i === 0) {
                ctx.moveTo(hx, hy);
            } else {
                ctx.lineTo(hx, hy);
            }
        }

        ctx.closePath();
        ctx.stroke();
    }
}

// Global sprite manager
const spriteManager = new SpriteManager();
