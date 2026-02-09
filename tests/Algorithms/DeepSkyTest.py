import sqlite3
import unittest
import os
import sys

from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Utils.DataModifier.DataNormalizerDeepSky import DataNormalizerDeepSky
from Utils.DataModifier.JsonUtils import readJson
from Algorithms.CoskySql import CoskySQL
from Algorithms.DeepSky import DeepSky
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class DeepSkyTest(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        rTuple = os.path.abspath(os.path.join(base_dir, "..", "..", "Algorithms", "Datas", "rTuples8.json"))
        self.rTuples8 = readJson(rTuple)
        self.k = 7
        rbig_path = os.path.abspath(os.path.join(base_dir, "..", "..", "Algorithms", "Datas", "DeepSkyTest.db"))
        self.path = rbig_path
        self.dataNorm = DataNormalizerDeepSky(self.rTuples8, self.path)

    def testDeepSkyCoskySql(self):
        """
        Test the DeepSky algorithm with CoskySql.
        """
        deepSky = DeepSky(self.path, self.k, CoskySQL)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testDeepSkyCoskyAlgo(self):
        """
        Test the DeepSky algorithm with CoskyAlgo.
        """
        deepSky = DeepSky(self.path, self.k, CoskyAlgorithme)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    '''def testDeepSkyDpIdpDh(self):
        DpIdp with deepSky currently in dev !
        """
        Test the DeepSky algorithm with DpIdpDh.
        """
        deepSky = DeepSky("../../Algorithms/Datas/DeepSkyTest.db", self.k, DpIdpDh)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")'''

    def testDeepSkyRankSky(self):
        """
        Test the DeepSky algorithm with RankSky.
        """
        deepSky = DeepSky(self.path, self.k, RankSky)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testCompareDict(self):
        """
        Test every algorithm with the same data.
        """
        deepSkyCoskySql = DeepSky(self.path, self.k, CoskySQL).topK
        deepSkyCoskyAlgo = DeepSky(self.path,  self.k, CoskyAlgorithme).topK
        deepSkyRankSky = DeepSky(self.path, self.k, RankSky).topK

        deepSkyCoskySql = sorted(deepSkyCoskySql.keys())
        deepSkyCoskyAlgo = sorted(deepSkyCoskyAlgo.keys())
        deepSkyRankSky = sorted(deepSkyRankSky.keys())

        self.assertEqual(deepSkyCoskySql, deepSkyCoskyAlgo, "The results should be the same.")
        self.assertEqual(deepSkyCoskyAlgo, deepSkyRankSky, "The results should be the same.")
        self.assertEqual(deepSkyRankSky, deepSkyCoskySql, "The results should be the same.")

if __name__ == "__main__":
    unittest.main()
