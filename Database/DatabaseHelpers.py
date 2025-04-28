import random
import sqlite3, math
import string

from Utils.DataParser import DataParser
from Utils.DisplayHelpers import beauty_print


class Database:
    """
    Class to manage the database
    """

    def __init__(self, db_filepath, col_len=9, row_len=0, is_debug=True):
        self.is_debug = is_debug
        self.relations = []
        self.conn = sqlite3.connect(db_filepath)
        self.conn.create_function('sqrt', 1, math.sqrt)
        self.cursor = self.conn.cursor()
        self.table_name = "Pokemon"
        self.colonnes_initiales_str = []
        self.create_table_query_str = self.generer_table(col_len)
        self.create_table(self.create_table_query_str)
        try:
            self.colonne_len = self.nombre_colonnes_table()
        except Exception as e:
            print(e)
            self.colonne_len = 9
        self.colonne_names = self.get_column_names(self.table_name)
        if self.colonne_len > 1:
            if row_len > 0:
                self.insert_random_tuples(row_len)

    def get_column_names(self, nom_table):
        """
        Get the column's name
        :param nom_table: the table name
        :return: The column's name in a list
        """
        try:
            # Get the column names of the table
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            info_colonnes = self.cursor.fetchall()
            noms_colonnes = [colonne[1] for colonne in info_colonnes]
            # Return column names
            return noms_colonnes
        except sqlite3.Error as e:
            print("Error while retrieving column names of the table:", e)
            return None

    def nombre_colonnes_table(self, nom_table=None):
        """
        Get the number of columns
        :param nom_table: table name
        :return: the number of columns
        """
        if nom_table == None:
            nom_table = self.table_name
        try:
            # Get information about the table
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            self.colonnes = self.cursor.fetchall()
            # Get the number of columns (count)
            return len(self.colonnes)
        except sqlite3.Error as e:
            print("Error while retrieving information about the table:", e)
            return None

    def create_table(self, sql_query=None):
        """
        Create the table
        :param sql_query: the query, otherwise a basic schema is auto-provided
        :return: Boolean indicating creation status
        """
        if sql_query == None:
            sql_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            RowId INTEGER PRIMARY KEY,
            Rarete REAL,
            Duree REAL,
            Victoire REAL);
            """
        try:
            # Drop the table if it exists
            self.conn.execute(f"DROP TABLE IF EXISTS {self.table_name};")
            self.conn.commit()
            # Create the table
            self.conn.execute(sql_query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def select_by_id(self, row_id):
        """
        Select an entry by id
        :param row_id: The id of the entry
        :return: The entry
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId = ?"
        self.cursor.execute(sql_query, (row_id,))
        return self.cursor.fetchall()

    def select_all_for_check_max(self):
        """
        Check if the random generation rules have been respected
        :return: All records that do not respect the rules (an empty list if all are valid)
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete > 10 or Duree < 2 or Duree > 132 or Victoire > 100"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_all_until_id(self, until_id):
        """
        Select entries up to a specific id
        :param until_id: The maximum id
        :return: The records up to the desired id
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId <= ?"
        self.cursor.execute(sql_query, (until_id,))
        self.data = [x for x in self.cursor.fetchall()]
        return

    def select_all(self):
        """
        Select all records
        :return: All records in the table
        """
        sql_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_by_rarete(self, rarete):
        """
        Select by rarity
        :param rarete: The exact rarity
        :return: The records matching this rarity
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete = ?"
        self.cursor.execute(sql_query, (rarete,))
        return self.cursor.fetchall()

    def select_by_duree(self, duree):
        """
        Select by duration
        :param duree: The exact duration
        :return: The records matching this duration
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Duree = ?"
        self.cursor.execute(sql_query, (duree,))
        return self.cursor.fetchall()

    def select_by_victoire(self, victoire):
        """
        Select by victory
        :param victoire: The exact victory value
        :return: The records matching this victory value
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Victoire = ?"
        self.cursor.execute(sql_query, (victoire,))
        return self.cursor.fetchall()

    def generer_table(self, n_rnd_cols):
        """
        Generate the table with a specified number of random columns
        :param n_rnd_cols: The number of random columns to generate
        :return: The SQL query to create the table
        """
        # Fixed columns
        colonnes_fixes_str = ", ".join([f"{colonne} REAL" for colonne in self.colonnes_initiales_str])

        alphaUpper = string.ascii_uppercase
        alpha_len = len(alphaUpper)
        _2_chars_len = alpha_len**2
        _3_chars_len = alpha_len**3
        _4_chars_len = alpha_len**4
        # Random columns

        if n_rnd_cols <= alpha_len:
            col_suffixes = [alphaUpper[i] for i in range(n_rnd_cols)]

        elif n_rnd_cols <= _2_chars_len:
            col_suffixes = [f"{alphaUpper[i // alpha_len]}{alphaUpper[i % alpha_len]}" for i in range(n_rnd_cols)]

        elif n_rnd_cols <= _3_chars_len:
            col_suffixes = [f"{alphaUpper[i // (_2_chars_len)]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}" for i in range(n_rnd_cols)]

        elif n_rnd_cols <= _4_chars_len:
            col_suffixes = [
                f"{alphaUpper[i // (_3_chars_len)]}{alphaUpper[(i // (_2_chars_len)) % alpha_len]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}"
                for i in range(n_rnd_cols)]

        else:
            col_suffixes = [
                f"{alphaUpper[i // (alpha_len ** 4)]}{alphaUpper[(i // (alpha_len ** 3)) % alpha_len]}{alphaUpper[(i // (alpha_len ** 2)) % alpha_len]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}"
                for i in range(n_rnd_cols)]

        colonnes_aleatoires = [f"Col_{col_suffixes[i]}" for i in range(n_rnd_cols)]
        colonnes_aleatoires_str = ", ".join([f"{colonne} REAL" for colonne in colonnes_aleatoires])

        # Generate the CREATE TABLE query
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (RowId INTEGER PRIMARY KEY, {colonnes_aleatoires_str});"
        return query

    def generate_random_tuples(self, n):
        """
        Generate random tuples
        :param n: The number of tuples to generate
        :return: The tuples
        """
        random_tuples = []
        for _ in range(n):
            rarete = random.randint(0, 10)
            duree = random.randint(2, 132)
            victoire = random.randint(0, 100)
            random_tuples.append((rarete, duree, victoire))
        return random_tuples

    def generate_random_tuples_for_all_columns(self, n):
        """
        Generate random tuples for all columns
        :param n: The number of tuples to generate
        :return: The tuples
        """
        random_tuples = []
        for _ in range(n):
            col_tuple = []
            for col in range(self.colonne_len - 1):
                if col % 4 == 0:
                    rand_func = random.uniform
                else:
                    rand_func = random.randint
                categories_min = [1, 10, 100]
                coeff_categories_max = [5, 10, 50, 100]

                max_of_min_idx = random.choice(range(len(categories_min)))
                raw_mini = rand_func(0, categories_min[max_of_min_idx])
                mini = raw_mini - (raw_mini % categories_min[max(0, max_of_min_idx - 1)])
                mini = max(1, mini)
                max_of_max_idx = random.choice(range(1, len(coeff_categories_max)))
                max_of_max = categories_min[max_of_min_idx] * coeff_categories_max[max_of_max_idx]

                raw_maxi = rand_func(mini + coeff_categories_max[max(0, max_of_max_idx - 1)], max_of_max)
                maxi = raw_maxi - (raw_maxi % coeff_categories_max[max(0, max_of_max_idx - 1)])  #
                maxi = max(1, maxi)
                current_col = rand_func(mini, maxi)
                col_tuple.append(current_col)
            random_tuples.append(col_tuple)
        return random_tuples

    def insert_random_tuples(self, n):
        """
        Wrapper method that generates tuples and inserts them into the database
        :param n: The number of tuples to generate
        :return: Boolean
        """
        try:
            query = f"INSERT OR IGNORE INTO {self.table_name} ({','.join([x for x in self.colonne_names[1:]])}) VALUES ({','.join(['?' for _ in range(self.colonne_len - 1)])})"
            randomized_queries = self.generate_random_tuples_for_all_columns(n)
            self.cursor.executemany(query, randomized_queries)
            self.conn.commit()
            return True
        except Exception as e:
            print("212:", e)
            return False