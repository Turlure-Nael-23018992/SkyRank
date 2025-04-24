import sqlite3
from Utils.DatasModifier.DatabaseToDict import DatabaseToDict
from Utils.DatasModifier.JsonUtils import readJson
from Utils.DatasModifier.DictToDatabase import DictToDatabase

class DataNormalizer:

    def __init__(self, r, fp):
        self.relation = r
        self.filepath = fp
        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"

    def fpToRelation(self):
        """
        Convert the databases to a relation
        """
        dbToDict = DatabaseToDict(self.filepath)
        self.relation = dbToDict.toDict()
        self.conn.close()

    def jsonToRelation(self):
        """
        Convert the json to a relation
        """
        self.relation = readJson(self.filepath, asTuple=True)

    def deleteLineDb(self, line):
        """
        Delete a line from the database
        :param line: the line to delete
        """
        self.cursor.execute(f"DELETE FROM {self.tableName} WHERE RowId = {line}")
        self.conn.commit()

    def addLinesDb(self, lines):
        """
        Add lines to the database
        :param lines: the lines to add
        """
        for line in lines:
            self.cursor.execute(f"INSERT INTO {self.tableName} VALUES ({line[0]}, {line[1]}, {line[2]}, {line[3]})")
        self.conn.commit()

    def refreshDb(self):
        """
        Refresh the database
        """
        dictToDb = DictToDatabase(self.filepath)
        dictToDb.toDatabase(self.relation)

    @staticmethod
    def beautyPrintDict(r):
        """
        Print the dictionary in a beautiful way
        """
        for key, value in r.items():
            print(f"{key}: {value}")
        print("========================================")
        print("Longueur de la relation:", len(r))

    @staticmethod
    def beautyPrintSkylinePoint(r):
        """
        Print the skyline points in a beautiful way
        :param r: the relation
        """
        print("========================================")
        print("Points du SkyLine:")
        for key in r.keys():
            print(f"{key}")
        print("========================================")
        print("Longueur de la relation:", len(r))
        print("========================================")

    @staticmethod
    def sortArr(arr):
        """
        Sort the array in ascending order (in-place).
        :param arr: The array to sort
        :return: The sorted array
        """
        return arr.sort()



if __name__ == "__main__":
    """fp = "../../Assets/DeepSkyTest.db"
    jsonfp = "../../Algorithms/Datas/RTuples8.json"
    r = readJson(jsonfp, asTuple=True)
    dataNorm = DataNormalizer(r, fp)
    dataNorm.refreshDb()"""
    tab = [3,1,5,7]
    print(DataNormalizer.sortArr(tab))

