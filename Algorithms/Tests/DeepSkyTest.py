import unittest
from Utils.JsonUtils import readJson, writeJson, updateJson, sortJson, prettyPrintTimeData

from Algorithms.DeepSky import DeepSky

class DeepSkyTest(unittest.TestCase):
    def setUp(self):
        r_big_loaded = readJson("../Datas/RBig.json")
        # Convert the loaded dictionary values to tuples
        print(r_big_loaded)
        self.r_big_reloaded = {key: tuple(value) for key, value in r_big_loaded.items()}