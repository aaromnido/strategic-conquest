"""Combat resolution system."""

import random
from typing import Dict, Optional
from server.models.unit import Unit, UNIT_STATS

def resolve_combat(attacker: Unit, defender: Unit, terrain_modifier: int = 0) -> Dict:
    """Resolve combat between two units.

    Args:
        attacker: Attacking unit
        defender: Defending unit
        terrain_modifier: Defense bonus from terrain

    Returns:
        Dictionary with combat results
    """
    attacker_stats = attacker.get_stats()
    defender_stats = defender.get_stats()

    # Calculate effective strengths
    attack_power = attacker_stats['attack'] * (attacker.health / attacker_stats['max_health'])
    defense_power = (defender_stats['defense'] + terrain_modifier) * (defender.health / defender_stats['max_health'])

    # Add random factor (dice roll)
    attack_roll = random.randint(1, 6)
    defense_roll = random.randint(1, 6)

    attack_power += attack_roll
    defense_power += defense_roll

    # Calculate damage
    damage_to_defender = max(0, int(attack_power - defense_power / 2))
    damage_to_attacker = max(0, int(defense_power / 2 - attack_power / 3))

    # Apply damage
    defender.health = max(0, defender.health - damage_to_defender)
    attacker.health = max(0, attacker.health - damage_to_attacker)

    # Mark attacker as having attacked
    attacker.has_attacked = True

    result = {
        'success': True,
        'attacker_id': attacker.id,
        'defender_id': defender.id,
        'damage_to_defender': damage_to_defender,
        'damage_to_attacker': damage_to_attacker,
        'attacker_health': attacker.health,
        'defender_health': defender.health,
        'defender_destroyed': defender.health <= 0,
        'attacker_survived': attacker.health > 0
    }

    return result

def can_attack(attacker: Unit, defender: Unit, distance: int) -> tuple[bool, str]:
    """Check if attacker can attack defender.

    Returns:
        (can_attack, reason) tuple
    """
    if attacker.health <= 0:
        return False, "Attacker is destroyed"

    if defender.health <= 0:
        return False, "Defender is destroyed"

    if attacker.owner == defender.owner:
        return False, "Cannot attack own units"

    if not attacker.can_attack():
        return False, "Unit has already attacked this turn"

    attacker_stats = attacker.get_stats()
    attack_range = attacker_stats.get('range', 1)

    if distance > attack_range:
        return False, f"Target out of range (range: {attack_range}, distance: {distance})"

    return True, "OK"
