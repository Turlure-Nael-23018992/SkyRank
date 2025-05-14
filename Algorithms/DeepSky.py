"""
=======
DeepSky
=======
Entrée :
	La relation r.
	Un entier k.
Sortie :
    Ldx top-k tuples/points avec les meilleurs scores topk.

topk <- nouveau tableau
tot <- 0 // Nombre total de résultats calculés
rl = r // Niveau courant
Tant que tot >= k and !rl
    s <- CoSky(rl)
	n <- taille(s) - 1
	tot <- tot + taille(s)
	Si tot < k
        topk <- topk U s
		rl <- rl \ s
	Sinon
	    Si tot >= k
		    Pour i de 0 à k
		        topk[i] <- s[i]
			retourner topk

retourner topk
"""



import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from Utils.DataModifier.DatabaseToDict import DatabaseToDict
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR
from Utils.TimerUtils import TimeCalc
from Utils.DataModifier.DataNormalizerDeepSky import DataNormalizerDeepSky
from Utils.Preference import Preference



# MODES contains all the algorithms to be compared
MODES = {
    "CoskyAlgo": CoskyAlgorithme,
    "CoskySql": CoskySQL,
    "DpIdpDh": DpIdpDh,
    "RankSky": RankSky,
    "SkyIR": SkyIR,
}

"""
r = [
    (1, 5, 20, 1 / 70),
    (2, 4, 60, 1 / 50),
    (3, 5, 30, 1 / 60),
    (4, 1, 80, 1 / 60),
    (5, 5, 90, 1 / 40),
    (6, 9, 30, 1 / 50),
    (7, 7, 80, 1 / 40),
    (8, 9, 90, 1 / 30)
]
"""


r_next = {
    1:(5, 20, 1 / 70),
    2:(4, 60, 1 / 50),
    4:(1, 80, 1 / 60)
}

r = {
    1:(5, 20, 1 / 70),
    2:(4, 60, 1 / 50),
    3:(5, 30, 1 / 60),
    4:(1, 80, 1 / 60),
    5:(5, 90, 1 / 40),
    6:(9, 30, 1 / 50),
    7:(7, 80, 1 / 40),
    8:(9, 90, 1 / 30)
}



"""
def DeepSky(r,k):
    topK={}
    tot=0
    rl=r

    while tot<k and rl!={}:
        print(100*"*")
        print("rl:\n",'\n'.join([str(x) for x in rl.items()]))
        print()
        #s=Cosky(rl).relations
        s = r_next
        tot+=len(s)

        if tot<=k:
            print(100*"-")
            topK.update(s)
            print("topK:\n",'\n'.join([str(x) for x in topK.items()]))
            print()
            print("s:\n",'\n'.join([str(x) for x in s.items()]))
            print()
            #print(f"rl:{rl}")

            rl = {k:v for k,v in rl.items() if k not in s.keys()}
        else:
            print(100 * "|")
            topK.update({x:s[x] for x in list(s.keys())[:k]})
            print("topK:\n", '\n'.join([str(x) for x in topK.items()]))
            print()


            return topK
    return topK

res = DeepSky(r,k)
print(res)
"""
def addBest(k, topK, s):
    """
    Add the best elements to the topK based on the score (last value of the tuple).
    :param k: the number of top elements to add
    :param topK: the topK
    :param s: the elements to add
    """
    n = k - len(topK)  # Number of elements to add
    # Sort elements in `s` by the last value of the tuple (score) in descending order
    print("s", s)
    print("s type", type(s))
    sorted_s = sorted(s.items(), key=lambda x: x[1][-1] if x[1][-1] is not None else float('-inf'), reverse=True)

    # Add the top `n` elements to `topK`
    for key, value in sorted_s[:n]:
        topK[key] = value

    return topK

class DeepSky:
    """
    Class to implement the DeepSky algorithm with SQL.
    """
    def __init__(self, fp, k, algo, pref=None):
        """
        Initialize the DeepSky algorithm with the given database file path and relation.
        :param fp: the path to the SQLite database file
        :param k: the number of top tuples to find
        :param algo: the algorithm to use (CoskySQL, CoskyAlgorithme, DpIdpDh, RankSky, SkyIR)
        """
        if pref is None:
            pref = [Preference.MIN, Preference.MIN, Preference.MIN]
        self.dbToDict = DatabaseToDict(fp)
        self.fp = fp
        self.r = self.dbToDict.toDict()
        self.k = k
        self.algo = algo.__name__
        self.topK = {}
        self.dataNorm = DataNormalizerDeepSky(self.r, self.fp)
        self.lineToInsertBack = []
        self.preference = pref
        self.run()

    def DeepSkyCoskySql(self):
        linesToSave = []
        tot = 0
        rl = self.r
        while tot < self.k and rl != {}:
            cosky = CoskySQL(self.fp, self.preference)
            linesToSave.append(cosky.rows_res)
            s = cosky.dict
            tot += len(s)
            if tot <= self.k:
                self.topK.update(s)
                linesToSave = self.delLines(linesToSave)
            else:
                addBest(self.k, self.topK, s)
                return self.topK
        return self.topK


    def DeepSky(self):
        """
        DeepSky algorithm to find the top-k tuples with the best scores.
        :return: the top-k tuples
        """
        tot=0
        rl=self.r
        while tot<self.k and rl!={}:
            if self.algo == "CoskyAlgorithme":
                s = CoskyAlgorithme(rl, self.preference).s
                """elif self.algo == "DpIdpDh":
                s = DpIdpDh(rl).score"""
            elif self.algo == "RankSky":
                s = RankSky(rl, self.preference).score
                print("s 1", s)
            """elif self.algo == "SkyIR":
                s = SkyIR(rl).r"""
            tot+=len(s)
            if tot<=self.k:
                self.topK.update(s)
                print("self.topK", self.topK)
                rl = {k:v for k,v in rl.items() if k not in s.keys()}
            else:
                self.topK = addBest(self.k, self.topK, s)
                return self.topK
        return self.topK


    def delLines(self, linesToSave):
        """
        Delete the lines from the database.
        :param linesToSave: the lines to delete
        """
        linesToSave = linesToSave[0]
        for i in range(len(linesToSave)):
            self.dataNorm.deleteLineDb(linesToSave[i][0])
            self.lineToInsertBack.append(linesToSave[i])
        return []

    def run(self):
        """
        Run the DeepSky algorithm.
        :return: the top-k tuples
        """
        print(self.algo)
        if self.algo == "CoskySQL":
            self.DeepSkyCoskySql()
            self.dataNorm.addLinesDb(self.lineToInsertBack)
        else:
            self.DeepSky()
        return self.topK

if __name__ == "__main__":
    linesToInsertBack = []
    k = 7
    algos = [CoskySQL, CoskyAlgorithme, DpIdpDh, RankSky, SkyIR]
    fp = "../Assets/Databases/cosky_db_C3_R10000.db"
    fp = "../Assets/DeepSkyTest.db"
    deepSky = DeepSky(fp, k, CoskyAlgorithme)
    print("deepSky.topK", deepSky.topK)

