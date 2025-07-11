"""
Logger Module
Manages logging and display of messages

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""
import re
import tkinter as tk


class Logger:
    """
    Class for logging and displaying messages
    Manages the output display and processes log messages to update position and servo angle values from the log content.
    """
    
    def __init__(self, output_widget, position_var, servo_angle_var, update_callback):
        """
        Initializes the logger with UI elements and variables to monitor

        Args:
            output_widget: The ScrolledText widget where logs are displayed
            position_var: The DoubleVar for tracking the current position
            servo_angle_var: The IntVar for tracking the current servo angle
            update_callback: Function called after updating position or angle
        """
        self.output = output_widget
        self.position = position_var
        self.servo_angle_var = servo_angle_var
        self.update_callback = update_callback
    
    def log(self, msg):
        """
        Displays a message in the log with appropriate formatting and color
        Also analyzes the message to update position and servo angle values

        Args:
            msg (str): The message to log
        """
        # Determine message type and select color based on content
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["motor", "stepper", "steps"]):
            color = "#1e90ff"  # Blue for motor/stepper messages
        elif "servo" in msg_lower:
            color = "#228B22"  # Green for servo messages
        elif "button" in msg_lower:
            color = "#ff8800"  # Orange for button messages
        elif "led" in msg_lower or "color" in msg_lower or "brightness" in msg_lower:
            color = "#c71585"  # Magenta for LED messages
        else:
            color = "#000000"  # Black for other messages
        # Add message to output widget with selected color
        self.output.config(state='normal')
        self.output.insert(tk.END, msg + "\n\n", (color,))
        self.output.tag_config(color, foreground=color)
        self.output.see(tk.END)
        self.output.config(state='disabled')
        # Update GUI after each log output
        try:
            self.update_callback()
        except Exception:
            pass
        # Analyze log message to update position and servo angle
        self._update_from_log(msg)
    
    def _update_from_log(self, msg):
        """
        Updates position and servo angle based on log messages
        Analyzes various formats of log messages to extract relevant values
        
        Args:
            msg (str): The log message to analyze
        """
        # Format 1: Standard format with position field
        # "Motor: 100 Steps, 0.21 cm, Direction down, Position: 10.50 cm"
        try:
            motor_match = re.search(r"Motor:.*Steps,.*cm, Direction .*, Position: ([-\d\.]+) cm", msg)
            if motor_match:
                new_pos = float(motor_match.group(1))
                self.position.set(new_pos)
                self.update_callback()
                return
        except Exception:
            pass
            
        # Format 2: Legacy-Format (für Abwärtskompatibilität)
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
            
        # Servo-Log-Format: "Servo set to 45 degrees. Response: ..."
        try:
            servo_match = re.search(r"Servo: Angle (\d+)°", msg)
            if servo_match:
                angle = int(servo_match.group(1))
                self.servo_angle_var.set(angle)
                self.update_callback()
        except Exception:
            pass
