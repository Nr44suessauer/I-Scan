# I-Scan Control Software - Version 1 (Original)

Die ursprüngliche, vollständige I-Scan Control Software mit allen Kernfunktionen.

**Author:** Marc Nauendorf  
**Email:** marc.nauendorf@hs-heilbronn.de  
**Website:** deadlinedriven.dev

## 🚀 Schnellstart

```bash
# Über Batch-Datei aus dem ControlScript-Verzeichnis
start_software_iscan.bat

# Oder direkt
python main.py
```

## 📁 Datei-Struktur (bereinigt)

```
Software_IScan/
├── main.py                    # 🎯 Hauptanwendung (monolithisch)
├── api_client.py             # 🌐 HTTP API-Client
├── device_control.py         # 🔧 Hardware-Steuerung  
├── logger.py                 # 📝 Logging-System
├── operation_queue.py        # 🔄 Operations-Warteschlange
├── webcam_helper.py          # 📷 Webcam-Funktionen
├── servo_angle_calculator.py # 📐 Servo-Winkel-Berechnungen
├── angle_calculator_commands.py # 🧮 Winkel-Rechner-Dialog
├── requirements.txt          # 📦 Python-Abhängigkeiten
├── wizard_icon.png          # 🎨 Anwendungs-Icon
└── README_V1.md             # 📖 Diese Dokumentation
```

## ✨ Funktionen

### Hardware-Steuerung
- **Servo-Motor**: Winkel-Steuerung (0-90°)
- **Stepper-Motor**: Positionierung in mm
- **LED-Steuerung**: Farbe und Helligkeit
- **Button-Status**: Abfrage von Hardware-Buttons

### Kamera-Integration
- **Live-Stream**: Webcam-Anzeige in der GUI
- **Foto-Aufnahme**: Bilder speichern
- **Autofokus-Delay**: Konfigurierbare Verzögerung

### Batch-Operationen
- **Operations-Queue**: Mehrere Befehle in Reihenfolge
- **CSV Import/Export**: Queue-Operationen speichern/laden
- **Wiederholung**: Automatische Queue-Wiederholung

### Winkel-Berechnungen
- **Geometrische Berechnungen**: Servo-Positionierung
- **Visualisierung**: Graphische Darstellung
- **CSV-Export**: Berechnungsergebnisse exportieren

## 🔧 Abhängigkeiten

```bash
pip install -r requirements.txt
```

Hauptabhängigkeiten:
- `tkinter` - GUI-Framework
- `opencv-python` - Webcam-Handling  
- `Pillow` - Bildverarbeitung
- `requests` - HTTP API-Calls
- `numpy` - Numerische Operationen

## ⚙️ Konfiguration

### API-Endpunkt
Tragen Sie die Hardware-API-URL in das Eingabefeld ein (z.B. `http://192.168.1.100`)

### Kamera-Einstellungen
- **Device Index**: Kamera-Index (0, 1, 2, ...)
- **Autofokus-Delay**: Verzögerung vor Foto-Aufnahme

## 🎯 Anwendungsfälle

1. **Manuelle Hardware-Steuerung**: Einzelne Befehle ausführen
2. **Automatisierte Abläufe**: Queue-System für Batch-Operationen  
3. **Kamera-Dokumentation**: Live-Stream und Foto-Aufnahme
4. **Präzisions-Positionierung**: Geometrische Berechnungen für Servo-Winkel

## 🔄 Queue-System

Das Queue-System ermöglicht die Automatisierung von Befehlssequenzen:

1. **Befehle hinzufügen**: Über "+" Buttons
2. **Queue ausführen**: "Warteschlange ausführen"
3. **Export/Import**: Queue als CSV speichern/laden
4. **Wiederholung**: Automatische Queue-Wiederholung aktivieren

## 📊 Winkel-Rechner

Integrierter Geometrie-Rechner für präzise Servo-Positionierung:
- Geometrische Visualisierung
- Berechnungstabellen  
- CSV-Export der Ergebnisse
- Integration in Queue-System

## 🏗️ Architektur

**Monolithische Struktur**: Alle GUI- und Logik-Funktionen in `main.py` integriert für einfache Wartung und Verständlichkeit.

---

**Hinweis**: Für eine modernere, modulare Architektur siehe **Version 2** im `Version 2/` Ordner.
