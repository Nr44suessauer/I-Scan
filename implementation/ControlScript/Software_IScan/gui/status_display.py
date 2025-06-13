"""
Status Display GUI Component
Contains position, servo angle display, and diameter input for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk


class StatusDisplay:
    """GUI component for status display and basic settings"""
    
    def __init__(self, parent, position_var=None, servo_angle_var=None, base_url_var=None):
        """
        Initialize status display
        
        Args:
            parent: Parent widget
            position_var: DoubleVar for position display
            servo_angle_var: IntVar for servo angle display
            base_url_var: StringVar for base URL
        """
        self.parent = parent
        self.position_var = position_var
        self.servo_angle_var = servo_angle_var
        self.base_url_var = base_url_var
        
        # URL frame widgets
        self.url_frame = None
        self.base_url_entry = None
        
        # Diameter frame widgets
        self.diameter_frame = None
        self.diameter_entry = None
        
        # Position display widgets
        self.position_frame = None
        self.position_label = None
        self.servo_angle_label = None
        
    def create_url_frame(self):
        """Create the URL input frame"""
        self.url_frame = tk.Frame(self.parent)
        self.url_frame.pack(fill="x", padx=10, pady=(10, 2))
        
        tk.Label(self.url_frame, text="API-Adresse:").pack(side=tk.LEFT)
        self.base_url_entry = tk.Entry(self.url_frame, textvariable=self.base_url_var, width=30)
        self.base_url_entry.pack(side=tk.LEFT, padx=5)
        
        return self.url_frame
    
    def create_diameter_frame(self, default_diameter="28"):
        """
        Create the diameter input frame
        
        Args:
            default_diameter: Default diameter value
        """
        self.diameter_frame = tk.Frame(self.parent)
        self.diameter_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(self.diameter_frame, text="Zahnraddurchmesser (mm):").pack(side=tk.LEFT)
        self.diameter_entry = tk.Entry(self.diameter_frame, width=10)
        self.diameter_entry.insert(0, default_diameter)
        self.diameter_entry.pack(side=tk.LEFT, padx=5)
        
        return self.diameter_frame
    
    def create_position_display(self):
        """Create the position and servo angle display"""
        self.position_frame = tk.Frame(self.parent)
        self.position_frame.pack(fill="x", padx=10, pady=2)
        
        # Position display
        tk.Label(self.position_frame, text="Position (mm):").pack(side=tk.LEFT)
        self.position_label = tk.Label(
            self.position_frame, 
            text="0.00", 
            relief="sunken", 
            width=10, 
            font=("Arial", 10, "bold")
        )
        self.position_label.pack(side=tk.LEFT, padx=5)
        
        # Servo angle display
        tk.Label(self.position_frame, text="Servo-Winkel (°):").pack(side=tk.LEFT, padx=(20, 0))
        self.servo_angle_label = tk.Label(
            self.position_frame, 
            text="0", 
            relief="sunken", 
            width=5, 
            font=("Arial", 10, "bold")
        )
        self.servo_angle_label.pack(side=tk.LEFT, padx=5)
        
        return self.position_frame
    
    def update_position_label(self):
        """Update the position and servo angle labels with current values"""
        if self.position_label and self.position_var:
            self.position_label.config(text=f"{self.position_var.get():.2f}")
        if self.servo_angle_label and self.servo_angle_var:
            self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.parent.update_idletasks()
    
    def get_diameter(self):
        """Get diameter value from input field"""
        try:
            return float(self.diameter_entry.get()) if self.diameter_entry else None
        except ValueError:
            return None
    
    def set_diameter(self, diameter):
        """Set diameter value in input field"""
        if self.diameter_entry:
            self.diameter_entry.delete(0, tk.END)
            self.diameter_entry.insert(0, str(diameter))
    
    def get_base_url(self):
        """Get base URL from input field"""
        return self.base_url_var.get() if self.base_url_var else ""
    
    def set_base_url(self, url):
        """Set base URL in input field"""
        if self.base_url_var:
            self.base_url_var.set(url)
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'url_frame': self.url_frame,
            'base_url_entry': self.base_url_entry,
            'diameter_frame': self.diameter_frame,
            'diameter_entry': self.diameter_entry,
            'position_frame': self.position_frame,
            'position_label': self.position_label,
            'servo_angle_label': self.servo_angle_label
        }
