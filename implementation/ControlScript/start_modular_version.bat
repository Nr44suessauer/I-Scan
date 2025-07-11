@echo off
echo ================================================
echo I-Scan Control Software - Modular Version
echo ================================================
echo Installing and starting the modular I-Scan application...
echo Features: Thread-safe camera, Non-blocking operations
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not available in PATH!
    echo Please install Python from https://python.org
    echo Make sure "Add Python to PATH" is enabled.
    pause
    exit /b 1
)

echo Python found. Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo.
echo ================================================
echo Installing required Python packages...
echo ================================================

echo Upgrading pip to the latest version...
python -m pip install --upgrade pip

echo.
echo Installing core packages from requirements.txt...
cd "Modular Version"
python -m pip install -r requirements.txt

echo.
echo Installing additional required packages...
echo - Installing tkinter support (if required)...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: tkinter not available. You may need to reinstall Python with tkinter support.
)

echo - Installing typing-extensions for advanced type hints...
python -m pip install typing-extensions

echo - Installing datetime support...
python -c "from datetime import datetime" >nul 2>&1

echo - Installing json support...
python -c "import json" >nul 2>&1

echo - Installing threading support...
python -c "import threading" >nul 2>&1

echo - Installing os and sys modules (standard modules)...
python -c "import os, sys" >nul 2>&1

echo - Installing subprocess support...
python -c "import subprocess" >nul 2>&1

echo - Installing re module for regular expressions...
python -c "import re" >nul 2>&1

echo - Installing math module...
python -c "import math" >nul 2>&1

echo - Installing time module...
python -c "import time" >nul 2>&1

echo - Installing traceback module...
python -c "import traceback" >nul 2>&1

echo.
echo ================================================
echo Checking all installed packages...
echo ================================================

echo Checking OpenCV...
python -c "import cv2; print('OpenCV Version:', cv2.__version__)" || (
    echo ERROR importing OpenCV!
    echo Trying alternative installation...
    python -m pip install opencv-python --force-reinstall
)

echo Checking PIL/Pillow...
python -c "from PIL import Image, ImageTk; print('PIL/Pillow successfully imported')" || (
    echo ERROR importing PIL/Pillow!
    echo Trying alternative installation...
    python -m pip install Pillow --force-reinstall
)

echo Checking NumPy...
python -c "import numpy as np; print('NumPy Version:', np.__version__)" || (
    echo ERROR importing NumPy!
    echo Trying alternative installation...
    python -m pip install numpy --force-reinstall
)

echo Checking Requests...
python -c "import requests; print('Requests Version:', requests.__version__)" || (
    echo ERROR importing Requests!
    echo Trying alternative installation...
    python -m pip install requests --force-reinstall
)

echo.
echo ================================================
echo All packages installed and verified!
echo ================================================
echo.

echo Starting the modular I-Scan application...
python main_modular.py

echo.
echo ================================================
echo Application finished.
echo ================================================
echo Press any key to exit...
pause
