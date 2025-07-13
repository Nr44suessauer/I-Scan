"""
IScan-Script - API Control Window
A GUI application for controlling hardware through an API interface.
This application provides a user interface to interact with hardware components 
like servo motors, stepper motors, LED lights, and buttons via a REST API.
"""

import tkinter as tk
from tkinter import scrolledtext, Label
import threading
import requests
import time
import json
import re
import math
import csv
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import os
from datetime import datetime

# Constants for default values and calculations
PI = 3.141592653589793
DEFAULT_BASE_URL = "http://192.168.137.232"
DEFAULT_DIAMETER = "28"
DEFAULT_SPEED = "80"
DEFAULT_DISTANCE = "3.0"
DEFAULT_DIRECTION = "1"
DEFAULT_LED_COLOR = "#B00B69"
DEFAULT_LED_BRIGHTNESS = "69"

class CameraHelper:
    """
    Klasse zur Steuerung einer Webcam über OpenCV
    Bietet Methoden zum Anzeigen des Kamera-Streams und Aufnehmen von Bildern
    """
    
    def __init__(self, device_index=0, frame_size=(320, 240)):
        """
        Initialisiert die Webcam mit dem angegebenen Geräteindex und Framegröße
        
        Args:
            device_index (int): Index der zu verwendenden Kamera (Standard: 0)
            frame_size (tuple): Größe des angezeigten Frames (Breite, Höhe)
        """
        self.device_index = device_index
        self.frame_size = frame_size
        self.cap = None
        self.running = False
        self.current_frame = None
        self.thread = None
        self.bild_zaehler = 0
    
    def starten(self):
        """Kamera starten und initialisieren"""
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            return False
        self.running = True
        return True
    
    def stop_camera(self):
        """Stop camera stream and release resources"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
        self.cap = None
    
    def read_frame(self):
        """Einzelnes Frame von der Kamera lesen"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
    
    def stream_loop(self, panel, fps=30):
        """
        Haupt-Loop für den Kamera-Stream
        
        Args:
            panel: Das Label-Widget zur Anzeige des Streams
            fps (int): Gewünschte Bildrate für den Stream
        """
        delay = max(1, int(1000 / fps))
        
        while self.running:
            frame = self.read_frame()
            if frame is not None:
                # Bild auf die gewünschte Größe skalieren
                frame = cv2.resize(frame, self.frame_size)
                
                # Bild für Tkinter konvertieren (BGR -> RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Foto speichern im aktuellen Frame
                self.current_frame = frame.copy()
                
                # In ein Format umwandeln, das Tkinter anzeigen kann
                img = tk.PhotoImage(data=cv2.imencode('.png', rgb_frame)[1].tobytes())
                
                # Bild im Panel anzeigen
                panel.configure(image=img)
                panel.image = img  # Referenz halten!
            
            # Pause für FPS-Begrenzung
            time.sleep(delay / 1000.0)
    
    def start_stream(self, panel):
        """
        Kamerastream in einem separaten Thread starten
        
        Args:
            panel: Das Label-Widget zur Anzeige des Streams
        """
        if self.starten():
            self.thread = threading.Thread(target=self.stream_loop, args=(panel,))
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def foto_aufnehmen(self, ordner=None):
        """
        Foto aufnehmen und speichern
        
        Args:
            ordner (str, optional): Ordner zum Speichern des Fotos
            
        Returns:
            str: Pfad zum gespeicherten Foto oder None bei Fehler
        """
        if self.current_frame is None:
            return None
            
        # Zeitstempel für eindeutige Dateinamen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Basispfad bestimmen
        if ordner is None:
            # Verwende aktuelles Verzeichnis, falls nicht angegeben
            base_path = os.path.dirname(os.path.abspath(__file__))
            ordner = os.path.join(base_path, "fotos")
        
        # Ordner erstellen, falls nicht vorhanden
        os.makedirs(ordner, exist_ok=True)
        
        # Dateinamen generieren
        dateiname = f"kamera_{timestamp}_{self.bild_zaehler}.jpg"
        dateipfad = os.path.join(ordner, dateiname)
        
        # Bild speichern
        cv2.imwrite(dateipfad, self.current_frame)
        self.bild_zaehler += 1
        
        return dateipfad

class ApiClient:
    """
    Class for API communication
    Handles all HTTP requests to the API endpoints and provides
    methods for controlling different hardware components.
    """
    
    @staticmethod
    def make_request(endpoint, params=None, base_url=None, timeout=30):
        """
        Sends a GET request to the specified API endpoint with extended timeout.
        
        Args:
            endpoint (str): The API endpoint to call
            params (dict, optional): Query parameters to include in the request
            base_url (str): The base URL of the API
            timeout (int): Request timeout in seconds
            
        Returns:
            The JSON response if valid, otherwise the raw text response
        """
        url = f"{base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.exceptions.RequestException as e:
            return f"Error in API request: {e}"
    
    @staticmethod
    def set_servo_angle(angle, base_url):
        """
        Sets the servo angle via the API
        
        Args:
            angle (int): The angle to set (0-90 degrees)
            base_url (str): The base URL of the API
            
        Returns:
            str: Response message with the result of the operation
        """
        if not 0 <= angle <= 90:
            return "Error: The angle must be between 0 and 90 degrees."
        params = {"angle": angle}
        response = ApiClient.make_request("setServo", params, base_url)
        return f"Servo set to {angle} degrees. Response: {response}"
    
    @staticmethod
    def move_stepper(steps, direction, speed, base_url):
        """
        Controls the stepper motor via the API
        
        Args:
            steps (int): The number of steps to move
            direction (int): The direction to move (1 for up, -1 for down)
            speed (int, optional): The speed of the movement
            base_url (str): The base URL of the API
            
        Returns:
            str: Response message with the result of the operation
        """
        if steps < 0:
            return "Error: The number of steps must be positive."
        if direction not in [1, -1]:
            return "Error: The direction must be 1 (up) or -1 (down)."
        params = {"steps": steps, "direction": direction}
        if speed is not None:
            params["speed"] = speed
        response = ApiClient.make_request("setMotor", params, base_url)
        dir_text = "up" if direction == 1 else "down"
        speed_text = f" with speed {speed}" if speed is not None else ""
        return f"Stepper motor moves {steps} steps {dir_text}{speed_text}. Response: {response}"
    
    @staticmethod
    def set_led_color(color_hex, base_url):
        """
        Sets the LED color via the API
        
        Args:
            color_hex (str): The hexadecimal color code (e.g., "#FF0000")
            base_url (str): The base URL of the API
            
        Returns:
            str: Response message with the result of the operation
        """
        if not color_hex.startswith("#"):
            color_hex = "#" + color_hex
        params = {"hex": color_hex}
        response = ApiClient.make_request("hexcolor", params, base_url)
        return f"LED color set to {color_hex}. Response: {response}"
    
    @staticmethod
    def set_led_brightness(brightness, base_url):
        """
        Sets the LED brightness via the API
        
        Args:
            brightness (int): The brightness level (0-100 percent)
            base_url (str): The base URL of the API
            
        Returns:
            str: Response message with the result of the operation
        """
        if not 0 <= brightness <= 100:
            return "Error: Brightness must be between 0 and 100 percent."
        params = {"value": brightness}
        response = ApiClient.make_request("setBrightness", params, base_url)
        return f"LED brightness set to {brightness}%. Response: {response}"
    
    @staticmethod
    def get_button_state(base_url, nocache=False):
        """
        Queries the button state via the API
        
        Args:
            base_url (str): The base URL of the API
            nocache (bool): If True, adds a timestamp to prevent caching
            
        Returns:
            The button state response from the API
        """
        endpoint = "getButtonState"
        if nocache:
            current_time = int(time.time())
            endpoint = f"{endpoint}?nocache={current_time}"
        response = ApiClient.make_request(endpoint, base_url=base_url)
        return response
    
    @staticmethod
    def is_button_pressed(response):
        """
        Checks if the button is pressed based on the API response
        Different response formats are supported for compatibility.
        
        Args:
            response: The API response to check
            
        Returns:
            bool: True if the button is pressed, False otherwise
        """
        btn_str = str(response).lower()
        return ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)


class Logger:
    """
    Class for logging and displaying messages
    Manages the output display and processes log messages to update
    position and servo angle values from the log content.
    """
    
    def __init__(self, output_widget, position_var, servo_angle_var, update_callback):
        """
        Initialize the logger with UI elements and variables to track
        
        Args:
            output_widget: The ScrolledText widget where logs are displayed
            position_var: The DoubleVar tracking the current position
            servo_angle_var: The IntVar tracking the current servo angle
            update_callback: Function to call after updating position or angle
        """
        self.output = output_widget
        self.position = position_var
        self.servo_angle_var = servo_angle_var
        self.update_callback = update_callback
    
    def log(self, msg):
        """
        Display a message in the log with appropriate formatting and color
        Also parses the message to update position and servo angle values
        
        Args:
            msg (str): The message to log
        """
        # Determine message type and choose color based on content
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["motor", "stepper", "schrittmotor", "steps"]):
            color = "#1e90ff"  # Blue for motor/stepper messages
        elif "servo" in msg_lower:
            color = "#228B22"  # Green for servo messages
        elif "button" in msg_lower:
            color = "#ff8800"  # Orange for button messages
        elif "led" in msg_lower or "color" in msg_lower or "brightness" in msg_lower:
            color = "#c71585"  # Magenta for LED messages
        else:
            color = "#000000"  # Black for other messages
            
        # Add the message to the output widget with the selected color
        self.output.config(state='normal')
        self.output.insert(tk.END, msg + "\n\n", (color,))
        self.output.tag_config(color, foreground=color)
        self.output.see(tk.END)
        self.output.config(state='disabled')
        
        # Update the GUI after each log output
        try:
            self.update_callback()
        except Exception:
            pass
            
        # Parse the log message to update position and servo angle
        self._update_from_log(msg)
    
    def _update_from_log(self, msg):
        """
        Updates position and servo angle based on log messages
        Parses different formats of log messages to extract the relevant values
        
        Args:
            msg (str): The log message to parse
        """
        # Format 1: Standard format with Position field
        # "Motor: 100 Steps, 0.21 cm, Direction down, Position: 10.50 cm"
        try:
            motor_match = re.search(r"Motor:.*Steps,.*cm, Direction .*, Position: ([-\d\.]+) cm", msg)
            if motor_match:
                pos_cm = float(motor_match.group(1))
                self.position.set(pos_cm)
                self.update_callback()
                return
        except Exception:
            pass
            
        # Format 2: Legacy format (for backward compatibility)
        # "3.5 cm → 1234 Steps (Gear 28.5 mm)...direction 1"
        try:
            match = re.search(r"([\d,.]+) cm → (\d+) Steps \(Gear ([\d,.]+) mm\).*direction ([-]?[1])", msg)
            if match:
                dist_cm = float(match.group(1).replace(",", "."))
                direction = int(match.group(4))
                pos_cm = self.position.get()
                if direction == 1:
                    self.position.set(pos_cm + dist_cm)
                else:
                    self.position.set(pos_cm - dist_cm)
                self.update_callback()
                return
        except Exception:
            pass
            
        # Servo log format: "Servo set to 45 degrees. Response: ..."
        try:
            servo_match = re.search(r"Servo set to (\d+) degrees", msg)
            if servo_match:
                angle = int(servo_match.group(1))
                self.servo_angle_var.set(angle)
                self.update_callback()
        except Exception:
            pass


class OperationQueue:
    """
    Class for managing the operation queue
    Handles adding, removing, and executing operations in a queue.
    """
    
    def __init__(self, logger, queue_list):
        """
        Initialize the operation queue
        
        Args:
            logger: The Logger instance to use for logging
            queue_list: The Listbox widget displaying the queue
        """
        self.operations = []
        self.logger = logger
        self.queue_list = queue_list
    
    def add(self, operation_type, params, description):
        """
        Add an operation to the queue
        
        Args:
            operation_type (str): The type of operation (servo, stepper, etc.)
            params (dict): The parameters for the operation
            description (str): A human-readable description of the operation
        """
        self.operations.append({
            'type': operation_type,
            'params': params,
            'description': description
        })
        self.update_display()
        self.logger.log(f"Added to queue: {description}")
    
    def clear(self):
        """Clears all operations from the queue"""
        self.operations.clear()
        self.update_display()
        self.logger.log("Operation queue cleared")
    
    def remove(self, index):
        """
        Remove an operation from the queue by index
        
        Args:
            index (int): The index of the operation to remove
        """
        if 0 <= index < len(self.operations):
            removed = self.operations.pop(index)
            self.update_display()
            self.logger.log(f"Removed from queue: {removed['description']}")
    
    def update_display(self):
        """
        Update the queue display in the UI
        Refreshes the list of operations shown in the queue listbox
        """
        self.queue_list.delete(0, tk.END)  # Clear current entries
        for idx, op in enumerate(self.operations):
            self.queue_list.insert(tk.END, f"{idx+1}. {op['description']}")
    
    def execute_all(self, base_url, widgets, position_var, servo_angle_var, last_distance_value, run_in_thread=True):
        """
        Execute all operations in the queue sequentially
        
        Args:
            base_url (str): The base URL of the API
            widgets (dict): Dictionary of UI widgets needed for operations
            position_var: The DoubleVar tracking the current position
            servo_angle_var: The IntVar tracking the current servo angle
            last_distance_value: The StringVar for the last distance value
            run_in_thread (bool): Ob die Ausführung in einem Thread erfolgen soll (Standard: True)
        """
        if not self.operations:
            self.logger.log("Queue is empty. Nothing to execute.")
            return
        
        self.logger.log("Starting queue execution...")
        
        def run_queue():
            """Run all operations in the queue in a separate thread"""
            total_distance = 0  # Track total distance for distance field update
            
            for idx, op in enumerate(self.operations):
                try:
                    self.logger.log(f"Executing {idx+1}/{len(self.operations)}: {op['description']}")
                    
                    if op['type'] == 'servo':
                        angle = op['params']['angle']
                        ApiClient.set_servo_angle(angle, base_url)
                        self.logger.log(f"Servo: Angle {angle}°")
                        # Aktualisiere Servo-Winkel in der GUI im Hauptthread
                        servo_angle_var.set(angle)
                        widgets['root'].after(0, lambda: widgets['update_position_label']())
                    
                    elif op['type'] == 'stepper':
                        steps = op['params']['steps']
                        direction = op['params']['direction']
                        speed = op['params'].get('speed')
                        
                        # Calculate position change for stepper movement
                        d = float(widgets['diameter_entry'].get())
                        circumference = PI * d  # mm
                        
                        # Calculate distance in cm
                        distance_cm = (steps / 4096) * (circumference / 10)
                        
                        # Update total distance with direction
                        if direction == 1:
                            total_distance += distance_cm
                        else:
                            total_distance -= distance_cm
                            
                        # Update the distance field
                        widgets['root'].after(0, lambda: last_distance_value.set(last_distance_value.get()))
                        
                        # Calculate new position
                        dir_text = "up" if direction == 1 else "down"
                        pos_cm = position_var.get() + (distance_cm if direction == 1 else -distance_cm)
                        
                        # Execute the move
                        ApiClient.move_stepper(steps, direction, speed, base_url)
                        
                        # Log message for stepper
                        self.logger.log(f"Motor: {steps} Steps, {distance_cm:.2f} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
                    
                    elif op['type'] == 'led_color':
                        color_hex = op['params']['color']
                        ApiClient.set_led_color(color_hex, base_url)
                        self.logger.log(f"LED: Color {color_hex}")
                    
                    elif op['type'] == 'led_brightness':
                        brightness = op['params']['brightness']
                        ApiClient.set_led_brightness(brightness, base_url)
                        self.logger.log(f"LED: Brightness {brightness}%")
                    
                    elif op['type'] == 'button':
                        response = ApiClient.get_button_state(base_url)
                        self.logger.log(f"Button status: {response}")
                    
                    elif op['type'] == 'home':
                        self._execute_home_function(base_url, widgets, position_var, last_distance_value)
                        
                    # Small delay between operations
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.logger.log(f"Error executing operation {idx+1}: {e}")
            
            self.logger.log("Queue execution completed!")
        
        if run_in_thread:
            threading.Thread(target=run_queue).start()
        else:
            run_queue()
    
    def _execute_home_function(self, base_url, widgets, position_var, last_distance_value):
        """
        Execute the home function as part of queue execution
        Moves the stepper motor down until the button is pressed,
        then moves up slightly and resets the position to zero.
        
        Args:
            base_url (str): The base URL of the API
            widgets (dict): Dictionary of UI widgets needed for operations
            position_var: The DoubleVar tracking the current position
            last_distance_value: The StringVar for the last distance value
        """
        try:
            d = float(widgets['diameter_entry'].get())
            self.logger.log('Starting Home function...')
            
            # Reset button state
            self.logger.log("Resetting button state...")
            reset_attempts = 0
            max_reset_attempts = 10
            
            # Wait until button is no longer pressed
            while reset_attempts < max_reset_attempts:
                reset_attempts += 1
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                button_still_pressed = ApiClient.is_button_pressed(btn_response)
                
                if button_still_pressed:
                    self.logger.log(f"Button still pressed, waiting for release (attempt {reset_attempts})...")
                    time.sleep(1)
                else:
                    self.logger.log(f"Button released, proceeding with home function.")
                    break
            
            if reset_attempts >= max_reset_attempts:
                self.logger.log("Warning: Could not reset button state, proceeding anyway.")
            
            # Continue with home function
            time.sleep(1)
            
            # Initial 100 steps down
            speed = int(widgets['stepper_speed'].get())
            params = {"steps": 100, "direction": -1, "speed": speed}
            ApiClient.make_request("setMotor", params, base_url)
            pos_cm = position_var.get() - (100 / 4096 * PI * d / 10)
            distance_cm = (100 / 4096 * PI * d / 10)
            self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
            
            # Loop until button is pressed - reduced logging
            max_attempts = 100
            attempt = 0
            button_pressed = False
            
            while not button_pressed and attempt < max_attempts:
                attempt += 1
                
                # Query button state
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                
                # Log only on important events
                if attempt % 5 == 0:
                    self.logger.log(f"Button check attempt {attempt}: Not pressed yet")
                
                # Check button state
                button_pressed = ApiClient.is_button_pressed(btn_response)
                
                if button_pressed:
                    # Button pressed, 100 steps up and finish
                    self.logger.log(f"Button pressed detected on attempt {attempt}")
                    params = {"steps": 100, "direction": 1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = position_var.get() + (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                    break
                else:
                    # Button not pressed, another 100 steps down
                    params = {"steps": 100, "direction": -1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = position_var.get() - (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                    
                    # Delay after each step
                    time.sleep(0.5)
            
            # Warn if needed
            if not button_pressed:
                self.logger.log("Warning: Maximum attempts reached without detecting button press.")
                
            # Set position to 0
            position_var.set(0)
            widgets['root'].after(0, lambda: widgets['update_position_label']())
            self.logger.log("Home function completed, position set to 0.")
            
            # Reset distance field
            widgets['root'].after(0, lambda: (
                widgets['stepper_length_cm'].delete(0, tk.END),
                widgets['stepper_length_cm'].insert(0, "0.00")
            ))
        except Exception as e:
            self.logger.log(f"Error in home function: {e}")


class DeviceControl:
    """
    Class for controlling various hardware devices
    Provides methods to control servo motors, stepper motors, LEDs, and
    query button states through the API.
    """
    
    def __init__(self, logger, base_url_var, widgets, position_var, servo_angle_var):
        """
        Initialize the device controller
        
        Args:
            logger: The Logger instance for logging operations
            base_url_var: The StringVar containing the base URL of the API
            widgets: Dictionary of UI widgets needed for operations
            position_var: The DoubleVar tracking the current position
            servo_angle_var: The IntVar tracking the current servo angle
        """
        self.logger = logger
        self.base_url_var = base_url_var
        self.widgets = widgets
        self.position = position_var
        self.servo_angle_var = servo_angle_var
        
    def servo_cmd(self):
        """
        Execute servo command directly
        """
        try:
            angle = int(self.widgets['servo_angle'].get())
            base_url = self.base_url_var.get()
            ApiClient.set_servo_angle(angle, base_url)
            self.logger.log(f"Servo: Angle {angle}°")
            self.servo_angle_var.set(angle)
            self.widgets['update_position_label']()
        except Exception as e:
            self.logger.log(f"Error: {e}")
            
    def stepper_cmd(self):
        """
        Execute stepper motor command directly
        """
        try:
            d = float(self.widgets['diameter_entry'].get())
            circumference = PI * d  # mm
            length_cm = float(self.widgets['stepper_length_cm'].get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.widgets['stepper_dir'].get()) if self.widgets['stepper_dir'].get() else 1
            speed = int(self.widgets['stepper_speed'].get()) if self.widgets['stepper_speed'].get() else None
            dir_text = "up" if direction == 1 else "down"
            base_url = self.base_url_var.get()
            
            ApiClient.move_stepper(steps, direction, speed, base_url)
            pos_cm = self.position.get() + (length_cm if direction == 1 else -length_cm)
            self.logger.log(f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
        except Exception as e:
            self.logger.log(f"Error: {e}")    def led_cmd(self):
        """
        Set LED color direkt
        """
        try:
            color_hex = self.widgets['led_color'].get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
            base_url = self.base_url_var.get()
            
            ApiClient.set_led_color(color_hex, base_url)
            self.logger.log(f"LED: Color {color_hex}")
        except Exception as e:
            self.logger.log(f"Error: {e}")    def bright_cmd(self):
        """
        Set LED brightness direkt
        """
        try:
            val = int(self.widgets['led_bright'].get())
            base_url = self.base_url_var.get()
            
            ApiClient.set_led_brightness(val, base_url)
            self.logger.log(f"LED: Brightness {val}%")
        except Exception as e:
            self.logger.log(f"Error: {e}")    def button_cmd(self):
        """
        Query button state direkt
        """
        base_url = self.base_url_var.get()
        response = ApiClient.get_button_state(base_url)
        self.logger.log(f"Button status: {response}")    def _home_logic_for_ip(self, base_url):
        try:
            d = float(self.widgets['diameter_entry'].get())
            self.logger.log("Starting Home function...")
            # Erste Überprüfung des Button-Status
            self.logger.log("Checking initial button state...")
            btn_response = ApiClient.get_button_state(base_url, nocache=True)
            button_pressed = ApiClient.is_button_pressed(btn_response)
            if button_pressed:
                self.logger.log("Button is already pressed. Waiting for release...")
                reset_attempts = 0
                max_reset_attempts = 10
                while reset_attempts < max_reset_attempts:
                    reset_attempts += 1
                    time.sleep(1)
                    btn_response = ApiClient.get_button_state(base_url, nocache=True)
                    button_still_pressed = ApiClient.is_button_pressed(btn_response)
                    if button_still_pressed:
                        self.logger.log(f"Button still pressed, waiting for release (attempt {reset_attempts})...")
                    else:
                        self.logger.log("Button released, proceeding with home function.")
                        break
                if reset_attempts >= max_reset_attempts:
                    self.logger.log("Warning: Button still pressed after maximum attempts. Please check hardware.")
                    return
            else:
                self.logger.log("Button is not pressed. Proceeding with home function.")
            time.sleep(1)
            speed = int(self.widgets['stepper_speed'].get())
            params = {"steps": 100, "direction": -1, "speed": speed}
            ApiClient.make_request("setMotor", params, base_url)
            pos_cm = self.position.get() - (100 / 4096 * PI * d / 10)
            distance_cm = (100 / 4096 * PI * d / 10)
            self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
            max_attempts = 100
            attempt = 0
            button_pressed = False
            while not button_pressed and attempt < max_attempts:
                attempt += 1
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                if attempt % 5 == 0:
                    self.logger.log(f"Button check attempt {attempt}: Response: {btn_response}")
                button_pressed = ApiClient.is_button_pressed(btn_response)
                if button_pressed:
                    self.logger.log(f"Button press detected on attempt {attempt}, moving up and completing home")
                    params = {"steps": 100, "direction": 1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = self.position.get() + (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                    break
                else:
                    params = {"steps": 100, "direction": -1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = self.position.get() - (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                    time.sleep(0.5)
                    btn_response = ApiClient.get_button_state(base_url, nocache=True)
                    if ApiClient.is_button_pressed(btn_response):
                        self.logger.log(f"Button press detected after move, proceeding to completion")
                        params = {"steps": 100, "direction": 1, "speed": speed}
                        ApiClient.make_request("setMotor", params, base_url)
                        pos_cm = self.position.get() + (100 / 4096 * PI * d / 10)
                        distance_cm = (100 / 4096 * PI * d / 10)
                        self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                        break
            if not button_pressed:
                self.logger.log("Warning: Maximum attempts reached in home function without detecting button press.")
            self.position.set(0)
            self.widgets['update_position_label']()
            self.logger.log("Home function completed, position set to 0.")
        except Exception as e:
            self.logger.log(f"Error: {e}")def home_func(self):
        """
        Execute the home function
        """
        try:
            base_url = self.base_url_var.get()
            self._home_logic_for_ip(base_url)
        except Exception as e:
            self.logger.log(f"Error: {e}")


class ControlApp:
    """
    Main application class for the control application
    Manages the GUI, user interactions, and coordinates between the
    different components of the application.
    """
    
    def __init__(self):
        """Initialize the control application and set up the GUI"""
        self.root = tk.Tk()
        self.root.title("API Window - Control")
        
        # State variables
        self.position = tk.DoubleVar(value=0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.base_url_var = tk.StringVar(value=DEFAULT_BASE_URL)
        self.last_distance_value = tk.StringVar(value=DEFAULT_DISTANCE)
        self.repeat_queue = tk.BooleanVar(value=False)  # Repeat-Flag
        
        # Webcam Initialisieren
        self.webcam = CameraHelper(device_index=0, frame_size=(320, 240))
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize logger
        self.logger = Logger(
            self.output, 
            self.position, 
            self.servo_angle_var, 
            self.update_position_label
        )
        
        # Widget dictionary for access to GUI elements
        self.widgets = {
            'root': self.root,
            'diameter_entry': self.diameter_entry,
            'servo_angle': self.servo_angle,
            'stepper_length_cm': self.stepper_length_cm,
            'stepper_dir': self.stepper_dir,
            'stepper_speed': self.stepper_speed,
            'led_color': self.led_color,
            'led_bright': self.led_bright,
            'update_position_label': self.update_position_label
        }
        
        # Initialize operation queue
        self.operation_queue = OperationQueue(self.logger, self.queue_list)
        
        # Initialize device control
        self.device_control = DeviceControl(
            self.logger,
            self.base_url_var,
            self.widgets,
            self.position,
            self.servo_angle_var
        )
          # Assign callback functions
        self.assign_callbacks()
      def create_widgets(self):
        """Create all GUI elements in the application window"""
        # URL input field
        self.create_url_frame()
        
        # Gear diameter at top
        self.create_diameter_frame()
        
        # Position and servo angle display at top right
        self.create_position_display()
        
        # Output window
        self.create_output_display()
        
        # Webcam-Anzeige
        self.create_webcam_frame()
        
        # Servo control
        self.create_servo_frame()
        
        # Stepper motor control
        self.create_stepper_frame()
        
        # LED color
        self.create_led_color_frame()
        
        # LED brightness
        self.create_led_brightness_frame()
        
        # Button status
        self.create_button_frame()
        
        # Home function
        self.create_home_frame()
        
        # Operation queue
        self.create_queue_frame()
    
    def create_url_frame(self):
        """
        Create the URL input field frame
        Allows the user to specify the API base URL
        """
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill="x", padx=10, pady=(10,2))
        tk.Label(url_frame, text="API Address:").pack(side=tk.LEFT)
        base_url_entry = tk.Entry(url_frame, textvariable=self.base_url_var, width=30)
        base_url_entry.pack(side=tk.LEFT, padx=5)
      def create_diameter_frame(self):
        """
        Create the diameter input field frame
        Allows the user to specify the gear diameter in mm
        """
        diameter_frame = tk.Frame(self.root)
        diameter_frame.pack(fill="x", padx=10, pady=(2,2))
        tk.Label(diameter_frame, text="Gear Diameter (mm):").pack(side=tk.LEFT)
        self.diameter_entry = tk.Entry(diameter_frame, width=8)
        self.diameter_entry.insert(0, DEFAULT_DIAMETER)
        self.diameter_entry.pack(side=tk.LEFT)
    
    def create_position_display(self):
        """
        Create the position and servo angle display
        Shows the current position and servo angle in the top right corner
        """
        pos_frame = tk.Frame(self.root)
        pos_frame.place(relx=1.0, y=0, anchor='ne')
        tk.Label(pos_frame, text="Position:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.position_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                               fg="blue", width=6, anchor='e', text="0.00")
        self.position_label.pack(side=tk.LEFT)
        tk.Label(pos_frame, text="cm", font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT)
        tk.Label(pos_frame, text="   Servo Angle:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.servo_angle_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                                 fg="green", width=3, anchor='e', text="0")
        self.servo_angle_label.pack(side=tk.LEFT)
        tk.Label(pos_frame, text="°", font=("Arial", 12, "bold"), fg="green").pack(side=tk.LEFT)
    
    def create_output_display(self):
        """
        Create the scrolled text output display
        Shows log messages and operation results
        """
        self.output = scrolledtext.ScrolledText(self.root, width=80, height=16, state='disabled')
        self.output.pack(padx=10, pady=10)
    
    def create_webcam_frame(self):
        """
        Erstellt das Frame für die Webcam-Anzeige und die Steuerelemente
        """
        webcam_frame = tk.LabelFrame(self.root, text="Kamera")
        webcam_frame.pack(fill="both", expand=True, padx=10, pady=5, side=tk.LEFT)
        
        # Frame für die Kameraanzeige
        camera_view_frame = tk.Frame(webcam_frame)
        camera_view_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Label für die Kameraanzeige
        self.cam_label = tk.Label(camera_view_frame, text="Kein Kamerabild", 
                          bg="black", fg="white", width=40, height=15)
        self.cam_label.pack(fill="both", expand=True)
        
        # Frame für die Kamera-Buttons
        camera_control_frame = tk.Frame(webcam_frame)
        camera_control_frame.pack(fill="x", padx=5, pady=5)
        
        # Buttons für Kamerabedienung
        self.btn_start_camera = tk.Button(camera_control_frame, text="Kamera starten", 
                                bg="#4CAF50", fg="white", width=15, 
                                command=self.start_camera)
        self.btn_start_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_stop_camera = tk.Button(camera_control_frame, text="Kamera stoppen", 
                               bg="#F44336", fg="white", width=15, 
                               command=self.stop_camera)
        self.btn_stop_camera.pack(side=tk.LEFT, padx=2)
        
        self.btn_take_photo = tk.Button(camera_control_frame, text="Foto aufnehmen", 
                              bg="#2196F3", fg="white", width=15, 
                              command=self.take_photo)
        self.btn_take_photo.pack(side=tk.LEFT, padx=2)
    
    def create_servo_frame(self):
        """
        Create the servo control frame
        Allows the user to set the servo angle
        """
        servo_frame = tk.LabelFrame(self.root, text="Control Servo")
        servo_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(servo_frame, text="Angle (0-90):").pack(side=tk.LEFT)
        self.servo_angle = tk.Entry(servo_frame, width=5)
        self.servo_angle.pack(side=tk.LEFT)
        
        # Buttons will be configured in assign_callbacks
        self.servo_exec_btn = tk.Button(servo_frame, text="Execute Servo")
        self.servo_exec_btn.pack(side=tk.LEFT, padx=5)
        self.servo_add_btn = tk.Button(servo_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.servo_add_btn.pack(side=tk.LEFT)
    
    def create_stepper_frame(self):
        """
        Create the stepper motor control frame
        Allows the user to control the stepper motor with distance,
        direction, and speed parameters
        """
        stepper_frame = tk.LabelFrame(self.root, text="Control Stepper")
        stepper_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(stepper_frame, text="Distance (cm):").pack(side=tk.LEFT)
        
        self.stepper_length_cm = tk.Entry(stepper_frame, width=8, textvariable=self.last_distance_value)
        self.stepper_length_cm.pack(side=tk.LEFT)
        
        tk.Label(stepper_frame, text="Direction (1/-1):").pack(side=tk.LEFT)
        self.stepper_dir = tk.Entry(stepper_frame, width=4)
        self.stepper_dir.insert(0, DEFAULT_DIRECTION)
        self.stepper_dir.pack(side=tk.LEFT)
        tk.Label(stepper_frame, text="Speed (optional):").pack(side=tk.LEFT)
        self.stepper_speed = tk.Entry(stepper_frame, width=6)
        self.stepper_speed.insert(0, DEFAULT_SPEED)
        self.stepper_speed.pack(side=tk.LEFT)
        
        self.stepper_exec_btn = tk.Button(stepper_frame, text="Execute Stepper")
        self.stepper_exec_btn.pack(side=tk.LEFT, padx=5)
        self.stepper_add_btn = tk.Button(stepper_frame, text="+", 
                               bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.stepper_add_btn.pack(side=tk.LEFT)
    
    def create_led_color_frame(self):
        """
        Create the LED color control frame
        Allows the user to set the LED color with a hex code
        """
        led_frame = tk.LabelFrame(self.root, text="Set LED Color")
        led_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(led_frame, text="Color (e.g. #FF0000):").pack(side=tk.LEFT)
        self.led_color = tk.Entry(led_frame, width=10)
        self.led_color.insert(0, DEFAULT_LED_COLOR)
        self.led_color.pack(side=tk.LEFT)
        
        self.led_exec_btn = tk.Button(led_frame, text="Execute LED")
        self.led_exec_btn.pack(side=tk.LEFT, padx=5)
        self.led_add_btn = tk.Button(led_frame, text="+", 
                            bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.led_add_btn.pack(side=tk.LEFT)
    
    def create_led_brightness_frame(self):
        """
        Create the LED brightness control frame
        Allows the user to set the LED brightness (0-100%)
        """
        bright_frame = tk.LabelFrame(self.root, text="Set LED Brightness")
        bright_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(bright_frame, text="Brightness (0-100):").pack(side=tk.LEFT)
        self.led_bright = tk.Entry(bright_frame, width=5)
        self.led_bright.insert(0, DEFAULT_LED_BRIGHTNESS)
        self.led_bright.pack(side=tk.LEFT)
        
        self.bright_exec_btn = tk.Button(bright_frame, text="Execute Brightness")
        self.bright_exec_btn.pack(side=tk.LEFT, padx=5)
        self.bright_add_btn = tk.Button(bright_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.bright_add_btn.pack(side=tk.LEFT)
    
    def create_button_frame(self):
        """
        Create the button status query frame
        Allows the user to query the current button state
        """
        btn_frame = tk.LabelFrame(self.root, text="Query Button Status")
        btn_frame.pack(fill="x", padx=10, pady=2)
        
        self.button_exec_btn = tk.Button(btn_frame, text="Query Button")
        self.button_exec_btn.pack(side=tk.LEFT, padx=5)
        self.button_add_btn = tk.Button(btn_frame, text="+", 
                              bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.button_add_btn.pack(side=tk.LEFT)
    
    def create_home_frame(self):
        """
        Create the home function frame
        Allows the user to execute the home function,
        which finds the hardware's home position
        """
        home_frame = tk.LabelFrame(self.root, text="Home Function")
        home_frame.pack(fill="x", padx=10, pady=2)
        
        self.home_exec_btn = tk.Button(home_frame, text="Execute Home")
        self.home_exec_btn.pack(side=tk.LEFT, padx=5)
        self.home_add_btn = tk.Button(home_frame, text="+", 
                             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3)
        self.home_add_btn.pack(side=tk.LEFT)
    
    def create_queue_frame(self):
        """
        Create the operation queue frame
        Displays the queued operations and provides controls
        to manage and execute the queue
        """
        queue_frame = tk.LabelFrame(self.root, text="Operation Queue")
        queue_frame.pack(fill="both", expand=True, padx=10, pady=2)
        
        self.queue_list = tk.Listbox(queue_frame, width=70, height=8)
        self.queue_list.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        queue_scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=self.queue_list.yview)
        queue_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.queue_list.config(yscrollcommand=queue_scrollbar.set)
        
        queue_buttons_frame = tk.Frame(queue_frame)
        queue_buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)
        
        self.queue_exec_btn = tk.Button(queue_buttons_frame, text="Execute Queue", 
                               bg="#77dd77", fg="black", font=("Arial", 10, "bold"))
        self.queue_exec_btn.pack(side=tk.LEFT, padx=5)
        
        self.queue_clear_btn = tk.Button(queue_buttons_frame, text="Clear Queue",
                                bg="#ff6961", fg="black")
        self.queue_clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.queue_remove_btn = tk.Button(queue_buttons_frame, text="Remove Selected")
        self.queue_remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.repeat_check = tk.Checkbutton(queue_buttons_frame, text="Repeat Queue", variable=self.repeat_queue)
        self.repeat_check.pack(side=tk.LEFT, padx=5)

        self.queue_export_btn = tk.Button(queue_buttons_frame, text="Export Queue (CSV)", bg="#b0c4de", fg="black")
        self.queue_export_btn.pack(side=tk.LEFT, padx=5)
        self.queue_import_btn = tk.Button(queue_buttons_frame, text="Import Queue (CSV)", bg="#b0c4de", fg="black")
        self.queue_import_btn.pack(side=tk.LEFT, padx=5)
    
    def assign_callbacks(self):
        """
        Assign callback functions to all buttons in the UI
        Links UI events to their corresponding actions
        """
        # Servo callbacks
        self.servo_exec_btn.config(command=self.device_control.servo_cmd)
        self.servo_add_btn.config(command=self.add_servo_to_queue)
        
        # Stepper callbacks
        self.stepper_exec_btn.config(command=self.device_control.stepper_cmd)
        self.stepper_add_btn.config(command=self.add_stepper_to_queue)
        
        # LED callbacks
        self.led_exec_btn.config(command=self.device_control.led_cmd)
        # FEHLER KORRIGIERT: = hinzugefügt
        self.led_add_btn.config(command=self.add_led_color_to_queue)
        
        # Brightness callbacks
        self.bright_exec_btn.config(command=self.device_control.bright_cmd)
        self.bright_add_btn.config(command=self.add_brightness_to_queue)
        
        # Button callbacks
        self.button_exec_btn.config(command=self.device_control.button_cmd)
        self.button_add_btn.config(command=self.add_button_to_queue)
        
        # Home callbacks - run in a separate thread to keep UI responsive
        self.home_exec_btn.config(command=lambda: threading.Thread(target=self.device_control.home_func).start())
        # FEHLER KORRIGIERT: = hinzugefügt
        self.home_add_btn.config(command=self.add_home_to_queue)
        
        # Queue callbacks
        self.queue_exec_btn.config(command=self.execute_queue)
        self.queue_clear_btn.config(command=self.operation_queue.clear)
        self.queue_remove_btn.config(command=lambda: self.remove_selected_operation(self.queue_list.curselection()))
        self.queue_export_btn.config(command=self.export_queue_to_csv)
        self.queue_import_btn.config(command=self.import_queue_from_csv)
    
    def update_position_label(self):
        """
        Update the position display label
        Updates the position and servo angle labels with current values
        """
        self.position_label.config(text=f"{self.position.get():.2f}")
        self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.root.update_idletasks()
    
    def add_servo_to_queue(self):
        """
        Add a servo operation to the queue
        Reads the servo angle from the input field and adds the operation
        """
        try:
            angle = int(self.servo_angle.get())
            description = f"Servo: Set angle to {angle}°"
            self.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_stepper_to_queue(self):
        """
        Add a stepper motor operation to the queue
        Calculates steps from distance and adds the operation to the queue
        """
        try:
            d = float(self.diameter_entry.get())
            circumference = PI * d  # mm
            length_cm = float(self.stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.stepper_dir.get()) if self.stepper_dir.get() else 1
            speed = int(self.stepper_speed.get()) if self.stepper_speed.get() else None
            
            dir_text = "up" if direction == 1 else "down"
            
            params = {"steps": steps, "direction": direction}
            if speed is not None:
                params["speed"] = speed
                
            description = f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}" + (f", Speed: {speed}" if speed else "")
            self.operation_queue.add('stepper', params, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_led_color_to_queue(self):
        """
        Add a LED color operation to the queue
        Reads the color from the input field and adds the operation
        """
        try:
            color_hex = self.led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
                
            description = f"LED: Set color to {color_hex}"
            self.operation_queue.add('led_color', {'color': color_hex}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_brightness_to_queue(self):
        """
        Add a LED brightness operation to the queue
        Reads the brightness from the input field and adds the operation
        """
        try:
            val = int(self.led_bright.get())
            description = f"LED: Set brightness to {val}%"
            self.operation_queue.add('led_brightness', {'brightness': val}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_button_to_queue(self):
        """
        Add a button status query to the queue
        Adds an operation to query the button status
        """
        description = "Button: Query button status"
        self.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """
        Add a home function to the queue
        Adds an operation to execute the home function
        """
        description = "Home: Execute home function"
        self.operation_queue.add('home', {}, description)
    
    def execute_queue(self):
        """
        Execute all operations in the queue
        Starts the queue execution process für alle ausgewählten IPs, synchronisiert mit Repeat
        """
        def run_queue_with_repeat():
            while True:
                selected_ips = self.get_selected_ips()
                if not selected_ips:
                    self.logger.log("Keine IP-Adresse ausgewählt!")
                    break
                for ip in selected_ips:
                    self.logger.log(f"Starte Queue für {ip} ...")
                    self.operation_queue.execute_all(
                        ip,
                        self.widgets,
                        self.position,
                        self.servo_angle_var,
                        self.last_distance_value,
                        run_in_thread=False  # WICHTIG: synchron ausführen!
                    )
                if not self.repeat_queue.get():
                    break
        threading.Thread(target=run_queue_with_repeat).start()
    
    def remove_selected_operation(self, selection):
        """
        Remove the selected operation from the queue
        
        Args:
            selection: The selected item indices from the listbox
        """
        if not selection:
            self.logger.log("No operation selected for removal")
            return
        
        idx = selection[0]
        self.operation_queue.remove(idx)
    
    def export_queue_to_csv(self):
        """
        Exportiert die aktuelle Queue als CSV-Datei.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "params", "description"])
                for op in self.operation_queue.operations:
                    writer.writerow([op['type'], json.dumps(op['params']), op['description']])
            messagebox.showinfo("Export erfolgreich", f"Queue wurde als CSV gespeichert: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def import_queue_from_csv(self):
        """
        Importiert eine Queue aus einer CSV-Datei.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
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
            messagebox.showinfo("Import erfolgreich", f"Queue wurde aus CSV geladen: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))

    def start_camera(self):
        """Startet die Kameraansicht"""
        success = self.webcam.start_stream(self.cam_label)
        if success:
            self.logger.log("Kamera gestartet")
        else:
            self.logger.log("Fehler: Kamera konnte nicht gestartet werden")
            messagebox.showerror("Kamera-Fehler", 
                      "Die Kamera konnte nicht gestartet werden. Bitte Verbindung prüfen.")
    
    def stop_camera(self):
        """Stoppt die Kameraansicht und gibt die Ressourcen frei"""
        self.webcam.stop_camera()
        self.cam_label.config(text="Kamera gestoppt", image="")
        self.logger.log("Kamera gestoppt")
    
    def take_photo(self):
        """Nimmt ein Foto auf und speichert es im Projektordner"""
        if not self.webcam.running or self.webcam.current_frame is None:
            self.logger.log("Fehler: Kamera nicht aktiv oder kein Bild verfügbar")
            return
            
        foto_path = self.webcam.foto_aufnehmen()
        if foto_path:
            self.logger.log(f"Foto aufgenommen und gespeichert als: {foto_path}")
            messagebox.showinfo("Foto aufgenommen", f"Das Foto wurde gespeichert als:\n{foto_path}")
        else:
            self.logger.log("Fehler: Foto konnte nicht gespeichert werden")
            
    def on_closing(self):
        """Methode zum sauberen Schließen des Programms"""
        if hasattr(self, 'webcam'):
            self.webcam.stop_camera()
        self.root.destroy()

    def assign_callbacks(self):
        """
        Assign callback functions to all buttons in the UI
        Links UI events to their corresponding actions
        """
        # Servo callbacks
        self.servo_exec_btn.config(command=self.device_control.servo_cmd)
        self.servo_add_btn.config(command=self.add_servo_to_queue)
        
        # Stepper callbacks
        self.stepper_exec_btn.config(command=self.device_control.stepper_cmd)
        self.stepper_add_btn.config(command=self.add_stepper_to_queue)
        
        # LED callbacks
        self.led_exec_btn.config(command=self.device_control.led_cmd)
        # FEHLER KORRIGIERT: = hinzugefügt
        self.led_add_btn.config(command=self.add_led_color_to_queue)
        
        # Brightness callbacks
        self.bright_exec_btn.config(command=self.device_control.bright_cmd)
        self.bright_add_btn.config(command=self.add_brightness_to_queue)
        
        # Button callbacks
        self.button_exec_btn.config(command=self.device_control.button_cmd)
        self.button_add_btn.config(command=self.add_button_to_queue)
        
        # Home callbacks - run in a separate thread to keep UI responsive
        self.home_exec_btn.config(command=lambda: threading.Thread(target=self.device_control.home_func).start())
        # FEHLER KORRIGIERT: = hinzugefügt
        self.home_add_btn.config(command=self.add_home_to_queue)
        
        # Queue callbacks
        self.queue_exec_btn.config(command=self.execute_queue)
        self.queue_clear_btn.config(command=self.operation_queue.clear)
        self.queue_remove_btn.config(command=lambda: self.remove_selected_operation(self.queue_list.curselection()))
        self.queue_export_btn.config(command=self.export_queue_to_csv)
        self.queue_import_btn.config(command=self.import_queue_from_csv)
    
    def update_position_label(self):
        """
        Update the position display label
        Updates the position and servo angle labels with current values
        """
        self.position_label.config(text=f"{self.position.get():.2f}")
        self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.root.update_idletasks()
    
    def add_servo_to_queue(self):
        """
        Add a servo operation to the queue
        Reads the servo angle from the input field and adds the operation
        """
        try:
            angle = int(self.servo_angle.get())
            description = f"Servo: Set angle to {angle}°"
            self.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_stepper_to_queue(self):
        """
        Add a stepper motor operation to the queue
        Calculates steps from distance and adds the operation to the queue
        """
        try:
            d = float(self.diameter_entry.get())
            circumference = PI * d  # mm
            length_cm = float(self.stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.stepper_dir.get()) if self.stepper_dir.get() else 1
            speed = int(self.stepper_speed.get()) if self.stepper_speed.get() else None
            
            dir_text = "up" if direction == 1 else "down"
            
            params = {"steps": steps, "direction": direction}
            if speed is not None:
                params["speed"] = speed
                
            description = f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}" + (f", Speed: {speed}" if speed else "")
            self.operation_queue.add('stepper', params, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_led_color_to_queue(self):
        """
        Add a LED color operation to the queue
        Reads the color from the input field and adds the operation
        """
        try:
            color_hex = self.led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
                
            description = f"LED: Set color to {color_hex}"
            self.operation_queue.add('led_color', {'color': color_hex}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_brightness_to_queue(self):
        """
        Add a LED brightness operation to the queue
        Reads the brightness from the input field and adds the operation
        """
        try:
            val = int(self.led_bright.get())
            description = f"LED: Set brightness to {val}%"
            self.operation_queue.add('led_brightness', {'brightness': val}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_button_to_queue(self):
        """
        Add a button status query to the queue
        Adds an operation to query the button status
        """
        description = "Button: Query button status"
        self.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """
        Add a home function to the queue
        Adds an operation to execute the home function
        """
        description = "Home: Execute home function"
        self.operation_queue.add('home', {}, description)
    
    def execute_queue(self):
        """
        Execute all operations in the queue
        Starts the queue execution process für alle ausgewählten IPs, synchronisiert mit Repeat
        """
        def run_queue_with_repeat():
            while True:
                selected_ips = self.get_selected_ips()
                if not selected_ips:
                    self.logger.log("Keine IP-Adresse ausgewählt!")
                    break
                for ip in selected_ips:
                    self.logger.log(f"Starte Queue für {ip} ...")
                    self.operation_queue.execute_all(
                        ip,
                        self.widgets,
                        self.position,
                        self.servo_angle_var,
                        self.last_distance_value,
                        run_in_thread=False  # WICHTIG: synchron ausführen!
                    )
                if not self.repeat_queue.get():
                    break
        threading.Thread(target=run_queue_with_repeat).start()
    
    def remove_selected_operation(self, selection):
        """
        Remove the selected operation from the queue
        
        Args:
            selection: The selected item indices from the listbox
        """
        if not selection:
            self.logger.log("No operation selected for removal")
            return
        
        idx = selection[0]
        self.operation_queue.remove(idx)
    
    def export_queue_to_csv(self):
        """
        Exportiert die aktuelle Queue als CSV-Datei.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "params", "description"])
                for op in self.operation_queue.operations:
                    writer.writerow([op['type'], json.dumps(op['params']), op['description']])
            messagebox.showinfo("Export erfolgreich", f"Queue wurde als CSV gespeichert: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def import_queue_from_csv(self):
        """
        Importiert eine Queue aus einer CSV-Datei.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
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
            messagebox.showinfo("Import erfolgreich", f"Queue wurde aus CSV geladen: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))

    def start_camera(self):
        """Startet die Kameraansicht"""
        success = self.webcam.start_stream(self.cam_label)
        if success:
            self.logger.log("Kamera gestartet")
        else:
            self.logger.log("Fehler: Kamera konnte nicht gestartet werden")
            messagebox.showerror("Kamera-Fehler", 
                      "Die Kamera konnte nicht gestartet werden. Bitte Verbindung prüfen.")
    
    def stop_camera(self):
        """Stoppt die Kameraansicht und gibt die Ressourcen frei"""
        self.webcam.stop_camera()
        self.cam_label.config(text="Kamera gestoppt", image="")
        self.logger.log("Kamera gestoppt")
    
    def take_photo(self):
        """Nimmt ein Foto auf und speichert es im Projektordner"""
        if not self.webcam.running or self.webcam.current_frame is None:
            self.logger.log("Fehler: Kamera nicht aktiv oder kein Bild verfügbar")
            return
            
        foto_path = self.webcam.foto_aufnehmen()
        if foto_path:
            self.logger.log(f"Foto aufgenommen und gespeichert als: {foto_path}")
            messagebox.showinfo("Foto aufgenommen", f"Das Foto wurde gespeichert als:\n{foto_path}")
        else:
            self.logger.log("Fehler: Foto konnte nicht gespeichert werden")
            
    def on_closing(self):
        """Methode zum sauberen Schließen des Programms"""
        if hasattr(self, 'webcam'):
            self.webcam.stop_camera()
        self.root.destroy()

    def assign_callbacks(self):
        """
        Assign callback functions to all buttons in the UI
        Links UI events to their corresponding actions
        """
        # Servo callbacks
        self.servo_exec_btn.config(command=self.device_control.servo_cmd)
        self.servo_add_btn.config(command=self.add_servo_to_queue)
        
        # Stepper callbacks
        self.stepper_exec_btn.config(command=self.device_control.stepper_cmd)
        self.stepper_add_btn.config(command=self.add_stepper_to_queue)
        
        # LED callbacks
        self.led_exec_btn.config(command=self.device_control.led_cmd)
        # FEHLER KORRIGIERT: = hinzugefügt
        self.led_add_btn.config(command=self.add_led_color_to_queue)
        
        # Brightness callbacks
        self.bright_exec_btn.config(command=self.device_control.bright_cmd)
        self.bright_add_btn.config(command=self.add_brightness_to_queue)
        
        # Button callbacks
        self.button_exec_btn.config(command=self.device_control.button_cmd)
        self.button_add_btn.config(command=self.add_button_to_queue)
        
        # Home callbacks - run in a separate thread to keep UI responsive
        self.home_exec_btn.config(command=lambda: threading.Thread(target=self.device_control.home_func).start())
        # FEHLER KORRIGIERT: = hinzugefügt
        self.home_add_btn.config(command=self.add_home_to_queue)
        
        # Queue callbacks
        self.queue_exec_btn.config(command=self.execute_queue)
        self.queue_clear_btn.config(command=self.operation_queue.clear)
        self.queue_remove_btn.config(command=lambda: self.remove_selected_operation(self.queue_list.curselection()))
        self.queue_export_btn.config(command=self.export_queue_to_csv)
        self.queue_import_btn.config(command=self.import_queue_from_csv)
    
    def update_position_label(self):
        """
        Update the position display label
        Updates the position and servo angle labels with current values
        """
        self.position_label.config(text=f"{self.position.get():.2f}")
        self.servo_angle_label.config(text=f"{self.servo_angle_var.get()}")
        self.root.update_idletasks()
    
    def add_servo_to_queue(self):
        """
        Add a servo operation to the queue
        Reads the servo angle from the input field and adds the operation
        """
        try:
            angle = int(self.servo_angle.get())
            description = f"Servo: Set angle to {angle}°"
            self.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_stepper_to_queue(self):
        """
        Add a stepper motor operation to the queue
        Calculates steps from distance and adds the operation to the queue
        """
        try:
            d = float(self.diameter_entry.get())
            circumference = PI * d  # mm
            length_cm = float(self.stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.stepper_dir.get()) if self.stepper_dir.get() else 1
            speed = int(self.stepper_speed.get()) if self.stepper_speed.get() else None
            
            dir_text = "up" if direction == 1 else "down"
            
            params = {"steps": steps, "direction": direction}
            if speed is not None:
                params["speed"] = speed
                
            description = f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}" + (f", Speed: {speed}" if speed else "")
            self.operation_queue.add('stepper', params, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_led_color_to_queue(self):
        """
        Add a LED color operation to the queue
        Reads the color from the input field and adds the operation
        """
        try:
            color_hex = self.led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
                
            description = f"LED: Set color to {color_hex}"
            self.operation_queue.add('led_color', {'color': color_hex}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_brightness_to_queue(self):
        """
        Add a LED brightness operation to the queue
        Reads the brightness from the input field and adds the operation
        """
        try:
            val = int(self.led_bright.get())
            description = f"LED: Set brightness to {val}%"
            self.operation_queue.add('led_brightness', {'brightness': val}, description)
        except Exception as e:
            self.logger.log(f"Error adding to queue: {e}")
    
    def add_button_to_queue(self):
        """
        Add a button status query to the queue
        Adds an operation to query the button status
        """
        description = "Button: Query button status"
        self.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """
        Add a home function to the queue
        Adds an operation to execute the home function
        """
        description = "Home: Execute home function"
        self.operation_queue.add('home', {}, description)
    
    def execute_queue(self):
        """
        Execute all operations in the queue
        Starts the queue execution process für alle ausgewählten IPs, synchronisiert mit Repeat
        """
        def run_queue_with_repeat():
            while True:
                selected_ips = self.get_selected_ips()
                if not selected_ips:
                    self.logger.log("Keine IP-Adresse ausgewählt!")
                    break
                for ip in selected_ips:
                    self.logger.log(f"Starte Queue für {ip} ...")PS C:\Users\Marc\Desktop\I-Scan> & C:/Users/Marc/AppData/Local/Programs/Python/Python313/python.exe c:/Users/Marc/Desktop/I-Scan/I-Scan/implementation/Api-Fenster.py
  File "c:\Users\Marc\Desktop\I-Scan\I-Scan\implementation\Api-Fenster.py", 
line 862
    """
    ^^^
IndentationError: expected an indented block after class definition on line 
861
PS C:\Users\Marc\Desktop\I-Scan> & C:/Users/Marc/AppData/Local/Programs/Python/Python313/python.exe c:/Users/Marc/Desktop/I-Scan/I-Scan/implementation/Api-Fenster.py
  File "c:\Users\Marc\Desktop\I-Scan\I-Scan\implementation\Api-Fenster.py", 
line 699
    def servo_cmd(self):
                        ^
IndentationError: unindent does not match any outer indentation level       
PS C:\Users\Marc\Desktop\I-Scan> & C:/Users/Marc/AppData/Local/Programs/Python/Python313/python.exe c:/Users/Marc/Desktop/I-Scan/I-Scan/implementation/Api-Fenster.py
  File "c:\Users\Marc\Desktop\I-Scan\I-Scan\implementation\Api-Fenster.py", 
line 699
    def servo_cmd(self):
                        ^
IndentationError: unindent does not match any outer indentation level       
PS C:\Users\Marc\Desktop\I-Scan>
                    self.operation_queue.execute_all(
                        ip,
                        self.widgets,
                        self.position,
                        self.servo_angle_var,
                        self.last_distance_value,
                        run_in_thread=False  # WICHTIG: synchron ausführen!
                    )
                if not self.repeat_queue.get():
                    break
        threading.Thread(target=run_queue_with_repeat).start()
    
    def remove_selected_operation(self, selection):
        """
        Remove the selected operation from the queue
        
        Args:
            selection: The selected item indices from the listbox
        """
        if not selection:
            self.logger.log("No operation selected for removal")
            return
        
        idx = selection[0]
        self.operation_queue.remove(idx)
    
    def export_queue_to_csv(self):
        """
        Exportiert die aktuelle Queue als CSV-Datei.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "params", "description"])
                for op in self.operation_queue.operations:
                    writer.writerow([op['type'], json.dumps(op['params']), op['description']])
            messagebox.showinfo("Export erfolgreich", f"Queue wurde als CSV gespeichert: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def import_queue_from_csv(self):
        """
        Importiert eine Queue aus einer CSV-Datei.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
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
            messagebox.showinfo("Import erfolgreich", f"Queue wurde aus CSV geladen: {file_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))

    def start_camera(self):
        """Startet die Kameraansicht"""
        success = self.webcam.start_stream(self.cam_label)
        if success:
            self.logger.log("Kamera gestartet")
        else:
            self.logger.log("Fehler: Kamera konnte nicht gestartet werden")
            messagebox.showerror("Kamera-Fehler", 
                      "Die Kamera konnte nicht gestartet werden. Bitte Verbindung prüfen.")
    
    def stop_camera(self):
        """Stoppt die Kameraansicht und gibt die Ressourcen frei"""
        self.webcam.stop_camera()
        self.cam_label.config(text="Kamera gestoppt", image="")
        self.logger.log("Kamera gestoppt")
    
    def take_photo(self):
        """Nimmt ein Foto auf und speichert es im Projektordner"""
        if not self.webcam.running or self.webcam.current_frame is None:
            self.logger.log("Fehler: Kamera nicht aktiv oder kein Bild verfügbar")
            return
            
        foto_path = self.webcam.foto_aufnehmen()
        if foto_path:
            self.logger.log(f"Foto aufgenommen und gespeichert als: {foto_path}")
            messagebox.showinfo("Foto aufgenommen", f"Das Foto wurde gespeichert als:\n{foto_path}")
        else:
            self.logger.log("Fehler: Foto konnte nicht gespeichert werden")
            
    def on_closing(self):
        """Methode zum sauberen Schließen des Programms"""
        if hasattr(self, 'webcam'):
            self.webcam.stop_camera()
        self.root.destroy()

# Hauptausführungslogik
if __name__ == "__main__":
    app = ControlApp()
    # WM_DELETE_WINDOW-Protokoll hinzufügen, damit Ressourcen richtig freigegeben werden
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()