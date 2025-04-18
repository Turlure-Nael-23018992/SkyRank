#!/usr/bin/ python

"""
Skylines using Branch and bound with R-tree as a data structure
usage: python Skyline.py queryFile dataFile
arguments:
queryFile : file that contains query data for getting skylines
dataFile  : file from which we want to get skylines
"""
from RTree.rTree import RTree
from Bbs.Bbs import Bbs
import sys
import getopt
import time

def main(argv=None):


	if argv is None:
		argv = sys.argv
	# parse command line options
	try:
		opts, args = getopt.getopt(argv[1:], "h", ["help"])
	except getopt.error as msg:
		print(msg)
		print("for help use --help")
		sys.exit(2)
	# process options
	for o, a in opts:
		if o in ("-h", "--help"):
			print(__doc__)
			sys.exit(0)
	# process arguments
	if len(args) == 2:
		queryFileName = args[0]
		dataFileName = args[1]
	else:
		print("Program requires two files names as arguments.")
		print("for help use --help")
		sys.exit(2)
		
	# open the query file
	startTime1 = time.time()

	queryFile = open(queryFileName, 'r')

	# get the dimensions on which skylines needs to be calculated
	dimns = list(map(int, queryFile.readline().split()))

	# get the disk page size from query file
	diskPageSize  = list(map(int, queryFile.readline().split()))[0]
	# get the size of pointer and keys from query file
	pointers, keys = list(map(int, queryFile.readline().split()))
	print(f"diskPageSize, pointers, keys:{diskPageSize, pointers, keys}")


	# close the file
	queryFile.close()
	# calculate the maximum node size allowed for R-tree 
	# a node containes M keys, respectively M pointers to their child nodes
	# so value of M for a given disk access
	M = diskPageSize/(pointers + keys)

	# set minimum size allowed for a node
	m = M/2

	# create R-Tree object for M and m
	rTree = RTree(M, m)

	# now fill the rTree with data file
	fillRTree(dataFileName, dimns, rTree)

	print("##### Time till Rtree build #####")
	print(str((time.time() - startTime1)*1000) + "ms")

	startTime2 = time.time()


	# now we have created our R-Tree in rTree
	# so run the skyline algorithm Branch and Bound Skyline (BBS)
	# to get the skylines
	
	# create instance of BBS class with rTree
	bbs = Bbs(rTree)
	
	# get the skyline from rTree
	skylines, comparisions = bbs.skyline(1, 2)

	print("##### Time for BBS algorithm #####")
	print(str((time.time() - startTime2)*1000) + "ms")


	print("##### Total running time #####")
	print(str((time.time() - startTime1)*1000) + "ms")

	print("#### Object to object comparitions ####")
	print(comparisions)

	print("##### Skyline from data set #####")
	print("Number of skylines:"+ str(len(skylines)))



	# print skylines ids
	#printSkylineIds(skylines)

	# now print skylines
	#printSkylines(skylines, dataFileName)

	r = skylines_to_list(skylines, dataFileName)
	print("\n".join([str(x) for x in r]))
	

# function to fill the rTree with input data file
def fillRTree(dataFileName, dimns, rTree):
	# open the sample data file
	sampleData = open(dataFileName,'r')

	for row in sampleData:
		inputTuple = list(map(float, row.split()))
		tupleId = int(inputTuple[0])
		attrValue = inputTuple[1:]
		minMbr = []
		for dimn in dimns:
			minMbr.append(attrValue[dimn-1])
		print(f"minMbr:{minMbr}")
		print(f"attrValue:{attrValue}")
		print()
		# insert into rTree
		# rTree.Insert(tupleId, mbrMin, mbrMax)
		rTree.Insert(tupleId, minMbr, minMbr)	
	# close the file
	sampleData.close()

# print skylines ids
def printSkylineIds(skylines):
	for skyline in skylines:
		print(skyline.tupleId)


# function to print skylines
def printSkylines(skylines, dataFileName):
	# sort the skylines by tupleId
	skylines.sort(key=lambda item: item.tupleId)
	# print skylines
	sampleData = open(dataFileName, 'r')
	j = 0
	for i, row in enumerate(sampleData):
		# get the next skyline
		if len(skylines) == j:
			break
   	
		skyline = skylines[j]
		# check if current row in file is a skyline or not
		tupleId = int(row.strip().split(" ")[0])
		if skyline.tupleId == tupleId:

			#if skyline.tupleId == i + 1:
			print(row.strip())
			j += 1
		elif (i+1) > skyline.tupleId:
			break
	# close the sample data file
	sampleData.close()


# function to print skylines
def skylines_to_list(skylines, dataFileName):
	sky_list=[[] for _ in range(len(skylines))]

	# sort the skylines by tupleId
	skylines.sort(key=lambda item: item.tupleId)
	# print skylines
	sampleData = open(dataFileName, 'r')
	j = 0
	idx=0
	for i, row in enumerate(sampleData):
		# get the next skyline
		if len(skylines) == j:
			break

		skyline = skylines[j]
		# check if current row in file is a skyline or not
		if skyline.tupleId == i + 1:
			raw_elem= [float(x) if x.count('.') else int(x)  for x in row.strip().replace('\t',' ').split(' ') if x.count(' ') == 0 and x != '']
			sky_list[idx] = raw_elem
			j += 1
			idx += 1
		elif (i + 1) > skyline.tupleId:
			break
	# close the sample data file
	sampleData.close()
	return sky_list



# main function
if __name__ == "__main__":
	main()
	
