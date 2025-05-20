#!/bin/bash

echo "[SkyRank] Setting up environment with Python 3.8..."

# Check for python3.8
if ! command -v python3.8 &> /dev/null
then
    echo "❌ Python 3.8 is not installed. Please install it manually."
    exit 1
fi

# Create virtual env
echo "Creating virtual environment..."
python3.8 -m venv .venv

# Activate and install
source .venv/bin/activate
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e .

# Init git submodules
echo "Initializing Git submodules..."
git submodule update --init --recursive

echo
echo "✅ SkyRank is ready. To launch:"
echo "  source .venv/bin/activate"
echo "  skyrank-gui"
