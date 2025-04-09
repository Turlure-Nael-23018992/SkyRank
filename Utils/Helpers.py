import sqlite3, random
import time
from collections import OrderedDict
from colorama import Back, Fore, Style
import numpy as np
#TODO:
from Utils.DisplayHelpers import print_green, print_red


class DP_IDP_ALL:
    '''
    Classe qui lance l'algorithme DP-IDP
    '''

    def __init__(self, r, is_debug=False):
        self.is_debug = is_debug  # Permet de toogle le graphe et les matrices
        self.relations = r
        self.dom, self.tot = self.dp_idp1()
        if self.is_debug:
            self.graph_it()

    def dp_idp1(self):
        len_ = len(self.relations)
        dom = [["/" if x == y else 0 for y in range(len_)] for x in range(len_)]
        tot = [0] * len_
        for row in range(len_):
            for col in range(len_):
                if row != col:
                    must_increase = all(
                        self.relations[col][k] <= self.relations[row][k] for k in range(len(self.relations[col])))
                    dom[row][col] = int(must_increase)
                    tot[row] += int(must_increase)
        if self.is_debug:
            self.display_console(dom, tot)
        return dom, tot

    def display_console(self, dom, tot):
        for i, d in enumerate(dom):
            print(dom[i], end="")
            print(f"({tot[i]})")
        print(100 * "*")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


def python2_to_python3_folders(py3_dir, py2_dir):
    command_to_run_in_cmd = fr"2to3 --output-dir={py3_dir} -w -n {py2_dir}"
    print(f"commande à lancer dans la console:\n{command_to_run_in_cmd}")
    return command_to_run_in_cmd


def menu(default_choice="2"):
    '''
    Menu d'init
    :return: L'objet de la base de données
    '''
    user_choice = default_choice
    while user_choice not in ("0", "1"):
        user_choice = input('Première utilisation\n0.Oui\n1.Non')

    if user_choice == "0":
        # generate
        nb_str = str(input("Nombre d'enregistrements à générer:\n")).strip()
        db_obj.insert_random_tuples(int(nb_str))
        print(f"lignes hors règles {db_obj.select_all_for_check_max()}")

        #print(db_obj.select_all())
    return db_obj


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    r = {
        1: (5, 20, 1 / 70),
        2: (4, 60, 1 / 50),
        3: (5, 30, 1 / 60),
        4: (1, 80, 1 / 60),
        5: (5, 90, 1 / 40),
        6: (9, 30, 1 / 50),
        7: (7, 80, 1 / 40),
        8: (9, 90, 1 / 30)
    }

    r = {
        1: (5, 20, 1 / 70),
        2: (4, 60, 1 / 50),
        4: (1, 80, 1 / 60)
    }

    cosky = Cosky(r)
    print("\n" * 2)
    print("r", r)
    print("cosky.relation", cosky.relations)
    quit()

    db_obj = menu("1")
    #algo_types = [Cosky, DP_IDP, DP_IDP_ALL, CoskySQL, JF]
    algo_types = [Cosky, DP_IDP, DP_IDP_ALL, CoskySQL]
    print_green("ALGOS comparaisons")
    iterations = [8, 40, 200, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    all_logs = []
    # Pour toutes mes itérations demandées
    for row_count in iterations:
        iteration_logs = []
        print()
        print_red(f"[{row_count}] iterations...")

        # Pour tous les types d'algos
        for algo_type in algo_types:
            # Le nom de la classe de l'algo
            algo_name = algo_type.__name__
            #print_green(f"\tALGO [{algo_name}]")
            r = db_obj.select_all_until_id(row_count)
            time_calc = TimeCalc(row_count, algo_name)
            # Pour l'algo SQL on lui rajoute l'objet connection dans les arguments
            if algo_name == "CoskySQL":
                algo_obj = algo_type(r, db_obj.conn)
            else:
                algo_obj = algo_type(r)
            time_calc.stop()
            iteration_logs.append(time_calc)
        min_for_sample = min([x.ratio for x in iteration_logs])
        for x in iteration_logs:
            if x.ratio == min_for_sample:
                print_green(x.get_formated_data())
            else:
                print(x.get_formated_data())
    db_obj.conn.close()


class Ranking:
    '''
    Classe qui optimise le 'sort' par split du ranking
    '''

    def __init__(self):
        self.ordered_dict = OrderedDict()


classement = []
r = [
    (5, 20, 1 / 70),
    (4, 60, 1 / 50),
    (5, 30, 1 / 60),
    (1, 80, 1 / 60),
    (5, 90, 1 / 40),
    (9, 30, 1 / 50),
    (7, 80, 1 / 60),
    (9, 90, 1 / 30)
]

# Si un nombre A est meilleur qu'un autre nombre B ce n'est pas la peine de
# comparer A avec les nombres qui sont moins bons que B

len_ = len(r)
dom = [["/" if x == y else 0 for y in range(len_)] for x in range(len_)]
tot = [0] * len_
for i in range(len_):
    if i == 0:
        classement.append(dom[i])
