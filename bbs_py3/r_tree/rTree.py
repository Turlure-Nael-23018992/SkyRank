#!/usr/bin/ python

from .node import *

class RTree():
  """R-Tree Class"""
  def __init__(self, M, m):
    self.M = M
    self.m = m
    self.root = Node()


  '''
  K = Key()
  Insert new tuple Key in tree
  '''
  def Insert(self, tupleId, minDim, maxDim):
      
    # create the key to insert
    mbr = MBR(minDim, maxDim)
    K = Key(tupleId, mbr)

    # Find position for new record
    leafNode = self.ChooseLeaf(self.root, K)
    K.node = leafNode

    N1 = None
    N2 = None

    # add record to leaf if it has space
    if not leafNode.IsFull(self.M):
      leafNode.keys.append(K)
      N1 = leafNode
    # else make a split after adding node to leaf
    else:
      leafNode.keys.append(K)
      N1, N2 = leafNode.Split(self.m)
    # now adjust the tree
    self.AdjustTree(N1, N2)

  '''
  K = Key()
  Find leaf node for new Key in tree
  '''
  def ChooseLeaf(self, N, K):
    if(N.nodeType == NodeType.leaf):
      return N
    # intialization 
    minExpandableArea = float("inf")
    L = Node()

    for key in N.keys:
      combinedArea = key.mbr.combine(K.mbr)                        
      expandableArea = combinedArea.area() - key.mbr.area()
      
      if(minExpandableArea == None or minExpandableArea > expandableArea):
        minExpandableArea = expandableArea
        L = key.childNode
      elif(minExpandableArea == expandableArea):
        if L.MBR().area() > key.mbr.area():
          L = key.childNode
    return self.ChooseLeaf(L, K)

  '''
  N = leafNode
  NN = if N was previously splitted
  Ascend from a leaf node L to the root, adjusting covering rectangles,
  and propagating node splits if necessary
  '''
  def AdjustTree(self, N1, N2 = None):
    # check if done
    if(N1.parent == None):
      # reached at root
      if(N2 != None):
        # root was splitted
        self.MakeRoot(N1, N2)
      return 

    # update the parents mbr for N1
    N1.parent.mbr = N1.MBR()

    # get the parent node
    parentNode = N1.parent.node


    # if previously node was splitted, make a new parent node and 
    # then do some adjustment
    if N2 != None:
     # make a new key which is parent of splited node
      newKey = Key(mbr=N2.MBR(), node=parentNode)
      N2.parent = newKey
      newKey.childNode = N2
      # add this new key to parent of N1 if it is not full 
      # else add and split parent
      if not parentNode.IsFull(self.M):
        parentNode.keys.append(newKey)
        return self.AdjustTree(parentNode, None)
      else:
        parentNode.keys.append(newKey)
        N, NN = parentNode.Split(self.m)
        return self.AdjustTree(N, NN)
    # else Adjust the parent node
    else:
      return self.AdjustTree(parentNode, None)


  '''
  Make a root with given two nodes which are result of a split
  '''
  def MakeRoot(self, N1, N2):

    if(N1.nodeType != NodeType.leaf):
      N1.nodeType = NodeType.node
    if(N2.nodeType != NodeType.leaf):
      N2.nodeType = NodeType.node

     # create a new node
    self.root = Node(nodeType=NodeType.root)
    # create key for N1
    newKey = Key(mbr=N1.MBR(), node=self.root)
    N1.parent = newKey
    newKey.childNode = N1
    
    self.root.keys.append(newKey)
    # create key for N2
    newKey = Key(mbr=N2.MBR(), node=self.root)
    N2.parent = newKey
    newKey.childNode = N2
    self.root.keys.append(newKey)
   