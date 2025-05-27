"""
I-Scan ControlScript - Installationsanweisungen

Diese Datei enthält Anweisungen zur Installation und zum Starten des I-Scan ControlScript.
"""

# Erforderliche Bibliotheken
# =========================
#
# Um das I-Scan ControlScript zu verwenden, müssen die folgenden Bibliotheken installiert werden:
# - tkinter (kommt üblicherweise mit Python)
# - PIL (Python Imaging Library/Pillow)
# - OpenCV für Python
# - requests

# Installation der erforderlichen Bibliotheken
# ===========================================
#
# Sie können die erforderlichen Bibliotheken mit pip installieren:
#
# Windows:
# py -m pip install pillow opencv-python requests
#
# Linux/macOS:
# python3 -m pip install pillow opencv-python requests

# Programm starten
# ===============
#
# Nach der Installation der Bibliotheken können Sie das Programm starten mit:
#
# Windows:
# py main.py
#
# Linux/macOS:
# python3 main.py

# Programmstruktur
# ===============
#
# Die Anwendung besteht aus folgenden Dateien:
# - main.py - Hauptanwendung und GUI
# - api_client.py - API-Kommunikation
# - device_control.py - Gerätekontrolle
# - logger.py - Logging-Funktionalität
# - operation_queue.py - Verwaltung der Operationen
# - webcam_helper.py - Kamera-Funktionalität
#
# Alle diese Dateien müssen sich im selben Verzeichnis befinden.
