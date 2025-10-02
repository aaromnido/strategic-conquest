"""Unit data models."""

from dataclasses import dataclass, asdict
from typing import Tuple, Optional

# Unit type configurations
UNIT_STATS = {
    'infantry': {
        'name': 'Infantry',
        'movement': 2,
        'attack': 3,
        'defense': 4,
        'range': 1,
        'cost': 50,
        'max_health': 10,
        'can_capture': True
    },
    'tank': {
        'name': 'Tank',
        'movement': 3,
        'attack': 8,
        'defense': 6,
        'range': 1,
        'cost': 100,
        'max_health': 15,
        'can_capture': False
    },
    'fighter': {
        'name': 'Fighter',
        'movement': 6,
        'attack': 6,
        'defense': 4,
        'range': 1,
        'cost': 80,
        'max_health': 8,
        'can_capture': False
    },
    'bomber': {
        'name': 'Bomber',
        'movement': 5,
        'attack': 10,
        'defense': 2,
        'range': 1,
        'cost': 120,
        'max_health': 10,
        'can_capture': False
    },
    'transport': {
        'name': 'Transport',
        'movement': 4,
        'attack': 0,
        'defense': 3,
        'range': 0,
        'cost': 70,
        'max_health': 12,
        'can_capture': False
    },
    'destroyer': {
        'name': 'Destroyer',
        'movement': 4,
        'attack': 7,
        'defense': 5,
        'range': 2,
        'cost': 90,
        'max_health': 12,
        'can_capture': False
    }
}

@dataclass
class Unit:
    """Represents a military unit."""
    id: str
    type: str
    owner: str  # 'player1' or 'player2'
    position: Tuple[int, int]  # (q, r) hex coordinates
    health: int
    movement_remaining: int
    has_attacked: bool = False

    def get_stats(self) -> dict:
        """Get unit's base stats."""
        return UNIT_STATS.get(self.type, {})

    def reset_turn(self):
        """Reset unit for new turn."""
        stats = self.get_stats()
        self.movement_remaining = stats.get('movement', 0)
        self.has_attacked = False

    def can_move(self) -> bool:
        """Check if unit can move."""
        return self.movement_remaining > 0

    def can_attack(self) -> bool:
        """Check if unit can attack."""
        return not self.has_attacked and self.health > 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['stats'] = self.get_stats()
        return data

    @staticmethod
    def from_dict(data: dict) -> 'Unit':
        """Create Unit from dictionary."""
        # Convert position from list to tuple if needed
        if isinstance(data['position'], list):
            data['position'] = tuple(data['position'])

        return Unit(
            id=data['id'],
            type=data['type'],
            owner=data['owner'],
            position=data['position'],
            health=data['health'],
            movement_remaining=data['movement_remaining'],
            has_attacked=data.get('has_attacked', False)
        )
