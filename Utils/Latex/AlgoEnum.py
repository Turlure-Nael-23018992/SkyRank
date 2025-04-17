from enum import Enum

class AlgoEnum(Enum):
    """
    Enumération des algorithmes, avec nom lisible et chemin JSON associé.
    """
    CoskySql = ("CoSky 'Sql Querry'", "OneAlgoDatas/ExecutionCoskySql369.json")
    CoskyAlgorithme = ("CoSky 'Algorithm'", "OneAlgoDatas/ExecutionCoskyAlgo369.json")
    RankSky = ("RankSky 'Algorithm'", "OneAlgoDatas/ExecutionRankSky369.json")

    def __init__(self, label, filepath):
        self.label = label
        self.filepath = filepath
