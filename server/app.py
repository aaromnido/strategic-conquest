"""Flask application entry point for Strategic Conquest."""

from flask import Flask, render_template
from server.config import Config

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
app.config.from_object(Config)

# Import routes after app creation to avoid circular imports
from server.routes import game_routes

# Register blueprints
app.register_blueprint(game_routes.bp)

@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
