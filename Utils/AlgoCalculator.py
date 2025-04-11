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

    def __init__(self):
        self.latexMaker = LatexMaker()
        self.jsonFilePath = "../Assets/LatexDatas/"
        self.tableName = "Pokemon"
        self.conn = sqlite3.connect(fr"..\Assets\databases\{self.tableName}.db")


    def compareExecutionTime(self, algo):
        """
        Compare le temps d'éxécution d'un algo sur plusieurs bases de données de tailles différentes
        """
        # iterations =[8, 40, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 500000]
        #rows = ROWS_RATIO  # [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        cols = [3, 6, 9]
        rows = [10, 100, 1000, 10000, 100000]
        time_dict = {k: [0 for i in range(len(cols))] for k in rows}
        beauty_print("time_dict", time_dict)
        self.jsonFilePath += "ExecutionCoskyDatas.json"
        beauty_print("jsonFilePath", self.jsonFilePath)
        max_rows = 0
        max_time = 0

        root_databases = fr"..\Assets\databases"
        i = -1
        for col in cols:
            i += 1
            for row in rows:
                # beauty_print("Colonne", col)
                # beauty_print("Ligne", rows)
                # Permets d'afficher le temps d'éxécution de chaque algo
                database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"  # Récupération du chemin
                # print(f"[{row}] iterations...")
                beauty_print("Chemin de la base de données", database_filepath)
                db = Database(database_filepath)
                r = DataParser(db.select_all()).r_dict
                # Le nom de la classe de l'algo
                algo_name = algo.__name__
                print(f"\tALGO [{algo_name}]")
                time_calc = TimeCalc(row, algo_name)
                # Pour l'algo SQL on lui rajoute l'objet connection dans les arguments
                if algo_name == "CoskySQL":
                    # a besoin d'un chemin
                    algo_obj = algo(database_filepath)

                elif algo_name == "SkyIR":
                    # a besoin d'un dictionnaire de données
                    algo_obj = algo(r).skyIR(10)

                elif algo_name == "CoskyAlgorithme":
                    # a besoin d'un dictionnaire de données
                    algo_obj = algo(r)
                # Récupérer le temps d'éxécution pour chaque bd sur l'algo donné
                time_calc.stop()
                # mettre dans le dictionnaire le temps d'éxécution
                current_time = time_calc.execution_time
                time_dict[row][i] = current_time

                if row > max_rows:
                    max_rows = row

                if current_time > max_time:
                    max_time = current_time

                # beauty_print("time_dict", time_dict)
        dataToSave = {
            "time_data": time_dict,  # Le dictionnaire avec les temps
            "max_rows": max_rows,  # Le nombre maximum de lignes
            "max_time": max_time  # Le temps d'exécution maximum
        }

        with open("../Assets/LatexDatas/ExecutionCoskyDatas.json", "w") as f:
            # Sauvegarder tout dans le fichier JSON
            json.dump(dataToSave, f, indent=4)

    def compareExecutionTimeSqlAlgo(self):
        """
        Compare execution time of CoSky SQL and Algo
        """


# Déclaration des algos
COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
#DP_IDP_ = "DP_IDP"
CONFIG_DATA = "CONFIG_DATA"

# MODES Contient tous les algos dont on veut faire la comparaison
MODES = {
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    #DP_IDP_: DP_IDP,
}



if __name__ == "__main__":
    # Créer une instance de la classe AlgoCalculator
    calculator = AlgoCalculator()
    calculator.compareExecutionTime(CoskySQL)


