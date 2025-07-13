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
        """Connect to the camera"""
        try:
            if self.hardware_interface.get('type') == 'usb':
                device_index = self.hardware_interface.get('device_index', 0)
                self.cap = cv2.VideoCapture(device_index)
                
                if not self.cap.isOpened():
                    print(f"Error: Cannot open USB camera {device_index}")
                    return False
                
                # Set resolution if configured
                if 'resolution' in self.config:
                    width, height = self.config['resolution']
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                # Set FPS if configured
                if 'fps' in self.config:
                    self.cap.set(cv2.CAP_PROP_FPS, self.config['fps'])
                
                print(f"USB camera {device_index} connected successfully")
                return True
            
            elif self.hardware_interface.get('type') == 'network':
                # Network camera (RTSP, HTTP, etc.)
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
            print(f"Error connecting to camera {self.name}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect camera"""
        self.stop_stream()
        if self.cap:
            self.cap.release()
            self.cap = None
        print(f"Camera {self.name} disconnected")
    
    def start_stream(self) -> bool:
        """Start stream"""
        if self.running:
            print(f"Stream for {self.name} is already running")
            return True
        
        if not self.cap or not self.cap.isOpened():
            if not self.connect():
                return False
        
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()
        print(f"Stream for {self.name} started")
        return True
    
    def stop_stream(self):
        """Stop stream"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=2)
            print(f"Stream for {self.name} stopped")
    
    def _stream_loop(self):
        """Stream loop (runs in separate thread)"""
        while self.running:
            try:
                if not self.cap or not self.cap.isOpened():
                    print(f"Camera {self.name} not connected")
                    break
                
                ret, frame = self.cap.read()
                if not ret:
                    print(f"No frame received from camera {self.name}")
                    time.sleep(0.1)
                    continue
                
                # Safely store frame
                with self.frame_lock:
                    self.current_frame = frame.copy()
                    self.frames_captured += 1
                    
                    # Calculate FPS
                    current_time = time.time()
                    if self.last_frame_time > 0:
                        time_diff = current_time - self.last_frame_time
                        if time_diff > 0:
                            self.fps_actual = 1.0 / time_diff
                    self.last_frame_time = current_time
                
                # Call callback if available
                if self.on_frame_callback:
                    self.on_frame_callback(self.index, frame)
                
                # Short pause to save CPU
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Error in stream loop for {self.name}: {e}")
                time.sleep(0.5)
    
    def get_frame(self):
        """Get current frame (thread-safe)"""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def take_photo(self):
        """Take photo"""
        frame = self.get_frame()
        if frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{self.name}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Photo saved: {filename}")
            return filename
        else:
            print(f"No frame available for photo from {self.name}")
            return None
    
    def get_status(self) -> Dict:
        """Get stream status"""
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
    """Manager for all camera streams based on JSON configuration"""
    def __init__(self, config_file: str = "cameras_config.json"):
        self.config = JSONCameraConfig(config_file)
        self.streams: Dict[int, CameraStream] = {}
        self.gui_callbacks: Dict[int, Callable] = {}
        
        print("JSONCameraStreamManager initialized")
    
    def reload_config(self):
        """Reload configuration"""
        print("Reloading camera configuration...")
        self.config.load_config()
        self.update_streams()
    
    def update_streams(self):
        """Update streams based on configuration"""
        print("Updating camera streams...")
        
        # Get available cameras from configuration
        available_cameras = self.config.get_available_cameras()
        current_indices = set(self.streams.keys())
        new_indices = set(cam['index'] for cam in available_cameras)
        
        # Remove streams no longer configured
        for index in current_indices - new_indices:
            print(f"Removing stream for camera {index}")
            self.streams[index].disconnect()
            del self.streams[index]
        
        # Add new streams
        for camera_config in available_cameras:
            index = camera_config['index']
            if index not in self.streams:
                print(f"Creating new stream for camera {index}")
                callback = self.gui_callbacks.get(index)
                self.streams[index] = CameraStream(camera_config, callback)
        
        print(f"Streams updated: {len(self.streams)} active streams")
    
    def start_all_streams(self):
        """Start all configured streams"""
        print("Starting all camera streams...")
        
        self.update_streams()
        
        started_count = 0
        for index, stream in self.streams.items():
            if stream.start_stream():
                started_count += 1
        
        print(f"{started_count} of {len(self.streams)} streams started")
        return started_count
    
    def stop_all_streams(self):
        """Stop all streams"""
        print("Stopping all camera streams...")
        
        for index, stream in self.streams.items():
            stream.stop_stream()
        
        print("All streams stopped")
    
    def get_stream(self, index: int) -> Optional[CameraStream]:
        """Get stream by index"""
        return self.streams.get(index)
    
    def get_all_streams(self) -> Dict[int, CameraStream]:
        """Get all streams"""
        return self.streams.copy()
    
    def take_photo_all(self):
        """Take photo from all cameras"""
        print("Taking photos from all cameras...")
        
        photos = {}
        for index, stream in self.streams.items():
            if stream.running:
                filename = stream.take_photo()
                if filename:
                    photos[index] = filename
        
        print(f"Photos created: {len(photos)} cameras")
        return photos
    
    def get_status_all(self) -> Dict[int, Dict]:
        """Get status of all streams"""
        status = {}
        for index, stream in self.streams.items():
            status[index] = stream.get_status()
        return status
    
    def set_gui_callback(self, index: int, callback: Callable):
        """Set GUI callback for specific camera"""
        self.gui_callbacks[index] = callback
        if index in self.streams:
            self.streams[index].on_frame_callback = callback
    
    def refresh_camera(self, index: int):
        """Refresh specific camera"""
        if index in self.streams:
            stream = self.streams[index]
            was_running = stream.running
            
            # Stop and disconnect
            stream.disconnect()
            
            # Update configuration
            camera_config = None
            for cam in self.config.get_available_cameras():
                if cam['index'] == index:
                    camera_config = cam
                    break
            
            if camera_config:
                # Create new stream
                callback = self.gui_callbacks.get(index)
                self.streams[index] = CameraStream(camera_config, callback)
                
                # Restart if previously active
                if was_running:
                    self.streams[index].start_stream()
                
                print(f"Camera {index} refreshed")
            else:
                # Camera was removed from configuration
                del self.streams[index]
                print(f"Camera {index} removed")
    
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
