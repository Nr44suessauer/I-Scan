
"""
JSON-based camera configuration
Manages camera settings via JSON file
"""

import json
import os
from typing import List, Dict, Optional


class JSONCameraConfig:
    """JSON-based camera configuration"""
    
    def __init__(self, config_file: str = "cameras_config.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config_data = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"JSON configuration loaded: {len(self.get_cameras())} cameras")
                return True
            else:
                print(f"Configuration file not found: {self.config_file}")
                self.create_default_config()
                return False
        except Exception as e:
            print(f"Error loading JSON configuration: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            print("JSON configuration saved")
            return True
        except Exception as e:
            print(f"Error saving JSON configuration: {e}")
            return False
    
    def create_default_config(self):
        """Create default configuration"""
        self.config_data = {
            "cameras": [
                {
                    "index": 0,
                    "connection": "USB:0",
                    "description": "Default USB camera",
                    "name": "Camera 1",
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
        """Get all camera configurations"""
        return self.config_data.get('cameras', [])
    
    def get_enabled_cameras(self) -> List[Dict]:
        """Get only enabled cameras"""
        return [cam for cam in self.get_cameras() if cam.get('enabled', True)]
    
    def get_camera_by_index(self, index: int) -> Optional[Dict]:
        """Get camera by index"""
        for camera in self.get_cameras():
            if camera.get('index') == index:
                return camera
        return None
    
    def add_camera(self, index: int, connection: str, description: str, name: str = None) -> bool:
        """Add new camera"""
        try:
            if 'cameras' not in self.config_data:
                self.config_data['cameras'] = []
            # Check if index already exists
            if self.get_camera_by_index(index):
                print(f"Camera with index {index} already exists")
                return False
            new_camera = {
                "index": index,
                "connection": connection,
                "description": description,
                "name": name or f"Camera {index + 1}",
                "enabled": True,
                "resolution": [640, 480],
                "fps": 30
            }
            self.config_data['cameras'].append(new_camera)
            return self.save_config()
        except Exception as e:
            print(f"Error adding camera: {e}")
            return False
    
    def update_camera(self, index: int, **kwargs) -> bool:
        """Update camera settings"""
        try:
            camera = self.get_camera_by_index(index)
            if not camera:
                print(f"Camera with index {index} not found")
                return False
            # Update fields
            for key, value in kwargs.items():
                if key in camera:
                    camera[key] = value
            return self.save_config()
        except Exception as e:
            print(f"Error updating camera: {e}")
            return False
    
    def remove_camera(self, index: int) -> bool:
        """Remove camera"""
        try:
            cameras = self.config_data.get('cameras', [])
            original_count = len(cameras)
            self.config_data['cameras'] = [cam for cam in cameras if cam.get('index') != index]
            if len(self.config_data['cameras']) < original_count:
                return self.save_config()
            else:
                print(f"Camera with index {index} not found")
                return False
        except Exception as e:
            print(f"Error removing camera: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Get global settings"""
        return self.config_data.get('settings', {})
    
    def update_settings(self, **kwargs) -> bool:
        """Update global settings"""
        try:
            if 'settings' not in self.config_data:
                self.config_data['settings'] = {}
            for key, value in kwargs.items():
                self.config_data['settings'][key] = value
            return self.save_config()
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def parse_connection(self, connection: str) -> Dict:
        """Parse connection string and extract hardware interface"""
        try:
            if connection.startswith("USB:"):
                device_index = int(connection.split(":")[1])
                return {
                    "type": "usb",
                    "device_index": device_index,
                    "interface": f"/dev/video{device_index}" if os.name != 'nt' else device_index
                }
            elif connection.startswith("IP:"):
                ip_address = connection.split(":")[1]
                return {
                    "type": "network",
                    "ip_address": ip_address,
                    "interface": f"rtsp://{ip_address}/stream"
                }
            elif connection.startswith("COM:"):
                com_port = connection.split(":")[1]
                return {
                    "type": "serial",
                    "com_port": com_port,
                    "interface": f"COM{com_port}"
                }
            else:
                # Fallback: versuche als direkte USB-Index
                try:
                    device_index = int(connection)
                    return {
                        "type": "usb",
                        "device_index": device_index,
                        "interface": device_index
                    }
                except ValueError:
                    print(f"Unknown connection format: {connection}")
                    return None
        except Exception as e:
            print(f"Error parsing connection '{connection}': {e}")
            return None
    
    def get_available_cameras(self) -> List[Dict]:
        """Get all available cameras with hardware interface info"""
        available_cameras = []
        for camera in self.get_enabled_cameras():
            connection_info = self.parse_connection(camera['connection'])
            if connection_info:
                camera_info = camera.copy()
                camera_info['hardware_interface'] = connection_info
                available_cameras.append(camera_info)
        return available_cameras
