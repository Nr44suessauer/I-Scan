"""
Gerätesteuerungs-Modul
Bietet Klassen und Methoden zur Steuerung verschiedener Hardware-Geräte
"""
from api_client import ApiClient

# Konstante für Berechnungen
PI = 3.141592653589793

class DeviceControl:
    """
    Klasse zur Steuerung verschiedener Hardware-Geräte
    Bietet Methoden zur Steuerung von Servomotoren, Schrittmotoren, LEDs und
    zur Abfrage von Button-Zuständen über die API.
    """
    
    def __init__(self, logger, base_url_var, widgets, position_var, servo_angle_var):
        """
        Initialisiert den Gerätecontroller
        
        Args:
            logger: Die Logger-Instanz für die Protokollierung von Operationen
            base_url_var: Die StringVar mit der Basis-URL der API
            widgets: Wörterbuch der für Operationen benötigten UI-Widgets
            position_var: Die DoubleVar zur Verfolgung der aktuellen Position
            servo_angle_var: Die IntVar zur Verfolgung des aktuellen Servo-Winkels
        """
        self.logger = logger
        self.base_url_var = base_url_var
        self.widgets = widgets
        self.position = position_var
        self.servo_angle_var = servo_angle_var
        
    def servo_cmd(self):
        """
        Führt Servo-Befehl direkt aus
        """
        try:
            angle = int(self.widgets['servo_angle'].get())
            base_url = self.base_url_var.get()
            ApiClient.set_servo_angle(angle, base_url)
            self.logger.log(f"Servo: Angle {angle}°")
            self.servo_angle_var.set(angle)
            self.widgets['update_position_label']()
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
            
    def stepper_cmd(self):
        """
        Führt Schrittmotor-Befehl direkt aus
        """
        try:
            d = float(self.widgets['diameter_entry'].get())
            circumference = PI * d  # mm
            length_cm = float(self.widgets['stepper_length_cm'].get())
            length_mm = length_cm * 10
            steps = int((length_mm / circumference) * 4096)
            direction = int(self.widgets['stepper_dir'].get()) if self.widgets['stepper_dir'].get() else 1
            speed = int(self.widgets['stepper_speed'].get()) if self.widgets['stepper_speed'].get() else None
            dir_text = "aufwärts" if direction == 1 else "abwärts"
            base_url = self.base_url_var.get()
            
            ApiClient.move_stepper(steps, direction, speed, base_url)
            pos_cm = self.position.get() + (length_cm if direction == 1 else -length_cm)
            self.logger.log(f"Motor: {steps} Steps, {length_cm} cm, Direction {dir_text}, Position: {pos_cm:.2f} cm")
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
            
    def led_cmd(self):
        """
        Setzt LED-Farbe direkt
        """
        try:
            color_hex = self.widgets['led_color'].get()
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
            base_url = self.base_url_var.get()
            
            ApiClient.set_led_color(color_hex, base_url)
            self.logger.log(f"LED: Farbe {color_hex}")
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
            
    def bright_cmd(self):
        """
        Setzt LED-Helligkeit direkt
        """
        try:
            val = int(self.widgets['led_bright'].get())
            base_url = self.base_url_var.get()
            
            ApiClient.set_led_brightness(val, base_url)
            self.logger.log(f"LED: Helligkeit {val}%")
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
            
    def button_cmd(self):
        """
        Fragt Button-Status direkt ab
        """
        base_url = self.base_url_var.get()
        response = ApiClient.get_button_state(base_url)
        self.logger.log(f"Button-Status: {response}")
            
    def home_func(self):
        """
        Führt die Home-Funktion aus
        """
        try:
            base_url = self.base_url_var.get()
            self._home_logic(base_url)
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
            
    def _home_logic(self, base_url):
        """
        Implementiert die Home-Funktion-Logik
        Bewegt den Schrittmotor nach unten, bis der Button gedrückt wird,
        dann leicht nach oben und setzt die Position auf Null zurück.
        
        Args:
            base_url (str): Die Basis-URL der API
        """
        try:
            d = float(self.widgets['diameter_entry'].get())
            self.logger.log("Starte Home-Funktion...")
            
            # Erste Überprüfung des Button-Status
            self.logger.log("Überprüfe anfänglichen Button-Status...")
            btn_response = ApiClient.get_button_state(base_url, nocache=True)
            button_pressed = ApiClient.is_button_pressed(btn_response)
            
            if button_pressed:
                self.logger.log("Button ist bereits gedrückt. Warte auf Freigabe...")
                reset_attempts = 0
                max_reset_attempts = 10
                
                while reset_attempts < max_reset_attempts:
                    reset_attempts += 1
                    
                    # Kleine Pause, um auf Button-Freigabe zu warten
                    import time
                    time.sleep(1)
                    
                    btn_response = ApiClient.get_button_state(base_url, nocache=True)
                    button_still_pressed = ApiClient.is_button_pressed(btn_response)
                    
                    if button_still_pressed:
                        self.logger.log(f"Button noch immer gedrückt, warte auf Freigabe (Versuch {reset_attempts})...")
                    else:
                        self.logger.log("Button freigegeben, fahre mit Home-Funktion fort.")
                        break
                        
                if reset_attempts >= max_reset_attempts:
                    self.logger.log("Warnung: Button noch immer gedrückt nach maximalen Versuchen. Bitte Hardware überprüfen.")
                    return
            else:
                self.logger.log("Button ist nicht gedrückt. Fahre mit Home-Funktion fort.")
            
            # Kleine Pause vor dem Beginn
            import time
            time.sleep(1)
            
            # Anfängliche Schritte nach unten
            speed = int(self.widgets['stepper_speed'].get())
            params = {"steps": 100, "direction": -1, "speed": speed}
            ApiClient.make_request("setMotor", params, base_url)
            pos_cm = self.position.get() - (100 / 4096 * PI * d / 10)
            distance_cm = (100 / 4096 * PI * d / 10)
            self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction abwärts, Position: {pos_cm:.2f} cm")
            
            # Hauptschleife: Fahre nach unten, bis der Button gedrückt wird
            max_attempts = 100
            attempt = 0
            button_pressed = False
            
            while not button_pressed and attempt < max_attempts:
                attempt += 1
                
                # Button-Status abfragen
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                
                # Seltener protokollieren - nur alle 5 Versuche
                if attempt % 5 == 0:
                    self.logger.log(f"Button-Überprüfungsversuch {attempt}: Antwort: {btn_response}")
                
                button_pressed = ApiClient.is_button_pressed(btn_response)
                
                if button_pressed:
                    self.logger.log(f"Button-Druck bei Versuch {attempt} erkannt, fahre nach oben und beende Home")
                    params = {"steps": 100, "direction": 1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = self.position.get() + (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction aufwärts, Position: {pos_cm:.2f} cm")
                    break
                else:
                    params = {"steps": 100, "direction": -1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = self.position.get() - (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction abwärts, Position: {pos_cm:.2f} cm")
                    
                    # Kleine Pause nach jeder Bewegung
                    time.sleep(0.5)
                    
                    # Prüfen, ob der Button nach der Bewegung gedrückt wurde
                    btn_response = ApiClient.get_button_state(base_url, nocache=True)
                    if ApiClient.is_button_pressed(btn_response):
                        self.logger.log(f"Button-Druck nach Bewegung erkannt, fahre fort mit Abschluss")
                        params = {"steps": 100, "direction": 1, "speed": speed}
                        ApiClient.make_request("setMotor", params, base_url)
                        pos_cm = self.position.get() + (100 / 4096 * PI * d / 10)
                        distance_cm = (100 / 4096 * PI * d / 10)
                        self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction aufwärts, Position: {pos_cm:.2f} cm")
                        break
            
            if not button_pressed:
                self.logger.log("Warnung: Maximale Versuche in der Home-Funktion erreicht, ohne Button-Druck zu erkennen.")
            
            # Position auf 0 setzen
            self.position.set(0)
            self.widgets['update_position_label']()
            self.logger.log("Home-Funktion abgeschlossen, Position auf 0 gesetzt.")
            
            # Distanzanzeige zurücksetzen
            self.widgets['stepper_length_cm'].delete(0, 'end')
            self.widgets['stepper_length_cm'].insert(0, "0.00")
        except Exception as e:
            self.logger.log(f"Fehler: {e}")
