# Strategic Conquest Clone

A turn-based strategy game inspired by the classic Mac game Strategic Conquest. Built with Python/Flask backend and vanilla JavaScript frontend featuring retro 16-bit pixel art aesthetic.

## Features

- **Hexagonal grid-based map** with terrain types (water, land, forest, mountain)
- **Multiple unit types**: Infantry, Tank, Fighter, Bomber, Destroyer, Transport
- **City production system**: Build units in captured cities
- **Turn-based combat** with terrain modifiers
- **AI opponent** with strategic decision-making
- **Save/Load functionality**
- **Retro pixel art aesthetic** with 16-color palette

## Installation

### Requirements

- Python 3.10+
- Flask

### Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

Start the Flask server:
```bash
python run.py
```

Or using Flask CLI:
```bash
flask --app server/app run --debug --port 5001
```

The game will be available at: `http://localhost:5001`

## How to Play

### Controls

- **Click on your units** to select them
- **Click on highlighted hexes** to move (green) or attack (red)
- **Click on your cities** to open production menu
- **Build units** by clicking the build buttons in the city panel
- **End Turn** button to finish your turn (AI will play automatically)

### Game Rules

1. **Objective**: Capture all enemy cities to win
2. **Movement**: Each unit has limited movement per turn
3. **Combat**: Units can attack adjacent enemies (or ranged if applicable)
4. **Cities**: Produce units each turn, generate resources
5. **Capture**: Infantry units can capture enemy/neutral cities by moving onto them

### Unit Types

| Unit | Movement | Attack | Defense | Cost | Special |
|------|----------|--------|---------|------|---------|
| Infantry | 2 | 3 | 4 | 50 | Can capture cities |
| Tank | 3 | 8 | 6 | 100 | Strong ground unit |
| Fighter | 6 | 6 | 4 | 80 | Fast air unit |
| Bomber | 5 | 10 | 2 | 120 | Heavy damage |
| Transport | 4 | 0 | 3 | 70 | Naval transport |
| Destroyer | 4 | 7 | 5 | 90 | Naval combat |

## Project Structure

```
strategic-conquest/
├── server/              # Backend Python code
│   ├── app.py          # Flask application
│   ├── config.py       # Configuration
│   ├── engine/         # Game logic
│   ├── models/         # Data models
│   ├── routes/         # API endpoints
│   └── utils/          # Utilities (hex grid)
├── static/             # Frontend assets
│   ├── js/             # JavaScript code
│   └── css/            # Stylesheets
├── templates/          # HTML templates
└── saves/              # Saved games

```

## Architecture

- **Backend**: Python/Flask with REST API
- **Frontend**: Vanilla JavaScript with Canvas rendering
- **Coordinate System**: Axial hex coordinates (q, r)
- **Rendering**: Pixel-perfect canvas with geometric shapes for units
- **AI**: Simple rule-based strategic AI

## Development

See `.claude/plan.md` for detailed development roadmap and `.claude/architecture.md` for technical architecture.

### Testing

```bash
pytest
```

## License

MIT

## Credits

Inspired by the original Strategic Conquest by Peter Merrill (1984)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
