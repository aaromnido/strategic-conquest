# Technical Architecture
## Strategic Conquest Clone

### 1. Technology Stack

#### 1.1 Backend
- **Language:** Python 3.10+
- **Web Framework:** Flask (lightweight, suitable for game server)
- **Game Logic:** Pure Python (no game engine dependencies)
- **Data Storage:** JSON files for save/load (SQLite optional for future)

#### 1.2 Frontend
- **HTML5:** Structure and canvas element for rendering
- **CSS3:** Styling and retro UI theming
- **JavaScript (Vanilla ES6+):** Game client, rendering, user interaction
- **Canvas API:** 2D rendering for game map and sprites

#### 1.3 Communication
- **REST API:** Flask endpoints for game state management
- **JSON:** Data exchange format
- **WebSocket (Optional Phase 2):** Real-time updates for future multiplayer

### 2. Architecture Overview

```
┌─────────────────────────────────────────┐
│           Web Browser (Client)          │
│  ┌────────────────────────────────────┐ │
│  │  HTML/CSS UI Layer                 │ │
│  │  - Game controls                   │ │
│  │  - Info panels                     │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  JavaScript Game Client            │ │
│  │  - Rendering engine (Canvas)       │ │
│  │  - Event handling                  │ │
│  │  - State management               │ │
│  │  - API communication              │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    ↕ HTTP/JSON
┌─────────────────────────────────────────┐
│         Python Flask Server             │
│  ┌────────────────────────────────────┐ │
│  │  REST API Endpoints                │ │
│  │  - /api/game/new                   │ │
│  │  - /api/game/state                 │ │
│  │  - /api/game/move                  │ │
│  │  - /api/game/attack                │ │
│  │  - /api/game/produce               │ │
│  │  - /api/game/end-turn              │ │
│  │  - /api/game/save                  │ │
│  │  - /api/game/load                  │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Game Engine (Python)              │ │
│  │  - Game state manager              │ │
│  │  - Turn processor                  │ │
│  │  - Combat resolver                 │ │
│  │  - Map generator                   │ │
│  │  - AI engine                       │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Data Layer                        │ │
│  │  - Save/Load manager               │ │
│  │  - JSON persistence                │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 3. Backend Architecture (Python/Flask)

#### 3.1 Project Structure
```
strategic-conquest/
├── server/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── routes/
│   │   └── game_routes.py     # API endpoints
│   ├── engine/
│   │   ├── game.py            # Main game controller
│   │   ├── map.py             # Map and hex grid logic
│   │   ├── units.py           # Unit classes and logic
│   │   ├── combat.py          # Combat resolution
│   │   ├── production.py      # Unit production system
│   │   └── ai.py              # AI opponent logic
│   ├── models/
│   │   ├── game_state.py      # Game state data model
│   │   ├── unit.py            # Unit data model
│   │   ├── city.py            # City data model
│   │   └── player.py          # Player data model
│   └── utils/
│       ├── hex_utils.py       # Hexagonal grid calculations
│       └── save_load.py       # Persistence utilities
├── static/
│   ├── js/
│   │   ├── main.js            # Main application logic
│   │   ├── renderer.js        # Canvas rendering
│   │   ├── input.js           # User input handling
│   │   ├── api.js             # API client
│   │   └── sprites.js         # Sprite management
│   ├── css/
│   │   ├── main.css           # Main styles
│   │   └── retro.css          # Retro theme
│   └── assets/
│       ├── sprites/           # Unit and tile sprites (PNG)
│       └── ui/                # UI elements
├── templates/
│   └── index.html             # Main game page
├── saves/                     # Saved games (JSON)
├── requirements.txt
└── README.md
```

#### 3.2 Core Python Modules

**Game Engine (`engine/game.py`)**
- `GameController`: Main game loop coordinator
- `initialize_game()`: Create new game instance
- `process_turn()`: Execute player/AI turn
- `check_victory()`: Evaluate win conditions

**Map System (`engine/map.py`)**
- `HexMap`: Hexagonal grid map
- `Hex`: Individual hex tile (terrain, occupant)
- `generate_map()`: Procedural map generation
- `get_neighbors()`: Adjacent hex calculation

**Unit System (`engine/units.py`)**
- `Unit` (base class): Common unit attributes
- `Infantry`, `Tank`, `Fighter`, etc.: Specific unit types
- `move_unit()`: Movement logic with path validation
- `can_attack()`: Attack range/eligibility check

**Combat System (`engine/combat.py`)**
- `resolve_combat()`: Combat calculation
- `calculate_strength()`: Factor in terrain, unit stats
- `apply_damage()`: Update unit health/elimination

**AI System (`engine/ai.py`)**
- `AIPlayer`: AI controller
- `evaluate_board()`: Strategic assessment
- `decide_production()`: Build decisions
- `decide_moves()`: Movement planning
- `decide_attacks()`: Target selection

**Data Models (`models/`)**
- JSON-serializable dataclasses for game state
- Type hints for all attributes
- Validation methods

#### 3.3 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/game/new` | POST | Start new game |
| `/api/game/state` | GET | Get current game state |
| `/api/game/move` | POST | Move unit |
| `/api/game/attack` | POST | Attack with unit |
| `/api/game/produce` | POST | Build unit in city |
| `/api/game/end-turn` | POST | End player turn, trigger AI |
| `/api/game/save` | POST | Save game to file |
| `/api/game/load` | POST | Load game from file |

**Request/Response Format (JSON)**
```json
// Move Request
{
  "unit_id": "unit_123",
  "target_hex": {"q": 5, "r": 3}
}

// Game State Response
{
  "turn": 15,
  "current_player": "player1",
  "map": [...],
  "units": [...],
  "cities": [...],
  "resources": {"player1": 500, "player2": 450}
}
```

### 4. Frontend Architecture (JavaScript/HTML/CSS)

#### 4.1 JavaScript Modules

**Main Application (`main.js`)**
- Initialize game on page load
- Coordinate between modules
- Handle game flow

**Renderer (`renderer.js`)**
- Canvas-based rendering engine
- Draw hexagonal map grid
- Render units, cities, terrain
- Handle zoom and pan
- Pixel art scaling (no anti-aliasing)

**Input Handler (`input.js`)**
- Mouse click detection on hex grid
- Unit selection
- Movement target selection
- UI button handling

**API Client (`api.js`)**
- Wrapper for fetch() calls to Flask API
- Error handling
- Loading states

**Sprite Manager (`sprites.js`)**
- Load and cache sprite images
- Pixel art sprites (16x16 or 32x32)
- Color palette management

#### 4.2 Rendering Strategy

**Canvas Layers:**
1. **Base layer:** Terrain tiles
2. **Overlay layer:** Grid lines, highlights
3. **Unit layer:** Units and cities
4. **UI layer:** Selection indicators, info tooltips

**Coordinate Systems:**
- **Screen coordinates:** Canvas pixels
- **Hex coordinates:** Axial (q, r) system
- Conversion functions between systems

**Pixel Art Rendering:**
- Disable image smoothing: `ctx.imageSmoothingEnabled = false`
- Integer-only positioning for crisp pixels
- Limited color palette (CSS custom properties)

#### 4.3 HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Strategic Conquest</title>
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="/static/css/retro.css">
</head>
<body>
    <div id="game-container">
        <div id="top-bar">
            <!-- Turn info, resources -->
        </div>
        <div id="main-game">
            <canvas id="game-canvas"></canvas>
            <div id="side-panel">
                <!-- Unit/city info, production menu -->
            </div>
        </div>
        <div id="bottom-bar">
            <!-- End turn button, menu -->
        </div>
    </div>
    <script src="/static/js/api.js"></script>
    <script src="/static/js/sprites.js"></script>
    <script src="/static/js/renderer.js"></script>
    <script src="/static/js/input.js"></script>
    <script src="/static/js/main.js"></script>
</body>
</html>
```

#### 4.4 CSS Styling

**Retro Theme:**
- Pixel font (e.g., Press Start 2P from Google Fonts)
- Chunky borders and buttons
- Limited color palette (16 colors)
- CRT scanline effect (optional)

**Color Palette:**
```css
:root {
    --color-bg: #000000;
    --color-player1: #0000FF;
    --color-player2: #FF0000;
    --color-neutral: #808080;
    --color-water: #0080FF;
    --color-land: #00FF00;
    --color-mountain: #A0A0A0;
    --color-city: #FFFF00;
}
```

### 5. Data Models

#### 5.1 Game State
```python
@dataclass
class GameState:
    turn: int
    current_player: str
    map: HexMap
    units: List[Unit]
    cities: List[City]
    players: Dict[str, Player]
    game_over: bool
    winner: Optional[str]
```

#### 5.2 Unit
```python
@dataclass
class Unit:
    id: str
    type: str  # infantry, tank, fighter, etc.
    owner: str
    position: Tuple[int, int]  # (q, r) hex coordinates
    health: int
    movement_remaining: int
    has_attacked: bool
```

#### 5.3 City
```python
@dataclass
class City:
    id: str
    name: str
    position: Tuple[int, int]
    owner: Optional[str]
    production_capacity: int
    current_production: Optional[str]
    production_progress: int
```

### 6. Hexagonal Grid System

**Axial Coordinates (q, r):**
- `q`: column (diagonal left-right)
- `r`: row (diagonal top-bottom)

**Key Operations:**
- Distance: `(abs(q1-q2) + abs(q1+r1-q2-r2) + abs(r1-r2)) / 2`
- Neighbors: 6 directions `[(+1,0), (+1,-1), (0,-1), (-1,0), (-1,+1), (0,+1)]`
- Line drawing: Lerp in cube coordinates
- Range: All hexes within N steps

### 7. AI Architecture

**Decision Pipeline:**
1. **Assess situation:** Count units, cities, resources
2. **Set priorities:** Expand, defend, or attack
3. **Production:** Build units based on strategy
4. **Movement:** Move units toward objectives
5. **Combat:** Attack vulnerable targets

**Simple Rule-Based AI:**
- If cities < 3: prioritize expansion
- If enemy nearby: build defensive units
- If strong army: attack enemy cities
- Always protect owned cities

**Difficulty Levels:**
- Easy: Random moves with basic logic
- Medium: Strategic priorities, some planning
- Hard: Optimal decisions, aggressive tactics

### 8. Performance Considerations

- **Client-side rendering:** 60 FPS target
- **API response time:** < 200ms per request
- **AI turn time:** < 2 seconds for decision making
- **Memory:** Efficient sprite caching
- **Map size limit:** 50x50 hexes maximum

### 9. Security & Validation

- Input validation on all API endpoints
- Game state validation before processing moves
- Save file integrity checks
- No client-side game logic (prevent cheating)

### 10. Deployment

**Development:**
- Flask development server
- Hot reload for frontend assets

**Production:**
- Gunicorn WSGI server
- Nginx reverse proxy
- Static file serving via CDN (optional)
- Docker containerization (optional)

### 11. Testing Strategy

**Backend:**
- Unit tests for game logic (pytest)
- Integration tests for API endpoints
- AI behavior tests

**Frontend:**
- Manual testing for rendering
- Input handling verification
- Cross-browser compatibility (Chrome, Firefox, Safari)

### 12. Future Technical Enhancements

- WebSocket for real-time multiplayer
- Progressive Web App (PWA) for offline play
- SQLite for game history and statistics
- Replay system for game recordings
- Advanced AI using minimax or Monte Carlo Tree Search
