"""
Camera Module Package
Modulares JSON-basiertes Kamera-System für wiederverwendbare Kamera-Integration

JSON-basierte Module:
- JSONCameraConfig: JSON-basierte Kamera-Konfiguration
- JSONCameraStreamManager: Automatische Stream-Verwaltung für alle konfigurierten Kameras
- CameraStream: Einzelner Kamera-Stream mit Threading-Support
"""

# JSON-basierte Module
from .json_camera_config import JSONCameraConfig
from .json_camera_stream import JSONCameraStreamManager, CameraStream

__all__ = [
    # JSON-basierte Module
    'JSONCameraConfig',
    'JSONCameraStreamManager',
    'CameraStream'
]

__version__ = "1.0.0"
