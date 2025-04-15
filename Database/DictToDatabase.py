import sqlite3

class DictToDatabase:
    """
    Class to convert a dictionary into a database
    """

    def __init__(self, databaseFilepath):
        """
        Constructor of the class
        :param databaseFilepath: The path to the database file
        """
        self.conn = sqlite3.connect(databaseFilepath)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"
        self.data = {}

    def toDatabase(self, data):
        """
        Convert the dictionary into a database
        :param data: The dictionary to convert
        """
        self.data = data
        print(f"Data received: {self.data}")  # Check the received data

        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.tableName}") # Drop the table if it exists
            print(f"Table {self.tableName} dropped.")
            self.cursor.execute(f"CREATE TABLE {self.tableName} " # Create the table
                                f"(RowId INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"Col_A NUMERIC, Col_B NUMERIC, Col_C NUMERIC)")
            print(f"Table {self.tableName} created.")
        except sqlite3.OperationalError as e:
            print(f"Error creating table: {e}")

        try:
            for value in self.data.values():
                print(f"Inserting: {value}") # Check the value being inserted
                self.cursor.execute(f"INSERT INTO {self.tableName}" # Insert the data
                                    f" (Col_A, Col_B, Col_C) VALUES (?, ?, ?)", value)
            print("All data inserted.")
        except sqlite3.OperationalError as e:
            print(f"Error inserting data: {e}")

        self.conn.commit() # Commit the changes
        print("Changes committed.")
        self.conn.close() # Close the connection
        print("Connection closed.")

if __name__ == "__main__":
    databaseFilepath = "test.db"
    db = DictToDatabase(databaseFilepath)
    data = {1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9)}
    db.toDatabase(data)