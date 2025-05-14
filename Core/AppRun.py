import sys
import os

# Ajoute le chemin du répertoire parent de Core au chemin de recherche des modules


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

#Importation des librairies
import sqlite3
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
#from Algorithms.DP_IDP import DP_IDP
#from Algorithms.DP_IDP_cpp import DP_IDP
from Database.SqlDataMocker import SqlDataMocker
from Utils.DataParser import DataParser
from Utils.TimerUtils import TimeCalc
from Utils.DisplayHelpers import beauty_print

#Déclaration des constantes
ROWS_RATIO_MULT = pow(10, 3)
ROWS_RATIO_UNITS = [1, 2, 5, 10]
ROWS_RATIO = [x * ROWS_RATIO_MULT for x in ROWS_RATIO_UNITS]



class AppRun:
    """
    Entry point of the application for interacting with the SQLite database
    and managing table creation and data retrieval.
    """

    def __init__(self, db_filepath):
        """
        Initialize AppRun with the given database filepath.

        :param db_filepath: Path to the SQLite database file
        """
        self.table_name = "Pokemon"
        self.db_filepath = db_filepath
        self.conn = sqlite3.connect(db_filepath)
        self.cursor = self.conn.cursor()
        self.ratio_for_count = ROWS_RATIO_MULT
        self.rows_ratios = ROWS_RATIO_UNITS
        self.rows = ROWS_RATIO

    def select_all(self):
        """
        Select all rows from the table.

        :return: All records from the table
        """
        sql_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def create_table(self, root_databases, col, row):
        """
        Create a new database file and generate a table with mock data.

        :param root_databases: Root folder for database generation
        :param col: Number of columns
        :param row: Number of rows
        """
        database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row // self.ratio_for_count}M.db"
        sql_mocker = SqlDataMocker(col, row, filepath=database_filepath)
        r_dict = sql_mocker.run()
        database = sql_mocker.database
        print(f"{database_filepath} created with {col} columns / {row} rows...")

    def create_tables(self):
        """
        Create multiple tables using predefined column and row configurations.
        """
        cols = range(3, 12, 3)
        root_databases = fr"..\Assets\databases"
        for col in cols:
            for row in self.rows:
                self.create_table(root_databases, col, row)

    def mock_data(self):
        """
        Generate mock data and display results for different configurations.
        """
        db_filepath = f"../Assets/pokemon.db"
        for col in range(3, 4):
            for row in range(5, 10):
                col_len = col
                row_len = row
                dict_data = SqlDataMocker(col_len, row_len, db_filepath).dict_data
                beauty_print(f"[col]:{col} [row]:{row}", dict_data)
        print("Mock data done")

def data_normalizer(time_dict, max_rows, max_time, scaleX=280, scaleY=280):
    """
    Normalize execution time data for graph plotting.

    :param time_dict: Dictionary with execution time per row count
    :param max_rows: Maximum number of rows
    :param max_time: Maximum execution time
    :param scaleX: X-axis scaling factor (default: 280)
    :param scaleY: Y-axis scaling factor (default: 280)
    """
    colors = [f"gray", "brightmaroon", "cyan", "skyblue"]
    NL = '\n'
    ratio_x = scaleX / max_rows
    ratio_y = scaleY / max_time
    dict_ = '\n'.join([f"{k}:{v}" for k, v in time_dict.items()])
    mini_ = min(time_dict.keys())
    mini_key = time_dict[mini_]
    len_dict_val = len(mini_key)

    line2 = ""
    print("% Lines")
    for alg_idx in range(len_dict_val):
        line1_header = f"\\draw[{colors[alg_idx]}, line width=2pt]"
        line1 = ""
        for k in time_dict.keys():
            x = int(round(k * ratio_x))
            y = int(round(time_dict[k][alg_idx] * ratio_y))
            line1 += f"({x}pt, {y}pt) -- "
            line2 += fr"\filldraw[color=black, fill={colors[alg_idx]}] ({x}pt, {y}pt) circle (2pt);{NL}"
        line1_full = line1_header + line1 + ";"
        line1_full = line1_full.replace(" -- ;", ";")
        print(line1_full)

def compare_all():
    """
    Compare execution time of all algorithms over different database configurations.
    """
    db_filepath = f"../Assets/pokemon.db"
    log_filepath = fr"..\Assets\log.txt"
    algo_types = [CoskySQL]
    rows = [100, 1000]
    col_count = 3
    cols = [3, 6, 9]
    time_dict = {k: [0, 0, 0, 0] for k in rows}
    max_rows = 0
    max_time = 0

    root_databases = fr"..\Assets\databasesGenerated"
    for col in cols:
        for row in rows:
            database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"
            iteration_logs = []
            beauty_print("Chemin de la base de données", database_filepath)
            app_run = (AppRun("../Assets/Databases/cosky_db_C3_R10.db"))
            r = DataParser(app_run.select_all()).r_dict

            for idx, algo_type in enumerate(algo_types):
                algo_name = algo_type.__name__
                time_calc = TimeCalc(row, algo_name)

                if algo_name == "CoskySQL":
                    algo_obj = algo_type(database_filepath)

                elif algo_name == "SkyIR":
                    algo_obj = algo_type(r).skyIR(10)

                elif algo_name == "CoskyAlgorithme":
                    algo_obj = algo_type(r)

                time_calc.stop()
                iteration_logs.append(time_calc)
                current_time = time_calc.execution_time
                time_dict[row][idx] = current_time

                if row > max_rows:
                    max_rows = row
                if current_time > max_time:
                    max_time = current_time

            min_for_sample = min([x.ratio for x in iteration_logs])
            for x in iteration_logs:
                print(x.get_formated_data(), file=open(log_filepath, 'a'))

    '''
    beauty_print("time_dict2", time_dict2)
    beauty_print("time_dict", time_dict)
    beauty_print("max_rows", max_rows)
    beauty_print("max_time", max_time)
    '''
    #data_normalizer(time_dict, max_rows, max_time)




COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
#DP_IDP_ = "DP_IDP"
CONFIG_DATA = "CONFIG_DATA"

MODES = {
    COMPARE_ALL: compare_all,
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    #DP_IDP_: DP_IDP,
    CONFIG_DATA: SqlDataMocker
}


if __name__ == '__main__':
    """App = AppRun("")
    quit()"""
