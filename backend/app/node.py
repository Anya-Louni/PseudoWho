"""
Binary Tree Node Structure for PseudoQui Game
Implements nodes that can be either questions (internal nodes) or animals (leaf nodes)
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Represents a single node in the decision tree.
    
    Attributes:
        data: The content (question or animal name)
        is_leaf: True if this is a terminal node (animal), False if it's a decision node
        left_child: Child node for "Yes" answers
        right_child: Child node for "No" answers
        parent: Reference to parent node for tree navigation
    """
    data: str
    is_leaf: bool = False
    left_child: Optional['Node'] = None
    right_child: Optional['Node'] = None
    parent: Optional['Node'] = None
    
    def __post_init__(self):
        """Initialize child parent references"""
        if self.left_child:
            self.left_child.parent = self
        if self.right_child:
            self.right_child.parent = self
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert node to dictionary for JSON serialization
        
        Returns:
            Dictionary representation of the node
        """
        return {
            'data': self.data,
            'is_leaf': self.is_leaf,
            'left': self.left_child.to_dict() if self.left_child else None,
            'right': self.right_child.to_dict() if self.right_child else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """
        Create a node from dictionary representation
        
        Args:
            data: Dictionary representation of node
            
        Returns:
            Reconstructed Node object
        """
        if data is None:
            return None
        
        node = cls(
            data=data['data'],
            is_leaf=data['is_leaf']
        )
        
        if data.get('left'):
            node.left_child = cls.from_dict(data['left'])
            node.left_child.parent = node
        
        if data.get('right'):
            node.right_child = cls.from_dict(data['right'])
            node.right_child.parent = node
        
        return node
    
    def __repr__(self) -> str:
        """String representation of node"""
        node_type = "ANIMAL" if self.is_leaf else "QUESTION"
        return f"[{node_type}] {self.data}"
