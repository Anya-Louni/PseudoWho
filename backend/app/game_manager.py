"""
Game Management and Game Session Logic
Handles game flow, scoring, and persistence
"""

import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from .tree import BinaryTree


class GameSession:
    """
    Represents a single game session with scoring
    """
    def __init__(self):
        self.questions_asked = 0
        self.start_time = datetime.now()
        self.end_time = None
        self.guessed_correctly = False
        self.animal_guessed = ""
        self.animal_actual = ""
        self.learned_new_animal = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for storage"""
        return {
            'questions_asked': self.questions_asked,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'guessed_correctly': self.guessed_correctly,
            'animal_guessed': self.animal_guessed,
            'animal_actual': self.animal_actual,
            'learned_new_animal': self.learned_new_animal
        }


class GameManager:
    """
    Manages the overall game state, persistence, and scoring
    """
    
    def __init__(self, data_file: str = "data/tree_data.json", 
                 history_file: str = "data/game_history.json"):
        """
        Initialize game manager
        
        Args:
            data_file: Path to save/load tree data
            history_file: Path to save/load game history
        """
        # Ensure absolute paths for deployment
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_file = os.path.join(base_dir, data_file)
        self.history_file = os.path.join(base_dir, history_file)
        self.tree = BinaryTree()
        self.current_session = GameSession()
        self.game_history: List[GameSession] = []
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Load existing data
        self.load_tree()
        self.load_history()
    
    def start_new_game(self):
        """Start a new game session"""
        self.current_session = GameSession()
        self.tree.reset_game()
    
    def process_answer(self, answer: str) -> Dict[str, Any]:
        """
        Process user answer and update game state
        
        Args:
            answer: "yes" or "no" (case-insensitive)
            
        Returns:
            Dictionary with game state update
        """
        answer_bool = answer.lower() in ['yes', 'oui', 'o', 'y', '1', 'true']
        self.current_session.questions_asked += 1
        
        reached_leaf = self.tree.answer_question(answer_bool)
        
        return {
            'reached_leaf': reached_leaf,
            'current_question': self.tree.get_current_question(),
            'animal_guessed': self.tree.get_guess() if reached_leaf else None,
            'questions_asked': self.current_session.questions_asked
        }
    
    def submit_guess_result(self, was_correct: bool, actual_animal: str = None):
        """
        Submit result of the guess
        
        Args:
            was_correct: Whether the guess was correct
            actual_animal: The actual animal (if guess was wrong)
        """
        self.current_session.guessed_correctly = was_correct
        if not was_correct:
            self.current_session.animal_actual = actual_animal
            self.current_session.animal_guessed = self.tree.get_guess()
    
    def teach_new_animal(self, new_animal: str, discriminating_question: str,
                        answer_for_new: str) -> bool:
        """
        Teach the system a new animal
        
        Args:
            new_animal: The animal to learn
            discriminating_question: Question to distinguish it
            answer_for_new: "yes" or "no"
            
        Returns:
            True if learning was successful
        """
        answer_bool = answer_for_new.lower() in ['yes', 'oui', 'o', 'y', '1', 'true']
        success = self.tree.learn_new_animal(new_animal, discriminating_question, answer_bool)
        
        if success:
            self.current_session.learned_new_animal = True
            self.save_tree()
        
        return success
    
    def end_current_game(self):
        """End the current game and add to history"""
        self.current_session.end_time = datetime.now()
        self.game_history.append(self.current_session)
        self.save_history()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics
        
        Returns:
            Dictionary with game and tree statistics
        """
        tree_stats = self.tree.get_statistics()
        
        # Calculate game statistics
        total_games = len(self.game_history)
        correct_guesses = sum(1 for g in self.game_history if g.guessed_correctly)
        average_questions = sum(g.questions_asked for g in self.game_history) / total_games if total_games > 0 else 0
        
        return {
            'tree': tree_stats,
            'games': {
                'total': total_games,
                'correct_guesses': correct_guesses,
                'incorrect_guesses': total_games - correct_guesses,
                'success_rate': (correct_guesses / total_games * 100) if total_games > 0 else 0,
                'average_questions_per_game': round(average_questions, 2)
            }
        }
    
    def save_tree(self) -> bool:
        """
        Save tree to file
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(self.data_file) if os.path.dirname(self.data_file) else ".", exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tree.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tree: {e}")
            return False
    
    def load_tree(self) -> bool:
        """
        Load tree from file
        
        Returns:
            True if successful (or file doesn't exist yet)
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tree = BinaryTree.from_dict(data)
                return True
            else:
                # File doesn't exist, use default tree and save it
                self.save_tree()
                return True
        except Exception as e:
            print(f"Error loading tree: {e}")
            # Use default tree on error
            self.tree = BinaryTree()
            return False
    
    def save_history(self) -> bool:
        """
        Save game history to file
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(self.history_file) if os.path.dirname(self.history_file) else ".", exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                history_data = [g.to_dict() for g in self.game_history]
                json.dump(history_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False
    
    def load_history(self) -> bool:
        """
        Load game history from file
        
        Returns:
            True if successful
        """
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    self.game_history = []
                    for item in history_data:
                        session = GameSession()
                        session.questions_asked = item['questions_asked']
                        session.start_time = datetime.fromisoformat(item['start_time'])
                        session.end_time = datetime.fromisoformat(item['end_time']) if item.get('end_time') else None
                        session.guessed_correctly = item['guessed_correctly']
                        session.animal_guessed = item['animal_guessed']
                        session.animal_actual = item['animal_actual']
                        session.learned_new_animal = item['learned_new_animal']
                        self.game_history.append(session)
                return True
            return True  # No history file is fine
        except Exception as e:
            print(f"Error loading history: {e}")
            return False
    
    def get_all_animals(self) -> List[str]:
        """Get list of all known animals"""
        return self.tree.get_all_animals()
