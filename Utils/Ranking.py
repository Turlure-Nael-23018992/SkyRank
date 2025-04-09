

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