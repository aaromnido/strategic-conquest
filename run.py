"""Run the Strategic Conquest game server."""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
