import math
import bisect
from queue import PriorityQueue

from Algorithms.BbsCosky import BbsCosky
from Utils.DisplayHelpers import beauty_print
from Utils.DataModifier.JsonUtils import readJson
from Utils.TimerUtils import TimeCalc


class SkyIR:
    """
    Implementation of the SkyIR (Skyline-based Information Retrieval) algorithm.

    This algorithm ranks items based on their skyline dominance and scoring metrics.
    """

    def __init__(self, r):
        """
        Initializes the SkyIR algorithm with a dataset.

        SkyIR (Skyline-based Information Retrieval) is designed to find and rank
        representative points from a dataset based on their dominance levels.

        Args:
            r (dict): The dataset. A dictionary where keys are point IDs and 
                     values are lists or tuples of numerical coordinates.
        """
        time1 = TimeCalc(100, "SkyIR")
        self.r = r
        time1.stop()
        self.time = time1.execution_time


    def calculSkylineEtNbDominants(self):
        """
        Initial pass: Identifies the first layer of skyline points.

        A skyline point is one that is not "dominated" by any other point.
        A point A dominates point B if A is at least as good as B in all 
        dimensions and strictly better in at least one.

        Returns:
            tuple: (s, gamma, spTot)
                - s (dict): Coordinates of points in the first skyline layer.
                - gamma (dict): Maps each point ID to the number of points it dominates.
                - spTot (int): Total count of points in the first skyline.
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
                        s[row_index]=[self.r[row_index][k]]
                spTot += 1

        return s, gamma, spTot


    def upperBound(self, s, poi, minIdp, layer, pending, gamma):
        """
        Calculates an optimistic 'upper bound' score for a Point of Interest (POI).

        Used for pruning: if even the best possible score (upper bound) for this
        point is lower than our current Top-K scores, we can stop processing it.

        Args:
            s (dict): Skyline points.
            poi (int/str): The point ID being evaluated.
            minIdp (dict): Current Influence-Dominance Power values.
            layer (int): Depth of processing.
            pending (dict): Remaining dominance counts for points.
            gamma (dict): Initial dominance counts.

        Returns:
            float: The maximum potential score this point could achieve.
        """
        #vidp=[]
        #vpnd=[]
        ub=0
        n=len(self.r)
        m=len(s)
        #vidp.append(minIdp)
        vidp = [v for v in minIdp.values()]
        #vpnd.append(pending)
        vpnd = [v for v in pending.values()]
        gamma = {k:v for k,v in sorted(gamma.items(), key=lambda item: item[1], reverse=True)}
        #beauty_print("gamma [AFTER]", gamma)
        for sp in s:
            if sp != poi:
                surplus = pending[poi] + gamma[sp]
                """
                if gamma[sp]>n:
                    surplus+=gamma[sp]
                """
                #print("surplus", surplus)
                if surplus>0:
                    vpnd[-1]-=surplus
                    vpnd.append(surplus)
                    if len(vidp):
                        vidp.append(vidp[-1]+1)

        #print(len(vpnd))
        l=min(len(vpnd), len(vidp))
        for i in range(l):
            v1=1/(layer+1)
            v2=m/vidp[i]
            v3=vpnd[i]
            ub+=v1*v3*math.log(v2)

            #beauty_print(f"vpnd[{i}]", vpnd[i])
            #beauty_print(f"math.log(m/vidp[{i}])", math.log(m/vidp[i]))

        return ub







    def nextLayer(self, poi, rLayer, sLayer, layer, minIdp):
        """
        Peels back a layer of dominance to find points 'hidden' behind the POI.

        Args:
            poi (int/str): The point being processed.
            rLayer (dict): Data candidates for the next layer.
            sLayer (dict): Current skyline layer.
            layer (int): Current recursion/iteration depth.
            minIdp (dict): Running minimum IDP status.

        Returns:
            tuple: Updated (rLayer, sLayer, lm, minIdp, see)
        """
        minIdpInit = minIdp.copy()

        sNextLayer = {key: sLayer[key] for key in sLayer if poi != key}
        rLayer = {key: rLayer[key] for key in rLayer if key not in sNextLayer.keys()}

        bbs = BbsCosky(rLayer, poi, layer, minIdp)
        sLayer = {k: list(v) for k, v in bbs.skyline.items()}
        if len(sLayer) == 1:
            return rLayer, sLayer, bbs.lm, bbs.minIdp, bbs.see
        else:
            return rLayer, sLayer, {}, minIdpInit, 0


    def updateScore(self, poi, lm, minIdp, spTot):
        """
        Computes the ranking score for a point.

        The score balances how many points it dominates (influence) vs how
        deeply those points are dominated (rank depth).

        Args:
            poi (int/str): Point ID.
            lm (dict): Dominance level metrics.
            minIdp (dict): Influence-Dominance Power values.
            spTot (int): Total skyline size.

        Returns:
            float: The computed score for ranking.
        """
        score=0
        # Iterate through points dominated by 'poi' and sum their contributions
        for j in lm[poi].keys():
            # Contribution formula: inverse of level * log of (total skyline / influence power)
            score += 1 / lm[poi][j] * math.log10(spTot / minIdp[j])
        return score


    def insererTrie(self, topkLbl, topk, poi, score):
        """
        Inserts a new score into the top-K list if it's high enough.

        Args:
            topkLbl (list): Current top-K point IDs.
            topk (list): Current top-K scores.
            poi (int/str): Potential new point ID.
            score (float): Score of the new point.

        Returns:
            tuple: (topkLbl, topk, inserted)
        """
        inserted=False
        # Insertion tout en maintenant la liste triée
        '''
        print("insererTrie->topk", topk)
        print("insererTrie->score", score)
        '''
        if len(topk) == 0:
            topkLbl.insert(0, poi)
            topk.insert(0, score)
            inserted = True
        else:
            lo = bisect.bisect_left(topk, score)
            '''
            print("insererTrie->lo", lo)
            '''
            if lo>0:
                topkLbl.insert(lo, poi)
                topk.insert(lo, score)
                inserted=True

        return topkLbl, topk, inserted


    def skyIR(self, k):
        """
        Main execution loop for the SkyIR algorithm.

        Runs iteratively to find the best 'k' representative points by 
        layering the dominance relationships.

        Args:
            k (int): Number of representative items to return.

        Returns:
            list: Top-K items as a list of tuples (ID, score).
        """
        time2 = TimeCalc(100, "SkyIR")
        # Step 1: Initial skyline layer
        s, gamma, spTot = self.calculSkylineEtNbDominants()
        lm={}
        pending={}
        fileDePriorite=PriorityQueue()
        minIdp = {}

        # Initialize priority queue based on initial dominance counts (gamma)
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
        score={k:0 for k in sLayer.keys()}
        kScore=0

        # Iteratively process points in the priority queue
        while not fileDePriorite.empty():
            poi=fileDePriorite.get()[1]
            
            # Use upper bound pruning to skip points that cannot enter Top-K
            val=self.upperBound(s, poi, minIdp, layer, pending, gamma)
            
            if pending[poi]>0:
                layer+=1
                #print("************************************************************")
                #print(f"poi[{poi}] : ", pending[poi], " - layer : ", layer)
                #print(f"rLayer : {poi} :", rLayer)
                #beauty_print(f"rLayer Before", rLayer)
                #beauty_print(f"sLayer Before", sLayer)
                #beauty_print(f"minIdp Before", minIdp)
                rLayer, sLayer, lm_nextLayer, minIdp, see= self.nextLayer(poi, rLayer, sLayer, layer, minIdp)
                #beauty_print(f"minIdp After", minIdp)
                #beauty_print(f"rLayer After", rLayer)
                #beauty_print(f"sLayer After", sLayer)
                #beauty_print(f"lm_nextLayer", lm_nextLayer)
                #beauty_print(f"LM[{poi}] Before ", lm[poi])
                lm[poi].update(lm_nextLayer)
                #beauty_print(f"LM[{poi}] After ", lm[poi])
                #print(f"pending[{poi}] Before ", pending[poi])
                #print("see",see)
                pending[poi] -= see
                #print(f"pending[{poi}] After ", pending[poi])
                score[poi]=self.updateScore(poi, lm, minIdp, spTot)
                #beauty_print(f"score[{poi}]", score[poi])

                inserted = False
                if pending[poi] == 0:
                    #beauty_print("topK Before", topK)
                    topkLbl, topK, inserted = self.insererTrie(topkLbl, topK, poi, score[poi])
                    #beauty_print("topK After", topK)

                #print("inserted :", inserted, f" - pending[{poi}] :", pending[poi])
                #if !inserted and pending[poi]==0:
                if pending[poi]==0:
                    #print("------------------------------------------------------------")
                    rLayer = self.r
                    sLayer = s
                    layer = 1
                    continue
                #print("============================================================")
                #print(f"k", k)
                #print(f"len(topK)", len(topK))
                #print(f"kScore", kScore)
                if len(topK)>=k and topK[-k]>kScore:
                    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    kScore=topK[-k]
                    #print("kScore", kScore)

                """
                if layer == 6:
                    break
                """
            if pending[poi] > 0:
                fileDePriorite.put((gamma[poi], poi))
        
        good_K=min(k, len(topK))
        time2.stop()
        self.time = time2.execution_time + self.time
        # self.result = topK[-good_K:]
        # return topK[-good_K:]
        self.result = [(topkLbl[i-1], topK[i-1]) for i in range(len(topK)-good_K+1, len(topK)+1)]
        return self.result








if __name__ == '__main__':



    r_big = readJson("Datas/RTuples8.json")
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

    topK=sky_ir.skyIR(10)
    beauty_print("topK", topK)









