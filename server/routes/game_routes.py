"""API routes for game operations."""

from flask import Blueprint, jsonify, request
from server.engine.game import GameController

bp = Blueprint('game', __name__, url_prefix='/api/game')

# Global game controller instance (in production, use session management)
game_controller = None

@bp.route('/new', methods=['POST'])
def new_game():
    """Start a new game."""
    global game_controller
    try:
        data = request.get_json() or {}
        width = data.get('width', 30)
        height = data.get('height', 20)

        game_controller = GameController(width, height)
        state = game_controller.get_state()

        return jsonify({
            'success': True,
            'state': state
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/state', methods=['GET'])
def get_state():
    """Get current game state."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        state = game_controller.get_state()
        return jsonify({
            'success': True,
            'state': state
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/move', methods=['POST'])
def move_unit():
    """Move a unit."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        data = request.get_json()
        unit_id = data.get('unit_id')
        target = data.get('target_hex')

        result = game_controller.move_unit(unit_id, (target['q'], target['r']))

        return jsonify({
            'success': result['success'],
            'message': result.get('message', ''),
            'state': game_controller.get_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/attack', methods=['POST'])
def attack():
    """Attack with a unit."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        data = request.get_json()
        attacker_id = data.get('attacker_id')
        defender_id = data.get('defender_id')

        result = game_controller.attack(attacker_id, defender_id)

        return jsonify({
            'success': result['success'],
            'result': result,
            'state': game_controller.get_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/produce', methods=['POST'])
def produce_unit():
    """Produce a unit in a city."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        data = request.get_json()
        city_id = data.get('city_id')
        unit_type = data.get('unit_type')

        result = game_controller.start_production(city_id, unit_type)

        return jsonify({
            'success': result['success'],
            'message': result.get('message', ''),
            'state': game_controller.get_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/end-turn', methods=['POST'])
def end_turn():
    """End current player's turn."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        game_controller.end_turn()

        return jsonify({
            'success': True,
            'state': game_controller.get_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/save', methods=['POST'])
def save_game():
    """Save current game."""
    global game_controller
    if game_controller is None:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    try:
        data = request.get_json()
        filename = data.get('filename', 'savegame')

        filepath = game_controller.save_game(filename)

        return jsonify({
            'success': True,
            'filepath': filepath
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/load', methods=['POST'])
def load_game():
    """Load a saved game."""
    global game_controller
    try:
        data = request.get_json()
        filename = data.get('filename')

        game_controller = GameController.load_game(filename)

        return jsonify({
            'success': True,
            'state': game_controller.get_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
