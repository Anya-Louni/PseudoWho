"""
Unit Tests for PseudoQui Binary Tree Implementation
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.node import Node
from app.tree import BinaryTree


class TestNode(unittest.TestCase):
    """Test Node class"""
    
    def test_node_creation(self):
        """Test creating a node"""
        node = Node("Is it a mammal?", is_leaf=False)
        self.assertEqual(node.data, "Is it a mammal?")
        self.assertFalse(node.is_leaf)
        self.assertIsNone(node.left_child)
        self.assertIsNone(node.right_child)
    
    def test_leaf_node_creation(self):
        """Test creating a leaf node (animal)"""
        node = Node("Cat", is_leaf=True)
        self.assertEqual(node.data, "Cat")
        self.assertTrue(node.is_leaf)
    
    def test_node_parent_assignment(self):
        """Test parent-child relationships"""
        parent = Node("Question", is_leaf=False)
        child = Node("Child", is_leaf=True)
        parent.left_child = child
        self.assertEqual(child.parent, parent)
    
    def test_node_serialization(self):
        """Test converting node to dictionary"""
        node = Node("Test", is_leaf=False)
        node.left_child = Node("Left", is_leaf=True)
        node.right_child = Node("Right", is_leaf=True)
        
        data = node.to_dict()
        self.assertEqual(data['data'], "Test")
        self.assertFalse(data['is_leaf'])
        self.assertIsNotNone(data['left'])
        self.assertIsNotNone(data['right'])
    
    def test_node_deserialization(self):
        """Test creating node from dictionary"""
        data = {
            'data': 'Test',
            'is_leaf': False,
            'left': {'data': 'Left', 'is_leaf': True, 'left': None, 'right': None},
            'right': {'data': 'Right', 'is_leaf': True, 'left': None, 'right': None}
        }
        
        node = Node.from_dict(data)
        self.assertEqual(node.data, "Test")
        self.assertIsNotNone(node.left_child)
        self.assertEqual(node.left_child.data, "Left")


class TestBinaryTree(unittest.TestCase):
    """Test BinaryTree class"""
    
    def setUp(self):
        """Create a fresh tree for each test"""
        self.tree = BinaryTree()
    
    def test_tree_initialization(self):
        """Test tree is initialized correctly"""
        self.assertIsNotNone(self.tree.root)
        self.assertFalse(self.tree.root.is_leaf)
    
    def test_default_tree_structure(self):
        """Test default tree has correct structure"""
        self.assertEqual(self.tree.get_leaf_count(), 4)
        self.assertEqual(self.tree.get_node_count(), 7)
    
    def test_tree_height_calculation(self):
        """Test height calculation"""
        height = self.tree.get_tree_height()
        self.assertEqual(height, 2)  # Default tree has height 2
    
    def test_answer_navigation(self):
        """Test navigating tree with answers"""
        # First answer "yes" (mammals)
        reached_leaf = self.tree.answer_question(True)
        self.assertFalse(reached_leaf)
        self.assertIn("4 pattes", self.tree.get_current_question())
        
        # Second answer "yes" (4 legs)
        reached_leaf = self.tree.answer_question(True)
        self.assertTrue(reached_leaf)
        self.assertEqual(self.tree.get_guess(), "Chat")
    
    def test_different_path(self):
        """Test different navigation path"""
        self.tree.answer_question(False)  # Not mammal
        self.assertIn("voler", self.tree.get_current_question())
        
        self.tree.answer_question(False)  # Can't fly
        self.assertEqual(self.tree.get_guess(), "Serpent")
    
    def test_reset_game(self):
        """Test resetting game"""
        self.tree.answer_question(True)
        self.assertNotEqual(self.tree.current_node, self.tree.root)
        
        self.tree.reset_game()
        self.assertEqual(self.tree.current_node, self.tree.root)
    
    def test_learn_new_animal(self):
        """Test learning mechanism"""
        # Reach a guess
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        self.assertEqual(self.tree.get_guess(), "Chat")
        
        # Teach new animal
        success = self.tree.learn_new_animal(
            "Tigre",
            "Vit-il en Afrique ?",
            True
        )
        
        self.assertTrue(success)
        
        # Reset and verify tree was updated
        self.tree.reset_game()
        self.assertIn("Vit-il en Afrique ?", self.tree.get_current_question())
    
    def test_leaf_count_increases_with_learning(self):
        """Test that leaf count increases when learning new animal"""
        initial_leaves = self.tree.get_leaf_count()
        
        # Navigate to a leaf and teach new animal
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        self.tree.learn_new_animal("Lion", "Est-il roi de la jungle ?", True)
        
        self.assertEqual(self.tree.get_leaf_count(), initial_leaves + 1)
    
    def test_get_all_animals(self):
        """Test retrieving all animals"""
        animals = self.tree.get_all_animals()
        self.assertEqual(len(animals), 4)
        self.assertIn("Chat", animals)
        self.assertIn("Dauphin", animals)
        self.assertIn("Aigle", animals)
        self.assertIn("Serpent", animals)
    
    def test_statistics(self):
        """Test statistics calculation"""
        stats = self.tree.get_statistics()
        
        self.assertIn('height', stats)
        self.assertIn('total_nodes', stats)
        self.assertIn('leaf_count', stats)
        self.assertIn('average_depth', stats)
        self.assertIn('balance_factor', stats)
        
        self.assertEqual(stats['height'], 2)
        self.assertEqual(stats['total_nodes'], 7)
        self.assertEqual(stats['leaf_count'], 4)
    
    def test_tree_serialization(self):
        """Test tree serialization to dictionary"""
        original_leaves = self.tree.get_leaf_count()
        tree_dict = self.tree.to_dict()
        
        new_tree = BinaryTree.from_dict(tree_dict)
        self.assertEqual(new_tree.get_leaf_count(), original_leaves)
        self.assertEqual(new_tree.get_node_count(), self.tree.get_node_count())
    
    def test_game_history_tracking(self):
        """Test game history tracking"""
        initial_history = len(self.tree.game_history)
        
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        
        self.assertEqual(len(self.tree.game_history), initial_history + 2)
    
    def test_tree_display(self):
        """Test tree display function"""
        display = self.tree.display_tree()
        self.assertIsInstance(display, str)
        self.assertIn("mammifère", display)
        self.assertIn("Chat", display)


class TestGameFlow(unittest.TestCase):
    """Test complete game flow scenarios"""
    
    def setUp(self):
        """Create a fresh tree for each test"""
        self.tree = BinaryTree()
    
    def test_complete_game_correct_guess(self):
        """Test a complete game where guess is correct"""
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        guess = self.tree.get_guess()
        self.assertEqual(guess, "Chat")
    
    def test_complete_game_with_learning(self):
        """Test complete game with learning new animal"""
        # Play game, guess wrong
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        old_guess = self.tree.get_guess()
        
        # Teach new animal
        initial_count = self.tree.get_leaf_count()
        self.tree.learn_new_animal(
            "Chien",
            "Aboie-t-il ?",
            True
        )
        
        self.assertEqual(self.tree.get_leaf_count(), initial_count + 1)
        
        # Reset and verify new animal can be found
        self.tree.reset_game()
        self.tree.answer_question(True)
        self.tree.answer_question(True)
        new_question = self.tree.get_current_question()
        self.assertIn("Aboie", new_question)
    
    def test_multiple_games(self):
        """Test playing multiple games"""
        for _ in range(3):
            self.tree.reset_game()
            self.tree.answer_question(True)
            self.tree.answer_question(False)
    
    def test_average_depth_calculation(self):
        """Test average depth is calculated correctly"""
        avg_depth = self.tree.get_average_depth()
        self.assertGreater(avg_depth, 0)
        self.assertLessEqual(avg_depth, self.tree.get_tree_height())


if __name__ == '__main__':
    unittest.main()
