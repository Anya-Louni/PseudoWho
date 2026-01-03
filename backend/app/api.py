"""
Flask REST API for PseudoQui Backend
Provides endpoints for the frontend to interact with the game
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
from .game_manager import GameManager

# Initialize Flask app
app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
CORS(app)

# Initialize game manager
game_manager = GameManager(
    data_file=os.path.join('data', 'tree_data.json'),
    history_file=os.path.join('data', 'game_history.json')
)


@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """
    Start a new game session
    
    Returns:
        JSON with initial game state and first question
    """
    try:
        game_manager.start_new_game()
        
        return jsonify({
            'success': True,
            'message': 'New game started',
            'question': game_manager.tree.get_current_question(),
            'questions_asked': game_manager.current_session.questions_asked
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting game: {str(e)}'
        }), 500


@app.route('/api/game/answer', methods=['POST'])
def process_answer():
    """
    Process user answer to current question
    
    Request body:
        {
            "answer": "yes" or "no"
        }
    
    Returns:
        JSON with next question or guess
    """
    try:
        data = request.get_json()
        answer = data.get('answer', '').strip().lower()
        
        if answer not in ['yes', 'no', 'oui', 'non', 'y', 'n', 'o']:
            return jsonify({
                'success': False,
                'message': 'Invalid answer. Please answer with yes or no.'
            }), 400
        
        result = game_manager.process_answer(answer)
        
        response_data = {
            'success': True,
            'questions_asked': result['questions_asked'],
            'reached_guess': result['reached_leaf']
        }
        
        if result['reached_leaf']:
            response_data['guess'] = result['animal_guessed']
        else:
            response_data['question'] = result['current_question']
        
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing answer: {str(e)}'
        }), 500


@app.route('/api/game/guess-result', methods=['POST'])
def submit_guess_result():
    """
    Submit whether the guess was correct
    
    Request body:
        {
            "was_correct": true/false,
            "actual_animal": "animal name" (only if was_correct is false)
        }
    
    Returns:
        JSON with status
    """
    try:
        data = request.get_json()
        was_correct = data.get('was_correct', False)
        actual_animal = data.get('actual_animal', '')
        
        game_manager.submit_guess_result(was_correct, actual_animal)
        
        return jsonify({
            'success': True,
            'message': 'Guess result recorded'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error recording guess: {str(e)}'
        }), 500


@app.route('/api/game/learn', methods=['POST'])
def learn_new_animal():
    """
    Teach the system a new animal
    
    Request body:
        {
            "new_animal": "animal name",
            "question": "discriminating question",
            "answer_for_new": "yes" or "no"
        }
    
    Returns:
        JSON with status
    """
    try:
        data = request.get_json()
        new_animal = data.get('new_animal', '').strip()
        question = data.get('question', '').strip()
        answer_for_new = data.get('answer_for_new', '').strip().lower()
        
        if not new_animal or not question:
            return jsonify({
                'success': False,
                'message': 'Animal name and question are required'
            }), 400
        
        if answer_for_new not in ['yes', 'no', 'oui', 'non', 'y', 'n', 'o']:
            return jsonify({
                'success': False,
                'message': 'Invalid answer. Please answer with yes or no.'
            }), 400
        
        success = game_manager.teach_new_animal(new_animal, question, answer_for_new)
        
        if success:
            game_manager.end_current_game()
            return jsonify({
                'success': True,
                'message': f'Learned new animal: {new_animal}',
                'tree_updated': True
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error learning new animal'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error teaching new animal: {str(e)}'
        }), 500


@app.route('/api/game/end', methods=['POST'])
def end_game():
    """
    End the current game session
    
    Returns:
        JSON with status
    """
    try:
        game_manager.end_current_game()
        
        return jsonify({
            'success': True,
            'message': 'Game ended',
            'session': {
                'questions_asked': game_manager.current_session.questions_asked,
                'correct': game_manager.current_session.guessed_correctly
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error ending game: {str(e)}'
        }), 500


@app.route('/api/tree/display', methods=['GET'])
def get_tree_display():
    """
    Get text representation of the tree
    
    Returns:
        JSON with tree structure as string
    """
    try:
        tree_display = game_manager.tree.display_tree()
        return jsonify({
            'success': True,
            'tree': tree_display
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error displaying tree: {str(e)}'
        }), 500


@app.route('/api/tree/path', methods=['GET'])
def get_tree_path():
    """
    Get the decision path taken in the current game
    
    Returns:
        JSON with path history showing questions and answers
    """
    try:
        path = []
        current = game_manager.tree.root
        
        # Reconstruct the path from game history
        for question, answer in game_manager.tree.game_history:
            path.append({
                'question': question,
                'answer': 'Yes' if answer else 'No'
            })
            # Navigate to next node
            if answer:
                current = current.left_child
            else:
                current = current.right_child
        
        # Add the final guess
        if current:
            path.append({
                'question': f'Is it a {current.data}?',
                'answer': 'Guess'
            })
        
        return jsonify({
            'success': True,
            'path': path
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting tree path: {str(e)}'
        }), 500


@app.route('/api/tree/data', methods=['GET'])
def get_tree_data():
    """
    Get full tree data as JSON for visualization
    
    Returns:
        JSON tree structure
    """
    try:
        tree_data = game_manager.tree.to_dict()
        return jsonify({
            'success': True,
            'tree': tree_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving tree: {str(e)}'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Get game and tree statistics
    
    Returns:
        JSON with comprehensive statistics
    """
    try:
        stats = game_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving statistics: {str(e)}'
        }), 500


@app.route('/api/animals', methods=['GET'])
def get_animals():
    """
    Get list of all known animals
    
    Returns:
        JSON with list of animals
    """
    try:
        animals = game_manager.get_all_animals()
        return jsonify({
            'success': True,
            'animals': animals,
            'count': len(animals)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving animals: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'PseudoQui API is running'
    }), 200


@app.route('/api/learn-animal', methods=['POST'])
def learn_animal():
    """
    Learn a new animal that the player was thinking of
    
    Request body:
        {
            "animal": "animal_name"
        }
    
    Returns:
        JSON confirmation
    """
    try:
        data = request.get_json()
        animal_name = data.get('animal', '').strip()
        
        if not animal_name:
            return jsonify({
                'success': False,
                'message': 'Animal name is required'
            }), 400
        
        # The game manager will handle learning in future updates
        # For now, just acknowledge the learning
        
        return jsonify({
            'success': True,
            'message': f'Learned about {animal_name}!',
            'animal': animal_name
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error learning animal: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors - serve frontend for SPA routing"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': 'Endpoint not found'
        }), 404
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': f'Internal server error: {str(e)}'
    }), 500


if __name__ == '__main__':
    # Run in development mode
    app.run(debug=True, host='0.0.0.0', port=5000)
