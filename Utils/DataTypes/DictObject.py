class DictObject:
    """
    A class that allows access to dictionary keys as attributes.
    """
    def __init__(self, r):
        """
        Initialize the DictObject with a dictionary.
        :param data: Dictionary to be accessed as attributes.
        """
        self.r = r

    def __name__(self):
        """
        Return the name of the class.
        """
        return "DictObject"