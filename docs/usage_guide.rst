📖 SkyRank GUI — Usage Guide
============================

This guide covers the main graphical interface launched via the ``skyrank-gui`` command (PyQt5).

.. contents:: Table of Contents
   :depth: 2
   :local:

---

🚀 Launching the Application
-----------------------------

Activate your virtual environment and run:

.. code-block:: bash

    # Linux / macOS
    source .venv/bin/activate
    skyrank-gui

    # Windows
    .\.venv\Scripts\activate
    skyrank-gui

The main window opens with a **control panel** on the left and a **3D visualization canvas** on the right.

---

🗂️ Step 1 — Choose a Data Source
----------------------------------

Use the **"Choose Data Type"** dropdown to select how data is loaded.

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Option
     - Description
   * - **Database**
     - Load a SQLite ``.db`` file from ``Assets/Databases/``. The table must be named ``Pokemon`` with numeric columns ``A1, A2, A3, ...``.
   * - **JSON**
     - Load a ``.json`` file from ``Assets/AlgoExecution/JsonFiles/``. Format: ``{"id": [v1, v2, ...], ...}``.
   * - **Dictionary**
     - Paste a Python dictionary directly into the text area, or select a JSON file as a fallback.
   * - **Generate Random Database**
     - Enter a number of columns (3, 6, or 9) and a number of rows to generate a synthetic SQLite database for testing.

After selecting the type, choose the file from the dropdown or click **"Import File"** to browse for it.

---

⚙️ Step 2 — Choose an Algorithm
---------------------------------

Use the **"Choose Algorithm"** dropdown to select the Skyline ranking method to run.

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Algorithm
     - Description
   * - **SkyIR**
     - Information-retrieval–based Skyline ranking. No preferences required.
   * - **DpIdpDh**
     - Dominance-hierarchy–based ``dp-idp`` ranking. No preferences required.
   * - **CoskyAlgorithme**
     - Cosine-similarity Skyline ranking. Requires column preferences (``min``/``max``).
   * - **CoskySQL**
     - SQL-based CoSky variant. Requires column preferences (``min``/``max``).
   * - **RankSky**
     - PageRank-based Skyline ranking. Requires column preferences (``min``/``max``).

---

🎯 Step 3 — Set Preferences (if required)
------------------------------------------

For **CoskyAlgorithme**, **CoskySQL**, and **RankSky**, a dialog box will appear after clicking **"Run Algorithm"**:

.. code-block:: text

    3 columns detected.
    For each column, enter 'min' (lower is better) or 'max' (higher is better),
    separated by commas.

    Example: min,max,min

    Enter 3 values:

Type one preference per column, separated by commas (e.g. ``min,max,min``).
The number of values must match the number of columns in the dataset.

---

▶️ Step 4 — Run the Algorithm
------------------------------

Click **"Run Algorithm"**. The status bar below the buttons displays the execution time once the algorithm completes.

Results are automatically exported to:

- ``Assets/Export/CSVFiles/Results.csv`` (CSV format)
- ``Assets/Export/JsonFiles/Result.json`` (JSON format)

depending on the **"Choose Output Format"** dropdown selection.

---

📊 Step 5 — View Results
--------------------------

**3D Scatter Plot**

The right panel updates automatically after each run with a 3D scatter plot (only for 3-dimensional datasets):

- 🔵 **Blue points** — all regular dataset points.
- 🔴 **Red points** — Skyline points (the Pareto-optimal set).
- A semi-transparent red surface approximates the Pareto front (rendered when at least 4 skyline points are available).

Use the **navigation toolbar** above the canvas (zoom, pan, rotate) to explore the plot interactively.

**Skyline Points Table**

Click **"View Skyline Points"** to open a separate window listing every Skyline point with its ID, coordinates, and score:

.. code-block:: text

    Total Points in Dataset (Unified): 8 | Skyline Points: 3

    ID: 1 | Coords: [5, 20, 0.014] | Score: 0.87
    ID: 4 | Coords: [1, 80, 0.016] | Score: 0.74
    ...

---

🔁 Running Multiple Experiments
---------------------------------

The interface supports successive runs without restarting:

1. Change the data source, algorithm, or preferences.
2. Click **"Run Algorithm"** again.
3. The graph and results table refresh automatically.

---

💡 Tips
--------

- For quick testing, use **"Generate Random Database"** with 3 columns and 100–1 000 rows.
- The PyQt5 GUI (``skyrank-gui``) includes full 3D visualization. The alternative Tkinter interface (``skyrank-gui2``) is lighter but offers fewer visual features.
- For scripted or batch usage, prefer the Python API via the ``App`` class (see the `README <https://github.com/Turlure-Nael-23018992/SkyRank>`_).

---

Common Issues
-----------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Symptom
     - Fix
   * - Blank graph after running
     - The dataset may not be 3-dimensional. Only 3D data is supported for visualization.
   * - "Incorrect preference list" error
     - The number of ``min``/``max`` values must exactly match the number of columns.
   * - No files in the dropdown
     - Place ``.db`` files in ``Assets/Databases/`` and ``.json`` files in ``Assets/AlgoExecution/JsonFiles/``.
   * - GUI does not open (Linux)
     - Run ``sudo apt install python3-tk libxcb-cursor0`` and retry.
