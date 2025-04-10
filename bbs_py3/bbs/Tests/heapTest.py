import unittest
from bbs_py3.bbs.heap import Heap
from bbs_py3.r_tree.node import Node
from bbs_py3.r_tree.Key import Key
from bbs_py3.r_tree.mbr import MBR

class heapTest(unittest.TestCase):
    """
    Test class for the heap.
    """

    def setUp(self):
        """
        Setup method to initialize the heap instance.
        """
        # Initialize the keys
        self.key1 = Key(tupleId=1, mbr=MBR([1, 2], [3, 4]))
        self.key2 = Key(tupleId=2, mbr=MBR([5, 6], [7, 8]))
        self.key3 = Key(tupleId=3, mbr=MBR([9, 10], [11, 12]))
        # Initialize the root node with the keys
        self.root_node = Node()
        self.root_node.keys = [self.key1, self.key2, self.key3]
        # Initialize the heap with the root node
        self.heap = Heap(self.root_node)

    def test_initialization(self):
        """
        Test the initialization of the heap.
        """
        # Check if the heap contains 3 keys
        self.assertEqual(self.heap.size(), 3)

    def test_delete_min(self):
        """
        Test the deleteMin method of the heap.
        """
        # Delete the minimum element from the heap
        min_element = self.heap.deleteMin()
        # Check if the deleted element is the one with the lowest priority
        self.assertEqual(min_element[1], self.key1)
        # Check if the heap size is now 2
        self.assertEqual(self.heap.size(), 2)

    def test_enqueue(self):
        """
        Test the enqueue method of the heap.
        """
        # Create a new node with a new key
        new_key = Key(tupleId=4, mbr=MBR([13, 14], [15, 16]))
        new_key2 = Key(tupleId=5, mbr=MBR([17, 18], [19, 20]))
        new_node = Node()
        new_node.keys = [new_key, new_key2]
        # Enqueue the new node into the heap
        self.heap.enqueue(new_node)
        # Check if the heap size is now 5
        self.assertEqual(self.heap.size(), 5)

