import os
import sys
import unittest

# Configure path for internal package imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Utils.Preference import Preference
from Utils.DataModifier.JsonUtils import readJson
from Algorithms.CoskyAlgorithme import CoskyAlgorithme

class CoskyAlgoTest(unittest.TestCase):
    """
    Test suite for the Cosky algorithm core.
    Verifies rarity-based scoring and handling of specific dataset patterns.
    """

    def setUp(self):
        """
        Initializes benchmark environment using RBig.json.
        Runs the algorithm once to populate actual results for standard verification.
        """
        base_dir = os.path.dirname(__file__)
        rbig_path = os.path.abspath(os.path.join(base_dir, "..", "..", "Algorithms", "Datas", "RBig.json"))

        # Load and normalize dataset
        r_big_loaded = readJson(rbig_path)
        self.r_big_reloaded = {int(k): tuple(v) for k, v in r_big_loaded.items()}

        # Reference skyline IDs for RBig.json
        self.expected_keys = [32, 67, 89, 103, 150, 382, 399, 496, 541, 551, 593, 604]

        # Execute Cosky with default MIN preferences
        cosky_inst = CoskyAlgorithme(
            self.r_big_reloaded,
            [Preference.MIN, Preference.MIN, Preference.MIN]
        )
        self.cosky_algo = cosky_inst.s
        self.actual_keys = list(self.cosky_algo.keys())

    def test_cosky_skyline(self):
        """
        Benchmark test on RBig.json.
        Ensures the returned set of keys matches the expected list of non-dominated points.
        """
        self.assertEqual(
            sorted(self.expected_keys),
            sorted(self.actual_keys),
            "The computed skyline points do not match the expected benchmark keys."
        )

    def test_single_point(self):
        """
        Edge case: verify behavior on a dataset containing only one point.
        Expects the point to be its own skyline with a default ranking score.
        """
        r = {1: (1, 2, 3)}
        cosky = CoskyAlgorithme(r, [Preference.MIN] * 3)
        self.assertEqual(list(cosky.s.keys()), [1], "A single-point dataset should return that point.")
        self.assertEqual(cosky.s[1][-1], 1.0, "Score for a single non-dominated point should be 1.0.")

    def test_identical_points(self):
        """
        Edge case: verify behavior when multiple identical non-dominated points exist.
        Ensures the algorithm doesn't crash or lose both points.
        """
        r = {
            1: (5, 5, 5),
            2: (5, 5, 5)
        }
        cosky = CoskyAlgorithme(r, [Preference.MIN] * 3)
        # BBS implementation typically preserves both if they don't strictly dominate each other
        self.assertTrue(len(cosky.s) >= 1, "At least one instance of identical points should be preserved.")

if __name__ == "__main__":
    unittest.main()
