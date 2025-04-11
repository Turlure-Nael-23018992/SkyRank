import sys
import os
import textwrap
import json

# Ajoute le chemin du répertoire parent de Core au chemin de recherche des modules


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

#Importation des librairies
import sqlite3
from colorama import Back, Fore, Style
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
#from Algorithms.DP_IDP import DP_IDP
#from Algorithms.DP_IDP_cpp import DP_IDP
from Algorithms.SkyIR import SkyIR
from Database.DatabaseHelpers import  Database
from Database.SqlDataMocker import SqlDataMocker
from Utils.DataParser import DataParser
from Utils.TimerUtils import TimeCalc
from Utils.DisplayHelpers import beauty_print, print_color
from time import *
from Utils.LatexMaker import LatexMaker

#Déclaration des constantes
ROWS_RATIO_MULT = pow(10, 3)
ROWS_RATIO_UNITS = [1, 2, 5, 10]
ROWS_RATIO = [x * ROWS_RATIO_MULT for x in ROWS_RATIO_UNITS]



class AppRun:
    """
    EntryPoint of the app
    """

    def __init__(self, db_filepath):
        self.table_name = "Pokemon"
        self.db_filepath = db_filepath
        self.conn = sqlite3.connect(db_filepath)
        self.cursor = self.conn.cursor()
        self.ratio_for_count = ROWS_RATIO_MULT
        self.rows_ratios = ROWS_RATIO_UNITS
        self.rows = ROWS_RATIO

    def select_all(self):
        """
        Select tout
        :return: Tous les enregistrements de la table
        """
        sql_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def create_table(self, root_databases, col, row):
        """
        Crée une table dans la base de données
        :param root_databases: Le chemin vers le dossier contenant les bases de données
        :param col: Le nombre de colonnes
        :param row: Le nombre de lignes
        """
        database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row // self.ratio_for_count}M.db"
        sql_mocker = SqlDataMocker(col, row, filepath=database_filepath)
        r_dict = sql_mocker.run()
        database = sql_mocker.database
        print(f"{database_filepath} créé avec {col} colonnes / {row} rows...")

    def create_tables(self):
        """
        Crée les tables dans la base de données
        """
        #Apelle la fonction create_table pour chaque combinaison de colonnes et de lignes
        cols = range(3, 12, 3)
        root_databases = fr"..\Assets\databases"
        for col in cols:
            for row in self.rows:
                self.create_table(root_databases, col, row)

    def mock_data(self):
        """
        Mock des données
        """
        db_filepath = f"../Assets/pokemon.db"
        for col in range(3, 4):
            for row in range(5, 10):
                col_len = col
                row_len = row
                dict_data = SqlDataMocker(col_len, row_len, db_filepath).dict_data
                beauty_print(f"[col]:{col} [row]:{row}", dict_data)
                # sleep(5)
        print("Mock data done")

def data_normalizer(time_dict, max_rows, max_time, scaleX=280, scaleY=280):
    """
    Normalize les données pour le graphique
    :param time_dict: Dictionnaire contenant les temps d'exécution
    :param max_rows: Nombre maximum de lignes
    :param max_time: Temps maximum
    :param scaleX: Échelle pour l'axe X (280)
    :param scaleY: Échelle pour l'axe Y (280)
    """
    colors = [f"gray", "brightmaroon", "cyan", "skyblue"]
    #colors=[Fore.LIGHTBLACK_EX, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.BLUE]
    NL = '\n'
    # calcul des ratios pour les axes du graphique
    ratio_x = scaleX / max_rows
    ratio_y = scaleY / max_time
    dict_ = '\n'.join([f"{k}:{v}" for k, v in time_dict.items()])
    '''
    print(f"""
        time_dict:{dict_}
        max_rows:{max_rows} 
        max_time:{max_time}
        ratio_x:{ratio_x}
        ratio_y:{ratio_y}""")'''
    mini_ = min(time_dict.keys()) # minimum colonne bd
    mini_key = time_dict[mini_] # Tableau des valeurs pour la colonne mini_
    len_dict_val = len(mini_key) # Nombre BD testée
    '''
    beauty_print("time_dict", time_dict)
    beauty_print("mini_", mini_)
    beauty_print("mini_key", mini_key)
    beauty_print("len_dict_val", len_dict_val)
    '''



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
    #print()
    #print("% Filldraws")
    #print(line2)


def compare_all():
    """
    Compare le temps d'éxécution de tous les algos
    """
    db_filepath = f"../Assets/pokemon.db"
    log_filepath = fr"..\Assets\log.txt"
    algo_types = [CoskySQL] #SkyIR, CoskyAlgorithme,
    #iterations =[8, 40, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 500000]
    rows = ROWS_RATIO  #[10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
    col_count = 3
    cols = [3, 6, 9]
    rows = [100, 1000]
    time_dict = {k: [0, 0, 0, 0] for k in rows}
    #beauty_print("time_dict", time_dict)

    max_rows = 0
    max_time = 0

    root_databases = fr"..\Assets\databases"
    for col in cols:
        for row in rows:
            #beauty_print("Colonne", col)
            #beauty_print("Ligne", rows)
            #Permets d'afficher le temps d'éxécution de chaque algo
            database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db" # Récupération du chemin
            iteration_logs = []
            #print(f"[{row}] iterations...")
            beauty_print("Chemin de la base de données", database_filepath)
            app_run = (AppRun("../Assets/Databases/cosky_db_C3_R10.db"))
            #print(app_run.select_all())  # Sélectionne toutes les données de la table
            r = DataParser(app_run.select_all()).r_dict  # Transformation des données en dictionnaire
            #On a transformé les données en dictionnaire Pour les algos qui en ont besoin
            
            # Pour tous les types d'algos
            for idx, algo_type in enumerate(algo_types):
                # Le nom de la classe de l'algo
                algo_name = algo_type.__name__
                #print(f"\tALGO [{algo_name}]")

                time_calc = TimeCalc(row, algo_name)
                # Pour l'algo SQL on lui rajoute l'objet connection dans les arguments

                if algo_name == "CoskySQL":
                    # a besoin d'un chemin
                    algo_obj = algo_type(database_filepath)


                elif algo_name == "SkyIR":
                    # a besoin d'un dictionnaire de données
                    algo_obj = algo_type(r).skyIR(10)


                elif algo_name == "CoskyAlgorithme":
                    # a besoin d'un dictionnaire de données
                    algo_obj = algo_type(r)

                time_calc.stop()  # Arrête le timer
                iteration_logs.append(time_calc)  # Ajoute le temps d'éxécution à la liste
                current_time = time_calc.execution_time
                time_dict[row][idx] = current_time  # Ajoute le temps d'éxécution au dictionnaire

                if row > max_rows:
                    max_rows = row

                if current_time > max_time:
                    max_time = current_time

            # Affichage du temps d'éxécution de chaque algo
            min_for_sample = min([x.ratio for x in iteration_logs])
            for x in iteration_logs:
                if x.ratio == min_for_sample:
                    print(x.get_formated_data(), file=open(log_filepath, 'a'))
                else:
                    print(x.get_formated_data(), file=open(log_filepath, 'a'))

                #print(x.get_formated_data())
    '''
    beauty_print("time_dict2", time_dict2)
    beauty_print("time_dict", time_dict)
    beauty_print("max_rows", max_rows)
    beauty_print("max_time", max_time)
    '''
    latexMaker = LatexMaker()
    latexMaker.coskyComparaisonLatex(time_dict, max_rows, max_time)
    #data_normalizer(time_dict, max_rows, max_time)

def compareExecutionTime(algo):
    """
    Compare le temps d'éxécution d'un algo sur plusieurs bases de données de tailles différentes
    """
    db_filepath = f"../Assets/pokemon.db"
    log_filepath = fr"..\Assets\log.txt"
    algo_types = [CoskySQL]  # SkyIR, CoskyAlgorithme,
    # iterations =[8, 40, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 500000]
    rows = ROWS_RATIO  # [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
    col_count = 3
    cols = [3, 6, 9]
    rows = [10, 100, 1000]
    time_dict = {k: [0 for i in range(len(cols))] for k in rows}
    beauty_print("time_dict", time_dict)

    max_rows = 0
    max_time = 0

    root_databases = fr"..\Assets\databases"
    i= -1
    for col in cols:
        i+=1
        for row in rows:
            # beauty_print("Colonne", col)
            # beauty_print("Ligne", rows)
            # Permets d'afficher le temps d'éxécution de chaque algo
            database_filepath = fr"{root_databases}\cosky_db_C{col}_R{row}.db"  # Récupération du chemin
            iteration_logs = []
            # print(f"[{row}] iterations...")
            beauty_print("Chemin de la base de données", database_filepath)
            app_run = (AppRun(database_filepath))
            # print(app_run.select_all())  # Sélectionne toutes les données de la table
            r = DataParser(app_run.select_all()).r_dict  # Transformation des données en dictionnaire
            # On a transformé les données en dictionnaire Pour les algos qui en ont besoin

            # Pour l'algo donnée mettre dans le dictionnaire le temps d'éxécution

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
            #mettre dans le dictionnaire le temps d'éxécution
            current_time = time_calc.execution_time
            time_dict[row][i] = current_time

            if row > max_rows:
                max_rows = row

            if current_time > max_time:
                max_time = current_time

            #beauty_print("time_dict", time_dict)
    with open("../Assets/LatexDatas/ExecutionCoskyDatas.json", "w") as f:
        json.dump(time_dict, f, indent=4)

    latexMaker = LatexMaker()
    latexMaker.coskyComparaisonLatex(time_dict, max_rows, max_time)


# Déclaration des algos
COMPARE_ALL = "COMPARE_ALL"
COSKY_ALGO_ = "COSKY_ALGO"
COSKY_SQL_ = "COSKY_SQL"
#DP_IDP_ = "DP_IDP"
CONFIG_DATA = "CONFIG_DATA"

# MODES Contient tous les algos dont on veut faire la comparaison
MODES = {
    COMPARE_ALL: compare_all,
    COSKY_ALGO_: CoskyAlgorithme,
    COSKY_SQL_: CoskySQL,
    #DP_IDP_: DP_IDP,
    CONFIG_DATA: SqlDataMocker
}

# Comparateur

# Time calc

# print

# Single algos

# Config

# choice row and columns


if __name__ == '__main__':
    App = AppRun("")
    compareExecutionTime(CoskySQL)

    quit()
