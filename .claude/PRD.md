# Product Requirements Document (PRD)
## Strategic Conquest Clone

### 1. Overview
Strategic Conquest clone - a turn-based strategy game for two players (human vs AI). The game is inspired by the classic Mac game Strategic Conquest, featuring territorial conquest, resource management, and tactical combat.

### 2. Game Objectives
- Conquer enemy cities and capture all territory
- Manage resources (production, movement)
- Build and command military units
- Eliminate opponent forces

### 3. Core Features

#### 3.1 Game Map
- **Hexagonal grid-based map**
- **Terrain types:**
  - Water (ocean/sea)
  - Land (plains, forests, mountains)
  - Cities (neutral, player-owned, enemy-owned)
- **Retro 16-bit pixel art style**
- **Basic color palette** (8-16 colors maximum)
- **Map size:** Configurable (default: 30x20 hexes)

#### 3.2 Units
- **Unit types:**
  - Infantry (ground, slow, cheap)
  - Armor/Tanks (ground, medium speed, expensive)
  - Fighter planes (air, fast, medium cost)
  - Bombers (air, medium speed, expensive)
  - Transport ships (naval, cargo capacity)
  - Destroyers (naval, combat)
  - Carriers (naval, can carry planes)

- **Unit attributes:**
  - Movement points
  - Attack strength
  - Defense strength
  - Range (for ranged units)
  - Production cost
  - Fuel/supplies

- **Retro pixel sprites** with basic colors

#### 3.3 Cities
- **Production centers:** Generate new units
- **Resource generation:** Cities produce resources per turn
- **Capture mechanic:** Infantry can capture neutral/enemy cities
- **City levels:** Different production capacities
- **Visual:** Pixelated buildings with player color indicator

#### 3.4 Player Turn Structure
1. **Production phase:** Build new units in cities
2. **Movement phase:** Move units across the map
3. **Combat phase:** Attack enemy units/cities
4. **End turn:** Resources calculated, AI takes turn

#### 3.5 Combat System
- **Simple combat resolution:**
  - Attacker strength vs Defender strength
  - Terrain modifiers (bonus for defenders in cities/mountains)
  - Random factor (dice roll)
- **Combat results:** Damage/elimination of units
- **Visual feedback:** Simple animation or flash effect

#### 3.6 AI Opponent
- **Difficulty levels:** Easy, Medium, Hard
- **AI behaviors:**
  - Expand territory (capture cities)
  - Build balanced army
  - Defend owned cities
  - Attack weak positions
  - Resource management
- **Decision-making:** Rule-based AI with simple strategic logic

#### 3.7 Game Interface
- **Main map view:** Central game board
- **Unit panel:** Selected unit information
- **City panel:** Selected city production menu
- **Resource display:** Current resources, income
- **Turn counter:** Current turn number
- **End turn button:** Complete player turn
- **Menu:** New game, save, load, quit

#### 3.8 Win Conditions
- **Victory:** Capture all enemy cities
- **Defeat:** Lose all cities
- **Optional:** Turn limit with score calculation

### 4. Visual Design
- **Retro aesthetic:** 16-bit era graphics
- **Pixel art:** All sprites hand-drawn in pixel style
- **Limited palette:** 16 colors maximum
- **Color coding:**
  - Player 1 (Human): Blue
  - Player 2 (AI): Red
  - Neutral: Gray/White
- **UI elements:** Retro-styled buttons, panels, borders

### 5. Technical Requirements
- **Platform:** Web-based (browser)
- **Single-player:** Human vs AI
- **Save/Load:** Game state persistence
- **Responsive:** Playable on desktop screens (minimum 1024x768)

### 6. Out of Scope (Phase 1)
- Multiplayer (human vs human online)
- Sound effects and music
- Multiple campaigns or scenarios
- Advanced AI using machine learning
- Mobile support
- Fog of war
- Diplomacy system

### 7. Success Metrics
- Playable end-to-end game loop
- AI makes reasonable strategic decisions
- Game runs smoothly in modern browsers
- Retro aesthetic achieved
- Fun and engaging gameplay

### 8. Future Enhancements (Post-MVP)
- Sound effects and background music
- Multiple map scenarios
- Campaign mode
- Improved AI difficulty levels
- Multiplayer support
- Fog of war mechanic
- Unit experience/veterancy system
