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
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Get port from environment variable (for Render/Heroku) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    print("Starting PseudoQui Backend Server...")
    print(f"API available at: http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)
