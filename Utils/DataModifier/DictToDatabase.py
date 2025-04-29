import sqlite3

class DictToDatabase:
    """
    Class to convert a dictionary into a SQLite database table.
    """

    def __init__(self, databaseFilepath):
        """
        Initialize the DictToDatabase class.

        :param databaseFilepath: The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(databaseFilepath)
        self.cursor = self.conn.cursor()
        self.tableName = "Pokemon"
        self.data = {}

    def toDatabase(self, data):
        """
        Convert the provided dictionary to a SQLite database table.

        :param data: The dictionary to be converted (key -> tuple of values).
        """
        self.data = data

        try:
            # Drop the table if it already exists
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.tableName}")
            print(f"Table {self.tableName} dropped.")

            # Create a new table
            self.cursor.execute(
                f"CREATE TABLE {self.tableName} "
                f"(RowId INTEGER PRIMARY KEY AUTOINCREMENT, "
                f"Col_A NUMERIC, Col_B NUMERIC, Col_C NUMERIC)"
            )
            print(f"Table {self.tableName} created.")
        except sqlite3.OperationalError as e:
            print(f"Error creating table: {e}")

        try:
            # Insert all records into the table
            for value in self.data.values():
                print(f"Inserting: {value}")
                self.cursor.execute(
                    f"INSERT INTO {self.tableName} (Col_A, Col_B, Col_C) VALUES (?, ?, ?)",
                    value
                )
            print("All data inserted.")
        except sqlite3.OperationalError as e:
            print(f"Error inserting data: {e}")

        # Commit changes and close the connection
        self.conn.commit()
        print("Changes committed.")
        self.conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    """
    Example usage of DictToDatabase.
    """

    databaseFilepath = "../../Assets/DeepSkyTest.db"
    db = DictToDatabase(databaseFilepath)

    r = {
        1: (5, 20, 1/70),
        2: (4, 60, 1/50),
        3: (5, 30, 1/60),
        4: (1, 80, 1/60),
        5: (5, 90, 1/40),
        6: (9, 30, 1/50),
        7: (7, 80, 1/40),
        8: (9, 90, 1/30)
    }

    db.toDatabase(r)
