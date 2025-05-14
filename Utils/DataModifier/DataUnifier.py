from Utils.DataTypes.DictObject import DictObject
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DbObject import DbObject
from Utils.Preference import Preference

class DataUnifier:
    """
    This class is used to unify data with given preferences.
    """
    def __init__(self, data, preferences, mode="auto"):
        """
        :param data: the data to be unified can be a dictionary, JSON or database object
        :param preferences: the preferences to be used for unifying the data
        """
        self.data = data
        self.preferences = preferences
        self.mode = mode
        self.unified_data = None

    def unifyPreferencesMin(self):
        """
        Converts all preferences in the relation to MIN by inverting MAX dimensions.
        """
        self.tupleToTab(self.data)
        for i in range(len(self.preferences)):
            if self.preferences[i] == Preference.MAX:
                self.preferences[i] = Preference.MIN
                for val in self.data.values():
                    val[i] = 1 / val[i]
        self.tabToTuple(self.data)
        return self.data

    def unifyPreferencesMax(self):
        """
        Converts all preferences in the relation to MAX by inverting MIN dimensions.
        """
        for i in range(len(self.preferences)):
            if self.preferences[i] == Preference.MIN:
                self.preferences[i] = Preference.MAX
                for val in self.data.values():
                    val[i] = 1 / val[i]
        return self.data

    def tupleToTab(self, rTuple):
        """
        Converts all tuple values in the relation dictionary to lists.

        This is used to allow in-place modification of the data (since lists are mutable,
        unlike tuples).

        :param rTuple: dict - the relation dictionary with tuple values to be converted
        """
        for key, val in rTuple.items():
            rTuple[key] = list(val)

    def tabToTuple(self, rTab):
        """
        Converts all list values in the relation dictionary back to tuples.

        This is typically used after data processing to restore the original tuple format.

        :param rTab: dict - the relation dictionary with list values to be converted
        """
        for key, val in rTab.items():
            rTab[key] = tuple(val)

    def unifyPreferences(self):
        """
        Unify the preferences based on the given mode.
        :return: unified preferences
        """
        if self.mode == "Min":
            return [Preference.MIN] * len(self.preferences)
        elif self.mode == "Max":
            return [Preference.MAX] * len(self.preferences)
        elif self.mode == "auto":
            countMin = self.preferences.count(Preference.MIN)
            countMax = self.preferences.count(Preference.MAX)
            if countMin > countMax:
                return [Preference.MIN] * len(self.preferences)
            elif countMax > countMin:
                return [Preference.MAX] * len(self.preferences)
            else:
                return [Preference.MAX] * len(self.preferences)
        return None

if __name__ == "__main__":
    data = JsonObject("../../Assets/AlgoExecution/JsonFiles/RTuples8.json")
    preferences = [Preference.MIN, Preference.MAX, Preference.MIN]

    data_unifier = DataUnifier(data, preferences, "auto")
    data_unifier.unify()