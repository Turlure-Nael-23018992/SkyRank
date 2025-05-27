---
title: "SkyRank: A Unified Toolkit for Skyline Ranking and Visualization"
tags:
  - skyline
  - multi-criteria decision making
  - ranking algorithms
  - data analysis
  - visualization
authors:
  - name: Nael Turlure
    orcid: 0009-0005-9978-5163
    affiliation: 1
  - name: Mickaël Martin Nevot
    orcid: 0009-0004-7893-3449
    affiliation: 1
affiliations:
  - name: Aix-Marseille Université, France
    index: 1
date: 27 May 2025
bibliography: paper.bib
---

# Summary

SkyRank is an open-source Python framework that implements and compares various **Skyline ranking algorithms**, including `dp-idp`, `RankSky`, `CoSky`, and `DeepSky`. While these methods have been independently introduced in the literature, SkyRank provides a **unified, reproducible, and extensible platform** to evaluate and visualize them interactively [@Borzsony2001].

SkyRank is designed for researchers, students, and practitioners working on **multi-criteria decision making**, **Pareto optimality**, and **database preference queries**. It includes a modular benchmarking backend, a LaTeX-compatible graph generator, and two graphical user interfaces (based on PyQt5 and Tkinter) for interactive data exploration.

# Statement of Need

While the Skyline [@Borzsony2001] operator is widely studied, **few open-source tools** exist to explore, rank, and visualize Skyline points across diverse datasets and scoring models. Implementations are often scattered, hard to reproduce, and lack integrated visual support.

SkyRank addresses this gap by:

- Providing **ready-to-use implementations** of major Skyline ranking approaches.
- Offering **graphical interfaces** to run algorithms and compare results visually.
- Supporting **LaTeX-based chart generation** for scientific reporting.
- Enabling **rapid experimentation** and educational use.

# Features

- ✅ Implementations of `dp-idp`, `RankSky`, `CoSky`, `DeepSky`
- ✅ Automatic scoring using PageRank [@Page1998], cosine similarity, and TOPSIS scoring [@Lai1994]
- ✅ Modular architecture for adding new ranking strategies
- ✅ GUI interfaces for ranking and visual inspection of results
- ✅ Graph export in TikZ/LaTeX format
- ✅ Installation via script or editable pip package
- ✅ Tested on real-world datasets (e.g., Pokémon attributes)
- ✅ Benchmarking on synthetic uncorrelated datasets with 3, 6, and 9 dimensions, ranging from 10 to 1,000,000,000 tuples

# Software Architecture

- `Algorithms/` contains the core implementations of Skyline ranking methods, including `dp-idp`, `RankSky`, `CoSky`, and `DeepSky`.

- `Core/` hosts the application logic and UI entry points:
  - `App.py` handles global orchestration and job launching.
  - `AppUI.py` and `AppUIPyQT.py` provide Tkinter and PyQt5 graphical interfaces.
  - `LatexMain.py` generates ready-to-use LaTeX/TikZ charts.

- `Utils/` gathers reusable tools and utilities, organized by functionality:
  - `DataModifier/` and `DataTypes/` handle data preparation and internal structures.
  - `Exporter/` defines data export interfaces (e.g., CSV, LaTeX).
  - `Latex/` includes tools for LaTeX/TikZ generation.

- `Database/` provides database integration and mock data generation:
  - The `Database` class manages SQLite creation and insertion of random test data (with dynamic column scaling).
  - `SqlDataMocker` retrieves controlled subsets of rows/columns for benchmarking and converts them using a `DataParser`.

- `Assets/` contains benchmark datasets (e.g., Pokémon), test databases, execution logs, and configuration files.

- `docs/` includes documentation built with `pdoc`.

- `paper/` contains the JOSS submission material (`paper.md`, `paper.bib`).

- `external/` hosts Git submodules for third-party algorithms ([BBS](https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-), [RTree](https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-)).

# Acknowledgements

The CoSky method and the overall Skyline ranking approach are based on work by Martin-Nevot & Lakhal [@MartinNevot2024].  
SkyRank implements and adapts these methods in a unified open-source environment.
