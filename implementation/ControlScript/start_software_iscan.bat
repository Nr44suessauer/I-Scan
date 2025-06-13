@echo off
echo ====================================================
echo  I-SCAN SOFTWARE STARTUP SCRIPT
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not available in PATH.
    echo Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Install/Update required Python packages
echo 📦 Installing required Python packages...
echo.

REM Core packages for GUI and image processing
python -m pip install --upgrade pip
python -m pip install pillow>=8.0.0
python -m pip install opencv-python>=4.5.0
python -m pip install requests>=2.25.0
python -m pip install numpy>=1.20.0

REM Visualization and plotting packages for Calculator
python -m pip install matplotlib>=3.5.0
python -m pip install scipy>=1.7.0

REM Additional packages for advanced functionality
python -m pip install pandas>=1.3.0

if errorlevel 1 (
    echo.
    echo ⚠️ Warning: Some packages could not be installed.
    echo The program may not work completely.
    echo.
    pause
)

echo.
echo ✅ All packages installed!
echo.

REM Clean up any accidentally created pip log files/folders
echo 🧹 Cleaning up installation artifacts...

REM Remove files that look like version numbers (e.g., 1.3.0, 2.25.0, etc.)
for /f "delims=" %%f in ('dir /b /a-d ^| findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$"') do (
    if exist "%%f" (
        del /f /q "%%f" >nul 2>&1
        echo   Removed file: %%f
    )
)

REM Remove files that look like version numbers without patch version (e.g., 1.3, 2.25)
for /f "delims=" %%f in ('dir /b /a-d ^| findstr /r "^[0-9][0-9]*\.[0-9][0-9]*$"') do (
    if exist "%%f" (
        del /f /q "%%f" >nul 2>&1
        echo   Removed file: %%f
    )
)

REM Remove directories that look like version numbers
for /f "delims=" %%d in ('dir /b /ad ^| findstr /r "^[0-9][0-9]*\.[0-9][0-9]*"') do (
    if exist "%%d" (
        rmdir /s /q "%%d" >nul 2>&1
        echo   Removed directory: %%d
    )
)

REM Also clean up common pip temporary files/folders
if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
if exist "*.tmp" del /f /q "*.tmp" >nul 2>&1
if exist "pip-*.txt" del /f /q "pip-*.txt" >nul 2>&1

echo ✓ Cleanup completed
echo.

REM Navigate to Software_IScan directory and start the application
echo 🚀 Starting Software_IScan GUI...
cd Software_IScan
python main.py

REM Pause to show any error messages
if errorlevel 1 (
    echo.
    echo ❌ Error starting the application!
    pause
)
