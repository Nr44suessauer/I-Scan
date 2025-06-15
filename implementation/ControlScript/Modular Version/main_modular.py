"""
IScan-ControlScript - Main Program (Modular Structure)
A GUI application for controlling hardware via an API interface.
This version uses a modular, maintainable structure that's easy to extend.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""

import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Import configuration and components
from config import *
from gui_components import GUIBuilder
from event_handlers import EventHandlers
from queue_operations import QueueOperations

# Import existing modules
from api_client import ApiClient
from logger import Logger
from device_control import DeviceControl
from operation_queue import OperationQueue
from webcam_helper import WebcamHelper
from angle_calculator_commands import AngleCalculatorInterface


class ControlApp:
    """
    Main application class with modular structure
    Easy to understand, debug, and extend
    """
    
    def __init__(self):
        """Initialize the application"""
        # Create main window
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.setup_window_icon()
        
        # Initialize variables
        self.init_variables()
          # Initialize webcam with smaller frame size for side-by-side layout
        self.webcam = WebcamHelper(device_index=DEFAULT_CAMERA_DEVICE, 
                                 frame_size=(300, 300))
        
        # Create GUI components
        self.create_all_widgets()
        
        # Initialize backend modules
        self.init_backend_modules()
        
        # Initialize helper classes
        self.event_handlers = EventHandlers(self)
        self.queue_ops = QueueOperations(self)
          # Assign all callbacks
        self.event_handlers.assign_all_callbacks()
        
        # Initialize calculator display and load images
        self.initialize_calculator_display()
        
        # Setup close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_window_icon(self):
        """Set up the window icon"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, ICON_FILENAME)
            
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
                self.root.icon_image = icon  # Keep reference
            else:
                print(f"Warning: Icon not found at {icon_path}")
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
    
    def init_variables(self):
        """Initialize all tkinter variables"""
        self.position = tk.DoubleVar(value=0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.base_url_var = tk.StringVar(value=DEFAULT_BASE_URL)
        self.last_distance_value = tk.StringVar(value=DEFAULT_DISTANCE)
        self.repeat_queue = tk.BooleanVar(value=DEFAULT_REPEAT_QUEUE)
        self.global_delay = DEFAULT_AUTOFOCUS_DELAY
    
    def create_all_widgets(self):
        """Create all GUI widgets using GUIBuilder"""
        # URL input
        self.url_frame, self.base_url_entry = GUIBuilder.create_url_frame(
            self.root, self.base_url_var)
        
        # Camera settings
        (self.camera_settings_frame, self.camera_device_index_var, 
         self.camera_device_entry, self.set_camera_device_btn,
         self.camera_delay_var, self.camera_delay_entry, 
         self.set_delay_btn) = GUIBuilder.create_camera_settings_frame(self.root)
        
        # Diameter input
        self.diameter_frame, self.diameter_entry = GUIBuilder.create_diameter_frame(self.root)        # Position display
        (self.position_frame, self.position_label, 
         self.servo_angle_label) = GUIBuilder.create_position_display(
            self.root, self.position, self.servo_angle_var)
          # Main container for 3-column grid layout (Log | Configuration | Queue) + Camera row
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid configuration for 3 columns in first row, camera in second row
        self.main_container.columnconfigure(0, weight=1, minsize=300)  # Log console
        self.main_container.columnconfigure(1, weight=1, minsize=400)  # Calculator/Config (wider)
        self.main_container.columnconfigure(2, weight=1, minsize=300)  # Queue
        self.main_container.rowconfigure(0, weight=1)  # Main controls row
        self.main_container.rowconfigure(1, weight=1)  # Camera row
        
        # Row 0, Column 0: Log console
        self.log_frame = tk.LabelFrame(self.main_container, text="Log Console", font=("Arial", 10, "bold"))
        self.log_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        self.output = scrolledtext.ScrolledText(self.log_frame, width=35, height=20, state='disabled')
        self.output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Row 0, Column 1: Calculator Commands Panel (Configuration)
        (self.calc_panel, self.calc_vars, 
         self.calc_widgets) = GUIBuilder.create_calculator_commands_panel(
            self.main_container, grid_mode=True)
        
        # Row 0, Column 2: Operation Queue
        (self.queue_frame, self.queue_list, self.queue_exec_btn, self.queue_pause_btn, 
         self.queue_exec_selected_btn, self.queue_clear_btn, self.queue_remove_btn, 
         self.queue_duplicate_btn, self.queue_edit_btn, self.queue_settings_btn, 
         self.queue_move_up_btn, self.queue_move_down_btn,
         self.queue_export_btn, self.queue_import_btn, self.repeat_checkbox) = GUIBuilder.create_queue_frame(
            self.main_container, self.repeat_queue, grid_mode=True)
        
        # Row 1: Camera Stream Display (spans all 3 columns)
        (self.webcam_frame, self.camera_label, self.btn_start_camera,
         self.btn_stop_camera, self.btn_take_photo, 
         self.btn_add_photo_to_queue) = GUIBuilder.create_webcam_frame(self.main_container, grid_mode=True)
    
    def init_backend_modules(self):
        """Initialize backend modules (logger, device control, etc.)"""
        # Logger
        self.logger = Logger(
            self.output, 
            self.position, 
            self.servo_angle_var, 
            self.update_position_label
        )        # Widget dictionary for device control - create necessary control variables
        # Since controls are now in Calculator panel, we need to define these here
        self.servo_angle = tk.DoubleVar(value=0.0)
        self.stepper_length_cm = tk.DoubleVar(value=1.0)
        self.stepper_dir = tk.StringVar(value="forward")
        self.stepper_speed = tk.IntVar(value=int(DEFAULT_SPEED))
        self.led_color = tk.StringVar(value="red")
        self.led_bright = tk.IntVar(value=int(DEFAULT_LED_BRIGHTNESS))
        
        self.widgets = {
            'root': self.root,
            'diameter_entry': self.diameter_entry,
            'servo_angle': self.servo_angle,
            'stepper_length_cm': self.stepper_length_cm,
            'stepper_dir': self.stepper_dir,
            'stepper_speed': self.stepper_speed,
            'led_color': self.led_color,
            'led_bright': self.led_bright,
            'update_position_label': self.update_position_label,
            'webcam': self.webcam,
            'global_delay': self
        }
        
        # Operation queue
        self.operation_queue = OperationQueue(self.logger, self.queue_list)
        
        # Device control
        self.device_control = DeviceControl(
            self.logger,
            self.base_url_var,
            self.widgets,
            self.position,
            self.servo_angle_var
        )
          # Angle calculator interface
        self.angle_calculator = AngleCalculatorInterface(self.logger)
    
    def initialize_calculator_display(self):
        """Initialize the calculator display with current values and load images"""
        if hasattr(self, 'event_handlers'):
            # Update command display with initial values
            self.event_handlers.update_command_display()
            # Load initial servo images
            self.event_handlers.load_servo_images()
    
    def update_position_label(self):
        """Update position and servo angle display"""
        self.position_label.config(text=f"{self.position.get():.2f}")
        self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.root.update_idletasks()
    
    def on_closing(self):
        """Handle window closing event"""
        try:
            self.webcam.cleanup()
        except:
            pass
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to start the application"""
    app = ControlApp()
    app.run()


if __name__ == "__main__":
    main()
