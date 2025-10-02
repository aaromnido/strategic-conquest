# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Strategic Conquest Clone - A turn-based strategy game inspired by the classic Mac game Strategic Conquest. Web-based implementation with Python/Flask backend and vanilla JavaScript frontend featuring hexagonal grid-based gameplay, unit management, city production, combat system, and AI opponent.

**Visual Style:** Retro 16-bit pixel art aesthetic with limited 16-color palette.

## Technology Stack

- **Backend:** Python 3.10+ with Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), Canvas API
- **Data:** JSON for game state and save files
- **Communication:** REST API with JSON payloads

## Project Structure

```
strategic-conquest/
├── server/
│   ├── app.py                 # Flask entry point
│   ├── config.py              # Configuration
│   ├── routes/
│   │   └── game_routes.py     # API endpoints
│   ├── engine/
│   │   ├── game.py            # Game controller
│   │   ├── map.py             # Hex grid and map generation
│   │   ├── units.py           # Unit management
│   │   ├── combat.py          # Combat resolution
│   │   ├── production.py      # City production
│   │   └── ai.py              # AI opponent
│   ├── models/
│   │   ├── game_state.py      # Game state data model
│   │   ├── unit.py            # Unit data model
│   │   ├── city.py            # City data model
│   │   └── player.py          # Player data model
│   └── utils/
│       ├── hex_utils.py       # Hexagonal grid math
│       └── save_load.py       # Persistence
├── static/
│   ├── js/
│   │   ├── main.js            # Main game loop
│   │   ├── renderer.js        # Canvas rendering
│   │   ├── input.js           # User input
│   │   ├── api.js             # API client
│   │   └── sprites.js         # Sprite management
│   ├── css/
│   │   ├── main.css           # Layout
│   │   └── retro.css          # Retro theme
│   └── assets/
│       ├── sprites/           # Unit/tile sprites
│       └── ui/                # UI elements
├── templates/
│   └── index.html             # Main page
└── saves/                     # Saved games
```

## Development Commands

**Setup:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Run Development Server:**
```bash
python server/app.py
# Or with Flask:
flask --app server/app run --debug
```

**Run Tests:**
```bash
pytest                          # All tests
pytest server/tests/test_hex.py # Specific test file
pytest -k "test_combat"         # Tests matching pattern
```

**Run Single Test:**
```bash
pytest server/tests/test_combat.py::test_resolve_combat -v
```

## Core Architecture Concepts

### Hexagonal Grid System

The game uses **axial coordinates (q, r)** for hexagonal grid representation:
- `q`: column (diagonal left-right)
- `r`: row (diagonal top-bottom)

**Critical hex operations** are in `server/utils/hex_utils.py`:
- Distance calculation between hexes
- Finding neighbors (6 directions)
- Range/area calculations
- Coordinate conversion to/from screen pixels

### Game State Flow

1. **Client initiates action** → POST to API endpoint
2. **Backend validates** → Game engine processes
3. **State updated** → Serialized to JSON
4. **Response sent** → Frontend updates UI

All game logic resides server-side to prevent cheating. Client only handles rendering and input.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/game/new` | POST | Start new game |
| `/api/game/state` | GET | Get current state |
| `/api/game/move` | POST | Move unit |
| `/api/game/attack` | POST | Attack with unit |
| `/api/game/produce` | POST | Build unit in city |
| `/api/game/end-turn` | POST | End player turn, trigger AI |
| `/api/game/save` | POST | Save game |
| `/api/game/load` | POST | Load game |

### Canvas Rendering Architecture

Frontend uses **multi-layer rendering** approach:
1. Base layer: Terrain tiles
2. Overlay: Grid lines, highlights
3. Unit layer: Units and cities
4. UI layer: Selection indicators

**Critical for pixel art:** `ctx.imageSmoothingEnabled = false` to maintain crisp pixels.

### AI Decision Pipeline

AI in `server/engine/ai.py` follows this sequence:
1. Assess situation (count units, cities, resources)
2. Set strategic priorities (expand/defend/attack)
3. Production decisions (build units)
4. Movement planning (pathfinding)
5. Combat decisions (target selection)

AI uses rule-based logic with difficulty levels (Easy/Medium/Hard).

### Data Models

All models use Python dataclasses with type hints and are JSON-serializable:
- `GameState`: Complete game state snapshot
- `Unit`: Individual unit with position, health, stats
- `City`: Production center with owner, capacity
- `Player`: Resources, owned units/cities

### Turn Structure

1. **Player Phase:**
   - Production (build units)
   - Movement (move units)
   - Combat (attack enemies)
   - End turn

2. **AI Phase:** (automatic after player ends turn)
   - AI executes all decisions
   - State updated
   - Control returns to player

3. **Turn End Processing:**
   - Reset unit action flags
   - Process city production
   - Generate resources
   - Check victory conditions

## Code Style

- **Python:** Follow PEP 8, use type hints, write docstrings
- **JavaScript:** ES6+ features, avoid jQuery/frameworks
- **Comments:** Explain WHY, not WHAT (code should be self-documenting)
- **Functions:** Keep small and focused, single responsibility

## Visual Design Requirements

- **Pixel art sprites:** 16x16 or 32x32 PNG
- **16-color palette maximum**
- **Player color coding:**
  - Player 1 (Human): Blue (#0000FF)
  - Player 2 (AI): Red (#FF0000)
  - Neutral: Gray (#808080)
- **Retro UI:** Pixel fonts (Press Start 2P), chunky borders

## Important Implementation Notes

### Hexagonal Grid Math
Don't reinvent the wheel - hexagonal coordinate math is complex. Reference `hex_utils.py` for all hex calculations. Uses axial coordinate system with standard conversions.

### Combat Resolution
Combat in `combat.py` uses formula:
```
strength = base_strength + terrain_modifier + random_factor
damage = max(0, attacker_strength - defender_strength)
```

### AI Pathfinding
Simple greedy pathfinding initially. For improvements, use A* with hex distance heuristic.

### Canvas Performance
- Cache sprites after first load
- Use integer-only positioning
- Minimize full redraws (only redraw changed areas if possible)
- Target 60 FPS

### Save/Load System
Game state serializes to JSON with all necessary data to reconstruct exact game state. Validate loaded data for integrity.

## Testing Approach

- **Unit tests:** Core game logic (hex math, combat, movement validation)
- **Integration tests:** API endpoints
- **Manual testing:** Frontend rendering, full game playthrough
- **AI testing:** Play against AI to validate behavior

## Development Phases

The project follows a 10-phase development plan (see `.claude/plan.md`):
1. Project Setup
2. Core Map System (hexagonal grid)
3. Unit System
4. City & Production
5. Combat System
6. Turn System & Game Flow
7. AI Opponent
8. Save/Load
9. UI/UX Polish
10. Testing & Deployment

Complete architectural details in `.claude/architecture.md` and requirements in `.claude/PRD.md`.
