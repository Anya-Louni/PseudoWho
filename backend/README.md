# PseudoQui - Backend

Professional Python backend for the PseudoQui animal guessing game.

## Features

- **Binary Tree Decision Engine**: Optimal implementation for game logic
- **Adaptive Learning**: System learns new animals from user feedback
- **Persistent Storage**: Tree and game history saved in JSON format
- **Comprehensive Statistics**: Tree analysis and game metrics
- **REST API**: Flask-based API for frontend integration
- **Production Ready**: Error handling, CORS support, health checks

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Game Management
- `POST /api/game/start` - Start a new game
- `POST /api/game/answer` - Submit answer to current question
- `POST /api/game/guess-result` - Submit whether guess was correct
- `POST /api/game/learn` - Teach system a new animal
- `POST /api/game/end` - End current game session

### Data Retrieval
- `GET /api/tree/display` - Get text representation of tree
- `GET /api/tree/data` - Get full tree structure as JSON
- `GET /api/stats` - Get comprehensive statistics
- `GET /api/animals` - Get list of all known animals
- `GET /api/health` - Health check

## Running Tests

```bash
python -m pytest tests/ -v
```

or

```bash
python -m unittest discover tests/
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── node.py           # Node structure definition
│   ├── tree.py           # Binary tree implementation
│   ├── game_manager.py   # Game session and persistence
│   └── api.py            # Flask REST API
├── tests/
│   └── test_tree.py      # Unit tests
├── data/                 # Persistent data (created at runtime)
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

## Architecture

### Node Structure
- **Internal Nodes**: Store questions
- **Leaf Nodes**: Store animal names
- **Convention**: Left = "Yes", Right = "No"

### Tree Operations
- **Traversal**: Navigate based on yes/no answers
- **Learning**: Insert new animal with discriminating question
- **Analysis**: Calculate height, average depth, balance

### Game Flow
1. Start game → Reset tree to root
2. Ask question → Navigate tree
3. Make guess → Reach leaf node
4. Get feedback → Learn if wrong

## Data Persistence

- Tree structure saved in `data/tree_data.json`
- Game history saved in `data/game_history.json`
- Automatic loading on startup
- Automatic saving after learning

## Performance

- **Time Complexity**: O(log n) average for tree operations
- **Space Complexity**: O(n) for tree storage
- **Serialization**: Efficient JSON format

## Development

For development mode with auto-reload:
```bash
python run.py
```

For production, use a WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app.api:app
```

## Author

Created for University Project - PseudoQui Assignment

## License

MIT
