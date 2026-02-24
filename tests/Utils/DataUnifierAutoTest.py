import sys
import os
import unittest

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Utils.DataModifier.DataUnifier import DataUnifier
from Utils.Preference import Preference

class TestDataUnifierAuto(unittest.TestCase):

    def test_majority_min(self):
        # 2 MIN, 1 MAX -> Majority MIN
        data = {1: (10, 20, 30), 2: (5, 40, 60)}
        prefs = [Preference.MIN, Preference.MIN, Preference.MAX]
        unifier = DataUnifier(data, prefs, mode="auto")
        
        unified_prefs = unifier.unifyPreferences()
        self.assertEqual(unified_prefs, [Preference.MIN, Preference.MIN, Preference.MIN])
        
        result = unifier.unify()
        self.assertEqual(result[1], (10, 20, 1/30))
        self.assertEqual(result[2], (5, 40, 1/60))

    def test_majority_max(self):
        # 1 MIN, 2 MAX -> Majority MAX
        data = {1: (10, 20, 30), 2: (5, 40, 60)}
        prefs = [Preference.MIN, Preference.MAX, Preference.MAX]
        unifier = DataUnifier(data, prefs, mode="auto")
        
        unified_prefs = unifier.unifyPreferences()
        self.assertEqual(unified_prefs, [Preference.MAX, Preference.MAX, Preference.MAX])
        
        result = unifier.unify()
        self.assertEqual(result[1], (1/10, 20, 30))
        self.assertEqual(result[2], (1/5, 40, 60))

    def test_equality_to_min(self):
        # 1 MIN, 1 MAX -> MIN (implementation choice)
        data = {1: (10, 20), 2: (5, 40)}
        prefs = [Preference.MIN, Preference.MAX]
        unifier = DataUnifier(data, prefs, mode="auto")
        
        unified_prefs = unifier.unifyPreferences()
        self.assertEqual(unified_prefs, [Preference.MIN, Preference.MIN])
        
        result = unifier.unify()
        self.assertEqual(result[1], (10, 1/20))

    def test_unify_min_mode(self):
        # Explicit MIN mode
        data = {1: (10, 20), 2: (5, 40)}
        prefs = [Preference.MAX, Preference.MAX]
        unifier = DataUnifier(data, prefs, mode="Min")
        
        result = unifier.unify()
        self.assertEqual(result[1], (1/10, 1/20))

    def test_unify_max_mode(self):
        # Explicit MAX mode
        data = {1: (10, 20), 2: (5, 40)}
        prefs = [Preference.MIN, Preference.MIN]
        unifier = DataUnifier(data, prefs, mode="Max")
        
        result = unifier.unify()
        self.assertEqual(result[1], (1/10, 1/20))

if __name__ == "__main__":
    unittest.main()
