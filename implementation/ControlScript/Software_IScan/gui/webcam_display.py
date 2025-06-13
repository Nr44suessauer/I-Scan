"""
Webcam Display GUI Component
Contains webcam display and camera control interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk
import threading


class WebcamDisplay:
    """GUI component for webcam display and controls"""
    
    def __init__(self, parent, callbacks=None, webcam_helper=None):
        """
        Initialize webcam display
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
            webcam_helper: WebcamHelper instance
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        self.webcam_helper = webcam_helper
        
        self.frame = None
        self.webcam_label = None
        self.btn_start_camera = None
        self.btn_stop_camera = None
        self.btn_take_photo = None
        self.btn_add_photo_to_queue = None
        
        # Camera device settings
        self.camera_device_index_var = None
        self.camera_device_entry = None
        self.set_camera_device_btn = None
        
        # Delay settings
        self.camera_delay_var = None
        self.camera_delay_entry = None
        self.set_delay_btn = None
        
    def create_camera_settings_frame(self):
        """Create camera settings frame with device index and delay controls"""
        camera_settings_frame = tk.Frame(self.parent)
        camera_settings_frame.pack(fill="x", padx=10, pady=(2, 2))
        
        # Device index setting
        tk.Label(camera_settings_frame, text="Kamera Device Index (z.B. 0, 1, 2):").pack(side=tk.LEFT)
        self.camera_device_index_var = tk.StringVar(value="0")
        self.camera_device_entry = tk.Entry(camera_settings_frame, width=5, textvariable=self.camera_device_index_var)
        self.camera_device_entry.pack(side=tk.LEFT)
        self.set_camera_device_btn = tk.Button(camera_settings_frame, text="Setzen")
        self.set_camera_device_btn.pack(side=tk.LEFT, padx=5)
        
        # Autofocus delay setting
        tk.Label(camera_settings_frame, text="  Autofokus-Delay (s):").pack(side=tk.LEFT, padx=(20, 0))
        self.camera_delay_var = tk.StringVar(value="0.5")
        self.camera_delay_entry = tk.Entry(camera_settings_frame, width=5, textvariable=self.camera_delay_var)
        self.camera_delay_entry.pack(side=tk.LEFT)
        self.set_delay_btn = tk.Button(camera_settings_frame, text="set")
        self.set_delay_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure callbacks
        if 'set_camera_device' in self.callbacks:
            self.set_camera_device_btn.config(command=self.callbacks['set_camera_device'])
        if 'set_delay' in self.callbacks:
            self.set_delay_btn.config(command=self.callbacks['set_delay'])
        
        return camera_settings_frame
    
    def create_webcam_frame(self):
        """Create the webcam display frame and controls"""
        self.frame = tk.LabelFrame(self.parent, text="Webcam")
        self.frame.pack(fill="x", padx=10, pady=2)
        
        # Webcam display
        self.webcam_label = tk.Label(self.frame, text="Kamera nicht aktiv", width=40, height=15, bg="lightgray")
        self.webcam_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Control buttons frame
        buttons_frame = tk.Frame(self.frame)
        buttons_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill="y")
        
        # Camera control buttons
        self.btn_start_camera = tk.Button(buttons_frame, text="Kamera starten", width=15)
        self.btn_start_camera.pack(pady=2)
        
        self.btn_stop_camera = tk.Button(buttons_frame, text="Kamera stoppen", width=15)
        self.btn_stop_camera.pack(pady=2)
        
        self.btn_take_photo = tk.Button(buttons_frame, text="Foto machen", width=15)
        self.btn_take_photo.pack(pady=2)
        
        self.btn_add_photo_to_queue = tk.Button(
            buttons_frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.btn_add_photo_to_queue.pack(pady=2)
        
        # Configure callbacks
        self.configure_callbacks()
        
        return self.frame
    
    def configure_callbacks(self):
        """Configure button callbacks"""
        if 'start_camera' in self.callbacks:
            self.btn_start_camera.config(command=self.callbacks['start_camera'])
        if 'stop_camera' in self.callbacks:
            self.btn_stop_camera.config(command=self.callbacks['stop_camera'])
        if 'take_photo' in self.callbacks:
            self.btn_take_photo.config(command=self.callbacks['take_photo'])
        if 'add_photo_to_queue' in self.callbacks:
            self.btn_add_photo_to_queue.config(command=self.callbacks['add_photo_to_queue'])
    
    def update_webcam_display(self, image):
        """Update the webcam display with new image"""
        if self.webcam_label and image:
            self.webcam_label.config(image=image, text="")
            self.webcam_label.image = image  # Keep reference to prevent garbage collection
    
    def set_webcam_status(self, status_text):
        """Set webcam status text"""
        if self.webcam_label:
            self.webcam_label.config(image="", text=status_text)
    
    def get_camera_device_index(self):
        """Get camera device index from input"""
        try:
            return int(self.camera_device_index_var.get()) if self.camera_device_index_var else 0
        except ValueError:
            return 0
    
    def get_camera_delay(self):
        """Get camera delay from input"""
        try:
            return float(self.camera_delay_var.get()) if self.camera_delay_var else 0.5
        except ValueError:
            return 0.5
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'frame': self.frame,
            'webcam_label': self.webcam_label,
            'btn_start_camera': self.btn_start_camera,
            'btn_stop_camera': self.btn_stop_camera,
            'btn_take_photo': self.btn_take_photo,
            'btn_add_photo_to_queue': self.btn_add_photo_to_queue,
            'camera_device_index_var': self.camera_device_index_var,
            'camera_device_entry': self.camera_device_entry,
            'set_camera_device_btn': self.set_camera_device_btn,
            'camera_delay_var': self.camera_delay_var,
            'camera_delay_entry': self.camera_delay_entry,
            'set_delay_btn': self.set_delay_btn
        }
