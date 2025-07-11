
# I-Scan Control Software

A modular control software for the I-Scan system with JSON-based camera configuration and live streaming functionality.

## 🎯 Overview

The I-Scan Control Software is a professional application for controlling measurement and camera systems. The software provides an intuitive user interface with real-time camera streams, automated device control, and flexible JSON-based configuration.

## 🚀 Main Features

- **📷 Multi-camera system**: Support for multiple USB cameras with live streaming
- **⚙️ JSON configuration**: Flexible camera configuration via JSON editor
- **🔄 Live reload**: Apply configuration changes without restart
- **🎛️ Hardware interface**: Control of servo motors and sensors
- **📊 Angle calculation**: Integrated calculation functions
- **🗂️ Queue system**: Manage and execute operation sequences
- **📝 Logging**: Complete logging of all actions

## 🏗️ Architecture

The software follows a modular architecture with clear separation of responsibilities:

```
I-Scan Control Software/
├── main_modular.py          # Main application
├── camera/                  # Camera system (JSON-based)
├── gui_components.py        # GUI components
├── event_handlers.py        # Event management
├── queue_operations.py      # Operations queue
├── config.py                # Configuration
└── requirements.txt         # Python dependencies
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating system**: Windows 10/11
- **Hardware**: USB cameras, servo controller (optional)
- **Memory**: Minimum 4GB RAM

## 🔧 Installation

1. **Repository klonen oder herunterladen**
2. **Dependencies installieren**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Anwendung starten**:
   ```bash
   python main_modular.py
   ```

## 📖 Verwendung

### Kamera-Konfiguration
1. Öffnen Sie die Anwendung
2. Klicken Sie auf "Foto Config" im Queue/Settings-Bereich
3. Bearbeiten Sie die JSON-Konfiguration nach Bedarf
4. Speichern & Live-Reload für sofortige Anwendung

### Operationen ausführen
1. Wählen Sie die gewünschte Operation aus der Queue
2. Konfigurieren Sie Parameter falls erforderlich
3. Führen Sie die Operation aus
4. Überwachen Sie den Fortschritt im Log

## 🎮 Benutzeroberfläche

- **Kamera-Ansicht**: Live-Streams aller konfigurierten Kameras
- **Operations-Queue**: Verwalten von Arbeitsabläufen
- **JSON-Editor**: Direkte Bearbeitung der Kamera-Konfiguration
- **Log-Ausgabe**: Echtzeit-Protokollierung aller Aktionen
- **Hardware-Controls**: Manuelle Steuerung von Geräten

## 🔧 Konfiguration

Die Kamera-Konfiguration erfolgt über `camera/cameras_config.json`:

```json
{
  "cameras": [
    {
      "index": 0,
      "verbindung": "USB:0",
      "name": "Hauptkamera",
      "enabled": true,
      "resolution": [640, 480],
      "fps": 30
    }
  ]
}
```

## 🛠️ Entwicklung

### Module
- `camera/` - JSON-basiertes Kamera-System
- `gui_components.py` - UI-Komponenten
- `event_handlers.py` - Event-Management
- `webcam_helper.py` - Thread-sichere Kamera-Funktionen
- `logger.py` - Logging-System

### Erweitern
Die modulare Architektur ermöglicht einfache Erweiterungen:
1. Neue Module im entsprechenden Bereich hinzufügen
2. Imports in `main_modular.py` aktualisieren
3. Event-Handler bei Bedarf erweitern

## 📞 Support

Bei Fragen oder Problemen:
- Überprüfen Sie die Log-Ausgabe der Anwendung
- Stellen Sie sicher, dass alle Dependencies installiert sind
- Prüfen Sie die Kamera-Konfiguration auf Fehler

## 📄 Lizenz

Proprietäre Software - Alle Rechte vorbehalten.

---
**Entwickelt für professionelle Mess- und Steuerungsanwendungen**

## Verbesserungen gegenüber Original

1. **Bessere Struktur**: Keine verschachtelte GUI-Ordner-Struktur
2. **Thread-Sicherheit**: Kamera läuft kontinuierlich
3. **Non-blocking**: Alle API-Calls blockieren nicht die GUI
4. **Wartbarkeit**: Klare Trennung der Module
5. **Erweiterbarkeit**: Einfach neue Features hinzufügbar

## Technische Details

### Event-Handler (Non-blocking)
```python
def on_servo_execute(self):
    def servo_thread():
        self.app.device_control.servo_cmd()
    
    thread = threading.Thread(target=servo_thread)
    thread.daemon = True
    thread.start()
```

### Thread-sichere Kamera
```python
def _update_panel(self, panel, img_tk):
    panel.after(0, self._safe_update, panel, img_tk)
```

## Abhängigkeiten

Siehe `requirements.txt` für alle Python-Abhängigkeiten.
