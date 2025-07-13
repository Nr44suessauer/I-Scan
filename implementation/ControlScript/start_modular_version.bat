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
    echo Checking if Python is installed but not in PATH...
    set /p PYTHONFOLDER="Please enter your Python installation folder (e.g. C:\\Users\\USERNAME\\AppData\\Local\\Programs\\Python\\Python3x or C:\\Python3x), or leave blank to download Python: "
    if not "%PYTHONFOLDER%"=="" (
        set "PATH=%PYTHONFOLDER%;%PYTHONFOLDER%\\Scripts;%PATH%"
        echo PATH variable temporarily set to: %PYTHONFOLDER%
        echo Checking for python.exe in: %PYTHONFOLDER%\python.exe
        if exist "%PYTHONFOLDER%\python.exe" (
            echo Python executable found in the specified folder.
            "%PYTHONFOLDER%\python.exe" --version
            rem Set python command to use this executable for the rest of the script
            set "PYTHONCMD=%PYTHONFOLDER%\python.exe"
        ) else (
            echo Python executable NOT found in the specified folder!
            echo Please check the path and try again.
            pause
            exit /b 1
        )
    ) else (
        echo Python will be downloaded and installed...
        powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile %TEMP%\python-installer.exe"
        start /wait %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        echo Installation abgeschlossen. Bitte starten Sie das Skript erneut.
        pause
        exit /b 1
    )
)

if defined PYTHONCMD (
    set "PYTHON=%%PYTHONCMD%%"
) else (
    set "PYTHON=python"
)
echo Python found. Checking pip...
%PYTHON% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    echo Installing pip...
    %PYTHON% -m ensurepip --upgrade
)

echo.
echo ================================================
echo Installing required Python packages...
echo ================================================

echo Upgrading pip to the latest version...
%PYTHON% -m pip install --upgrade pip

echo.
echo Creating temp folder for install logs...
set "LOGDIR=%CD%\temp_install_logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo Installing core packages...
cd "Modular Version"
%PYTHON% -m pip install pillow>=8.0.0 > "%LOGDIR%\pillow.log"
%PYTHON% -m pip install opencv-python>=4.5.0 > "%LOGDIR%\opencv-python.log"
%PYTHON% -m pip install requests>=2.25.0 > "%LOGDIR%\requests.log"
%PYTHON% -m pip install numpy>=1.20.0 > "%LOGDIR%\numpy.log"

echo.
echo Installing additional required packages...
echo - Installing tkinter support (if required)...
%PYTHON% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: tkinter not available. You may need to reinstall Python with tkinter support.
)

echo - Installing scipy...
%PYTHON% -m pip install scipy > "%LOGDIR%\scipy.log"

echo - Installing matplotlib...
%PYTHON% -m pip install matplotlib > "%LOGDIR%\matplotlib.log"

echo - Installing pandas...
%PYTHON% -m pip install pandas > "%LOGDIR%\pandas.log"

echo - Installing pyserial...
%PYTHON% -m pip install pyserial > "%LOGDIR%\pyserial.log"

echo - Checking csv module (standard)...
%PYTHON% -c "import csv" >nul 2>&1

echo - Checking json module (standard)...
%PYTHON% -c "import json" >nul 2>&1

echo - Checking threading module (standard)...
%PYTHON% -c "import threading" >nul 2>&1

echo - Checking os and sys modules (standard)...
%PYTHON% -c "import os, sys" >nul 2>&1

echo - Checking subprocess module (standard)...
%PYTHON% -c "import subprocess" >nul 2>&1

echo - Checking re module for regular expressions...
%PYTHON% -c "import re" >nul 2>&1

echo - Checking math module...
%PYTHON% -c "import math" >nul 2>&1

echo - Checking time module...
%PYTHON% -c "import time" >nul 2>&1

echo - Checking traceback module...
%PYTHON% -c "import traceback" >nul 2>&1

echo - Checking typing-extensions...
%PYTHON% -m pip install typing-extensions > "%LOGDIR%\typing-extensions.log"

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

rem Clean up temp install logs directly before starting the application

pushd ..
if exist "%LOGDIR%" rmdir /s /q "%LOGDIR%"
popd

python main_modular.py

echo.
echo ================================================
echo Application finished.
echo ================================================
echo Press any key to exit...
pause
echo.
echo ================================================
echo Application finished.
echo ================================================
echo Press any key to exit...
pause
echo Cleaning up temp install logs...
cd ..
if exist "%LOGDIR%" rmdir /s /q "%LOGDIR%"
