import unittest
from bbs_py3.bbs.bbs import BBS
from bbs_py3.r_tree.rTree import RTree

class TestBBS(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the R-Tree and BBS instance.
        """
        # Create a r-Tree for the tests
        self.tree = RTree(M=4, m=2)
        # Insert some tuples into the tree
        self.tree.Insert(tupleId=1, minDim=[1, 2], maxDim=[3, 4])
        self.tree.Insert(tupleId=2, minDim=[2, 3], maxDim=[4, 5])
        self.tree.Insert(tupleId=3, minDim=[5, 6], maxDim=[7, 8])
        self.tree.Insert(tupleId=4, minDim=[6, 7], maxDim=[8, 9])

        self.bbs = BBS(self.tree)

    def test_skyline_output_types(self):
        """
        Test the skyline function.
        """
        # Define the expected skyline points
        skyline_points, comparisons, dominated_points, minIdp, see = self.bbs.skyline(sp=1, layer=0)

        # Check the types of the returned values
        self.assertIsInstance(skyline_points, list) # List of skyline points
        self.assertIsInstance(comparisons, int) # Number of dominance comparisons
        self.assertIsInstance(dominated_points, dict) # Dictionary of dominated points
        self.assertIsInstance(minIdp, dict) # Dictionary of dominated points at this level
        self.assertIsInstance(see, int) # Total number of dominated points

    def test_skyline(self):
        """
        Test the skyline function.
        """
        # Expected values
        expected_skyline_points = [3, 4]
        expected_comparisons = 2
        expected_dominated_points = {3: 0, 4: 0}
        expected_minIdp = {3: 1, 4: 1}
        expected_seen = 2

        skyline_points, comparisons, dominated_points, minIdp, see = self.bbs.skyline(sp=1, layer=0)

        #self.assertEqual(skyline_points, expected_skyline_points)

        self.assertEqual(comparisons, expected_comparisons)

        self.assertEqual(dominated_points, expected_dominated_points)

        self.assertEqual(minIdp, expected_minIdp)

        self.assertEqual(see, expected_seen)


    if __name__ == "main":
        unittest.main()





