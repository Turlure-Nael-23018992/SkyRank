import unittest
import os
from Utils.DataModifier.JsonUtils import readJson

from Algorithms.DpIdpDh import DpIdpDh

class DpIdpDhTest(unittest.TestCase):
    """Test suite for DpIdpDh algorithm"""

    def setUp(self):
        """Set up the test case"""
        base_dir = os.path.dirname(__file__)
        rbig_path = os.path.abspath(os.path.join(base_dir, "..", "Datas", "RBig.json"))
        self.r_big = readJson(rbig_path)

        # Excepted values for Dp_IDP algorithm
        self.exceptedOutput = [32,
                                67,
                                89,
                                103,
                                150,
                                382,
                                399,
                                496,
                                541,
                                551,
                                593,
                                604]
        # Run DP_IDP algorithm
        self.dpIdpDhValues = DpIdpDh(self.r_big).score
        self.dpIdpDhSkyline = list(self.dpIdpDhValues.keys())

    def test_Algo_DPIDP(self):
        """Test the DP_IDP algorithm with a sample dataset"""
        self.assertEqual(self.exceptedOutput, self.dpIdpDhSkyline)