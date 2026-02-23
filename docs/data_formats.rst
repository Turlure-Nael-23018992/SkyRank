SkyRank Input Data Formats
==========================

SkyRank supports multiple input data formats, including Python Dictionaries, JSON files, and SQLite databases. This guide explains how to structure your data for successful processing.

1. Python Dictionary (Relation)
-------------------------------

The core data structure used internally by algorithms is a dictionary where:

* **Key**: A unique identifier for the point (integer or string).
* **Value**: A tuple or list of numerical coordinates.

.. code-block:: python

    # Example dictionary format
    data = {
        1: (0.5, 0.2, 0.7),
        2: (0.1, 0.9, 0.4),
        3: (0.4, 0.5, 0.5)
    }

2. JSON Files
-------------

JSON files should represent a dictionary of lists/tuples. Note that JSON keys are always strings, but SkyRank will attempt to treat them as IDs.

.. code-block:: json

    {
        "1": [0.5, 0.2, 0.7],
        "2": [0.1, 0.9, 0.4],
        "3": [0.4, 0.5, 0.5]
    }

.. tip::
   See ``Algorithms/Datas/RTuples8.json`` for a real-world example used in the project tests.

3. SQLite Databases
-------------------

SkyRank can read data directly from a SQLite database. For compatibility with the ``DataConverter`` and ``App`` classes, your database must follow these conventions:

* **Table Name**: Must be exactly ``Pokemon``.
* **Primary Key**: An ``id`` column (auto-incrementing integer).
* **Attributes**: Named ``A1``, ``A2``, ``A3``, etc., containing numerical values.

**Schema Example**

.. code-block:: sql

    CREATE TABLE Pokemon (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        A1 REAL,
        A2 REAL,
        A3 REAL
    );

    INSERT INTO Pokemon (A1, A2, A3) VALUES (0.5, 0.2, 0.7);
    INSERT INTO Pokemon (A1, A2, A3) VALUES (0.1, 0.9, 0.4);

.. important::
   The preference list provided to the algorithm must have the same length as the number of "A" columns in your database table.

4. Converting Data
------------------

You can use the ``DataConverter`` utility class located in ``Utils/DataModifier/DataConverter.py`` to move data between these formats programmatically.

.. code-block:: python

    from Utils.DataModifier.DataConverter import DataConverter

    # Convert JSON to a temporary SQLite DB
    converter = DataConverter("path/to/data.json")
    converter.jsonToDb("output.db")
