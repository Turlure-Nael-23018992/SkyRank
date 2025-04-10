from Database.DatabaseHelpers import Database
from Utils.DataParser import DataParser

class SqlDataMocker:
    """
    Class that mock data from the database above
    """

    def __init__(self, col_count, row_count, filepath=f"../Assets/pokemon.db"):
        """
        Constructor for the DataMocker
        :param col_count: The number of cols needed
        :param row_count: The number of rows needed
        :param filepath: The filepath of the database
        """
        self.col_count = col_count
        self.row_count = row_count
        self.filepath = filepath
        self.run()

    def run(self):
        self.database = Database(self.filepath,self.col_count, self.row_count, is_debug=True)
        self.sql_data=self.database.select_all()
        self.dict_data=DataParser(self.sql_data).r_dict
        return self.dict_data




if __name__ == '__main__':

    db_filepath= f"../Assets/pokemon.db"
    for col in range(3, 4):
        for row in range(500, 501):

            col_len=col
            row_len=row
            dict_data = SQL_DataMocker(col_len, row_len,db_filepath).dict_data
    print(dict_data)