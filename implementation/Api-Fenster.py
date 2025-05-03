import tkinter as tk
from tkinter import scrolledtext
import threading
import requests
import time
import json
import re

# --- API logic from Api-Posunit ---
# BASE_URL is now dynamically read from the input field

def make_api_request(endpoint, params=None, base_url=None, timeout=30):
    """
    Sends a GET request to the specified API endpoint with longer timeout.
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

# --- GUI ---
def main():
    root = tk.Tk()
    root.title("API Window - Control")
    
    # Position and servo angle variables
    position = tk.DoubleVar(value=0)  # DoubleVar for decimal values
    servo_angle_var = tk.IntVar(value=0)
    
    # Operation queue list
    operation_queue = []
    
    # Function to update the display
    def update_position_label():
        # Explizit die Position und Servo-Winkel aktualisieren
        position_label.config(text=f"{position.get():.2f}")
        servo_angle_label.config(text=f"{servo_angle_var.get()}")
        # Alle ausstehenden GUI-Updates verarbeiten
        root.update_idletasks()

    # BASE_URL input field
    url_frame = tk.Frame(root)
    url_frame.pack(fill="x", padx=10, pady=(10,2))
    tk.Label(url_frame, text="API Address:").pack(side=tk.LEFT)
    base_url_var = tk.StringVar(value="http://192.168.178.77")
    base_url_entry = tk.Entry(url_frame, textvariable=base_url_var, width=30)
    base_url_entry.pack(side=tk.LEFT, padx=5)

    # Gear diameter at top
    diameter_frame = tk.Frame(root)
    diameter_frame.pack(fill="x", padx=10, pady=(2,2))
    tk.Label(diameter_frame, text="Gear Diameter (mm):").pack(side=tk.LEFT)
    diameter_entry = tk.Entry(diameter_frame, width=8)
    diameter_entry.insert(0, "28")
    diameter_entry.pack(side=tk.LEFT)
    
    # Position and servo angle display at top right
    pos_frame = tk.Frame(root)
    pos_frame.place(relx=1.0, y=0, anchor='ne')
    tk.Label(pos_frame, text="Position:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
    position_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                             fg="blue", width=6, anchor='e', text="0.00")  # Direkter Text statt textvariable
    position_label.pack(side=tk.LEFT)
    tk.Label(pos_frame, text="cm", font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT)
    tk.Label(pos_frame, text="   Servo Angle:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
    servo_angle_label = tk.Label(pos_frame, font=("Arial", 14, "bold"), 
                                fg="green", width=3, anchor='e', text="0")  # Direkter Text statt textvariable
    servo_angle_label.pack(side=tk.LEFT)
    tk.Label(pos_frame, text="°", font=("Arial", 12, "bold"), fg="green").pack(side=tk.LEFT)

    output = scrolledtext.ScrolledText(root, width=80, height=16, state='disabled')
    output.pack(padx=10, pady=10)

    def log(msg):
        # Recognize process type and choose color
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["motor", "stepper", "schrittmotor", "steps"]):
            color = "#1e90ff"  # Blue
        elif "servo" in msg_lower:
            color = "#228B22"  # Green
        elif "button" in msg_lower:
            color = "#ff8800"  # Orange
        elif "led" in msg_lower or "color" in msg_lower or "brightness" in msg_lower:
            color = "#c71585"  # Magenta
        else:
            color = "#000000"  # Black
            
        output.config(state='normal')
        output.insert(tk.END, msg + "\n\n", (color,))
        output.tag_config(color, foreground=color)
        output.see(tk.END)
        output.config(state='disabled')
        
        # Update in main thread after each log output
        try:
            root.after(0, update_position_label)
        except Exception:
            update_position_label()
            
        # --- Position and servo angle calculation based on log message ---
        # Motor/Stepper log patterns:
        # 1. Standard format: "Motor: 100 Steps, 0.21 cm, Direction down, Position: 10.50 cm"
        try:
            motor_match = re.search(r"Motor:.*Steps,.*cm, Direction .*, Position: ([-\d\.]+) cm", msg)
            if motor_match:
                pos_cm = float(motor_match.group(1))
                position.set(pos_cm)  # Set directly to the position value in the log
                update_position_label()
                return  # Exit early after successful match
        except Exception:
            pass
            
        # 2. Legacy format (for backward compatibility)
        try:
            match = re.search(r"([\d,.]+) cm → (\d+) Steps \(Gear ([\d,.]+) mm\).*direction ([-]?[1])", msg)
            if match:
                dist_cm = float(match.group(1).replace(",", "."))
                steps = int(match.group(2))
                d = float(match.group(3).replace(",", "."))
                direction = int(match.group(4))
                pos_cm = position.get()
                if direction == 1:
                    position.set(pos_cm + dist_cm)
                else:
                    position.set(pos_cm - dist_cm)
                update_position_label()
                return  # Exit early after successful match
        except Exception:
            pass
            
        # Servo log: "Servo set to 45 degrees. Response: ..."
        try:
            servo_match = re.search(r"Servo set to (\d+) degrees", msg)
            if servo_match:
                angle = int(servo_match.group(1))
                servo_angle_var.set(angle)
                update_position_label()
        except Exception:
            pass

    def set_servo_angle(angle, base_url):
        if not 0 <= angle <= 90:
            return "Error: The angle must be between 0 and 90 degrees."
        params = {"angle": angle}
        response = make_api_request("setServo", params, base_url)
        # Set servo angle only here
        try:
            servo_angle_var.set(angle)
            root.after(0, update_position_label)
        except Exception:
            pass
        return f"Servo set to {angle} degrees. Response: {response}"

    def move_stepper(steps, direction, speed, base_url):
        if steps < 0:
            return "Error: The number of steps must be positive."
        if direction not in [1, -1]:
            return "Error: The direction must be 1 (up) or -1 (down)."
        params = {"steps": steps, "direction": direction}
        if speed is not None:
            params["speed"] = speed
        response = make_api_request("setMotor", params, base_url)
        dir_text = "up" if direction == 1 else "down"
        speed_text = f" with speed {speed}" if speed is not None else ""
        # Adjust position
        try:
            # No longer adding steps directly to the position, only in the log parser
            # The log message is evaluated by the parser and sets the position correctly
            update_position_label()
        except Exception:
            pass
        return f"Stepper motor moves {steps} steps {dir_text}{speed_text}. Response: {response}"

    def set_led_color(color_hex, base_url):
        if not color_hex.startswith("#"):
            color_hex = "#" + color_hex
        params = {"hex": color_hex}
        response = make_api_request("hexcolor", params, base_url)
        return f"LED color set to {color_hex}. Response: {response}"

    def set_led_brightness(brightness, base_url):
        if not 0 <= brightness <= 100:
            return "Error: Brightness must be between 0 and 100 percent."
        params = {"value": brightness}
        response = make_api_request("setBrightness", params, base_url)
        return f"LED brightness set to {brightness}%. Response: {response}"

    def get_button_state(base_url):
        response = make_api_request("getButtonState", base_url=base_url)
        return f"Button status: {response}"

    # Servo
    servo_frame = tk.LabelFrame(root, text="Control Servo")
    servo_frame.pack(fill="x", padx=10, pady=2)
    tk.Label(servo_frame, text="Angle (0-90):").pack(side=tk.LEFT)
    servo_angle = tk.Entry(servo_frame, width=5)
    servo_angle.pack(side=tk.LEFT)
    def servo_cmd():
        try:
            angle = int(servo_angle.get())
            # Execute API call
            params = {"angle": angle}
            response = make_api_request("setServo", params, base_url_var.get())
            
            # Simplified log output for servo
            log(f"Servo: Angle {angle}°")
            
            # Update servo angle in GUI
            servo_angle_var.set(angle)
            update_position_label()
        except Exception as e:
            log(f"Error: {e}")
    
    def add_servo_to_queue():
        try:
            angle = int(servo_angle.get())
            description = f"Servo: Set angle to {angle}°"
            add_to_queue('servo', {'angle': angle}, description)
        except Exception as e:
            log(f"Error adding to queue: {e}")
    
    tk.Button(servo_frame, text="Execute Servo", command=servo_cmd).pack(side=tk.LEFT, padx=5)
    tk.Button(servo_frame, text="+", command=add_servo_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # Stepper
    stepper_frame = tk.LabelFrame(root, text="Control Stepper")
    stepper_frame.pack(fill="x", padx=10, pady=2)
    tk.Label(stepper_frame, text="Distance (cm):").pack(side=tk.LEFT)
    
    # Variable für den letzten eingegebenen Wert im Distance-Feld
    last_distance_value = tk.StringVar(value="3.0")  # Standardwert 3
    
    stepper_length_cm = tk.Entry(stepper_frame, width=8, textvariable=last_distance_value)
    stepper_length_cm.pack(side=tk.LEFT)
    
    tk.Label(stepper_frame, text="Direction (1/-1):").pack(side=tk.LEFT)
    stepper_dir = tk.Entry(stepper_frame, width=4)
    stepper_dir.insert(0, "1")
    stepper_dir.pack(side=tk.LEFT)
    tk.Label(stepper_frame, text="Speed (optional):").pack(side=tk.LEFT)
    stepper_speed = tk.Entry(stepper_frame, width=6)
    stepper_speed.insert(0, "80")
    stepper_speed.pack(side=tk.LEFT)
    def stepper_cmd():
        try:
            # Get diameter from length calculation field
            d = float(diameter_entry.get())
            circumference = 3.141592653589793 * d  # mm
            length_cm = float(stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(stepper_dir.get()) if stepper_dir.get() else 1
            speed = int(stepper_speed.get()) if stepper_speed.get() else None
            
            # Execute API call
            dir_text = "up" if direction == 1 else "down"
            params = {"steps": steps, "direction": direction}
            if speed is not None:
                params["speed"] = speed
            response = make_api_request("setMotor", params, base_url_var.get())
            
            # Calculate new position
            pos_cm = position.get() + (length_cm if direction == 1 else -length_cm)
            
            # Use the standard log format that the log parser will recognize
            log(f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
            
            # Position is now updated via the log parser
            # No need to set position directly
        except Exception as e:
            log(f"Error: {e}")
    
    def add_stepper_to_queue():
        try:
            d = float(diameter_entry.get())
            circumference = 3.141592653589793 * d  # mm
            length_cm = float(stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(stepper_dir.get()) if stepper_dir.get() else 1
            speed = int(stepper_speed.get()) if stepper_speed.get() else None
            
            dir_text = "up" if direction == 1 else "down"
            
            params = {"steps": steps, "direction": direction}
            if speed is not None:
                params["speed"] = speed
                
            description = f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}" + (f", Speed: {speed}" if speed else "")
            add_to_queue('stepper', params, description)
        except Exception as e:
            log(f"Error adding to queue: {e}")
            
    tk.Button(stepper_frame, text="Execute Stepper", command=stepper_cmd).pack(side=tk.LEFT, padx=5)
    tk.Button(stepper_frame, text="+", command=add_stepper_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # LED Color
    led_frame = tk.LabelFrame(root, text="Set LED Color")
    led_frame.pack(fill="x", padx=10, pady=2)
    tk.Label(led_frame, text="Color (e.g. #FF0000):").pack(side=tk.LEFT)
    led_color = tk.Entry(led_frame, width=10)
    led_color.insert(0, "#B00B69")
    led_color.pack(side=tk.LEFT)
    def led_cmd():
        try:
            color_hex = led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
            
            # Execute API call
            params = {"hex": color_hex}
            response = make_api_request("hexcolor", params, base_url_var.get())
            
            # Simplified log output for LED color
            log(f"LED: Color {color_hex}")
            
        except Exception as e:
            log(f"Error: {e}")
    
    def add_led_color_to_queue():
        try:
            color_hex = led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
                
            description = f"LED: Set color to {color_hex}"
            add_to_queue('led_color', {'color': color_hex}, description)
        except Exception as e:
            log(f"Error adding to queue: {e}")
            
    tk.Button(led_frame, text="Execute LED", command=led_cmd).pack(side=tk.LEFT, padx=5)
    tk.Button(led_frame, text="+", command=add_led_color_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # LED Brightness
    bright_frame = tk.LabelFrame(root, text="Set LED Brightness")
    bright_frame.pack(fill="x", padx=10, pady=2)
    tk.Label(bright_frame, text="Brightness (0-100):").pack(side=tk.LEFT)
    led_bright = tk.Entry(bright_frame, width=5)
    led_bright.insert(0, "69")
    led_bright.pack(side=tk.LEFT)
    def bright_cmd():
        try:
            val = int(led_bright.get())
            # Execute API call
            params = {"value": val}
            response = make_api_request("setBrightness", params, base_url_var.get())
            
            # Simplified log output for LED brightness
            log(f"LED: Brightness {val}%")
            
        except Exception as e:
            log(f"Error: {e}")
    
    def add_brightness_to_queue():
        try:
            val = int(led_bright.get())
            description = f"LED: Set brightness to {val}%"
            add_to_queue('led_brightness', {'brightness': val}, description)
        except Exception as e:
            log(f"Error adding to queue: {e}")
            
    tk.Button(bright_frame, text="Execute Brightness", command=bright_cmd).pack(side=tk.LEFT, padx=5)
    tk.Button(bright_frame, text="+", command=add_brightness_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # Button Status
    btn_frame = tk.LabelFrame(root, text="Query Button Status")
    btn_frame.pack(fill="x", padx=10, pady=2)
    def button_cmd():
        res = get_button_state(base_url_var.get())
        log(res)
        
    def add_button_to_queue():
        description = "Button: Query button status"
        add_to_queue('button', {}, description)
        
    tk.Button(btn_frame, text="Query Button", command=button_cmd).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="+", command=add_button_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # --- Home Function ---
    def home_func():
        try:
            d = float(diameter_entry.get())
            base_url = base_url_var.get()
            log('Starting Home function...')
            
            # Button-Status zurücksetzen - warte, bis Button nicht mehr gedrückt ist
            log("Resetting button state before starting home function...")
            reset_attempts = 0
            max_reset_attempts = 10
            
            # Schleife, die wartet, bis der Button nicht mehr gedrückt ist
            while reset_attempts < max_reset_attempts:
                reset_attempts += 1
                current_time = int(time.time())
                btn_response = make_api_request(f"getButtonState?nocache={current_time}", base_url=base_url)
                btn_str = str(btn_response).lower()
                button_still_pressed = ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)
                
                if button_still_pressed:
                    log(f"Button still pressed, waiting for release (attempt {reset_attempts})...")
                    time.sleep(1)  # Warte 1 Sekunde
                else:
                    log(f"Button released, proceeding with home function.")
                    break
            
            if reset_attempts >= max_reset_attempts:
                log("Warning: Could not reset button state, proceeding anyway.")
            
            # Zurücksetzen abgeschlossen, fahre mit Home-Funktion fort
            time.sleep(1)  # Extra Wartezeit, um sicherzustellen, dass der Button-Status aktualisiert wird
            
            # Initial 100 steps in direction -1
            params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
            make_api_request("setMotor", params, base_url)
            pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
            distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
            log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
            
            # Loop until button is pressed with explicit check and maximum retries
            max_attempts = 100  # Maximale Anzahl von Versuchen
            attempt = 0
            button_pressed = False
            
            while not button_pressed and attempt < max_attempts:
                attempt += 1
                
                # Force a new button request with a unique parameter to avoid caching
                current_time = int(time.time())
                btn_response = make_api_request(f"getButtonState?nocache={current_time}", base_url=base_url)
                log(f"Button check attempt {attempt}: Response: {btn_response}")
                
                # Explizite String-Prüfung für verschiedene mögliche Formate der Antwort
                btn_str = str(btn_response).lower()
                button_pressed = ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)
                
                log(f"Button: Pressed: {button_pressed} (Attempt {attempt})")
                
                if button_pressed:
                    # Button pressed, 100 steps up and exit
                    log(f"Button pressed detected on attempt {attempt}, moving up and completing home")
                    params = {"steps": 100, "direction": 1, "speed": int(stepper_speed.get())}
                    make_api_request("setMotor", params, base_url)
                    pos_cm = position.get() + (100 / 4096 * 3.141592653589793 * d / 10)
                    distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
                    log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                    break
                else:
                    # Button not pressed, another 100 steps down
                    params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
                    make_api_request("setMotor", params, base_url)
                    pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
                    distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
                    log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                    
                    # Explizite Verzögerung nach jedem Schritt
                    time.sleep(0.5)
            
            # Wenn der Button nie gedrückt wurde, gebe eine Warnung aus
            if not button_pressed:
                log("Warning: Maximum attempts reached in home function without detecting button press.")
            
            # Set position to 0
            position.set(0)
            update_position_label()
            log("Home function completed, position set to 0.")
        except Exception as e:
            log(f"Error: {e}")

    home_frame = tk.LabelFrame(root, text="Home Function")
    home_frame.pack(fill="x", padx=10, pady=2)
    
    def add_home_to_queue():
        description = "Home: Execute home function"
        add_to_queue('home', {}, description)
        
    tk.Button(home_frame, text="Execute Home", command=lambda: threading.Thread(target=home_func).start()).pack(side=tk.LEFT, padx=5)
    tk.Button(home_frame, text="+", command=add_home_to_queue, 
             bg="#b0c4de", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.LEFT)

    # Operation queue listbox and controls
    queue_frame = tk.LabelFrame(root, text="Operation Queue")
    queue_frame.pack(fill="both", expand=True, padx=10, pady=2)
    
    queue_list = tk.Listbox(queue_frame, width=70, height=8)
    queue_list.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
    
    queue_scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=queue_list.yview)
    queue_scrollbar.pack(side=tk.RIGHT, fill="y")
    queue_list.config(yscrollcommand=queue_scrollbar.set)
    
    queue_buttons_frame = tk.Frame(queue_frame)
    queue_buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)
    
    # Function to update the queue listbox
    def update_queue_display():
        queue_list.delete(0, tk.END)  # Clear current items
        for idx, op in enumerate(operation_queue):
            queue_list.insert(tk.END, f"{idx+1}. {op['description']}")
    
    # Function to add operation to queue
    def add_to_queue(operation_type, params, description):
        operation_queue.append({
            'type': operation_type,
            'params': params,
            'description': description
        })
        update_queue_display()
        log(f"Added to queue: {description}")
    
    # Function to execute all operations in queue
    def execute_queue():
        if not operation_queue:
            log("Queue is empty. Nothing to execute.")
            return
        
        log("Starting queue execution...")
        base_url = base_url_var.get()
        
        def run_queue():
            total_distance = 0  # Track total distance for distance field update
            
            for idx, op in enumerate(operation_queue):
                try:
                    log(f"Executing {idx+1}/{len(operation_queue)}: {op['description']}")
                    
                    if op['type'] == 'servo':
                        angle = op['params']['angle']
                        # Verwende den direkten Funktionsaufruf, aber ohne Response-Logging
                        set_servo_angle(angle, base_url)
                        # Nur eine Log-Nachricht ausgeben
                        log(f"Servo: Angle {angle}°")
                    
                    elif op['type'] == 'stepper':
                        steps = op['params']['steps']
                        direction = op['params']['direction']
                        speed = op['params'].get('speed')
                        
                        # Calculate position change for stepper movement
                        d = float(diameter_entry.get())
                        circumference = 3.141592653589793 * d  # mm
                        
                        # Calculate distance in cm (same calculation as in stepper_cmd)
                        distance_cm = (steps / 4096) * (circumference / 10)
                        
                        # Update total distance with direction
                        if direction == 1:
                            total_distance += distance_cm
                        else:
                            total_distance -= distance_cm
                            
                        # Update the distance field with the same value (nicht mit total_distance)
                        # Wir aktualisieren den Wert nur visuell ohne ihn zu verändern
                        root.after(0, lambda: last_distance_value.set(last_distance_value.get()))
                        
                        # Calculate new position
                        dir_text = "up" if direction == 1 else "down"
                        pos_cm = position.get() + (distance_cm if direction == 1 else -distance_cm)
                        
                        # Führe den Move aus ohne zusätzliches Logging
                        move_stepper(steps, direction, speed, base_url)
                        
                        # Nur eine einzige Log-Nachricht für den Stepper
                        log(f"Motor: {steps} Steps, {distance_cm:.2f} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
                    
                    elif op['type'] == 'led_color':
                        color_hex = op['params']['color']
                        # Führe die Funktion aus ohne Response-Logging
                        set_led_color(color_hex, base_url)
                        # Nur ein Log
                        log(f"LED: Color {color_hex}")
                    
                    elif op['type'] == 'led_brightness':
                        brightness = op['params']['brightness']
                        # Führe die Funktion aus ohne Response-Logging
                        set_led_brightness(brightness, base_url)
                        # Nur ein Log
                        log(f"LED: Brightness {brightness}%")
                    
                    elif op['type'] == 'button':
                        # Button-Status abfragen und in einer Meldung ausgeben
                        response = make_api_request("getButtonState", base_url=base_url)
                        log(f"Button status: {response}")
                    
                    elif op['type'] == 'home':
                        # Implementierung der Home-Funktion für die Queue-Ausführung
                        try:
                            d = float(diameter_entry.get())
                            log('Starting Home function...')
                            
                            # Button-Status zurücksetzen - warte, bis Button nicht mehr gedrückt ist
                            log("Resetting button state...")
                            reset_attempts = 0
                            max_reset_attempts = 10
                            
                            # Schleife, die wartet, bis der Button nicht mehr gedrückt ist
                            while reset_attempts < max_reset_attempts:
                                reset_attempts += 1
                                current_time = int(time.time())
                                btn_response = make_api_request(f"getButtonState?nocache={current_time}", base_url=base_url)
                                btn_str = str(btn_response).lower()
                                button_still_pressed = ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)
                                
                                if button_still_pressed:
                                    log(f"Button still pressed, waiting for release (attempt {reset_attempts})...")
                                    time.sleep(1)  # Warte 1 Sekunde
                                else:
                                    log(f"Button released, proceeding with home function.")
                                    break
                            
                            if reset_attempts >= max_reset_attempts:
                                log("Warning: Could not reset button state, proceeding anyway.")
                            
                            # Zurücksetzen abgeschlossen, fahre mit Home-Funktion fort
                            time.sleep(1)  # Extra Wartezeit
                            
                            # Initial 100 steps in direction -1
                            params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
                            make_api_request("setMotor", params, base_url)
                            pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
                            distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
                            log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                            
                            # Loop until button is pressed - reduziertes Logging
                            max_attempts = 100
                            attempt = 0
                            button_pressed = False
                            
                            while not button_pressed and attempt < max_attempts:
                                attempt += 1
                                
                                # Button-Status abfragen mit Anti-Cache-Parameter
                                current_time = int(time.time())
                                btn_response = make_api_request(f"getButtonState?nocache={current_time}", base_url=base_url)
                                
                                # Nur bei wichtigen Ereignissen loggen (alle 5 Versuche oder wenn gedrückt)
                                if attempt % 5 == 0:
                                    log(f"Button check attempt {attempt}: Not pressed yet")
                                
                                # Button-Status prüfen
                                btn_str = str(btn_response).lower()
                                button_pressed = ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)
                                
                                if button_pressed:
                                    # Button pressed, 100 steps up and exit
                                    log(f"Button pressed detected on attempt {attempt}")
                                    params = {"steps": 100, "direction": 1, "speed": int(stepper_speed.get())}
                                    make_api_request("setMotor", params, base_url)
                                    pos_cm = position.get() + (100 / 4096 * 3.141592653589793 * d / 10)
                                    distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
                                    log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                                    break
                                else:
                                    # Button not pressed, another 100 steps down
                                    params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
                                    make_api_request("setMotor", params, base_url)
                                    pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
                                    distance_cm = (100 / 4096 * 3.141592653589793 * d / 10)
                                    log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                                    
                                    # Verzögerung nach jedem Schritt
                                    time.sleep(0.5)
                            
                            # Nur bei Bedarf warnen
                            if not button_pressed:
                                log("Warning: Maximum attempts reached without detecting button press.")
                                
                            # Position auf 0 setzen
                            position.set(0)
                            root.after(0, update_position_label)
                            log("Home function completed, position set to 0.")
                            
                            # Reset total_distance
                            total_distance = 0
                            root.after(0, lambda: (
                                stepper_length_cm.delete(0, tk.END),
                                stepper_length_cm.insert(0, "0.00")
                            ))
                        except Exception as e:
                            log(f"Error in home function: {e}")
                        
                    # Kleine Verzögerung zwischen den Operationen
                    time.sleep(0.5)
                    
                except Exception as e:
                    log(f"Error executing operation {idx+1}: {e}")
            
            log("Queue execution completed!")
        
        # Run in a separate thread to keep UI responsive
        threading.Thread(target=run_queue).start()
    
    # Function to clear the queue
    def clear_queue():
        operation_queue.clear()
        update_queue_display()
        log("Operation queue cleared")
    
    # Queue control buttons
    tk.Button(queue_buttons_frame, text="Execute Queue", command=execute_queue, 
             bg="#77dd77", fg="black", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(queue_buttons_frame, text="Clear Queue", command=clear_queue,
             bg="#ff6961", fg="black").pack(side=tk.LEFT, padx=5)
    tk.Button(queue_buttons_frame, text="Remove Selected", 
             command=lambda: remove_selected_operation(queue_list.curselection())).pack(side=tk.LEFT, padx=5)
    
    # Function to remove selected operation
    def remove_selected_operation(selection):
        if not selection:
            log("No operation selected for removal")
            return
        
        idx = selection[0]
        if 0 <= idx < len(operation_queue):
            removed = operation_queue.pop(idx)
            update_queue_display()
            log(f"Removed from queue: {removed['description']}")

    root.mainloop()

if __name__ == "__main__":
    main()