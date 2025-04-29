class DbObject:
    """
    A class to represent a database object.
    """

    def __init__(self, fp):
        """
        Initialize the database object.

        :param fp: Path to the database file.
        """
        self.fp = fp

    @staticmethod
    def __name__():
        """
        Return the name of the class.
        """
        return "DbObject"