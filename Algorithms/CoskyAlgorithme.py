"""
Cosky Algorithm
===============

This module implements the Cosky algorithm for ranking points in a dataset.
Cosky focuses on "diverse" ranking, aiming to find points that are part of 
the skyline and are representative of the overall dataset's variation.
"""
import math
import time

from Algorithms.BbsCosky import BbsCosky
from Utils.DataModifier.DatabaseToDict import DatabaseToDict
from Utils.Preference import Preference
from Utils.TimerUtils import TimeCalc
from Utils.DisplayHelpers import beauty_print
from Utils.DataModifier.JsonUtils import readJson
from Utils.DataModifier.DataUnifier import DataUnifier


class CoskyAlgorithme:
    """
    Implementation of the Cosky algorithm for diversity-aware ranking.

    Cosky evaluates skyline points based on their 'rarity' and 'variation'
    across different dimensions.
    """

    def __init__(self, r, pref, is_debug=False):
        """
        Initializes the Cosky algorithm.

        Args:
            r (dict): The dataset (mapping ID to coordinates).
            pref (list): List of preferences (e.g., Preference.MIN).
            is_debug (bool): Enable internal logging for debugging.
        """
        time = TimeCalc(100, "CoskyAlgorithme")
        self.is_debug=is_debug
        self.pref = pref
        self.r = r
        self.unifyData()
        self.bbs = BbsCosky(self.r, 1, 2)
        self.s = {k: list(v) for k, v in self.bbs.skyline.items()}
        # Initializing internal data structures for the ranking steps
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
        time.stop()
        self.time = time.execution_time

    def unifyData(self):
        dataUnifier = DataUnifier(self.r, self.pref, mode="auto")
        self.r = dataUnifier.unifyAuto()
        return self.r

    def run(self):
        """
        Executes the main steps of the Cosky algorithm.

        1. Totals coordinates across dimensions.
        2. Normalizes values (ni).
        3. Computes Gini impurity per dimension (diversity measure).
        4. Calculates final representative weights (p).
        5. Assigns final ranking scores using cosine similarity to an 'ideal' vector.

        Returns:
            dict: Skyline points with an appended score column.
        """
        if len(self.s) == 1:
            for i in self.s:
                self.s[i].append(1.0)
            return self.s
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
                if self.totGini == 0:
                    for i in self.s:
                        self.s[i].append(1.0)
                    return self.s
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
        self.sort("Desc")
        # print("CoskyAlgorithme Result : ", self.s)
        return self.s

    def sort(self,rev):
        """
        Sort the data based on the last column of the dictionary which is the score.
        """
        reverse = True if rev == "Desc" else False
        self.s = dict(sorted(self.s.items(), key=lambda item: item[1][-1], reverse=reverse))

if __name__ == '__main__':
    r = {
        1: (5, 20, 0.014285714),
        2: (4, 60, 0.02),
        3: (5, 30, 0.016666667),
        4: (1, 80, 0.016666667),
        5: (5, 90, 0.025),
        6: (9, 30, 0.02),
        7: (7, 80, 0.025),
        8: (9, 90, 0.033333333)
    }
    
    startTime = time.time()
    cosky = CoskyAlgorithme(r, [Preference.MIN, Preference.MIN, Preference.MIN])
    print("-----------------Avant-----------------")
    print(cosky.s)
    print(f"temps: {time.time() - startTime}")
    print("-----------------Apres-----------------")
    cosky.sort("Desc")
    print(cosky.s)