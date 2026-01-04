"""
Main entry point for running PseudoQui backend server
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.api import app

if __name__ == '__main__':
    # Create data directory with absolute path
    data_dir = os.path.join(backend_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Delete old tree data to force fresh start (for deployment and local)
    tree_file = os.path.join(data_dir, 'tree_data.json')
    if os.path.exists(tree_file):
        os.remove(tree_file)
        print("✓ Cleared old tree data - starting fresh")
    
    history_file = os.path.join(data_dir, 'game_history.json')
    if os.path.exists(history_file):
        os.remove(history_file)
        print("✓ Cleared game history")
    
    # Get port from environment variable (for Render/Heroku) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    print("Starting PseudoQui Backend Server...")
    print(f"API available at: http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)
