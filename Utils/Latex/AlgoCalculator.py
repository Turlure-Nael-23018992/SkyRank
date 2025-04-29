import json
import sqlite3
import sys
import os

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Algorithms import CoskySql
from Algorithms.CoskySql import CoskySQL
from Utils.Latex.LatexMaker import LatexMaker
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Utils.DisplayHelpers import beauty_print
from Utils.DataParser import DataParser
from Utils.TimerUtils import TimeCalc
from Algorithms.RankSky import RankSky
from Algorithms.DpIdpDh import DpIdpDh
from Utils.Preference import Preference
from Utils.DataModifier.JsonUtils import readJson, writeJson, sortJson, addServerConfigToJson
from Algorithms.SkyIR import SkyIR

# Constants for row scaling
ROWS_RATIO_MULT = pow(10, 3)
ROWS_RATIO_UNITS = [1, 2, 5, 10]
ROWS_RATIO = [x * ROWS_RATIO_MULT for x in ROWS_RATIO_UNITS]


class AlgoCalculator:
    """
    Class to calculate and store the response time of different Skyline algorithms.
    """

    def __init__(self, db_filepath: str):
        """
        Initialize the AlgoCalculator with the given database filepath.

        :param db_filepath: Path to the SQLite database.
        """
        self.conn = sqlite3.connect(db_filepath)
        self.cursor = self.conn.cursor()
        self.latexMaker = LatexMaker()
        self.jsonFilePath = "../Assets/LatexData/"
        self.tableName = "Pokemon"
        self.conn = sqlite3.connect(fr"..\..\Assets\databases\{self.tableName}.db")
        self.cols = [3, 6, 9]
        self.rows = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]

    def select_all(self):
        """
        Select and return all records from the configured database table.
        """
        sql_query = f"SELECT * FROM {self.tableName}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def compareExecutionTime(self, algo, fp: str, cols=None, rows=None):
        """
        Measure and store the execution time of a given algorithm on several databases of different sizes.

        :param algo: The algorithm class to execute (e.g., CoskySQL, RankSky, etc.)
        :param fp: The JSON file path where execution times should be stored.
        :param cols: List of column numbers (default: [3,6,9]).
        :param rows: List of row numbers (default: common experimental settings).
        """
        print(algo)
        if not cols:
            cols = self.cols
        if not rows:
            rows = self.rows

        print("rows : ", rows)
        print("cols : ", cols)

        time_dict = {k: [0 for i in range(len(self.cols))] for k in self.rows}
        self.jsonFilePath += "ExecutionRankSky369.json"
        max_rows = 0
        max_time = 0
        pref = [Preference.MIN, Preference.MIN, Preference.MIN]

        root_databases = fr"..\..\Assets\databases"
        i = -1

        for col in cols:
            i += 1
            for row in rows:
                database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"
                algo_name = algo.__name__
                beauty_print("Algorithm name ", algo_name)
                beauty_print("Database path ", database_filepath)

                time_calc = None

                if algo_name == "CoskySQL":
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(database_filepath)
                    time_calc.stop()

                elif algo_name == "SkyIR":
                    sel = AlgoCalculator(database_filepath)
                    r = DataParser(sel.select_all()).r_dict
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(r).skyIR(10)
                    time_calc.stop()

                elif algo_name == "CoskyAlgorithme":
                    sel = AlgoCalculator(database_filepath)
                    r = DataParser(sel.select_all()).r_dict
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(r)
                    time_calc.stop()

                elif algo_name == "RankSky":
                    sel = AlgoCalculator(database_filepath)
                    r = DataParser(sel.select_all()).r_dict
                    print("algo lancé")
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(r, pref)
                    time_calc.stop()

                elif algo_name == "DpIdpDh":
                    sel = AlgoCalculator(database_filepath)
                    r = DataParser(sel.select_all()).r_dict
                    print("algo lancé")
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(r)
                    time_calc.stop()

                current_time = time_calc.execution_time
                print(current_time)

                if algo_name == "RankSky":
                    time_dict[row][i] = algo_obj.time

                if row > max_rows:
                    max_rows = row
                if current_time > max_time:
                    max_time = current_time

                row_str = str(row)
                try:
                    savedDatas = readJson(fp)
                except (FileNotFoundError, json.JSONDecodeError):
                    savedDatas = {}

                time_data = savedDatas.get("time_data", {})
                if row_str not in time_data:
                    time_data[row_str] = ["NA", "NA", "NA"]

                col_to_index = {3: 0, 6: 1, 9: 2}
                if col not in col_to_index:
                    continue
                k = col_to_index[col]

                previous_time = time_data[row_str][k]
                try:
                    prev_val = float(previous_time)
                except (ValueError, TypeError):
                    prev_val = float('inf')

                if current_time < prev_val:
                    time_data[row_str][k] = current_time

                max_rows = max(int(savedDatas.get("max_rows", 0)), row)
                max_time = max(savedDatas.get("max_time", 0), current_time)

                dataToSave = {
                    "time_data": time_data,
                    "max_rows": max_rows,
                    "max_time": max_time
                }

                writeJson(fp, dataToSave)
                addServerConfigToJson(fp, "../../Assets/ServerConfig/ConfigNael.json")
                sortJson(fp)


# Algorithm declarations
COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
CONFIG_DATA = "CONFIG_DATA"
RANK_SKY = "RANK_SKY"

# Mapping for algorithm names to classes
MODES = {
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    "DpIdpDh": DpIdpDh,
    RANK_SKY: RankSky,
    "SkyIR": SkyIR,
}


if __name__ == "__main__":
    calculator = AlgoCalculator("")
    """calculator.compareExecutionTime(
        CoskySQL,
        "../../Assets/test.json",
        cols=[],
        rows=[]
    )"""
