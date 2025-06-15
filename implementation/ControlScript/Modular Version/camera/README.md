# Camera Module - JSON-basiertes Kamera-System

Dieses Modul implementiert ein vollständig JSON-basiertes Kamera-System für die I-Scan Control Software.

## 📋 Dateien

- `cameras_config.json` - Kamera-Konfigurationsdatei
- `json_camera_config.py` - Konfigurations-Manager
- `json_camera_stream.py` - Stream-Manager
- `__init__.py` - Modul-Exporte

## ⚙️ Konfiguration

### Kamera-Definition in `cameras_config.json`:

```json
{
  "cameras": [
    {
      "index": 0,
      "verbindung": "USB:0",
      "beschreibung": "Hauptkamera USB Port 0",
      "name": "Kamera 1",
      "enabled": true,
      "resolution": [640, 480],
      "fps": 30
    }
  ],
  "settings": {
    "auto_start_streams": true,
    "stream_timeout": 5,
    "reconnect_attempts": 3
  }
}
```

### Parameter-Beschreibung:

- **index**: Eindeutige Kamera-ID (0, 1, 2, ...)
- **verbindung**: Hardware-Interface ("USB:0", "USB:1", etc.)
- **beschreibung**: Textuelle Beschreibung der Kamera
- **name**: Anzeigename in der GUI
- **enabled**: Kamera aktiviert (true/false)
- **resolution**: Auflösung als [Breite, Höhe]
- **fps**: Bildrate pro Sekunde

## 🔧 Verwendung

### Konfiguration laden:
```python
from camera import JSONCameraConfig

config = JSONCameraConfig("cameras_config.json")
cameras = config.get_enabled_cameras()
```

### Stream-Manager:
```python
from camera import JSONCameraStreamManager

stream_manager = JSONCameraStreamManager(config)
stream_manager.start_auto_streams()
```

### Hardware-Interface parsen:
```python
# Aus "USB:0" wird {'type': 'usb', 'device_index': 0, 'interface': 0}
hardware_info = config.parse_verbindung("USB:0")
```

## 🔄 Live-Reload

Das System unterstützt Live-Reload der Konfiguration:
1. JSON-Datei bearbeiten
2. Konfiguration neu laden
3. Nur Streams werden aktualisiert (GUI bleibt unverändert)

## 🛠️ Entwicklung

Das Modul ist vollständig thread-safe und kann parallel zur GUI ausgeführt werden. Alle Kamera-Operationen sind non-blocking implementiert.
