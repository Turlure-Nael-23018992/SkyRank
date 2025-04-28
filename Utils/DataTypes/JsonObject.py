from Utils.DataModifier.JsonUtils import *

class JsonObject:
    """
    A class to represent a JSON object.
    """

    def __init__(self, jsonFilepath):
        """
        Initialize the JSON object
        """
        self.fp = jsonFilepath

    def __name__(self):
        """
        Return the name of the class.
        """
        return "JsonObject"