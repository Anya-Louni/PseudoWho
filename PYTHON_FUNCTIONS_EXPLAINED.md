# Python Functions Guide

This document explains every Python function used in the PseudoQui project in simple terms.

---

## Table of Contents
1. [Node Class (node.py)](#node-class)
2. [BinaryTree Class (tree.py)](#binarytree-class)
3. [GameManager Class (game_manager.py)](#gamemanager-class)
4. [API Routes (api.py)](#api-routes)

---

## Node Class

### `__init__(self, data, is_leaf=False, left_child=None, right_child=None, parent=None)`
**What it does:** Creates a new node (like a box) that can hold either a question or an animal name.

**Parameters:**
- `data`: The question or animal name stored in this node
- `is_leaf`: True if this is an answer (animal), False if it's a question
- `left_child`: The node to go to if answer is "Yes"
- `right_child`: The node to go to if answer is "No"
- `parent`: The node that came before this one

**Example:**
```python
# Create a question node
question_node = Node("Is it a mammal?", is_leaf=False)

# Create an animal node
animal_node = Node("Dog", is_leaf=True)
```

### `__post_init__(self)`
**What it does:** Automatically runs after creating a node to connect children to their parent.

**Why it's useful:** Makes sure family relationships are set up correctly (children know their parent).

### `to_dict(self)`
**What it does:** Converts the node and all its children into a dictionary (like a JSON object).

**Returns:** A dictionary with the node's data and its children

**Example output:**
```python
{
    'data': 'Is it a mammal?',
    'is_leaf': False,
    'left': {'data': 'Dog', 'is_leaf': True},
    'right': None
}
```

### `from_dict(cls, data)`
**What it does:** Creates a node from a dictionary (opposite of `to_dict`).

**Parameters:**
- `data`: Dictionary containing node information

**Returns:** A reconstructed Node object

---

## BinaryTree Class

### `__init__(self, root=None)`
**What it does:** Creates a new binary tree for the game.

**Parameters:**
- `root`: The starting node (if None, creates a default tree with 25 animals)

**What happens:**
- Sets up the tree structure
- Creates `current_node` to track where we are in the game
- Creates `game_history` to remember questions asked

### `_create_default_tree()`
**What it does:** Builds the initial tree with 25 pre-programmed animals.

**Returns:** The root node of the complete tree

**How it works:**
1. Creates root: "Is it a mammal?"
2. Builds left branch for mammals (Dog, Cat, Whale, etc.)
3. Builds right branch for non-mammals (Eagle, Snake, Fish, etc.)
4. Connects all nodes together

**Time Complexity:** O(n) where n = 25 animals
**Space Complexity:** O(n) for storing 25 animals + 24 questions = 49 nodes

### `reset_game(self)`
**What it does:** Starts a fresh game by going back to the root question.

**What it resets:**
- `current_node` → back to root
- `game_history` → empty list

### `answer_question(self, answer)`
**What it does:** Moves to the next node based on Yes/No answer.

**Parameters:**
- `answer`: True for "Yes", False for "No"

**Returns:** True if we reached an animal (leaf), False if more questions needed

**How it works:**
1. Record the current question and answer
2. If answer is Yes → move to left child
3. If answer is No → move to right child
4. Check if we reached a leaf (animal)

**Time Complexity:** O(1) - just following a pointer
**Space Complexity:** O(1) - only storing one answer

### `get_current_question(self)`
**What it does:** Gets the question to ask the player.

**Returns:** String with the current question

**Example:** "Does it live in water?"

### `get_guess(self)`
**What it does:** Gets the AI's final guess for the animal.

**Returns:** String with animal name

**How it works:**
1. First tries to use percentage-based selection (smart guess)
2. If that fails, uses the default animal from the node

### `_get_best_animal_by_percentage(self)`
**What it does:** Uses statistics to make a smarter guess.

**Returns:** Best matching animal name or None

**How it works:**
1. Calculate percentage of "Yes" answers given
2. Load animal database with known percentages
3. Find animal with closest matching percentage
4. Only consider animals already in the tree

**Time Complexity:** O(m) where m = animals in database
**Space Complexity:** O(m) for loading database

**Example:**
If player answered Yes to 70% of questions, the AI looks for an animal that typically gets 70% Yes answers.

### `learn_new_animal(self, new_animal, discriminating_question, answer_for_new)`
**What it does:** Teaches the AI a new animal when it guesses wrong.

**Parameters:**
- `new_animal`: Name of the correct animal
- `discriminating_question`: Question that separates new animal from guessed one
- `answer_for_new`: True if new animal answers Yes to the question

**Returns:** True if learning succeeded

**How it works:**
1. Get the old animal that was guessed
2. Create three new nodes:
   - Question node (the discriminating question)
   - New animal node
   - Old animal node
3. Connect them: If new animal answers Yes, it goes left; otherwise right
4. Replace the old leaf with the new question branch

**Time Complexity:** O(1) - just creating 3 nodes and updating pointers
**Space Complexity:** O(1) - only 3 new nodes

**Visual Example:**
```
Before:
    → Dog

After (learned Cat with question "Does it meow?"):
    → Does it meow?
       ├─ Yes → Cat
       └─ No → Dog
```

### `get_tree_height(self)`
**What it does:** Calculates how deep the tree is (longest path from root to leaf).

**Returns:** Integer representing tree height

**Time Complexity:** O(n) - must visit all nodes
**Space Complexity:** O(h) where h = height (recursion stack)

**Example:** A tree with 3 levels has height = 2

### `_calculate_height(node)`
**What it does:** Helper function that recursively calculates height.

**Parameters:**
- `node`: Current node being examined

**Returns:** Height of subtree rooted at this node

**How it works:**
1. If node is None, return -1
2. Calculate height of left subtree
3. Calculate height of right subtree
4. Return 1 + maximum of the two

### `get_node_count(self)`
**What it does:** Counts total number of nodes in the tree.

**Returns:** Integer count of all nodes (questions + animals)

**Time Complexity:** O(n)
**Space Complexity:** O(h) for recursion

### `_count_nodes(node)`
**What it does:** Helper function that recursively counts nodes.

**How it works:**
1. If node is None, return 0
2. Return 1 + count of left subtree + count of right subtree

### `get_leaf_count(self)`
**What it does:** Counts only the leaf nodes (animals, not questions).

**Returns:** Integer count of animals

**Time Complexity:** O(n)
**Space Complexity:** O(h)

### `_count_leaves(node)`
**What it does:** Helper function that recursively counts leaves.

**How it works:**
1. If node is None, return 0
2. If node is a leaf, return 1
3. Otherwise, return count from left + count from right

### `get_average_depth(self)`
**What it does:** Calculates average number of questions to reach an animal.

**Returns:** Float representing average depth

**Why it matters:** Lower average = fewer questions needed = better game experience

**Formula:** Total depth of all leaves ÷ Number of leaves

**Time Complexity:** O(n)

### `_sum_leaf_depths(node, depth)`
**What it does:** Helper function that adds up depths of all leaves.

**Parameters:**
- `node`: Current node
- `depth`: How far we are from root

**Returns:** Sum of all leaf depths

### `get_statistics(self)`
**What it does:** Gathers all important statistics about the tree.

**Returns:** Dictionary with:
- `height`: Maximum depth
- `total_nodes`: Count of all nodes
- `leaf_count`: Number of animals
- `average_depth`: Average questions per game
- `balance_factor`: How balanced the tree is (0 = perfect, 1 = worst)

**Time Complexity:** O(n)

### `_calculate_balance_factor(self)`
**What it does:** Measures how balanced the tree is.

**Returns:** Float between 0 and 1

**How it works:**
1. Get actual height of tree
2. Calculate optimal height for this many animals: log₂(animals)
3. Compare actual vs optimal
4. Return difference as percentage

**Example:**
- 8 animals optimal height = 3
- If actual height = 5, balance factor = (5-3)/5 = 0.4 (40% unbalanced)

### `get_all_animals(self)`
**What it does:** Makes a list of all animals in the tree.

**Returns:** List of animal names

**Time Complexity:** O(n)
**Space Complexity:** O(leaves) for storing animal names

### `_collect_animals(node, animals)`
**What it does:** Helper function that recursively collects animal names.

**Parameters:**
- `node`: Current node to check
- `animals`: List to add animals to

### `display_tree(self, node=None, prefix="", is_left=None)`
**What it does:** Creates a visual text representation of the tree.

**Returns:** String with ASCII art showing tree structure

**Example output:**
```
○ [Q1] Is it a mammal?
    └─> YES─┐
        |
    ├─ [Q2] Does it live in water?
        └─> NO──┘
            └─[GUESS] Is it a Dog?
```

### `_display_tree_recursive(node, prefix, is_left, result)`
**What it does:** Helper function that builds tree display recursively.

**Parameters:**
- `node`: Current node
- `prefix`: Indentation string
- `is_left`: Whether this is a left child
- `result`: List to append lines to

### `to_dict(self)`
**What it does:** Converts entire tree to dictionary for saving.

**Returns:** Dictionary representation of tree

**Use case:** Saving tree to JSON file

### `from_dict(cls, data)`
**What it does:** Creates tree from dictionary (loading from JSON).

**Parameters:**
- `data`: Dictionary with tree structure

**Returns:** New BinaryTree object

---

## GameManager Class

### `__init__(self, data_file, history_file)`
**What it does:** Creates a game manager to handle games and persistence.

**Parameters:**
- `data_file`: Path to save tree data (e.g., "tree_data.json")
- `history_file`: Path to save game history (e.g., "game_history.json")

**What it sets up:**
- Binary tree for the game
- Current game session tracker
- List of past game sessions
- Creates data directory if needed

### `start_new_game(self)`
**What it does:** Begins a fresh game session.

**What it does:**
1. Creates new GameSession object
2. Resets the tree to root
3. Clears game history

### `process_answer(self, answer)`
**What it does:** Handles a player's Yes/No answer.

**Parameters:**
- `answer`: String like "yes", "no", "oui", "non"

**Returns:** Dictionary with:
- `reached_leaf`: True if we have a guess
- `current_question`: Next question to ask
- `animal_guessed`: The guess (if reached leaf)
- `questions_asked`: Total questions so far

**How it works:**
1. Convert answer string to boolean (Yes=True, No=False)
2. Increment question counter
3. Pass answer to tree
4. Check if we reached an animal
5. Return appropriate response

**Time Complexity:** O(1)

### `submit_guess_result(self, was_correct, actual_animal)`
**What it does:** Records whether the AI guessed correctly.

**Parameters:**
- `was_correct`: True if guess was right
- `actual_animal`: Name of actual animal (if wrong)

**Effect:** Updates current session statistics

### `teach_new_animal(self, new_animal, discriminating_question, answer_for_new)`
**What it does:** Adds a new animal to the tree after wrong guess.

**Parameters:**
- `new_animal`: Name of new animal to learn
- `discriminating_question`: Question to tell it apart
- `answer_for_new`: Yes/No for new animal

**Returns:** True if successful

**What it does:**
1. Convert answer to boolean
2. Call tree's learn function
3. Mark session as "learned new animal"
4. Save updated tree to file

**Time Complexity:** O(n) for saving tree to JSON

### `end_current_game(self)`
**What it does:** Finishes the current game and saves it to history.

**What it does:**
1. Set end timestamp
2. Add session to history list
3. Save history to file

### `get_statistics(self)`
**What it does:** Calculates comprehensive game statistics.

**Returns:** Dictionary with two sections:
- `tree`: Tree structure stats (height, nodes, balance)
- `games`: Game history stats (total, win rate, averages)

**Calculations:**
- Total games = length of history
- Win rate = (correct guesses ÷ total games) × 100
- Average questions = sum of all questions ÷ total games

**Time Complexity:** O(n) for tree stats + O(m) for game history

### `save_tree(self)`
**What it does:** Saves current tree to JSON file.

**Returns:** True if successful, False if error

**What it does:**
1. Create data directory if needed
2. Convert tree to dictionary
3. Write to file with pretty formatting (indent=2)

**Time Complexity:** O(n) where n = nodes in tree

### `load_tree(self)`
**What it does:** Loads tree from JSON file.

**Returns:** True if successful

**What it does:**
1. Check if file exists
2. If exists, read and parse JSON
3. Reconstruct tree from dictionary
4. If doesn't exist, use default tree and save it

**Time Complexity:** O(n) for parsing and reconstructing

### `save_history(self)`
**What it does:** Saves game history to JSON file.

**Returns:** True if successful

**What it saves:**
- List of all game sessions
- Each session includes: questions asked, timestamps, results

### `load_history(self)`
**What it does:** Loads game history from JSON file.

**Returns:** True if successful

**What it does:**
1. Check if file exists
2. Parse JSON
3. Convert each session dict back to GameSession object
4. If file doesn't exist, start with empty history

### `get_all_animals(self)`
**What it does:** Gets list of all animals in the tree.

**Returns:** List of animal names

**Delegates to:** tree.get_all_animals()

---

## GameSession Class

### `__init__(self)`
**What it does:** Creates a new game session to track one game.

**What it initializes:**
- `questions_asked`: Counter starting at 0
- `start_time`: Current timestamp
- `end_time`: None (set when game ends)
- `guessed_correctly`: False (updated at end)
- `animal_guessed`: Empty string
- `animal_actual`: Empty string (if wrong)
- `learned_new_animal`: False

### `to_dict(self)`
**What it does:** Converts session to dictionary for saving.

**Returns:** Dictionary with all session data

**Date handling:** Converts datetime to ISO format string

---

## API Routes (api.py)

### `start_game()`
**Route:** POST /api/game/start

**What it does:** Starts a new game session.

**Returns:** JSON with:
- `success`: True/False
- `message`: Status message
- `question`: First question to ask
- `questions_asked`: 0

**HTTP Status:** 200 if success, 500 if error

### `process_answer()`
**Route:** POST /api/game/answer

**Expected Input:**
```json
{
    "answer": "yes" or "no"
}
```

**What it does:** Processes player's answer and returns next question or guess.

**Returns:** JSON with:
- `success`: True/False
- `reached_guess`: True if at animal
- `question`: Next question (if not at animal)
- `guess`: Animal name (if at animal)
- `questions_asked`: Current count

**Validation:** Checks answer is valid (yes/no/oui/non)

### `submit_guess_result()`
**Route:** POST /api/game/guess-result

**Expected Input:**
```json
{
    "was_correct": true/false,
    "actual_animal": "name" (if wrong)
}
```

**What it does:** Records whether guess was correct.

**Returns:** JSON confirmation

### `learn_new_animal()`
**Route:** POST /api/game/learn

**Expected Input:**
```json
{
    "new_animal": "Kangaroo",
    "question": "Does it hop?",
    "answer_for_new": "yes"
}
```

**What it does:** Teaches AI a new animal.

**What it does:**
1. Validate inputs
2. Call teach_new_animal()
3. End current game
4. Return success

**Returns:** JSON with:
- `success`: True/False
- `message`: Confirmation or error
- `tree_updated`: True if successful

### `end_game()`
**Route:** POST /api/game/end

**What it does:** Ends current game session.

**Returns:** JSON with session summary

### `get_tree_display()`
**Route:** GET /api/tree/display

**What it does:** Gets text representation of tree.

**Returns:** JSON with:
- `success`: True/False
- `tree`: ASCII art string of tree

### `get_tree_path()`
**Route:** GET /api/tree/path

**What it does:** Gets decision path taken in current game.

**Returns:** JSON with:
- `success`: True/False
- `path`: Array of {question, answer} objects

**How it works:**
1. Get game history from tree
2. Reconstruct path by following answers
3. Add final guess at end

**Example output:**
```json
{
    "path": [
        {"question": "Is it a mammal?", "answer": "Yes"},
        {"question": "Does it live in water?", "answer": "No"},
        {"question": "Is it a Dog?", "answer": "Guess"}
    ]
}
```

### `get_tree_data()`
**Route:** GET /api/tree/data

**What it does:** Gets full tree structure as JSON.

**Returns:** Complete tree dictionary

**Use case:** Saving game state, visualization

### `get_statistics()`
**Route:** GET /api/stats

**What it does:** Gets comprehensive statistics.

**Returns:** JSON with:
- `tree`: Tree structure statistics
- `games`: Game history statistics

### `get_animals()`
**Route:** GET /api/animals

**What it does:** Gets list of all known animals.

**Returns:** JSON with:
- `animals`: Array of animal names
- `count`: Number of animals

### `health_check()`
**Route:** GET /api/health

**What it does:** Checks if API is running.

**Returns:** JSON with status "healthy"

**Use case:** Monitoring, debugging

---

## Built-in Python Functions Used

### `open(file, mode, encoding)`
**What it does:** Opens a file for reading or writing.

**Parameters:**
- `file`: Path to file
- `mode`: 'r' (read), 'w' (write), 'a' (append)
- `encoding`: Character encoding (use 'utf-8')

**Example:**
```python
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### `json.load(file)`
**What it does:** Reads JSON from file and converts to Python object.

**Returns:** Dictionary or list

### `json.dump(obj, file, indent, ensure_ascii)`
**What it does:** Writes Python object to file as JSON.

**Parameters:**
- `obj`: Python dictionary/list to save
- `file`: Open file object
- `indent`: Spaces for pretty printing
- `ensure_ascii`: False to allow non-ASCII characters

### `os.path.exists(path)`
**What it does:** Checks if file or directory exists.

**Returns:** True if exists, False otherwise

### `os.path.join(path1, path2, ...)`
**What it does:** Combines path parts with correct separator (/ or \).

**Example:**
```python
path = os.path.join('data', 'tree.json')
# Windows: 'data\\tree.json'
# Linux: 'data/tree.json'
```

### `os.makedirs(path, exist_ok)`
**What it does:** Creates directory and all parent directories.

**Parameters:**
- `path`: Directory to create
- `exist_ok`: True = don't error if already exists

### `datetime.now()`
**What it does:** Gets current date and time.

**Returns:** datetime object

### `datetime.isoformat()`
**What it does:** Converts datetime to standard string format.

**Example:** "2026-01-03T14:30:00"

### `sum(iterable)`
**What it does:** Adds up all numbers in a list.

**Example:**
```python
sum([1, 2, 3, 4])  # Returns 10
```

### `len(iterable)`
**What it does:** Counts items in list/string/dictionary.

### `max(a, b)`
**What it does:** Returns the larger of two numbers.

### `min(a, b)`
**What it does:** Returns the smaller of two numbers.

### `abs(x)`
**What it does:** Returns absolute value (removes negative sign).

**Example:** `abs(-5)` returns `5`

### `round(x, digits)`
**What it does:** Rounds number to specified decimal places.

**Example:** `round(3.14159, 2)` returns `3.14`

### `isinstance(obj, type)`
**What it does:** Checks if object is of specific type.

**Example:**
```python
isinstance("hello", str)  # True
isinstance(42, int)       # True
```

### `enumerate(iterable)`
**What it does:** Loops through list with index.

**Example:**
```python
for index, value in enumerate(['a', 'b', 'c']):
    print(f"{index}: {value}")
# Output:
# 0: a
# 1: b
# 2: c
```

---

## Summary of Complexity

| Function | Time Complexity | Space Complexity | Use Case |
|----------|----------------|------------------|----------|
| `answer_question()` | O(1) | O(1) | Navigate tree |
| `learn_new_animal()` | O(1) | O(1) | Add new animal |
| `get_tree_height()` | O(n) | O(h) | Tree analysis |
| `get_statistics()` | O(n) | O(1) | Get all stats |
| `save_tree()` | O(n) | O(n) | Persist data |
| `load_tree()` | O(n) | O(n) | Load data |
| `display_tree()` | O(n) | O(n) | Visualize tree |

Where:
- n = total nodes in tree
- h = height of tree
- m = number of animals

---

## Key Takeaways for High School Students

1. **Recursion**: Many tree functions call themselves on children nodes
2. **Time Complexity**: Most operations are O(1) or O(n), making the game fast
3. **Data Structures**: Binary tree is perfect for yes/no questions
4. **File I/O**: JSON files store game data between sessions
5. **API Design**: REST endpoints separate frontend from backend
6. **Error Handling**: Try/except blocks prevent crashes

This guide should help you understand exactly what every function does and why it's needed!
