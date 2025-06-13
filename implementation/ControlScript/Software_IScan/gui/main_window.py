"""
Main Window GUI Component
Main application window that coordinates all GUI components for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import os
from .servo_controls import ServoControls
from .stepper_controls import StepperControls
from .led_controls import LEDControls
from .webcam_display import WebcamDisplay
from .angle_calculator_gui import AngleCalculatorGUI
from .queue_management import QueueManagement
from .status_display import StatusDisplay


class MainWindow:
    """Main application window that coordinates all GUI components"""
    
    def __init__(self, title="I-Scan Wizard", default_values=None):
        """
        Initialize main window
        
        Args:
            title: Window title
            default_values: Dictionary with default values for various components
        """
        self.root = tk.Tk()
        self.root.title(title)
        
        # Set window icon
        self.setup_window_icon()
        
        # Default values
        self.defaults = default_values or {
            'base_url': "http://192.168.137.7",
            'diameter': "28",
            'speed': "80",
            'distance': "3.0",
            'direction': "1",
            'led_color': "#B00B69",
            'led_brightness': "69"
        }
        
        # Variables
        self.position = tk.DoubleVar(value=0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.base_url_var = tk.StringVar(value=self.defaults['base_url'])
        self.last_distance_value = tk.StringVar(value=self.defaults['distance'])
        self.repeat_queue = tk.BooleanVar(value=False)
        
        # GUI components
        self.status_display = None
        self.servo_controls = None
        self.stepper_controls = None
        self.led_controls = None
        self.webcam_display = None
        self.angle_calculator = None
        self.queue_management = None
        
        # Output display
        self.output = None
        
        # Button and home widgets
        self.button_exec_btn = None
        self.button_add_btn = None
        self.home_exec_btn = None
        self.home_add_btn = None
        
        # Global delay for autofocus
        self.global_delay = 0.5
        
    def setup_window_icon(self):
        """Set up the window icon"""
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(script_dir, "wizard_icon.png")
            
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
                self.root.icon_image = icon  # Keep reference
            else:
                print(f"Warning: Wizard icon not found at {icon_path}")
        except Exception as e:
            print(f"Warning: Could not load wizard icon: {e}")
    
    def create_all_widgets(self):
        """Create all GUI widgets using modular components"""
        # Status display components (URL, diameter, position)
        self.status_display = StatusDisplay(
            self.root, 
            self.position, 
            self.servo_angle_var, 
            self.base_url_var
        )
        self.status_display.create_url_frame()
        self.status_display.create_diameter_frame(self.defaults['diameter'])
        self.status_display.create_position_display()
        
        # Output display
        self.create_output_display()
        
        # Webcam display with camera settings
        webcam_callbacks = {
            'start_camera': None,  # Will be set later
            'stop_camera': None,
            'take_photo': None,
            'add_photo_to_queue': None,
            'set_camera_device': None,
            'set_delay': None
        }
        self.webcam_display = WebcamDisplay(self.root, webcam_callbacks)
        self.webcam_display.create_camera_settings_frame()
        self.webcam_display.create_webcam_frame()
        
        # Servo controls
        servo_callbacks = {
            'servo_exec': None,  # Will be set later
            'servo_add': None
        }
        self.servo_controls = ServoControls(self.root, servo_callbacks)
        self.servo_controls.create_frame()
        
        # Stepper controls
        stepper_callbacks = {
            'stepper_exec': None,  # Will be set later
            'stepper_add': None
        }
        stepper_defaults = {
            'distance': self.defaults['distance'],
            'direction': self.defaults['direction'],
            'speed': self.defaults['speed']
        }
        self.stepper_controls = StepperControls(self.root, stepper_callbacks, stepper_defaults)
        self.stepper_controls.create_frame(self.last_distance_value)
        
        # LED controls
        led_callbacks = {
            'led_exec': None,  # Will be set later
            'led_add': None,
            'bright_exec': None,
            'bright_add': None
        }
        led_defaults = {
            'color': self.defaults['led_color'],
            'brightness': self.defaults['led_brightness']
        }
        self.led_controls = LEDControls(self.root, led_callbacks, led_defaults)
        self.led_controls.create_both_frames()
        
        # Button frame for button status
        self.create_button_frame()
        
        # Home function frame
        self.create_home_frame()
        
        # Angle calculator
        calc_callbacks = {
            'execute_visualisation': None,  # Will be set later
            'execute_silent': None
        }
        self.angle_calculator = AngleCalculatorGUI(self.root, calc_callbacks)
        self.angle_calculator.create_frame()
        
        # Queue management
        queue_callbacks = {
            'queue_exec': None,  # Will be set later
            'queue_clear': None,
            'queue_remove': None,
            'queue_export': None,
            'queue_import': None
        }
        self.queue_management = QueueManagement(self.root, queue_callbacks, self.repeat_queue)
        self.queue_management.create_frame()
    
    def create_output_display(self):
        """Create the output/log display"""
        output_frame = tk.LabelFrame(self.root, text="Log-Ausgabe")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output = scrolledtext.ScrolledText(output_frame, height=8, width=80)
        self.output.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_button_frame(self):
        """Create button status query frame"""
        btn_frame = tk.LabelFrame(self.root, text="Button-Status abfragen")
        btn_frame.pack(fill="x", padx=10, pady=2)
        
        self.button_exec_btn = tk.Button(btn_frame, text="Button abfragen")
        self.button_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.button_add_btn = tk.Button(
            btn_frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.button_add_btn.pack(side=tk.LEFT)
    
    def create_home_frame(self):
        """Create home function frame"""
        home_frame = tk.LabelFrame(self.root, text="Home-Funktion")
        home_frame.pack(fill="x", padx=10, pady=2)
        
        self.home_exec_btn = tk.Button(home_frame, text="Home ausführen")
        self.home_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.home_add_btn = tk.Button(
            home_frame, 
            text="+", 
            bg="#b0c4de", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        self.home_add_btn.pack(side=tk.LEFT)
    
    def set_callbacks(self, callback_dict):
        """
        Set callbacks for all GUI components
        
        Args:
            callback_dict: Dictionary containing all callback functions
        """
        # Update webcam callbacks
        if self.webcam_display and 'webcam' in callback_dict:
            webcam_cbs = callback_dict['webcam']
            self.webcam_display.callbacks.update(webcam_cbs)
            self.webcam_display.configure_callbacks()
        
        # Update servo callbacks
        if self.servo_controls and 'servo' in callback_dict:
            servo_cbs = callback_dict['servo']
            self.servo_controls.callbacks.update(servo_cbs)
            self.servo_controls.configure_callbacks()
        
        # Update stepper callbacks
        if self.stepper_controls and 'stepper' in callback_dict:
            stepper_cbs = callback_dict['stepper']
            self.stepper_controls.callbacks.update(stepper_cbs)
            self.stepper_controls.configure_callbacks()
        
        # Update LED callbacks
        if self.led_controls and 'led' in callback_dict:
            led_cbs = callback_dict['led']
            self.led_controls.callbacks.update(led_cbs)
            self.led_controls.configure_color_callbacks()
            self.led_controls.configure_brightness_callbacks()
        
        # Update angle calculator callbacks
        if self.angle_calculator and 'calculator' in callback_dict:
            calc_cbs = callback_dict['calculator']
            self.angle_calculator.callbacks.update(calc_cbs)
        
        # Update queue callbacks
        if self.queue_management and 'queue' in callback_dict:
            queue_cbs = callback_dict['queue']
            self.queue_management.callbacks.update(queue_cbs)
            self.queue_management.configure_callbacks()
        
        # Update button and home callbacks
        if 'button_exec' in callback_dict:
            self.button_exec_btn.config(command=callback_dict['button_exec'])
        if 'button_add' in callback_dict:
            self.button_add_btn.config(command=callback_dict['button_add'])
        if 'home_exec' in callback_dict:
            self.home_exec_btn.config(command=callback_dict['home_exec'])
        if 'home_add' in callback_dict:
            self.home_add_btn.config(command=callback_dict['home_add'])
    
    def update_position_label(self):
        """Update position and servo angle labels"""
        if self.status_display:
            self.status_display.update_position_label()
    
    def set_camera_device_index(self):
        """Set camera device index from webcam display"""
        if self.webcam_display:
            return self.webcam_display.get_camera_device_index()
        return 0
    
    def set_global_delay(self):
        """Set global delay from webcam display"""
        if self.webcam_display:
            self.global_delay = self.webcam_display.get_camera_delay()
    
    def get_all_widgets(self):
        """Return dictionary of all widgets for external access"""
        widgets = {
            'root': self.root,
            'output': self.output,
            'position': self.position,
            'servo_angle_var': self.servo_angle_var,
            'base_url_var': self.base_url_var,
            'last_distance_value': self.last_distance_value,
            'repeat_queue': self.repeat_queue,
            'global_delay': self.global_delay,
            'update_position_label': self.update_position_label
        }
        
        # Add component widgets
        if self.status_display:
            widgets.update({'status_' + k: v for k, v in self.status_display.get_widgets().items()})
        if self.servo_controls:
            widgets.update({'servo_' + k: v for k, v in self.servo_controls.get_widgets().items()})
        if self.stepper_controls:
            widgets.update({'stepper_' + k: v for k, v in self.stepper_controls.get_widgets().items()})
        if self.led_controls:
            widgets.update({'led_' + k: v for k, v in self.led_controls.get_widgets().items()})
        if self.webcam_display:
            widgets.update({'webcam_' + k: v for k, v in self.webcam_display.get_widgets().items()})
        if self.angle_calculator:
            widgets.update({'calc_' + k: v for k, v in self.angle_calculator.get_widgets().items()})
        if self.queue_management:
            widgets.update({'queue_' + k: v for k, v in self.queue_management.get_widgets().items()})
        
        # Add button and home widgets
        widgets.update({
            'button_exec_btn': self.button_exec_btn,
            'button_add_btn': self.button_add_btn,
            'home_exec_btn': self.home_exec_btn,
            'home_add_btn': self.home_add_btn
        })
        
        return widgets
    
    def run(self):
        """Start the main application loop"""
        self.root.mainloop()
    
    def on_closing(self, callback=None):
        """Handle window closing event"""
        if callback:
            callback()
        self.root.destroy()
