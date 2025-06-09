@echo off
echo =====================================
echo I-Scan ControlScript Starter
echo =====================================
echo.
echo Pruefe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH.
    echo Bitte installieren Sie Python von https://python.org
    pause
    exit /b 1
)

echo Python gefunden!
echo.
echo Starte I-Scan ControlScript...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo =====================================
    echo FEHLER beim Starten des Programms!
    echo =====================================
    echo.
    echo Mögliche Lösungen:
    echo 1. Installieren Sie fehlende Abhängigkeiten:
    echo    pip install -r requirements.txt
    echo.
    echo 2. Oder installieren Sie manuell:
    echo    pip install pillow opencv-python requests numpy
    echo.
    echo 3. Prüfen Sie, ob alle Dateien vorhanden sind
    echo.
    pause
) else (
    echo.
    echo Programm erfolgreich beendet.
)
