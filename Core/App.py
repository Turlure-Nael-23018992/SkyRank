import sys
import os
import sqlite3

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

    def __init__(self, data, algo, exporter=None):
        """
        Initialize the application.

        :param data: Input data (DbObject, JsonObject, or DictObject).
        :param algo: Algorithm class to execute.
        :param exporter: Exporter instance (optional).
        """
        self.tableName = "Pokemon"
        self.exporter = exporter
        self.cardinality = None
        self.tuples = None
        self.algo_instance = None

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
        self.run()

    @staticmethod
    def askPreference():
        """
        Ask user for MIN/MAX preference.
        """
        val = input("Min/Max : ").strip()
        return Preference.MIN if val.lower() == "min" else Preference.MAX

    def run(self):
        """
        Main runner that selects and executes the corresponding algorithm.
        """
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

        # Export the result if an exporter is provided
        if self.exporter:
            self.exporter.export(self)

    def startCoskySql(self):
        """
        Start the Cosky SQL algorithm.
        """
        print_red("Starting CoskySQL")
        match self.dataName:
            case "DbObject":
                self.cardinality, self.tuples = self.extractDbData(self.dbFp)
                self.algo_instance = CoskySQL(self.dbFp)
            case "JsonObject":
                print("Input from JSON")
                dataConverter = DataConverter(self.jsonFp)
                dataConverter.jsonToDb()
                self.cardinality, self.tuples = self.extractDbData("../Assets/AlgoExecution/DbFiles/TestExecution.db")
                self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")
            case "DictObject":
                print("Input from Dictionary")
                dataConverter = DataConverter(self.r)
                dataConverter.relationToDb()
                self.cardinality, self.tuples = self.extractDbData("../Assets/AlgoExecution/DbFiles/TestExecution.db")
                self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db")

    def startCoskyAlgorithme(self):
        """
        Start the Cosky Algorithm.
        """
        print_red("Starting CoskyAlgorithme")
        match self.dataName:
            case "DbObject":
                print("Input from Database")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = CoskyAlgorithme(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                print("Input from JSON")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = CoskyAlgorithme(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                print("Input from Dictionary")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = CoskyAlgorithme(self.r)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startDpIdpDh(self):
        """
        Start the DP-IDP-DH algorithm.
        """
        print_red("Starting DpIdpDh")
        match self.dataName:
            case "DbObject":
                print("Input from Database")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = DpIdpDh(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                print("Input from JSON")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = DpIdpDh(data)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                print("Input from Dictionary")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = DpIdpDh(self.r)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startRankSky(self):
        """
        Start the RankSky algorithm.
        """
        print_red("Starting RankSky")
        match self.dataName:
            case "DbObject":
                print("Input from Database")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = RankSky(data, self.pref)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                print("Input from JSON")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = RankSky(data, self.pref)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                print("Input from Dictionary")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = RankSky(self.r, self.pref)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def startSkyIR(self):
        """
        Start the SkyIR algorithm.
        """
        print_red("Starting SkyIR")
        match self.dataName:
            case "DbObject":
                print("Input from Database")
                dataConverter = DataConverter(self.dbFp)
                data = dataConverter.dbToRelation()
                self.algo_instance = SkyIR(data)
                self.algo_instance.skyIR(10)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "JsonObject":
                print("Input from JSON")
                dataConverter = DataConverter(self.jsonFp)
                data = dataConverter.jsonToRelation()
                self.algo_instance = SkyIR(data)
                self.algo_instance.skyIR(10)
                self.cardinality = len(data[list(data.keys())[0]])
                self.tuples = len(data)
            case "DictObject":
                print("Input from Dictionary")
                self.r = {k: tuple(v) for k, v in self.r.items()}
                self.algo_instance = SkyIR(self.r)
                self.algo_instance.skyIR(10)
                self.cardinality = len(next(iter(self.r.values())))
                self.tuples = len(self.r)

    def extractDbData(self, db_path):
        """
        Extract the number of real data columns (excluding rowId) and the number of tuples from a SQLite database.

        :param db_path: Path to the database file
        :return: (cardinality, number of tuples)
        """
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Correctly select the right table
        cur.execute(f"PRAGMA table_info({self.tableName})")
        columns_info = cur.fetchall()

        if not columns_info:
            print_red(f"Warning: No columns found for table '{self.tableName}'. Check the table name.")
            return 0, 0

        # Remove rowId if needed
        columns = [col[1] for col in columns_info if col[1].lower() != "rowid"]

        # Get number of rows
        cur.execute(f"SELECT COUNT(*) FROM {self.tableName}")
        row_count = cur.fetchone()[0]

        conn.close()

        return len(columns), row_count


if __name__ == "__main__":
    from Utils.Exporter.CsvExporter import CsvExporter

    print_red("Choose the type of data:")
    print_red("1./ Database")
    print_red("2./ JSON")
    print_red("3./ Dictionary")
    print_red("4./ Generate a random database")
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
        print_red("Invalid data choice.")
        sys.exit(1)

    print_red("\nChoose the algorithm:")
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

    if algo_choice not in algo_map:
        print_red("Invalid algorithm choice.")
        sys.exit(1)

    exporter = CsvExporter(output_path="Results.csv")

    # Launch App with selected data, algorithm, and exporter
    app = App(data, algo_map[algo_choice], exporter=exporter)
    print_green("Execution completed.")