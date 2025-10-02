"""Main game controller."""

import random
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from server.engine.map import HexMap, TerrainType
from server.models.unit import Unit, UNIT_STATS
from server.models.city import City
from server.engine.combat import resolve_combat, can_attack
from server.utils.hex_utils import hex_distance, hex_neighbors
from server.config import Config

class GameController:
    """Main game state and logic controller."""

    def __init__(self, width: int = 30, height: int = 20):
        self.turn = 1
        self.current_player = 'player1'
        self.map = HexMap(width, height)
        self.units: Dict[str, Unit] = {}
        self.cities: Dict[str, City] = {}
        self.resources = {'player1': 200, 'player2': 200}
        self.game_over = False
        self.winner: Optional[str] = None

        self._unit_counter = 0
        self._city_counter = 0

        # Initialize game
        self._place_starting_cities()
        self._place_starting_units()

    def _place_starting_cities(self):
        """Place starting cities for both players."""
        land_hexes = [pos for pos, hex_tile in self.map.hexes.items()
                     if hex_tile.terrain == TerrainType.LAND]

        if len(land_hexes) < 4:
            # Fallback if not enough land
            land_hexes = list(self.map.hexes.keys())[:4]

        # Find positions far apart
        random.shuffle(land_hexes)

        # Player 1 starting cities (2 cities)
        for i in range(2):
            if i < len(land_hexes):
                pos = land_hexes[i]
                self._create_city(pos, 'player1', f'City-P1-{i+1}')

        # Player 2 starting cities (2 cities) - from the other end
        for i in range(2):
            idx = -(i + 1)
            if abs(idx) <= len(land_hexes):
                pos = land_hexes[idx]
                self._create_city(pos, 'player2', f'City-P2-{i+1}')

    def _place_starting_units(self):
        """Place starting units near cities."""
        for city in self.cities.values():
            if city.owner:
                # Place 2 infantry near each city
                neighbors = hex_neighbors(city.position)
                placed = 0

                for neighbor_pos in neighbors:
                    if placed >= 2:
                        break

                    hex_tile = self.map.get_hex(neighbor_pos)
                    if hex_tile and hex_tile.terrain != TerrainType.WATER and not hex_tile.unit_id:
                        self._create_unit('infantry', city.owner, neighbor_pos)
                        placed += 1

    def _create_unit(self, unit_type: str, owner: str, position: Tuple[int, int]) -> Unit:
        """Create a new unit."""
        self._unit_counter += 1
        unit_id = f"unit_{self._unit_counter}"

        stats = UNIT_STATS[unit_type]
        unit = Unit(
            id=unit_id,
            type=unit_type,
            owner=owner,
            position=position,
            health=stats['max_health'],
            movement_remaining=stats['movement']
        )

        self.units[unit_id] = unit

        # Place on map
        hex_tile = self.map.get_hex(position)
        if hex_tile:
            hex_tile.unit_id = unit_id

        return unit

    def _create_city(self, position: Tuple[int, int], owner: Optional[str], name: str):
        """Create a new city."""
        self._city_counter += 1
        city_id = f"city_{self._city_counter}"

        city = City(
            id=city_id,
            name=name,
            position=position,
            owner=owner,
            production_capacity=10,
            current_production=None,
            production_progress=0
        )

        self.cities[city_id] = city

        # Place on map
        hex_tile = self.map.get_hex(position)
        if hex_tile:
            hex_tile.city_id = city_id

    def move_unit(self, unit_id: str, target: Tuple[int, int]) -> Dict:
        """Move a unit to target position."""
        unit = self.units.get(unit_id)

        if not unit:
            return {'success': False, 'message': 'Unit not found'}

        if unit.owner != self.current_player:
            return {'success': False, 'message': 'Not your unit'}

        if not unit.can_move():
            return {'success': False, 'message': 'No movement remaining'}

        # Check distance
        distance = hex_distance(unit.position, target)
        if distance > unit.movement_remaining:
            return {'success': False, 'message': 'Target too far'}

        # Check if target is passable
        if not self.map.is_passable(target, unit.type):
            return {'success': False, 'message': 'Cannot move there'}

        # Check if target is occupied
        target_hex = self.map.get_hex(target)
        if target_hex and target_hex.unit_id and target_hex.unit_id != unit_id:
            return {'success': False, 'message': 'Hex occupied'}

        # Remove from old position
        old_hex = self.map.get_hex(unit.position)
        if old_hex:
            old_hex.unit_id = None

        # Move unit
        unit.position = target
        unit.movement_remaining -= distance

        # Place at new position
        if target_hex:
            target_hex.unit_id = unit_id

        # Check for city capture
        if target_hex and target_hex.city_id:
            city = self.cities.get(target_hex.city_id)
            if city and city.owner != unit.owner and UNIT_STATS[unit.type].get('can_capture'):
                city.owner = unit.owner
                return {'success': True, 'message': f'Captured {city.name}!', 'captured_city': city.id}

        return {'success': True, 'message': 'Unit moved'}

    def attack(self, attacker_id: str, defender_id: str) -> Dict:
        """Attack another unit."""
        attacker = self.units.get(attacker_id)
        defender = self.units.get(defender_id)

        if not attacker or not defender:
            return {'success': False, 'message': 'Unit not found'}

        if attacker.owner != self.current_player:
            return {'success': False, 'message': 'Not your unit'}

        distance = hex_distance(attacker.position, defender.position)
        can, reason = can_attack(attacker, defender, distance)

        if not can:
            return {'success': False, 'message': reason}

        # Get terrain modifier
        terrain_mod = self.map.get_defense_modifier(defender.position)

        # Resolve combat
        result = resolve_combat(attacker, defender, terrain_mod)

        # Remove destroyed units
        if defender.health <= 0:
            defender_hex = self.map.get_hex(defender.position)
            if defender_hex:
                defender_hex.unit_id = None
            del self.units[defender_id]

        if attacker.health <= 0:
            attacker_hex = self.map.get_hex(attacker.position)
            if attacker_hex:
                attacker_hex.unit_id = None
            del self.units[attacker_id]

        return result

    def start_production(self, city_id: str, unit_type: str) -> Dict:
        """Start producing a unit in a city."""
        city = self.cities.get(city_id)

        if not city:
            return {'success': False, 'message': 'City not found'}

        if city.owner != self.current_player:
            return {'success': False, 'message': 'Not your city'}

        if unit_type not in UNIT_STATS:
            return {'success': False, 'message': 'Invalid unit type'}

        city.start_production(unit_type)

        return {'success': True, 'message': f'Started producing {unit_type}'}

    def end_turn(self):
        """End current player's turn."""
        # Process production for current player's cities
        for city in self.cities.values():
            if city.owner == self.current_player:
                completed_unit = city.advance_production()

                if completed_unit:
                    # Find empty neighbor to place unit
                    neighbors = hex_neighbors(city.position)
                    for neighbor in neighbors:
                        hex_tile = self.map.get_hex(neighbor)
                        if hex_tile and not hex_tile.unit_id and self.map.is_passable(neighbor, completed_unit):
                            self._create_unit(completed_unit, city.owner, neighbor)
                            break

        # Generate resources
        player_cities = sum(1 for c in self.cities.values() if c.owner == self.current_player)
        self.resources[self.current_player] += player_cities * 10

        # Switch player
        if self.current_player == 'player1':
            self.current_player = 'player2'
            # Simple AI turn
            self._ai_turn()
            self.current_player = 'player1'
            self.turn += 1
        else:
            self.current_player = 'player1'
            self.turn += 1

        # Reset units
        for unit in self.units.values():
            if unit.owner == self.current_player:
                unit.reset_turn()

        # Check victory
        self._check_victory()

    def _ai_turn(self):
        """Simple AI turn logic."""
        # AI produces units
        for city in self.cities.values():
            if city.owner == 'player2' and not city.current_production:
                unit_types = ['infantry', 'tank', 'fighter']
                city.start_production(random.choice(unit_types))

        # AI moves and attacks
        ai_units = [u for u in self.units.values() if u.owner == 'player2']

        for unit in ai_units:
            # Try to find enemy units to attack
            enemy_units = [u for u in self.units.values() if u.owner == 'player1']

            if enemy_units:
                # Find closest enemy
                closest = min(enemy_units, key=lambda e: hex_distance(unit.position, e.position))
                distance = hex_distance(unit.position, closest.position)

                # Try to attack if in range
                if distance <= unit.get_stats().get('range', 1) and unit.can_attack():
                    self.current_player = 'player2'
                    self.attack(unit.id, closest.id)
                    self.current_player = 'player1'
                # Otherwise move closer
                elif unit.can_move():
                    # Simple movement towards enemy
                    neighbors = hex_neighbors(unit.position)
                    valid_moves = []

                    for neighbor in neighbors:
                        hex_tile = self.map.get_hex(neighbor)
                        if hex_tile and not hex_tile.unit_id and self.map.is_passable(neighbor, unit.type):
                            new_dist = hex_distance(neighbor, closest.position)
                            if new_dist < distance:
                                valid_moves.append(neighbor)

                    if valid_moves:
                        target = random.choice(valid_moves)
                        self.current_player = 'player2'
                        self.move_unit(unit.id, target)
                        self.current_player = 'player1'

    def _check_victory(self):
        """Check if game is over."""
        player1_cities = sum(1 for c in self.cities.values() if c.owner == 'player1')
        player2_cities = sum(1 for c in self.cities.values() if c.owner == 'player2')

        if player1_cities == 0:
            self.game_over = True
            self.winner = 'player2'
        elif player2_cities == 0:
            self.game_over = True
            self.winner = 'player1'

    def get_state(self) -> Dict:
        """Get current game state."""
        return {
            'turn': self.turn,
            'current_player': self.current_player,
            'map': self.map.to_dict(),
            'units': [unit.to_dict() for unit in self.units.values()],
            'cities': [city.to_dict() for city in self.cities.values()],
            'resources': self.resources,
            'game_over': self.game_over,
            'winner': self.winner
        }

    def save_game(self, filename: str) -> str:
        """Save game to file."""
        save_dir = Config.SAVE_DIR
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(save_dir, f'{filename}_{timestamp}.json')

        with open(filepath, 'w') as f:
            json.dump(self.get_state(), f, indent=2)

        return filepath

    @staticmethod
    def load_game(filename: str) -> 'GameController':
        """Load game from file."""
        save_dir = Config.SAVE_DIR
        filepath = os.path.join(save_dir, filename)

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Reconstruct game controller
        game = GameController.__new__(GameController)
        game.turn = data['turn']
        game.current_player = data['current_player']
        game.map = HexMap.from_dict(data['map'])
        game.units = {u['id']: Unit.from_dict(u) for u in data['units']}
        game.cities = {c['id']: City.from_dict(c) for c in data['cities']}
        game.resources = data['resources']
        game.game_over = data['game_over']
        game.winner = data.get('winner')

        game._unit_counter = len(game.units)
        game._city_counter = len(game.cities)

        return game
