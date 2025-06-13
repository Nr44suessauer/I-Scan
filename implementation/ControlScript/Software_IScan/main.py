"""
IScan-ControlScript - Main Program
A GUI application for controlling hardware via an API interface.
This application provides a user interface to interact with hardware components
such as servo motors, stepper motors, LED lights, and buttons via a REST API.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""
import os
import csv
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, Label, filedialog, messagebox, StringVar, DoubleVar, IntVar, BooleanVar
from PIL import Image, ImageTk
import subprocess

# Import eigener Module
from api_client import ApiClient
from logger import Logger
from device_control import DeviceControl
from operation_queue import OperationQueue
from webcam_helper import WebcamHelper
from angle_calculator_commands import AngleCalculatorInterface, show_angle_calculator_dialog

# Konstanten für Standardwerte und Berechnungen
PI = 3.141592653589793
DEFAULT_BASE_URL = "http://192.168.137.7"
DEFAULT_DIAMETER = "28"
DEFAULT_SPEED = "80"
DEFAULT_DISTANCE = "3.0"
DEFAULT_DIRECTION = "1"
DEFAULT_LED_COLOR = "#B00B69"
DEFAULT_LED_BRIGHTNESS = "69"


class ControlApp:
    """
    Main application class for the control application
    Manages the GUI, user interactions, and coordinates the
    various components of the application.
    """
    
    def __init__(self):
        """Initializes the control application and sets up the GUI"""
        self.root = tk.Tk()
        self.root.title("I-Scan Wizard")
        
        # Set the window icon
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "wizard_icon.png")
            
            if os.path.exists(icon_path):
                # Load and set the icon
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
                # Keep a reference to prevent garbage collection
                self.root.icon_image = icon
            else:
                print("Warning: Wizard icon not found at", icon_path)
        except Exception as e:
            print(f"Warning: Could not load wizard icon: {e}")
        
        # Statusvariablen
        self.position = tk.DoubleVar(value=0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.base_url_var = tk.StringVar(value=DEFAULT_BASE_URL)
        self.last_distance_value = tk.StringVar(value=DEFAULT_DISTANCE)
        self.repeat_queue = tk.BooleanVar(value=False)  # Wiederholungsflag
        self.global_delay = 0.5  # Globale Autofokus-Delay-Zeit
        
        # Webcam initialisieren
        self.webcam = WebcamHelper(device_index=0, frame_size=(320, 240))
        
        # GUI-Elemente erstellen
        self.create_widgets()
        
        # Logger initialisieren
        self.logger = Logger(
            self.output, 
            self.position, 
            self.servo_angle_var, 
            self.update_position_label
        )          # Widget-Wörterbuch für den Zugriff auf GUI-Elemente
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
        
        # Operationswarteschlange initialisieren
        self.operation_queue = OperationQueue(self.logger, self.queue_list)
        
        # Gerätesteuerung initialisieren
        self.device_control = DeviceControl(
            self.logger,
            self.base_url_var,
            self.widgets,
            self.position,
            self.servo_angle_var
        )
        
        # Angle Calculator Interface initialisieren
        self.angle_calculator = AngleCalculatorInterface(self.logger)
        
        # Callback-Funktionen zuweisen
        self.assign_callbacks()
        
        # Ereignishandler für das Schließen des Fensters
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente im Anwendungsfenster"""
        # URL-Eingabefeld
        self.create_url_frame()
        
        # Kamera-Einstellungen
        self.create_camera_settings_frame()  # Kamera-Einstellungen-Feld hinzufügen
        
        # Zahnraddurchmesser oben
        self.create_diameter_frame()
        
        # Positions- und Servo-Winkel-Anzeige oben rechts
        self.create_position_display()
        
        # Ausgabefenster
        self.create_output_display()
        
        # Webcam-Anzeige
        self.create_webcam_frame()
        
        # Servo-Steuerung
        self.create_servo_frame()
        
        # Schrittmotor-Steuerung
        self.create_stepper_frame()
        
        # LED-Farbe
        self.create_led_color_frame()
        
        # LED-Helligkeit
        self.create_led_brightness_frame()
        
        # Button-Status
        self.create_button_frame()
        
        # Home-Funktion
        self.create_home_frame()
        
        # Angle Calculator Commands
        self.create_angle_calculator_frame()
        
        # Operationswarteschlange
        self.create_queue_frame()
    
    def create_url_frame(self):
        """
        Erstellt den Rahmen für das URL-Eingabefeld
        Ermöglicht es dem Benutzer, die API-Basis-URL anzugeben
        """
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill="x", padx=10, pady=(10,2))
        tk.Label(url_frame, text="API-Adresse:").pack(side=tk.LEFT)
        base_url_entry = tk.Entry(url_frame, textvariable=self.base_url_var, width=30)
        base_url_entry.pack(side=tk.LEFT, padx=5)
    
    def create_camera_settings_frame(self):
        """
        Erstellt einen Rahmen für Kamera-Einstellungen (z.B. COM-Port/Device Index)
        """
        camera_settings_frame = tk.Frame(self.root)
        camera_settings_frame.pack(fill="x", padx=10, pady=(2,2))
        tk.Label(camera_settings_frame, text="Kamera Device Index (z.B. 0, 1, 2):").pack(side=tk.LEFT)
        self.camera_device_index_var = tk.StringVar(value="0")
        self.camera_device_entry = tk.Entry(camera_settings_frame, width=5, textvariable=self.camera_device_index_var)
        self.camera_device_entry.pack(side=tk.LEFT)
        self.set_camera_device_btn = tk.Button(camera_settings_frame, text="Setzen", command=self.set_camera_device_index)
        self.set_camera_device_btn.pack(side=tk.LEFT, padx=5)
        
        # Autofokus-Delay-Setting hinzufügen
        tk.Label(camera_settings_frame, text="  Autofokus-Delay (s):").pack(side=tk.LEFT, padx=(20,0))
        self.camera_delay_var = tk.StringVar(value="0.5")
        self.camera_delay_entry = tk.Entry(camera_settings_frame, width=5, textvariable=self.camera_delay_var)
        self.camera_delay_entry.pack(side=tk.LEFT)
        self.set_delay_btn = tk.Button(camera_settings_frame, text="set", command=self.set_global_delay)
        self.set_delay_btn.pack(side=tk.LEFT, padx=5)
    
    def create_diameter_frame(self):
        """
        Erstellt den Rahmen für das Durchmesser-Eingabefeld
        Ermöglicht es dem Benutzer, den Zahnraddurchmesser in mm anzugeben
        """
        diameter_frame = tk.Frame(self.root)
        diameter_frame.pack(fill="x", padx=10, pady=(2,2))
        tk.Label(diameter_frame, text="Zahnraddurchmesser (mm):").pack(side=tk.LEFT)
        self.diameter_entry = tk.Entry(diameter_frame, width=8)
        self.diameter_entry.insert(0, DEFAULT_DIAMETER)
        self.diameter_entry.pack(side=tk.LEFT)
    
    def create_position_display(self):
        """
        Erstellt die Positions- und Servo-Winkel-Anzeige
        Zeigt die aktuelle Position und den Servo-Winkel in der oberen rechten Ecke an
        """
        pos_frame = tk.Frame(self.root)
        pos_frame.place(relx=1.0, y=0, anchor='ne')
        tk.Label(pos_frame, text="Position:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.position_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                               fg="blue", width=6, anchor='e', text="0.00")
        self.position_label.pack(side=tk.LEFT)
        tk.Label(pos_frame, text="cm", font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT)
        tk.Label(pos_frame, text="   Servo-Winkel:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.servo_angle_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                                 fg="green", width=3, anchor='e', text="0")
        self.servo_angle_label.pack(side=tk.LEFT)
        tk.Label(pos_frame, text="°", font=("Arial", 12, "bold"), fg="green").pack(side=tk.LEFT)
    
    def create_output_display(self):
        """
        Erstellt die Anzeige für Text mit Bildlauf und das Calculator Command Panel
        Zeigt Protokollnachrichten und Operationsergebnisse an
        """
        # Hauptcontainer für Output und Calculator Commands
        output_container = tk.Frame(self.root)
        output_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Grid-Layout für gleichmäßige Aufteilung
        output_container.columnconfigure(0, weight=1, minsize=350)  # Log-Konsole schmaler
        output_container.columnconfigure(1, weight=1, minsize=350)  # Scan-Konfiguration + Bild
        output_container.rowconfigure(0, weight=1)

        # Log-Konsole (links)
        log_frame = tk.Frame(output_container)
        log_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(log_frame, text="Log-Konsole", font=("Arial", 10, "bold")).pack(anchor='w')
        self.output = scrolledtext.ScrolledText(log_frame, width=45, height=16, state='disabled')
        self.output.pack(fill="both", expand=True)

        # Calculator Commands Panel (rechts)
        self.create_calculator_commands_panel(output_container, grid_mode=True)
    
    def create_calculator_commands_panel(self, parent, grid_mode=False):
        """
        Erstellt das Calculator Commands Panel neben der Log-Konsole
        Zeigt rechts neben der Scan-Konfiguration das Bild 06_servo_geometry_graph_only.png an
        """
        calc_panel = tk.LabelFrame(parent, text="Calculator Commands", font=("Arial", 10, "bold"))
        if grid_mode:
            calc_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        else:
            calc_panel.pack(side=tk.RIGHT, fill="y", padx=(10, 0))

        # Frame für Parameter und Bild nebeneinander
        content_frame = tk.Frame(calc_panel)
        content_frame.pack(fill="both", expand=True)

        # Parameter für beide Modi (links)
        params_frame = tk.Frame(content_frame)
        params_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
          # CSV Name
        tk.Label(params_frame, text="CSV Name:", font=("Arial", 8)).grid(row=0, column=0, sticky="w", padx=2, pady=1)
        self.calc_csv_name = tk.Entry(params_frame, width=18, font=("Arial", 8))
        self.calc_csv_name.insert(0, "original_iscan")
        self.calc_csv_name.grid(row=0, column=1, padx=2, pady=1)
        self.calc_csv_name.bind('<KeyRelease>', self.update_command_display)
        self.calc_csv_name.bind('<FocusOut>', self.update_command_display)
        
        # Target X
        tk.Label(params_frame, text="Target X (cm):", font=("Arial", 8)).grid(row=1, column=0, sticky="w", padx=2, pady=1)
        self.calc_target_x = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_target_x.insert(0, "33")
        self.calc_target_x.grid(row=1, column=1, sticky="w", padx=2, pady=1)
        self.calc_target_x.bind('<KeyRelease>', self.update_command_display)
        self.calc_target_x.bind('<FocusOut>', self.update_command_display)
        
        # Target Y
        tk.Label(params_frame, text="Target Y (cm):", font=("Arial", 8)).grid(row=2, column=0, sticky="w", padx=2, pady=1)
        self.calc_target_y = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_target_y.insert(0, "50")
        self.calc_target_y.grid(row=2, column=1, sticky="w", padx=2, pady=1)
        self.calc_target_y.bind('<KeyRelease>', self.update_command_display)
        self.calc_target_y.bind('<FocusOut>', self.update_command_display)
        
        # Scan Distance
        tk.Label(params_frame, text="Scan Distance (cm):", font=("Arial", 8)).grid(row=3, column=0, sticky="w", padx=2, pady=1)
        self.calc_scan_distance = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_scan_distance.insert(0, "80")
        self.calc_scan_distance.grid(row=3, column=1, sticky="w", padx=2, pady=1)
        self.calc_scan_distance.bind('<KeyRelease>', self.update_command_display)
        self.calc_scan_distance.bind('<FocusOut>', self.update_command_display)
          # Measurements
        tk.Label(params_frame, text="Measurements:", font=("Arial", 8)).grid(row=4, column=0, sticky="w", padx=2, pady=1)
        self.calc_measurements = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_measurements.insert(0, "7")
        self.calc_measurements.grid(row=4, column=1, sticky="w", padx=2, pady=1)
        self.calc_measurements.bind('<KeyRelease>', self.update_command_display)
        self.calc_measurements.bind('<FocusOut>', self.update_command_display)
        
        # Servo Configuration Section Header
        servo_header = tk.Label(params_frame, text="Servo Configuration:", font=("Arial", 8, "bold"), fg="darkblue")
        servo_header.grid(row=5, column=0, columnspan=2, sticky="w", padx=2, pady=(8, 2))
        
        # Servo Min Angle
        tk.Label(params_frame, text="Servo Min Angle:", font=("Arial", 8)).grid(row=6, column=0, sticky="w", padx=2, pady=1)
        self.calc_servo_min = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_servo_min.insert(0, "0.0")
        self.calc_servo_min.grid(row=6, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_min.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_min.bind('<FocusOut>', self.update_command_display)
        
        # Servo Max Angle
        tk.Label(params_frame, text="Servo Max Angle:", font=("Arial", 8)).grid(row=7, column=0, sticky="w", padx=2, pady=1)
        self.calc_servo_max = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_servo_max.insert(0, "90.0")
        self.calc_servo_max.grid(row=7, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_max.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_max.bind('<FocusOut>', self.update_command_display)
          # Servo Neutral Angle
        tk.Label(params_frame, text="Servo Neutral Angle:", font=("Arial", 8)).grid(row=8, column=0, sticky="w", padx=2, pady=1)
        self.calc_servo_neutral = tk.Entry(params_frame, width=8, font=("Arial", 8))
        self.calc_servo_neutral.insert(0, "45.0")
        self.calc_servo_neutral.grid(row=8, column=1, sticky="w", padx=2, pady=1)
        self.calc_servo_neutral.bind('<KeyRelease>', self.update_command_display)
        self.calc_servo_neutral.bind('<FocusOut>', self.update_command_display)
        
        # Separator
        separator = tk.Frame(params_frame, height=2, bg="gray")
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", pady=8)

        # Command Buttons
        commands_frame = tk.LabelFrame(params_frame, text="Execute Commands", font=("Arial", 8, "bold"))
        commands_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=2)
        visual_btn = tk.Button(commands_frame, text="Visualisation Mode\n(--visualize)", 
                              command=self.execute_visualisation_mode,
                              bg="#FFD700", fg="black", font=("Arial", 8, "bold"), width=15, height=2)
        visual_btn.pack(fill="x", padx=2, pady=2)
        silent_btn = tk.Button(commands_frame, text="Silent Mode\n(--silent)", 
                              command=self.execute_silent_mode,
                              bg="#98FB98", fg="black", font=("Arial", 8, "bold"), width=15, height=2)
        silent_btn.pack(fill="x", padx=2, pady=2)

        # Current Command Display
        current_cmd_frame = tk.LabelFrame(params_frame, text="Current Command", font=("Arial", 8, "bold"))
        current_cmd_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=5)
        self.current_command_label = tk.Label(current_cmd_frame, 
                                             text="python main.py --visualize --csv-name original_iscan --target-x 33 --target-y 50 --scan-distance 80 --measurements 7",
                                             wraplength=200, justify="left", font=("Arial", 7), fg="blue")
        self.current_command_label.pack(padx=2, pady=2)        # Bildanzeige mit Tabs (rechts)
        image_frame = tk.Frame(content_frame)
        image_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Tab-Notebook für Bildwechsel
        self.image_notebook = ttk.Notebook(image_frame)
        self.image_notebook.pack(fill="both", expand=True)
        
        # Tab 1: Servo Geometry Graph
        self.tab1_frame = tk.Frame(self.image_notebook)
        self.image_notebook.add(self.tab1_frame, text="Servo Graph")
        
        # Tab 2: Servo Cone Detail
        self.tab2_frame = tk.Frame(self.image_notebook)
        self.image_notebook.add(self.tab2_frame, text="Cone Detail")
          # Image Labels für beide Tabs
        self.servo_graph_img_label = tk.Label(self.tab1_frame)
        self.servo_graph_img_label.pack(fill="both", expand=True)
        
        self.servo_cone_img_label = tk.Label(self.tab2_frame)
        self.servo_cone_img_label.pack(fill="both", expand=True)
        
        # Lade Bilder initial (ohne permanente Größenanpassung)
        self.load_servo_images()
        
        # Initialize the command display with current values
        self.update_command_display()

    def create_webcam_frame(self):
        """
        Creates the frame for the webcam display and the control elements
        """
        webcam_frame = tk.LabelFrame(self.root, text="Camera")
        webcam_frame.pack(fill="both", expand=True, padx=10, pady=5, side=tk.LEFT)
        
        # Rahmen für die Kameraanzeige
        camera_view_frame = tk.Frame(webcam_frame)
        camera_view_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Label für Kameraanzeige
        self.cam_label = tk.Label(camera_view_frame, text="No camera image", 
                          bg="black", fg="white", width=40, height=15)
        self.cam_label.pack(fill="both", expand=True)
        
        # Rahmen für die Kamera-Schaltflächen
        camera_control_frame = tk.Frame(webcam_frame)
        camera_control_frame.pack(fill="x", padx=5, pady=5)
        # Camera control buttons
        self.btn_start_camera = tk.Button(camera_control_frame, text="Start Camera", 
                                bg="#4CAF50", fg="white", width=15)
        self.btn_start_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_stop_camera = tk.Button(camera_control_frame, text="Stop Camera", 
                               bg="#F44336", fg="white", width=15)
        self.btn_stop_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_take_photo = tk.Button(camera_control_frame, text="Take Photo", 
                              bg="#2196F3", fg="white", width=15)
        self.btn_take_photo.pack(side=tk.LEFT, padx=2)
        
        self.btn_add_photo_to_queue = tk.Button(camera_control_frame, text="+", 
                                     bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.btn_add_photo_to_queue.pack(side=tk.LEFT, padx=2)
    
    def create_servo_frame(self):
        """
        Creates the frame for servo control
        Allows the user to set the servo angle
        """
        servo_frame = tk.LabelFrame(self.root, text="Servo Control")
        servo_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(servo_frame, text="Angle (0-90):").pack(side=tk.LEFT)
        self.servo_angle = tk.Entry(servo_frame, width=5)
        self.servo_angle.pack(side=tk.LEFT)
        
        # Buttons are configured in assign_callbacks
        self.servo_exec_btn = tk.Button(servo_frame, text="Execute Servo")
        self.servo_exec_btn.pack(side=tk.LEFT, padx=5)
        self.servo_add_btn = tk.Button(servo_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.servo_add_btn.pack(side=tk.LEFT)
    
    def create_stepper_frame(self):
        """
        Erstellt den Rahmen für die Schrittmotor-Steuerung
        Ermöglicht es dem Benutzer, den Schrittmotor mit Distanz-,
        Richtungs- und Geschwindigkeitsparametern zu steuern
        """
        stepper_frame = tk.LabelFrame(self.root, text="Schrittmotor-Steuerung")
        stepper_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(stepper_frame, text="Distanz (cm):").pack(side=tk.LEFT)
        
        self.stepper_length_cm = tk.Entry(stepper_frame, width=8, textvariable=self.last_distance_value)
        self.stepper_length_cm.pack(side=tk.LEFT)
        
        tk.Label(stepper_frame, text="Richtung (1/-1):").pack(side=tk.LEFT)
        self.stepper_dir = tk.Entry(stepper_frame, width=4)
        self.stepper_dir.insert(0, DEFAULT_DIRECTION)
        self.stepper_dir.pack(side=tk.LEFT)
        tk.Label(stepper_frame, text="Geschwindigkeit (opt.):").pack(side=tk.LEFT)
        self.stepper_speed = tk.Entry(stepper_frame, width=6)
        self.stepper_speed.insert(0, DEFAULT_SPEED)
        self.stepper_speed.pack(side=tk.LEFT)
        
        self.stepper_exec_btn = tk.Button(stepper_frame, text="Stepper ausführen")
        self.stepper_exec_btn.pack(side=tk.LEFT, padx=5)
        self.stepper_add_btn = tk.Button(stepper_frame, text="+", 
                               bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.stepper_add_btn.pack(side=tk.LEFT)
    
    def create_led_color_frame(self):
        """
        Erstellt den Rahmen für die LED-Farb-Steuerung
        Ermöglicht es dem Benutzer, die LED-Farbe mit einem Hex-Code einzustellen
        """
        led_frame = tk.LabelFrame(self.root, text="LED-Farbe setzen")
        led_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(led_frame, text="Farbe (z.B. #FF0000):").pack(side=tk.LEFT)
        self.led_color = tk.Entry(led_frame, width=10)
        self.led_color.insert(0, DEFAULT_LED_COLOR)
        self.led_color.pack(side=tk.LEFT)
        
        self.led_exec_btn = tk.Button(led_frame, text="LED ausführen")
        self.led_exec_btn.pack(side=tk.LEFT, padx=5)
        self.led_add_btn = tk.Button(led_frame, text="+", 
                            bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.led_add_btn.pack(side=tk.LEFT)
    
    def create_led_brightness_frame(self):
        """
        Erstellt den Rahmen für die LED-Helligkeitssteuerung
        Ermöglicht es dem Benutzer, die LED-Helligkeit (0-100%) einzustellen
        """
        bright_frame = tk.LabelFrame(self.root, text="LED-Helligkeit setzen")
        bright_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(bright_frame, text="Helligkeit (0-100):").pack(side=tk.LEFT)
        self.led_bright = tk.Entry(bright_frame, width=5)
        self.led_bright.insert(0, DEFAULT_LED_BRIGHTNESS)
        self.led_bright.pack(side=tk.LEFT)
        
        self.bright_exec_btn = tk.Button(bright_frame, text="Helligkeit ausführen")
        self.bright_exec_btn.pack(side=tk.LEFT, padx=5)
        self.bright_add_btn = tk.Button(bright_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.bright_add_btn.pack(side=tk.LEFT)
    
    def create_button_frame(self):
        """
        Erstellt den Rahmen für die Button-Status-Abfrage
        Ermöglicht es dem Benutzer, den aktuellen Button-Status abzufragen
        """
        btn_frame = tk.LabelFrame(self.root, text="Button-Status abfragen")
        btn_frame.pack(fill="x", padx=10, pady=2)
        
        self.button_exec_btn = tk.Button(btn_frame, text="Button abfragen")
        self.button_exec_btn.pack(side=tk.LEFT, padx=5)
        self.button_add_btn = tk.Button(btn_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.button_add_btn.pack(side=tk.LEFT)
    
    def create_home_frame(self):
        """
        Erstellt den Rahmen für die Home-Funktion
        Ermöglicht es dem Benutzer, die Home-Funktion auszuführen,
        die die Ausgangsposition der Hardware findet
        """
        home_frame = tk.LabelFrame(self.root, text="Home-Funktion")
        home_frame.pack(fill="x", padx=10, pady=2)
        
        self.home_exec_btn = tk.Button(home_frame, text="Home ausführen")
        self.home_exec_btn.pack(side=tk.LEFT, padx=5)
        self.home_add_btn = tk.Button(home_frame, text="+", 
                             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.home_add_btn.pack(side=tk.LEFT)
    
    def create_angle_calculator_frame(self):
        """
        Erstellt den Rahmen für Calculator_Angle_Maschine Befehle
        Ermöglicht CSV-Export und Visualisierungsgenerierung mit konfigurierbaren Parametern
        """
        calc_frame = tk.LabelFrame(self.root, text="Calculator_Angle_Maschine")
        calc_frame.pack(fill="x", padx=10, pady=2)
        
        # Info label
        info_label = tk.Label(calc_frame, text="3D Scanner Winkelberechnung mit konfigurierbaren Parametern", 
                             font=("Arial", 9), fg="gray")
        info_label.pack(anchor="w", padx=5, pady=(5, 0))
    
    def create_queue_frame(self):
        """
        Erstellt den Rahmen für die Operationswarteschlange
        Zeigt die in der Warteschlange stehenden Operationen an und bietet Steuerelemente
        zur Verwaltung und Ausführung der Warteschlange
        """
        queue_frame = tk.LabelFrame(self.root, text="Operationswarteschlange")
        queue_frame.pack(fill="both", expand=True, padx=10, pady=2)
        
        self.queue_list = tk.Listbox(queue_frame, width=70, height=8)
        self.queue_list.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        queue_scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=self.queue_list.yview)
        queue_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.queue_list.config(yscrollcommand=queue_scrollbar.set)
        
        queue_buttons_frame = tk.Frame(queue_frame)
        queue_buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)

        # Buttons in mehreren kompakten Reihen anordnen (je 2 pro Reihe)
        row1 = tk.Frame(queue_buttons_frame)
        row1.pack(fill="x")
        self.queue_exec_btn = tk.Button(row1, text="Warteschlange ausführen", 
                               bg="#77dd77", fg="black", font=("Arial", 10, "bold"))
        self.queue_exec_btn.pack(side=tk.LEFT, padx=5, pady=2)
        self.queue_clear_btn = tk.Button(row1, text="Warteschlange löschen",
                                bg="#ff6961", fg="black")
        self.queue_clear_btn.pack(side=tk.LEFT, padx=5, pady=2)

        row2 = tk.Frame(queue_buttons_frame)
        row2.pack(fill="x")
        self.queue_remove_btn = tk.Button(row2, text="Ausgewählte entfernen")
        self.queue_remove_btn.pack(side=tk.LEFT, padx=5, pady=2)
        self.repeat_check = tk.Checkbutton(row2, text="Warteschlange wiederholen", variable=self.repeat_queue)
        self.repeat_check.pack(side=tk.LEFT, padx=5, pady=2)

        row3 = tk.Frame(queue_buttons_frame)
        row3.pack(fill="x")
        self.queue_export_btn = tk.Button(row3, text="Warteschlange exportieren (CSV)", bg="#b0c4de", fg="black")
        self.queue_export_btn.pack(side=tk.LEFT, padx=5, pady=2)
        self.queue_import_btn = tk.Button(row3, text="Warteschlange importieren (CSV)", bg="#b0c4de", fg="black")
        self.queue_import_btn.pack(side=tk.LEFT, padx=5, pady=2)
    
    def assign_callbacks(self):
        """
        Weist allen Schaltflächen in der Benutzeroberfläche Callback-Funktionen zu
        Verknüpft UI-Ereignisse mit ihren entsprechenden Aktionen
        """        # Kamera-Callbacks
        self.btn_start_camera.config(command=self.start_camera)
        self.btn_stop_camera.config(command=self.stop_camera)
        self.btn_take_photo.config(command=self.take_photo)
        self.btn_add_photo_to_queue.config(command=self.add_photo_to_queue)
        
        # Servo-Callbacks
        self.servo_exec_btn.config(command=self.device_control.servo_cmd)
        self.servo_add_btn.config(command=self.add_servo_to_queue)
        
        # Stepper-Callbacks
        self.stepper_exec_btn.config(command=self.device_control.stepper_cmd)
        self.stepper_add_btn.config(command=self.add_stepper_to_queue)
        
        # LED-Callbacks
        self.led_exec_btn.config(command=self.device_control.led_cmd)
        self.led_add_btn.config(command=self.add_led_color_to_queue)
        
        # Helligkeits-Callbacks
        self.bright_exec_btn.config(command=self.device_control.bright_cmd)
        self.bright_add_btn.config(command=self.add_brightness_to_queue)
        
        # Button-Callbacks
        self.button_exec_btn.config(command=self.device_control.button_cmd)
        self.button_add_btn.config(command=self.add_button_to_queue)
        
        # Home-Callbacks - in einem separaten Thread ausführen, um die Benutzeroberfläche reaktionsfähig zu halten
        self.home_exec_btn.config(command=lambda: threading.Thread(target=self.device_control.home_func).start())
        self.home_add_btn.config(command=self.add_home_to_queue)
          # Warteschlangen-Callbacks
        self.queue_exec_btn.config(command=self.execute_queue)
        self.queue_clear_btn.config(command=self.operation_queue.clear)
        self.queue_remove_btn.config(command=lambda: self.remove_selected_operation(self.queue_list.curselection()))
        self.queue_export_btn.config(command=self.export_queue_to_csv)
        self.queue_import_btn.config(command=self.import_queue_from_csv)
    
    def update_position_label(self):
        """
        Aktualisiert das Positions-Anzeigelabel
        Aktualisiert die Positions- und Servo-Winkel-Labels mit aktuellen Werten
        """
        self.position_label.config(text=f"{self.position.get():.2f}")
        self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.root.update_idletasks()
    
    def add_servo_to_queue(self):
        """
        Fügt eine Servo-Operation zur Warteschlange hinzu
        Liest den Servo-Winkel aus dem Eingabefeld und fügt die Operation hinzu
        """
        try:
            angle = int(self.servo_angle.get())
            description = f"Servo: Winkel auf {angle}° setzen"
            self.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_stepper_to_queue(self):
        """
        Fügt eine Schrittmotor-Operation zur Warteschlange hinzu
        Berechnet Schritte aus der Distanz und fügt die Operation zur Warteschlange hinzu
        """
        try:            
            d = float(self.diameter_entry.get())
            circumference = PI * d  # mm
            length_cm = float(self.stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.stepper_dir.get()) if self.stepper_dir.get() else 1
            speed = int(self.stepper_speed.get()) if self.stepper_speed.get() else int(DEFAULT_SPEED)
            
            dir_text = "aufwärts" if direction == 1 else "abwärts"
            
            # Immer die Geschwindigkeit zum Parameter-Dictionary hinzufügen
            params = {"steps": steps, "direction": direction, "speed": speed}
                
            description = f"Stepper: {steps} Schritte, {length_cm} cm, Richtung {dir_text}" + (f", Geschwindigkeit: {speed}" if speed else "")
            self.operation_queue.add('stepper', params, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_led_color_to_queue(self):
        """
        Fügt eine LED-Farb-Operation zur Warteschlange hinzu
        Liest die Farbe aus dem Eingabefeld und fügt die Operation hinzu
        """
        try:
            color_hex = self.led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
                
            description = f"LED: Farbe auf {color_hex} setzen"
            self.operation_queue.add('led_color', {'color': color_hex}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_brightness_to_queue(self):
        """
        Fügt eine LED-Helligkeits-Operation zur Warteschlange hinzu
        Liest die Helligkeit aus dem Eingabefeld und fügt die Operation hinzu
        """
        try:
            val = int(self.led_bright.get())
            description = f"LED: Helligkeit auf {val}% setzen"
            self.operation_queue.add('led_brightness', {'brightness': val}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_button_to_queue(self):
        """
        Fügt eine Button-Status-Abfrage zur Warteschlange hinzu        Fügt eine Operation zum Abfragen des Button-Status hinzu
        """
        description = "Button: Button-Status abfragen"
        self.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """
        Fügt eine Home-Funktion zur Warteschlange hinzu
        Fügt eine Operation zum Ausführen der Home-Funktion hinzu
        """
        description = "Home: Home-Funktion ausführen"
        self.operation_queue.add('home', {}, description)
    
    def add_photo_to_queue(self):
        """
        Fügt eine Foto-Aufnahme-Operation zur Warteschlange hinzu
        Fügt eine Operation zum Aufnehmen und Speichern eines Fotos hinzu
        Verwendet die global gesetzte Delay-Zeit
        """
        # Globale Delay verwenden
        delay = self.global_delay
        
        description = f"Kamera: Foto aufnehmen (Global Delay: {delay}s)"
        self.operation_queue.add('photo', {'delay': delay}, description)
    
    def execute_queue(self):
        """
        Führt alle Operationen in der Warteschlange aus
        Startet den Warteschlangenausführungsprozess mit der konfigurierten Basis-URL
        """
        def run_queue_with_repeat():
            while True:
                base_url = self.base_url_var.get()
                if not base_url:
                    self.logger.log("Keine URL konfiguriert!")
                    break
                
                self.logger.log(f"Führe Warteschlange für {base_url} aus...")
                self.operation_queue.execute_all(
                    base_url,
                    self.widgets,
                    self.position,
                    self.servo_angle_var,
                    self.last_distance_value,
                    run_in_thread=False
                )
                
                if not self.repeat_queue.get():
                    break
                    
        threading.Thread(target=run_queue_with_repeat).start()
    
    def remove_selected_operation(self, selection):
        """
        Entfernt die ausgewählte Operation aus der Warteschlange
        
        Args:
            selection: Die ausgewählten Elementindizes aus der Listbox
        """
        if not selection:
            self.logger.log("Keine Operation zum Entfernen ausgewählt")
            return
        
        idx = selection[0]
        self.operation_queue.remove(idx)
    
    def export_queue_to_csv(self):
        """
        Exportiert die aktuelle Warteschlange als CSV-Datei
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV-Dateien", "*.csv")])
        if not file_path:
            return
        
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "params", "description"])
                
                for op in self.operation_queue.operations:
                    writer.writerow([
                        op['type'],
                        json.dumps(op['params']),
                        op['description']
                    ])
                    
            messagebox.showinfo("Export erfolgreich", f"Warteschlange wurde als CSV gespeichert: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def import_queue_from_csv(self):
        """
        Importiert eine Warteschlange aus einer CSV-Datei
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")])
        if not file_path:
            return
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.operation_queue.clear()
                
                for row in reader:
                    op_type = row['type']
                    params = json.loads(row['params'])
                    description = row['description']
                    self.operation_queue.add(op_type, params, description)
                    
            messagebox.showinfo("Import erfolgreich", f"Warteschlange wurde aus CSV geladen: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))
    
    def start_camera(self):
        """Startet die Kameraansicht"""
        success = self.webcam.stream_starten(self.cam_label)
        if success:
            self.logger.log("Kamera gestartet")
        else:
            self.logger.log("Fehler: Kamera konnte nicht gestartet werden")
            messagebox.showerror("Kamera-Fehler", 
                      "Die Kamera konnte nicht gestartet werden. Bitte Verbindung prüfen.")
    
    def stop_camera(self):
        """Stoppt die Kameraansicht und gibt die Ressourcen frei"""
        self.webcam.stoppen()
        self.cam_label.config(text="Kamera gestoppt", image="")
        self.logger.log("Kamera gestoppt")
    
    def take_photo(self):
        """Nimmt ein Foto auf und speichert es im Projektordner"""
        if not self.webcam.running or self.webcam.current_frame is None:
            self.logger.log("Fehler: Kamera nicht aktiv oder kein Bild verfügbar")
            return
        
        # Delay aus dem Eingabefeld lesen
        try:
            delay = float(self.camera_delay_var.get())
        except ValueError:
            delay = 0.5  # Fallback-Wert
            self.logger.log("Ungültiger Delay-Wert, verwende Standard-Delay von 0.5s")
            
        self.logger.log(f"Foto wird aufgenommen mit {delay}s Autofokus-Delay...")
        foto_path = self.webcam.foto_aufnehmen(delay=delay)
        if foto_path:
            self.logger.log(f"Foto aufgenommen und gespeichert als: {foto_path}")
            messagebox.showinfo("Foto aufgenommen", f"Das Foto wurde gespeichert als:\n{foto_path}")
        else:
            self.logger.log("Fehler: Foto konnte nicht gespeichert werden")
            
    def set_camera_device_index(self):
        """
        Setzt den Kamera-Device-Index neu und initialisiert die Webcam neu
        """
        try:
            idx = int(self.camera_device_index_var.get())
            self.webcam.stoppen()
            self.webcam = WebcamHelper(device_index=idx, frame_size=(320, 240))
            self.widgets['webcam'] = self.webcam
            self.logger.log(f"Kamera Device Index auf {idx} gesetzt. Kamera neu initialisiert.")
        except Exception as e:
            self.logger.log(f"Fehler beim Setzen des Kamera Device Index: {e}")
    
    def set_global_delay(self):
        """
        Setzt die globale Autofokus-Delay-Zeit aus dem Eingabefeld
        """
        try:
            delay = float(self.camera_delay_var.get())
            if delay < 0:
                raise ValueError("Delay kann nicht negativ sein")
            self.global_delay = delay
            self.logger.log(f"Globale Autofokus-Delay-Zeit auf {delay}s gesetzt")
            messagebox.showinfo("Delay gesetzt", f"Globale Autofokus-Delay-Zeit wurde auf {delay}s gesetzt")
        except ValueError as e:
            self.logger.log(f"Ungültiger Delay-Wert: {e}")
            messagebox.showerror("Ungültiger Wert", f"Bitte geben Sie einen gültigen Delay-Wert ein.\nFehler: {e}")
    
    def csv_silent_mode(self):
        """
        CSV Silent Mode - Generiert nur CSV mit konfigurierbaren Parametern
        """
        config = show_angle_calculator_dialog(self.root, "CSV Silent Mode Konfiguration")
        if config is None:
            return
        
        self.logger.log("🔇 Starte CSV Silent Mode...")
        
        def on_completion(csv_path):
            if csv_path:
                self.logger.log(f"✅ CSV erfolgreich generiert: {csv_path}")
                # Ask if user wants to import immediately
                if messagebox.askyesno("CSV Import", "CSV wurde erfolgreich generiert. Soll die CSV-Datei sofort in die Warteschlange importiert werden?"):
                    self.import_specific_csv(csv_path)
            else:
                self.logger.log("❌ CSV-Generierung fehlgeschlagen")
        
        # Run asynchronously to keep GUI responsive
        self.angle_calculator.generate_csv_silent_async(callback=on_completion, **config)
    
    def full_analysis_mode(self):
        """
        Vollanalyse Mode - Generiert Visualisierungen UND CSV
        """
        config = show_angle_calculator_dialog(self.root, "Vollanalyse Konfiguration")
        if config is None:
            return
        
        self.logger.log("🎨 Starte Vollanalyse Mode...")
        self.logger.log("⏳ Bitte warten - Visualisierungen werden erstellt...")
        
        def on_completion(csv_path):
            if csv_path:
                self.logger.log(f"✅ Vollanalyse erfolgreich abgeschlossen: {csv_path}")
                self.logger.log("📊 Visualisierungen wurden im Calculator_Angle_Maschine/MathVisualisation/output/ Ordner gespeichert")
                # Ask if user wants to import immediately
                if messagebox.askyesno("CSV Import", "Vollanalyse wurde erfolgreich abgeschlossen. Soll die CSV-Datei sofort in die Warteschlange importiert werden?"):
                    self.import_specific_csv(csv_path)
            else:
                self.logger.log("❌ Vollanalyse fehlgeschlagen")
        
        # Run asynchronously to keep GUI responsive
        self.angle_calculator.generate_full_analysis_async(callback=on_completion, **config)
    
    def import_calculator_csv(self):
        """
        Importiert CSV-Datei vom Calculator_Angle_Maschine
        """
        # Default to the Calculator_Angle_Maschine output directory
        initial_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "Calculator_Angle_Maschine", 
            "MathVisualisation", 
            "output"
        )
        
        file_path = filedialog.askopenfilename(
            title="Calculator_Angle_Maschine CSV importieren",
            initialdir=initial_dir if os.path.exists(initial_dir) else None,
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        
        if file_path:
            self.import_specific_csv(file_path)

    def import_specific_csv(self, file_path):
        """
        Importiert eine spezifische CSV-Datei in die Warteschlange
          Args:
            file_path (str): Pfad zur CSV-Datei
        """
        try:
            import csv
            import json
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.operation_queue.clear()
                imported_count = 0
                for row in reader:
                    op_type = row['type']
                    params = json.loads(row['params'])
                    description = row['description']
                    self.operation_queue.add(op_type, params, description)
                    imported_count += 1
            self.logger.log(f"✅ CSV erfolgreich importiert: {os.path.basename(file_path)}")
            self.logger.log(f"📋 {imported_count} Operationen zur Warteschlange hinzugefügt")
            messagebox.showinfo("Import erfolgreich", f"CSV wurde erfolgreich importiert!\n{imported_count} Operationen hinzugefügt.")
        except Exception as e:
            self.logger.log(f"❌ Fehler beim CSV-Import: {str(e)}")
            messagebox.showerror("Import Fehler", f"Fehler beim Importieren der CSV-Datei:\n{str(e)}")

    def update_command_display(self, event=None):
        """
        Aktualisiert die Anzeige des aktuellen Befehls
        """
        try:
            csv_name = self.calc_csv_name.get()
            target_x = self.calc_target_x.get()
            target_y = self.calc_target_y.get()
            scan_distance = self.calc_scan_distance.get()
            measurements = self.calc_measurements.get()
            servo_min = self.calc_servo_min.get()
            servo_max = self.calc_servo_max.get()
            servo_neutral = self.calc_servo_neutral.get()
            
            command = f"python main.py --visualize --csv-name {csv_name} --target-x {target_x} --target-y {target_y} --scan-distance {scan_distance} --measurements {measurements} --servo-min {servo_min} --servo-max {servo_max} --servo-neutral {servo_neutral}"
            self.current_command_label.config(text=command)
        except Exception:            pass
    
    def execute_visualisation_mode(self):
        """
        Führt den Visualisation Mode mit den aktuellen Parametern aus
        """
        try:
            csv_name = self.calc_csv_name.get()
            target_x = float(self.calc_target_x.get())
            target_y = float(self.calc_target_y.get())
            scan_distance = float(self.calc_scan_distance.get())
            measurements = int(self.calc_measurements.get())
            servo_min = float(self.calc_servo_min.get())
            servo_max = float(self.calc_servo_max.get())
            servo_neutral = float(self.calc_servo_neutral.get())
            
            self.logger.log(f"🖼️ Starte Visualisation Mode: {csv_name}")
            self.logger.log(f"📍 Target: ({target_x}, {target_y}), Distance: {scan_distance}, Measurements: {measurements}")
            self.logger.log(f"🔧 Servo: Min={servo_min}°, Max={servo_max}°, Neutral={servo_neutral}°")

            calc_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Calculator_Angle_Maschine", "MathVisualisation")
            command = [
                "python", "main.py", "--visualize",
                "--csv-name", csv_name,
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ]

            def run_command():
                try:
                    result = subprocess.run(command, cwd=calc_dir, capture_output=True, text=True, encoding="utf-8")
                    if result.returncode == 0:
                        self.logger.log(f"✅ Visualisation Mode erfolgreich abgeschlossen")
                        self.logger.log("📊 Visualisierungen wurden im Calculator_Angle_Maschine/MathVisualisation/output/ Ordner gespeichert")
                        self.update_servo_graph_image()
                    else:
                        self.logger.log(f"❌ Visualisation Mode fehlgeschlagen: {result.stderr}")
                except Exception as e:
                    self.logger.log(f"❌ Fehler bei Visualisation Mode: {e}")

            threading.Thread(target=run_command).start()

        except Exception as e:
            self.logger.log(f"❌ Fehler bei Visualisation Mode: {e}")
            messagebox.showerror("Fehler", f"Fehler bei der Visualisation Mode Ausführung:\n{e}")
    
    def execute_silent_mode(self):
        """
        Führt den Silent Mode mit den aktuellen Parametern aus
        """
        try:
            csv_name = self.calc_csv_name.get()
            target_x = float(self.calc_target_x.get())
            target_y = float(self.calc_target_y.get())
            scan_distance = float(self.calc_scan_distance.get())
            measurements = int(self.calc_measurements.get())
            servo_min = float(self.calc_servo_min.get())
            servo_max = float(self.calc_servo_max.get())
            servo_neutral = float(self.calc_servo_neutral.get())
            
            self.logger.log(f"🔇 Starte Silent Mode: {csv_name}")
            self.logger.log(f"📍 Target: ({target_x}, {target_y}), Distance: {scan_distance}, Measurements: {measurements}")
            self.logger.log(f"🔧 Servo: Min={servo_min}°, Max={servo_max}°, Neutral={servo_neutral}°")
            
            calc_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Calculator_Angle_Maschine", "MathVisualisation")
            command = [
                "python", "main.py", "--silent",
                "--csv-name", csv_name,
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ]
            def run_command():
                try:
                    result = subprocess.run(command, cwd=calc_dir, capture_output=True, text=True, encoding="utf-8")
                    if result.returncode == 0:
                        self.logger.log(f"✅ Silent Mode erfolgreich abgeschlossen")
                        # Suche nach der generierten CSV-Datei
                        output_dir = os.path.join(calc_dir, "output")
                        csv_file = os.path.join(output_dir, f"{csv_name}.csv")
                        if os.path.exists(csv_file):
                            if messagebox.askyesno("CSV Import", "CSV wurde erfolgreich generiert. Soll die CSV-Datei sofort in die Warteschlange importiert werden?"):
                                self.import_specific_csv(csv_file)
                    else:
                        self.logger.log(f"❌ Silent Mode fehlgeschlagen: {result.stderr}")
                except Exception as e:
                    self.logger.log(f"❌ Fehler bei Silent Mode: {e}")
            
            threading.Thread(target=run_command).start()
            
        except Exception as e:
            self.logger.log(f"❌ Fehler bei Silent Mode: {e}")
            messagebox.showerror("Fehler", f"Fehler bei der Silent Mode Ausführung:\n{e}")

    def on_closing(self):
        """Methode zum sauberen Schließen des Programms"""
        if hasattr(self, 'webcam'):
            self.webcam.stoppen()
        self.root.destroy()

    def update_servo_graph_image(self):
        """
        Aktualisiert das Servo-Graph-Bild im Calculator Commands Panel
        """
        self.load_servo_images()

    def load_servo_images(self):
        """
        Lädt beide Servo-Bilder (Graph und Cone Detail) mit fester Größe
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Pfad zum Servo Graph
            graph_path = os.path.join(script_dir, "..", "Calculator_Angle_Maschine", "MathVisualisation", "output", "06_servo_geometry_graph_only.png")
            graph_path = os.path.normpath(graph_path)
            
            # Pfad zum Cone Detail
            cone_path = os.path.join(script_dir, "..", "Calculator_Angle_Maschine", "MathVisualisation", "output", "07_servo_cone_detail.png")
            cone_path = os.path.normpath(cone_path)
            
            # Feste Bildgröße verwenden (keine permanente Anpassung)
            max_width, max_height = 500, 400
            
            # Lade Servo Graph mit gleichmäßiger Skalierung
            if os.path.exists(graph_path):
                img = Image.open(graph_path)
                # Berechne gleichmäßige Skalierung (Aspect Ratio beibehalten)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.servo_graph_img = ImageTk.PhotoImage(img)
                self.servo_graph_img_label.config(image=self.servo_graph_img, text="")
            else:
                self.servo_graph_img_label.config(image="", text=f"Servo Graph nicht gefunden:\n{graph_path}")
            
            # Lade Cone Detail mit gleichmäßiger Skalierung
            if os.path.exists(cone_path):
                img = Image.open(cone_path)
                # Berechne gleichmäßige Skalierung (Aspect Ratio beibehalten)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
              # Lade Servo Graph mit gleichmäßiger Skalierung
            if os.path.exists(graph_path):
                img = Image.open(graph_path)
                # Berechne gleichmäßige Skalierung (Aspect Ratio beibehalten)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.servo_graph_img = ImageTk.PhotoImage(img)
                self.servo_graph_img_label.config(image=self.servo_graph_img, text="")
            else:
                self.servo_graph_img_label.config(image="", text=f"Servo Graph nicht gefunden:\n{graph_path}")
            
            # Lade Cone Detail mit gleichmäßiger Skalierung
            if os.path.exists(cone_path):
                img = Image.open(cone_path)
                # Berechne gleichmäßige Skalierung (Aspect Ratio beibehalten)
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
            else:
                self.servo_cone_img_label.config(image="", text=f"Cone Detail nicht gefunden:\n{cone_path}")
                
        except Exception as e:
            if hasattr(self, 'servo_graph_img_label'):
                self.servo_graph_img_label.config(image="", text=f"Fehler beim Laden des Servo Graphs: {e}")
            if hasattr(self, 'servo_cone_img_label'):
                self.servo_cone_img_label.config(image="", text=f"Fehler beim Laden des Cone Details: {e}")
# Hauptausführungslogik
if __name__ == "__main__":
    try:
        app = ControlApp()
        app.root.mainloop()
    except Exception as e:
        import traceback
        print(f"Fehler beim Starten der Anwendung: {e}")
        traceback.print_exc()
