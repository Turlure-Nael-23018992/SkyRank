import math
import time
import json

from Algorithms.BbsCosky import BbsCosky
from Utils.DisplayHelpers import beauty_print


class CoskyAlgorithme:
    '''
    Classe qui utilise l'algorithme Cosky en version algorithme
    '''

    def __init__(self, r, is_debug=False):
        self.is_debug=is_debug
        self.r = r
        self.bbs = BbsCosky(r, 1, 2)
        self.s= {k:list(v) for k,v in self.bbs.skyline.items()}
        #beauty_print("s",self.s)
        self.data_keys=self.s.keys()
        self.n = len(self.s)
        self.m = len(list(self.s.values())[0])
        self.tot=[0]*self.m
        self.ni={k:[0]*len(v) for k,v in self.s.items()}
        self.gini=[0]*self.m
        self.totGini=0
        self.totNN=[0]*self.m
        self.p = {k:[0]*len(v) for k,v in self.s.items()}
        self.totPP={k:0 for k in self.data_keys}
        self.ideal=[1]*self.m
        self.totIdealIdeal=0
        self.sqrtTotPP= {k:0 for k in self.data_keys}
        self.sqrtTotIdealIdeal=0
        self.totIdealP=0
        self.run()




    def run(self):
        # for each key (row) of s
        for i in self.data_keys:
            # for each element of s's values (column)
            for j in range(self.m):
                self.tot[j]+=self.s[i][j]
        if self.is_debug:
            beauty_print("tot",self.tot)
        # for each key (row) of s
        for i in self.data_keys:
            # for each element of s's values (column)
            for j in range(self.m):
                self.ni[i][j]=self.s[i][j] / self.tot[j]
                self.totNN[j]+=pow(self.ni[i][j],2)
        if self.is_debug:
            beauty_print("ni", self.ni)
            beauty_print("totNN", self.totNN)
        # for each element of s's values (column)
        for j in range(self.m):
            self.gini[j]=1-self.totNN[j]
            self.totGini+=self.gini[j]
        if self.is_debug:
            beauty_print("gini", self.gini)
            beauty_print("totGini", self.totGini)
        # for each key (row) of s
        for i in self.data_keys:
            # for each element of s's values (column)
            for j in range(self.m):
                self.p[i][j]=self.gini[j]/self.totGini*self.ni[i][j]
                p_i_j=self.p[i][j]
                self.totPP[i]+=pow(p_i_j, 2)
                if p_i_j<self.ideal[j]:
                    self.ideal[j]=p_i_j
        if self.is_debug:
            beauty_print("p", self.p)
            beauty_print("totPP", self.totPP)
            beauty_print("ideal", self.ideal)
        # for each element of s's values (column)
        for j in range(self.m):
            self.totIdealIdeal+=pow(self.ideal[j], 2)
        if self.is_debug:
            beauty_print("totIdealIdeal", self.totIdealIdeal)
        # for each key (row) of s
        """
        for i in self.data_keys:
            self.sqrtTotPP[i]=math.sqrt(self.totPP[i])
        """
        self.sqrtTotIdealIdeal=math.sqrt(self.totIdealIdeal)
        if self.is_debug:
            beauty_print("sqrtTotPP", self.sqrtTotPP)
            beauty_print("sqrtTotIdealIdeal", self.sqrtTotIdealIdeal)
        # for each key (row) of s

        for i in self.data_keys:
            self.totIdealP=0
            # for each element of s's values (column)

            for j in range(self.m):
                self.totIdealP+=self.ideal[j]*self.p[i][j]
            val=self.totIdealP / (math.sqrt(self.totPP[i]) * self.sqrtTotIdealIdeal)
            self.s[i].append(val)
        if self.is_debug:
            beauty_print("totIdealP", self.totIdealP)
        return self.s

    def sort(self,rev):
        reverse = True if rev == "Desc" else False
        self.s = dict(sorted(self.s.items(), key=lambda item: item[1][-1], reverse=reverse))

if __name__ == '__main__':
    r_petit = {
        1: (5, 20, 0.014285714),
        2: (4, 60,0.02),
        3: (5, 30, 0.016666667),
        4: (1, 80, 0.016666667),
        5: (5, 90, 0.025),
        6: (9, 30, 0.02),
        7: (7, 80, 0.025),
        8: (9, 90, 0.033333333)
    }

    with open ("Datas/RBig.json", "r") as f:
        r_big = json.load(f)

    r = {
        1: (5, 20, 1 / 70),
        2: (4, 60, 1 / 50),
        4: (1, 80, 1 / 60)
    }


    startTime = time.time()
    cosky = CoskyAlgorithme(r_petit)
    print("-----------------Avant-----------------")
    print(cosky.s)
    print(f"temps: {time.time() - startTime}")
    print("-----------------Apres-----------------")
    cosky.sort("Desc")
    print(cosky.s)
