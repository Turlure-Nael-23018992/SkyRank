from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataModifier.JsonUtils import *
from Utils.DataModifier.DictToDatabase import DictToDatabase
from Utils.DataModifier.DatabaseToDict import DatabaseToDict

class DataConverter:
    """
    A utility class for converting data between different formats:
    JSON, dictionaries (relations), and SQLite database files.
    """

    def __init__(self, data):
        """
        Initializes a DataConverter with the provided data.

        :param data: Can be a dictionary representing a relation, or a path to a JSON/database file.
        """
        self.data = data
        self.DictToDatabase = DictToDatabase("../Assets/AlgoExecution/DbFiles/TestExecution.db")

    def jsonToRelation(self):
        """
        Converts a JSON file to a dictionary with tuples (relation format).

        :return: A dictionary where each key maps to a tuple of values.
        """
        data = readJson(self.data)
        data = {k: tuple(v) for k, v in data.items()}
        return data

    def jsonToDb(self):
        """
        Converts JSON data into a database.
        The result is stored in TestExecution.db.
        """
        data = self.jsonToRelation()
        self.DictToDatabase.toDatabase(data)

    def relationToDb(self):
        """
        Converts a relation (dictionary) to a database.
        The result is stored in TestExecution.db.
        """
        self.DictToDatabase.toDatabase(self.data)

    def dbToRelation(self):
        """
        Converts data from a database into a dictionary (relation).

        :return: A dictionary representation of the database table.
        """
        databaseToDict = DatabaseToDict(self.data)
        return databaseToDict.toDict()
