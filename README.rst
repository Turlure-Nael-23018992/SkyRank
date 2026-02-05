📦 SkyRank — Installation Guide
===============================

.. image:: https://joss.theoj.org/papers/5f3289355fa004bf243ef2533b3d2117/status.svg
   :target: https://joss.theoj.org/papers/5f3289355fa004bf243ef2533b3d2117
   :alt: JOSS status

SkyRank is an open-source benchmarking and visualization framework for multi-dimensional Skyline algorithms.
It provides a modular architecture to run, compare, and visualize advanced preference queries over large datasets.
SkyRank includes multiple algorithmic implementations (e.g., BBS, RankSky, Cosky), graphical user interfaces (PyQt5 and Tkinter), and tools to generate publication-ready visualizations using LaTeX.
It is designed for researchers, students, and practitioners interested in preference-based data analysis, algorithm evaluation, and Skyline computation.

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
  `CONTRIBUTING <https://github.com/Turlure-Nael-23018992/SkyRank/blob/main/CONTRIBUTING.rst>`_ file.

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
