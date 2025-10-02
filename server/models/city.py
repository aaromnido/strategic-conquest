"""City data model."""

from dataclasses import dataclass, asdict
from typing import Tuple, Optional

@dataclass
class City:
    """Represents a city that produces units."""
    id: str
    name: str
    position: Tuple[int, int]  # (q, r) hex coordinates
    owner: Optional[str]  # 'player1', 'player2', or None for neutral
    production_capacity: int  # Production points per turn
    current_production: Optional[str]  # Unit type being produced
    production_progress: int  # Accumulated production points

    def start_production(self, unit_type: str):
        """Start producing a unit."""
        self.current_production = unit_type
        self.production_progress = 0

    def advance_production(self) -> Optional[str]:
        """Advance production by one turn.

        Returns:
            Unit type if production completed, None otherwise.
        """
        if self.current_production is None:
            return None

        self.production_progress += self.production_capacity

        from server.models.unit import UNIT_STATS
        cost = UNIT_STATS.get(self.current_production, {}).get('cost', 100)

        if self.production_progress >= cost:
            completed_unit = self.current_production
            self.current_production = None
            self.production_progress = 0
            return completed_unit

        return None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'City':
        """Create City from dictionary."""
        # Convert position from list to tuple if needed
        if isinstance(data['position'], list):
            data['position'] = tuple(data['position'])

        return City(
            id=data['id'],
            name=data['name'],
            position=data['position'],
            owner=data.get('owner'),
            production_capacity=data['production_capacity'],
            current_production=data.get('current_production'),
            production_progress=data.get('production_progress', 0)
        )
