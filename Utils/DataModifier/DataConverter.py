import json
import os
import sqlite3

class DataConverter:
    """
    Utility class for converting data between JSON files, Python dictionaries (relations),
    and SQLite databases using a standardized table format (named 'Pokemon').

    Supported conversions:
    - JSON → SQLite
    - Dictionary → SQLite
    - JSON → Python dict
    - SQLite → Python dict
    """

    def __init__(self, source):
        """
        Initialize the converter.

        :param source: Either a path to a JSON or SQLite file, or a Python dictionary (relation).
        """
        self.source = source

    def jsonToDb(self, output_path="../Assets/AlgoExecution/DbFiles/TestExecution.db"):
        """
        Convert a JSON file into a SQLite database.
        The JSON should represent a dictionary of tuples/lists.

        :param output_path: Output path of the SQLite database file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(self.source, 'r') as f:
            data = json.load(f)

        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()

        # Drop existing table
        cursor.execute("DROP TABLE IF EXISTS Pokemon")

        # Determine number of attributes and create table
        sample = next(iter(data.values()))
        nb_cols = len(sample)
        columns = ", ".join([f"A{i} REAL" for i in range(1, nb_cols + 1)])
        cursor.execute(f"CREATE TABLE Pokemon (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")

        # Insert data
        for values in data.values():
            if not isinstance(values, (list, tuple)):
                raise ValueError("Each value in the JSON must be a list or tuple")
            if len(values) != nb_cols:
                raise ValueError("All tuples must have the same length")
            placeholders = ", ".join(["?"] * nb_cols)
            cursor.execute(f"INSERT INTO Pokemon ({', '.join([f'A{i}' for i in range(1, nb_cols + 1)])}) VALUES ({placeholders})", values)

        conn.commit()
        conn.close()

    def relationToDb(self, output_path="../Assets/AlgoExecution/DbFiles/TestExecution.db"):
        """
        Convert a Python dictionary (relation) into a SQLite database.

        :param output_path: Output path of the SQLite database file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        relation = self.source  # dict {id: tuple}
        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS Pokemon")
        nb_cols = len(next(iter(relation.values())))
        columns = ", ".join([f"A{i} REAL" for i in range(1, nb_cols + 1)])
        cursor.execute(f"CREATE TABLE Pokemon (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")

        for values in relation.values():
            placeholders = ", ".join(["?"] * nb_cols)
            cursor.execute(f"INSERT INTO Pokemon ({', '.join([f'A{i}' for i in range(1, nb_cols + 1)])}) VALUES ({placeholders})", values)

        conn.commit()
        conn.close()

    def jsonToRelation(self):
        """
        Convert a JSON file into a Python dictionary.

        :return: Dictionary {id: tuple}
        """
        with open(self.source, 'r') as f:
            data = json.load(f)
        return {int(k): tuple(v) for k, v in data.items()}

    def dbToRelation(self):
        """
        Convert a SQLite database table 'Pokemon' into a Python dictionary.

        :return: Dictionary {id: tuple of attribute values}
        """
        conn = sqlite3.connect(self.source)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pokemon")
        rows = cursor.fetchall()
        conn.close()
        return {i + 1: tuple(row[1:]) for i, row in enumerate(rows)}
