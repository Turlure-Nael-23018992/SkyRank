import unittest
import os
import sys

# Ensure project root is reachable for dependencies
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Utils.DataModifier.JsonUtils import readJson
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.SkyIR import SkyIR

class DpIdpDhTest(unittest.TestCase):
    """
    Test suite for the DpIdpDh algorithm.
    Focuses on dominance power calculation and consistency with other algorithms.
    """

    def setUp(self):
        """
        Loads the large benchmark dataset RBig.json and defines expected output.
        Normalizes keys to strings for consistency across tests.
        """
        base_dir = os.path.dirname(__file__)
        rbig_path = os.path.abspath(os.path.join(base_dir, "..", "..", "Algorithms", "Datas", "RBig.json"))
        self.r_big = readJson(rbig_path)

        # Pre-verified skyline IDs for the RBig.json dataset
        self.exceptedOutput = ["32", "67", "89", "103", "150", "382", "399", "496", "541", "551", "593", "604"]

    def test_Algo_DPIDP(self):
        """
        Functional test on a real dataset (RBig.json).
        Verifies that the set of correctly identified skyline points matches the benchmark.
        """
        values = DpIdpDh(self.r_big).score
        skyline = sorted([str(k) for k in values.keys()])
        self.assertEqual(sorted(self.exceptedOutput), skyline)

    def test_Algo_DPIDP_OddDataset_Regression(self):
        """
        Regression test: Handles datasets with an odd number of tuples.
        Prevents previous bugs where odd-sized data caused internal processing corruptions.
        """
        odd_r = {
            "1": (1, 10),
            "2": (10, 1),
            "3": (5, 5)
        }
        try:
            dp = DpIdpDh(odd_r)
            self.assertTrue(len(dp.score) > 0, "Algorithm should produce results for odd-sized datasets.")
        except Exception as e:
            self.fail(f"DpIdpDh failed on odd dataset regression: {e}")

    def test_Consistency_With_SkyIR(self):
        """
        Consistency test: Compares DpIdpDh with SkyIR's first dominance layer.
        Both algorithms should identify the same base skyline for the same dataset.
        """
        r = {
            "1": (1, 10, 5),
            "2": (2, 5, 10),
            "3": (10, 1, 2),
            "4": (5, 5, 5),
            "5": (10, 10, 10)
        }
        # DpIdpDh result (all non-dominated points)
        dp_result = set(str(k) for k in DpIdpDh(r).score.keys())
        
        # SkyIR result (from internal calculSkylineEtNbDominants pass)
        skyir = SkyIR(r)
        s_ir_l1, _, _ = skyir.calculSkylineEtNbDominants()
        skyir_l1_keys = set(str(k) for k in s_ir_l1.keys())
        
        self.assertEqual(dp_result, skyir_l1_keys, "Skyline points should be identical between DpIdpDh and SkyIR L1.")

if __name__ == "__main__":
    unittest.main()