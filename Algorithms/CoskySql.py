import random
import sqlite3, math
import string
import time
import os
import sys

from Utils.DataModifier.DataUnifier import DataUnifier
from Utils.Preference import Preference

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import AnyStr

from Utils.TimerUtils import TimeCalc

def safe_sqrt(x):
    try:
        return math.sqrt(float(x)) if x is not None and float(x) >= 0 else 0.0
    except:
        return 0.0

class CoskySQL:
    """
    Class to implement the Cosky algorithm for ranking and sorting data based on multiple criteria using SQLite.
    """
    def __init__(self, db_filepath, preferences, is_debug=False):
        """
        Initialize the Cosky algorithm with the given database file path and debug flag.
        :param db_filepath: the path to the SQLite database file
        :param is_debug: flag to enable debug mode
        """
        self.pref = preferences
        self.dbFilepath = db_filepath
        time = TimeCalc(100, "CoskySQL")
        self.is_debug=is_debug
        self.relations = []
        self.conn=sqlite3.connect(db_filepath)
        self.conn.create_function('sqrt', 1, safe_sqrt)
        self.cursor =self.conn.cursor()
        self.table_name="Pokemon"
        self.colonnes_initiales_str = []
        self.dict = {}
        try:
            self.colonne_len=self.nombre_colonnes_table()
        except Exception as e:
            print(e)
            self.colonne_len = 9
        self.colonne_names = self.get_column_names(self.table_name)
        self.run()
        time.stop()
        self.time = time.execution_time

    def get_column_names(self, nom_table):
        """
        Get the column's names of the table
        :param nom_table: the table name
        :return: The column's names in a list
        """
        try:
            # Get the column's names of the table
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            info_colonnes = self.cursor.fetchall()
            noms_colonnes = [colonne[1] for colonne in info_colonnes]
            # Return column's names
            return noms_colonnes
        except sqlite3.Error as e:
            print("Erreur lors de la récupération des noms des colonnes de la table :", e)
            return None


    def nombre_colonnes_table(self, nom_table=None):
        """
        Get the columns length
        :param nom_table: Le name of the table
        :return: Le number of column into the table (int)
        """
        if nom_table is None:
            nom_table=self.table_name
        try:
            # Get information about the table
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            self.colonnes = self.cursor.fetchall()
            # Get the columns length (count)
            return len(self.colonnes)
        except sqlite3.Error as e:
            print("Error while recovering informations about table :", e)
            return None



    def run(self):
        """
        Run the Cosky algorithm to compute the ranking and sorting of data based on multiple criteria.
        :return: The result of the Cosky algorithm
        """
        cursor = self.conn.cursor()
        #self.colonne_len=self.nombre_colonnes_table("Pokemon")

        col_offset = self.colonne_names[1:]
        #print(col_offset)
        # "<=" de S. (skyline)
        s1 = " AND ".join([f"R2.{name} <= R1.{name}" for name in col_offset])

        # "<" de S.
        s2 = " OR ".join([f"R2.{name} < R1.{name}" for name in col_offset])

        # N de SN.
        snn = ", ".join([f"CAST({name} AS REAL) / T{name} AS N{name}" for name in col_offset])

        # T de SN.
        snt = ", ".join([f"SUM({name}) AS T{name}" for name in col_offset])

        # SGini
        sgini = ", ".join([f"1 - (SUM(N{name} * N{name})) AS Gini{name}" for name in col_offset])

        # Somme des Gini.
        giniTot = " + ".join(["Gini" + name for name in col_offset])

        # SW.
        sw = ", ".join([f"Gini{name} / ({giniTot}) AS W{name}" for name in col_offset])

        # SP.
        sp = ", ".join([f"W{name} * N{name} AS P{name}" for name in col_offset])

        # Ideal.
        ideal = ", ".join([f"MIN(P{name}) AS I{name}" for name in col_offset])

        # score numerator.
        scoreNum = " + ".join([f"I{name} * P{name}" for name in col_offset])

        # P².
        pp = " + ".join([f"P{name} * P{name}" for name in col_offset])

        # I².
        ii = " + ".join([f"I{name} * I{name}" for name in col_offset])

        # Projection finale.
        proj = ", ".join(col_offset)

        self.unifyPreferences()
        q1= self.unifyPreferencesQuery()

        sql_queries = f"""
           WITH {q1},
            S AS (SELECT * FROM {"T"} AS R1
            WHERE NOT EXISTS (SELECT * FROM {"T"} AS R2 WHERE ({s1}) AND ({s2}))),
            SN AS (SELECT RowId, {snn} FROM S, (SELECT {snt} FROM S) AS ST),
            SGini AS (SELECT {sgini} FROM SN),
            SW AS (SELECT {sw} FROM SGini),
            SP AS (SELECT RowId, {sp} FROM SN, SW),
            Ideal AS (SELECT {ideal} FROM SP),
            SScore AS (SELECT RowId, ({scoreNum}) / (SQRT({pp}) * SQRT({ii})) AS Score FROM Ideal, SP)
            SELECT {self.table_name}.RowId, {proj}, Score AS Score
            FROM {self.table_name} INNER JOIN SScore rs ON {self.table_name}.RowId = rs.RowId
            ORDER BY Score DESC;
            """

        #print(sql_queries)
        """open = 0
        close = 0
        for i in range(len(sql_queries)):
            if sql_queries[i] == "(":
                open += 1
            elif sql_queries[i] == ")":
                close += 1

        if open != close:
            print("Erreur dans la requête SQL : nombre de parenthèses non équilibré.")
            return None"""

        cursor.execute(sql_queries)

        results = cursor.fetchall()
        if len(results) == 1:
            row = results[0]
            #print("Un seul point Skyline trouvé – attribution automatique du score 1.0")
            row_with_score = row + (1.0,)
            self.rows_res = [row_with_score]
            self.dict = {row_with_score[0]: row_with_score[1:]}
            #print(self.rows_res)
            #print(self.dict)

            return self.rows_res

        # Récupération des résultats de la dernière instruction

        self.rows_res = [row for row in results]
        dict = {}
        for row in results:
            dict[row[0]] = row[1:]
        self.dict = dict
        #print(dict)
        #print(self.executionTime)
        print("rows_res", self.rows_res)
        return self.rows_res

    def unifyPreferences(self):
        dataUnifier = DataUnifier(self.dbFilepath, self.pref)
        self.prefNext = dataUnifier.unifyPreferences()

    def unifyPreferencesQuery(self):
        querry = f"""T AS {"("}
        SELECT RowId, """
        col_offset = self.get_column_names(self.table_name)[1:]
        if len(col_offset) != len(self.pref):
            print("Erreur : le nombre de colonnes ne correspond pas au nombre de préférences.")
            return None
        for i in range(len(col_offset)):
            if self.pref[i] != self.prefNext[i]:
                querry += f""" {1.0} / {col_offset[i]} AS {col_offset[i]},"""
            else :
                querry += f""" {col_offset[i]},"""

        query1 = querry[:-1] + f"""
        FROM {self.table_name}
        )"""
        return query1



if __name__ == '__main__':
    #print("Sqlite version : ", sqlite3.sqlite_version)
    db_filepath= "../Assets/DeepSkyTest.db"
    #startTime = time.time()
    CoskySQL(db_filepath, [Preference.MIN, Preference.MAX, Preference.MIN])



    #print("cosky_sql:",cosky_sql.rows_res)
    #print(f"temps: {time.time() - startTime}")

