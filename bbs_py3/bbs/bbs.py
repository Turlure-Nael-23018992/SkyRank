#!/usr/bin/ python

from .heap import Heap

class BBS():
	"""class for Branch and Bound algorith"""
	def __init__(self, tree):
		self.tree = tree
		
	"""
	Get skylines from tree and return
	"""
	def skyline(self, sp, layer, minIdp={}):
		lm = {}
		#minIdp = {}
		see = 0


		# now create the priority heap for skylines with rTree.root
		prHeap = Heap(self.tree.root)
		# create empty skyline set
		skylines = []

		# initialize the comparision
		comparirions = 0
		# loop through heap untill it's not empty
		while prHeap.size() != 0:
			# 
			dominated = False
			# get the minimum heap key for next iteration
			# this is a (pripority, key) tuple
			heapItem = prHeap.deleteMin()
			
			# get the key value from heap item
			key = heapItem[1]

			# loop through all the skylines for dominance for this key
			for item in skylines:
				# check for dominance of key with items in skyline set
				comparirions += 1
				if(item.mbr.dominates(key.mbr)):
					if (key.tupleId == None and key.childNode != None):
						for item in key.childNode.keys:
							lm[item.tupleId] = layer
							if minIdp.get(item.tupleId):
								minIdp[item.tupleId] += 1
							else:
								minIdp[item.tupleId]= 1
							see = see + 1
							#print(sp, "dominates", item.tupleId, "(c)")
					else:
						if (item.tupleId == sp):
							lm[key.tupleId] = layer
							if minIdp.get(key.tupleId):
								minIdp[key.tupleId] += 1
							else:
								minIdp[key.tupleId] = 1
							see = see + 1
							#print(sp, "dominates", key.tupleId)

					# key is dominated by a skyline
					# so continue with another key
					dominated = True
					break
			if dominated:
				# key is domintated and is removed from heap
				# so continue with next key
				continue

			# key is not dominated 
			if(key.childNode != None):
				# we are not at leaf node
				# do the expansions
				prHeap.enqueue(key.childNode)
			else:
				# we are at leap and found a tuple, so insert it into skyline set
				skylines.append(key)
		"""
		print("============================================================")
		print("sp=", sp)
		print("layer=", layer)
		print("lm=", lm)
		print("minIdp=", minIdp)
		print("see=", see)
		print("\===========================================================")
		"""
		# now return the skyline set
		return skylines, comparirions, lm, minIdp, see
