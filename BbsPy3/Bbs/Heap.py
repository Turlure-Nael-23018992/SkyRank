#!/usr/bin/python

from heapq import *  # Import useful functions from heapq (heappush, heappop, etc.)


class Heap():
    """
    Class representing a heap used for the skyline algorithm
    """

    def __init__(self, rootNode):
        """
        Constructor: initializes the heap with the keys of the root node of the R-tree.

        Each element is inserted into the heap with a priority based on its MBR
        (Minimum Bounding Rectangle).
        """
        self.heap = []  # Initializing an empty heap
        for key in rootNode.keys:
            # Each element is stored as a tuple: (priority, element)
            heappush(self.heap, (key.mbr.priority(), key))

    def deleteMin(self):
        """
        Removes and returns the element with the lowest priority from the heap.
        This is the most promising element according to the chosen heuristic.
        """
        return heappop(self.heap)

    def enqueue(self, node):
        """
        Inserts all children of a node into the heap with their priority.

        Useful when exploring an internal node of the R-tree.
        """
        for key in node.keys:
            heappush(self.heap, (key.mbr.priority(), key))

    def size(self):
        """
        Returns the number of elements currently in the heap.
        Used to check if the queue is empty or not.
        """
        return len(self.heap)
