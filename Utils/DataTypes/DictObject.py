class DictObject:
    """
    A class to represent a dictionary object.
    """

    def __init__(self, r):
        """
        Initialize the DictObject with a dictionary.

        :param r: Dictionary to be accessed as attributes.
        """
        self.r = r

    @staticmethod
    def __name__():
        """
        Return the name of the class.
        """
        return "DictObject"