from enum import Enum
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR

class AlgoEnum(Enum):
    """
    Enum class representing different Skyline algorithms along with their label and JSON file path.
    """

    CoskySql = ("CoSky 'Sql query'", "Assets/LatexData/OneAlgoData/CoskySql/ThreeColumnsData/ExecutionCoskySql369.json")
    CoskyAlgorithme = ("CoSky 'algorithm'", "Assets/LatexData/OneAlgoData/CoskyAlgo/ThreeColumnsData/ExecutionCoskyAlgo369.json")
    RankSky = ("RankSky", "Assets/LatexData/OneAlgoData/RankSky/ThreeColumnsData/ExecutionRankSky369.json")
    DpIdpDh = ("dp-idp with dominance hierarchy", "Assets/LatexData/OneAlgoData/DpIdpDh/ThreeColumnsData/ExecutionDpIdpDh369.json")
    SkyIR = ("SkyIR-UBS", "Assets/LatexData/OneAlgoData/SkyIR/ThreeColumnsData/ExecutionSkyIR369.json")

    def __init__(self, label: str, filepath: str):
        """
        Initialize each enum member.

        :param label: The display label for the algorithm.
        :param filepath: The JSON file path where the execution times are stored.
        """
        self.label = label
        self.filepath = filepath

    def get_algo_class(self):
        return {
            AlgoEnum.CoskySql: CoskySQL,
            AlgoEnum.CoskyAlgorithme: CoskyAlgorithme,
            AlgoEnum.RankSky: RankSky,
            AlgoEnum.DpIdpDh: DpIdpDh,
            AlgoEnum.SkyIR: SkyIR,
        }[self]


if __name__ == "__main__":
    # Example usage
    for algo in AlgoEnum:
        print(f"{algo.name}: {algo.label}, {algo.filepath}")
