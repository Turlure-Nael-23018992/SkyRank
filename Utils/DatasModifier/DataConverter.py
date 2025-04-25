from Utils.DataTypes.JsonObject import JsonObject
from Utils.DatasModifier.JsonUtils import *
from Utils.DatasModifier.DictToDatabase import DictToDatabase

class DataConverter:
    """
    A class to convert data between different formats.
    """

    def __init__(self, data):
        """
        Initialize the DataConverter with data.
        :param data: Data to be converted.
        """
        self.data = data
        self.DictToDatabase = DictToDatabase("../Assets/AlgoExecution/DbFiles/TestExecution.db")

    def jsonToRelation(self):
        """
        Convert JSON data to a relation.
        :return: Converted data.
        """
        data = readJson(self.data)
        data = {k: tuple(v) for k, v in data.items()}
        return data

    def jsonToDb(self):
        """
        Convert JSON data to a database format.
        """
        data = self.jsonToRelation()
        self.DictToDatabase.toDatabase(data)

    def relationToDb(self):
        """
        Convert relation data to a database format.
        """
        print("self.data : 2 ", self.data)
        self.DictToDatabase.toDatabase(self.data)