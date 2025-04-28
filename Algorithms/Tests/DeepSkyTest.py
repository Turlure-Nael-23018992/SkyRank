import sqlite3
import unittest
import os
import sys

from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.SkyIR import SkyIR
from Utils.DatasModifier.DataNormalizerDeepSky import DataNormalizerDeepSky
from Utils.DatasModifier.JsonUtils import readJson
from Algorithms.CoskySql import CoskySQL
from Algorithms.DeepSky import DeepSky
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class DeepSkyTest(unittest.TestCase):
    def setUp(self):
        self.rTuples8 = readJson("../Datas/Rtuples8.json")
        self.k = 4
        self.dataNorm = DataNormalizerDeepSky(self.rTuples8, "../../Assets/DeepSkyTest.db")

    def testDeepSkyCoskySql(self):
        """
        Test the DeepSky algorithm with CoskySql.
        """
        deepSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, CoskySQL)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testDeepSkyCoskyAlgo(self):
        """
        Test the DeepSky algorithm with CoskyAlgo.
        """
        deepSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, CoskyAlgorithme)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testDeepSkyDpIdpDh(self):
        """
        Test the DeepSky algorithm with DpIdpDh.
        """
        deepSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, DpIdpDh)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testDeepSkySkyIR(self):
        """
        Test the DeepSky algorithm with SkyIR.
        """
        deepSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, SkyIR)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testDeepSkyRankSky(self):
        """
        Test the DeepSky algorithm with RankSky.
        """
        deepSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, RankSky)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "The result should contain k elements.")

    def testCompareDict(self):
        """
        Test every algorithm with the same data.
        """

        deepSkyCoskySql = DeepSky("../../Assets/DeepSkyTest.db", self.k, CoskySQL).topK
        deepSkyCoskyAlgo = DeepSky("../../Assets/DeepSkyTest.db",  self.k, CoskyAlgorithme).topK
        deepSkyDpIdpDh = DeepSky("../../Assets/DeepSkyTest.db", self.k, DpIdpDh).topK
        deepSkySkyIR = DeepSky("../../Assets/DeepSkyTest.db", self.k, SkyIR).topK
        deepSkyRankSky = DeepSky("../../Assets/DeepSkyTest.db", self.k, RankSky).topK

        deepSkyCoskySql = self.dataNorm.sortArr([int(k) for k in deepSkyCoskySql.keys()])
        deepSkyCoskyAlgo = self.dataNorm.sortArr([int(k) for k in deepSkyCoskyAlgo.keys()])
        deepSkyDpIdpDh = self.dataNorm.sortArr([int(k) for k in deepSkyDpIdpDh.keys()])
        deepSkySkyIR = self.dataNorm.sortArr([int(k) for k in deepSkySkyIR.keys()])
        deepSkyRankSky = self.dataNorm.sortArr([int(k) for k in deepSkyRankSky.keys()])

        self.assertEqual(deepSkyCoskySql, deepSkyCoskyAlgo, "The results should be the same.")
        self.assertEqual(deepSkyCoskyAlgo, deepSkyDpIdpDh, "The results should be the same.")
        self.assertEqual(deepSkyDpIdpDh, deepSkySkyIR, "The results should be the same.")
        self.assertEqual(deepSkySkyIR, deepSkyRankSky, "The results should be the same.")
        self.assertEqual(deepSkyRankSky, deepSkyCoskySql, "The results should be the same.")

