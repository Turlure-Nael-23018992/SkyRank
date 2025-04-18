import random
import sqlite3, math
import string
import time

class CoskySQL:
    """
    Class to implement the Cosky algorithm for ranking and sorting data based on multiple criteria using SQLite.
    """
    def __init__(self, db_filepath,is_debug=False):
        """
        Initialize the Cosky algorithm with the given database file path and debug flag.
        :param db_filepath: the path to the SQLite database file
        :param is_debug: flag to enable debug mode
        """
        self.is_debug=is_debug
        self.relations = []
        self.conn=sqlite3.connect(db_filepath)
        self.conn.create_function('sqrt', 1, math.sqrt)
        self.cursor =self.conn.cursor()
        self.table_name="Pokemon"
        self.colonnes_initiales_str = []
        try:
            self.colonne_len=self.nombre_colonnes_table()
        except Exception as e:
            print(e)
            self.colonne_len = 9
        self.colonne_names = self.get_column_names(self.table_name)

        self.run()

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


        sql_queries = f"""
           WITH S AS (SELECT * FROM {self.table_name} AS R1
            WHERE NOT EXISTS (SELECT * FROM {self.table_name} AS R2 WHERE ({s1}) AND ({s2}))),
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

        cursor.execute(sql_queries)
        # Récupération des résultats de la dernière instruction
        results = cursor.fetchall()
        self.rows_res = []

        # Affichage des résultats
        self.rows_res = [row for row in results]

        return self.rows_res

if __name__ == '__main__':
    #print("Sqlite version : ", sqlite3.sqlite_version)
    db_filepath= "../Assets/CoskySqlTest.db"
    #startTime = time.time()
    cosky_sql = CoskySQL(db_filepath)
    #print("cosky_sql:",cosky_sql.rows_res)
    #print(f"temps: {time.time() - startTime}")