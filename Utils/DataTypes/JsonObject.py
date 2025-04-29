class JsonObject:
    """
    A class to represent a JSON object.
    """

    def __init__(self, fp):
        """
        Initialize the JSON object

        :param fp: Path to the JSON file.
        """
        self.fp = fp

    @staticmethod
    def __name__():
        """
        Return the name of the class.
        """
        return "JsonObject"