import unittest
import os
import sys

# Ensure the project root is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Algorithms.BbsCosky import BbsCosky
from Utils.Preference import Preference

class TestBBSCosky(unittest.TestCase):
    """
    Test suite for the BBS_COSKY (Branch and Bound Skyline) algorithm.
    Focuses on skyline computation accuracy and multi-layer behavior.
    """

    def setUp(self):
        """
        Initializes a hierarchical dataset:
        - Points '1' and '2' are non-dominated (Layer 1).
        - Point '3' is dominated by '1'.
        - Point '4' is dominated by '2'.
        - Point '5' is dominated by all others (Layer 3+).
        """
        self.r = {
            "1": (1, 10, 5),
            "2": (10, 1, 5),
            "3": (5, 12, 6),
            "4": (12, 5, 6),
            "5": (15, 15, 15)
        }

    def test_basic_skyline(self):
        """
        Verify basic skyline computation (Layer 1).
        Expects only points that are not dominated by anyone else.
        """
        bbs = BbsCosky(self.r, 1, 1)
        sky = bbs.skyline
        # Points '1' and '2' are the global Pareto front
        self.assertIn("1", sky)
        self.assertIn("2", sky)
        self.assertEqual(len(sky), 2, "Layer 1 skyline should contain exactly 2 points in this dataset.")

    def test_multiple_layers(self):
        """
        Verify that requesting more layers expands the result set.
        In this implementation, Layer K returns (Layer 1 union ... union Layer K).
        """
        bbs_l1 = BbsCosky(self.r, 1, 1)
        sky_l1 = set(bbs_l1.skyline.keys())
        
        bbs_l2 = BbsCosky(self.r, 1, 2)
        sky_all_l2 = set(bbs_l2.skyline.keys())
        
        # Layer 1 should be a strict subset of the multi-layer result if more points exist
        self.assertTrue(sky_l1.issubset(sky_all_l2), "Layer 1 result must be included in Layer 2 result.")
        self.assertTrue(len(sky_all_l2) >= len(sky_l1), "Layer 2 should return at least as many points as Layer 1.")
        self.assertTrue(set(sky_all_l2).issubset(set(self.r.keys())), "Result must only contain existing IDs.")

    def test_empty_dataset(self):
        """
        Edge case: verify robustness when the input dictionary is empty.
        """
        bbs = BbsCosky({}, 1, 1)
        self.assertEqual(bbs.skyline, {}, "Empty input should yield an empty result.")

if __name__ == "__main__":
    unittest.main()
