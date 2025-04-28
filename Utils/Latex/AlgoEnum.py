from enum import Enum

class AlgoEnum(Enum):
    """
    Algo enum class to represent different algorithms and their associated file paths.
    """
    CoskySql = ("CoSky 'Sql query'", "Assets/LatexData/OneAlgoData/CoskySql/ThreeColumnsData/ExecutionCoskySql369.json")
    CoskyAlgorithme = ("CoSky 'algorithm'", "Assets/LatexData/OneAlgoData/CoskyAlgo/ThreeColumnsData/ExecutionCoskyAlgo369.json")
    RankSky = ("RankSky", "Assets/LatexData/OneAlgoData/RankSky/ThreeColumnsData/ExecutionRankSky369.json")
    DpIdpDh = ("dp-idp with dominance hierarchy", "Assets/LatexData/OneAlgoData/DpIdpDh/ThreeColumnsData/ExecutionDpIdpDh69.json")
    SkyIR = ("SkyIR-UBS", "Assets/LatexData/OneAlgoData/SkyIR/ThreeColumnsData/ExecutionSkyIR369.json")

    def __init__(self, label, filepath):
        """
        Initialize the enum with a label and file path.
        """
        self.label = label
        self.filepath = filepath


if __name__ == "__main__":
    # Example usage
    for algo in AlgoEnum:
        print(f"{algo.name}: {algo.label}, {algo.filepath}")
