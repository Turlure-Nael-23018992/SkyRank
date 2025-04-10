#!/usr/bin/python

class MBR():
    """Minimum Bounding Region Structure (MBR) - Represents a minimum bounding rectangle in multidimensional space."""

    def __init__(self, minDim=[], maxDim=[]):
        """Initializes the MBR with minimum and maximum coordinates in each dimension."""
        self.minDim = minDim  # List of minimum coordinates (e.g., xmin, ymin, ...)
        self.maxDim = maxDim  # List of maximum coordinates (e.g., xmax, ymax, ...)

    def __repr__(self):
        """Textual representation of the MBR with its min and max coordinates."""
        return f"""
            minDim:{self.minDim}
            maxDim:{self.maxDim}
            """

    def area(self):
        """Calculates the area or volume of the MBR (based on number of dimensions)."""
        areaCovered = 1
        for i in range(0, len(self.minDim)):
            areaCovered *= (self.maxDim[i] - self.minDim[i])  # Multiply differences in each dimension
        return areaCovered

    def combine(self, mbr):
        """Merges two MBRs into one by taking the smallest minimums and largest maximums."""
        minDim = []
        maxDim = []
        # Calculate smallest and largest values
        for i in range(0, len(self.minDim)):
            minDim.append(min(self.minDim[i], mbr.minDim[i]))  # Select smallest
            maxDim.append(max(self.maxDim[i], mbr.maxDim[i]))  # Select largest

        combinedMBR = MBR(minDim, maxDim)  # Create combined MBR
        return combinedMBR

    def priority(self):
        """Calculates the MBR's priority based on the sum of its minimum coordinates."""
        value = 0
        for val in self.minDim:
            value += val  # Sum values of minimum coordinates
        return value

    def dominates(self, mbr):
        """Checks if the current MBR dominates another MBR by comparing their min/max coordinates."""
        dims = len(self.maxDim)
        for dim in range(0, dims):
            # Check if self dominates mbr
            if self.maxDim[dim] > mbr.minDim[dim]:
                return False  # self does not dominate mbr
        return True  # self dominates mbr