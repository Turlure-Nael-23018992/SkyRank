📦 SkyRank — Installation Guide
===============================

.. image:: https://joss.theoj.org/papers/5f3289355fa004bf243ef2533b3d2117/status.svg
   :target: https://joss.theoj.org/papers/5f3289355fa004bf243ef2533b3d2117
   :alt: JOSS status

SkyRank is an open-source benchmarking and visualization framework for multi-dimensional Skyline algorithms.
It provides a modular architecture to run, compare, and visualize advanced preference queries over large datasets.

✨ Features

----------

* **Multiple Algorithms**: Implementation of ``SkyIR``, ``RankSky``, ``CoSky``, and ``DP-IDP-DH`` (with dominance hierarchy).
* **Visual Exploration**: Built-in PyQt5 and Tkinter GUIs for 2D and 3D data visualization.
* **Flexible Data Inputs**: Supports Python dictionaries, JSON files, and SQLite databases.
* **Scientific Readiness**: Export tools to generate publication-ready LaTeX graphs.
* **High Accessibility**: Clean Python code with extensive documentation and minimal technical barriers for new researchers.

🚀 Minimal Working Example (MWE)
--------------------------------

A minimal working example has been incorporated to illustrate a comprehensive fundamental workflow. 
SkyRank provides a unified ``App`` class that serves as the primary entry point for all algorithms. 
To use it, you wrap your raw data in a **Data Object** (like ``DictObject``) and choose an algorithm.

.. code-block:: python

    from Core.App import App
    from Algorithms.CoskySql import CoskySQL
    from Utils.DataTypes.DictObject import DictObject
    from Utils.Preference import Preference

    # 1. Prepare your data {id: (coord1, coord2, ...)}
    # This data matches the Algorithms/Datas/RTuples8.json dataset
    raw_data = {
        1: (5, 20, 0.014), 
        2: (4, 60, 0.02), 
        3: (5, 30, 0.016),
        4: (1, 80, 0.016),
        5: (5, 90, 0.025),
        6: (9, 30, 0.02),
        7: (7, 80, 0.025),
        8: (9, 90, 0.033)
    }
    
    # 2. Wrap data and define preferences
    data = DictObject(raw_data)
    prefs = [Preference.MIN, Preference.MIN, Preference.MIN]
    
    # 3. Execute the workflow through the App
    app = App(data, CoskySQL, preferences=prefs)
    
    # 4. Access results
    print(f"Algorithm: {app.algo}")
    print(f"Execution Time: {app.execution_time}s")
    print(f"Skyline Points: {app.algo_instance.dict}")

💡 Why Use Data Objects?

-----------------------

SkyRank uses wrapper classes (``DictObject``, ``JsonObject``, ``DbObject``) to provide a consistent interface to the ``App`` class. This abstraction allows the ``App`` to automatically handle file loading, database connections, and format conversions without you worrying about the underlying storage.

🔄 Switching Data Sources

-------------------------

Depending on where your data is stored, you only need to change the object passed to the ``App``:

* **From a JSON file**:
  
  .. code-block:: python

      from Utils.DataTypes.JsonObject import JsonObject
      data = JsonObject("path/to/your_data.json")
      app = App(data, SkyIR)

* **From a SQLite database**:
  
  .. code-block:: python

      from Utils.DataTypes.DbObject import DbObject
      data = DbObject("path/to/database.db")
      app = App(data, SkyIR)

  *(Note: Databases must contain a table named 'Pokemon' with columns A1, A2, etc. See* `Data Formats Guide <docs/data_formats.rst>`_ *)*

🔧 App Parameters

----------------

The ``App`` constructor accepts several parameters to customize its behavior:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Parameter
     - Description
   * - ``data``
     - A ``DictObject``, ``JsonObject``, or ``DbObject`` instance.
   * - ``algo``
     - The algorithm class to run (e.g., ``SkyIR``, ``RankSky``, ``DpIdpDh``, ``CoskyAlgorithme``, ``CoskySQL``).
   * - ``preferences``
     - (Optional) A list of ``Preference.MIN`` or ``Preference.MAX`` for each dimension. Required for ``RankSky``, ``CoskySQL`` and ``CoskyAlgorithme``.
   * - ``exporter``
     - (Optional) An instance of an exporter (e.g., ``CsvExporter``) to automatically save results.

⚙️ Requirements
---------------

- Git installed
- Python 3.8 installed (https://www.python.org/downloads/release/python-380/)
- Internet connection
- (On Windows) Python launcher ``py``

📥 Clone the Repository with Submodules
---------------------------------------

SkyRank depends on nested Git submodules for external algorithms:

- ``external/BBS/`` → `BBS-Python-3.x- <https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-.git>`__
- ``external/BBS/RTree/`` → `R-Tree-Python-3.x- <https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-.git>`__

To clone the full project with all submodules in one step:

.. code-block:: bash

    git clone --recurse-submodules https://github.com/Turlure-Nael-23018992/SkyRank.git

If you already cloned it without ``--recurse-submodules``, run:

.. code-block:: bash

    git submodule update --init --recursive


🚀 Installation on Linux/macOS
------------------------------

Run the provided shell script:

.. code-block:: bash

    chmod +x install.sh
    ./install.sh

This script will:

- Use ``python3.8`` to create a virtual environment in ``.venv``
- Install all dependencies
- Initialize Git submodules
- Make the ``skyrank-gui`` and ``skyrank-gui2`` commands available inside the virtual environment


�️ Troubleshooting & Common Failure Modes
-----------------------------------------

The following guide addresses common issues and technical "paper cuts" that may occur during setup or execution.

**1. ModuleNotFoundError (BBS or RTree)**
  If you see an error related to missing modules inside ``external/``, it means the Git submodules were not correctly initialized. Run:

  .. code-block:: bash

      git submodule update --init --recursive

**2. GUI Dependencies (Linux)**
  If you encounter ``ModuleNotFoundError: No module named '_tkinter'`` or PyQt5 library errors, install the missing system packages:

  .. code-block:: bash

      sudo apt update
      sudo apt install python3-tk libxcb-cursor0

**3. Data Structure Errors**
  SkyRank expects specific naming conventions for SQLite databases:
  
  * The table must be named **'Pokemon'**.
  * Numerical columns must be named **'A1', 'A2', 'A3', ...**.
  * If your columns are named differently, the algorithm will fail to find the attributes. 
  * See the `Data Formats Guide <docs/data_formats.rst>`_ for details.

**4. Execution Time / Performance**
  For very large datasets, algorithms like ``RankSky`` (which uses a square matrix for PageRank) may require significant memory.
  If the application crashes or hangs, try using a smaller sample or a more pruning-efficient algorithm like ``CoskySQL``.


🐧 Installing on Ubuntu 23 and newer versions
---------------------------------------------

Ubuntu 23 and later no longer provide Python 3.8 in the default repositories.
If you try to run ``install.sh``, you may see an error saying **“Python 3.8 not found.”**
You have two simple options:

**Option 1 — Install Python 3.8 from deadsnakes PPA**

.. code-block:: bash

    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install -y python3.8 python3.8-venv python3.8-dev python3.8-distutils

Then create and activate a virtual environment:

.. code-block:: bash

    python3.8 -m venv .venv
    source .venv/bin/activate
    bash install.sh

**Option 2 — Install Python 3.8 with pyenv (no system changes)**

.. code-block:: bash

    curl https://pyenv.run | bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

    pyenv install 3.8.18
    pyenv local 3.8.18
    python -m venv .venv
    source .venv/bin/activate
    bash install.sh



🚀 Installation on Windows
--------------------------

SkyRank provides an installation script that does everything for you:

1. Checks for Python 3.8
2. Creates ``.venv`` with CPython 3.8
3. Installs all dependencies
4. Initializes submodules
5. Exposes CLI commands: ``skyrank-gui``, ``skyrank-gui2``

To launch it:

.. code-block:: bash

    install.bat

If you encounter a permissions issue, try running the terminal **as administrator**.


🧪 Manual Setup (Alternative)
-----------------------------

If you prefer setting it up manually:

On **Linux/macOS**:

.. code-block:: bash

    python3.8 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e .
    git submodule update --init --recursive

On **Windows**:

.. code-block:: bash

    py -3.8 -m venv .venv
    .\.venv\Scripts\activate
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
    python -m pip install -e .
    git submodule update --init --recursive


🏁 Usage
--------

Once installed, launch one of the interfaces:

On **Linux/macOS**:

.. code-block:: bash

    source .venv/bin/activate

    skyrank-gui     # PyQt5 GUI with Skyline visualizations
    skyrank-gui2    # Tkinter GUI (alternative interface)
    skyrank-graph   # LatexMaker (create your own graphs)

On **Windows**:

.. code-block:: bash

    .\.venv\Scripts\activate

    skyrank-gui     # PyQt5 GUI with Skyline visualizations
    skyrank-gui2    # Tkinter GUI (alternative interface)
    skyrank-graph   # LatexMaker (create your own graphs)


📂 Project Structure
--------------------

SkyRank is structured as a modular Python project relying on several Git repositories:

- `SkyRank-Client <https://github.com/Turlure-Nael-23018992/SkyRank-Client>`_ serves as the main interface and execution environment for SkyRank, allowing it to be used as a Python API.
- `SkyRank <https://github.com/Turlure-Nael-23018992/SkyRank>`_ is the core backend containing the main algorithms (``dp-idp`` improved with dominance hierarchy, ``RankSky``, ``CoSky``, etc.), benchmarking tools, data handling modules, export systems, and UI apps.
- `BBS-Python-3.x- <https://github.com/Turlure-Nael-23018992/BBS-Python-3.x->`_ is a dedicated submodule that implements the Branch-and-Bound Skyline (BBS) algorithm.
- `R-Tree-Python-3.x- <https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x->`_ provides the spatial indexing structures used internally by BBS.

These repositories are embedded hierarchically:

::

    SkyRank-Client
      └── SkyRank
            └── BBS-Python-3.x-
                  └── R-Tree-Python-3.x-

This structure enables clean separation of features, modular development, and reusability across different Skyline-related components.


📖 Documentation
----------------

The full Python documentation is available online via GitHub Pages:
https://turlure-nael-23018992.github.io/SkyRank/

The source files for the documentation are available in the repository:
`docs <https://github.com/Turlure-Nael-23018992/SkyRank/tree/main/docs>`_


🤝 Community Guidelines

----------------------

We welcome contributions from the community and encourage users to get involved in the development and improvement of SkyRank.

**Contributing**
  Guidelines for contributing to the project (code, documentation, bug fixes, feature requests) are described in the
  `CONTRIBUTING <https://github.com/Turlure-Nael-23018992/SkyRank/blob/main/CONTRIBUTING.md>`_ file.

**Reporting issues**
  Bugs, unexpected behavior, and feature requests can be reported via the GitHub issue tracker:
  https://github.com/Turlure-Nael-23018992/SkyRank/issues

**Support and questions**
  For general questions, usage help, or discussions, please open a GitHub issue with the *question* label.
  This allows the discussion to remain public and useful to the community.


📄 License
----------

``SkyRank`` is a free software made available under the MIT License.
For details see the `LICENSE <https://github.com/Turlure-Nael-23018992/SkyRank/blob/main/LICENSE>`_ file.


👥 Contributors
---------------

See the `AUTHORS.rst <https://github.com/Turlure-Nael-23018992/SkyRank/blob/main/AUTHORS.rst>`_ file for a complete list of contributors to the project.
