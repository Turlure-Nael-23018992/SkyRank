from enum import Enum

class AlgoEnum(Enum):
    """
    Algo enum class to represent different algorithms and their associated file paths.
    """
    CoskySql = ("CoSky 'Sql query'", "Assets/LatexDatas/OneAlgoDatas/CoskySql/ThreeColumnsDatas/ExecutionCoskySql369.json")
    CoskyAlgorithme = ("CoSky 'algorithm'", "Assets/LatexDatas/OneAlgoDatas/CoskyAlgo/ThreeColumnsDatas/ExecutionCoskyAlgo369.json")
    RankSky = ("RankSky", "Assets/LatexDatas/OneAlgoDatas/RankSky/ThreeColumnsDatas/ExecutionRankSky369.json")
    DpIdpDh = ("dp-idp with dominance hierarchy", "Assets/LatexDatas/OneAlgoDatas/DpIdpDh/ThreeColumnsDatas/ExecutionDpIdpDh69.json")
    SkyIR = ("SkyIR-UBS", "Assets/LatexDatas/OneAlgoDatas/SkyIR/ThreeColumnsDatas/ExecutionSkyIR369.json")

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
