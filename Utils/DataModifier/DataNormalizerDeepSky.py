import sqlite3
from Utils.DataModifier.DatabaseToDict import DatabaseToDict
from Utils.DataModifier.JsonUtils import readJson
from Utils.DataModifier.DictToDatabase import DictToDatabase

class DataNormalizerDeepSky:
    """
    A utility class to normalize and manipulate relations (datasets)
    stored either in a database file or JSON file format.
    """

    def __init__(self, r, fp):
        """
        Initialize the DataNormalizerDeepSky.

        :param r: A relation represented as a dictionary (key -> tuple of values).
        :param fp: Path to the database or JSON file.
        """
        self.relation = r
        self.filepath = fp
        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"

    def fpToRelation(self):
        """
        Convert the database into a relation (dictionary format).
        """
        dbToDict = DatabaseToDict(self.filepath)
        self.relation = dbToDict.toDict()
        self.conn.close()

    def jsonToRelation(self):
        """
        Convert a JSON file into a relation (dictionary format).
        """
        self.relation = readJson(self.filepath, asTuple=True)

    def deleteLineDb(self, line):
        """
        Delete a specific row from the database based on its RowId.

        :param line: The RowId of the line to delete.
        """
        self.cursor.execute(f"DELETE FROM {self.tableName} WHERE RowId = {line}")
        self.conn.commit()

    def addLinesDb(self, lines):
        """
        Add multiple rows to the database.

        :param lines: A list of lines to insert, where each line is a tuple.
        """
        for line in lines:
            self.cursor.execute(f"INSERT INTO {self.tableName} VALUES ({line[0]}, {line[1]}, {line[2]}, {line[3]})")
        self.conn.commit()

    def refreshDb(self):
        """
        Overwrite and refresh the database content with the current relation.
        """
        dictToDb = DictToDatabase(self.filepath)
        dictToDb.toDatabase(self.relation)

    @staticmethod
    def beautyPrintDict(r):
        """
        Nicely print a full dictionary with its keys and values.

        :param r: The dictionary to print.
        """
        for key, value in r.items():
            print(f"{key}: {value}")
        print("========================================")
        print("Relation size:", len(r))

    @staticmethod
    def beautyPrintSkylinePoint(r):
        """
        Nicely print the keys of a dictionary representing skyline points.

        :param r: The dictionary containing skyline points.
        """
        print("========================================")
        print("Skyline Points:")
        for key in r.keys():
            print(f"{key}")
        print("========================================")
        print("Relation size:", len(r))
        print("========================================")

    @staticmethod
    def sortArr(arr):
        """
        Sort an array in ascending order (modifies the array in-place).

        :param arr: The list to sort.
        :return: The sorted list (same object).
        """
        return arr.sort()


if __name__ == "__main__":
    """
    Example usage of DataNormalizerDeepSky.
    """
    r = readJson("../../Assets/AlgoExecution/JsonFiles/RTuples8.json")
    DataNorm = DataNormalizerDeepSky(r, "../../Assets/DeepSkyTest.db")
    DataNorm.refreshDb()
