import unittest
import json

from Algorithms.DeepSky import DeepSky

class DeepSkyTest(unittest.TestCase):
    def setUp(self):
        with open('../RBig.json', 'r') as f:
            r_big_loaded = json.load(f)
        # Convert the loaded dictionary values to tuples
        print(r_big_loaded)
        self.r_big_reloaded = {key: tuple(value) for key, value in r_big_loaded.items()}