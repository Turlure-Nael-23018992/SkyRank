from enum import Enum

class Preference(Enum):
    """
    Enum class to define preference types for the RankSky algorithm.
    Each preference determines whether an attribute should be minimized or maximized.
    """

    MIN = 1
    """Preference to minimize the value."""

    MAX = 2
    """Preference to maximize the value."""