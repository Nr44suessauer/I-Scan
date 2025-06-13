"""
Stepper Motor Controls GUI Component
Contains stepper motor control interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk


class StepperControls:
    """GUI component for stepper motor control"""
    
    def __init__(self, parent, callbacks=None, default_values=None):
        """
        Initialize stepper controls
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
            default_values: Dictionary with default values for fields
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        self.defaults = default_values or {
            'distance': '3.0',
            'direction': '1',
            'speed': '80'
        }
        
        self.frame = None
        self.stepper_length_cm = None
        self.stepper_dir = None
        self.stepper_speed = None
        self.stepper_exec_btn = None
        self.stepper_add_btn = None
        
    def create_frame(self, distance_var=None):
        """
        Create the stepper control frame and widgets
        
        Args:
            distance_var: StringVar for distance input (optional)
        """
        self.frame = tk.LabelFrame(self.parent, text="Schrittmotor-Steuerung")
        self.frame.pack(fill="x", padx=10, pady=2)
        
        # Distance input
        tk.Label(self.frame, text="Distanz (cm):").pack(side=tk.LEFT)
        if distance_var:
            self.stepper_length_cm = tk.Entry(self.frame, width=8, textvariable=distance_var)
        else:
            self.stepper_length_cm = tk.Entry(self.frame, width=8)
            self.stepper_length_cm.insert(0, self.defaults['distance'])
        self.stepper_length_cm.pack(side=tk.LEFT)
        
        # Direction input
        tk.Label(self.frame, text="Richtung (1/-1):").pack(side=tk.LEFT)
        self.stepper_dir = tk.Entry(self.frame, width=4)
        self.stepper_dir.insert(0, self.defaults['direction'])
        self.stepper_dir.pack(side=tk.LEFT)
        
        # Speed input
        tk.Label(self.frame, text="Geschwindigkeit (opt.):").pack(side=tk.LEFT)
        self.stepper_speed = tk.Entry(self.frame, width=6)
        self.stepper_speed.insert(0, self.defaults['speed'])
        self.stepper_speed.pack(side=tk.LEFT)
        
        # Control buttons
        self.stepper_exec_btn = tk.Button(self.frame, text="Stepper ausführen")
        self.stepper_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.stepper_add_btn = tk.Button(
            self.frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.stepper_add_btn.pack(side=tk.LEFT)
        
        # Configure callbacks
        self.configure_callbacks()
        
        return self.frame
    
    def configure_callbacks(self):
        """Configure button callbacks"""
        if 'stepper_exec' in self.callbacks:
            self.stepper_exec_btn.config(command=self.callbacks['stepper_exec'])
        if 'stepper_add' in self.callbacks:
            self.stepper_add_btn.config(command=self.callbacks['stepper_add'])
    
    def get_values(self):
        """Get all stepper values from input fields"""
        try:
            return {
                'distance': float(self.stepper_length_cm.get()),
                'direction': int(self.stepper_dir.get()),
                'speed': int(self.stepper_speed.get()) if self.stepper_speed.get() else None
            }
        except ValueError:
            return None
    
    def set_values(self, distance=None, direction=None, speed=None):
        """Set values in input fields"""
        if distance is not None:
            self.stepper_length_cm.delete(0, tk.END)
            self.stepper_length_cm.insert(0, str(distance))
        if direction is not None:
            self.stepper_dir.delete(0, tk.END)
            self.stepper_dir.insert(0, str(direction))
        if speed is not None:
            self.stepper_speed.delete(0, tk.END)
            self.stepper_speed.insert(0, str(speed))
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'frame': self.frame,
            'stepper_length_cm': self.stepper_length_cm,
            'stepper_dir': self.stepper_dir,
            'stepper_speed': self.stepper_speed,
            'stepper_exec_btn': self.stepper_exec_btn,
            'stepper_add_btn': self.stepper_add_btn
        }
