# Software IScan - Main GUI Application

The complete I-Scan hardware control application with GUI interface for 3D scanning operations. This application provides comprehensive control over all scanner hardware components through a user-friendly interface.

**Author:** Marc Nauendorf  
**Email:** marc.nauendorf@hs-heilbronn.de  
**Website:** deadlinedriven.dev

## Core Application - `main.py`

### Primary Features
- **Hardware Control GUI**: Complete graphical interface for all scanner components
- **Real-time Camera Integration**: Live webcam feed with photo capture capabilities  
- **Operation Queue System**: Batch operation management with CSV import
- **Device Communication**: REST API integration for hardware control
- **Position Tracking**: Real-time position monitoring and logging

### Hardware Components Supported

#### Servo Motor Control
- Angle adjustment (0-90°)
- Real-time angle feedback
- Queue-based operation support

#### Stepper Motor Control  
- Precise distance-based movement (cm input)
- Direction control (forward/backward)
- Speed adjustment
- Automatic step calculation for 28BYJ-48 stepper motor

#### LED Lighting System
- Hex color selection (#RRGGBB)
- Brightness control (0-100%)
- Real-time color preview

#### Camera System
- Live webcam streaming
- Photo capture with timestamping
- Automatic focus delay configuration

## Module Architecture

### `api_client.py` - Hardware Communication
- REST API client for device communication
- HTTP request management with error handling
- Connection status monitoring

### `device_control.py` - Hardware Interface
- Unified device control layer
- Position calculation and tracking
- Hardware state management

### `operation_queue.py` - Batch Operations
- CSV operation file import
- Sequential operation execution
- Queue management with pause/resume

### `webcam_helper.py` - Camera Integration
- OpenCV-based camera interface
- Image capture and processing
- Tkinter GUI integration

### `logger.py` - System Logging
- Real-time operation logging
- GUI output integration
- Status monitoring

## Installation & Setup

### Requirements
```bash
pip install tkinter pillow opencv-python requests numpy
```

### Quick Start
```bash
# Using batch file (Windows)
start.bat

# Or directly with Python
python main.py
```

### Configuration
- **Default API URL**: `http://192.168.137.7`
- **Default Stepper Parameters**: 28mm diameter, 80 speed
- **Camera**: Index 0, 320x240 resolution

## Operation Modes

### Manual Control
Direct hardware control through GUI buttons and input fields.

### CSV Batch Operations
Import operation sequences from Calculator_Angle_Maschine:
```csv
type,params,description
servo,"{\"angle\": 45}","Set servo angle"
photo,"{}","Take photograph"  
stepper,"{\"steps\": 100, \"direction\": 1, \"speed\": 80}","Move stepper"
```

### Queue Repeat Mode
Automatic repetition of loaded operation sequences for multiple scan runs.

## API Integration

The application communicates with hardware through REST endpoints:
- `/servo` - Servo motor control
- `/stepper` - Stepper motor control  
- `/led` - LED lighting control
- `/home` - Return to home position

## File Output

- **Photos**: Saved as `foto_YYYYMMDD_HHMMSS.jpg`
- **Logs**: Real-time operation logging in GUI
- **Position Data**: Automatic position tracking
- **Button-Abfrage** - Status-Monitoring

### Kamera-Integration:
- **Live-Vorschau** - Webcam-Feed in der GUI
- **Foto-Aufnahme** - Automatische Speicherung mit konfigurierbarem Delay
- **Multi-Kamera-Unterstützung** - Verschiedene Device-Indices

### Warteschlangen-System:
- **Operation Queue** - Sequenzielle Ausführung von Befehlen
- **CSV-Import/Export** - Speichern und Laden von Befehlssequenzen
- **Wiederholung** - Automatische Wiederholung der gesamten Warteschlange

### API-Konfiguration:
- **Flexible URL** - Anpassbare API-Endpunkt-Adresse
- **Fehlerbehandlung** - Robuste Fehlerbehandlung und Logging
- **Threading** - Nicht-blockierende UI durch Hintergrund-Operationen

## Konfiguration:

### Standard-Einstellungen:
- **API-URL**: `http://192.168.137.7`
- **Zahnraddurchmesser**: 28mm
- **Schrittmotor-Geschwindigkeit**: 80
- **LED-Farbe**: #B00B69
- **LED-Helligkeit**: 69%

### Anpassungen:
Standardwerte können direkt in `main.py` in den `DEFAULT_*` Konstanten geändert werden.

## Troubleshooting:

### Häufige Probleme:
1. **Kamera nicht erkannt**: Device-Index in den Kamera-Einstellungen ändern
2. **API-Verbindung fehlgeschlagen**: URL-Adresse und Netzwerkverbindung prüfen
3. **Import-Fehler**: Alle Python-Abhängigkeiten installieren

### Logs:
Alle Aktivitäten werden im Ausgabebereich der GUI protokolliert.

## Support:
Bei Problemen siehe `Doc.md` für detaillierte Anleitungen.
