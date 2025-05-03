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
    
    # Function to update the display
    def update_position_label():
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
    position_label = tk.Label(pos_frame, textvariable=position, font=("Arial", 14, "bold"), 
                             fg="blue", width=6, anchor='e')  # Fixed width for stable display
    position_label.pack(side=tk.LEFT)
    tk.Label(pos_frame, text="cm", font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT)
    tk.Label(pos_frame, text="   Servo Angle:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
    servo_angle_label = tk.Label(pos_frame, textvariable=servo_angle_var, font=("Arial", 14, "bold"), 
                                fg="green", width=3, anchor='e')  # Fixed width for stable display
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
        # Stepper log as before
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
    tk.Button(servo_frame, text="Execute Servo", command=servo_cmd).pack(side=tk.LEFT, padx=5)

    # Stepper
    stepper_frame = tk.LabelFrame(root, text="Control Stepper")
    stepper_frame.pack(fill="x", padx=10, pady=2)
    tk.Label(stepper_frame, text="Distance (cm):").pack(side=tk.LEFT)
    stepper_length_cm = tk.Entry(stepper_frame, width=8)
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
            
            # Simplified log output for move_stepper
            pos_cm = position.get() + (length_cm if direction == 1 else -length_cm)
            log(f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
            
            # Update position in GUI
            position.set(pos_cm)
            update_position_label()
        except Exception as e:
            log(f"Error: {e}")
    tk.Button(stepper_frame, text="Execute Stepper", command=stepper_cmd).pack(side=tk.LEFT, padx=5)

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
    tk.Button(led_frame, text="Execute LED", command=led_cmd).pack(side=tk.LEFT, padx=5)

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
    tk.Button(bright_frame, text="Execute Brightness", command=bright_cmd).pack(side=tk.LEFT, padx=5)

    # Button Status
    btn_frame = tk.LabelFrame(root, text="Query Button Status")
    btn_frame.pack(fill="x", padx=10, pady=2)
    def button_cmd():
        res = get_button_state(base_url_var.get())
        log(res)
    tk.Button(btn_frame, text="Query Button", command=button_cmd).pack(side=tk.LEFT, padx=5)

    # --- Home Function ---
    def home_func():
        try:
            d = float(diameter_entry.get())
            base_url = base_url_var.get()
            log('Starting Home function...')
            
            # Initial 100 steps in direction -1
            params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
            response = make_api_request("setMotor", params, base_url)
            pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
            log(f"Motor: 100 Steps, {(100 / 4096 * 3.141592653589793 * d / 10):.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
            position.set(pos_cm)
            update_position_label()
            
            # Loop until button is pressed
            while True:
                # Query button
                btn_response = make_api_request("getButtonState", base_url=base_url)
                is_pressed = 'True' in str(btn_response) or '1' in str(btn_response)
                log(f"Button: Pressed: {is_pressed}")
                
                if is_pressed:
                    # Button pressed, 100 steps up and exit
                    params = {"steps": 100, "direction": 1, "speed": int(stepper_speed.get())}
                    response = make_api_request("setMotor", params, base_url)
                    pos_cm = position.get() + (100 / 4096 * 3.141592653589793 * d / 10)
                    log(f"Motor: 100 Steps, {(100 / 4096 * 3.141592653589793 * d / 10):.2f} cm, Direction up, Position: {pos_cm:.2f} cm")
                    position.set(pos_cm)
                    update_position_label()
                    break
                else:
                    # Button not pressed, another 100 steps down
                    params = {"steps": 100, "direction": -1, "speed": int(stepper_speed.get())}
                    response = make_api_request("setMotor", params, base_url)
                    pos_cm = position.get() - (100 / 4096 * 3.141592653589793 * d / 10)
                    log(f"Motor: 100 Steps, {(100 / 4096 * 3.141592653589793 * d / 10):.2f} cm, Direction down, Position: {pos_cm:.2f} cm")
                    position.set(pos_cm)
                    update_position_label()
                    
            # Set position to 0
            position.set(0)
            update_position_label()
            log("Home function completed, position set to 0.")
        except Exception as e:
            log(f"Error: {e}")

    home_frame = tk.LabelFrame(root, text="Home Function")
    home_frame.pack(fill="x", padx=10, pady=2)
    tk.Button(home_frame, text="Execute Home", command=lambda: threading.Thread(target=home_func).start()).pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()