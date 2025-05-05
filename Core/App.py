import sys
import os
import sqlite3
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algorithms.CoskySql import CoskySQL
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR

from Database.DatabaseHelpers import Database
from Utils.Preference import Preference
from Utils.DataModifier.DataConverter import DataConverter
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DbObject import DbObject
from Utils.DataTypes.DictObject import DictObject
from Utils.DisplayHelpers import *
from Utils.DataModifier.JsonUtils import *


class App:
    """
    Main application class to run algorithms on different types of input data
    and delegate the results to an exporter.
    """

    def __init__(self, data, algo, exporter=None, input_type=None, input_file=None):
        self.tableName = "Pokemon"
        self.exporter = exporter
        self.cardinality = None
        self.tuples = None
        self.algo_instance = None
        self.execution_time = 0

        self.input_type = input_type or "Unknown"
        self.input_file = input_file or "generated"

        if isinstance(data, DictObject):
            self.r = data.r
            self.dataName = "DictObject"
        elif isinstance(data, JsonObject):
            self.jsonFp = data.fp
            self.dataName = "JsonObject"
        elif isinstance(data, DbObject):
            self.dbFp = data.fp
            self.dataName = "DbObject"
        else:
            raise ValueError("Unsupported data type.")

        self.algo = algo.__name__

        start = time.perf_counter()
        self.run()
        end = time.perf_counter()
        self.execution_time = round(end - start, 6)

        if self.algo_instance and not hasattr(self.algo_instance, "time"):
            self.algo_instance.time = self.execution_time

        if self.exporter:
            self.exporter.export(self)

    @staticmethod
    def askPreference():
        val = input("Min/Max : ").strip()
        return Preference.MIN if val.lower() == "min" else Preference.MAX

    def run(self):
        match self.algo:
            case "CoskyAlgorithme":
                self.startCoskyAlgorithme()
            case "CoskySQL":
                self.startCoskySql()
            case "DpIdpDh":
                self.startDpIdpDh()
            case "RankSky":
                print_red("Choose your preferences:")
                a = self.askPreference()
                b = self.askPreference()
                c = self.askPreference()
                self.pref = [a, b, c]
                self.startRankSky()
            case "SkyIR":
                self.startSkyIR()
            case _:
                print("Unknown algorithm.")

    def startCoskySql(self):
        print_red("Starting CoskySQL")
        match self.dataName:
            case "DbObject":
                self.cardinality, self.tuples = self.extractDbData(self.dbFp)
                self.algo_instance = CoskySQL(self.dbFp)
            case "JsonObject":
                dataConverter = DataConverter(self.jsonFp)
                dataConverter.jsonToDb()
                self.cardinality, self.tuples = self.extractDbData("../Assets/AlgoExecution/DbFiles/TestExecution.db")
                self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")
            case "DictObject":
                dataConverter = DataConverter(self.r)
                dataConverter.relationToDb()
                self.cardinality, self.tuples = self.extractDbData("../Assets/AlgoExecution/DbFiles/TestExecution.db")
                self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")

    def startCoskyAlgorithme(self):
        print_red("Starting CoskyAlgorithme")
        match self.dataName:
            case "DbObject":
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = CoskyAlgorithme(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = CoskyAlgorithme(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = CoskyAlgorithme(self.r)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startDpIdpDh(self):
        print_red("Starting DpIdpDh")
        match self.dataName:
            case "DbObject":
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = DpIdpDh(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = DpIdpDh(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = DpIdpDh(self.r)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startRankSky(self):
        print_red("Starting RankSky")
        match self.dataName:
            case "DbObject":
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = RankSky(data, self.pref)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = RankSky(data, self.pref)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = RankSky(self.r, self.pref)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startSkyIR(self):
        print_red("Starting SkyIR")
        match self.dataName:
            case "DbObject":
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = SkyIR(data)
                self.algo_instance.skyIR(10)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = SkyIR(data)
                self.algo_instance.skyIR(10)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = SkyIR(self.r)
                self.algo_instance.skyIR(10)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def extractDbData(self, db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(f"PRAGMA table_info({self.tableName})")
        columns_info = cur.fetchall()

        if not columns_info:
            print_red(f"Warning: No columns found for table '{self.tableName}'.")
            return 0, 0

        columns = [col[1] for col in columns_info if col[1].lower() != "rowid"]

        cur.execute(f"SELECT COUNT(*) FROM {self.tableName}")
        row_count = cur.fetchone()[0]

        conn.close()

        return len(columns), row_count
