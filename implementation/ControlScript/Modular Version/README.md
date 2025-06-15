# I-Scan Control Software

Eine modulare Steuerungssoftware für das I-Scan System mit JSON-basierter Kamera-Konfiguration und Live-Streaming-Funktionalität.

## 🎯 Übersicht

Das I-Scan Control Software ist eine professionelle Anwendung zur Steuerung von Mess- und Kamerasystemen. Die Software bietet eine intuitive Benutzeroberfläche mit Echtzeit-Kamera-Streams, automatisierter Gerätesteuerung und flexibler JSON-basierter Konfiguration.

## 🚀 Hauptfunktionen

- **📷 Multi-Kamera-System**: Unterstützung mehrerer USB-Kameras mit Live-Streaming
- **⚙️ JSON-Konfiguration**: Flexible Kamera-Konfiguration über JSON-Editor
- **🔄 Live-Reload**: Konfigurationsänderungen ohne Neustart anwenden
- **🎛️ Hardware-Interface**: Steuerung von Servo-Motoren und Sensoren
- **📊 Winkel-Berechnung**: Integrierte Berechnungsfunktionen
- **🗂️ Queue-System**: Verwalten und Ausführen von Operationssequenzen
- **📝 Logging**: Vollständige Protokollierung aller Aktionen

## 🏗️ Architektur

Die Software folgt einer modularen Architektur mit klarer Trennung der Verantwortlichkeiten:

```
I-Scan Control Software/
├── main_modular.py          # Hauptanwendung
├── camera/                  # Kamera-System (JSON-basiert)
├── gui_components.py        # GUI-Komponenten
├── event_handlers.py        # Event-Management
├── queue_operations.py      # Operations-Queue
├── config.py               # Konfiguration
└── requirements.txt        # Python-Dependencies
```

## 📋 Systemanforderungen

- **Python**: 3.8 oder höher
- **Betriebssystem**: Windows 10/11
- **Hardware**: USB-Kameras, Servo-Controller (optional)
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
