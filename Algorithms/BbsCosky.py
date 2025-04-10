from Utils.DisplayHelpers import beauty_print
from BbsPy3.Bbs.Bbs import Bbs
from BbsPy3.RTree.rTree import RTree


class BbsCosky:
    '''
    BBS Algorithm
    '''
    DISK_PAGE_SIZE=2048
    POINTER=4
    KEYS=8
    # calculate the maximum node size allowed for R-tree
    # a node containes M keys, respectively M pointers to their child nodes
    # so value of M for a given disk access
    M=DISK_PAGE_SIZE/(POINTER+KEYS)
    def __init__(self, relation, sp, layer, minIdp={}):
        self.relation=relation
        self.minIdp=minIdp
        self.sp=sp
        self.layer=layer
        # create R-Tree object for M and m
        self.rTree = RTree(BbsCosky.M, BbsCosky.M/2)
        # now fill the rTree with data file
        self.fillRTree()
        # create instance of BBS class with rTree
        self.bbs = Bbs(self.rTree)
        # get the skyline from rTree
        self.skylines, self.comparisions, self.lm, self.minIdp, self.see = self.bbs.skyline(self.sp, self.layer, self.minIdp)
        self.skyline=self.skylines_to_dict(self.skylines)

    # function to fill the rTree with dictionnary
    def fillRTree(self):
        for k,v in self.relation.items():
            self.rTree.Insert(k, v, v)

    def skylines_to_dict(self, skylines):
        # sort the skylines by tupleId
        skylines.sort(key=lambda item: item.tupleId)
        sky_dict = {sky.tupleId:self.relation[sky.tupleId] for sky in skylines}
        return sky_dict




if __name__ == '__main__':
    r_big = {
        1: (5, 20, 0.014285714),
        2: (4, 60, 0.02),
        3: (5, 30, 0.016666667),
        4: (1, 80, 0.016666667),
        5: (5, 90, 0.025),
        6: (9, 30, 0.02),
        7: (7, 80, 0.025),
        8: (9, 90, 0.033333333)
    }

    bbs_cosky=BbsCosky(r_big, 1, 2)
    beauty_print("skyline",bbs_cosky.skyline)