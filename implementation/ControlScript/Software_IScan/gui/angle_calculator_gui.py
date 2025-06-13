"""
Angle Calculator GUI Component
Contains the angle calculator interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class AngleCalculatorGUI:
    """GUI component for angle calculator with parameter controls and image display"""
    
    def __init__(self, parent, callbacks=None):
        """
        Initialize angle calculator GUI
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        
        self.frame = None
        self.content_frame = None
        self.params_frame = None
        self.image_frame = None
        
        # Parameter entry widgets
        self.calc_csv_name = None
        self.calc_target_x = None
        self.calc_target_y = None
        self.calc_scan_distance = None
        self.calc_measurements = None
        self.calc_servo_min = None
        self.calc_servo_max = None
        self.calc_servo_neutral = None
        
        # Command display
        self.current_command_label = None
        
        # Image display
        self.image_notebook = None
        self.tab1_frame = None
        self.tab2_frame = None
        self.servo_graph_img_label = None
        self.servo_cone_img_label = None
        self.servo_graph_img = None
        self.servo_cone_img = None
        
        # Default values
        self.defaults = {
            'csv_name': 'original_iscan',
            'target_x': '33',
            'target_y': '50',
            'scan_distance': '80',
            'measurements': '7',
            'servo_min': '0.0',
            'servo_max': '90.0',
            'servo_neutral': '45.0'
        }
    
    def create_frame(self):
        """Create the angle calculator frame with simplified layout"""
        self.frame = tk.LabelFrame(self.parent, text="Calculator_Angle_Maschine")
        self.frame.pack(fill="x", padx=10, pady=2)
        
        # Info label
        info_label = tk.Label(
            self.frame, 
            text="3D Scanner Winkelberechnung mit konfigurierbaren Parametern", 
            font=("Arial", 9), 
            fg="gray"
        )
        info_label.pack(anchor="w", padx=5, pady=(5, 0))
        
        return self.frame
    
    def create_calculator_commands_panel(self, parent, grid_mode=False):
        """
        Create the complete calculator commands panel with parameters and image display
        
        Args:
            parent: Parent widget
            grid_mode: Whether to use grid layout
        """
        calc_panel = tk.LabelFrame(parent, text="Calculator Commands", font=("Arial", 10, "bold"))
        if grid_mode:
            calc_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        else:
            calc_panel.pack(side=tk.RIGHT, fill="y", padx=(10, 0))
        
        # Content frame for parameters and image
        self.content_frame = tk.Frame(calc_panel)
        self.content_frame.pack(fill="both", expand=True)
        
        # Create parameter controls (left side)
        self.create_parameter_controls()
        
        # Create image display (right side)
        self.create_image_display()
        
        # Initialize command display
        self.update_command_display()
        
        return calc_panel
    
    def create_parameter_controls(self):
        """Create parameter input controls"""
        self.params_frame = tk.Frame(self.content_frame)
        self.params_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # CSV Name
        tk.Label(self.params_frame, text="CSV Name:", font=("Arial", 8)).grid(
            row=0, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_csv_name = tk.Entry(self.params_frame, width=18, font=("Arial", 8))
        self.calc_csv_name.insert(0, self.defaults['csv_name'])
        self.calc_csv_name.grid(row=0, column=1, padx=2, pady=1)
        self.calc_csv_name.bind('<KeyRelease>', self.update_command_display)
        self.calc_csv_name.bind('<FocusOut>', self.update_command_display)
        
        # Target X
        tk.Label(self.params_frame, text="Target X (cm):", font=("Arial", 8)).grid(
            row=1, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_target_x = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_target_x.insert(0, self.defaults['target_x'])
        self.calc_target_x.grid(row=1, column=1, sticky="w", padx=2, pady=1)
        self.calc_target_x.bind('<KeyRelease>', self.update_command_display)
        self.calc_target_x.bind('<FocusOut>', self.update_command_display)
        
        # Target Y
        tk.Label(self.params_frame, text="Target Y (cm):", font=("Arial", 8)).grid(
            row=2, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_target_y = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_target_y.insert(0, self.defaults['target_y'])
        self.calc_target_y.grid(row=2, column=1, sticky="w", padx=2, pady=1)
        self.calc_target_y.bind('<KeyRelease>', self.update_command_display)
        self.calc_target_y.bind('<FocusOut>', self.update_command_display)
        
        # Scan Distance
        tk.Label(self.params_frame, text="Scan Distance (cm):", font=("Arial", 8)).grid(
            row=3, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_scan_distance = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_scan_distance.insert(0, self.defaults['scan_distance'])
        self.calc_scan_distance.grid(row=3, column=1, sticky="w", padx=2, pady=1)
        self.calc_scan_distance.bind('<KeyRelease>', self.update_command_display)
        self.calc_scan_distance.bind('<FocusOut>', self.update_command_display)
        
        # Measurements
        tk.Label(self.params_frame, text="Measurements:", font=("Arial", 8)).grid(
            row=4, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_measurements = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_measurements.insert(0, self.defaults['measurements'])
        self.calc_measurements.grid(row=4, column=1, sticky="w", padx=2, pady=1)
        self.calc_measurements.bind('<KeyRelease>', self.update_command_display)
        self.calc_measurements.bind('<FocusOut>', self.update_command_display)
        
        # Create servo configuration section
        self.create_servo_configuration()
        
        # Create command buttons
        self.create_command_buttons()
        
        # Create command display
        self.create_command_display()
    
    def create_servo_configuration(self):
        """Create servo configuration controls"""
        # Servo Configuration Section Header
        servo_header = tk.Label(
            self.params_frame, 
            text="Servo Configuration:", 
            font=("Arial", 8, "bold"), 
            fg="darkblue"
        )
        servo_header.grid(row=5, column=0, columnspan=2, sticky="w", padx=2, pady=(8, 2))
        
        # Servo Min Angle
        tk.Label(self.params_frame, text="Servo Min Angle:", font=("Arial", 8)).grid(
            row=6, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_servo_min = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_servo_min.insert(0, self.defaults['servo_min'])
        self.calc_servo_min.grid(row=6, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_min.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_min.bind('<FocusOut>', self.update_command_display)
        
        # Servo Max Angle
        tk.Label(self.params_frame, text="Servo Max Angle:", font=("Arial", 8)).grid(
            row=7, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_servo_max = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_servo_max.insert(0, self.defaults['servo_max'])
        self.calc_servo_max.grid(row=7, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_max.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_max.bind('<FocusOut>', self.update_command_display)
        
        # Servo Neutral Angle
        tk.Label(self.params_frame, text="Servo Neutral Angle:", font=("Arial", 8)).grid(
            row=8, column=0, sticky="w", padx=2, pady=1
        )
        self.calc_servo_neutral = tk.Entry(self.params_frame, width=8, font=("Arial", 8))
        self.calc_servo_neutral.insert(0, self.defaults['servo_neutral'])
        self.calc_servo_neutral.grid(row=8, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_neutral.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_neutral.bind('<FocusOut>', self.update_command_display)
    
    def create_command_buttons(self):
        """Create command execution buttons"""
        # Separator
        separator = tk.Frame(self.params_frame, height=2, bg="gray")
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", pady=8)
        
        # Command Buttons
        commands_frame = tk.LabelFrame(self.params_frame, text="Execute Commands", font=("Arial", 8, "bold"))
        commands_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=2)
        
        visual_btn = tk.Button(
            commands_frame, 
            text="Visualisation Mode\n(--visualize)", 
            bg="#FFD700", 
            fg="black", 
            font=("Arial", 8, "bold"), 
            width=15, 
            height=2
        )
        visual_btn.pack(fill="x", padx=2, pady=2)
        
        silent_btn = tk.Button(
            commands_frame, 
            text="Silent Mode\n(--silent)", 
            bg="#98FB98", 
            fg="black", 
            font=("Arial", 8, "bold"), 
            width=15, 
            height=2
        )
        silent_btn.pack(fill="x", padx=2, pady=2)
        
        # Configure callbacks
        if 'execute_visualisation' in self.callbacks:
            visual_btn.config(command=self.callbacks['execute_visualisation'])
        if 'execute_silent' in self.callbacks:
            silent_btn.config(command=self.callbacks['execute_silent'])
    
    def create_command_display(self):
        """Create current command display"""
        current_cmd_frame = tk.LabelFrame(self.params_frame, text="Current Command", font=("Arial", 8, "bold"))
        current_cmd_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.current_command_label = tk.Label(
            current_cmd_frame, 
            text="python main.py --visualize --csv-name original_iscan --target-x 33 --target-y 50 --scan-distance 80 --measurements 7",
            wraplength=200, 
            justify="left", 
            font=("Arial", 7), 
            fg="blue"
        )
        self.current_command_label.pack(padx=2, pady=2)
    
    def create_image_display(self):
        """Create image display with tabs"""
        self.image_frame = tk.Frame(self.content_frame)
        self.image_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Tab notebook for image switching
        self.image_notebook = ttk.Notebook(self.image_frame)
        self.image_notebook.pack(fill="both", expand=True)
        
        # Tab 1: Servo Geometry Graph
        self.tab1_frame = tk.Frame(self.image_notebook)
        self.image_notebook.add(self.tab1_frame, text="Servo Graph")
        
        # Tab 2: Servo Cone Detail
        self.tab2_frame = tk.Frame(self.image_notebook)
        self.image_notebook.add(self.tab2_frame, text="Cone Detail")
        
        # Image labels for both tabs
        self.servo_graph_img_label = tk.Label(self.tab1_frame)
        self.servo_graph_img_label.pack(fill="both", expand=True)
        
        self.servo_cone_img_label = tk.Label(self.tab2_frame)
        self.servo_cone_img_label.pack(fill="both", expand=True)
        
        # Load images initially
        self.load_servo_images()
    
    def update_command_display(self, event=None):
        """Update the command display with current parameter values"""
        if not self.current_command_label:
            return
        
        try:
            csv_name = self.calc_csv_name.get() if self.calc_csv_name else self.defaults['csv_name']
            target_x = self.calc_target_x.get() if self.calc_target_x else self.defaults['target_x']
            target_y = self.calc_target_y.get() if self.calc_target_y else self.defaults['target_y']
            scan_distance = self.calc_scan_distance.get() if self.calc_scan_distance else self.defaults['scan_distance']
            measurements = self.calc_measurements.get() if self.calc_measurements else self.defaults['measurements']
            servo_min = self.calc_servo_min.get() if self.calc_servo_min else self.defaults['servo_min']
            servo_max = self.calc_servo_max.get() if self.calc_servo_max else self.defaults['servo_max']
            servo_neutral = self.calc_servo_neutral.get() if self.calc_servo_neutral else self.defaults['servo_neutral']
            
            command = (f"python main.py --visualize --csv-name {csv_name} "
                      f"--target-x {target_x} --target-y {target_y} --scan-distance {scan_distance} "
                      f"--measurements {measurements} --servo-min-angle {servo_min} "
                      f"--servo-max-angle {servo_max} --servo-neutral-angle {servo_neutral}")
            
            self.current_command_label.config(text=command)
        except Exception as e:
            self.current_command_label.config(text=f"Error updating command: {e}")
    
    def load_servo_images(self):
        """Load servo images with proper scaling"""
        try:
            # Define image paths
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            graph_path = os.path.join(script_dir, "Calculator_Angle_Maschine", "MathVisualisation", "output", "06_servo_geometry_graph_only.png")
            cone_path = os.path.join(script_dir, "Calculator_Angle_Maschine", "MathVisualisation", "output", "07_servo_cone_detail.png")
            
            # Load and scale images
            max_width, max_height = 400, 300
            
            # Load Servo Graph
            if os.path.exists(graph_path):
                img = Image.open(graph_path)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.servo_graph_img = ImageTk.PhotoImage(img)
                self.servo_graph_img_label.config(image=self.servo_graph_img, text="")
            else:
                self.servo_graph_img_label.config(image="", text=f"Servo Graph nicht gefunden:\n{graph_path}")
            
            # Load Cone Detail
            if os.path.exists(cone_path):
                img = Image.open(cone_path)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.servo_cone_img = ImageTk.PhotoImage(img)
                self.servo_cone_img_label.config(image=self.servo_cone_img, text="")
            else:
                self.servo_cone_img_label.config(image="", text=f"Cone Detail nicht gefunden:\n{cone_path}")
                
        except Exception as e:
            if hasattr(self, 'servo_graph_img_label'):
                self.servo_graph_img_label.config(image="", text=f"Fehler beim Laden des Servo Graphs: {e}")
            if hasattr(self, 'servo_cone_img_label'):
                self.servo_cone_img_label.config(image="", text=f"Fehler beim Laden des Cone Details: {e}")
    
    def get_parameters(self):
        """Get all parameter values"""
        return {
            'csv_name': self.calc_csv_name.get() if self.calc_csv_name else self.defaults['csv_name'],
            'target_x': self.calc_target_x.get() if self.calc_target_x else self.defaults['target_x'],
            'target_y': self.calc_target_y.get() if self.calc_target_y else self.defaults['target_y'],
            'scan_distance': self.calc_scan_distance.get() if self.calc_scan_distance else self.defaults['scan_distance'],
            'measurements': self.calc_measurements.get() if self.calc_measurements else self.defaults['measurements'],
            'servo_min': self.calc_servo_min.get() if self.calc_servo_min else self.defaults['servo_min'],
            'servo_max': self.calc_servo_max.get() if self.calc_servo_max else self.defaults['servo_max'],
            'servo_neutral': self.calc_servo_neutral.get() if self.calc_servo_neutral else self.defaults['servo_neutral']
        }
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'frame': self.frame,
            'content_frame': self.content_frame,
            'params_frame': self.params_frame,
            'image_frame': self.image_frame,
            'calc_csv_name': self.calc_csv_name,
            'calc_target_x': self.calc_target_x,
            'calc_target_y': self.calc_target_y,
            'calc_scan_distance': self.calc_scan_distance,
            'calc_measurements': self.calc_measurements,
            'calc_servo_min': self.calc_servo_min,
            'calc_servo_max': self.calc_servo_max,
            'calc_servo_neutral': self.calc_servo_neutral,
            'current_command_label': self.current_command_label,
            'image_notebook': self.image_notebook,
            'servo_graph_img_label': self.servo_graph_img_label,
            'servo_cone_img_label': self.servo_cone_img_label
        }
