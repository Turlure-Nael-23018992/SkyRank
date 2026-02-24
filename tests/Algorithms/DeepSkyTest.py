import sqlite3
import unittest
import os
import sys
import tempfile
from pathlib import Path

# Fix paths to include project root for dependencies
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Utils.DataModifier.DataNormalizerDeepSky import DataNormalizerDeepSky
from Utils.DataModifier.JsonUtils import readJson
from Algorithms.CoskySql import CoskySQL
from Algorithms.DeepSky import DeepSky
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Utils.Preference import Preference

class DeepSkyTest(unittest.TestCase):
    """
    Test suite for the DeepSky framework.
    Uses a temporary SQLite database to avoid binary file dependency in the repository.
    Verifies Top-K result harvesting across different underlying algorithms.
    """

    def setUp(self):
        """
        Prepares a temporary SQLite environment:
        1. Creates a dummy dataset with 6 diverse points.
        2. Generates a temporary .db file.
        3. Populates it using DataNormalizerDeepSky.
        """
        self.rTuples8 = {
            "1": (1, 10, 5),
            "2": (2, 5, 10),
            "3": (10, 1, 2),
            "4": (5, 5, 5),
            "5": (1, 1, 1),
            "6": (2, 2, 2)
        }
        self.k = 2
        
        # Windows-safe temporary file handling (delete=False to avoid permission issues during test)
        self.test_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        self.path = self.test_db_file
        
        # Initialize and refresh the DB table
        self.dataNorm = DataNormalizerDeepSky(self.rTuples8, self.path)
        self.dataNorm.refreshDb()

    def tearDown(self):
        """
        Cleanup: Closes database handles and removes the temporary file to avoid leaks/locks.
        """
        if hasattr(self, 'dataNorm') and self.dataNorm.conn:
            self.dataNorm.conn.close()
        
        if os.path.exists(self.test_db_file):
            try:
                os.remove(self.test_db_file)
            except PermissionError:
                # Common on Windows if another handle is lingering; ignore to avoid test failure
                pass

    def testDeepSkyCoskySql(self):
        """
        Integrated test: DeepSky + CoskySql.
        Ensures the SQL-based ranking correctly harvests exactly K points.
        """
        deepSky = DeepSky(self.path, self.k, CoskySQL)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "DeepSky(CoskySQL) should return exactly k items.")

    def testDeepSkyCoskyAlgo(self):
        """
        Integrated test: DeepSky + CoskyAlgorithme.
        Ensures the memory-based ranking harvested from the DB works as expected.
        """
        deepSky = DeepSky(self.path, self.k, CoskyAlgorithme)
        result = deepSky.topK
        self.assertEqual(self.k, len(result), "DeepSky(CoskyAlgo) should return exactly k items.")

    def testLargeK(self):
        """
        Edge case: verify behavior when requested K exceeds total data size.
        Should gracefully return all available points without crashing or padding.
        """
        large_k = 100
        # Use RankSky for high-speed verification
        deepSky = DeepSky(self.path, large_k, RankSky)
        self.assertEqual(len(deepSky.topK), 6, "If K > size, result should contain all available records.")

if __name__ == "__main__":
    unittest.main()
