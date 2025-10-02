"""Map and terrain system."""

import random
from typing import Dict, Tuple, List, Optional
from server.utils.hex_utils import hex_neighbors

class TerrainType:
    """Terrain type constants."""
    WATER = 'water'
    LAND = 'land'
    FOREST = 'forest'
    MOUNTAIN = 'mountain'

class Hex:
    """Represents a single hex tile."""

    def __init__(self, q: int, r: int, terrain: str = TerrainType.LAND):
        self.q = q
        self.r = r
        self.terrain = terrain
        self.unit_id: Optional[str] = None
        self.city_id: Optional[str] = None

    @property
    def position(self) -> Tuple[int, int]:
        """Get position as tuple."""
        return (self.q, self.r)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'q': self.q,
            'r': self.r,
            'terrain': self.terrain,
            'unit_id': self.unit_id,
            'city_id': self.city_id
        }

class HexMap:
    """Hexagonal grid map."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self._generate_map()

    def _generate_map(self):
        """Generate the map with terrain."""
        # Create hexes in offset coordinates and convert to axial
        for row in range(self.height):
            for col in range(self.width):
                # Convert offset to axial coordinates
                q = col - (row - (row & 1)) // 2
                r = row
                self.hexes[(q, r)] = Hex(q, r)

        # Generate terrain
        self._generate_terrain()

    def _generate_terrain(self):
        """Generate terrain using simple noise."""
        positions = list(self.hexes.keys())

        # Generate water (coastline)
        num_water = int(len(positions) * 0.2)
        water_seeds = random.sample(positions, min(5, len(positions)))

        for seed in water_seeds:
            self.hexes[seed].terrain = TerrainType.WATER

            # Spread water
            spread_positions = [seed]
            for _ in range(num_water // len(water_seeds)):
                if not spread_positions:
                    break

                pos = random.choice(spread_positions)
                neighbors = [n for n in hex_neighbors(pos) if n in self.hexes]

                if neighbors:
                    next_pos = random.choice(neighbors)
                    if self.hexes[next_pos].terrain != TerrainType.WATER:
                        self.hexes[next_pos].terrain = TerrainType.WATER
                        spread_positions.append(next_pos)

        # Generate forests
        land_positions = [pos for pos, h in self.hexes.items()
                         if h.terrain == TerrainType.LAND]
        num_forests = int(len(land_positions) * 0.15)

        for pos in random.sample(land_positions, min(num_forests, len(land_positions))):
            self.hexes[pos].terrain = TerrainType.FOREST

        # Generate mountains
        remaining_land = [pos for pos, h in self.hexes.items()
                         if h.terrain == TerrainType.LAND]
        num_mountains = int(len(remaining_land) * 0.1)

        for pos in random.sample(remaining_land, min(num_mountains, len(remaining_land))):
            self.hexes[pos].terrain = TerrainType.MOUNTAIN

    def get_hex(self, position: Tuple[int, int]) -> Optional[Hex]:
        """Get hex at position."""
        return self.hexes.get(position)

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if position is on the map."""
        return position in self.hexes

    def is_passable(self, position: Tuple[int, int], unit_type: str) -> bool:
        """Check if unit can move to position."""
        hex_tile = self.get_hex(position)
        if not hex_tile:
            return False

        # Air units can go anywhere
        if unit_type in ['fighter', 'bomber']:
            return True

        # Naval units need water
        if unit_type in ['transport', 'destroyer']:
            return hex_tile.terrain == TerrainType.WATER

        # Ground units can't enter water
        if unit_type in ['infantry', 'tank']:
            return hex_tile.terrain != TerrainType.WATER

        return True

    def get_defense_modifier(self, position: Tuple[int, int]) -> int:
        """Get terrain defense bonus."""
        hex_tile = self.get_hex(position)
        if not hex_tile:
            return 0

        modifiers = {
            TerrainType.FOREST: 1,
            TerrainType.MOUNTAIN: 2,
            TerrainType.LAND: 0,
            TerrainType.WATER: 0
        }

        return modifiers.get(hex_tile.terrain, 0)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'width': self.width,
            'height': self.height,
            'hexes': [hex.to_dict() for hex in self.hexes.values()]
        }

    @staticmethod
    def from_dict(data: dict) -> 'HexMap':
        """Create HexMap from dictionary."""
        hex_map = HexMap.__new__(HexMap)
        hex_map.width = data['width']
        hex_map.height = data['height']
        hex_map.hexes = {}

        for hex_data in data['hexes']:
            q, r = hex_data['q'], hex_data['r']
            hex_tile = Hex(q, r, hex_data['terrain'])
            hex_tile.unit_id = hex_data.get('unit_id')
            hex_tile.city_id = hex_data.get('city_id')
            hex_map.hexes[(q, r)] = hex_tile

        return hex_map
