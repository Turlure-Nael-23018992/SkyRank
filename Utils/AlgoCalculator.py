import json
import sqlite3

from Algorithms import CoskySql
from Algorithms.CoskySql import CoskySQL
from Utils.LatexMaker import LatexMaker
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Utils.DisplayHelpers import beauty_print
from Utils.DataParser import DataParser
from Database.DatabaseHelpers import Database
from Utils.TimerUtils import TimeCalc

ROWS_RATIO_MULT = pow(10, 3)
ROWS_RATIO_UNITS = [1, 2, 5, 10]
ROWS_RATIO = [x * ROWS_RATIO_MULT for x in ROWS_RATIO_UNITS]


class AlgoCalculator:
    """
    Class to calculate the response time of the algorithms
    """

    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)
        self.cursor = self.conn.cursor()
        self.latexMaker = LatexMaker()
        self.jsonFilePath = "../Assets/LatexDatas/"
        self.tableName = "Pokemon"
        self.conn = sqlite3.connect(fr"..\Assets\databases\{self.tableName}.db")

    def select_all(self):
        """
        Select all
        :return: All records from the table
        """
        sql_query = f"SELECT * FROM {self.tableName}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def compareExecutionTime(self, algo):
        """
        Compare the execution time of an algorithm on several databases of different sizes
        """
        # iterations = [8, 40, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 500000]
        # rows = ROWS_RATIO  # [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        cols = [3, 6, 9]
        rows = [50, 200, 500, 20000]
        time_dict = {k: [0 for i in range(len(cols))] for k in rows}
        self.jsonFilePath += "ExecutionCoskyDatas.json"
        max_rows = 0
        max_time = 0

        root_databases = fr"..\Assets\databases"
        i = -1
        for col in cols:
            i += 1
            for row in rows:
                # beauty_print("Column", col)
                # beauty_print("Row", rows)
                # Displays the execution time of each algorithm
                database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"  # Retrieve the path
                beauty_print("Database path", database_filepath)
                db = Database(database_filepath)
                sel = AlgoCalculator(database_filepath)
                r = DataParser(sel.select_all()).r_dict
                # The name of the algorithm class
                algo_name = algo.__name__
                print(f"\tALGO [{algo_name}]")
                time_calc = TimeCalc(row, algo_name)
                # For the SQL algorithm, add the connection object to the arguments
                if algo_name == "CoskySQL":
                    # Need a database path
                    algo_obj = algo(database_filepath)

                elif algo_name == "SkyIR":
                    # Needs a data dictionary
                    algo_obj = algo(r).skyIR(10)

                elif algo_name == "CoskyAlgorithme":
                    # Needs a data dictionary
                    algo_obj = algo(r)
                # Retrieve the execution time for each database on the given algorithm
                time_calc.stop()
                # Add the execution time to the dictionary
                current_time = time_calc.execution_time
                time_dict[row][i] = current_time

                if row > max_rows:
                    max_rows = row

                if current_time > max_time:
                    max_time = current_time

                # beauty_print("time_dict", time_dict)
        dataToSave = {
            "time_data": time_dict,  # The dictionary with execution times
            "max_rows": max_rows,  # The maximum number of rows
            "max_time": max_time  # The maximum execution time
        }
        beauty_print("time_dict", time_dict)

        with open("../Assets/LatexDatas/ExecutionCoskyDatas.json", "w") as f:
            # Save everything in the JSON file
            json.dump(dataToSave, f, indent=4)

    def compareExecutionTimeSqlAlgo(self):
        """
        Compare execution time of CoSky SQL and Algorithm
        """


# Algorithm declarations
COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
# DP_IDP_ = "DP_IDP"
CONFIG_DATA = "CONFIG_DATA"

# MODES contains all the algorithms to be compared
MODES = {
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    # DP_IDP_: DP_IDP,
}


if __name__ == "__main__":
    # Create an instance of the AlgoCalculator class
    calculator = AlgoCalculator("")
    calculator.compareExecutionTime(CoskySQL)