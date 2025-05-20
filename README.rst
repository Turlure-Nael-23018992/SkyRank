📦 SkyRank — Installation Guide
===============================

SkyRank is a benchmarking and visualization framework for Skyline algorithms.

This guide explains how to install and run SkyRank correctly on **Windows** and **Linux/macOS**, including its Git submodules and required dependencies.

🚀 Clone the Repository with Submodules
---------------------------------------

SkyRank depends on two Git submodules:

- ``external/BBS/`` → `BBS-Python-3.x- <https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-.git>`__
- ``external/BBS/RTree/`` → `R-Tree-Python-3.x- <https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-.git>`__

Clone everything in one command:

.. code-block:: bash

    git clone --recurse-submodules https://github.com/Turlure-Nael-23018992/SkyRank.git

Already cloned without submodules? Run this inside the project folder:

.. code-block:: bash

    git submodule update --init --recursive

🧪 Step-by-Step Installation
----------------------------

📍 **Windows Setup**

1. **Install Python 3.8**
   Download it from: https://www.python.org/downloads/release/python-380/

2. **Create and activate a virtual environment**:

.. code-block:: cmd

    python -m venv .venv
    .venv\Scripts\activate

3. **Install dependencies using `pip`**:

.. code-block:: cmd

    pip install -e .

📍 **Linux / macOS Setup**

1. **Install Python 3.8**
   (Use `pyenv` or your system’s package manager)

2. **Create and activate a virtual environment**:

.. code-block:: bash

    python3.8 -m venv .venv
    source .venv/bin/activate

3. **Install project in editable mode**:

.. code-block:: bash

    pip install -e .

📜 Dependencies Overview
-------------------------

The following Python packages are required:

- ``PyQt5==5.15.10`` — GUI with modern components and 3D visualization
- ``tkinter`` — Lightweight fallback interface (already included in most Python distributions)
- ``matplotlib`` — Plotting graphs
- ``numpy`` — Matrix/vector computations
- ``scikit-learn`` — Dimensionality reduction (PCA)
- ``colorama`` and ``humanize`` — Terminal output formatting

🖥️ Launch the Graphical Interfaces
-----------------------------------

SkyRank comes with **two GUI modes**:

- ✅ **Modern GUI (PyQt5)**: 3D visualization, interactive selection, better UX
- 🪶 **Lightweight GUI (Tkinter)**: Requires fewer libraries, suitable for older machines

Launch them using:

.. code-block:: bash

    skyrank-gui      # PyQt5 interface
    skyrank-gui2     # Tkinter interface

🔍 Need Help?
-------------

For issues or contributions, feel free to open a GitHub issue or contact the maintainers:

- Naël Turlure
- Mickael Martin-Nevot
