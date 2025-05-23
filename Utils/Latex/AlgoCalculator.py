import json
import sqlite3
import sys
import os

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Algorithms import CoskySql
from Algorithms.CoskySql import CoskySQL
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
    def __init__(self, db_filepath: str):
        abs_db_path = os.path.abspath(db_filepath)
        self.conn = sqlite3.connect(abs_db_path)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"
        self.cols = [3, 6, 9]
        self.rows = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]

    def select_all(self):
        self.cursor.execute(f"SELECT * FROM {self.tableName}")
        return self.cursor.fetchall()

    def compareExecutionTime(self, algo, fp: str, cols=None, rows=None, pref=None, config=None):
        if not cols:
            cols = self.cols
        if not rows:
            rows = self.rows

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        root_databases = os.path.join(root_dir, 'Assets', 'Databases')
        abs_json_path = os.path.abspath(fp)

        max_rows = 0
        max_time = 0
        if pref is None:
            pref = [Preference.MIN] * 3

        for i, col in enumerate(cols):
            for row in rows:
                db_file = os.path.join(root_databases, f"cosky_db_C{col}_R{row}.db")
                algo_name = algo.__name__
                beauty_print("Algorithm name ", algo_name)
                beauty_print("Database path ", db_file)

                time_calc = None

                if algo_name == "CoskySQL":
                    time_calc = TimeCalc(row, algo_name)
                    algo_obj = algo(db_file, pref)
                    time_calc.stop()

                elif algo_name == "SkyIR":
                    sel = AlgoCalculator(db_file)
                    r = DataParser(sel.select_all()).r_dict
                    time_calc = TimeCalc(row, algo_name)
                    algo(r).skyIR(10)
                    time_calc.stop()

                elif algo_name in ["CoskyAlgorithme", "RankSky", "DpIdpDh"]:
                    sel = AlgoCalculator(db_file)
                    r = DataParser(sel.select_all()).r_dict
                    time_calc = TimeCalc(row, algo_name)
                    if algo_name == "CoskyAlgorithme":
                        algo_obj = algo(r, pref)
                    elif algo_name == "RankSky":
                        algo_obj = algo(r, pref)
                    else:
                        algo_obj = algo(r)
                    time_calc.stop()

                current_time = time_calc.execution_time

                try:
                    saved = readJson(abs_json_path)
                except (FileNotFoundError, json.JSONDecodeError):
                    saved = {}

                time_data = saved.get("time_data", {})
                row_str = str(row)
                if row_str not in time_data:
                    time_data[row_str] = ["NA", "NA", "NA"]

                col_to_index = {3: 0, 6: 1, 9: 2}
                idx = col_to_index[col]
                try:
                    prev_val = float(time_data[row_str][idx])
                except (ValueError, TypeError):
                    prev_val = float('inf')

                if current_time < prev_val:
                    time_data[row_str][idx] = current_time

                max_rows = max(int(saved.get("max_rows", 0)), row)
                max_time = max(saved.get("max_time", 0), current_time)

                dataToSave = {
                    "time_data": time_data,
                    "max_rows": max_rows,
                    "max_time": max_time
                }

                writeJson(abs_json_path, dataToSave)
                if config:
                    addServerConfigToJson(abs_json_path, os.path.join(root_dir, "Assets", "ServerConfig", "ConfigNael.json"))
                sortJson(abs_json_path)



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
    alg = AlgoCalculator(fr"../../Assets/databases/cosky_db_C3_R1000.db")
    alg.compareExecutionTime(CoskySQL, "../../Assets/AlgoExecution/ExecutionTime/CoskySql.json", cols=[3], rows=[10, 20, 50, 1000], pref=[Preference.MIN] * 3)
    alg.compareExecutionTime(CoskySQL, "../../Assets/AlgoExecution/ExecutionTime/CoskySql.json", cols=[6], rows=[10, 20, 50, 1000], pref=[Preference.MIN] * 6)
    alg.compareExecutionTime(CoskySQL, "../../Assets/AlgoExecution/ExecutionTime/CoskySql.json", cols=[9], rows=[10, 20, 50, 1000], pref=[Preference.MIN] * 9)