"""
LED Controls GUI Component
Contains LED color and brightness control interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk


class LEDControls:
    """GUI component for LED control (color and brightness)"""
    
    def __init__(self, parent, callbacks=None, default_values=None):
        """
        Initialize LED controls
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
            default_values: Dictionary with default values for fields
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        self.defaults = default_values or {
            'color': '#B00B69',
            'brightness': '69'
        }
        
        # Color control widgets
        self.color_frame = None
        self.led_color = None
        self.led_exec_btn = None
        self.led_add_btn = None
        
        # Brightness control widgets
        self.brightness_frame = None
        self.led_bright = None
        self.bright_exec_btn = None
        self.bright_add_btn = None
        
    def create_color_frame(self):
        """Create the LED color control frame and widgets"""
        self.color_frame = tk.LabelFrame(self.parent, text="LED-Farbe setzen")
        self.color_frame.pack(fill="x", padx=10, pady=2)
        
        # Color input
        tk.Label(self.color_frame, text="Farbe (z.B. #FF0000):").pack(side=tk.LEFT)
        self.led_color = tk.Entry(self.color_frame, width=10)
        self.led_color.insert(0, self.defaults['color'])
        self.led_color.pack(side=tk.LEFT)
        
        # Control buttons
        self.led_exec_btn = tk.Button(self.color_frame, text="LED ausführen")
        self.led_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.led_add_btn = tk.Button(
            self.color_frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.led_add_btn.pack(side=tk.LEFT)
        
        # Configure callbacks
        self.configure_color_callbacks()
        
        return self.color_frame
    
    def create_brightness_frame(self):
        """Create the LED brightness control frame and widgets"""
        self.brightness_frame = tk.LabelFrame(self.parent, text="LED-Helligkeit setzen")
        self.brightness_frame.pack(fill="x", padx=10, pady=2)
        
        # Brightness input
        tk.Label(self.brightness_frame, text="Helligkeit (0-100):").pack(side=tk.LEFT)
        self.led_bright = tk.Entry(self.brightness_frame, width=5)
        self.led_bright.insert(0, self.defaults['brightness'])
        self.led_bright.pack(side=tk.LEFT)
        
        # Control buttons
        self.bright_exec_btn = tk.Button(self.brightness_frame, text="Helligkeit ausführen")
        self.bright_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.bright_add_btn = tk.Button(
            self.brightness_frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.bright_add_btn.pack(side=tk.LEFT)
        
        # Configure callbacks
        self.configure_brightness_callbacks()
        
        return self.brightness_frame
    
    def create_both_frames(self):
        """Create both color and brightness frames"""
        color_frame = self.create_color_frame()
        brightness_frame = self.create_brightness_frame()
        return color_frame, brightness_frame
    
    def configure_color_callbacks(self):
        """Configure color control callbacks"""
        if 'led_exec' in self.callbacks:
            self.led_exec_btn.config(command=self.callbacks['led_exec'])
        if 'led_add' in self.callbacks:
            self.led_add_btn.config(command=self.callbacks['led_add'])
    
    def configure_brightness_callbacks(self):
        """Configure brightness control callbacks"""
        if 'bright_exec' in self.callbacks:
            self.bright_exec_btn.config(command=self.callbacks['bright_exec'])
        if 'bright_add' in self.callbacks:
            self.bright_add_btn.config(command=self.callbacks['bright_add'])
    
    def get_color(self):
        """Get the LED color value from input field"""
        return self.led_color.get() if self.led_color else None
    
    def get_brightness(self):
        """Get the LED brightness value from input field"""
        try:
            return int(self.led_bright.get()) if self.led_bright else None
        except ValueError:
            return None
    
    def set_color(self, color):
        """Set the LED color value in input field"""
        if self.led_color:
            self.led_color.delete(0, tk.END)
            self.led_color.insert(0, color)
    
    def set_brightness(self, brightness):
        """Set the LED brightness value in input field"""
        if self.led_bright:
            self.led_bright.delete(0, tk.END)
            self.led_bright.insert(0, str(brightness))
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'color_frame': self.color_frame,
            'brightness_frame': self.brightness_frame,
            'led_color': self.led_color,
            'led_bright': self.led_bright,
            'led_exec_btn': self.led_exec_btn,
            'led_add_btn': self.led_add_btn,
            'bright_exec_btn': self.bright_exec_btn,
            'bright_add_btn': self.bright_add_btn
        }
