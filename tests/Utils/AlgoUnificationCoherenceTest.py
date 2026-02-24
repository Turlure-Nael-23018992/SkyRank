import sys
import os
import unittest

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Utils.DataModifier.DataUnifier import DataUnifier
from Utils.Preference import Preference

class TestAlgoUnificationCoherence(unittest.TestCase):
    """
    Tests the coherence between algorithms and their required unification modes.
    """

    def get_expected_mode(self, algo_name):
        """
        Mirror of the logic implemented in AppUIPyQT.get_all_points.
        """
        if algo_name in ("CoskyAlgorithme", "CoskySQL"):
            return "auto"
        elif algo_name == "RankSky":
            return "Max"
        return "auto"

    def test_cosky_auto_behavior(self):
        """Verify that Cosky algorithms use Auto (majority-based) unification."""
        mode = self.get_expected_mode("CoskyAlgorithme")
        self.assertEqual(mode, "auto")
        
        data = {1: (10, 20, 30)}
        prefs = [Preference.MIN, Preference.MIN, Preference.MAX]
        # Majority is MIN -> idx 2 should be inverted
        unifier = DataUnifier(data, prefs, mode=mode)
        result = unifier.unify()
        self.assertEqual(result[1], (10, 20, 1/30))

    def test_ranksky_max_behavior(self):
        """Verify that RankSky uses Max unification."""
        mode = self.get_expected_mode("RankSky")
        self.assertEqual(mode, "Max")
        
        data = {1: (10, 20, 30)}
        prefs = [Preference.MIN, Preference.MIN, Preference.MAX]
        # Forced MAX -> MIN columns (0 and 1) should be inverted
        unifier = DataUnifier(data, prefs, mode=mode)
        result = unifier.unify()
        self.assertEqual(result[1], (1/10, 1/20, 30))

if __name__ == "__main__":
    unittest.main()
