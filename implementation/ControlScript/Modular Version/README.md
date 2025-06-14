# I-Scan Modular Version

Diese modulare Version der I-Scan Software bietet eine saubere, wartbare Architektur mit klarer Trennung der Verantwortlichkeiten.

## Struktur

```
Software_IScan_Modular/
├── main_modular.py          # Hauptanwendung
├── gui_components.py        # GUI-Komponenten
├── event_handlers.py        # Event-Handler (non-blocking)
├── queue_operations.py      # Queue-Operationen
├── config.py               # Konfiguration und Konstanten
├── api_client.py           # API-Client
├── device_control.py       # Hardware-Steuerung
├── logger.py               # Logging
├── operation_queue.py      # Operations-Queue
├── servo_angle_calculator.py # Servo-Berechnungen
├── webcam_helper.py        # Webcam (thread-safe)
├── angle_calculator_commands.py # Winkel-Rechner
└── wizard_icon.png         # Icon
```

## Funktionen

### ✅ Modulare Architektur
- Klare Separation of Concerns
- Leicht erweiterbar und wartbar
- Keine verschachtelte GUI-Struktur

### ✅ Thread-sichere Kamera
- Kontinuierliche Kamera-Updates
- Non-blocking GUI während API-Calls
- Separate Thread-Aktualisierung

### ✅ Non-blocking Operationen
- Alle Hardware-Befehle laufen in separaten Threads
- GUI bleibt responsiv
- Kamera läuft parallel zu allen Operationen

## Starten

```bash
# Über Batch-Datei
start_iscan_modular.bat

# Oder direkt
cd Software_IScan_Modular
python main_modular.py
```

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
