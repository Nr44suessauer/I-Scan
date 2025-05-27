@echo off
echo Starte I-Scan ControlScript...
python main.py
if errorlevel 1 (
    echo Fehler beim Starten des Programms.
    echo Bitte stellen Sie sicher, dass Python installiert ist und alle Abhängigkeiten erfüllt sind.
    echo Sie können die Abhängigkeiten mit folgendem Befehl installieren:
    echo py -m pip install pillow opencv-python requests
    pause
)
