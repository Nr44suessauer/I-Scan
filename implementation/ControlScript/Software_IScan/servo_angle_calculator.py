"""
Servo-Winkel-Rechner-Modul
Berechnet den erforderlichen Servo-Winkel basierend auf der aktuellen Y-Position
im Koordinatensystem für den I-Scan-Aufbau.
"""
import math

class ServoAngleCalculator:
    """
    Berechnet Servo-Winkel basierend auf der aktuellen Position im Koordinatensystem.
    
    Koordinatensystem-Definition:
    - Bei Servo-Position 90° ist der Servo parallel zur X-Achse
    - Bei Servo-Position 0° zeigt der Servo von Y-Max nach Y-Min (0/0)
    - Das Zentrum des Koordinatensystems ist bei (0, 0)
    """
    
    def __init__(self, target_center_x=150, target_center_y=75, z_module_x=0):
        """
        Initialisiert den Servo-Winkel-Rechner.
        
        Args:
            target_center_x (float): X-Koordinate des Zielzentrums (Standard: 150)
            target_center_y (float): Y-Koordinate des Zielzentrums (Standard: 75)
            z_module_x (float): X-Koordinate des Z-Moduls (Standard: 0)
        """
        self.target_center_x = target_center_x
        self.target_center_y = target_center_y
        self.z_module_x = z_module_x
    
    def calculate_servo_angle_from_position(self, current_y_position):
        """
        Berechnet den erforderlichen Servo-Winkel basierend auf der aktuellen Y-Position.
        
        Args:
            current_y_position (float): Aktuelle Y-Position des Z-Moduls
            
        Returns:
            int: Servo-Winkel in Grad (0-90°)
        """
        # Abstand zwischen Zielzentrum und Z-Modul in X-Richtung
        dx = self.target_center_x - self.z_module_x
        
        # Abstand zwischen Zielzentrum und aktueller Y-Position
        dy = self.target_center_y - current_y_position
        
        # Winkel in Radiant berechnen (atan2 berücksichtigt Vorzeichen korrekt)
        alpha_rad = math.atan2(dy, dx)
          # In Grad umwandeln
        alpha_degrees = alpha_rad * 180 / math.pi
        
        # Servo-Winkel-Berechnung für physische Grenzen (0-90°)
        # Servo 90° = parallel zur X-Achse (horizontal)
        # Servo 0° = parallel zur Y-Achse (vertikal)
        
        # Berechne den Winkel zur Horizontalen (X-Achse)
        angle_to_horizontal = 90 - alpha_degrees
        
        # Korrigiere für die Servo-Ausrichtung und begrenzen auf 0-90°
        if angle_to_horizontal < 0:
            # Wenn der berechnete Winkel negativ ist, verwende 0° (vertikal)
            servo_angle = 0
        elif angle_to_horizontal > 90:
            # Wenn der berechnete Winkel > 90° ist, verwende 90° (horizontal)
            servo_angle = 90
        else:
            # Normaler Bereich: verwende den berechneten Winkel
            servo_angle = abs(angle_to_horizontal)
        
        return int(round(servo_angle))
    
    def calculate_targeting_angle(self, current_y_position):
        """
        Berechnet den direkten Zielwinkel vom Z-Modul zum Zielzentrum.
        
        Args:
            current_y_position (float): Aktuelle Y-Position des Z-Moduls
            
        Returns:
            tuple: (winkel_in_grad, servo_winkel)
        """
        # Abstand zwischen Zielzentrum und Z-Modul
        dx = self.target_center_x - self.z_module_x
        dy = self.target_center_y - current_y_position
        
        # Direkter Winkel zum Ziel
        angle_to_target = math.atan2(dy, dx) * 180 / math.pi
        
        # Servo-Winkel berechnen
        servo_angle = self.calculate_servo_angle_from_position(current_y_position)
        
        return angle_to_target, servo_angle
    
    def get_angle_info(self, current_y_position):
        """
        Gibt detaillierte Informationen über die Winkelberechnung zurück.
        
        Args:
            current_y_position (float): Aktuelle Y-Position des Z-Moduls
            
        Returns:
            dict: Detaillierte Winkel-Informationen
        """
        dx = self.target_center_x - self.z_module_x
        dy = self.target_center_y - current_y_position
        
        angle_to_target = math.atan2(dy, dx) * 180 / math.pi
        servo_angle = self.calculate_servo_angle_from_position(current_y_position)
        
        # Zusätzliche Berechnungen für Debug-Informationen
        angle_to_horizontal = 90 - angle_to_target
        is_servo_limited = angle_to_horizontal < 0 or angle_to_horizontal > 90
        
        return {
            'current_y': current_y_position,
            'target_center': (self.target_center_x, self.target_center_y),
            'z_module_position': (self.z_module_x, current_y_position),
            'dx': dx,
            'dy': dy,
            'angle_to_target_deg': angle_to_target,
            'angle_to_horizontal': angle_to_horizontal,
            'servo_angle_deg': servo_angle,
            'servo_limited': is_servo_limited,
            'servo_limit_reason': 'Too low' if angle_to_horizontal < 0 else 'Too high' if angle_to_horizontal > 90 else 'Within range',
            'distance_to_target': math.sqrt(dx*dx + dy*dy)
        }
    
    def update_target_center(self, new_x, new_y):
        """
        Aktualisiert die Zielzentrum-Koordinaten.
        
        Args:
            new_x (float): Neue X-Koordinate des Zielzentrums
            new_y (float): Neue Y-Koordinate des Zielzentrums
        """
        self.target_center_x = new_x
        self.target_center_y = new_y
    
    def validate_servo_angle(self, angle):
        """
        Überprüft, ob der Servo-Winkel im gültigen Bereich liegt.
        
        Args:
            angle (int): Zu überprüfender Winkel
            
        Returns:
            bool: True wenn gültig, False sonst
        """
        return 0 <= angle <= 90
