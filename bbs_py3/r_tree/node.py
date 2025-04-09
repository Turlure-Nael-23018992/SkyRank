#!/usr/bin/ python
#import six
from .enum import Enum
from .mbr import MBR

class NodeType(Enum):
    """Node types in R-Tree"""
    root = 1
    node = 2
    leaf = 3

class Key():
    """Key for R-Tree"""
    def __init__(self, tupleId=None, mbr=None, node=None, childNode=None):
        self.mbr = mbr
        self.tupleId = tupleId
        self.node = node
        self.childNode = childNode

    def __lt__(self, other):
        if other:
            return self.mbr.priority() < other.mbr.priority()

    def __repr__(self):
        return f"""
    mbr:{self.mbr}
    tupleId:{self.tupleId}
    node:{self.node}
    childNode:{self.childNode}
    """




class Node():
    """Node Structure"""
    def __init__(self,  nodeType=NodeType.leaf):
        self.parent = None
        self.keys = []
        self.nodeType = nodeType

    def __repr__(self):
        return f"""
    nodeType:{self.nodeType}

    """

    '''
    Split the current node to resolve the overflow
    Using Quadratic split
    '''
    def Split(self, m):
        # split into key1 and key2
        K1, K2 = self.PickSeed()
        self.keys.remove(K1)
        self.keys.remove(K2)
        # create two intially nodes
        N1 = Node(self.nodeType)
        N1.keys.append(K1)
        N1.parent = self.parent
        if self.parent != None:
            self.parent.childNode = N1

        
        N2 = Node(self.nodeType)
        N2.keys.append(K2)

        while(len(self.keys) > 0):

            # check for shortage in any group
            if(len(N1.keys) + len(self.keys) < m):
                for key in self.keys:
                    N1.keys.append(key)
                self.keys = []
                break
            elif(len(N2.keys) + len(self.keys) < m):
                for key in self.keys:
                    N2.keys.append(key)
                self.keys = []
                break

            # get the next key for insertion in a group    
            nextKey = self.PickNext(N1, N2)
            
            mbrN1 = N1.MBR()
            mbrN2 = N2.MBR()
            # get the enlargement in both groups after adding new key
            enlargementInN1 = mbrN1.combine(nextKey.mbr).area()
            enlargementInN2 = mbrN2.combine(nextKey.mbr).area()

            # add the new key to the group with least enlargement
            if(enlargementInN1 <= enlargementInN2 ):
                nextKey.node = N1
                N1.keys.append(nextKey)
            else:
                nextKey.node = N2
                N2.keys.append(nextKey)
            
            self.keys.remove(nextKey)

        # update node property for all keys in N1 and N2
        for key in N1.keys:
            key.node = N1
        for key in N2.keys:
            key.node = N2
        # return the splited two nodes
        return [N1, N2]

    '''
    PickSeed Subroutine for Quadratic split
    Return two seed keys
    '''
    def PickSeed(self):
        # intialization
        # intialize keys to empty nodes
        K1 = Key()
        K2 = Key() 
        # intialize max expanable area to minimum
        maxExpandableArea = -float("inf")
        
        # get some values from self node for use
        keys = self.keys
        keysCount = len(self.keys)

        for i in range(0, keysCount):
            key1 = keys[i]
            for j in range(i+1, keysCount):
                key2 = keys[j]
                # get the combined region of key1 and key2
                combinedRegion = key1.mbr.combine(key2.mbr)
                # calculate the expandable area b
                expandableArea = combinedRegion.area() - key1.mbr.area() - key2.mbr.area()
                # update area and nodes for out put
                if(expandableArea > maxExpandableArea):
                    maxExpandableArea = expandableArea
                    K1 = key1
                    K2 = key2
        # return Node list            
        return [K1, K2]

    '''
    Subroutine for Quadratic split
    N = 
    '''
    def PickNext(self, N1, N2):
        # intialize max expanable area to minimum
        maxExpandableArea = -float("inf")
        K1 = Key()

        # get mbr for N1 and N2
        tmp = Key()
        mbrN1 = N1.MBR()
        mbrN2 = N2.MBR()
        
        for key in self.keys:
            # get the combined area by adding key to both N1 and N2
            X = mbrN1.combine(key.mbr)
            Y = mbrN2.combine(key.mbr)
            
            # get area difference of areas after addition and before addition 
            d1 = X.area() - mbrN1.area()
            d2 = Y.area() - mbrN2.area()
            
            # get the difference of these expandable areas
            expandableArea = abs(d1-d2)

            # update return key value if necessary
            if maxExpandableArea < expandableArea:
                maxExpandableArea = expandableArea
                K1 = key
        
        return K1


    '''
    Is Node full
    '''
    def IsFull(self, M):
        # check for root node 
        if(self.parent == None):
            if(len(self.keys) == 2):
                return True
            else:
                return False
        # check for other nodes
        if(len(self.keys) == M):
            return True
        return False

    '''
    Get the mbr for Node
    '''
    def MBR(self):
        keys = self.keys
        if(len(keys) > 0):
            mbr = MBR(keys[0].mbr.minDim, keys[0].mbr.maxDim)
            for key in keys[1:]:
                mbr = mbr.combine(key.mbr)  
            return mbr
        return None
        