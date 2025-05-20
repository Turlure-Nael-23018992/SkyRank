#!/bin/bash
set -e

echo "[SkyRank] Installing using CPython 3.8..."

# Check Python 3.8
if ! command -v python3.8 &> /dev/null; then
    echo "❌ Python 3.8 not found. Please install it first:"
    echo "https://www.python.org/downloads/release/python-380/"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.8 -m venv .venv

# Activate and install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -e .

# Initialize git submodules
echo "Initializing Git submodules..."
git submodule update --init --recursive

echo
echo "✅ SkyRank is ready to use!"
echo "To run it:"
echo "    source .venv/bin/activate"
echo "    skyrank-gui     # PyQt5 interface"
echo "    skyrank-gui2    # Tkinter interface"
