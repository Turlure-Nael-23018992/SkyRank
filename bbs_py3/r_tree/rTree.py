#!/usr/bin/python

from node import Node
from Key import Key
from NodeType import NodeType
from mbr import MBR


class RTree():
    """R-Tree Class"""

    def __init__(self, M, m):
        self.M = M
        self.m = m
        self.root = Node()

    def Insert(self, tupleId, minDim, maxDim):
        """
        Insert a new tuple Key in the tree.
        """
        # Create the key to insert
        mbr = MBR(minDim, maxDim)
        K = Key(tupleId, mbr)

        # Find position for new record
        leafNode = self.ChooseLeaf(self.root, K)
        K.node = leafNode

        N1 = None
        N2 = None

        # Add record to leaf if it has space
        if not leafNode.IsFull(self.M):
            leafNode.keys.append(K)
            N1 = leafNode
        # Else make a split after adding node to leaf
        else:
            leafNode.keys.append(K)
            N1, N2 = leafNode.Split(self.m)

        # Now adjust the tree
        self.AdjustTree(N1, N2)

    def ChooseLeaf(self, N, K):
        """
        Find the leaf node for a new Key in the tree.
        """
        if N.nodeType == NodeType.leaf:
            return N

        # Initialization
        minExpandableArea = float("inf")
        L = Node()

        for key in N.keys:
            combinedArea = key.mbr.combine(K.mbr)
            expandableArea = combinedArea.area() - key.mbr.area()

            if minExpandableArea > expandableArea:
                minExpandableArea = expandableArea
                L = key.childNode
            elif minExpandableArea == expandableArea:
                if L.MBR().area() > key.mbr.area():
                    L = key.childNode

        return self.ChooseLeaf(L, K)

    def AdjustTree(self, N1, N2=None):
        """
        Ascend from a leaf node to the root, adjusting covering rectangles,
        and propagating node splits if necessary.
        """
        # Check if done
        if N1.parent is None:
            # Reached the root
            if N2 is not None:
                # Root was split
                self.MakeRoot(N1, N2)
            return

        # Update the parent's MBR for N1
        N1.parent.mbr = N1.MBR()

        # Get the parent node
        parentNode = N1.parent.node

        # If the node was split, make a new parent node and adjust
        if N2 is not None:
            # Make a new key which is the parent of the split node
            newKey = Key(mbr=N2.MBR(), node=parentNode)
            N2.parent = newKey
            newKey.childNode = N2

            # Add this new key to the parent of N1 if it is not full
            if not parentNode.IsFull(self.M):
                parentNode.keys.append(newKey)
                return self.AdjustTree(parentNode, None)
            else:
                parentNode.keys.append(newKey)
                N, NN = parentNode.Split(self.m)
                return self.AdjustTree(N, NN)
        else:
            # Adjust the parent node
            return self.AdjustTree(parentNode, None)

    def MakeRoot(self, N1, N2):
        """
        Make a new root with the given two nodes resulting from a split.
        """
        if N1.nodeType != NodeType.leaf:
            N1.nodeType = NodeType.node
        if N2.nodeType != NodeType.leaf:
            N2.nodeType = NodeType.node

        # Create a new root node
        self.root = Node(nodeType=NodeType.root)

        # Create key for N1
        newKey = Key(mbr=N1.MBR(), node=self.root)
        N1.parent = newKey
        newKey.childNode = N1
        self.root.keys.append(newKey)

        # Create key for N2
        newKey = Key(mbr=N2.MBR(), node=self.root)
        N2.parent = newKey
        newKey.childNode = N2
        self.root.keys.append(newKey)