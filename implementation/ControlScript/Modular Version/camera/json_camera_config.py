"""
JSON-basierte Kamera-Konfiguration
Verwaltet Kamera-Einstellungen über JSON-Datei
"""

import json
import os
from typing import List, Dict, Optional


class JSONCameraConfig:
    """JSON-basierte Kamera-Konfiguration"""
    
    def __init__(self, config_file: str = "cameras_config.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config_data = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """Lade Konfiguration aus JSON-Datei"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"JSON-Konfiguration geladen: {len(self.get_cameras())} Kameras")
                return True
            else:
                print(f"Konfigurationsdatei nicht gefunden: {self.config_file}")
                self.create_default_config()
                return False
        except Exception as e:
            print(f"Fehler beim Laden der JSON-Konfiguration: {e}")
            return False
    
    def save_config(self) -> bool:
        """Speichere Konfiguration in JSON-Datei"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            print("JSON-Konfiguration gespeichert")
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der JSON-Konfiguration: {e}")
            return False
    
    def create_default_config(self):
        """Erstelle Standard-Konfiguration"""
        self.config_data = {
            "cameras": [
                {
                    "index": 0,
                    "verbindung": "USB:0",
                    "beschreibung": "Standard USB-Kamera",
                    "name": "Kamera 1",
                    "enabled": True,
                    "resolution": [640, 480],
                    "fps": 30
                }
            ],
            "settings": {
                "auto_start_streams": True,
                "stream_timeout": 5,
                "reconnect_attempts": 3
            }
        }
        self.save_config()
    
    def get_cameras(self) -> List[Dict]:
        """Hole alle Kamera-Konfigurationen"""
        return self.config_data.get('cameras', [])
    
    def get_enabled_cameras(self) -> List[Dict]:
        """Hole nur aktivierte Kameras"""
        return [cam for cam in self.get_cameras() if cam.get('enabled', True)]
    
    def get_camera_by_index(self, index: int) -> Optional[Dict]:
        """Hole Kamera nach Index"""
        for camera in self.get_cameras():
            if camera.get('index') == index:
                return camera
        return None
    
    def add_camera(self, index: int, verbindung: str, beschreibung: str, name: str = None) -> bool:
        """Füge neue Kamera hinzu"""
        try:
            if 'cameras' not in self.config_data:
                self.config_data['cameras'] = []
            
            # Prüfe ob Index bereits existiert
            if self.get_camera_by_index(index):
                print(f"Kamera mit Index {index} existiert bereits")
                return False
            
            new_camera = {
                "index": index,
                "verbindung": verbindung,
                "beschreibung": beschreibung,
                "name": name or f"Kamera {index + 1}",
                "enabled": True,
                "resolution": [640, 480],
                "fps": 30
            }
            
            self.config_data['cameras'].append(new_camera)
            return self.save_config()
        except Exception as e:
            print(f"Fehler beim Hinzufügen der Kamera: {e}")
            return False
    
    def update_camera(self, index: int, **kwargs) -> bool:
        """Aktualisiere Kamera-Einstellungen"""
        try:
            camera = self.get_camera_by_index(index)
            if not camera:
                print(f"Kamera mit Index {index} nicht gefunden")
                return False
            
            # Aktualisiere Felder
            for key, value in kwargs.items():
                if key in camera:
                    camera[key] = value
            
            return self.save_config()
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Kamera: {e}")
            return False
    
    def remove_camera(self, index: int) -> bool:
        """Entferne Kamera"""
        try:
            cameras = self.config_data.get('cameras', [])
            original_count = len(cameras)
            self.config_data['cameras'] = [cam for cam in cameras if cam.get('index') != index]
            
            if len(self.config_data['cameras']) < original_count:
                return self.save_config()
            else:
                print(f"Kamera mit Index {index} nicht gefunden")
                return False
        except Exception as e:
            print(f"Fehler beim Entfernen der Kamera: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Hole globale Einstellungen"""
        return self.config_data.get('settings', {})
    
    def update_settings(self, **kwargs) -> bool:
        """Aktualisiere globale Einstellungen"""
        try:
            if 'settings' not in self.config_data:
                self.config_data['settings'] = {}
            
            for key, value in kwargs.items():
                self.config_data['settings'][key] = value
            
            return self.save_config()
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Einstellungen: {e}")
            return False
    
    def parse_verbindung(self, verbindung: str) -> Dict:
        """Parse Verbindungsstring und extrahiere Hardware-Interface"""
        try:
            if verbindung.startswith("USB:"):
                device_index = int(verbindung.split(":")[1])
                return {
                    "type": "usb",
                    "device_index": device_index,
                    "interface": f"/dev/video{device_index}" if os.name != 'nt' else device_index
                }
            elif verbindung.startswith("IP:"):
                ip_address = verbindung.split(":")[1]
                return {
                    "type": "network",
                    "ip_address": ip_address,
                    "interface": f"rtsp://{ip_address}/stream"
                }
            elif verbindung.startswith("COM:"):
                com_port = verbindung.split(":")[1]
                return {
                    "type": "serial",
                    "com_port": com_port,
                    "interface": f"COM{com_port}"
                }
            else:
                # Fallback: versuche als direkte USB-Index
                try:
                    device_index = int(verbindung)
                    return {
                        "type": "usb",
                        "device_index": device_index,
                        "interface": device_index
                    }
                except ValueError:
                    print(f"Unbekanntes Verbindungsformat: {verbindung}")
                    return None
        except Exception as e:
            print(f"Fehler beim Parsen der Verbindung '{verbindung}': {e}")
            return None
    
    def get_available_cameras(self) -> List[Dict]:
        """Hole alle verfügbaren Kameras mit Hardware-Interface-Info"""
        available_cameras = []
        
        for camera in self.get_enabled_cameras():
            verbindung_info = self.parse_verbindung(camera['verbindung'])
            if verbindung_info:
                camera_info = camera.copy()
                camera_info['hardware_interface'] = verbindung_info
                available_cameras.append(camera_info)
        
        return available_cameras
