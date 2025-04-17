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
from Utils.Preference import Preference

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
        self.conn = sqlite3.connect(fr"..\..\Assets\databases\{self.tableName}.db")
        self.cols = [3,6,9]
        self.rows = [10,20,50,100,200,500, 1000, 2000,5000, 10000, 20000, 50000, 100000, 200000]#20, 100, 1000, 2000, 5000, 10000, 20000, 50000 , 5000, 10000, 20000, 50000, 100000, 200000
        #
    def select_all(self):
        """
        Select all
        :return: All records from the table
        """
        sql_query = f"SELECT * FROM {self.tableName}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def sortJson(self, fp):
        with open(fp, "r") as f:
            data = json.load(f)

        time_data = data.get("time_data", {})
        sorted_time_data = dict(sorted(time_data.items(), key=lambda item: int(item[0])))

        data["time_data"] = sorted_time_data

        with open(fp, "w") as f:
            json.dump(data, f, indent=4)

    def compareExecutionTime(self, algo, fp):
        """
        Compare the execution time of an algorithm on several databases of different sizes
        """
        # iterations = [8, 40, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 500000]
        # rows = ROWS_RATIO  # [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        time_dict = {k: [0 for i in range(len(self.cols))] for k in self.rows}
        self.jsonFilePath += "ExecutionRankSky369.json"
        max_rows = 0
        max_time = 0
        pref = [Preference.MIN, Preference.MIN, Preference.MIN]

        root_databases = fr"..\..\Assets\databases"
        i = -1
        for col in self.cols:
            i += 1
            for row in self.rows:
                # beauty_print("Column", col)
                # beauty_print("Row", rows)
                # Displays the execution time of each algorithm
                database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"  # Retrieve the path
                sel = AlgoCalculator(database_filepath)
                r = DataParser(sel.select_all()).r_dict
                # The name of the algorithm class
                algo_name = algo.__name__
                beauty_print("Algorithm name ", algo_name)
                beauty_print("Database path ", database_filepath)
                time_calc = TimeCalc(row, algo_name)
                # For the SQL algorithm, add the connection object to the arguments
                if algo_name == "CoskySQL":
                    # Need a database path
                    print("zzzzz")
                    algo_obj = algo(database_filepath)

                elif algo_name == "SkyIR":
                    # Needs a data dictionary
                    algo_obj = algo(r).skyIR(10)

                elif algo_name == "CoskyAlgorithme":
                    # Needs a data dictionary
                    algo_obj = algo(r)

                elif algo_name == "RankSky":
                    algo_obj = algo(r,pref)
                # Retrieve the execution time for each database on the given algorithm
                time_calc.stop()
                # Add the execution time to the dictionary
                current_time = time_calc.execution_time

                if algo_name == "RankSky":
                    time_dict[row][i] = algo_obj.time
                if row > max_rows:
                    max_rows = row
                if current_time > max_time:
                    max_time = current_time
                row_str = str(row)
                try:
                    with open(fp, "r") as f:
                        savedDatas = json.load(f)
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
                with open(fp, "w") as f:
                    json.dump(dataToSave, f, indent=4)

                self.sortJson(fp)

    def compareExecutionTimeSqlAlgo(self):
        """
        Compare execution time of CoSky SQL and Algorithm
        """

        timeDictSql = {k: [0 for i in range(len(self.cols))] for k in self.rows}
        timeDictAlgo = {k: [0 for i in range(len(self.cols))] for k in self.rows}
        self.jsonFilePath += "ExecutionCoskySqlAlgo.json"
        maxRows = 0
        maxTime = 0

        rootDatabases = fr"..\Assets\databases"
        i = -1
        for col in self.cols:
            i += 1
            for row in self.rows:
                # Displays the execution time of each algorithm
                database_filepath = fr"{rootDatabases}\cosky_db_C{col}_R{row}.db"
                beauty_print("Database path", database_filepath)
                sel = AlgoCalculator(database_filepath)
                r = DataParser(sel.select_all()).r_dict
                # The name of the algorithm class
                algo_name1 = CoskySql
                algo_name2 = CoskyAlgorithme
                # For the SQL algorithm, add the connection object to the arguments
                timeCalcSql = TimeCalc(row, algo_name1)
                algoObj1 = CoskySQL(database_filepath)
                timeCalcSql.stop()
                timeCalcAlgo = TimeCalc(row, algo_name2)
                algoObj2 = CoskyAlgorithme(r)
                timeCalcAlgo.stop()
                # Retrieve the execution time for each database on the given algorithm
                currentTimeSql = timeCalcSql.execution_time
                currentTimeAlgo = timeCalcAlgo.execution_time
                # Add the execution time to the dictionary
                timeDictSql[row][i] = currentTimeSql
                timeDictAlgo[row][i] = currentTimeAlgo
                if row > maxRows:
                    maxRows = row

                if currentTimeSql > maxTime:
                    maxTime = currentTimeSql

                if currentTimeAlgo > maxTime:
                    maxTime = currentTimeAlgo

        dataToSave = {
            "timeDictSql": timeDictSql,  # The dictionary with execution times for the SQL algorithm
            "timeDictAlgo": timeDictAlgo,  # The dictionary with execution times for the algorithm
            "maxRows": maxRows,  # The maximum number of rows
            "maxTime": maxTime  # The maximum execution time
        }

        with open(self.jsonFilePath, "w") as f:
            # Save everything in the JSON file
            json.dump(dataToSave, f, indent=4)

    def compareExecutionTimeCoskySqlColumn(self, col):
        """
        Compare the execution time of an algorithm on several databases of different sizes with n columns
        :param algo: the algorithm to be compared
        :param col: the number of columns of the databases
        """
        timeDict = {k: [0 for i in [col]] for k in self.rows}
        match col:
            case 3:
                self.jsonFilePath += "ExecutionCoskySql3.json"
            case 6:
                self.jsonFilePath += "ExecutionCoskySql6.json"
            case 9:
                self.jsonFilePath += "ExecutionCoskySql9.json"
        maxRows = 0
        maxTime = 0
        rootDatabases = fr"..\Assets\databases"
        for row in self.rows:
            databaseFilepath =fr"{rootDatabases}\cosky_db_C{col}_R{row}.db"  # Retrieve the path
            beauty_print("Database path", databaseFilepath)
            Timecalc = TimeCalc(row, CoskySql)
            coskySql = CoskySQL(databaseFilepath)
            Timecalc.stop()
            # Retrieve the execution time for each database on the given algorithm
            currentTime = Timecalc.execution_time
            # Add the execution time to the dictionary
            timeDict[row][0] = currentTime
            if row > maxRows:
                maxRows = row

            if currentTime > maxTime:
                maxTime = currentTime

        dataToSave = {
            "timeDict": timeDict,  # The dictionary with execution times
            "maxRows": maxRows,  # The maximum number of rows
            "maxTime": maxTime  # The maximum execution time
        }

        with open(self.jsonFilePath, "w") as f:
            # Save everything in the JSON file
            json.dump(dataToSave, f, indent=4)

# Algorithm declarations
COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
# DP_IDP_ = "DP_IDP"
CONFIG_DATA = "CONFIG_DATA"
RANK_SKY = "RANK_SKY"

# MODES contains all the algorithms to be compared
MODES = {
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    # DP_IDP_: DP_IDP,
    RANK_SKY : RankSky,
}


if __name__ == "__main__":
    # Create an instance of the AlgoCalculator class
    calculator = AlgoCalculator("")
    #calculator.compareExecutionTime(CoskySQL)
    #calculator.compareExecutionTimeSqlAlgo()
    #calculator.compareExecutionTime(CoskyAlgorithme, "../../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskySql369.json")
    calculator.compareExecutionTime(RankSky, "../../Assets/LatexDatas/OneAlgoDatas/ExecutionRankSky369.json")
    calculator.compareExecutionTime(CoskySQL, "../../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskySql369.json")
    calculator.compareExecutionTime(CoskyAlgorithme, "../../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskyAlgo369.json")
    #calculator.compareExecutionTime(CoskySQL, "../../Assets/LatexDatas/OneAlgoDatas/TestExecution.json")