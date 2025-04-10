#!/usr/bin/python

from .heap import Heap


class BBS():
    """BBS Algorithm Class"""

    def __init__(self, tree):
        # R-Tree structure
        self.tree = tree

    def skyline(self, sp, layer, minIdp={}):
        """
        Computes the skyline points from the R-Tree.

        Arguments:
        - sp: source point identifier (for tracking)
        - layer: layer level (useful for multi-layer skylines)
        - minIdp: dictionary of dominations per point

        Returns:
        - list of skyline points
        - number of dominance comparisons performed
        - dictionary of dominated points at this level
        - updated minIdp
        - total number of dominated points
        """

        lm = {}  # Dictionary of dominated points
        see = 0   # Counter for dominated points

        # Heap initialization
        prHeap = Heap(self.tree.root)

        # List of skyline points (non-dominated)
        skylines = []

        # Dominance comparison counter
        comparirions = 0

        # Process elements in the heap until it's empty
        while prHeap.size() != 0:
            dominated = False  # Dominance status of the current element

            # Retrieve the highest-priority element from the heap
            heapItem = prHeap.deleteMin()
            key = heapItem[1]  # Key (node or point) to analyze

            # Check if 'key' is dominated by any existing skyline point
            for item in skylines:
                comparirions += 1
                if (item.mbr.dominates(key.mbr)):
                    # Case 1: 'key' is an internal node (not a leaf point)
                    if (key.tupleId == None and key.childNode != None):
                        for item in key.childNode.keys:
                            lm[item.tupleId] = layer
                            if minIdp.get(item.tupleId):
                                minIdp[item.tupleId] += 1
                            else:
                                minIdp[item.tupleId] = 1
                            see += 1
                    else:
                        # Case 2: 'key' is a dominated (leaf) point
                        if (item.tupleId == sp):
                            lm[key.tupleId] = layer
                            if minIdp.get(key.tupleId):
                                minIdp[key.tupleId] += 1
                            else:
                                minIdp[key.tupleId] = 1
                            see += 1

                    # If 'key' is dominated, discard it
                    dominated = True
                    break

            if dominated:
                # If the element is dominated, move to the next one
                continue

            # If the element is not dominated:
            if (key.childNode != None):
                # Case: It's an internal node -> explore its children
                prHeap.enqueue(key.childNode)
            else:
                # Case: It's a leaf point -> add it to the skyline
                skylines.append(key)

        # Return the results
        return skylines, comparirions, lm, minIdp, see

"""
        print("============================================================")
        print("sp=", sp)
        print("layer=", layer)
        print("lm=", lm)
        print("minIdp=", minIdp)
        print("see=", see)
        print("\===========================================================")
"""