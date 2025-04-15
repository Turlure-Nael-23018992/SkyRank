import unittest
import json

from Algorithms.DpIdpDh import DpIdpDh

class DpIdpDhTest(unittest.TestCase):
    """Test suite for DpIdpDh algorithm"""

    def setUp(self):
        """Set up the test case"""
        with open('../Datas/RBig.json', 'r') as f:
            self.r_big = json.load(f)

        # Excepted values for Dp_IDP algorithm
        self.exceptedOutput = {31: 100.12794123202812,
                                66: 4.814669361678212,
                                88: 177.54031859048024,
                                102: 64.33287037248346,
                                149: 56.588694473078284,
                                381: 19.348062785161932,
                                398: 19.69864863692009,
                                495: 24.734938700428767,
                                540: 0.23856062735983122,
                                550: 2.035309896463078,
                                592: 3.960770184126881,
                                603: 3.5719974892938056}
        # Run DP_IDP algorithm
        self.dpIdpDhValues = DpIdpDh(self.r_big).score


    def test_Algo_DPIDP(self):
        """Test the DP_IDP algorithm with a sample dataset"""
        self.assertEqual(self.exceptedOutput, self.dpIdpDhValues)