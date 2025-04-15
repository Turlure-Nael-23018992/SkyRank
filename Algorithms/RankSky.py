import numpy as np
from fractions import Fraction
import math
from Utils.Preference import Preference
from Utils.TimerUtils import TimeCalc
from Algorithms.BbsCosky import BbsCosky
from Database.DatabaseToDict import DatabaseToDict
import json



class RankSky:

    def __init__(self, rTuple, pref):  # [[5,1],[2,3],[3,2]]
        self.rTupleInit = rTuple
        self.prefInit = pref
        self.r = self.rTupleInit.copy()
        self.tupleToTab(self.r)
        self.rUnifyTab = self.r.copy()
        self.pref = self.prefInit.copy()
        self.unifyPreferencesMin(self.rUnifyTab, self.pref)
        self.rTupleNv = self.rUnifyTab.copy()
        self.tabToTuple(self.rTupleNv)
        self.sky = None
        self.rm = None # Relation matrix
        self.rt = None # Transposed matrix
        self.a = None # Square matrix
        self.s = None # Stochastic matrix
        self.n = None # Number of rows
        self.g = None # Google PageRank matrix
        self.vk = None # Score's vector
        self.alpha = 0.85 # Damping factor
        self.score = {}
        self.run()

    def unifyPreferences(r, pref, prefNext):
        for i in range(len(pref)):
            if prefNext[i] != pref[i]:
                pref[i] = prefNext[i]
                for val in r.values():
                    val[i] = 1 / val[i]


    def unifyPreferencesMax(self, r, pref):
        for i in range(len(pref)):
            if pref[i] == Preference.MIN:
                pref[i] = Preference.MAX
                for val in r.values():
                    val[i] = 1 / val[i]


    def unifyPreferencesMin(self, r, pref):
        for i in range(len(pref)):
            if pref[i] == Preference.MAX:
                pref[i] = Preference.MIN
                for val in r.values():
                    val[i] = 1 / val[i]

    def tupleToTab(self, rTuple):
        """
        Convert the tuples in the relation matrix to a list
        """
        for key, val in rTuple.items():
            rTuple[key] = list(val)

    def tabToTuple(self, rTab):
        """
        Convert the relation matrix to a tuple
        """
        for key, val in rTab.items():
            rTab[key] = tuple(val)

    def initMatrix(self):
        """
        Initialize the data
        """
        tab = []
        for val in self.sky.values():
            tab.append(val)
        self.rm = tab

    def skylineComputation(self):
        bbs = BbsCosky(self.r, 1, 2)  # Create BBS object
        self.sky = {k: list(v) for k, v in bbs.skyline.items()}


    def squareMatrix(self):
        """
        Create the square matrix from the relation matrix
        """
        self.rt = np.transpose(self.rm)
        self.a = np.dot(self.rm, self.rt)

    def stochasticMatrix(self):
        self.s = np.array(self.a, dtype=float)
        self.n = len(self.s)
        for i in range(self.n):
            tot = 0
            for j in range(self.n):
                tot += self.s[i][j]
            for j in range(self.n):
                self.s[i][j] = self.s[i][j] / tot

    def googlePageRank(self):
        dim = (self.n, self.n)
        e = np.ones(dim)
        self.g = self.alpha * self.s + (1 - self.alpha) / self.n * e

    def Ipl(self, p=3):
        eps = math.pow(10, -p)
        self.vk = [1 / self.n] * self.n
        zk = [0] * self.n
        zknorm = 0
        while True:
            vknorm = zknorm
            zk = np.dot(self.vk, self.g)
            zknorm = np.linalg.norm(zk)
            self.vk = zk / zknorm
            if abs(zknorm - vknorm) < eps:
                break

    def IplDom(self, p=3):
        vdom = -p / math.log10(self.alpha)
        self.vk = [1 / self.n] * self.n
        k = 0
        while True:
            k += 1
            self.vk = np.dot(self.vk, self.g)
            if k > vdom:
                print("IplDom", k)
                break

    def sort(self,rev="Desc"):
        reverse = False if rev == "Asc" else True
        i = 0
        for key in self.sky.keys():
            self.score[key] = self.rTupleInit[key] + tuple([float(self.vk[i])])
            i += 1
        self.score = dict(sorted(self.score.items(), key=lambda item: item[1][-1], reverse=reverse))


    def printOutcomes(self):
        """print("Skyline matrix : \n", self.sky)
        print("Transposed matrix : \n", self.rt)
        print("Square matrix : \n", self.a)
        print("Stochastic matrix : \n", self.s)
        print("Google PageRank matrix : \n", self.g)"""
        print("Score's vector : \n", self.score)

    def run(self):
        self.skylineComputation()
        self.unifyPreferencesMax(self.sky, self.pref)
        self.initMatrix()
        self.squareMatrix()
        self.stochasticMatrix()
        self.googlePageRank()
        self.Ipl()
        self.sort()

if __name__ == "__main__":
    """r = {
        1: [5, 20, 70],
        2: [4, 60, 50],
        4: [1, 80, 60], # mettre en tuples
    }"""

    r = {
        1: (5, 20, 70),
        2: (4, 60, 50),
        3: (5, 30, 60),
        4: (1, 80, 60),
        5: (5, 90, 40),
        6: (9, 30, 50),
        7: (7, 80, 40),
        8: (9, 90, 30)
    }
    pref = [Preference.MIN,Preference.MIN,Preference.MIN]

    db = DatabaseToDict("../Assets/Databases/cosky_db_C3_R10000.db")
    db.toDict()
    r = db.data

    print("1./ Utiliser rankSky avec ipl")
    print("2./ Utiliser rankSky avec iplDom")
    i = input("Choisir 1 ou 2 : ")
    rankSky = RankSky(r, pref)
    if i == "1":
        time1 = TimeCalc(100, "RankSky")
        rankSky.skylineComputation()
        time1.stop()
        rankSky.unifyPreferencesMax(rankSky.sky, rankSky.pref)
        rankSky.initMatrix()
        time2 = TimeCalc(100, "RankSky")
        rankSky.squareMatrix()
        rankSky.stochasticMatrix()
        rankSky.googlePageRank()
        rankSky.Ipl()
        rankSky.sort()
        time2.stop()
        #rankSky.printOutcomes()
        print("Execution time : ", time1.execution_time + time2.execution_time)

    elif i== "2":
        time1 = TimeCalc(100, "RankSky")
        rankSky.skylineComputation()
        time1.stop()
        rankSky.unifyPreferencesMax(rankSky.sky, rankSky.pref)
        rankSky.initMatrix()
        time2 = TimeCalc(100, "RankSky")
        rankSky.squareMatrix()
        rankSky.stochasticMatrix()
        rankSky.googlePageRank()
        rankSky.IplDom()
        rankSky.sort()
        time2.stop()
        rankSky.printOutcomes()
        print("Execution time : ", time1.execution_time + time2.execution_time)




    #[0.15840845 0.3688939  0.47269766]
    #[0.15630708 0.36914946 0.47454346]

    #[0.25400163 0.59434898 0.76304159]
