#!/usr/bin/ python

class MBR():
    """Minimum Bounding region Structure"""
    def __init__(self, minDim=[], maxDim=[]):
        self.minDim = minDim
        self.maxDim = maxDim

    def __repr__(self):
        return f"""
    minDim:{self.minDim}
    maxDim:{self.maxDim}
   
    """

    '''
    Area of MBR
    '''
    def area(self):
        areaCovered = 1
        for i in range(0, len(self.minDim)):
            areaCovered *= (self.maxDim[i] - self.minDim[i])
        return areaCovered

    '''
    return combined MBR of self with another mbr
    '''
    def combine(self, mbr):
        minDim = []
        maxDim = []
        # get the minimum of minimum and maximum of maximum
        for i in range(0, len(self.minDim)):
            minDim.append(min(self.minDim[i], mbr.minDim[i]))
            maxDim.append(max(self.maxDim[i], mbr.maxDim[i]))
       
        combinedMBR = MBR(minDim, maxDim)
        return combinedMBR


    '''
    gets the pripority for the mbr
    '''
    def priority(self):
        value = 0
        for val in self.minDim:
            value += val
        return value

    '''
    returns dominate relationship of self and a mbr 
    '''
    def dominates(self, mbr):
        dims = len(self.maxDim)
        for dim in range(0, dims):
            # check whether lower part of mbr with respect to upper part of self.mbr
            if self.maxDim[dim] > mbr.minDim[dim]:
                return False    
        return True