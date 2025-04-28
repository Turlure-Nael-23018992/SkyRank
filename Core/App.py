import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algorithms.CoskySql import CoskySQL
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR

from Database.DatabaseHelpers import Database
from Utils.Preference import Preference
from Utils.DatasModifier.DataNormalizerDeepSky import DataNormalizerDeepSky
from Utils.Latex.AlgoEnum import AlgoEnum
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
        if isinstance(data, DictObject):
            self.r = data.r
            self.dataName = "DictObject"
        elif isinstance(data, JsonObject):
            self.jsonFp = data.fp
            self.dataName = "JsonObject"
        elif isinstance(data, DbObject):
            self.dbFp = data.fp
            self.dataName = "DbObject"
        self.algo = algo.__name__
        self.run()

    @staticmethod
    def askPreference():
        val = input("Min/Max : ").strip()
        return Preference.MIN if val.lower() == "min" else Preference.MAX

    def run(self):
        """
        Run the application.
        """
        match self.algo:
            case "CoskyAlgorithme":
                self.startCoskyAlgorithme()
            case "CoskySQL":
                self.startCoskySql()
            case "DpIdpDh":
                self.startDpIdpDh()
            case "RankSky":
                print_red("1./ Choisissez vos préférences : ")
                a = self.askPreference()
                b = self.askPreference()
                c = self.askPreference()
                self.pref = [a, b, c]

                self.startRankSky()
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
        print_red("start CoskyAlgorithme")
        match self.dataName:
            case "DbObject":
                print("in dbobject")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                coskyAlgorithme = CoskyAlgorithme(data)
                #coskyAlgorithme = CoskyAlgorithme(data)
            case "JsonObject":
                print("in jsonobject")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                coskyAlgorithme = CoskyAlgorithme(data)
            case "DictObject":
                print("in dictobject")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                coskyAlgorithme = CoskyAlgorithme(self.r)

    def startDpIdpDh(self):
        """
        Start the DP-IDP-DH algorithm.
        """
        print_red("start DpIdpDh")
        match self.dataName:
            case "DbObject":
                print("in dbobject")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                DpIdpDh(data)
            case "JsonObject":
                print("in jsonobject")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                DpIdpDh(data)
            case "DictObject":
                print("in dictobject")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                dpIdpDh = DpIdpDh(self.r)

    def startRankSky(self):
        """
        Start the RankSky algorithm.
        """
        print_red("start RankSky")
        match self.dataName:
            case "DbObject":
                print("in dbobject")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                rankSky = RankSky(data, self.pref)
            case "JsonObject":
                print("in jsonobject")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                rankSky = RankSky(data, self.pref)
            case "DictObject":
                print("in dictobject")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                rankSky = RankSky(self.r, self.pref)

    def startSkyIR(self):
        """
        Start the SkyIR algorithm.
        """
        match self.dataName:
            case "DbObject":
                print("in dbobject")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                skyIR = SkyIR(data)
                skyIR.skyIR(10)
            case "JsonObject":
                print("in jsonobject")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                skyIR = SkyIR(data)
                skyIR.skyIR(10)
            case "DictObject":
                print("in dictobject")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                skyIR = SkyIR(self.r)
                skyIR.skyIR(10)


if __name__ == "__main__":
    print_red("Choisissez le type de données :")
    print_red("1./ Bd")
    print_red("2./ Json")
    print_red("3./ Dict")
    print_red("4./ Generer une base de données")
    data_choice = input("Your choice: ").strip()

    if data_choice == "1":
        data = DbObject("../Assets/databases/cosky_db_C3_R1000.db")
    elif data_choice == "2":
        data = JsonObject("../Assets/AlgoExecution/JsonFiles/RTuples8.json")
    elif data_choice == "3":
        raw_data = readJson("../Assets/AlgoExecution/JsonFiles/RBig.json")
        data = DictObject(raw_data)
    elif data_choice == "4":
        db = Database("../Assets/AlgoExecution/DbFiles/TestExecution.db", 3, 1000)
        data = DbObject("../Assets/AlgoExecution/DbFiles/TestExecution.db")
    else:
        print_red("Choix invalide pour les données.")
        sys.exit(1)

    print_red("\nChoisissez l'algorithme (1,2,3,4,5) :")
    print_red("1./ SkyIR")
    print_red("2./ DpIdpDh")
    print_red("3./ CoskyAlgorithme")
    print_red("4./ CoskySQL")
    print_red("5./ RankSky")
    algo_choice = input("Your choice: ").strip()

    algo_map = {
        "1": SkyIR,
        "2": DpIdpDh,
        "3": CoskyAlgorithme,
        "4": CoskySQL,
        "5": RankSky,
    }

    if algo_choice in algo_map:
        app = App(data, algo_map[algo_choice])
    else:
        print_red("Choix invalide pour l'algorithme.")
        sys.exit(1)



