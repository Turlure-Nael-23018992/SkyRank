from collections import OrderedDict
import random
import sqlite3, math
import string

class Database:
    """
    Class to manage an SQLite database: creation, insertion, selection and random data generation.
    """

    def __init__(self, db_filepath, col_len=9, row_len=0, is_debug=True):
        """
        Initialize the database connection and create a table if needed.

        :param db_filepath: Path to the SQLite database file.
        :param col_len: Number of columns for the table (default 9).
        :param row_len: Number of random rows to insert (optional).
        :param is_debug: Enable or disable debug mode.
        """
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
        if self.colonne_len > 1 and row_len > 0:
            self.insert_random_tuples(row_len)

    def get_column_names(self, nom_table):
        """
        Retrieve the column names from the table.

        :param nom_table: Name of the table.
        :return: List of column names.
        """
        try:
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            info_colonnes = self.cursor.fetchall()
            return [colonne[1] for colonne in info_colonnes]
        except sqlite3.Error as e:
            print("Error while retrieving column names:", e)
            return None

    def nombre_colonnes_table(self, nom_table=None):
        """
        Get the number of columns in the table.

        :param nom_table: Table name (optional).
        :return: Number of columns.
        """
        if nom_table is None:
            nom_table = self.table_name
        try:
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            self.colonnes = self.cursor.fetchall()
            return len(self.colonnes)
        except sqlite3.Error as e:
            print("Error while retrieving table information:", e)
            return None

    def create_table(self, sql_query=None):
        """
        Create the table from the provided SQL query.

        :param sql_query: SQL query to create the table.
        :return: Boolean indicating success or failure.
        """
        if sql_query is None:
            sql_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            RowId INTEGER PRIMARY KEY,
            Rarete REAL,
            Duree REAL,
            Victoire REAL);
            """
        try:
            self.conn.execute(f"DROP TABLE IF EXISTS {self.table_name};")
            self.conn.execute(sql_query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def select_by_id(self, row_id):
        """
        Select a record by its RowId.

        :param row_id: RowId to search.
        :return: Selected record(s).
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId = ?"
        self.cursor.execute(sql_query, (row_id,))
        return self.cursor.fetchall()

    def select_all_for_check_max(self):
        """
        Select all entries that do not respect predefined rules.

        :return: List of invalid records.
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete > 10 or Duree < 2 or Duree > 132 or Victoire > 100"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_all_until_id(self, until_id):
        """
        Select records until a specific RowId.

        :param until_id: The maximum RowId.
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId <= ?"
        self.cursor.execute(sql_query, (until_id,))
        self.data = [x for x in self.cursor.fetchall()]
        return

    def select_all(self):
        """
        Select all rows in the table.

        :return: All records.
        """
        sql_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_by_rarete(self, rarete):
        """
        Select rows by rarity.

        :param rarete: Rarity value.
        :return: Records matching rarity.
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete = ?"
        self.cursor.execute(sql_query, (rarete,))
        return self.cursor.fetchall()

    def select_by_duree(self, duree):
        """
        Select rows by duration.

        :param duree: Duration value.
        :return: Records matching duration.
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Duree = ?"
        self.cursor.execute(sql_query, (duree,))
        return self.cursor.fetchall()

    def select_by_victoire(self, victoire):
        """
        Select rows by victory.

        :param victoire: Victory value.
        :return: Records matching victory.
        """
        sql_query = f"SELECT * FROM {self.table_name} WHERE Victoire = ?"
        self.cursor.execute(sql_query, (victoire,))
        return self.cursor.fetchall()

    def generer_table(self, n_rnd_cols):
        """
        Generate a SQL query to create a table with a given number of random columns.

        :param n_rnd_cols: Number of columns to create.
        :return: SQL CREATE TABLE query.
        """
        alphaUpper = string.ascii_uppercase
        alpha_len = len(alphaUpper)
        _2_chars_len = alpha_len**2
        _3_chars_len = alpha_len**3
        _4_chars_len = alpha_len**4

        if n_rnd_cols <= alpha_len:
            col_suffixes = [alphaUpper[i] for i in range(n_rnd_cols)]
        elif n_rnd_cols <= _2_chars_len:
            col_suffixes = [f"{alphaUpper[i // alpha_len]}{alphaUpper[i % alpha_len]}" for i in range(n_rnd_cols)]
        elif n_rnd_cols <= _3_chars_len:
            col_suffixes = [f"{alphaUpper[i // _2_chars_len]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}" for i in range(n_rnd_cols)]
        elif n_rnd_cols <= _4_chars_len:
            col_suffixes = [
                f"{alphaUpper[i // _3_chars_len]}{alphaUpper[(i // _2_chars_len) % alpha_len]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}"
                for i in range(n_rnd_cols)]
        else:
            col_suffixes = [
                f"{alphaUpper[i // (alpha_len ** 4)]}{alphaUpper[(i // (alpha_len ** 3)) % alpha_len]}{alphaUpper[(i // (alpha_len ** 2)) % alpha_len]}{alphaUpper[(i // alpha_len) % alpha_len]}{alphaUpper[i % alpha_len]}"
                for i in range(n_rnd_cols)]

        colonnes_aleatoires_str = ", ".join([f"Col_{col} REAL" for col in col_suffixes])
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (RowId INTEGER PRIMARY KEY, {colonnes_aleatoires_str});"

    def generate_random_tuples(self, n):
        """
        Generate a list of n random tuples for basic columns (Rarete, Duree, Victoire).

        :param n: Number of tuples to generate.
        :return: List of tuples.
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
        Generate random tuples for all columns of the table.

        :param n: Number of tuples to generate.
        :return: List of tuples.
        """
        random_tuples = []
        for _ in range(n):
            col_tuple = []
            for col in range(self.colonne_len - 1):
                rand_func = random.uniform if col % 4 == 0 else random.randint
                categories_min = [1, 10, 100]
                coeff_categories_max = [5, 10, 50, 100]

                max_of_min_idx = random.choice(range(len(categories_min)))
                raw_mini = rand_func(0, categories_min[max_of_min_idx])
                mini = max(1, raw_mini - (raw_mini % categories_min[max(0, max_of_min_idx - 1)]))

                max_of_max_idx = random.choice(range(1, len(coeff_categories_max)))
                max_of_max = categories_min[max_of_min_idx] * coeff_categories_max[max_of_max_idx]
                raw_maxi = rand_func(mini + coeff_categories_max[max(0, max_of_max_idx - 1)], max_of_max)
                maxi = max(1, raw_maxi - (raw_maxi % coeff_categories_max[max(0, max_of_max_idx - 1)]))

                current_col = rand_func(mini, maxi)
                col_tuple.append(current_col)
            random_tuples.append(col_tuple)
        return random_tuples

    def insert_random_tuples(self, n):
        """
        Insert random tuples into the database.

        :param n: Number of tuples to generate and insert.
        :return: Boolean indicating success.
        """
        try:
            query = f"INSERT OR IGNORE INTO {self.table_name} ({','.join([x for x in self.colonne_names[1:]])}) VALUES ({','.join(['?' for _ in range(self.colonne_len - 1)])})"
            randomized_queries = self.generate_random_tuples_for_all_columns(n)
            self.cursor.executemany(query, randomized_queries)
            self.conn.commit()
            return True
        except Exception as e:
            print("Insert Error:", e)
            return False
