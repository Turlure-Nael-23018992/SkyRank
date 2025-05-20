import numpy as np
import math
from Utils.Preference import Preference
from Utils.TimerUtils import TimeCalc
from Algorithms.BbsCosky import BbsCosky
from Utils.DataModifier.DatabaseToDict import DatabaseToDict
from Utils.DataModifier.DataUnifier import DataUnifier
from Utils.DisplayHelpers import print_red


class RankSky:

    def __init__(self, rTuple, pref):
        """
        Constructor for the RankSky class.

        Initializes the RankSky ranking process using skyline computation and PageRank.
        It prepares the input data, unifies preferences, computes the skyline, and triggers
        matrix construction and scoring.

        :param rTuple: dict - the input relation as a dictionary of tuples (for exemple : {1: (val1, val2, ...), ...})
        :param pref: list[Preference] - a list of Preference enums (MIN or MAX) corresponding to each dimension
        """
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
        self.time = 0
        self.run()

    def unifyPreferencesMax(self, r, pref):
        """
        Converts all preferences in the relation to MAX by inverting MIN dimensions.

        :param r: dict - the relation data to modify (values are updated in place)
        :param pref: list[Preference] - list of current preferences, which will be updated to MAX
        """
        dataUnifier = DataUnifier(r, pref, mode="Max")
        self.r = dataUnifier.unifyPreferencesMax()

    def unifyPreferencesMin(self, r, pref):
        """
        Converts all preferences in the relation to MIN by inverting MAX dimensions.

        :param r: dict - the relation data to modify (values are updated in place)
        :param pref: list[Preference] - list of current preferences, which will be updated to MIN
        """
        dataUnifier = DataUnifier(r, pref, mode="Min")
        #print(f"Pre Unify data: {r}")
        self.r = dataUnifier.unifyPreferencesMin()
        #print(f"Post Unify data: {self.r}")

    def tupleToTab(self, rTuple):
        """
        Converts all tuple values in the relation dictionary to lists.

        This is used to allow in-place modification of the data (since lists are mutable,
        unlike tuples).

        :param rTuple: dict - the relation dictionary with tuple values to be converted
        """
        for key, val in rTuple.items():
            rTuple[key] = list(val)

    def tabToTuple(self, rTab):
        """
        Converts all list values in the relation dictionary back to tuples.

        This is typically used after data processing to restore the original tuple format.

        :param rTab: dict - the relation dictionary with list values to be converted
        """
        for key, val in rTab.items():
            rTab[key] = tuple(val)

    def initMatrix(self):
        """
        Initializes the relation matrix (self.rm) from the current skyline.

        It extracts the list of values for each skyline point and builds a matrix
        representation for further processing (exemple : matrix multiplication).
        """
        tab = []
        for val in self.sky.values():
            tab.append(val)
        self.rm = tab

    def skylineComputation(self):
        """
        Computes the skyline of the current dataset using the BBS (Branch and Bound Skyline) algorithm.

        The result is stored in self.sky as a dictionary of non-dominated tuples.
        This is a key step before performing any ranking or PageRank-based processing.
        """
        bbs = BbsCosky(self.r, 1, 2)  # Create BBS object
        self.sky = {k: list(v) for k, v in bbs.skyline.items()}
        return len(self.sky) == 1
    def squareMatrix(self):
        """
        Constructs the square matrix used for ranking.

        It transposes the relation matrix (self.rm), then multiplies the original
        matrix with its transpose to form a square similarity matrix (self.a),
        which will later be used to compute the stochastic matrix.
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
        """
        Constructs the Google PageRank matrix (self.g) from the stochastic matrix (self.s).
        """
        dim = (self.n, self.n)
        e = np.ones(dim)
        self.g = self.alpha * self.s + (1 - self.alpha) / self.n * e

    def Ipl(self, p=3):
        """
        Computes the PageRank vector using the Ipl method.
        :param p: int - precision for convergence (default is 3)
        """
        eps = math.pow(10, -p)
        self.vk = [1 / self.n] * self.n
        zk = [0] * self.n
        zknorm = 0
        while True:
            vknorm = zknorm
            zk = np.dot(self.vk, self.g)
            zknorm = np.linalg.norm(zk, ord=1)
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
        """
        Sorts the score vector based on the last column of the matrix which is the score.
        :param rev: str - "Asc" for ascending order, "Desc" for descending order, default is "Desc"
        """
        reverse = False if rev == "Asc" else True
        i = 0
        for key in self.sky.keys():
            self.score[key] = self.rTupleInit[key] + tuple([float(self.vk[i])])
            i += 1
        self.score = dict(sorted(self.score.items(), key=lambda item: item[1][-1], reverse=reverse))

    def printOutcomes(self):
        """
        Prints the outcomes of the ranking process, including the skyline matrix,
        """
        print("=" * 40)
        print("📌 Initial Relation:")
        print(self.rTupleInit)
        print("=" * 40)
        print("📌 Preference List:")
        print(self.prefInit)
        print("=" * 40)
        print("📌 Maximized Skyline:")
        print(self.rm)
        print("📌 Skyline Matrix:")
        print(self.sky)
        print("=" * 40)
        print("📌 Transposed Matrix:")
        print(self.rt)
        print("=" * 40)
        print("📌 Square Matrix:")
        print(self.a)
        print("=" * 40)
        print("📌 Stochastic Matrix:")
        print(self.s)
        print("=" * 40)
        print("📌 Google PageRank Matrix:")
        print(self.g)
        print("=" * 40)
        print("📌 Score Vector:")
        print(self.score)
        print("=" * 40)

    def run(self):
        """
        Executes the entire ranking process, including skyline computation, including a timer for performance measurement.
        """
        time1 = TimeCalc(100, "RankSky")
        if self.skylineComputation():
            time1.stop()
            self.time = time1.execution_time
            first_key = next(iter(self.sky))
            self.sky[first_key].append(1)
            self.score = {first_key : self.sky[first_key]}
            print("self.score", self.score)
            print_red("1")
        else :
            self.skylineComputation()
            print_red("2")
            time1.stop()
            self.unifyPreferencesMax(self.sky, self.pref)
            self.initMatrix()
            time2 = TimeCalc(100, "RankSky")
            self.squareMatrix()
            self.stochasticMatrix()
            self.googlePageRank()
            self.Ipl()
            self.sort()
            time2.stop()
            self.time = time1.execution_time + time2.execution_time
        print(self.sky)

if __name__ == "__main__":
    """r = {
        1: [5, 20, 70],
        2: [4, 60, 50],
        4: [1, 80, 60], # mettre en tuples
    }"""

    r = {
        1: (5, 20, 1/70),
        2: (4, 60, 1/50),
        3: (5, 30, 1/60),
        4: (1, 80, 1/60),
        5: (5, 90, 1/40),
        6: (9, 30, 1/50),
        7: (7, 80, 1/40),
        8: (9, 90, 1/30)
    }

    """r = {
        1: (5, 20, 1/70),
    }"""
    pref = [Preference.MIN,Preference.MIN,Preference.MIN]

    """db = DatabaseToDict("../Assets/DeepSkyTest.db")
    db.toDict()
    r = db.data"""

    rankSky = RankSky(r, pref)

    print("1./ Utiliser rankSky avec ipl")
    print("2./ Utiliser rankSky avec iplDom")
    i = input("Choisir 1 ou 2 : ")
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
        rankSky.printOutcomes()
        print("Execution time : ", time1.execution_time + time2.execution_time)
        print(rankSky.sky)

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
