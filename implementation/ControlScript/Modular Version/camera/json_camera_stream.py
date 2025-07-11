"""
JSON-based camera stream manager
Automatically creates streams for all configured cameras
"""

import cv2
import threading
import time
import tkinter as tk
from typing import Dict, List, Optional, Callable
try:
    from .json_camera_config import JSONCameraConfig
except ImportError:
    from json_camera_config import JSONCameraConfig


class CameraStream:
    """Single camera stream"""
    
    def __init__(self, camera_config: Dict, on_frame_callback: Optional[Callable] = None):
        self.config = camera_config
        self.index = camera_config['index']
        self.name = camera_config['name']
        self.connection = camera_config['connection']
        self.description = camera_config['description']
        self.hardware_interface = camera_config.get('hardware_interface', {})
        
        self.cap = None
        self.running = False
        self.thread = None
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.on_frame_callback = on_frame_callback
        
        # Stream statistics
        self.frames_captured = 0
        self.last_frame_time = 0
        self.fps_actual = 0
        
        print(f"CameraStream created: {self.name} ({self.connection})")
    
    def connect(self) -> bool:
        """Verbinde zur Kamera"""
        try:
            if self.hardware_interface.get('type') == 'usb':
                device_index = self.hardware_interface.get('device_index', 0)
                self.cap = cv2.VideoCapture(device_index)
                
                if not self.cap.isOpened():
                    print(f"Fehler: Kann USB-Kamera {device_index} nicht öffnen")
                    return False
                
                # Setze Auflösung wenn konfiguriert
                if 'resolution' in self.config:
                    width, height = self.config['resolution']
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                # Setze FPS wenn konfiguriert
                if 'fps' in self.config:
                    self.cap.set(cv2.CAP_PROP_FPS, self.config['fps'])
                
                print(f"USB camera {device_index} connected successfully")
                return True
            
            elif self.hardware_interface.get('type') == 'network':
                # Netzwerk-Kamera (RTSP, HTTP, etc.)
                stream_url = self.hardware_interface.get('interface')
                self.cap = cv2.VideoCapture(stream_url)
                
                if not self.cap.isOpened():
                    print(f"Error: Cannot open network camera {stream_url}")
                    return False
                
                print(f"Network camera {stream_url} connected successfully")
                return True
            
            else:
                print(f"Unknown camera type: {self.hardware_interface.get('type')}")
                return False
                
        except Exception as e:
            print(f"Fehler beim Verbinden zur Kamera {self.name}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect camera"""
        self.stop_stream()
        if self.cap:
            self.cap.release()
            self.cap = None
        print(f"Camera {self.name} disconnected")
    
    def start_stream(self) -> bool:
        """Starte Stream"""
        if self.running:
            print(f"Stream für {self.name} läuft bereits")
            return True
        
        if not self.cap or not self.cap.isOpened():
            if not self.connect():
                return False
        
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()
        print(f"Stream für {self.name} gestartet")
        return True
    
    def stop_stream(self):
        """Stoppe Stream"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=2)
            print(f"Stream für {self.name} gestoppt")
    
    def _stream_loop(self):
        """Stream-Loop (läuft in separatem Thread)"""
        while self.running:
            try:
                if not self.cap or not self.cap.isOpened():
                    print(f"Kamera {self.name} nicht verbunden")
                    break
                
                ret, frame = self.cap.read()
                if not ret:
                    print(f"Kein Frame von Kamera {self.name} erhalten")
                    time.sleep(0.1)
                    continue
                
                # Frame sicher speichern
                with self.frame_lock:
                    self.current_frame = frame.copy()
                    self.frames_captured += 1
                    
                    # FPS berechnen
                    current_time = time.time()
                    if self.last_frame_time > 0:
                        time_diff = current_time - self.last_frame_time
                        if time_diff > 0:
                            self.fps_actual = 1.0 / time_diff
                    self.last_frame_time = current_time
                
                # Callback aufrufen wenn vorhanden
                if self.on_frame_callback:
                    self.on_frame_callback(self.index, frame)
                
                # Kurze Pause um CPU zu schonen
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Fehler im Stream-Loop für {self.name}: {e}")
                time.sleep(0.5)
    
    def get_frame(self):
        """Hole aktuellen Frame (thread-safe)"""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def take_photo(self):
        """Mache Foto"""
        frame = self.get_frame()
        if frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{self.name}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Foto gespeichert: {filename}")
            return filename
        else:
            print(f"Kein Frame für Foto von {self.name} verfügbar")
            return None
    
    def get_status(self) -> Dict:
        """Hole Stream-Status"""
        return {
            'name': self.name,
            'index': self.index,
            'connection': self.connection,
            'running': self.running,
            'connected': self.cap is not None and self.cap.isOpened() if self.cap else False,
            'frames_captured': self.frames_captured,
            'fps_actual': round(self.fps_actual, 1),
            'hardware_interface': self.hardware_interface
        }


class JSONCameraStreamManager:
    """Manager für alle Kamera-Streams basierend auf JSON-Konfiguration"""
    def __init__(self, config_file: str = "cameras_config.json"):
        self.config = JSONCameraConfig(config_file)
        self.streams: Dict[int, CameraStream] = {}
        self.gui_callbacks: Dict[int, Callable] = {}
        
        print("JSONCameraStreamManager initialisiert")
    
    def reload_config(self):
        """Lade Konfiguration neu"""
        print("Lade Kamera-Konfiguration neu...")
        self.config.load_config()
        self.update_streams()
    
    def update_streams(self):
        """Aktualisiere Streams basierend auf Konfiguration"""
        print("Aktualisiere Kamera-Streams...")
        
        # Hole verfügbare Kameras aus Konfiguration
        available_cameras = self.config.get_available_cameras()
        current_indices = set(self.streams.keys())
        new_indices = set(cam['index'] for cam in available_cameras)
        
        # Entferne nicht mehr konfigurierte Streams
        for index in current_indices - new_indices:
            print(f"Entferne Stream für Kamera {index}")
            self.streams[index].disconnect()
            del self.streams[index]
        
        # Füge neue Streams hinzu
        for camera_config in available_cameras:
            index = camera_config['index']
            if index not in self.streams:
                print(f"Erstelle neuen Stream für Kamera {index}")
                callback = self.gui_callbacks.get(index)
                self.streams[index] = CameraStream(camera_config, callback)
        
        print(f"Streams aktualisiert: {len(self.streams)} aktive Streams")
    
    def start_all_streams(self):
        """Starte alle konfigurierten Streams"""
        print("Starte alle Kamera-Streams...")
        
        self.update_streams()
        
        started_count = 0
        for index, stream in self.streams.items():
            if stream.start_stream():
                started_count += 1
        
        print(f"{started_count} von {len(self.streams)} Streams gestartet")
        return started_count
    
    def stop_all_streams(self):
        """Stoppe alle Streams"""
        print("Stoppe alle Kamera-Streams...")
        
        for index, stream in self.streams.items():
            stream.stop_stream()
        
        print("Alle Streams gestoppt")
    
    def get_stream(self, index: int) -> Optional[CameraStream]:
        """Hole Stream nach Index"""
        return self.streams.get(index)
    
    def get_all_streams(self) -> Dict[int, CameraStream]:
        """Hole alle Streams"""
        return self.streams.copy()
    
    def take_photo_all(self):
        """Mache Foto von allen Kameras"""
        print("Mache Fotos von allen Kameras...")
        
        photos = {}
        for index, stream in self.streams.items():
            if stream.running:
                filename = stream.take_photo()
                if filename:
                    photos[index] = filename
        
        print(f"Fotos erstellt: {len(photos)} Kameras")
        return photos
    
    def get_status_all(self) -> Dict[int, Dict]:
        """Hole Status aller Streams"""
        status = {}
        for index, stream in self.streams.items():
            status[index] = stream.get_status()
        return status
    
    def set_gui_callback(self, index: int, callback: Callable):
        """Setze GUI-Callback für bestimmte Kamera"""
        self.gui_callbacks[index] = callback
        if index in self.streams:
            self.streams[index].on_frame_callback = callback
    
    def refresh_camera(self, index: int):
        """Aktualisiere spezifische Kamera"""
        if index in self.streams:
            stream = self.streams[index]
            was_running = stream.running
            
            # Stoppe und trenne
            stream.disconnect()
            
            # Aktualisiere Konfiguration
            camera_config = None
            for cam in self.config.get_available_cameras():
                if cam['index'] == index:
                    camera_config = cam
                    break
            
            if camera_config:
                # Erstelle neuen Stream
                callback = self.gui_callbacks.get(index)
                self.streams[index] = CameraStream(camera_config, callback)
                
                # Starte wieder wenn vorher aktiv
                if was_running:
                    self.streams[index].start_stream()
                
                print(f"Kamera {index} aktualisiert")
            else:
                # Kamera wurde aus Konfiguration entfernt
                del self.streams[index]
                print(f"Kamera {index} entfernt")
    
    def add_camera_to_config(self, index: int, connection: str, description: str, name: str = None):
        """Add new camera to configuration"""
        if self.config.add_camera(index, connection, description, name):
            self.update_streams()
            print(f"Camera {index} added")
            return True
        return False
    
    def remove_camera_from_config(self, index: int):
        """Remove camera from configuration"""
        if self.config.remove_camera(index):
            if index in self.streams:
                self.streams[index].disconnect()
                del self.streams[index]
            print(f"Camera {index} removed")
            return True
        return False
