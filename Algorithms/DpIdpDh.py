"""
*******************************************************************************
Légende : 0->false, 1 -> true

dom et sp après calculMatriceDesDominants() :
(1) / 0 0 0 0 0 0 0 | 0 |
(2) 0 / 0 0 0 0 0 0 | 0 |
(3) 1 0 / 0 0 0 0 0 | 1 |
(4) 0 0 0 / 0 0 0 0 | 0 |
(5) 1 1 1 1 / 0 0 0 | 1 |
(6) 1 0 1 0 0 / 0 0 | 1 |
(7) 1 1 1 1 0 0 / 0 | 1 |
(8) 1 1 1 1 1 1 1 / | 1 |

dom et sp après calculGrapheDeCouverture() :
(1) / 0 0 0 0 0 0 0 | 0 |
(2) 0 / 0 0 0 0 0 0 | 0 |
(3) 1 0 / 0 0 0 0 0 | 1 |
(4) 0 0 0 / 0 0 0 0 | 0 |
(5) 0 1 1 1 / 0 0 0 | 1 |
(6) 0 0 1 0 0 / 0 0 | 1 |
(7) 0 1 1 1 0 0 / 0 | 1 |
(8) 0 0 0 0 1 1 1 / | 1 |

sky, skyCard après calculGrapheDeCouverture() :
(1) 0 0 1 0 1 1 1 1 | 5
(2) 0 0 0 0 1 0 1 1 | 3
(4) 0 0 0 0 1 0 1 1 | 3

sky, skyCard et score calculLm() et calculScore() :
(1) 0 0 2 0 3 3 3 4 | 0 | 0.835
(2) 0 0 0 0 2 0 2 3 | 0 | 0.636
(4) 0 0 0 0 2 0 2 3 | 0 | 0.636

*******************************************************************************

==============================
dpIdpAvecHierarchieDeDominance
==============================
Entrée :
    La relation r.
Sortie :
    Le tableau des scores de dp-idp.

calculMatriceDesDominants(r);

calculGrapheDeCouverture(dom, sp);

calculLm(dom, sky, skyCard);

calculScore(sky, spTot);

=========================
calculMatriceDesDominants
=========================
Entrée :
    La relation r.
Sortie :
    Le tableau à deux dimensions carré indiquant les dominances dom.
    Le tableau indiquant les points du Skyline sp.

dom <- nouveau tableau
sp <- nouveau tableau
Pour i de 0 à taille(r) - 1
    dom[i] <- nouveau tableau
    sp[i] <- false
    Pour j de 0 à taille(r) - 1
        Si i = j
            dom[i][j] = "/"
        Sinon
            sup <- vrai
            Pour k de 0 à taille(r[j]) - 1
                Si r[j][k] > r[i][k] // ">" car Préférences = MIN, MIN, MIN
                    sup <- faux
                    break
            Si sup
                dom [i][k] = true
                sp[i] <- true
            Sinon
                dom[i][k] = false

========================
calculGrapheDeCouverture
========================

Entrée :
    Le tableau à deux dimensions carré indiquant les dominances dom.
    Le tableau indiquant les points du Skyline sp.
Sortie :
    Le tableau à deux dimensions carré indiquant les dominances du graphe de couveture dom.
    Le tableau des points du Skyline sky.
    Le nombre de points du Skyline spTot.
    Le tableau des cardinalités de dominance des points du Skyline skyCard.

sky <- nouveau tableau
spTot <- 0
skyCard <- nouveau tableau
n <- taille(dom) - 1
Pour i de 0 à n
    Si sp[i]
        sky[i] <- nouveau tableau
        spTot = spTot + 1
        skyCard[i] <- 0
    Sinon
        Pour j de 0 à n
            Si i != j et !sp[j] et dom[i, j]
                Si j dans sky
                    sky[j][i] <- 1
                    skyCard[j] <- skyCard[j] + 1
                Pour k de 0 à n
                    Si dom[j][k]
                        dom[i][k] <- false

========
calculLm
========
Entrée :
    Le tableau à deux dimensions carré indiquant les dominances du graphe de couveture dom.
    Le tableau des points du Skyline sky.
    Le tableau des cardinalités de dominance des points du Skyline skyCard.
Sortie :
    Le tableau des points du Skyline avec les lm des points dominés sky.

Pour tout i dans sky
    lm(dom, sky, skyCard, i, 1)

fonction lm(dom, sky, skyCard, i, prof)
    Si skyCard[i] = 0
        return
    Pour j de 0 à n
        Si dom[j][i]
            sky[i][j] = sky[i][j] + prof
            skyCard[i] <- skyCard[i] - 1
            lm(dom, sky, skyCard, j, prof + 1)

===========
calculScore
===========
Entrée :
    Le tableau des points du Skyline avec les lm des points dominés sky.
    Le nombre de points du Skyline spTot.
Sortie :
    Le tableau des scores de dp-idp.

// idp n'est calculé que pour les sp, alors|{sp'...}| = 1
idp <- log(spTot)
score <- nouveau tableau
Pour tout i dans sky
    tot <- 0
    Pour j de 0 à n
        tot <- tot + 1/sky[i][j]
    score[i] <- tot x idp




===========
CoskySQL_param
===========

Entrée :
    La relation r.
    Le tableau d'attributs de la relation r att.
Sortie :
    Le skyline de r, avec son score, ordonné par Cosky.

n <- taille(att) - 1
Si n < 1
    return

// "<=" de S. (skyline)
s1 = "R2." + att[0] + " <= " R1." + att[0]
Pour i de 1 à n
    s1 = s1 + " AND R2." + att[i] + " <= " R1." + att[i]

// "<" de S.
s2 = "R2." + att[0] + " < " R1." + att[0]
Pour i de 1 à n
    s2 = s2 + " OR R2." + att[i] + " < " R1." + att[i]

// N de SN.
snn = att[0] + " / T" + att[0] + " AS N" + att[0]
Pour i de 1 à n
    snn = snn + ", " + att[i] + " / T" + att[i] + " AS N" + att[i]

// T de SN.
snt = "SUM(" + att[0] + ") AS T" + att[0]
Pour i de 1 à n
    snt = snt + ", SUM(" + att[i] + ") AS T" + att[i]

// SGini.
sgini = "1 - (SUM(N" + att[0] + " * N" + att[0] + ")) AS Gini" + att[0]
Pour i de 1 à n
    sgini = sgini + ", 1 - (SUM(N" + att[i] + " * N" + att[i] + ")) AS Gini" + att[i]

// Somme des Gini.
giniTot = "Gini" + att[0]
Pour i de 1 à n
    giniTot = giniTot + " + Gini" + att[i]

// SW.
sw = "Gini" + att[0] + " / (" + giniTot + ") AS W" + att[0]
Pour i de 1 à n
    sw = sw + ", Gini" + att[i] + " / (" + giniTot + ") AS W" + att[i]

// SP.
sp = "W" + att[0] + " * N" + att[0] + " AS P" + att[0]
Pour i de 1 à n
    sp = sp + ", W" + att[i] + " * N" + att[i] + " AS P" + att[i]

// Idéal.
ideal = "MIN(P" + att[0] + ") AS I" + att[0]
Pour i de 1 à n
    ideal = ideal + ", MIN(P" + att[i] + ") AS I" + att[i]

// Numérateur du score.
scoreNum = "I" + att[0] + " * P" + att[0]
Pour i de 1 à n
    scoreNum = scoreNum + " + I" + att[i] + " * P" + att[i]

// P².
pp = "P" + att[0] + " * P" + att[0]
Pour i de 1 à n
    pp = pp + " + P" + att[i] + " * P" + att[i]

// I².
ii = "I" + att[0] + " * I" + att[0]
Pour i de 1 à n
    ii = ii + " + I" + att[i] + " * I" + att[i]

// Projection finale.
proj = att[0]
Pour i de 1 à n
    proj = proj + ", " + att[i]

q = "WITH S AS (SELECT * FROM " + r + " AS R1
WHERE NOT EXISTS (SELECT * FROM " + r + " AS R2 WHERE (" + s1 + ") AND (" + s2 + "))),
SN AS (SELECT RowId, " + snn + " FROM S, (SELECT " + snt + " FROM S) AS ST),
SGini AS (SELECT " + sgini + " FROM SN),
SW AS (SELECT " + sw + " FROM SGini),
SP AS (SELECT RowId, " + sp + " FROM SN, SW),
Idéal AS (SELECT " + ideal + FROM SP),
SScore AS (SELECT RowId, (" + scoreNum + ") / (SQRT(" + pp + ") * SQRT(" + ii + ")) AS Score FROM Idéal, SP)
SELECT " + r + ".RowId, " + proj + ", ROUND(Score, 3) AS Score
FROM " + r + " INNER JOIN SScore rs ON " + r + ".RowId = rs.RowId
ORDER BY Score DESC;"
ᐧ


*******************************************************************************
"""
# Traduire tous les algos


from colorama import Fore, Style
import math
import json
from Utils.JsonUtils import readJson, writeJson, updateJson, sortJson, prettyPrintTimeData


def display_matrice(matrice):
    """
    Display a matrix or a dictionary in a formatted way.
    :param matrice: the matrix or dictionary to display
    """
    if type(matrice[0])==list:
        for row in matrice:
            row = [int(x) if x != "/" else "/" for x in row ]
            print(row)
    elif type(matrice) == dict:
        for k,v in matrice.items():
            print(f"{k:{v}}")
    else:
        print([int(elem) for elem in matrice])


dom=[
["/",0,0,0,0,0,0,0],
[0,"/",0,0,0,0,0,0],
[1,0,"/",0,0,0,0,0],
[0,0,0,"/",0,0,0,0],
[1,1,1,1,"/",0,0,0],
[1,0,1,0,0,"/",0,0],
[1,1,1,1,0,0,"/",0],
[1,1,1,1,1,1,1,"/"],
]
sp=[0,0,1,0,1,1,1,1]

"""
  else:
        for row in range(len_):
            for col in range(len_):
                if row != col:
                    must_increase=0
                    for k in range(len(r[col])):
                        must_increase = int(r[col][k]<=r[row][k])
                        if must_increase==0:
                            break
                    dom[row][col]=must_increase
                    sp[row]+=must_increase
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------



#r = db_obj.select_all_until_id(8)

def calculMatriceDesDominants(r):
    """
    Calculate the dominance matrix and the skyline points.
    :param r: the relation
    :return: the dominance matrix and the skyline points
    """
    len_ = len(r)
    dom = [["/" if x == y else False for y in range(len_)] for x in range(len_)]
    sp = [True] * len_
    r_keys=list(r.keys())
    print()
    col_len = len(r.get(r_keys[0]))
    for row_index in range(len_):
        for col_index in range(len_):
            if row_index != col_index:
                sup = True
                for k in range(col_len):
                    r_val = list(r.values())
                    if r_val[col_index][k] > r_val[row_index][k]:
                        sup=False
                        break
                if sup:
                    dom[row_index][col_index] = True
                    sp[row_index] = False
                else:
                    dom[row_index][col_index]=False

    return dom, sp



# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------




def calculGrapheDeCouverture(dom, sp, display_graph=False):
    """
    Calculate the coverage graph of the dominance matrix.
    :param dom: the dominance matrix
    :param sp: the skyline points
    :param display_graph: the flag to display the graphS
    :return: the dominance matrix, the skyline points, the total skyline points, the skyline cardinality, and the dominance cardinality
    """
    import networkx as nx
    import matplotlib.pyplot as plt


    G,nodes=None, None
    edges = []
    Ip = "I+"
    if display_graph:
        # Création d'un graphe vide
        G = nx.DiGraph()

        #pos = {1: (0, 0), 2: (1, 1), 3: (2, 0), 4:(3,3), 5:(1,5), 6:(2,4), 7:(2,3),8:(2,4)}
        #nx.draw(G, pos=pos)
        # Ajout des nœuds
        nodes = [Ip]
        nodes.extend([i + 1 for i in range(len(dom))])

    n = len(dom)
    sky={}
    skyCard={}
    domCard = [0]*n
    spTot = 0
    for i in range(n):
        if sp[i]:
            sky[i]=[0] * n
            spTot+=1
            skyCard[i]=0
            if display_graph:
                edges.append((Ip, i + 1,))
        else:
            for j in range(n):
                if i != j and dom[i][j]==True:
                    #"""
                    if j in sky.keys():
                        sky[j][i]=1
                        skyCard[j]=skyCard[j]+1
                        domCard[i]=domCard[i]+1
                    #"""
                    if sp[j]==False:
                        for k in range(n):
                            if dom[j][k]==True:
                                dom[i][k] = False
            if display_graph:
                for j in range(n):
                    if dom[i][j] == 1:
                        edges.append((j + 1, i + 1,))

    if display_graph:
        G.add_nodes_from(nodes)
        # Ajout des arêtes
        G.add_edges_from(edges)

        # Dessin du graphe
        pos = nx.circular_layout(G)  # Définition de la disposition des nœuds
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)  # Dessin des nœuds
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray', arrows=True,
                               arrowsize=20)  # Dessin des arêtes
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')  # Ajout des labels

        # Affichage du graphe
        plt.title("Graphe simple avec des nœuds et des arêtes")
        plt.axis('off')  # Désactivation des axes
        plt.show()
    return dom, sky, spTot, skyCard, domCard




# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def print_color(color, text):
    """
    Print in the desired color
    :param color: The color (formatted for colorama) Fore.GREEN / Fore.BLUE etc...
    :param text: The text to display
    :return: None
    """
    print(f"{color} {text} {Style.RESET_ALL}")


def print_green(text):
    """
    Print in green
    :param text: The text to display
    :return: None
    """
    print_color(Fore.GREEN, text)


def print_red(text):
    """
    Print in red
    :param text: The text to display
    :return: None
    """
    print_color(Fore.RED, text)



def lm(dom, sky, skyCard, i,j, prof):
    """
    Function to calculate the lm of the skyline points.
    :param dom: the dominance matrix
    :param sky: the skyline points
    :param skyCard: the skyline cardinality
    :param i: the index of the skyline point
    :param prof: the current depth
    :return: the skyline points with the lm
    """
    n=len(dom)
    if skyCard[i]==0:
        #print_red(f"fin...i:{i+1} / j:{j+1} / prof:{prof}")
        return sky
    for k in range(n):
        if dom[k][j]==True:
            #print(f"sky:{sky[i]}\nskyCard:{skyCard[i]}\n{Fore.GREEN}i:{i+1} / j:{j+1} / k:{k+1} / prof:{prof} sky[{i}][{j}]:{sky[i][j]}{Style.RESET_ALL}")
            if sky[i][k]==1:
                sky[i][k]+=prof
                skyCard[i]-=1
            new_prof=prof+1
            sky = lm(dom, sky, skyCard, i, k, new_prof)
    return sky




def calculLm(dom, sky, skyCard):
    """
    Calculate the lm of the skyline points.
    :param dom: the dominance matrix
    :param sky: the skyline points
    :param skyCard: the skyline cardinality
    :return: the skyline points with the lm
    """
    for k,v in sky.items():
        sky = lm(dom, sky, skyCard, k, k, 1)
    return sky








# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


def calculScore(sky, domCard, spTot):
    """
    Calculate the score of the skyline points.
    :param sky: the skyline points
    :param domCard: the dominance cardinality
    :param spTot: the total skyline points
    :return: the score of the skyline points
    """
    score = {}
    for i in sky:
        tot=0
        for j in range(len(sky[i])):
            if sky[i][j]>0:
                tot+=1/sky[i][j] * math.log10(spTot / domCard[j])
        score[i]=tot
    return score




class DpIdpDh:
    """
    Class to implement the dp-idp-dh algorithm for ranking and sorting data based on multiple criteria.
    """

    def __init__(self, r):
        """
        Constructor to initialize the dp-idp-dh algorithm.
        :param r: the relation
        """
        self.r=r

        self.run()

    def run(self):
        """
        Run the dp-idp-dh algorithm to compute the ranking and sorting of data based on multiple criteria.
        """
        self.dom, self.sp = self.calculMatriceDesDominants(self.r)
        self.dom, self.sky, self.spTot, self.skyCard, self.domCard = self.calculGrapheDeCouverture(self.dom, self.sp)
        self.sky = self.calculLm(self.dom, self.sky, self.skyCard)
        self.score = self.calculScore(self.sky, self.domCard, self.spTot)



    def calculMatriceDesDominants(self, r):
        """
        Calculate the dominance matrix and the skyline points.
        :param r: the relation
        :return: the dominance matrix and the skyline points
        """
        len_ = len(r)
        dom = [["/" if x == y else False for y in range(len_)] for x in range(len_)]
        sp = [True] * len_
        r_keys = list(r.keys())
        print()
        col_len = len(r.get(r_keys[0]))
        for row_index in range(len_):
            for col_index in range(len_):
                if row_index != col_index:
                    sup = True
                    for k in range(col_len):
                        r_val = list(r.values())
                        if r_val[col_index][k] > r_val[row_index][k]:
                            sup = False
                            break
                    if sup:
                        dom[row_index][col_index] = True
                        sp[row_index] = False
                    else:
                        dom[row_index][col_index] = False

        return dom, sp

    def calculGrapheDeCouverture(self, dom, sp, display_graph=False):
        """
        Calculate the coverage graph of the dominance matrix.
        :param dom: the dominance matrix
        :param sp: the skyline points
        :param display_graph: flag to display the graph
        :return: the dominance matrix, the skyline points, the total skyline points, the skyline cardinality, and the dominance cardinality
        """

        n = len(dom)
        sky = {}
        skyCard = {}
        domCard = [0] * n
        spTot = 0
        for i in range(n):
            if sp[i]:
                sky[i] = [0] * n
                spTot += 1
                skyCard[i] = 0

            else:
                for j in range(n):
                    if i != j and dom[i][j] == True:
                        # """
                        if j in sky.keys():
                            sky[j][i] = 1
                            skyCard[j] = skyCard[j] + 1
                            domCard[i] = domCard[i] + 1
                        # """
                        if sp[j] == False:
                            for k in range(n):
                                if dom[j][k] == True:
                                    dom[i][k] = False


        return dom, sky, spTot, skyCard, domCard


    def calculGrapheDeCouverture1(self, dom, sp, display_graph=False):
        """
        Calculate the coverage graph of the dominance matrix.
        :param dom: the dominance matrix
        :param sp: the skyline points
        :param display_graph: flag to display the graph
        :return: the dominance matrix, the skyline points, the total skyline points, the skyline cardinality, and the dominance cardinality
        """
        import networkx as nx
        import matplotlib.pyplot as plt
        G, nodes = None, None
        edges = []
        Ip = "I+"
        if display_graph:
            # Création d'un graphe vide
            G = nx.DiGraph()
            # pos = {1: (0, 0), 2: (1, 1), 3: (2, 0), 4:(3,3), 5:(1,5), 6:(2,4), 7:(2,3),8:(2,4)}
            # nx.draw(G, pos=pos)
            # Ajout des nœuds
            nodes = [Ip]
            nodes.extend([i + 1 for i in range(len(dom))])
        n = len(dom)
        sky = {}
        skyCard = {}
        domCard = [0] * n
        spTot = 0
        for i in range(n):
            if sp[i]:
                sky[i] = [0] * n
                spTot += 1
                skyCard[i] = 0
                if display_graph:
                    edges.append((Ip, i + 1,))
            else:
                for j in range(n):
                    if i != j and dom[i][j] == True:
                        # """
                        if j in sky.keys():
                            sky[j][i] = 1
                            skyCard[j] = skyCard[j] + 1
                            domCard[i] = domCard[i] + 1
                        # """
                        if sp[j] == False:
                            for k in range(n):
                                if dom[j][k] == True:
                                    dom[i][k] = False
                if display_graph:
                    for j in range(n):
                        if dom[i][j] == 1:
                            edges.append((j + 1, i + 1,))
        if display_graph:
            G.add_nodes_from(nodes)
            # Ajout des arêtes
            G.add_edges_from(edges)
            # Dessin du graphe
            pos = nx.circular_layout(G)  # Définition de la disposition des nœuds
            nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)  # Dessin des nœuds
            nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray', arrows=True,
                                   arrowsize=20)  # Dessin des arêtes
            nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')  # Ajout des labels
            # Affichage du graphe
            plt.title("Graphe simple avec des nœuds et des arêtes")
            plt.axis('off')  # Désactivation des axes
            plt.show()
        return dom, sky, spTot, skyCard, domCard

    def lm_jf(self, dom, sky, skyCard, i, j, prof):
        """
        Function to calculate the lm of the skyline points using a stack instead of recursion.
        :param dom: the dominance matrix
        :param sky: the skyline points
        :param skyCard: the skyline cardinality
        :param i: the index of the skyline point
        :param j: the index of the skyline point
        :param prof: the current depth
        :return: the skyline points with the lm
        """
        n = len(dom)
        stack = [(i, j, prof)]  # Utilisation d'une pile au lieu de la récursion
        while stack:
            current_i, current_j, current_prof = stack.pop()
            for k in range(n):
                if dom[k][current_j]:
                    if sky[current_i][k] > 0 and skyCard[current_i] > 0:
                        sky[current_i][k] += current_prof
                        skyCard[current_i] -= 1
                    if skyCard[current_i] == 0:
                        break
                    stack.append((current_i, k, current_prof + 1))  # Ajout à la pile au lieu de l'appel récursif
        return sky





    def lm(self, dom, sky, skyCard, i, j, prof):
        """
        Recursive function to calculate and update the dominance levels (lm)
        of skyline points.

        When a point j is dominated by another point k, this function updates
        the 'sky' structure and decrements the corresponding cardinality.
        The update is propagated recursively with an incremented dominance level.

        :param dom: list[list[bool]] - dominance matrix (dom[k][j] == True means k dominates j)
        :param sky: dict - structure representing the skyline points
        :param skyCard: dict - dictionary containing the remaining dominance count for each point
        :param i: int - index of the current point being processed in sky
        :param j: int - target index in sky
        :param prof: int - current dominance level
        :yield: dict - updated version of the sky structure
        """
        n = len(dom)

        for k in range(n):
            if dom[k][j]:
                if sky[i][k] > 0 and skyCard[i] > 0:
                    dom[k][j] = False
                    value = sky[i][k]

                    # Prioritize the most probable condition first
                    if value == 1 or value > prof:
                        sky[i][k] = prof

                    skyCard[i] -= 1

                    if skyCard[i] == 0:
                        yield sky
                        return  # Stop recursion once all dominances are handled

                    new_prof = prof + 1

                    # Recursive call and iteration over updated skyline states
                    for updated_sky in self.lm(dom, sky, skyCard, i, k, new_prof):
                        yield updated_sky

        yield sky


    def calculLm(self, dom, sky, skyCard):
        """
        Initializes and calls the 'lm' function for each point in the skyline.
        Updates the sky structure incrementally using intermediate results from 'lm'.

        :param dom: list[list[bool]] - dominance matrix
        :param sky: dict - skyline point structure
        :param skyCard: dict - remaining dominance count for each point
        :return: dict - final updated sky structure
        """
        for k in sky.keys():
            for updated_sky in self.lm(dom, sky, skyCard, k, k, 2):
                sky = updated_sky  # Apply intermediate update to the sky
        return sky

    def calculLm1(self, dom, sky, skyCard):
        """
        Alternative version of 'calculLm' that calls 'lm' but returns the generator
        directly instead of consuming it. This version does NOT process the yielded values,
        which may lead to unexpected results.

        :param dom: list[list[bool]] - dominance matrix
        :param sky: dict - skyline point structure
        :param skyCard: dict - remaining dominance count for each point
        :return: generator - the generator returned by 'lm'
        """
        for k in sky.keys():
            sky= self.lm(dom, sky, skyCard, k, k, 2)
        return sky



    def calculScore(self, sky, domCard, spTot):
        """
        Calculates a score for each skyline entry based on dominance levels and frequency.

        The score is computed as a sum over all dimensions where the skyline value > 0:
        (1 / level) * log10(total support / cardinality of dominators)

        :param sky: dict - skyline structure (matrix-like: sky[i][j] gives dominance level of j for skyline i)
        :param domCard: dict - number of dominators for each point
        :param spTot: int - total number of support points
        :return: dict - scores per skyline index
        """
        score = {}
        for i in sky:
            tot = 0
            for j in range(len(sky[i])):
                if sky[i][j] > 0:
                    tot += 1 / sky[i][j] * math.log10(spTot / domCard[j])
            score[i] = tot
        return score

    def sort(self,rev):
        """
        Sorts the internal score dictionary in ascending or descending order.

        :param rev: str - sorting order, either "Asc" or "Desc"
        """
        reverse = True if rev == "Desc" else False
        self.score = dict(sorted(self.score.items(), key=lambda item: item[1], reverse=reverse))





def dpIdpAvecHierarchieDeDominance():
    """
    Demonstration of skyline processing using dominance hierarchy.

    This function performs the following steps:
    1. Constructs a set of items with 3D values.
    2. Computes the dominance matrix.
    3. Builds the skyline graph.
    4. Computes the dominance levels (lm).
    5. Calculates scores for each skyline node.
    6. Displays results at each step.
    """

    r={
    1:(5, 20, 1/70),
    2:(4, 60, 1/50),
    3:(5, 30, 1/60),
    4:(1, 80, 1/60),
    5:(5, 90, 1/40),
    6:(9, 30, 1/50),
    7:(7, 80, 1/40),
    8:(9, 90, 1/30)
    }


    dom, sp = calculMatriceDesDominants(r)

    print(f"STEP 1:")
    print("dom")
    display_matrice(dom)
    print(f"sp")
    display_matrice(sp)
    print(100*'*')
    dom, sky, spTot, skyCard, domCard = calculGrapheDeCouverture(dom, sp)


    print(f"STEP 2:")
    print("dom")
    display_matrice(dom)
    #display_matrice(sky)
    print(f"{Fore.GREEN}sky")
    for k,v in sky.items():
        print(f"{k}:{v}")

    print(f"{Style.RESET_ALL}spTot:{spTot}\nskyCard:{skyCard}\ndomCard:{domCard}")
    print(100*'*')

    sky=calculLm(dom, sky, skyCard)
    print(sky)

    """
    sky={
    0:[0, 0, 2, 0, 3, 3, 3, 4],
    1:[0,0,0,0,2,0,2,3],
    3:[0,0,0,0,2,0,2,3]
    }
    """

    score = calculScore(sky, domCard,spTot)
    print(score)



if __name__ == '__main__':
    import time

    r_big = readJson("Datas/RBig.json")

    # Convert the loaded dictionary values to tuples
    r_big = {key: tuple(value) for key, value in r_big.items()}

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

    startTime=time.time()
    dp_idp = DpIdpDh(r_big)
    print("--------------Avant--------------")
    print(dp_idp.score)
    print(f"temps: {time.time()-startTime}")
    print("--------------Apres--------------")
    dp_idp.sort("Desc")
    print(dp_idp.score)




