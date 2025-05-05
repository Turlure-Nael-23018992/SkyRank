from Database.DatabaseHelpers import Database
from Utils.DataParser import DataParser

class SqlDataMocker:
    """
    Class that mocks (generates) a subset of data from an SQL database,
    selecting a specific number of columns and rows.
    """

    def __init__(self, col_count, row_count, filepath=f"../Assets/pokemon.db"):
        """
        Constructor for the SqlDataMocker.

        :param col_count: Number of columns to retrieve from the database.
        :param row_count: Number of rows to retrieve from the database.
        :param filepath: Path to the database file.
        """
        self.col_count = col_count
        self.row_count = row_count
        self.filepath = filepath
        self.run()

    def run(self):
        """
        Connects to the database, retrieves the required subset of data,
        and converts it to a dictionary.

        :return: Dictionary where keys are row IDs and values are tuples of column data.
        """
        self.database = Database(self.filepath, self.col_count, self.row_count, is_debug=True)
        self.sql_data = self.database.select_all()
        self.dict_data = DataParser(self.sql_data).r_dict
        return self.dict_data


if __name__ == '__main__':
    # Example usage of SqlDataMocker to mock a dataset
    db_filepath = f"../Assets/pokemon.db"
    for col in range(3, 4):
        for row in range(500, 501):
            col_len = col
            row_len = row
            dict_data = SqlDataMocker(col_len, row_len, db_filepath).dict_data
    print(dict_data)
