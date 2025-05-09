# 📦 SkyRank — Installation Guide

This guide explains how to correctly install the SkyRank project along with its submodules (BBS and RTree).

## 🚀 Clone the Project with Submodules

SkyRank depends on two nested Git submodules:
- `external/BBS/` → [BBS-Python-3.x-](https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-.git)
- `external/BBS/RTree/` → [R-Tree-Python-3.x-](https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-.git)

To clone the full project with all submodules in one command:

```bash
git clone --recurse-submodules https://github.com/Turlure-Nael-23018992/SkyRank.git
```
Already cloned without submodules? Run this inside the repo:
```bash
git submodule update --init --recursive