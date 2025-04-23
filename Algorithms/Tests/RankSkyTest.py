import unittest
import json
import numpy as np
from numpy.ma.testutils import assert_equal

from Algorithms.RankSky import RankSky
from Utils.Preference import Preference

class RankSkyTest(unittest.TestCase):
    """Test suite for the RankSky algorithm"""

    def setUp(self):
        """Method called before each test. It initializes the necessary variables and objects."""
        # Define an example relation and preferences for the tests
        self.r = {
            1: (5, 20, 70),
            2: (4, 60, 50),
            3: (5, 30, 60),
            4: (1, 80, 60),
            5: (5, 90, 40),
            6: (9, 30, 50),
            7: (7, 80, 40),
            8: (9, 90, 30)
        }
        self.pref = [Preference.MIN, Preference.MIN, Preference.MIN]
        self.rank_sky = RankSky(self.r, self.pref)

        self.initR = [[5,1], [2,3], [3,2]]

    def test_unifyPreferencesMin(self):
        """
        Test of the unifyPreferencesMin method.
        :return:
        """
        original_data = self.rank_sky.rUnifyTab.copy()
        self.rank_sky.unifyPreferencesMin(self.rank_sky.rUnifyTab, self.rank_sky.pref)

        # Verify that values have been correctly inverted for MAX dimensions
        for i, val in enumerate(original_data.values()):
            for j, pref in enumerate(self.pref):
                if pref == Preference.MAX:
                    self.assertNotEqual(val[j], self.rank_sky.rUnifyTab[i][j],
                                        "Values should not be the same after unification for MAX preferences.")

    def test_skylineComputation(self):
        """Test of the skylineComputation method."""
        self.rank_sky.skylineComputation()
        self.assertIsNotNone(self.rank_sky.sky, "The skyline computation should generate a non-null result.")
        self.assertGreater(len(self.rank_sky.sky), 0, "There should be elements in the skyline.")

    def test_squareMatrix(self):
        """Test of the squareMatrix method."""
        self.rank_sky.skylineComputation()  # Ensure the skyline is computed before testing the square matrix.
        self.rank_sky.initMatrix()  # Initialize the relation matrix
        self.rank_sky.squareMatrix()  # Compute the square matrix
        self.assertIsNotNone(self.rank_sky.a, "The square matrix should not be null after computation.")
        self.assertEqual(self.rank_sky.a.shape[0], self.rank_sky.a.shape[1],
                         "The square matrix should be a square matrix.")

    def test_stochasticMatrix(self):
        """Test of the stochasticMatrix method."""
        self.rank_sky.skylineComputation()  # Ensure the skyline is computed before testing the stochastic matrix.
        self.rank_sky.initMatrix()
        self.rank_sky.squareMatrix()  # Compute the square matrix before obtaining the stochastic matrix.
        self.rank_sky.stochasticMatrix()  # Compute the stochastic matrix
        self.assertIsNotNone(self.rank_sky.s, "The stochastic matrix should not be null.")
        self.assertTrue(np.allclose(np.sum(self.rank_sky.s, axis=1), 1),
                        "The rows of the stochastic matrix should sum to 1.")

    def test_googlePageRank(self):
        """Test of the googlePageRank method."""
        self.rank_sky.skylineComputation()
        self.rank_sky.initMatrix()
        self.rank_sky.squareMatrix()
        self.rank_sky.stochasticMatrix()
        self.rank_sky.googlePageRank()
        self.assertIsNotNone(self.rank_sky.g, "The PageRank matrix should not be null.")
        self.assertEqual(self.rank_sky.g.shape, (self.rank_sky.n, self.rank_sky.n),
                         "The PageRank matrix should be a square matrix of dimension n x n.")

    def test_Ipl(self):
        """Test of the Ipl method to calculate the PageRank vector."""
        self.rank_sky.skylineComputation()
        self.rank_sky.initMatrix()
        self.rank_sky.squareMatrix()
        self.rank_sky.stochasticMatrix()
        self.rank_sky.googlePageRank()
        self.rank_sky.Ipl()
        self.assertIsNotNone(self.rank_sky.vk, "The PageRank vector should not be null.")
        self.assertEqual(len(self.rank_sky.vk), self.rank_sky.n,
                         "The PageRank vector should have a size equal to the dimension of the matrix.")

    def test_sort(self):
        """Test of the sort method to check the order of the score vector."""
        self.rank_sky.skylineComputation()
        self.rank_sky.unifyPreferencesMax(self.rank_sky.sky, self.rank_sky.pref)
        self.rank_sky.initMatrix()
        self.rank_sky.squareMatrix()
        self.rank_sky.stochasticMatrix()
        self.rank_sky.googlePageRank()
        self.rank_sky.Ipl()
        self.rank_sky.sort()
        self.assertIsNotNone(self.rank_sky.score, "The score dictionary should not be null.")
        self.assertGreater(len(self.rank_sky.score), 0,
                           "There should be elements in the score dictionary.")

    def test_run(self):
        """Test of the complete process in the run method."""
        self.rank_sky.run()
        self.assertIsNotNone(self.rank_sky.score, "Scores should not be null after running the process.")
        self.assertGreater(len(self.rank_sky.score), 0, "Scores should be computed after running the process.")
