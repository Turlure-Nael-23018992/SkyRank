import unittest
import json
from collections import OrderedDict

from Algorithms.CoskyAlgorithme import CoskyAlgorithme


class CoskyAlgoTest(unittest.TestCase):
    """
    Test class for the Cosky algorithm.
    """

    def setUp(self):
        """
        Setup method to initialize the CoskyAlgorithme instance.
        """
        with open('../Datas/RBig.json', 'r') as f:
            r_big_loaded = json.load(f)

        # Convert the loaded dictionary values to tuples
        self.r_big_reloaded = {key: tuple(value) for key, value in r_big_loaded.items()}

        # Expected values with keys converted to integers
        self.expected_values = {
            103: [1, 63, 0.0886754904499806, 0.5563069153560654],
            150: [1, 81, 0.0238015221847852, 0.744486440507893],
            32: [5, 68, 0.00101601862031575, 0.9881951629372444],
            382: [5, 16, 0.0290286872591493, 0.8536447098741473],
            399: [1, 37, 0.105243370873928, 0.3925627936821398],
            496: [1, 10, 0.123358262237618, 0.18326805476129948],
            541: [6, 113, 0.000471306256019766, 0.953194312519765],
            551: [6, 13, 0.0569350631190667, 0.7448746655457289],
            593: [2, 15, 0.0582544098560979, 0.5406510449527204],
            604: [8, 11, 0.0481795194440872, 0.7757600377716273],
            67: [2, 17, 0.00315426440199051, 0.9950462086984445],
            89: [3, 11, 0.0714556428342785, 0.5268573236431924]
        }

        # Run CoskyAlgorithme and sort the output dictionary
        self.cosky_algo = CoskyAlgorithme(self.r_big_reloaded).s
        # Convert the keys to integers
        self.cosky_algo = {int(k): v for k, v in self.cosky_algo.items()}
        print(self.cosky_algo)  # Vérification

    def test_cosky_algo(self):
        """
        Test the Cosky algorithm with a sample dataset.
        """
        self.assertEqual(self.cosky_algo, self.expected_values)


if __name__ == '__main__':
    print("Running tests...")
    unittest.main()
