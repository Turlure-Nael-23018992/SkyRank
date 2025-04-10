from enum import Enum

class NodeType(Enum):
    """Node types in R-Tree"""
    root = 1
    node = 2
    leaf = 3