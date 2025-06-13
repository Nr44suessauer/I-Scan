"""
IScan-ControlScript - Main Program (Refactored with Modular GUI)
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
from tkinter import filedialog, messagebox

# Import eigener Module
from api_client import ApiClient
from logger import Logger
from device_control import DeviceControl
from operation_queue import OperationQueue
from webcam_helper import WebcamHelper
from angle_calculator_commands import AngleCalculatorInterface, show_angle_calculator_dialog

# Import modularer GUI-Komponenten
from gui.main_window import MainWindow

# Konstanten für Standardwerte und Berechnungen
PI = 3.141592653589793
DEFAULT_VALUES = {
    'base_url': "http://192.168.137.7",
    'diameter': "28",
    'speed': "80",
    'distance': "3.0",
    'direction': "1",
    'led_color': "#B00B69",
    'led_brightness': "69"
}


class ControlApp:
    """
    Main application class for the control application (Refactored)
    Manages the GUI, user interactions, and coordinates the
    various components of the application using modular GUI structure.
    """
    
    def __init__(self):
        """Initializes the control application and sets up the GUI"""
        # Initialize main window with modular GUI components
        self.main_window = MainWindow("I-Scan Wizard", DEFAULT_VALUES)
        self.root = self.main_window.root
        
        # Get all widgets from main window
        self.widgets = self.main_window.get_all_widgets()
        
        # Status variables (now managed by main window)
        self.position = self.main_window.position
        self.servo_angle_var = self.main_window.servo_angle_var
        self.base_url_var = self.main_window.base_url_var
        self.last_distance_value = self.main_window.last_distance_value
        self.repeat_queue = self.main_window.repeat_queue
        self.global_delay = self.main_window.global_delay
        
        # Output widget
        self.output = self.main_window.output
        
        # Webcam initialisieren
        self.webcam = WebcamHelper(device_index=0, frame_size=(320, 240))
        
        # Create all GUI widgets
        self.main_window.create_all_widgets()
        
        # Update widgets dictionary after creation
        self.widgets = self.main_window.get_all_widgets()
        
        # Logger initialisieren
        self.logger = Logger(
            self.output, 
            self.position, 
            self.servo_angle_var, 
            self.main_window.update_position_label
        )
        
        # Add webcam to widgets dict
        self.widgets['webcam'] = self.webcam
        
        # Operationswarteschlange initialisieren
        self.operation_queue = OperationQueue(self.logger, self.widgets['queue_queue_list'])
        
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
    
    def assign_callbacks(self):
        """
        Assign all callback functions to GUI components using modular structure
        """
        # Prepare callback dictionary for main window
        callbacks = {
            'webcam': {
                'start_camera': self.start_camera,
                'stop_camera': self.stop_camera,
                'take_photo': self.take_photo,
                'add_photo_to_queue': self.add_photo_to_queue,
                'set_camera_device': self.set_camera_device_index,
                'set_delay': self.set_global_delay
            },
            'servo': {
                'servo_exec': self.device_control.servo_cmd,
                'servo_add': self.add_servo_to_queue
            },
            'stepper': {
                'stepper_exec': self.device_control.stepper_cmd,
                'stepper_add': self.add_stepper_to_queue
            },
            'led': {
                'led_exec': self.device_control.led_cmd,
                'led_add': self.add_led_color_to_queue,
                'bright_exec': self.device_control.bright_cmd,
                'bright_add': self.add_brightness_to_queue
            },
            'calculator': {
                'execute_visualisation': self.execute_visualisation_mode,
                'execute_silent': self.execute_silent_mode
            },
            'queue': {
                'queue_exec': self.execute_queue,
                'queue_clear': self.operation_queue.clear,
                'queue_remove': lambda: self.remove_selected_operation(self.widgets['queue_queue_list'].curselection()),
                'queue_export': self.export_queue_to_csv,
                'queue_import': self.import_queue_from_csv
            },
            'button_exec': self.device_control.button_cmd,
            'button_add': self.add_button_to_queue,
            'home_exec': lambda: threading.Thread(target=self.device_control.home_func).start(),
            'home_add': self.add_home_to_queue
        }
        
        # Set callbacks in main window
        self.main_window.set_callbacks(callbacks)
    
    def start_camera(self):
        """Start camera with current device index"""
        device_index = self.main_window.set_camera_device_index()
        if self.webcam.start_camera(device_index):
            self.update_webcam_display()
            self.logger.log("Kamera gestartet")
        else:
            self.logger.log("Fehler beim Starten der Kamera")
    
    def stop_camera(self):
        """Stop camera"""
        self.webcam.stop_camera()
        self.main_window.webcam_display.set_webcam_status("Kamera gestoppt")
        self.logger.log("Kamera gestoppt")
    
    def take_photo(self):
        """Take a photo with current camera"""
        if self.webcam.take_photo():
            self.logger.log("Foto aufgenommen")
        else:
            self.logger.log("Fehler beim Aufnehmen des Fotos")
    
    def add_photo_to_queue(self):
        """Add photo operation to queue"""
        description = "Foto aufnehmen"
        self.operation_queue.add('photo', {}, description)
    
    def update_webcam_display(self):
        """Update webcam display with current frame"""
        if self.webcam.is_active():
            frame = self.webcam.get_current_frame()
            if frame is not None:
                self.main_window.webcam_display.update_webcam_display(frame)
        # Schedule next update
        self.root.after(30, self.update_webcam_display)
    
    def set_camera_device_index(self):
        """Set camera device index"""
        device_index = self.main_window.set_camera_device_index()
        if self.webcam.set_device_index(device_index):
            self.logger.log(f"Kamera-Gerät auf Index {device_index} geändert")
        else:
            self.logger.log(f"Fehler beim Ändern des Kamera-Geräts auf Index {device_index}")
    
    def set_global_delay(self):
        """Set global delay for autofocus"""
        self.main_window.set_global_delay()
        self.logger.log(f"Autofokus-Delay auf {self.main_window.global_delay} Sekunden gesetzt")
    
    def add_servo_to_queue(self):
        """Add servo operation to queue"""
        try:
            angle = self.main_window.servo_controls.get_angle()
            if angle is not None:
                description = f"Servo: Winkel auf {angle}° setzen"
                self.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen des Servo-Befehls: {e}")
    
    def add_stepper_to_queue(self):
        """Add stepper operation to queue"""
        try:
            values = self.main_window.stepper_controls.get_values()
            if values:
                description = f"Stepper: {values['distance']} cm in Richtung {values['direction']} mit Geschwindigkeit {values['speed']}"
                self.operation_queue.add('stepper', values, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen des Stepper-Befehls: {e}")
    
    def add_led_color_to_queue(self):
        """Add LED color operation to queue"""
        try:
            color = self.main_window.led_controls.get_color()
            if color:
                description = f"LED Farbe: {color}"
                self.operation_queue.add('led', {'color': color}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen des LED-Farb-Befehls: {e}")
    
    def add_brightness_to_queue(self):
        """Add LED brightness operation to queue"""
        try:
            brightness = self.main_window.led_controls.get_brightness()
            if brightness is not None:
                description = f"LED Helligkeit: {brightness}%"
                self.operation_queue.add('brightness', {'brightness': brightness}, description)
        except Exception as e:
            self.logger.log(f"Fehler beim Hinzufügen des Helligkeits-Befehls: {e}")
    
    def add_button_to_queue(self):
        """Add button query operation to queue"""
        description = "Button-Status abfragen"
        self.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """Add home operation to queue"""
        description = "Home-Funktion ausführen"
        self.operation_queue.add('home', {}, description)
    
    def execute_queue(self):
        """Execute all operations in queue"""
        if self.operation_queue.is_empty():
            self.logger.log("Warteschlange ist leer")
            return
        
        def run_queue():
            self.operation_queue.execute_all(self.repeat_queue.get())
        
        threading.Thread(target=run_queue).start()
    
    def remove_selected_operation(self, selection):
        """Remove selected operation from queue"""
        if selection:
            for index in reversed(selection):
                self.operation_queue.remove_at_index(index)
    
    def export_queue_to_csv(self):
        """Export queue to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            if self.operation_queue.export_to_csv(filename):
                self.logger.log(f"Warteschlange exportiert nach: {filename}")
            else:
                self.logger.log("Fehler beim Exportieren der Warteschlange")
    
    def import_queue_from_csv(self):
        """Import queue from CSV file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            if self.operation_queue.import_from_csv(filename):
                self.logger.log(f"Warteschlange importiert von: {filename}")
            else:
                self.logger.log("Fehler beim Importieren der Warteschlange")
    
    def execute_visualisation_mode(self):
        """Execute Calculator_Angle_Maschine in visualization mode"""
        try:
            params = self.main_window.angle_calculator.get_parameters()
            self.angle_calculator.execute_visualisation_mode(params)
            self.logger.log("Visualisierungsmodus gestartet")
            # Refresh images after calculation
            self.main_window.angle_calculator.load_servo_images()
        except Exception as e:
            self.logger.log(f"Fehler beim Ausführen des Visualisierungsmodus: {e}")
    
    def execute_silent_mode(self):
        """Execute Calculator_Angle_Maschine in silent mode"""
        try:
            params = self.main_window.angle_calculator.get_parameters()
            self.angle_calculator.execute_silent_mode(params)
            self.logger.log("Silent-Modus gestartet")
        except Exception as e:
            self.logger.log(f"Fehler beim Ausführen des Silent-Modus: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            if self.webcam:
                self.webcam.stop_camera()
            self.root.destroy()
        except Exception as e:
            print(f"Fehler beim Schließen der Anwendung: {e}")
            self.root.destroy()
    
    def run(self):
        """Start the main application loop"""
        self.main_window.run()


# Hauptausführungslogik
if __name__ == "__main__":
    try:
        app = ControlApp()
        app.run()
    except Exception as e:
        import traceback
        print(f"Fehler beim Starten der Anwendung: {e}")
        traceback.print_exc()
