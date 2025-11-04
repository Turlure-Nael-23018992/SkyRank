import os
import unittest
from Utils.Preference import Preference
from Utils.DataModifier.JsonUtils import readJson
from Algorithms.CoskyAlgorithme import CoskyAlgorithme


class CoskyAlgoTest(unittest.TestCase):
    """Test suite for the Cosky algorithm (keys only)."""

    def setUp(self):
        """Set up the test case environment."""
        base_dir = os.path.dirname(__file__)
        rbig_path = os.path.abspath(os.path.join(base_dir, "..", "Datas", "RBig.json"))

        # Load JSON data
        r_big_loaded = readJson(rbig_path)
        self.r_big_reloaded = {int(k): tuple(v) for k, v in r_big_loaded.items()}

        # Expected output keys (IDs only)
        self.expected_keys = [
            32, 67, 89, 103, 150,
            382, 399, 496, 541, 551,
            593, 604
        ]

        # Run Cosky algorithm
        self.cosky_algo = CoskyAlgorithme(
            self.r_big_reloaded,
            [Preference.MIN, Preference.MIN, Preference.MIN]
        ).s

        # Extract actual keys from the result
        self.actual_keys = list(self.cosky_algo.keys())

        print("✅ CoskyAlgorithme skyline:", self.actual_keys)

    def test_cosky_skyline(self):
        """Check if CoskyAlgorithme returns the expected set of skyline points."""
        self.assertEqual(
            sorted(self.expected_keys),
            sorted(self.actual_keys),
            "Returned skyline points do not match the expected output."
        )


if __name__ == "__main__":
    unittest.main()
