"""
IScan-ControlScript - Hauptprogramm
Eine GUI-Anwendung zur Steuerung von Hardware über eine API-Schnittstelle.
Diese Anwendung stellt eine Benutzeroberfläche bereit, um mit Hardware-Komponenten
wie Servomotoren, Schrittmotoren, LED-Leuchten und Buttons über eine REST-API zu interagieren.
"""
import os
import csv
import json
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, Label, filedialog, messagebox, StringVar, DoubleVar, IntVar, BooleanVar
from PIL import Image, ImageTk

# Import eigener Module
from api_client import ApiClient
from logger import Logger
from device_control import DeviceControl
from operation_queue import OperationQueue
from webcam_helper import WebcamHelper

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
    Hauptanwendungsklasse für die Steueranwendung
    Verwaltet die GUI, Benutzerinteraktionen und koordiniert die
    verschiedenen Komponenten der Anwendung.
    """
    
    def __init__(self):
        """Initialisiert die Steueranwendung und richtet die GUI ein"""
        self.root = tk.Tk()
        self.root.title("I-Scan ControlScript - Hardware-Steuerung")
        
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
        Erstellt die Anzeige für Text mit Bildlauf
        Zeigt Protokollnachrichten und Operationsergebnisse an
        """
        self.output = scrolledtext.ScrolledText(self.root, width=80, height=16, state='disabled')
        self.output.pack(padx=10, pady=10, anchor='w')
    
    def create_webcam_frame(self):
        """
        Erstellt den Rahmen für die Webcam-Anzeige und die Steuerelemente
        """
        webcam_frame = tk.LabelFrame(self.root, text="Kamera")
        webcam_frame.pack(fill="both", expand=True, padx=10, pady=5, side=tk.LEFT)
        
        # Rahmen für die Kameraanzeige
        camera_view_frame = tk.Frame(webcam_frame)
        camera_view_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Label für die Kameraanzeige
        self.cam_label = tk.Label(camera_view_frame, text="Kein Kamerabild", 
                          bg="black", fg="white", width=40, height=15)
        self.cam_label.pack(fill="both", expand=True)
        
        # Rahmen für die Kamera-Schaltflächen
        camera_control_frame = tk.Frame(webcam_frame)
        camera_control_frame.pack(fill="x", padx=5, pady=5)
          # Schaltflächen für die Kamerabedienung
        self.btn_start_camera = tk.Button(camera_control_frame, text="Kamera starten", 
                                bg="#4CAF50", fg="white", width=15)
        self.btn_start_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_stop_camera = tk.Button(camera_control_frame, text="Kamera stoppen", 
                               bg="#F44336", fg="white", width=15)
        self.btn_stop_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_take_photo = tk.Button(camera_control_frame, text="Foto aufnehmen", 
                              bg="#2196F3", fg="white", width=15)
        self.btn_take_photo.pack(side=tk.LEFT, padx=2)
        
        self.btn_add_photo_to_queue = tk.Button(camera_control_frame, text="+", 
                                     bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.btn_add_photo_to_queue.pack(side=tk.LEFT, padx=2)
    
    def create_servo_frame(self):
        """
        Erstellt den Rahmen für die Servo-Steuerung
        Ermöglicht es dem Benutzer, den Servo-Winkel einzustellen
        """
        servo_frame = tk.LabelFrame(self.root, text="Servo-Steuerung")
        servo_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(servo_frame, text="Winkel (0-90):").pack(side=tk.LEFT)
        self.servo_angle = tk.Entry(servo_frame, width=5)
        self.servo_angle.pack(side=tk.LEFT)
        
        # Schaltflächen werden in assign_callbacks konfiguriert
        self.servo_exec_btn = tk.Button(servo_frame, text="Servo ausführen")
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
    
    def on_closing(self):
        """Methode zum sauberen Schließen des Programms"""
        if hasattr(self, 'webcam'):
            self.webcam.stoppen()
        self.root.destroy()


# Hauptausführungslogik
if __name__ == "__main__":
    try:
        app = ControlApp()
        app.root.mainloop()
    except Exception as e:
        import traceback
        print(f"Fehler beim Starten der Anwendung: {e}")
        traceback.print_exc()
