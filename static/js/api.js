/**
 * API client for game server communication
 */

class GameAPI {
    constructor(baseUrl = '/api/game') {
        this.baseUrl = baseUrl;
    }

    async newGame(width = 30, height = 20) {
        const response = await fetch(`${this.baseUrl}/new`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({width, height})
        });
        return await response.json();
    }

    async getState() {
        const response = await fetch(`${this.baseUrl}/state`);
        return await response.json();
    }

    async moveUnit(unitId, targetHex) {
        const response = await fetch(`${this.baseUrl}/move`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({unit_id: unitId, target_hex: targetHex})
        });
        return await response.json();
    }

    async attack(attackerId, defenderId) {
        const response = await fetch(`${this.baseUrl}/attack`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({attacker_id: attackerId, defender_id: defenderId})
        });
        return await response.json();
    }

    async produceUnit(cityId, unitType) {
        const response = await fetch(`${this.baseUrl}/produce`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({city_id: cityId, unit_type: unitType})
        });
        return await response.json();
    }

    async endTurn() {
        const response = await fetch(`${this.baseUrl}/end-turn`, {
            method: 'POST'
        });
        return await response.json();
    }

    async saveGame(filename) {
        const response = await fetch(`${this.baseUrl}/save`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({filename})
        });
        return await response.json();
    }

    async loadGame(filename) {
        const response = await fetch(`${this.baseUrl}/load`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({filename})
        });
        return await response.json();
    }
}

// Global API instance
const gameAPI = new GameAPI();
