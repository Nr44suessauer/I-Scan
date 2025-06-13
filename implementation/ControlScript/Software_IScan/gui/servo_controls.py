"""
Servo Controls GUI Component
Contains servo control interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk


class ServoControls:
    """GUI component for servo motor control"""
    
    def __init__(self, parent, callbacks=None):
        """
        Initialize servo controls
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        self.frame = None
        self.servo_angle = None
        self.servo_exec_btn = None
        self.servo_add_btn = None
        
    def create_frame(self):
        """Create the servo control frame and widgets"""
        self.frame = tk.LabelFrame(self.parent, text="Servo Control")
        self.frame.pack(fill="x", padx=10, pady=2)
        
        # Angle input
        tk.Label(self.frame, text="Angle (0-90):").pack(side=tk.LEFT)
        self.servo_angle = tk.Entry(self.frame, width=5)
        self.servo_angle.pack(side=tk.LEFT)
        
        # Control buttons
        self.servo_exec_btn = tk.Button(self.frame, text="Execute Servo")
        self.servo_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.servo_add_btn = tk.Button(
            self.frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.servo_add_btn.pack(side=tk.LEFT)
        
        # Configure callbacks
        self.configure_callbacks()
        
        return self.frame
    
    def configure_callbacks(self):
        """Configure button callbacks"""
        if 'servo_exec' in self.callbacks:
            self.servo_exec_btn.config(command=self.callbacks['servo_exec'])
        if 'servo_add' in self.callbacks:
            self.servo_add_btn.config(command=self.callbacks['servo_add'])
    
    def get_angle(self):
        """Get the servo angle value from input field"""
        try:
            return int(self.servo_angle.get())
        except ValueError:
            return None
    
    def set_angle(self, angle):
        """Set the servo angle value in input field"""
        self.servo_angle.delete(0, tk.END)
        self.servo_angle.insert(0, str(angle))
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'frame': self.frame,
            'servo_angle': self.servo_angle,
            'servo_exec_btn': self.servo_exec_btn,
            'servo_add_btn': self.servo_add_btn
        }
