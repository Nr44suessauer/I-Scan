@echo off
echo ================================================
echo I-Scan Control Software - Modular Version
echo ================================================
echo Installation und Start der modularen I-Scan Anwendung...
echo Features: Thread-safe camera, Non-blocking operations
echo.

echo Überprüfe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH verfügbar!
    echo Bitte installieren Sie Python von https://python.org
    echo Stellen Sie sicher, dass "Add Python to PATH" aktiviert ist.
    pause
    exit /b 1
)

echo Python gefunden. Überprüfe pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: pip ist nicht verfügbar!
    echo Installiere pip...
    python -m ensurepip --upgrade
)

echo.
echo ================================================
echo Installiere benötigte Python-Pakete...
echo ================================================

echo Aktualisiere pip auf die neueste Version...
python -m pip install --upgrade pip

echo.
echo Installiere Core-Pakete aus requirements.txt...
cd "Modular Version"
python -m pip install -r requirements.txt

echo.
echo Installiere zusätzliche benötigte Pakete...
echo - Installiere tkinter-Unterstützung (falls erforderlich)...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNUNG: tkinter nicht verfügbar. Möglicherweise müssen Sie Python neu installieren mit tkinter-Unterstützung.
)

echo - Installiere typing-extensions für erweiterte Type-Hints...
python -m pip install typing-extensions

echo - Installiere datetime-Unterstützung...
python -c "from datetime import datetime" >nul 2>&1

echo - Installiere json-Unterstützung...
python -c "import json" >nul 2>&1

echo - Installiere threading-Unterstützung...
python -c "import threading" >nul 2>&1

echo - Installiere os und sys Module (Standard-Module)...
python -c "import os, sys" >nul 2>&1

echo - Installiere subprocess-Unterstützung...
python -c "import subprocess" >nul 2>&1

echo - Installiere re-Modul für reguläre Ausdrücke...
python -c "import re" >nul 2>&1

echo - Installiere math-Modul...
python -c "import math" >nul 2>&1

echo - Installiere time-Modul...
python -c "import time" >nul 2>&1

echo - Installiere traceback-Modul...
python -c "import traceback" >nul 2>&1

echo.
echo ================================================
echo Überprüfe alle installierten Pakete...
echo ================================================

echo Überprüfe OpenCV...
python -c "import cv2; print('OpenCV Version:', cv2.__version__)" || (
    echo FEHLER beim Import von OpenCV!
    echo Versuche alternative Installation...
    python -m pip install opencv-python --force-reinstall
)

echo Überprüfe PIL/Pillow...
python -c "from PIL import Image, ImageTk; print('PIL/Pillow erfolgreich importiert')" || (
    echo FEHLER beim Import von PIL/Pillow!
    echo Versuche alternative Installation...
    python -m pip install Pillow --force-reinstall
)

echo Überprüfe NumPy...
python -c "import numpy as np; print('NumPy Version:', np.__version__)" || (
    echo FEHLER beim Import von NumPy!
    echo Versuche alternative Installation...
    python -m pip install numpy --force-reinstall
)

echo Überprüfe Requests...
python -c "import requests; print('Requests Version:', requests.__version__)" || (
    echo FEHLER beim Import von Requests!
    echo Versuche alternative Installation...
    python -m pip install requests --force-reinstall
)

echo.
echo ================================================
echo Alle Pakete installiert und überprüft!
echo ================================================
echo.

echo Starte die modulare I-Scan Anwendung...
python main_modular.py

echo.
echo ================================================
echo Anwendung beendet.
echo ================================================
echo Drücken Sie eine beliebige Taste zum Beenden...
pause
