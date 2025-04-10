import math
import bisect
from queue import PriorityQueue



from Algorithms.BbsCosky import BBS_COSKY
from Utils.DisplayHelpers import beauty_print


class SkyIR:
    """
    Algorithm about SkyIR
    """

    def __init__(self, r):
        self.r=r


    def calculSkylineEtNbDominants(self):
        """

        :return:
        """
        keys=list(self.r.keys())
        gamma={k:0 for k in self.r.keys()}
        gamma_inverse={k:0 for k in self.r.keys()}
        s={}
        spTot=0
        r_keys = list(self.r.keys())
        col_len = len(self.r.get(r_keys[0]))
        for row_index in keys:
            for col_index in keys:
                if row_index != col_index:
                    sup = True
                    for k in range(col_len):
                        if self.r[col_index][k] > self.r[row_index][k]:
                            sup = False
                            break
                    if sup:
                        gamma[col_index]+=1
                        gamma_inverse[row_index]+=1
        for row_index in keys:
            if gamma_inverse[row_index] == 0:
                for k in range(col_len):
                    if s.get(row_index):
                        s[row_index].append(self.r[row_index][k])
                    else:
                        s[row_index] = [self.r[row_index][k]]
                spTot += 1
        return s, gamma, spTot


    def upperBound(self, s, poi, minIdp, layer, pending, gamma):
        vidp=[]
        vpnd=[]
        ub=0
        n=len(self.r)
        m=len(s)
        vidp.append(minIdp)
        vpnd.append(pending)
        gamma = {k:v for k,v in sorted(gamma.items(), key=lambda item: item[1], reverse=True)}
        #beauty_print("gamma [AFTER]", gamma)
        for sp in s:
            if sp != poi:
                surplus = pending + gamma[sp]
                """
                if gamma[sp]>n:
                    surplus+=gamma[sp]
                """
                print("surplus", surplus)
                if surplus>0:
                    vpnd[-1]-=surplus
                    vpnd.append(surplus)
                    vidp.append(vidp[-1]+1)
        l=len(vidp)
        for i in range(l):
            ub+=1/(layer+1)*vpnd[i]*math.log(m/vidp[i])
            #beauty_print(f"vpnd[{i}]", vpnd[i])
            #beauty_print(f"math.log(m/vidp[{i}])", math.log(m/vidp[i]))
        return ub







    def nextLayer(self, poi, rLayer, sLayer, layer, minIdp):
        minIdpInit=minIdp.copy()

        sNextLayer = {key: sLayer[key] for key in sLayer if poi != key}
        rLayer = {key: rLayer[key] for key in rLayer if key not in sNextLayer.keys()}

        bbs = BBS_COSKY(rLayer, poi, layer, minIdp)
        sLayer = {k: list(v) for k, v in bbs.skyline.items()}
        if (len(sLayer) == 1):
            return rLayer, sLayer, bbs.lm, bbs.minIdp, bbs.see
        else:
            return rLayer, sLayer, {}, minIdpInit, 0





    def updateScore(self, poi, lm, minIdp, spTot):
        score=0
        for j in lm[poi].keys():
            """
            beauty_print("lm", lm)
            beauty_print("poi", poi)
            beauty_print("j", j)
            beauty_print("lm[poi][j]", lm[poi][j])
            beauty_print("spTot", spTot)
            print("minIdp", minIdp)
            """
            score += 1 / lm[poi][j] * math.log10(spTot / minIdp[j])
        return score


    def insererTrie(self, topkLbl, topk, poi, score):
        inserted = False
        # Insertion tout en maintenant la liste triée
        #print("insererTrie->topk", topk)
        #print("insererTrie->score", score)
        if len(topk) == 0:
            topkLbl.insert(0, poi)
            topk.insert(0, score)
            inserted = True
        else:
            lo = bisect.bisect_left(topk, score)
            #print("insererTrie->lo", lo)
            if lo > 0:
                topkLbl.insert(lo, poi)
                topk.insert(lo, score)
                inserted = True
        return topkLbl, topk, inserted


    def skyIR(self, k):
        s, gamma, spTot = self.calculSkylineEtNbDominants()
        lm={}
        pending={}
        fileDePriorite=PriorityQueue()
        minIdp = {}
        for sp in s.keys():
            spg=gamma[sp]
            lm[sp]={}
            pending[sp]=spg
            fileDePriorite.put((spg, sp))


        rLayer = self.r
        sLayer = s
        layer = 1
        topkLbl=[]
        topK=[]
        score=[0]*spTot
        kScore=0

        while not fileDePriorite.empty():
            poi=fileDePriorite.get_nowait()[1]
            #"""
            if minIdp.get(poi):
                val=self.upperBound(s, poi, minIdp[poi], layer, pending[poi], gamma)
                if val and val<kScore:
                    continue
            #"""
            if pending[poi]>0:
                layer+=1
                """
                beauty_print(f"poi", poi)
                beauty_print(f"rLayer before", rLayer)
                beauty_print(f"sLayer before", sLayer)
                rLayer,sLayer, lm_nextLayer, minIdp, see= self.nextLayer(poi, rLayer, sLayer, layer, minIdp)
                beauty_print(f"rLayer", rLayer)
                beauty_print(f"sLayer", sLayer)
                beauty_print(f"lm_nextLayer", lm_nextLayer)
                beauty_print(f"LM[{poi}] Before ", lm[poi])
                lm[poi].update(lm_nextLayer)
                beauty_print(f"LM[{poi}] After ", lm[poi])
                beauty_print(f"pending[{poi}] Before ", pending[poi])
                print("see",see)
                pending[poi] -= see
                beauty_print(f"pending[{poi}] After ", pending[poi])
                """
                rLayer, sLayer, lm_nextLayer, minIdp, see = self.nextLayer(poi, rLayer, sLayer, layer, minIdp)
                lm[poi].update(lm_nextLayer)
                pending[poi] -= see
                score[poi]=self.updateScore(poi, lm, minIdp, spTot)
                inserted=False
                if pending[poi]==0:
                    topkLbl, topK, inserted = self.insererTrie(topkLbl, topK, poi, score[poi])
                #if not inserted and pending[poi]==0:
                if pending[poi]==0:
                    rLayer = self.r
                    sLayer = s
                    layer = 1
                    continue

                if len(topK)>=k and topK[-k]>kScore:
                    kScore=topK[-k]
            if pending[poi] > 0:
                fileDePriorite.put((gamma[poi], poi))
        return topK








if __name__ == '__main__':



    r_big = {
        1: (5, 20, 0.014285714),
        2: (4, 60, 0.02),
        3: (5, 30, 0.016666667),
        4: (1, 80, 0.016666667),
        5: (5, 90, 0.025),
        6: (9, 30, 0.02),
        7: (7, 80, 0.025),
        8: (9, 90, 0.033333333)
    }
    sky_ir = SkyIR(r_big)
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------calculSkylineEtNbDominants-------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    is_debug=False
    if is_debug:
        minIdp = {}
        s,gamma, spTot=sky_ir.calculSkylineEtNbDominants()
        beauty_print("s",s)
        beauty_print("gamma",gamma)
        beauty_print("spTot",spTot)



    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------nextLayer----------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if is_debug:
        sLayer, lm, minIdp, see = sky_ir.nextLayer(2, sky_ir.r, s, 2, minIdp)

        beauty_print("sLayer", sLayer)
        beauty_print("lm", lm)
        beauty_print("minIdp", minIdp)
        beauty_print("see", see)

    # ------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------upperBound---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if is_debug:
        ub=sky_ir.upperBound(s, 5, minIdp[5], 5, 1, gamma)
        beauty_print("ub", ub)


    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------updateScore---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if is_debug:
        lm = {
            2:{
                5:2,
                7:2,
                8:2
            }
        }
        score = sky_ir.updateScore(2, lm, minIdp, 3)

        beauty_print("score", score)

    # ------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------insererTrie------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if is_debug:
        topkLbl=list(range(1,6))
        topK = [10, 20, 30, 40, 50]

        for poi, score in [(9,35), (8,5)]:
            topkLbl, topk, inserted=sky_ir.insererTrie(topkLbl, topK,poi, score)

            beauty_print("topkLbl", topkLbl)
            beauty_print("topk", topk)
            beauty_print("inserted", inserted)

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------skyIR----------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    topK=sky_ir.skyIR(3)
    beauty_print("topK", topK)









