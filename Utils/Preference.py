from enum import Enum

class Preference(Enum):
    MIN = "MIN"
    MAX = "MAX"

    def reverse(self):
        # Flip the current preference
        return Preference.MAX if self == Preference.MIN else Preference.MIN

    @staticmethod
    def unify(preferences, mode="auto"):
        # Unify preferences based on mode: 'min', 'max', or 'auto' (majority-based)
        if not preferences:
            return []

        if mode in ("min", "max"):
            target = Preference.MIN if mode == "min" else Preference.MAX
        elif mode == "auto":
            count_min = preferences.count(Preference.MIN)
            count_max = preferences.count(Preference.MAX)
            target = Preference.MIN if count_min >= count_max else Preference.MAX
        else:
            raise ValueError(f"Unknown unification mode: {mode}")

        return [target] * len(preferences)

    @staticmethod
    def resolve(preferences, force_mode=None, default_mode="min"):
        # If force_mode is set, apply it directly. Otherwise use auto mode with fallback
        if force_mode in ("min", "max"):
            return Preference.unify(preferences, mode=force_mode)

        count_min = preferences.count(Preference.MIN)
        count_max = preferences.count(Preference.MAX)

        if count_min > count_max:
            return [Preference.MIN] * len(preferences)
        elif count_max > count_min:
            return [Preference.MAX] * len(preferences)
        else:
            return Preference.unify(preferences, mode=default_mode)

    @staticmethod
    def unifyTuple(prefTuple, mode="auto"):
        # Same as unify, but returns a tuple instead of a list
        return tuple(Preference.unify(list(prefTuple), mode))
