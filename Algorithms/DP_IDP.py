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


def display_matrice(matrice):
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
    '''
    Print dans la couleur voulue
    :param color: La couleur (formatée pour colorama) Fore.GREEN / Fore.BLUE etc...
    :param text: Le texte à afficher
    :return: None
    '''
    print(f"{color} {text} {Style.RESET_ALL}")


def print_green(text):
    '''
    Print en vert
    :param text: Le texte à afficher
    :return: None
    '''
    print_color(Fore.GREEN, text)


def print_red(text):
    '''
    Print en rouge
    :param text: Le texte à afficher
    :return: None
    '''
    print_color(Fore.RED, text)



def lm(dom, sky, skyCard, i,j, prof):
    '''
    Calcul de lm
    :param dom: La matrice
    :param sky:
    :param skyCard:
    :param i:
    :param prof: La profondeur
    :return: Le sky
    '''
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
    for k,v in sky.items():
        sky = lm(dom, sky, skyCard, k, k, 1)
    return sky








# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


def calculScore(sky, domCard, spTot):
    score = {}
    for i in sky:
        tot=0
        for j in range(len(sky[i])):
            if sky[i][j]>0:
                tot+=1/sky[i][j] * math.log10(spTot / domCard[j])
        score[i]=tot
    return score




class DP_IDP:
    '''
    Classe qui lance l'algo de DP-IDP
    '''

    def __init__(self, r):
        self.r=r

        self.run()

    def run(self):
        self.dom, self.sp = self.calculMatriceDesDominants(self.r)
        self.dom, self.sky, self.spTot, self.skyCard, self.domCard = self.calculGrapheDeCouverture(self.dom, self.sp)
        self.sky = self.calculLm(self.dom, self.sky, self.skyCard)
        self.score = self.calculScore(self.sky, self.domCard, self.spTot)



    def calculMatriceDesDominants(self, r):
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
        n = len(dom)

        for k in range(n):

            if dom[k][j] == True:
                if sky[i][k] > 0 and skyCard[i] > 0:
                    dom[k][j] = False
                    # Stocker sky[i][k] dans une variable temporaire
                    value = sky[i][k]
                    # Réorganiser les conditions pour vérifier d'abord la condition la plus probable
                    if value == 1 or value > prof:
                        sky[i][k] = prof
                    skyCard[i] -= 1
                    if skyCard[i] == 0:
                        yield sky
                        return  # Ajoutez un retour pour arrêter l'exécution une fois qu'un yield est atteint
                    new_prof = prof + 1
                    # Appeler récursivement lm et itérer sur les résultats
                    for updated_sky in self.lm(dom, sky, skyCard, i, k, new_prof):
                        yield updated_sky
        yield sky


    def calculLm(self, dom, sky, skyCard):
        for k in sky.keys():
            for updated_sky in self.lm(dom, sky, skyCard, k, k, 2):
                sky = updated_sky  # Met à jour sky avec l'état intermédiaire
        return sky

    def calculLm1(self, dom, sky, skyCard):
        # Clone the original sky structure to avoid mutating input during iteration
        for k in sky.keys():
            sky= self.lm(dom, sky, skyCard, k, k, 2)
        return sky



    def calculScore(self, sky, domCard, spTot):
        score = {}
        for i in sky:
            tot = 0
            for j in range(len(sky[i])):
                if sky[i][j] > 0:
                    tot += 1 / sky[i][j] * math.log10(spTot / domCard[j])
            score[i] = tot
        return score






def dpIdpAvecHierarchieDeDominance():

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

    r_big = {
        1: (8, 98, 0.441203300890855),
        2: (6, 61, 0.150467894238805),
        3: (6, 48, 0.568964742942391),
        4: (2, 94, 0.749729120190558),
        5: (3, 70, 0.908692576004283),
        6: (4, 62, 0.119187329770861),
        7: (5, 36, 0.986012923607787),
        8: (6, 50, 0.219128047215667),
        9: (7, 81, 0.465460006664842),
        10: (3, 60, 0.592693863859302),
        11: (5, 63, 0.596061905428879),
        12: (10, 38, 0.568639779486858),
        13: (2, 91, 0.339380886851714),
        14: (9, 93, 0.113533833313162),
        15: (6, 25, 0.0713886279566314),
        16: (6, 45, 0.44162440602093),
        17: (10, 95, 0.434247157616438),
        18: (1, 83, 0.752096525739804),
        19: (9, 40, 0.100074909998509),
        20: (7, 63, 0.817761742763542),
        21: (9, 112, 0.833430488434567),
        22: (10, 13, 0.634438471155865),
        23: (3, 49, 0.586830078583634),
        24: (10, 49, 0.041069596987538),
        25: (8, 107, 0.885359739067722),
        26: (7, 23, 0.577170889681052),
        27: (7, 40, 0.910043331439209),
        28: (9, 36, 0.300383626219022),
        29: (8, 27, 0.545623835904753),
        30: (4, 27, 0.877348526010463),
        31: (6, 57, 0.270984450745639),
        32: (5, 68, 0.00101601862031575),
        33: (1, 94, 0.363020547819659),
        34: (9, 62, 0.9031587459189),
        35: (3, 31, 0.426163668027749),
        36: (6, 18, 0.231772771573258),
        37: (1, 57, 0.24864007361012),
        38: (4, 108, 0.737166650587925),
        39: (10, 72, 0.333664993469004),
        40: (4, 79, 0.0495298525625052),
        41: (1, 11, 0.368601566927865),
        42: (3, 58, 0.0357639076381291),
        43: (10, 89, 0.933188399536444),
        44: (8, 76, 0.224789147929696),
        45: (8, 23, 0.509971535851774),
        46: (9, 55, 0.261222199377314),
        47: (4, 39, 0.945807755049263),
        48: (9, 64, 0.183679185891512),
        49: (2, 89, 0.791974439285413),
        50: (6, 72, 0.66190379794812),
        51: (6, 84, 0.900787283277776),
        52: (3, 54, 0.586801457658212),
        53: (7, 108, 0.251710486084873),
        54: (10, 60, 0.631750760727525),
        55: (5, 80, 0.441766879059585),
        56: (7, 28, 0.768083729241915),
        57: (1, 33, 0.530553144184815),
        58: (7, 75, 0.543061462309096),
        59: (2, 17, 0.0244462569128471),
        60: (3, 79, 0.347529863380939),
        61: (1, 32, 0.441644469400527),
        62: (5, 37, 0.208678162395086),
        63: (3, 54, 0.96605820253626),
        64: (7, 115, 0.0757460288472711),
        65: (2, 84, 0.917318440718585),
        66: (10, 24, 0.800125017538456),
        67: (2, 17, 0.00315426440199051),
        68: (3, 16, 0.768043366623843),
        69: (6, 11, 0.248772050464968),
        70: (9, 30, 0.531641946843089),
        71: (9, 18, 0.960387906661008),
        72: (2, 116, 0.213127889766805),
        73: (7, 41, 0.381985609688396),
        74: (9, 66, 0.41147637887889),
        75: (2, 112, 0.25229267041266),
        76: (3, 61, 0.685105920004318),
        77: (10, 29, 0.133315779142173),
        78: (1, 88, 0.432698798369112),
        79: (6, 37, 0.279487643552506),
        80: (6, 96, 0.497762445409929),
        81: (1, 64, 0.62912017323514),
        82: (4, 98, 0.727263947311585),
        83: (3, 29, 0.863554924435569),
        84: (4, 103, 0.0926657955340335),
        85: (8, 71, 0.662251607968123),
        86: (4, 38, 0.651334616381753),
        87: (4, 116, 0.544507476819108),
        88: (1, 95, 0.0632048395132987),
        89: (3, 11, 0.0714556428342785),
        90: (8, 117, 0.013221752693374),
        91: (2, 90, 0.8362149731695),
        92: (10, 60, 0.701816547884115),
        93: (3, 13, 0.911221513501651),
        94: (1, 50, 0.364365987906372),
        95: (2, 80, 0.6659631422954),
        96: (5, 47, 0.259535617911372),
        97: (10, 117, 0.799832987605985),
        98: (7, 86, 0.660587117260031),
        99: (3, 105, 0.209411692815248),
        100: (3, 66, 0.534222858602814),
        101: (7, 116, 0.0936634330526123),
        102: (7, 72, 0.175742160035476),
        103: (1, 63, 0.0886754904499806),
        104: (2, 71, 0.243201779381442),
        105: (5, 115, 0.852120181737694),
        106: (1, 19, 0.680444104602576),
        107: (6, 14, 0.937736192469243),
        108: (4, 90, 0.881810684112022),
        109: (7, 109, 0.614667479927217),
        110: (9, 52, 0.400254891319157),
        111: (5, 15, 0.847304483390168),
        112: (7, 15, 0.639824048430654),
        113: (8, 51, 0.558671881011253),
        114: (7, 69, 0.469033388451631),
        115: (2, 80, 0.151413949943305),
        116: (2, 79, 0.729304349186804),
        117: (8, 50, 0.318914397617645),
        118: (8, 60, 0.941638505925477),
        119: (1, 10, 0.409750975675221),
        120: (10, 59, 0.939688285541514),
        121: (6, 66, 0.458155513751185),
        122: (7, 120, 0.638098466719114),
        123: (8, 14, 0.318633295751182),
        124: (3, 28, 0.885354652351936),
        125: (4, 37, 0.696321365802445),
        126: (2, 34, 0.860353887859093),
        127: (6, 80, 0.05907607644691),
        128: (8, 47, 0.275012732493077),
        129: (7, 41, 0.577519064058104),
        130: (6, 118, 0.717616283056777),
        131: (6, 111, 0.917086541400059),
        132: (2, 91, 0.505928835962916),
        133: (5, 87, 0.700496867528153),
        134: (10, 18, 0.970808084704528),
        135: (10, 84, 0.402259573213859),
        136: (3, 60, 0.812708803687275),
        137: (6, 102, 0.71608183717222),
        138: (9, 92, 0.331732205868357),
        139: (9, 29, 0.511561377938441),
        140: (9, 94, 0.397820601975295),
        141: (6, 98, 0.744196407122977),
        142: (10, 42, 0.714707313033275),
        143: (3, 80, 0.295464114053549),
        144: (7, 57, 0.182430460266773),
        145: (9, 95, 0.3859792930381),
        146: (4, 65, 0.128891270522563),
        147: (1, 80, 0.79224682963715),
        148: (6, 14, 0.766490315374168),
        149: (9, 90, 0.882223253316551),
        150: (1, 81, 0.0238015221847852),
        151: (1, 91, 0.508149382279683),
        152: (7, 100, 0.614254224718284),
        153: (9, 107, 0.0306774742325574),
        154: (7, 71, 0.539035694777522),
        155: (3, 58, 0.856913621837404),
        156: (7, 120, 0.894226573015631),
        157: (10, 13, 0.766393186266185),
        158: (7, 17, 0.18482097359591),
        159: (10, 26, 0.814865904873622),
        160: (4, 55, 0.518750529625367),
        161: (5, 10, 0.859984005517545),
        162: (2, 15, 0.814300305498911),
        163: (8, 23, 0.79895467492469),
        164: (4, 74, 0.918734508217252),
        165: (7, 78, 0.241731516193294),
        166: (1, 81, 0.934228291006097),
        167: (7, 69, 0.315356067542011),
        168: (9, 61, 0.354433643580879),
        169: (7, 64, 0.134528468664117),
        170: (2, 67, 0.719309178193325),
        171: (9, 70, 0.981341043200297),
        172: (6, 104, 0.793605685342472),
        173: (10, 114, 0.661604101426576),
        174: (1, 48, 0.992731609548244),
        175: (2, 73, 0.268539521818744),
        176: (4, 110, 0.556947122611679),
        177: (10, 105, 0.0423876196218024),
        178: (5, 101, 0.943661700001991),
        179: (3, 16, 0.382458697435881),
        180: (5, 74, 0.545447056270122),
        181: (5, 111, 0.51271442764279),
        182: (9, 95, 0.277294923397064),
        183: (5, 27, 0.203274755286765),
        184: (9, 62, 0.978304634797835),
        185: (9, 54, 0.0547541459057498),
        186: (6, 84, 0.628120277940855),
        187: (10, 28, 0.358796639173389),
        188: (2, 12, 0.628014065577625),
        189: (10, 80, 0.90987746307225),
        190: (9, 88, 0.462581815237643),
        191: (3, 55, 0.908917961937665),
        192: (8, 69, 0.164843205416476),
        193: (8, 55, 0.955871167666081),
        194: (6, 75, 0.00631716289819451),
        195: (7, 115, 0.0332873912734554),
        196: (3, 93, 0.51106674141787),
        197: (4, 86, 0.103903929294804),
        198: (4, 72, 0.551599251386407),
        199: (10, 61, 0.671091017188895),
        200: (4, 27, 0.458673625301989),
        201: (5, 37, 0.569994584607352),
        202: (10, 80, 0.550143158154637),
        203: (6, 47, 0.554794869827892),
        204: (7, 50, 0.928729279241384),
        205: (3, 110, 0.426787710467096),
        206: (9, 86, 0.0545065737340662),
        207: (7, 37, 0.937684525244906),
        208: (10, 69, 0.924299511578316),
        209: (1, 19, 0.372039712329528),
        210: (5, 17, 0.106444448070414),
        211: (9, 73, 0.776809893947919),
        212: (2, 83, 0.370460043745843),
        213: (2, 71, 0.870312801731208),
        214: (7, 71, 0.866195712684534),
        215: (7, 112, 0.245827343086187),
        216: (2, 23, 0.405219008916321),
        217: (2, 106, 0.860675435608037),
        218: (9, 18, 0.864694093714962),
        219: (7, 117, 0.399609441118316),
        220: (2, 61, 0.571933330021778),
        221: (8, 32, 0.456267330726977),
        222: (10, 107, 0.668981332071968),
        223: (9, 115, 0.879275518571938),
        224: (2, 91, 0.801481508673577),
        225: (7, 115, 0.838969882961682),
        226: (8, 120, 0.889393600430504),
        227: (10, 15, 0.316191907447551),
        228: (3, 21, 0.526652164026727),
        229: (8, 27, 0.354998088372166),
        230: (6, 77, 0.599482917759035),
        231: (4, 69, 0.319214293475692),
        232: (4, 91, 0.739652797373382),
        233: (8, 56, 0.980568820654453),
        234: (5, 64, 0.138443208628356),
        235: (7, 34, 0.825080106666395),
        236: (2, 75, 0.61506151370462),
        237: (6, 73, 0.408086859145156),
        238: (10, 56, 0.574191487599739),
        239: (7, 30, 0.0927583696254628),
        240: (2, 100, 0.346770585851837),
        241: (4, 112, 0.275756595508674),
        242: (4, 108, 0.29005055981493),
        243: (9, 99, 0.210822100982461),
        244: (3, 84, 0.280481336306188),
        245: (4, 31, 0.418014254605922),
        246: (2, 38, 0.640501448910055),
        247: (2, 71, 0.409355732084111),
        248: (8, 66, 0.605927314400618),
        249: (9, 104, 0.88106178067814),
        250: (6, 16, 0.447811791474795),
        251: (3, 98, 0.155097400147073),
        252: (9, 116, 0.894659747159314),
        253: (5, 22, 0.353454314839819),
        254: (9, 21, 0.533027954010836),
        255: (5, 95, 0.590543266511384),
        256: (3, 36, 0.994675139374091),
        257: (10, 99, 0.0881002405967991),
        258: (6, 96, 0.930453280832378),
        259: (8, 108, 0.982874254259375),
        260: (4, 31, 0.635804896742084),
        261: (9, 92, 0.00600172109316166),
        262: (8, 72, 0.691120795324362),
        263: (9, 91, 0.486906927432977),
        264: (8, 10, 0.447333870138163),
        265: (7, 107, 0.193158580239533),
        266: (1, 43, 0.800366305658184),
        267: (1, 14, 0.57489787788646),
        268: (8, 34, 0.359519483531166),
        269: (7, 66, 0.922413878239039),
        270: (1, 100, 0.396695693768668),
        271: (8, 50, 0.26358886068995),
        272: (5, 79, 0.801524276613604),
        273: (3, 29, 0.347307417423439),
        274: (2, 108, 0.371335220983936),
        275: (6, 19, 0.35677216636356),
        276: (1, 111, 0.381385988161742),
        277: (8, 37, 0.379467520693713),
        278: (7, 50, 0.532555459083433),
        279: (7, 25, 0.57781052210743),
        280: (9, 105, 0.991463816485171),
        281: (4, 99, 0.902850034219832),
        282: (1, 97, 0.15868957308744),
        283: (8, 42, 0.597648663685422),
        284: (5, 42, 0.946263700704331),
        285: (9, 112, 0.916998060900074),
        286: (7, 111, 0.98378401169666),
        287: (10, 120, 0.653857003021294),
        288: (8, 35, 0.462520540122297),
        289: (9, 107, 0.120836540409656),
        290: (2, 96, 0.34144361186174),
        291: (4, 119, 0.652010757163591),
        292: (7, 80, 0.64559092169221),
        293: (9, 85, 0.741752965682883),
        294: (7, 106, 0.265175220095087),
        295: (3, 73, 0.468141584572624),
        296: (7, 110, 0.432833478786274),
        297: (9, 14, 0.41306326587144),
        298: (6, 59, 0.503740383517802),
        299: (6, 94, 0.337388556974863),
        300: (4, 93, 0.919141353835941),
        301: (3, 61, 0.948605333544547),
        302: (10, 97, 0.921274812476435),
        303: (4, 59, 0.0641188408826159),
        304: (2, 79, 0.285676776280915),
        305: (2, 29, 0.493340418748172),
        306: (1, 52, 0.39555098387619),
        307: (7, 16, 0.281330741934919),
        308: (10, 90, 0.122770101536294),
        309: (1, 47, 0.675522880285716),
        310: (9, 113, 0.34305187801642),
        311: (5, 16, 0.404719289181593),
        312: (9, 116, 0.583713610085781),
        313: (7, 71, 0.931440463448827),
        314: (2, 30, 0.80096652451173),
        315: (3, 37, 0.0990400992667787),
        316: (5, 88, 0.215677788385649),
        317: (7, 88, 0.125756308932701),
        318: (4, 98, 0.099738470951615),
        319: (9, 53, 0.855546300579232),
        320: (7, 44, 0.975386612133274),
        321: (5, 88, 0.096429284873078),
        322: (5, 106, 0.631369096982536),
        323: (1, 19, 0.137020525757239),
        324: (4, 56, 0.863095862676152),
        325: (4, 18, 0.662963462106474),
        326: (6, 46, 0.187933828930483),
        327: (3, 19, 0.672766152254113),
        328: (8, 38, 0.487872431836438),
        329: (10, 116, 0.771172313136216),
        330: (9, 54, 0.449284293631779),
        331: (9, 22, 0.309551010583461),
        332: (10, 100, 0.0664484076065266),
        333: (5, 96, 0.494421281542448),
        334: (4, 93, 0.1841126036661),
        335: (6, 18, 0.0895547324861069),
        336: (9, 26, 0.839522930495295),
        337: (8, 51, 0.652307171583549),
        338: (4, 87, 0.18588587170577),
        339: (7, 113, 0.157540854890837),
        340: (6, 56, 0.521099203354105),
        341: (2, 86, 0.402400771671254),
        342: (3, 94, 0.21559467066303),
        343: (8, 60, 0.920402902967476),
        344: (9, 70, 0.294594653359079),
        345: (8, 65, 0.428930849111185),
        346: (5, 32, 0.841265574811435),
        347: (2, 96, 0.801410675933775),
        348: (5, 103, 0.682407793628189),
        349: (5, 66, 0.483870148479763),
        350: (10, 112, 0.959679141147557),
        351: (8, 71, 0.95574899689535),
        352: (4, 71, 0.885098271307311),
        353: (2, 119, 0.673889422198184),
        354: (4, 76, 0.957952291622556),
        355: (1, 24, 0.694572766424252),
        356: (3, 69, 0.75521392705348),
        357: (9, 42, 0.194130502120852),
        358: (2, 69, 0.213399769304519),
        359: (5, 75, 0.0263963322853297),
        360: (9, 104, 0.590722592666893),
        361: (5, 101, 0.0654867169718829),
        362: (6, 24, 0.0329287342782829),
        363: (5, 29, 0.661054440886107),
        364: (7, 47, 0.727410396774126),
        365: (7, 118, 0.170531875167016),
        366: (4, 91, 0.714802402064849),
        367: (3, 12, 0.175027612169961),
        368: (8, 68, 0.466378992716827),
        369: (1, 46, 0.187580690101544),
        370: (2, 12, 0.644102052649),
        371: (10, 71, 0.909160752708281),
        372: (7, 115, 0.659054640914426),
        373: (10, 67, 0.562987093236886),
        374: (1, 37, 0.112755364624988),
        375: (9, 58, 0.497849796754452),
        376: (5, 41, 0.339265208588607),
        377: (3, 36, 0.535642853987132),
        378: (2, 97, 0.125593100690129),
        379: (7, 42, 0.726582335603806),
        380: (2, 24, 0.825946359468138),
        381: (3, 73, 0.00714703325494226),
        382: (5, 16, 0.0290286872591493),
        383: (9, 34, 0.462937234152514),
        384: (7, 18, 0.429483975566061),
        385: (3, 22, 0.0494159622574248),
        386: (10, 88, 0.909572699235655),
        387: (9, 50, 0.597673211904114),
        388: (10, 24, 0.399945569763407),
        389: (9, 90, 0.29444184621172),
        390: (2, 82, 0.37342208982812),
        391: (10, 89, 0.661831146505925),
        392: (9, 113, 0.632314590186997),
        393: (9, 17, 0.0924243343696642),
        394: (2, 17, 0.123723278211693),
        395: (7, 55, 0.707042386754549),
        396: (8, 53, 0.50706391239328),
        397: (5, 23, 0.431431626009631),
        398: (8, 118, 0.366283654505753),
        399: (1, 37, 0.105243370873928),
        400: (3, 115, 0.234741447220809),
        401: (7, 12, 0.928804913899221),
        402: (5, 17, 0.278476749507068),
        403: (5, 90, 0.547365317857364),
        404: (9, 73, 0.96808307382069),
        405: (3, 10, 0.889418804454439),
        406: (9, 111, 0.609392738420916),
        407: (10, 24, 0.446980656331072),
        408: (9, 30, 0.465625718061025),
        409: (7, 98, 0.823957502046108),
        410: (5, 67, 0.836383042553425),
        411: (8, 27, 0.926530395496391),
        412: (6, 35, 0.937750992459573),
        413: (7, 67, 0.137107762369199),
        414: (3, 33, 0.827618259924572),
        415: (9, 108, 0.906875548592568),
        416: (7, 17, 0.0330927016051935),
        417: (6, 82, 0.335703840600001),
        418: (8, 95, 0.122183380392661),
        419: (7, 81, 0.946379212187319),
        420: (1, 37, 0.702136713958531),
        421: (2, 90, 0.181573133899848),
        422: (10, 33, 0.296783604221708),
        423: (2, 31, 0.678178685919095),
        424: (4, 47, 0.0251274221415327),
        425: (10, 51, 0.0160734157791113),
        426: (7, 118, 0.14675137873603),
        427: (3, 32, 0.0312962845237801),
        428: (10, 85, 0.843838560449464),
        429: (7, 62, 0.477117154465569),
        430: (1, 55, 0.542934199130005),
        431: (7, 66, 0.663823553288486),
        432: (5, 47, 0.0320458225164815),
        433: (4, 51, 0.235286713563157),
        434: (3, 63, 0.714831572596202),
        435: (6, 54, 0.0493740485048151),
        436: (9, 41, 0.197832815615915),
        437: (1, 75, 0.791343370781178),
        438: (9, 63, 0.718478416513045),
        439: (2, 86, 0.617088040232236),
        440: (10, 51, 0.689308646978623),
        441: (3, 85, 0.329990089838077),
        442: (5, 42, 0.18545013149688),
        443: (3, 87, 0.304557565240867),
        444: (8, 100, 0.0892265692387884),
        445: (3, 39, 0.19790096191587),
        446: (6, 56, 0.960911115346194),
        447: (6, 12, 0.59798984811604),
        448: (9, 29, 0.868827386637908),
        449: (1, 97, 0.184044554397919),
        450: (2, 115, 0.557905157823496),
        451: (3, 108, 0.37353272530144),
        452: (1, 116, 0.207595153919997),
        453: (7, 54, 0.626055580289893),
        454: (2, 13, 0.209054208306857),
        455: (2, 13, 0.621003211831816),
        456: (6, 111, 0.297075036714183),
        457: (3, 106, 0.271091296912925),
        458: (3, 17, 0.59484405668387),
        459: (5, 30, 0.29391312368828),
        460: (3, 66, 0.983161442827541),
        461: (4, 27, 0.0250804287605793),
        462: (7, 78, 0.568313242894348),
        463: (7, 76, 0.145683275587938),
        464: (9, 39, 0.509084731522826),
        465: (7, 77, 0.953458000757391),
        466: (1, 89, 0.503637237821551),
        467: (1, 38, 0.153505037237961),
        468: (2, 96, 0.457563121792384),
        469: (6, 39, 0.115788719891071),
        470: (9, 107, 0.515479228061616),
        471: (7, 109, 0.0522416125468593),
        472: (9, 76, 0.896452331704027),
        473: (2, 63, 0.303930163899511),
        474: (10, 89, 0.421194152211981),
        475: (5, 101, 0.160500102429803),
        476: (4, 112, 0.0785112405021324),
        477: (1, 44, 0.269340098943267),
        478: (2, 27, 0.0160856503292),
        479: (10, 61, 0.974535729037195),
        480: (5, 49, 0.897787895681464),
        481: (10, 60, 0.547427028072764),
        482: (1, 27, 0.217010440937332),
        483: (1, 53, 0.818435042924797),
        484: (5, 48, 0.449442515545408),
        485: (9, 106, 0.33092481125844),
        486: (6, 100, 0.113552182344067),
        487: (10, 86, 0.0420728977387003),
        488: (8, 19, 0.952279791330306),
        489: (3, 83, 0.760817898026949),
        490: (9, 71, 0.591628592107734),
        491: (7, 115, 0.539518242036608),
        492: (10, 46, 0.993079089392425),
        493: (6, 68, 0.645938370880844),
        494: (10, 53, 0.166695150301364),
        495: (3, 37, 0.219285924607448),
        496: (1, 10, 0.123358262237618),
        497: (1, 46, 0.105430758088899),
        498: (6, 20, 0.981656454605),
        499: (1, 48, 0.850807204562983),
        500: (8, 109, 0.473745306140199),
        501: (3, 111, 0.235870295324749),
        502: (3, 111, 0.475123906098941),
        503: (5, 80, 0.65624610072457),
        504: (3, 33, 0.341930353669979),
        505: (2, 108, 0.651659614174441),
        506: (6, 82, 0.229720673555084),
        507: (4, 85, 0.971302475653179),
        508: (4, 67, 0.21231344250385),
        509: (4, 16, 0.710081818353059),
        510: (6, 115, 0.140989364938128),
        511: (3, 47, 0.284700718673402),
        512: (9, 44, 0.512108565009919),
        513: (8, 49, 0.136530172776772),
        514: (4, 20, 0.045633702019568),
        515: (4, 80, 0.879323062092669),
        516: (9, 25, 0.318789248229534),
        517: (9, 111, 0.689552935488436),
        518: (6, 33, 0.857760297002488),
        519: (3, 14, 0.131917167553224),
        520: (8, 99, 0.130963046717179),
        521: (9, 53, 0.588601403933828),
        522: (2, 70, 0.203489515579275),
        523: (6, 27, 0.045362141292591),
        524: (10, 50, 0.942432440455937),
        525: (5, 107, 0.260319018510252),
        526: (5, 109, 0.82229525975542),
        527: (9, 26, 0.214532527712325),
        528: (3, 59, 0.164537818139258),
        529: (3, 32, 0.554577828570878),
        530: (3, 86, 0.111064878165037),
        531: (2, 102, 0.634644274824867),
        532: (8, 111, 0.752337670216784),
        533: (5, 92, 0.758653195708132),
        534: (6, 14, 0.657265318497091),
        535: (6, 113, 0.232664642791089),
        536: (3, 28, 0.0089124653881224),
        537: (6, 29, 0.380528725261271),
        538: (7, 44, 0.656877475575587),
        539: (9, 32, 0.876046785592276),
        540: (4, 77, 0.361366686027176),
        541: (6, 113, 0.000471306256019766),
        542: (7, 116, 0.349756943836369),
        543: (7, 53, 0.541027715043753),
        544: (3, 62, 0.713279582930487),
        545: (7, 75, 0.121524943555512),
        546: (10, 91, 0.100480034123935),
        547: (4, 54, 0.572655982985196),
        548: (2, 89, 0.73274259694959),
        549: (2, 24, 0.100678505788083),
        550: (2, 36, 0.0413754307836681),
        551: (6, 13, 0.0569350631190667),
        552: (9, 16, 0.35187547036598),
        553: (3, 16, 0.569851615638287),
        554: (8, 15, 0.934920936282601),
        555: (7, 49, 0.679725780633028),
        556: (7, 117, 0.668603360462751),
        557: (1, 10, 0.140243719735667),
        558: (5, 96, 0.819132794512055),
        559: (4, 51, 0.591478558732796),
        560: (5, 91, 0.231194603455882),
        561: (9, 30, 0.501242228376657),
        562: (5, 104, 0.375271108848963),
        563: (3, 82, 0.141059610072171),
        564: (7, 91, 0.706434778092103),
        565: (7, 14, 0.912632689595695),
        566: (7, 24, 0.127656032278934),
        567: (7, 75, 0.853234211904604),
        568: (1, 80, 0.72868088813161),
        569: (4, 120, 0.225059224343297),
        570: (5, 75, 0.275711950064542),
        571: (10, 77, 0.290235257309694),
        572: (3, 23, 0.307441934501265),
        573: (4, 44, 0.67441937248951),
        574: (7, 14, 0.862139989268698),
        575: (7, 76, 0.826368986443428),
        576: (5, 118, 0.284111595851204),
        577: (9, 80, 0.584257778280582),
        578: (2, 54, 0.978488351679807),
        579: (3, 66, 0.113206587537163),
        580: (3, 12, 0.220830326680588),
        581: (5, 74, 0.362381506117347),
        582: (4, 29, 0.769518427226572),
        583: (10, 49, 0.992355707325794),
        584: (6, 91, 0.851690236535969),
        585: (1, 77, 0.875549388728946),
        586: (9, 69, 0.23009902423091),
        587: (7, 38, 0.0821298292452608),
        588: (4, 15, 0.330335123448523),
        589: (6, 93, 0.505563435184246),
        590: (4, 27, 0.305781338254713),
        591: (4, 22, 0.61209358840783),
        592: (3, 86, 0.493428798262079),
        593: (2, 15, 0.0582544098560979),
        594: (8, 85, 0.65281154175745),
        595: (3, 41, 0.0295914683429829),
        596: (9, 65, 0.586398318351036),
        597: (5, 83, 0.247682077504052),
        598: (8, 73, 0.342627033221947),
        599: (4, 54, 0.195173911300932),
        600: (7, 12, 0.915256758286192),
        601: (7, 115, 0.669984596258953),
        602: (9, 96, 0.792440175451531),
        603: (6, 71, 0.667257045439558),
        604: (8, 11, 0.0481795194440872),
        605: (10, 13, 0.159164462218113),
        606: (6, 13, 0.532011178413695),
        607: (8, 70, 0.97511556710839),
        608: (7, 45, 0.2991188927398),
        609: (2, 25, 0.764774653311145),
        610: (2, 14, 0.725708022387616),
        611: (7, 55, 0.845714456305286),
        612: (1, 60, 0.184267832238795),
        613: (5, 16, 0.758683007089117),
        614: (6, 107, 0.928291566282704),
        615: (8, 36, 0.226613206962097),
        616: (4, 117, 0.905692907553467),
        617: (4, 48, 0.152109299055011),
        618: (4, 67, 0.213375499315465),
        619: (2, 49, 0.605224910256459),
        620: (1, 83, 0.515264736367443),
        621: (4, 79, 0.0637706945625405),
        622: (1, 81, 0.347815017960371),
        623: (9, 40, 0.8635458183885),
        624: (7, 99, 0.180825242089656),
        625: (9, 112, 0.329669534573681),
        626: (4, 48, 0.363805798386335),
        627: (9, 113, 0.272267065151345),
        628: (4, 62, 0.19080127312929),
        629: (4, 107, 0.221658941730457),
        630: (3, 50, 0.411888494700143),
        631: (6, 90, 0.1665487845649),
        632: (5, 88, 0.723359013659177),
        633: (8, 59, 0.864087686042602),
        634: (2, 26, 0.57969030219448),
        635: (2, 20, 0.120209237880931),
        636: (2, 55, 0.719562216575032),
        637: (5, 41, 0.861600908457437),
        638: (1, 64, 0.793619303918634),
        639: (4, 107, 0.189488486300076),
        640: (2, 81, 0.919630611588899),
        641: (10, 88, 0.876901127572111),
        642: (10, 113, 0.453006923903735),
        643: (8, 70, 0.32677758701116),
        644: (6, 32, 0.0409061568904949),
        645: (5, 81, 0.478976147044426),
        646: (7, 108, 0.451109595954372),
        647: (3, 77, 0.898822257296677),
        648: (3, 51, 0.524546592776928),
        649: (6, 67, 0.494087666754737),
        650: (1, 32, 0.63813737575379),
        651: (6, 98, 0.414139438538604),
        652: (8, 63, 0.310735583249868),
        653: (6, 118, 0.782779179094709),
        654: (10, 91, 0.347021922838993),
        655: (8, 112, 0.575478989627254),
        656: (3, 77, 0.87689370727307),
        657: (6, 17, 0.0148743409533795),
        658: (8, 92, 0.372774984502518),
        659: (4, 81, 0.615923746548427),
        660: (8, 63, 0.190085892249329),
        661: (6, 62, 0.679047381816558),
        662: (2, 91, 0.25541313947151),
        663: (3, 120, 0.585211217413161),
        664: (10, 57, 0.172590420050755),
        665: (10, 106, 0.434098117236592),
        666: (5, 69, 0.930234064697507),
        667: (7, 74, 0.953736330793404),
        668: (6, 33, 0.709646794305286),
        669: (6, 14, 0.984318004633441),
        670: (10, 69, 0.175840762390827),
        671: (9, 88, 0.820393873042069),
        672: (10, 15, 0.101789929134104),
        673: (5, 50, 0.147098782565717),
        674: (5, 10, 0.93909812763557),
        675: (1, 36, 0.238821571609221),
        676: (5, 32, 0.0899672525368046),
        677: (3, 57, 0.529144915376102),
        678: (7, 51, 0.550245233992505),
        679: (1, 90, 0.416258825229369),
        680: (5, 62, 0.413233458376767),
        681: (3, 16, 0.893922977692842),
        682: (6, 44, 0.709617587233583),
        683: (1, 43, 0.329538601742878),
        684: (5, 73, 0.705140570165555),
        685: (7, 71, 0.584028358162103),
        686: (5, 57, 0.141401627267334),
        687: (1, 47, 0.361116367913313),
        688: (5, 58, 0.0507624206173213),
        689: (6, 83, 0.818206744159186),
        690: (9, 24, 0.676847079651671),
        691: (2, 31, 0.995291995680531),
        692: (3, 57, 0.13830672121871),
        693: (10, 92, 0.178257340871594),
        694: (9, 39, 0.198452302041206),
        695: (5, 90, 0.729661244175799),
        696: (6, 36, 0.276574556080816),
        697: (4, 30, 0.668116922400287),
        698: (2, 40, 0.316359967586322),
        699: (6, 49, 0.859144344711544),
        700: (9, 98, 0.363015065474434)
    }

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
    dp_idp = DP_IDP(r_big)
    print(dp_idp.score)
    print(f"temps: {time.time()-startTime}")




