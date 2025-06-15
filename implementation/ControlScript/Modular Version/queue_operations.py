"""
Queue Operations for I-Scan Application
All queue-related operations in one place.
"""

from config import *


class QueueOperations:
    """Handles all queue operations"""
    
    def __init__(self, app_instance):
        """Initialize with reference to main app instance"""
        self.app = app_instance
    
    def add_servo_to_queue(self):
        """Add servo operation to queue"""
        try:
            angle = int(self.app.servo_angle.get())
            description = f"Servo: Winkel auf {angle}° setzen"
            self.app.operation_queue.add('servo', {'angle': angle}, description)
        except Exception as e:
            self.app.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_stepper_to_queue(self):
        """Add stepper motor operation to queue"""
        try:
            d = float(self.app.diameter_entry.get())
            circumference = PI * d
            length_cm = float(self.app.stepper_length_cm.get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.app.stepper_dir.get()) if self.app.stepper_dir.get() else 1
            speed = int(self.app.stepper_speed.get()) if self.app.stepper_speed.get() else int(DEFAULT_SPEED)
            
            dir_text = "aufwärts" if direction == 1 else "abwärts"
            params = {"steps": steps, "direction": direction, "speed": speed}
            description = f"Stepper: {steps} Schritte, {length_cm} cm, Richtung {dir_text}, Geschwindigkeit: {speed}"
            self.app.operation_queue.add('stepper', params, description)
        except Exception as e:
            self.app.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_led_color_to_queue(self):
        """Add LED color operation to queue"""
        try:
            color_hex = self.app.led_color.get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
            description = f"LED: Farbe auf {color_hex} setzen"
            self.app.operation_queue.add('led_color', {'color': color_hex}, description)
        except Exception as e:
            self.app.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_brightness_to_queue(self):
        """Add LED brightness operation to queue"""
        try:
            val = int(self.app.led_bright.get())
            description = f"LED: Helligkeit auf {val}% setzen"
            self.app.operation_queue.add('led_brightness', {'brightness': val}, description)
        except Exception as e:
            self.app.logger.log(f"Fehler beim Hinzufügen zur Warteschlange: {e}")
    
    def add_button_to_queue(self):
        """Add button status query to queue"""
        description = "Button: Button-Status abfragen"
        self.app.operation_queue.add('button', {}, description)
    
    def add_home_to_queue(self):
        """Add home function to queue"""
        description = "Home: Home-Funktion ausführen"
        self.app.operation_queue.add('home', {}, description)
    
    def add_photo_to_queue(self):
        """Add photo taking operation to queue with selected camera index"""
        delay = self.app.global_delay
        
        # Get selected camera index from photo combo box
        camera_index = 0  # Default camera
        if hasattr(self.app, 'photo_camera_combo') and self.app.photo_camera_combo:
            try:
                selected_camera = self.app.photo_camera_combo.get()
                if selected_camera:
                    camera_index = int(selected_camera)
            except ValueError:
                pass  # Use default if conversion fails
                
        description = f"Kamera {camera_index}: Foto aufnehmen (Delay: {delay}s)"
        self.app.operation_queue.add('photo', {'delay': delay, 'camera_index': camera_index}, description)
