from Utils.DisplayHelpers import beauty_print

import sqlite3

class DatabaseToDict:
    """
    Class to convert a database into a dictionary
    """
    def __init__(self, databaseFilepath):
        """
        Constructor of the class
        """
        self.conn = sqlite3.connect(databaseFilepath)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"
        self.data = []

    def toDict(self):
        """
        Convert the database into a dictionary
        :return: The database as a dictionary
        """
        sqlQuery = "SELECT * FROM " + self.tableName
        self.cursor.execute(sqlQuery)
        rows = self.cursor.fetchall()
        result = {}
        for row in rows:
            row_id = row[0]
            values = tuple(row[1:])
            result[row_id] = values
        self.data = result
        return result


if __name__ == "__main__":
    db = DatabaseToDict(fr"..\Assets\databases\cosky_db_C3_R100.db")
    data = db.toDict()
    print(data)