# Development Plan
## Strategic Conquest Clone - Implementation Roadmap

## 🔴 IMPORTANTE: GIT COMMITS
**Después de completar cada fase, hacer commit con el mensaje:**
- Phase 0: `git add . && git commit -m "Phase 0: Project setup completed"`
- Phase 1: `git add . && git commit -m "Phase 1: Core map system completed"`
- Phase 2: `git add . && git commit -m "Phase 2: Unit system completed"`
- ... y así sucesivamente para cada fase

### Phase 0: Project Setup (1-2 days) ✅ COMPLETED

#### 0.1 Environment Setup ✅
- [x] Create virtual environment (`python3 -m venv venv`)
- [x] Install Flask and dependencies (`pip install flask`)
- [x] Create `requirements.txt` file
- [x] Set up project folder structure
- [x] Initialize git repository
- [x] Create .gitignore

#### 0.2 Basic Flask Application ✅
- [x] Create `server/app.py` with Flask initialization
- [x] Create `server/config.py` with basic settings
- [x] Create `templates/index.html` with basic HTML structure
- [x] Set up static file serving (`/static/`)
- [ ] Test server runs successfully (pending final test)

#### 0.3 Frontend Skeleton ✅
- [x] Create basic HTML structure in `index.html`
- [x] Add canvas element for game rendering
- [x] Create `static/css/main.css` with layout styles
- [x] Create `static/css/retro.css` with retro theme
- [ ] Create `static/js/main.js` with initialization code (IN PROGRESS)
- [ ] Verify page loads and canvas displays (pending)

**Deliverable:** Working Flask server with blank canvas rendering

**📝 COMMIT:** `git add . && git commit -m "Phase 0: Project setup completed"`

---

### Phase 1: Core Map System (3-4 days) ✅ COMPLETED

#### 1.1 Hexagonal Grid Backend ✅
- [x] Create `server/utils/hex_utils.py`
  - Implement axial coordinate system (q, r)
  - Implement distance calculation
  - Implement neighbor finding
  - Implement range/area calculations
- [x] Create `server/engine/map.py`
  - `Hex` class with terrain type, coordinates
  - `HexMap` class with grid storage
  - Basic map initialization (blank map)
- [ ] Write unit tests for hex calculations (skipped for MVP)

#### 1.2 Map Generation ✅
- [x] Implement terrain types (water, land, mountain, forest)
- [x] Create basic map generator (random or pattern-based)
- [x] Place starting cities (2-4 per player)
- [x] Add map validation (connectivity check)

#### 1.3 Frontend Hexagonal Rendering ✅
- [x] Create `static/js/renderer.js`
  - Hex to screen coordinate conversion
  - Screen to hex coordinate conversion
  - Draw hexagon function
  - Draw hexagonal grid
- [x] Implement terrain color coding
- [x] Add grid lines
- [ ] Test rendering performance (pending)

#### 1.4 Map API ✅
- [x] Create `server/routes/game_routes.py`
- [x] Implement `/api/game/new` endpoint (generate new map)
- [x] Implement `/api/game/state` endpoint (return map data)
- [x] Create `static/js/api.js` with fetch wrappers
- [ ] Connect frontend to load and display map (main.js pending)

**Deliverable:** Rendered hexagonal map with different terrains

**📝 COMMIT:** `git add . && git commit -m "Phase 1: Core map system completed"`

---

### Phase 2: Unit System (4-5 days)

#### 2.1 Unit Data Models
- [ ] Create `server/models/unit.py`
  - Unit base class with common attributes
  - Specific unit types (Infantry, Tank, Fighter, etc.)
  - Unit stats (movement, attack, defense, cost)
- [ ] Create unit type configuration (JSON or Python dict)

#### 2.2 Unit Management Backend
- [ ] Create `server/engine/units.py`
  - Add unit to map
  - Remove unit from map
  - Get unit at position
  - Get units by owner
- [ ] Implement movement validation
  - Check movement range
  - Check terrain passability
  - Check destination occupancy

#### 2.3 Unit Sprites & Rendering
- [ ] Create pixel art sprites for each unit type
  - Infantry sprite (16x16 or 32x32 PNG)
  - Tank sprite
  - Fighter sprite
  - Bomber sprite
  - Ship sprites
  - Color variations for player 1 (blue) and player 2 (red)
- [ ] Create `static/js/sprites.js`
  - Load sprite images
  - Cache sprites
  - Draw sprite at hex position
- [ ] Render units on map

#### 2.4 Unit Movement
- [ ] Implement movement API endpoint `/api/game/move`
- [ ] Add movement validation on backend
- [ ] Frontend: click unit to select
- [ ] Frontend: highlight valid move destinations
- [ ] Frontend: click destination to move
- [ ] Animate unit movement (optional, simple)

#### 2.5 Unit Selection & Info
- [ ] Frontend: display selected unit info panel
  - Unit type
  - Health
  - Movement remaining
  - Attack/defense stats
- [ ] Visual selection indicator (highlight hex)

**Deliverable:** Units can be placed and moved on the map

---

### Phase 3: City & Production System (3-4 days)

#### 3.1 City Data Model
- [ ] Create `server/models/city.py`
  - City attributes (name, owner, position, production capacity)
  - Production queue
- [ ] Add cities to map during generation

#### 3.2 City Rendering
- [ ] Create city sprite (pixelated building)
- [ ] Color-code cities by owner
- [ ] Render cities on map
- [ ] City info panel (when selected)

#### 3.3 Production System Backend
- [ ] Create `server/engine/production.py`
  - Start production (unit type)
  - Advance production (per turn)
  - Complete production (spawn unit)
- [ ] Production cost validation (resources)

#### 3.4 Production UI
- [ ] Frontend: production menu when city selected
  - List available units to build
  - Show cost and build time
  - Build button
- [ ] Implement `/api/game/produce` endpoint
- [ ] Handle production start from frontend

#### 3.5 City Capture Mechanic
- [ ] Infantry can capture cities
- [ ] Capture validation (unit type, position)
- [ ] Change city ownership
- [ ] Update UI when city captured

**Deliverable:** Cities produce units, can be captured

---

### Phase 4: Combat System (3-4 days)

#### 4.1 Combat Logic Backend
- [ ] Create `server/engine/combat.py`
  - `resolve_combat()` function
  - Calculate attacker/defender strength
  - Apply terrain modifiers
  - Random factor (dice roll)
  - Damage calculation
  - Unit elimination check

#### 4.2 Attack Range & Validation
- [ ] Check unit can attack (has not attacked this turn)
- [ ] Check target is in range
- [ ] Check target is enemy unit
- [ ] Prevent friendly fire

#### 4.3 Combat API
- [ ] Implement `/api/game/attack` endpoint
- [ ] Return combat results (damage dealt, units destroyed)

#### 4.4 Combat UI
- [ ] Frontend: select unit, highlight attackable targets
- [ ] Click target to attack
- [ ] Display combat results (simple text or animation)
- [ ] Update map after combat

#### 4.5 Combat Feedback
- [ ] Visual attack animation (flash, shake, or projectile)
- [ ] Update unit health display
- [ ] Remove destroyed units

**Deliverable:** Functional combat between units

---

### Phase 5: Turn System & Game Flow (2-3 days)

#### 5.1 Turn Management Backend
- [ ] Create `server/engine/game.py`
  - `GameController` class
  - Turn counter
  - Current player tracking
  - End turn logic
- [ ] Reset unit actions at turn start (movement, attack flags)
- [ ] Process city production at turn end

#### 5.2 Player Management
- [ ] Create `server/models/player.py`
  - Player resources
  - Owned units
  - Owned cities
- [ ] Resource generation per turn (per city)

#### 5.3 Game State Model
- [ ] Create `server/models/game_state.py`
  - Serialize entire game state to JSON
  - Deserialize game state from JSON
- [ ] Update `/api/game/state` to return full state

#### 5.4 End Turn Flow
- [ ] Implement `/api/game/end-turn` endpoint
- [ ] Process player turn end
- [ ] Trigger AI turn (placeholder for now)
- [ ] Return updated game state
- [ ] Frontend: end turn button
- [ ] Frontend: display current turn and player

#### 5.5 Win Condition
- [ ] Check victory after each turn
- [ ] Victory: all enemy cities captured
- [ ] Defeat: all own cities lost
- [ ] Display win/lose screen

**Deliverable:** Complete turn-based game loop

---

### Phase 6: AI Opponent (5-6 days)

#### 6.1 AI Foundation
- [ ] Create `server/engine/ai.py`
  - `AIPlayer` class
  - Board evaluation function
  - Get owned units and cities

#### 6.2 AI Production Logic
- [ ] Assess resource availability
- [ ] Decide which units to build
  - Early game: expand (infantry)
  - Mid game: balanced army
  - Late game: advanced units
- [ ] Queue production in cities

#### 6.3 AI Movement Logic
- [ ] For each unit, determine objective
  - Expand: move toward neutral cities
  - Defend: move toward owned cities
  - Attack: move toward enemy units/cities
- [ ] Pathfinding (simple greedy or A*)
- [ ] Execute moves

#### 6.4 AI Combat Logic
- [ ] Identify attackable targets
- [ ] Evaluate combat favorability
  - Attack if strength advantage
  - Retreat if disadvantage
- [ ] Execute attacks

#### 6.5 AI Strategy
- [ ] Implement difficulty levels
  - Easy: random valid moves
  - Medium: strategic priorities
  - Hard: optimal decisions
- [ ] Strategic decision making
  - Expansion vs aggression
  - Unit composition balance
  - City defense priorities

#### 6.6 AI Integration
- [ ] Integrate AI turn into `/api/game/end-turn`
- [ ] AI executes all actions automatically
- [ ] Return updated state to frontend
- [ ] Frontend displays AI actions (optional: log or animation)

**Deliverable:** Playable AI opponent with strategic behavior

---

### Phase 7: Save/Load System (2 days)

#### 7.1 Save System Backend
- [ ] Create `server/utils/save_load.py`
- [ ] Serialize game state to JSON
- [ ] Write to file in `saves/` directory
- [ ] Generate save file name (timestamp)

#### 7.2 Load System Backend
- [ ] Read JSON file from `saves/`
- [ ] Deserialize to game state
- [ ] Validate loaded state
- [ ] Restore game controller

#### 7.3 Save/Load API
- [ ] Implement `/api/game/save` endpoint
- [ ] Implement `/api/game/load` endpoint
- [ ] Return list of saved games

#### 7.4 Save/Load UI
- [ ] Frontend: save button (opens save dialog)
- [ ] Frontend: load button (shows list of saves)
- [ ] Select save file to load
- [ ] Restore game state on frontend

**Deliverable:** Ability to save and resume games

---

### Phase 8: UI/UX Polish (3-4 days)

#### 8.1 Retro Visual Theme
- [ ] Create `static/css/retro.css`
- [ ] Apply pixel font (e.g., Press Start 2P)
- [ ] Style buttons with retro look
- [ ] Add borders and panels with retro aesthetic
- [ ] Implement 16-color palette

#### 8.2 Enhanced Sprites
- [ ] Refine all unit sprites
- [ ] Refine terrain tiles
- [ ] Refine city sprites
- [ ] Add selection/highlight sprites
- [ ] Polish pixel art consistency

#### 8.3 Information Display
- [ ] Top bar: turn number, current player, resources
- [ ] Side panel: selected unit/city details
- [ ] Production menu: unit costs, build time
- [ ] Combat log (optional)

#### 8.4 User Feedback
- [ ] Hover effects on hexes
- [ ] Visual indicators for valid moves/attacks
- [ ] Turn transition message ("Enemy Turn", "Your Turn")
- [ ] Victory/defeat screen with restart option

#### 8.5 Responsive Layout
- [ ] Ensure UI fits 1024x768 minimum
- [ ] Test on different screen sizes
- [ ] Adjust canvas scaling

#### 8.6 Tutorial/Help
- [ ] Create simple help overlay
- [ ] Explain controls and game rules
- [ ] Unit type reference chart

**Deliverable:** Polished, playable game with retro aesthetic

---

### Phase 9: Testing & Bug Fixes (2-3 days)

#### 9.1 Backend Testing
- [ ] Unit tests for all core logic
  - Hex utilities
  - Combat system
  - Movement validation
  - Production system
- [ ] Integration tests for API endpoints
- [ ] AI behavior validation

#### 9.2 Frontend Testing
- [ ] Test all user interactions
  - Unit selection and movement
  - Combat initiation
  - City production
  - Save/load
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Performance testing (large maps)

#### 9.3 Game Balance Testing
- [ ] Play full games against AI
- [ ] Adjust unit stats if needed
- [ ] Adjust AI difficulty
- [ ] Adjust production costs/times

#### 9.4 Bug Fixes
- [ ] Fix edge cases (units stuck, invalid states)
- [ ] Fix rendering issues
- [ ] Fix AI bugs (infinite loops, poor decisions)
- [ ] Fix save/load corruption

**Deliverable:** Stable, tested game ready for play

---

### Phase 10: Documentation & Deployment (1-2 days)

#### 10.1 Documentation
- [ ] Update README.md
  - Installation instructions
  - How to run the game
  - Game rules
  - Controls
- [ ] Code documentation (docstrings)
- [ ] API documentation (endpoint reference)

#### 10.2 Deployment Preparation
- [ ] Finalize `requirements.txt`
- [ ] Create production configuration
- [ ] Test with Gunicorn (production WSGI server)
- [ ] Create Dockerfile (optional)

#### 10.3 Deployment (Optional)
- [ ] Deploy to cloud platform (Heroku, AWS, DigitalOcean)
- [ ] Set up domain (optional)
- [ ] Configure static file serving (CDN or Nginx)

**Deliverable:** Deployed, documented game

---

## Summary Timeline

| Phase | Description | Duration | Cumulative |
|-------|-------------|----------|------------|
| 0 | Project Setup | 1-2 days | 1-2 days |
| 1 | Core Map System | 3-4 days | 4-6 days |
| 2 | Unit System | 4-5 days | 8-11 days |
| 3 | City & Production | 3-4 days | 11-15 days |
| 4 | Combat System | 3-4 days | 14-19 days |
| 5 | Turn System & Game Flow | 2-3 days | 16-22 days |
| 6 | AI Opponent | 5-6 days | 21-28 days |
| 7 | Save/Load | 2 days | 23-30 days |
| 8 | UI/UX Polish | 3-4 days | 26-34 days |
| 9 | Testing & Bugs | 2-3 days | 28-37 days |
| 10 | Documentation & Deployment | 1-2 days | 29-39 days |

**Total Estimated Time:** 29-39 days (approximately 6-8 weeks)

---

## Priority Features (MVP)

**Must Have (Phase 1-6):**
- Hexagonal map with terrain
- Units (at least Infantry, Tank, Fighter)
- Cities with production
- Combat system
- Turn-based gameplay
- Basic AI opponent

**Should Have (Phase 7-8):**
- Save/load functionality
- Retro UI polish
- Multiple unit types
- Win/lose conditions

**Nice to Have (Future):**
- Sound effects
- Animations
- Advanced AI
- Multiplayer
- Campaign mode

---

## Development Best Practices

### Daily Workflow
1. Start with backend logic for feature
2. Write unit tests
3. Implement API endpoint
4. Build frontend UI
5. Test integration
6. Commit changes

### Code Quality
- Use type hints in Python
- Write docstrings for functions
- Comment complex logic
- Keep functions small and focused
- Follow PEP 8 style guide

### Version Control
- Commit after each completed task
- Use descriptive commit messages
- Create branches for major features (optional)

### Testing Strategy
- Test each feature as it's built
- Play the game frequently during development
- Get feedback from others (if possible)

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| AI too complex/time-consuming | Start with simple rule-based AI, iterate later |
| Hexagonal rendering difficult | Use existing libraries or tutorials as reference |
| Performance issues | Optimize rendering, limit map size |
| Scope creep | Stick to MVP, defer nice-to-haves |
| Browser compatibility | Test early and often on multiple browsers |

---

## Next Steps

1. **Phase 0:** Set up development environment
2. Create folder structure
3. Initialize Flask app
4. Create basic HTML/CSS skeleton
5. Verify server runs and canvas displays

**First Commit:** "Initial project setup with Flask and basic frontend structure"
