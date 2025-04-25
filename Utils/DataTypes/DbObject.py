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

    def __name__(self):
        """
        Return the name of the class.
        """
        return "DbObject"