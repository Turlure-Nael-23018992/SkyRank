import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Core.App import App
from Algorithms.SkyIR import SkyIR
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
from Algorithms.RankSky import RankSky
from Utils.DataTypes.DictObject import DictObject
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DbObject import DbObject
from Utils.Preference import Preference

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Small 3-column dataset (8 tuples) used as the reference for all tests
RAW_DATA = {
    1: (5, 20, 0.014),
    2: (4, 60, 0.02),
    3: (5, 30, 0.016),
    4: (1, 80, 0.016),
    5: (5, 90, 0.025),
    6: (9, 30, 0.02),
    7: (7, 80, 0.025),
    8: (9, 90, 0.033),
}

PREFS_3 = [Preference.MIN, Preference.MIN, Preference.MIN]

JSON_PATH = os.path.join(BASE_DIR, "Assets", "AlgoExecution", "JsonFiles", "RTuples8.json")
DB_PATH   = os.path.join(BASE_DIR, "Assets", "Databases", "cosky_db_C3_R10.db")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _has_results(app: App) -> bool:
    """Returns True if the algo_instance produced at least one result."""
    inst = app.algo_instance
    if inst is None:
        return False
    # Each algorithm exposes results through a different attribute
    for attr in ("result", "score", "s", "dict"):
        val = getattr(inst, attr, None)
        if val is not None and len(val) > 0:
            return True
    return False


# ---------------------------------------------------------------------------
# SkyIR
# ---------------------------------------------------------------------------

class TestAppSkyIR(unittest.TestCase):
    """Integration tests for SkyIR via the App API."""

    def test_dict(self):
        """SkyIR runs on a DictObject and returns skyline results."""
        app = App(DictObject(RAW_DATA), SkyIR)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "SkyIR (DictObject) returned no results.")

    def test_json(self):
        """SkyIR runs on a JsonObject and returns skyline results."""
        app = App(JsonObject(JSON_PATH), SkyIR)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "SkyIR (JsonObject) returned no results.")

    def test_db(self):
        """SkyIR runs on a DbObject and returns skyline results."""
        app = App(DbObject(DB_PATH), SkyIR)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "SkyIR (DbObject) returned no results.")


# ---------------------------------------------------------------------------
# DpIdpDh
# ---------------------------------------------------------------------------

class TestAppDpIdpDh(unittest.TestCase):
    """Integration tests for DpIdpDh via the App API."""

    def test_dict(self):
        """DpIdpDh runs on a DictObject and returns scored results."""
        app = App(DictObject(RAW_DATA), DpIdpDh)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "DpIdpDh (DictObject) returned no results.")

    def test_json(self):
        """DpIdpDh runs on a JsonObject and returns scored results."""
        app = App(JsonObject(JSON_PATH), DpIdpDh)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "DpIdpDh (JsonObject) returned no results.")

    def test_db(self):
        """DpIdpDh runs on a DbObject and returns scored results."""
        app = App(DbObject(DB_PATH), DpIdpDh)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "DpIdpDh (DbObject) returned no results.")


# ---------------------------------------------------------------------------
# CoskyAlgorithme
# ---------------------------------------------------------------------------

class TestAppCoskyAlgorithme(unittest.TestCase):
    """Integration tests for CoskyAlgorithme via the App API."""

    def test_dict(self):
        """CoskyAlgorithme runs on a DictObject and returns scored results."""
        app = App(DictObject(RAW_DATA), CoskyAlgorithme, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskyAlgorithme (DictObject) returned no results.")

    def test_json(self):
        """CoskyAlgorithme runs on a JsonObject and returns scored results."""
        app = App(JsonObject(JSON_PATH), CoskyAlgorithme, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskyAlgorithme (JsonObject) returned no results.")

    def test_db(self):
        """CoskyAlgorithme runs on a DbObject and returns scored results."""
        app = App(DbObject(DB_PATH), CoskyAlgorithme, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskyAlgorithme (DbObject) returned no results.")


# ---------------------------------------------------------------------------
# CoskySQL
# ---------------------------------------------------------------------------

class TestAppCoskySQL(unittest.TestCase):
    """Integration tests for CoskySQL via the App API."""

    def test_dict(self):
        """CoskySQL runs on a DictObject (converted to SQLite) and returns results."""
        app = App(DictObject(RAW_DATA), CoskySQL, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskySQL (DictObject) returned no results.")

    def test_json(self):
        """CoskySQL runs on a JsonObject (converted to SQLite) and returns results."""
        app = App(JsonObject(JSON_PATH), CoskySQL, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskySQL (JsonObject) returned no results.")

    def test_db(self):
        """CoskySQL runs on a DbObject and returns results."""
        app = App(DbObject(DB_PATH), CoskySQL, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "CoskySQL (DbObject) returned no results.")


# ---------------------------------------------------------------------------
# RankSky
# ---------------------------------------------------------------------------

class TestAppRankSky(unittest.TestCase):
    """Integration tests for RankSky via the App API."""

    def test_dict(self):
        """RankSky runs on a DictObject and returns ranked skyline points."""
        app = App(DictObject(RAW_DATA), RankSky, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "RankSky (DictObject) returned no results.")

    def test_json(self):
        """RankSky runs on a JsonObject and returns ranked skyline points."""
        app = App(JsonObject(JSON_PATH), RankSky, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "RankSky (JsonObject) returned no results.")

    def test_db(self):
        """RankSky runs on a DbObject and returns ranked skyline points."""
        app = App(DbObject(DB_PATH), RankSky, preferences=PREFS_3)
        self.assertIsNotNone(app.algo_instance)
        self.assertTrue(_has_results(app), "RankSky (DbObject) returned no results.")

    def test_missing_preferences_raises(self):
        """RankSky raises ValueError when no preferences are provided."""
        with self.assertRaises(ValueError):
            App(DictObject(RAW_DATA), RankSky)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
