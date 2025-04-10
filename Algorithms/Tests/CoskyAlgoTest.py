import unittest
import json

from Algorithms.CoskyAlgorithme import CoskyAlgorithme

class CoskyAlgoTest(unittest.TestCase):

    def setUp(self):
        with open('../r_big.json', 'r') as f:
            r_big_loaded = json.load(f)

        # Convert the loaded dictionary values to tuples
        self.r_big_reloaded = {key: tuple(value) for key, value in r_big_loaded.items()}


    def test_cosky_algo(self):
        """
        Test the Cosky algorithm with a sample dataset.
        """
        expected_values = {32: [5, 68, 0.00101601862031575, 0.9881951629372444],
                           67: [2, 17, 0.00315426440199051, 0.9950462086984445],
                           89: [3, 11, 0.0714556428342785, 0.5268573236431923],
                           103: [1, 63, 0.0886754904499806, 0.5563069153560651],
                           150: [1, 81, 0.0238015221847852, 0.7444864405078929],
                           382: [5, 16, 0.0290286872591493, 0.8536447098741473],
                           399: [1, 37, 0.105243370873928, 0.39256279368213964],
                           496: [1, 10, 0.123358262237618, 0.18326805476129943],
                           541: [6, 113, 0.000471306256019766, 0.953194312519765],
                           551: [6, 13, 0.0569350631190667, 0.7448746655457289],
                           593: [2, 15, 0.0582544098560979, 0.5406510449527204],
                           604: [8, 11, 0.0481795194440872, 0.7757600377716272]}

        self.assertEqual(CoskyAlgorithme(self.r_big_reloaded), expected_values)


    if __name__ == '__main__':
        unittest.main()