📦 SkyRank — Installation Guide
===============================

This guide explains how to install and run the **SkyRank** project with its visual interfaces using **CPython 3.8** and virtual environments.

⚙️ Requirements
---------------

- Git installed
- Python 3.8 installed (https://www.python.org/downloads/release/python-380/)
- Internet connection
- (On Windows) Python launcher `py`

📥 Clone the Repository with Submodules
---------------------------------------

SkyRank depends on nested Git submodules for external algorithms:

- ``external/BBS/`` → `BBS-Python-3.x- <https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-.git>`__
- ``external/BBS/RTree/`` → `R-Tree-Python-3.x- <https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-.git>`__

To clone the full project with all submodules in one step:

.. code-block:: bash

    git clone --recurse-submodules https://github.com/Turlure-Nael-23018992/SkyRank.git

If you already cloned it without `--recurse-submodules`, run:

.. code-block:: bash

    git submodule update --init --recursive

🚀 Installation on Linux/macOS
------------------------------

Run the provided shell script:

.. code-block:: bash

    chmod +x install.sh
    ./install.sh

This script will:

- Use `python3.8` to create a virtual environment in `.venv`
- Install all dependencies
- Initialize Git submodules
- Make the `skyrank-gui` and `skyrank-gui2` commands available inside the virtual environment

🚀 Installation on Windows
--------------------------

SkyRank provides an installation script that does everything for you:

1. **Checks for Python 3.8**
2. **Creates `.venv` with CPython 3.8**
3. **Installs all dependencies**
4. **Initializes submodules**
5. **Exposes CLI commands: `skyrank-gui`, `skyrank-gui2`**

To launch it:

.. code-block:: bash

    install.bat

If you encounter a permissions issue, try launching the terminal **as administrator**.

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

Once installed, activate the environment and launch one of the interfaces:

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

📄 License
----------

MIT License. See ``LICENSE`` file for details.

``SkyRank`` is developed and maintained by Naël Turlure and Mickael Martin-Nevot.
