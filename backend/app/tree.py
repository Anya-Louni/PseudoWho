"""
Binary Tree Data Structure and Game Logic for PseudoQui
Implements the core decision tree for the guessing game with learning capabilities
"""

from typing import Optional, Tuple, Dict, List, Any
from .node import Node


class BinaryTree:
    """
    Binary Decision Tree for the animal guessing game.
    
    The tree uses a simple convention:
    - Left child: response "Yes" to the parent's question
    - Right child: response "No" to the parent's question
    """
    
    def __init__(self, root: Optional[Node] = None):
        """
        Initialize the tree with optional root node
        
        Args:
            root: Root node of the tree (if None, creates a basic tree)
        """
        if root is None:
            self.root = self._create_default_tree()
        else:
            self.root = root
        
        self.current_node = self.root
        self.game_history = []  # Track questions asked in current game
    
    @staticmethod
    def _create_default_tree() -> Node:
        """
        Create expanded default tree with 25+ animals
        Completely clean structure - NO overwrites
        
        Returns:
            Root node of default tree
        """
        # Root: Is it a mammal?
        root = Node("Is it a mammal?", is_leaf=False)
        
        # ===== MAMMALS (YES to mammal) =====
        mammals = Node("Does it live in water?", is_leaf=False)
        mammals.parent = root
        root.left_child = mammals
        
        # Water mammals (YES to water)
        water_mammals = Node("Is it huge?", is_leaf=False)
        water_mammals.parent = mammals
        mammals.left_child = water_mammals
        
        whale = Node("Whale", is_leaf=True)
        whale.parent = water_mammals
        water_mammals.left_child = whale
        
        dolphin = Node("Dolphin", is_leaf=True)
        dolphin.parent = water_mammals
        water_mammals.right_child = dolphin
        
        # Land mammals (NO to water)
        land_mammals = Node("Does it have 4 legs?", is_leaf=False)
        land_mammals.parent = mammals
        mammals.right_child = land_mammals
        
        # 4-legged land mammals (YES to 4 legs)
        four_legs = Node("Is it carnivorous?", is_leaf=False)
        four_legs.parent = land_mammals
        land_mammals.left_child = four_legs
        
        # Carnivores (YES to carnivorous)
        carnivores = Node("Does it hunt in packs?", is_leaf=False)
        carnivores.parent = four_legs
        four_legs.left_child = carnivores
        
        # Pack hunters (YES to packs)
        pack_hunters = Node("Is it a canine?", is_leaf=False)
        pack_hunters.parent = carnivores
        carnivores.left_child = pack_hunters
        
        dog = Node("Dog", is_leaf=True)
        dog.parent = pack_hunters
        pack_hunters.left_child = dog
        
        fox = Node("Fox", is_leaf=True)
        fox.parent = pack_hunters
        pack_hunters.right_child = fox
        
        # Solitary hunters (NO to packs)
        solo_hunters = Node("Is it a big cat?", is_leaf=False)
        solo_hunters.parent = carnivores
        carnivores.right_child = solo_hunters
        
        tiger = Node("Tiger", is_leaf=True)
        tiger.parent = solo_hunters
        solo_hunters.left_child = tiger
        
        lion = Node("Lion", is_leaf=True)
        lion.parent = solo_hunters
        solo_hunters.right_child = lion
        
        # Herbivores (NO to carnivorous)
        herbivores = Node("Is it very large?", is_leaf=False)
        herbivores.parent = four_legs
        four_legs.right_child = herbivores
        
        # Large herbivores (YES to large)
        large_herb = Node("Does it have a trunk?", is_leaf=False)
        large_herb.parent = herbivores
        herbivores.left_child = large_herb
        
        elephant = Node("Elephant", is_leaf=True)
        elephant.parent = large_herb
        large_herb.left_child = elephant
        
        horse = Node("Horse", is_leaf=True)
        horse.parent = large_herb
        large_herb.right_child = horse
        
        # Small herbivores (NO to large)
        small_herb = Node("Does it have horns?", is_leaf=False)
        small_herb.parent = herbivores
        herbivores.right_child = small_herb
        
        cow = Node("Cow", is_leaf=True)
        cow.parent = small_herb
        small_herb.left_child = cow
        
        rabbit = Node("Rabbit", is_leaf=True)
        rabbit.parent = small_herb
        small_herb.right_child = rabbit
        
        # Not 4-legged mammals (NO to 4 legs)
        not_four_legs = Node("Is it a primate?", is_leaf=False)
        not_four_legs.parent = land_mammals
        land_mammals.right_child = not_four_legs
        
        monkey = Node("Monkey", is_leaf=True)
        monkey.parent = not_four_legs
        not_four_legs.left_child = monkey
        
        bear = Node("Bear", is_leaf=True)
        bear.parent = not_four_legs
        not_four_legs.right_child = bear
        
        # ===== NOT MAMMALS (NO to mammal) =====
        not_mammals = Node("Does it have feathers?", is_leaf=False)
        not_mammals.parent = root
        root.right_child = not_mammals
        
        # Birds (YES to feathers)
        birds = Node("Can it fly?", is_leaf=False)
        birds.parent = not_mammals
        not_mammals.left_child = birds
        
        # Flying birds (YES to fly)
        flying = Node("Is it a bird of prey?", is_leaf=False)
        flying.parent = birds
        birds.left_child = flying
        
        eagle = Node("Eagle", is_leaf=True)
        eagle.parent = flying
        flying.left_child = eagle
        
        parrot = Node("Parrot", is_leaf=True)
        parrot.parent = flying
        flying.right_child = parrot
        
        # Non-flying birds (NO to fly)
        penguin = Node("Penguin", is_leaf=True)
        penguin.parent = birds
        birds.right_child = penguin
        
        # Not birds (NO to feathers)
        not_birds = Node("Does it have scales?", is_leaf=False)
        not_birds.parent = not_mammals
        not_mammals.right_child = not_birds
        
        # Reptiles (YES to scales)
        reptiles = Node("Is it dangerous?", is_leaf=False)
        reptiles.parent = not_birds
        not_birds.left_child = reptiles
        
        # Dangerous reptiles (YES to dangerous)
        dangerous_rept = Node("Is it venomous?", is_leaf=False)
        dangerous_rept.parent = reptiles
        reptiles.left_child = dangerous_rept
        
        snake = Node("Snake", is_leaf=True)
        snake.parent = dangerous_rept
        dangerous_rept.left_child = snake
        
        crocodile = Node("Crocodile", is_leaf=True)
        crocodile.parent = dangerous_rept
        dangerous_rept.right_child = crocodile
        
        # Non-dangerous reptiles (NO to dangerous)
        turtle = Node("Turtle", is_leaf=True)
        turtle.parent = reptiles
        reptiles.right_child = turtle
        
        # No scales (NO to scales)
        no_scales = Node("Does it have wings?", is_leaf=False)
        no_scales.parent = not_birds
        not_birds.right_child = no_scales
        
        # Has wings (YES to wings)
        winged = Node("Does it make honey?", is_leaf=False)
        winged.parent = no_scales
        no_scales.left_child = winged
        
        bee = Node("Bee", is_leaf=True)
        bee.parent = winged
        winged.left_child = bee
        
        butterfly = Node("Butterfly", is_leaf=True)
        butterfly.parent = winged
        winged.right_child = butterfly
        
        # No wings (NO to wings)
        no_wings = Node("Does it live in water?", is_leaf=False)
        no_wings.parent = no_scales
        no_scales.right_child = no_wings
        
        fish = Node("Fish", is_leaf=True)
        fish.parent = no_wings
        no_wings.left_child = fish
        
        # Land creatures without wings/scales
        land_no_scale = Node("Does it jump?", is_leaf=False)
        land_no_scale.parent = no_wings
        no_wings.right_child = land_no_scale
        
        frog = Node("Frog", is_leaf=True)
        frog.parent = land_no_scale
        land_no_scale.left_child = frog
        
        spider = Node("Spider", is_leaf=True)
        spider.parent = land_no_scale
        land_no_scale.right_child = spider
        
        return root
    
    def reset_game(self):
        """Reset to root node for a new game"""
        self.current_node = self.root
        self.game_history = []
    
    def answer_question(self, answer: bool) -> bool:
        """
        Navigate the tree based on the answer to current question
        
        Args:
            answer: True for "Yes", False for "No"
            
        Returns:
            True if we've reached a leaf node (guessed the animal), False otherwise
        """
        if self.current_node.is_leaf:
            return True
        
        # Record the question in history
        self.game_history.append((self.current_node.data, answer))
        
        # Navigate: Yes (True) = left, No (False) = right
        if answer:
            self.current_node = self.current_node.left_child
        else:
            self.current_node = self.current_node.right_child
        
        return self.current_node.is_leaf if self.current_node else False
    
    def get_current_question(self) -> str:
        """
        Get the current question to ask the user
        
        Returns:
            Current question string
        """
        if not self.current_node:
            return ""
        return self.current_node.data
    
    def get_guess(self) -> str:
        """
        Get the current guess (animal at leaf node)
        Always returns the animal at the current leaf - the tree structure is truth
        
        Returns:
            The animal name the tree guessed
        """
        if not self.current_node or not self.current_node.is_leaf:
            return ""
        
        # The tree path determines the guess - always use the leaf node's animal
        return self.current_node.data
    
    def learn_new_animal(self, new_animal: str, discriminating_question: str, 
                        answer_for_new: bool) -> bool:
        """
        Learn a new animal when the current guess was wrong
        
        Args:
            new_animal: The animal the user was thinking of
            discriminating_question: Question that differentiates new animal from guessed one
            answer_for_new: True if answer is "Yes" for the new animal, False for "No"
            
        Returns:
            True if learning was successful
        """
        if not self.current_node or not self.current_node.is_leaf:
            return False
        
        old_animal = self.current_node.data
        
        # Create new nodes
        new_animal_node = Node(new_animal, is_leaf=True)
        old_animal_node = Node(old_animal, is_leaf=True)
        question_node = Node(discriminating_question, is_leaf=False)
        
        # Insert based on answer for new animal
        if answer_for_new:
            question_node.left_child = new_animal_node
            question_node.right_child = old_animal_node
        else:
            question_node.left_child = old_animal_node
            question_node.right_child = new_animal_node
        
        new_animal_node.parent = question_node
        old_animal_node.parent = question_node
        
        # Replace the old leaf with the new question node
        if self.current_node.parent:
            if self.current_node.parent.left_child == self.current_node:
                self.current_node.parent.left_child = question_node
            else:
                self.current_node.parent.right_child = question_node
            question_node.parent = self.current_node.parent
        else:
            # The old guess was at the root
            self.root = question_node
        
        self.current_node = question_node
        
        # Update the animals database with this new animal
        self._update_animal_in_database(new_animal)
        
        return True
    
    def update_animal_success(self, animal: str, was_correct: bool):
        """
        Update an animal's success rate in the database to improve future predictions
        
        Args:
            animal: The animal that was guessed or corrected
            was_correct: Whether the guess was correct
        """
        import json
        import os
        
        animals_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'animals.json')
        
        if not os.path.exists(animals_path):
            return
        
        try:
            with open(animals_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                animals = data.get('animals', [])
            
            # Calculate the yes percentage from this game
            if self.game_history:
                yes_count = sum(1 for _, answer in self.game_history if answer)
                total = len(self.game_history)
                path_percentage = (yes_count / total) * 100
                
                # Find and update the animal
                found = False
                for animal_data in animals:
                    if animal_data.get('name') == animal:
                        found = True
                        # Adjust the percentage slightly toward the actual path if correct
                        if was_correct:
                            current_pct = animal_data.get('yes_percentage', 50)
                            # Move 10% toward the actual percentage
                            new_pct = current_pct * 0.9 + path_percentage * 0.1
                            animal_data['yes_percentage'] = round(new_pct, 1)
                        break
                
                # If animal not in database and guess was correct, add it
                if not found and was_correct:
                    animals.append({
                        'name': animal,
                        'yes_percentage': round(path_percentage, 1)
                    })
                
                # Save back to file
                data['animals'] = animals
                with open(animals_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error updating animal database: {e}")
    
    def _update_animal_in_database(self, animal: str):
        """Add a newly learned animal to the database with current path percentage"""
        if not self.game_history:
            return
        
        yes_count = sum(1 for _, answer in self.game_history if answer)
        total = len(self.game_history)
        path_percentage = (yes_count / total) * 100
        
        import json
        import os
        
        animals_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'animals.json')
        
        try:
            if os.path.exists(animals_path):
                with open(animals_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'animals': []}
            
            animals = data.get('animals', [])
            
            # Check if animal already exists
            exists = any(a.get('name') == animal for a in animals)
            if not exists:
                animals.append({
                    'name': animal,
                    'yes_percentage': round(path_percentage, 1)
                })
                
                data['animals'] = animals
                with open(animals_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error adding animal to database: {e}")
    
    def get_tree_height(self) -> int:
        """
        Calculate the height of the tree
        
        Returns:
            Height of the tree (0 for single node, -1 for empty tree)
        """
        return self._calculate_height(self.root)
    
    @staticmethod
    def _calculate_height(node: Optional[Node]) -> int:
        """
        Recursively calculate height of subtree
        
        Args:
            node: Node to calculate height from
            
        Returns:
            Height of the subtree
        """
        if node is None:
            return -1
        return 1 + max(
            BinaryTree._calculate_height(node.left_child),
            BinaryTree._calculate_height(node.right_child)
        )
    
    def get_node_count(self) -> int:
        """
        Count total number of nodes in the tree
        
        Returns:
            Total number of nodes
        """
        return self._count_nodes(self.root)
    
    @staticmethod
    def _count_nodes(node: Optional[Node]) -> int:
        """Recursively count nodes"""
        if node is None:
            return 0
        return 1 + BinaryTree._count_nodes(node.left_child) + BinaryTree._count_nodes(node.right_child)
    
    def get_leaf_count(self) -> int:
        """
        Count number of leaf nodes (animals)
        
        Returns:
            Number of animals (leaves) in the tree
        """
        return self._count_leaves(self.root)
    
    @staticmethod
    def _count_leaves(node: Optional[Node]) -> int:
        """Recursively count leaves"""
        if node is None:
            return 0
        if node.is_leaf:
            return 1
        return BinaryTree._count_leaves(node.left_child) + BinaryTree._count_leaves(node.right_child)
    
    def get_average_depth(self) -> float:
        """
        Calculate average depth of leaf nodes (average questions per game)
        
        Returns:
            Average depth of leaves (lower is better)
        """
        leaves = self._count_leaves(self.root)
        if leaves == 0:
            return 0
        total_depth = self._sum_leaf_depths(self.root, 0)
        return total_depth / leaves
    
    @staticmethod
    def _sum_leaf_depths(node: Optional[Node], depth: int) -> int:
        """Recursively sum depths of all leaves"""
        if node is None:
            return 0
        if node.is_leaf:
            return depth
        return (BinaryTree._sum_leaf_depths(node.left_child, depth + 1) +
                BinaryTree._sum_leaf_depths(node.right_child, depth + 1))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the tree
        
        Returns:
            Dictionary with tree statistics
        """
        return {
            'height': self.get_tree_height(),
            'total_nodes': self.get_node_count(),
            'leaf_count': self.get_leaf_count(),
            'average_depth': round(self.get_average_depth(), 2),
            'balance_factor': self._calculate_balance_factor()
        }
    
    def _calculate_balance_factor(self) -> float:
        """
        Calculate balance factor of the tree (0 = perfectly balanced, 1 = completely unbalanced)
        
        Returns:
            Balance factor between 0 and 1
        """
        height = self.get_tree_height()
        if height <= 0:
            return 0
        
        # Compare actual height with optimal height for perfect tree
        leaves = self.get_leaf_count()
        if leaves <= 1:
            return 0
        
        import math
        optimal_height = math.ceil(math.log2(leaves))
        balance = (height - optimal_height) / height if height > 0 else 0
        return max(0, min(1, balance))  # Clamp between 0 and 1
    
    def get_all_animals(self) -> List[str]:
        """
        Get list of all known animals in the tree
        
        Returns:
            List of animal names (leaf nodes)
        """
        animals = []
        self._collect_animals(self.root, animals)
        return animals
    
    @staticmethod
    def _collect_animals(node: Optional[Node], animals: List[str]):
        """Recursively collect all animals from the tree"""
        if node is None:
            return
        if node.is_leaf:
            animals.append(node.data)
        else:
            BinaryTree._collect_animals(node.left_child, animals)
            BinaryTree._collect_animals(node.right_child, animals)
    
    def display_tree(self, node: Optional[Node] = None, prefix: str = "", 
                     is_left: Optional[bool] = None) -> str:
        """
        Display tree structure in a readable format with proper ASCII art
        
        Args:
            node: Node to display (default: root)
            prefix: Prefix for indentation
            is_left: Whether this is a left child
            
        Returns:
            String representation of tree
        """
        if node is None:
            node = self.root
        
        if node is None:
            return "Empty tree"
        
        result = []
        self._display_tree_recursive(node, "", None, result)
        return "\n".join(result)
    
    @staticmethod
    def _display_tree_recursive(node: Node, prefix: str, is_left: Optional[bool], 
                               result: List[str]):
        """Recursively build tree display with proper formatting"""
        if node is None:
            return
        
        # Format the node display
        node_label = node.data
        if node.is_leaf:
            node_display = f"🐾 {node_label}"
        else:
            node_display = f"❓ {node_label}"
        
        # Add the node with appropriate connector
        if is_left is None:  # Root node
            result.append(node_display)
            new_prefix = ""
        else:
            # Determine the connector and extension
            if is_left:
                connector = "├─ YES  ↙"
                extension = "│       "
            else:
                connector = "└─ NO   ↘"
                extension = "        "
            
            result.append(prefix + connector)
            result.append(prefix + extension + node_display)
            new_prefix = prefix + extension
        
        # Recursively add children
        if not node.is_leaf:
            if node.left_child:
                BinaryTree._display_tree_recursive(node.left_child, new_prefix, True, result)
            if node.right_child:
                BinaryTree._display_tree_recursive(node.right_child, new_prefix, False, result)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire tree to dictionary"""
        return self.root.to_dict() if self.root else None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BinaryTree':
        """Create tree from dictionary"""
        root = Node.from_dict(data)
        return cls(root)
