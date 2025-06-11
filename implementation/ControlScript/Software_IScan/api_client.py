"""
API-Client-Modul
Verwaltet die HTTP-Requests an die API-Endpunkte

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""
import requests
import time


class ApiClient:
    """
    Klasse für die API-Kommunikation
    Verarbeitet alle HTTP-Anfragen an die API-Endpunkte und bietet
    Methoden zur Steuerung verschiedener Hardware-Komponenten.
    """
    
    @staticmethod
    def make_request(endpoint, params=None, base_url=None, timeout=30):
        """
        Sendet eine HTTP-Anfrage an den angegebenen API-Endpunkt
        
        Args:
            endpoint (str): Der API-Endpunkt (ohne den base_url)
            params (dict, optional): Die zu sendenden Parameter
            base_url (str): Die Basis-URL der API
            timeout (int): Timeout-Zeit in Sekunden
            
        Returns:
            Die Antwort von der API oder eine Fehlermeldung
        """
        url = f"{base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Fehler bei API-Anfrage: {str(e)}"
    
    @staticmethod
    def set_servo_angle(angle, base_url):
        """
        Setzt den Servo-Winkel über die API
        
        Args:
            angle (int): Der zu setzende Winkel (0-90 Grad)
            base_url (str): Die Basis-URL der API
            
        Returns:
            str: Antwortnachricht mit dem Ergebnis der Operation
        """
        if not 0 <= angle <= 90:
            return "Ungültiger Winkel. Der Winkel muss zwischen 0 und 90 liegen."
        
        params = {"angle": angle}
        response = ApiClient.make_request("setServo", params, base_url)
        return f"Servo auf {angle} Grad gesetzt. Antwort: {response}"
    
    @staticmethod
    def move_stepper(steps, direction, speed, base_url):
        """
        Steuert den Schrittmotor über die API
        
        Args:
            steps (int): Die Anzahl der Schritte
            direction (int): Die Richtung (1 für aufwärts, -1 für abwärts)
            speed (int, optional): Die Geschwindigkeit der Bewegung
            base_url (str): Die Basis-URL der API
            
        Returns:
            str: Antwortnachricht mit dem Ergebnis der Operation
        """
        if steps < 0:
            return "Ungültige Schrittzahl. Die Schrittzahl muss positiv sein."
        
        if direction not in [1, -1]:
            return "Ungültige Richtung. Richtung muss 1 (aufwärts) oder -1 (abwärts) sein."
        
        params = {"steps": steps, "direction": direction}
        if speed is not None:
            params["speed"] = speed
        
        response = ApiClient.make_request("setMotor", params, base_url)
        dir_text = "aufwärts" if direction == 1 else "abwärts"
        speed_text = f" mit Geschwindigkeit {speed}" if speed is not None else ""
        return f"Schrittmotor bewegt sich {steps} Schritte {dir_text}{speed_text}. Antwort: {response}"
    
    @staticmethod
    def set_led_color(color_hex, base_url):
        """
        Setzt die LED-Farbe über die API
        
        Args:
            color_hex (str): Der hexadezimale Farbcode (z.B. "#FF0000")
            base_url (str): Die Basis-URL der API
            
        Returns:
            str: Antwortnachricht mit dem Ergebnis der Operation
        """
        if not color_hex.startswith("#"):
            color_hex = "#" + color_hex
        
        params = {"hex": color_hex}
        response = ApiClient.make_request("hexcolor", params, base_url)
        return f"LED-Farbe auf {color_hex} gesetzt. Antwort: {response}"
    
    @staticmethod
    def set_led_brightness(brightness, base_url):
        """
        Setzt die LED-Helligkeit über die API
        
        Args:
            brightness (int): Die Helligkeitsstufe (0-100 Prozent)
            base_url (str): Die Basis-URL der API
            
        Returns:
            str: Antwortnachricht mit dem Ergebnis der Operation
        """
        if not 0 <= brightness <= 100:
            return "Ungültige Helligkeit. Die Helligkeit muss zwischen 0 und 100 liegen."
        
        params = {"value": brightness}
        response = ApiClient.make_request("setBrightness", params, base_url)
        return f"LED-Helligkeit auf {brightness}% gesetzt. Antwort: {response}"
    
    @staticmethod
    def get_button_state(base_url, nocache=False):
        """
        Fragt den Button-Status über die API ab
        
        Args:
            base_url (str): Die Basis-URL der API
            nocache (bool): Falls True, wird ein Zeitstempel hinzugefügt, um Caching zu verhindern
            
        Returns:
            Die Button-Status-Antwort von der API
        """
        endpoint = "getButtonState"
        if nocache:
            endpoint = f"{endpoint}?nocache={int(time.time())}"
        
        response = ApiClient.make_request(endpoint, base_url=base_url)
        return response
    
    @staticmethod
    def is_button_pressed(response):
        """
        Prüft, ob der Button gedrückt ist, basierend auf der API-Antwort
        Verschiedene Antwortformate werden für die Kompatibilität unterstützt.
        
        Args:
            response: Die zu überprüfende API-Antwort
            
        Returns:
            bool: True, wenn der Button gedrückt ist, sonst False
        """
        btn_str = str(response).lower()
        return ('true' in btn_str) or ('1' in btn_str) or ('"pressed": true' in btn_str)
