import random
import sqlite3, math
import string

from Utils.DataParser import DataParser
from Utils.DisplayHelpers import beauty_print


class Database:
    '''
    Classe qui lance l'algo en SQL
    '''

    def __init__(self, db_filepath,col_len, row_len=0, is_debug=True):
        self.is_debug=is_debug
        self.relations = []
        self.conn=sqlite3.connect(db_filepath)
        self.conn.create_function('sqrt', 1, math.sqrt)
        self.cursor =self.conn.cursor()
        self.table_name="Pokemon"
        self.colonnes_initiales_str = []
        self.create_table_query_str = self.generer_table(col_len)
        self.create_table(self.create_table_query_str)
        try:
            self.colonne_len=self.nombre_colonnes_table()
        except Exception as e:
            print(e)
            self.colonne_len = 9
        self.colonne_names = self.get_column_names(self.table_name)
        if self.colonne_len>1:
            if row_len>0:
                self.insert_random_tuples(row_len)




    def get_column_names(self, nom_table):
        '''
        Get the column's names of the table
        :param nom_table: the table name
        :return: The column's names in a list
        '''
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
        '''
        Get the columns length
        :param nom_table: Le name of the table
        :return: Le number of column into the table (int)
        '''
        if nom_table==None:
            nom_table=self.table_name
        try:
            # Get informations about the table
            self.cursor.execute(f"PRAGMA table_info({nom_table})")
            self.colonnes = self.cursor.fetchall()
            # Get the columns length (count)
            return len(self.colonnes)
        except sqlite3.Error as e:
            print("Error while recovering informations about table :", e)
            return None

    def create_table(self, sql_query=None):
        '''
        Create the table
        :param sql_query: the query otherwise basic schema is auto provided
        :return: Bolean of status creation
        '''
        if sql_query==None:
            sql_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            RowId INTEGER PRIMARY KEY, 
            Rarete REAL, 
            Duree REAL, 
            Victoire REAL);
            """
        try:
            #print(sql_query)

            self.conn.execute(f"DROP TABLE IF EXISTS {self.table_name};")
            self.conn.commit()
            self.conn.execute(sql_query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


    def select_by_id(self, row_id):
        '''
        Select un enregistrement par id
        :param row_id: L'id
        :return: L'enregistrement
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId = ?"
        self.cursor.execute(sql_query, (row_id,))
        return self.cursor.fetchall()

    def select_all_for_check_max(self):
        '''
        Vérifie si les règles de générations àléatoires ont été respectées
        :return: Tous les enregistrements qui ne respectent pas les règles (donc une liste vide)
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete > 10 or Duree < 2 or Duree > 132 or Victoire > 100"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_all_until_id(self, until_id):
        '''
        Select jusqu'à un id
        :param until_id: L'id max
        :return: Les enregistrements jusqu'à l'id voulu
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE RowId <= ?"
        self.cursor.execute(sql_query, (until_id,))
        self.data = [x for x in self.cursor.fetchall()]
        return

    def select_all(self):
        '''
        Select tout
        :return: Tous les enregistrements de la table
        '''
        sql_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def select_by_rarete(self, rarete):
        '''
        Select par rareté
        :param rarete: La rareté exacte
        :return: Les enregistrements qui correspondent à cette rareté
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE Rarete = ?"
        self.cursor.execute(sql_query, (rarete,))
        return self.cursor.fetchall()

    def select_by_duree(self, duree):
        '''
        Select par durée
        :param duree: La durée exacte
        :return: Les enregistrements qui correspondent à cette durée
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE Duree = ?"
        self.cursor.execute(sql_query, (duree,))
        return self.cursor.fetchall()

    def select_by_victoire(self, victoire):
        '''
        Select par victoire
        :param victoire: La victoire exacte
        :return: Les enregistrements qui correspondent à cette victoire
        '''
        sql_query = f"SELECT * FROM {self.table_name} WHERE Victoire = ?"
        self.cursor.execute(sql_query, (victoire,))
        return self.cursor.fetchall()

    def generer_table(self, n_rnd_cols):
        # Colonnes fixes
        colonnes_fixes_str = ", ".join([f"{colonne} REAL" for colonne in self.colonnes_initiales_str])

        alphaUpper=string.ascii_uppercase
        alpha_len=len(alphaUpper)
        _2_chars_len=alpha_len**2
        _3_chars_len=alpha_len**3
        _4_chars_len=alpha_len**4
        # Colonnes aléatoires

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

        # Génération de la requête CREATE TABLE
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (RowId INTEGER PRIMARY KEY, {colonnes_aleatoires_str});"
        #print(query)
        return query

    def generate_random_tuples(self, n):
        '''
        Génère des tuples de manière aléatoire
        :param n: Le nombre de tuples à générer
        :return: Les tuples
        '''
        random_tuples = []
        for _ in range(n):
            rarete = random.randint(0, 10)
            duree = random.randint(2, 132)
            victoire = random.randint(0, 100)
            random_tuples.append((rarete, duree, victoire))
        return random_tuples


    def generate_random_tuples_for_all_columns(self, n):
        '''
        Génère des tuples de manière aléatoire
        :param n: Le nombre de tuples à générer
        :return: Les tuples
        '''
        random_tuples = []
        for _ in range(n):
            col_tuple = []
            for col in range(self.colonne_len-1):
                if col%4==0:
                    rand_func = random.uniform
                else:
                    rand_func = random.randint
                categories_min = [1, 10, 100]
                coeff_categories_max = [5, 10, 50, 100]

                max_of_min_idx = random.choice(range(len(categories_min)))
                raw_mini = rand_func(0, categories_min[max_of_min_idx])
                mini = raw_mini - (raw_mini % categories_min[max(0, max_of_min_idx - 1)])
                mini=max(1,mini)
                max_of_max_idx = random.choice(range(1, len(coeff_categories_max)))
                max_of_max = categories_min[max_of_min_idx] * coeff_categories_max[max_of_max_idx]

                raw_maxi = rand_func(mini + coeff_categories_max[max(0, max_of_max_idx - 1)], max_of_max)
                maxi = raw_maxi - (raw_maxi % coeff_categories_max[max(0, max_of_max_idx - 1)])  #
                maxi=max(1,maxi)
                current_col = rand_func(mini, maxi)
                col_tuple.append(current_col)
            random_tuples.append(col_tuple)
            """
            for col in range(self.colonne_len):
                mini=random.randint(0, 100)
                maxi=random.randint(mini+1, min(1000, mini**2))
                current_col = random.randint(mini, maxi)
                col_tuple.append(current_col)
            random_tuples.append(col_tuple)
            """
        return random_tuples

    def insert_random_tuples(self, n):
        '''
        Méthode wrapper qui prend le nombre de tuples à générer et qui les génère pour les
        insérer directement en base de données
        :param n: Le nombre de tuples à générer
        :return: Booleen
        '''
        try:

            query=f"INSERT OR IGNORE INTO {self.table_name} ({','.join([x for x in self.colonne_names[1:]])}) VALUES ({','.join(['?' for _ in range(self.colonne_len-1)])})"
            #print(query)
            randomized_queries = self.generate_random_tuples_for_all_columns(n)
            #print(randomized_queries[0])

            self.cursor.executemany(query,
                                    randomized_queries)
            self.conn.commit()
            return True
        except Exception as e:
            print("212:", e)
            return False