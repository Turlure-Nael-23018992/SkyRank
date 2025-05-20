@echo off
setlocal

echo [SkyRank] Installing using CPython 3.8...

REM Check if Python 3.8 is installed
where py >nul 2>&1 || (
    echo ❌ Python launcher not found. Please install Python 3.8.
    exit /b 1
)

py -3.8 --version >nul 2>&1 || (
    echo ❌ Python 3.8 not detected. Please install it from:
    echo https://www.python.org/downloads/release/python-380/
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
py -3.8 -m venv .venv

REM Install dependencies directly inside the venv
echo Installing dependencies...
call .venv\Scripts\activate.bat && (
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
    python -m pip install -e .
)

REM Initialize Git submodules
echo Initializing Git submodules...
git submodule update --init --recursive

echo.
echo ✅ SkyRank is ready to use!
echo To run it:
echo     .venv\Scripts\activate
echo     skyrank-gui for PyQt5 Interface with Skyline Points visualization
echo     skyrank-gui2 for Tkinter Interface
echo.
pause
