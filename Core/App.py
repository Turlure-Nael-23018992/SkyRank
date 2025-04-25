from Utils.DatasModifier import DataNormalizer
from Utils.Latex.AlgoEnum import AlgoEnum
from Algorithms.CoskySql import CoskySQL
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DbObject import DbObject
from Utils.DataTypes.DictObject import DictObject
from Utils.DatasModifier.DataConverter import DataConverter
from Utils.DisplayHelpers import *
from Utils.DatasModifier.JsonUtils import *


class App:
    """
    Main class for the application.
    """

    def __init__(self, data, algo):
        """
        Initialize the application with the given database file path and JSON file path.
        :param data: Path to the database file.
        :param algo: Algorithm for data processing.
        """
        self.r = data.r if data.__name__() == "DictObject" else None
        self.jsonFp = data.fp if data.__name__() == "JsonObject" else None
        self.dbFp = data.fp if data.__name__() == "DbObject" else None
        self.dataName = data.__name__()
        self.algo = algo.__name__
        self.run()

    def run(self):
        """
        Run the application.
        """
        match (self.algo):
            case "CoskyAlgorithme":
                self.startCoskyAlgorithme()
            case "CoskySQL":
                self.startCoskySql()
            case "DP_IDP_DH":
                self.startDpIdpDh()
            case "RankSky":
                self.startRankSky()
            case "DeepSky":
                self.startDeepSky()
            case "SkyIR":
                self.startSkyIR()
            case _:
                print("Unknown algorithm")

    def startCoskySql(self):
        """
        Start the Cosky SQL algorithm.
        """
        print_red("start CoskySql")
        match self.dataName:
            case "DbObject":
                CoskySQL(self.dbFp)
            case "JsonObject":
                print("in jsonobject")
                dataConverter = DataConverter(self.jsonFp)
                dataConverter.jsonToDb()
                CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")
            case "DictObject":
                print("in dictobject")
                dataConverter = DataConverter(self.r)
                dataConverter.relationToDb()
                CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")

        pass

    def startCoskyAlgorithme(self):
        """
        Start the Cosky algorithm.
        """
        pass

    def startDpIdpDh(self):
        """
        Start the DP-IDP-DH algorithm.
        """
        pass

    def startRankSky(self):
        """
        Start the RankSky algorithm.
        """
        pass

    def startDeepSky(self):
        """
        Start the DeepSky algorithm.
        """
        pass

    def startSkyIR(self):
        """
        Start the SkyIR algorithm.
        """
        pass


if __name__ == "__main__":
    # Example usage
    print_red("1./ Bd")
    print_red("2./ Json")
    print_red("3./ Dict")
    a = input("Choose the type of data to use: ")
    if a == "1":
        dbFilepath = DbObject("../Assets/databases/cosky_db_C3_R2000.db")
        app = App(dbFilepath, CoskySQL)
    elif a == "2":
        jsonObjet = JsonObject("../Assets/AlgoExecution/JsonFiles/RTuples8.json")
        app = App(jsonObjet, CoskySQL)
    elif a == "3":
        data = readJson("../Assets/AlgoExecution/JsonFiles/RBig.json")
        DictObject = DictObject(data)
        app = App(DictObject, CoskySQL)
