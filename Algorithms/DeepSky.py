"""
=======
DeepSky
=======
Entrée :
	La relation r.
	Un entier k.
Sortie :
    Ldx top-k tuples/points avec les meilleurs scores topk.

topk <- nouveau tableau
tot <- 0 // Nombre total de résultats calculés
rl = r // Niveau courant
Tant que tot >= k and !rl
    s <- CoSky(rl)
	n <- taille(s) - 1
	tot <- tot + taille(s)
	Si tot < k
        topk <- topk U s
		rl <- rl \ s
	Sinon
	    Si tot >= k
		    Pour i de 0 à k
		        topk[i] <- s[i]
			retourner topk

retourner topk
"""

"""
r = [
    (1, 5, 20, 1 / 70),
    (2, 4, 60, 1 / 50),
    (3, 5, 30, 1 / 60),
    (4, 1, 80, 1 / 60),
    (5, 5, 90, 1 / 40),
    (6, 9, 30, 1 / 50),
    (7, 7, 80, 1 / 40),
    (8, 9, 90, 1 / 30)
]
"""


r_next = {
    1:(5, 20, 1 / 70),
    2:(4, 60, 1 / 50),
    4:(1, 80, 1 / 60)
}

r = {
    1:(5, 20, 1 / 70),
    2:(4, 60, 1 / 50),
    3:(5, 30, 1 / 60),
    4:(1, 80, 1 / 60),
    5:(5, 90, 1 / 40),
    6:(9, 30, 1 / 50),
    7:(7, 80, 1 / 40),
    8:(9, 90, 1 / 30)
}


k = 1

"""
def DeepSky(r,k):
    topK={}
    tot=0
    rl=r

    while tot<k and rl!={}:
        print(100*"*")
        print("rl:\n",'\n'.join([str(x) for x in rl.items()]))
        print()
        #s=Cosky(rl).relations
        s = r_next
        tot+=len(s)

        if tot<=k:
            print(100*"-")
            topK.update(s)
            print("topK:\n",'\n'.join([str(x) for x in topK.items()]))
            print()
            print("s:\n",'\n'.join([str(x) for x in s.items()]))
            print()
            #print(f"rl:{rl}")

            rl = {k:v for k,v in rl.items() if k not in s.keys()}
        else:
            print(100 * "|")
            topK.update({x:s[x] for x in list(s.keys())[:k]})
            print("topK:\n", '\n'.join([str(x) for x in topK.items()]))
            print()


            return topK
    return topK

res = DeepSky(r,k)
print(res)
"""



def DeepSky(r,k):
    topK={}
    tot=0
    rl=r
    while tot<k and rl!={}:
        #s=Cosky(rl).relations
        s = r_next
        tot+=len(s)
        if tot<=k:
            topK.update(s)
            rl = {k:v for k,v in rl.items() if k not in s.keys()}
        else:
            topK.update({x:s[x] for x in list(s.keys())[:k]})
            return topK
    return topK

res = DeepSky(r,k)
print(res)