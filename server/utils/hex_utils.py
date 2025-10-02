"""Hexagonal grid utilities using axial coordinates."""

import math
from typing import Tuple, List

# Axial directions: E, NE, NW, W, SW, SE
HEX_DIRECTIONS = [
    (1, 0), (1, -1), (0, -1),
    (-1, 0), (-1, 1), (0, 1)
]

def hex_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculate distance between two hexes in axial coordinates."""
    q1, r1 = a
    q2, r2 = b
    return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2

def hex_neighbor(hex_pos: Tuple[int, int], direction: int) -> Tuple[int, int]:
    """Get neighbor hex in given direction (0-5)."""
    q, r = hex_pos
    dq, dr = HEX_DIRECTIONS[direction % 6]
    return (q + dq, r + dr)

def hex_neighbors(hex_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Get all 6 neighbors of a hex."""
    return [hex_neighbor(hex_pos, i) for i in range(6)]

def hex_in_range(center: Tuple[int, int], radius: int) -> List[Tuple[int, int]]:
    """Get all hexes within given radius of center hex."""
    results = []
    q, r = center

    for dq in range(-radius, radius + 1):
        for dr in range(max(-radius, -dq - radius), min(radius, -dq + radius) + 1):
            results.append((q + dq, r + dr))

    return results

def hex_to_pixel(q: int, r: int, size: int) -> Tuple[float, float]:
    """Convert axial hex coordinates to pixel coordinates.

    Args:
        q: q coordinate (column)
        r: r coordinate (row)
        size: hex size (distance from center to vertex)

    Returns:
        (x, y) pixel coordinates
    """
    x = size * (3/2 * q)
    y = size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return (x, y)

def pixel_to_hex(x: float, y: float, size: int) -> Tuple[int, int]:
    """Convert pixel coordinates to axial hex coordinates.

    Args:
        x: pixel x
        y: pixel y
        size: hex size

    Returns:
        (q, r) axial coordinates
    """
    q = (2/3 * x) / size
    r = (-1/3 * x + math.sqrt(3)/3 * y) / size

    return hex_round(q, r)

def hex_round(q: float, r: float) -> Tuple[int, int]:
    """Round fractional hex coordinates to nearest hex."""
    s = -q - r

    rq = round(q)
    rr = round(r)
    rs = round(s)

    q_diff = abs(rq - q)
    r_diff = abs(rr - r)
    s_diff = abs(rs - s)

    if q_diff > r_diff and q_diff > s_diff:
        rq = -rr - rs
    elif r_diff > s_diff:
        rr = -rq - rs

    return (rq, rr)

def hex_line(a: Tuple[int, int], b: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Get hexes along line from a to b."""
    distance = hex_distance(a, b)
    if distance == 0:
        return [a]

    results = []
    for i in range(distance + 1):
        t = i / distance
        q = a[0] * (1 - t) + b[0] * t
        r = a[1] * (1 - t) + b[1] * t
        results.append(hex_round(q, r))

    return results
