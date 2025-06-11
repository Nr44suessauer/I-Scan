#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Target Coordinate Angle Debug - Einfache Version ohne Unicode
"""

import math
from config import TARGET_CENTER_X, TARGET_CENTER_Y, SCANNER_MODULE_X
from calculations import calculate_geometric_angles

def debug_target_coord_angle():
    """Debug Target Coordinate Angle Berechnung"""
    
    print("TARGET COORDINATE ANGLE BERECHNUNG")
    print("=" * 50)
    print("")
    
    print("KOORDINATENSYSTEM:")
    print("0 Grad = +X-Achse (rechts)")
    print("90 Grad = +Y-Achse (oben)")  
    print("180 Grad = -X-Achse (links)")
    print("270 Grad = -Y-Achse (unten)")
    print("")
    
    print("VARIABLEN:")
    print(f"TARGET_CENTER_X = {TARGET_CENTER_X} cm")
    print(f"TARGET_CENTER_Y = {TARGET_CENTER_Y} cm")
    print(f"SCANNER_MODULE_X = {SCANNER_MODULE_X} cm")
    print("")
    
    print("FORMEL:")
    print("1. dx = TARGET_CENTER_X - SCANNER_MODULE_X")
    print("2. dy = TARGET_CENTER_Y - scanner_y")
    print("3. target_coord_angle = atan2(dy, dx) * (180/pi)")
    print("4. Normalisierung auf -180 bis +180 Grad")
    print("")
    
    # Get measurement data
    geometric_angles = calculate_geometric_angles()
    
    print("BERECHNUNG FUER ALLE MESSPUNKTE:")
    print("-" * 50)
    
    for i, angle_data in enumerate(geometric_angles):
        scanner_y = angle_data['y_pos']
        
        print(f"")
        print(f"MESSPUNKT {i+1} (Scanner Y = {scanner_y} cm):")
        
        # Schritt 1: dx berechnen
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        print(f"  Schritt 1: dx = {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm")
        
        # Schritt 2: dy berechnen
        dy = TARGET_CENTER_Y - scanner_y
        print(f"  Schritt 2: dy = {TARGET_CENTER_Y} - {scanner_y} = {dy} cm")
        
        # Schritt 3: atan2 berechnen
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        print(f"  Schritt 3: atan2({dy}, {dx}) = {angle_rad:.4f} rad = {angle_deg:.2f} Grad")
        
        # Schritt 4: Normalisierung
        normalized_angle = angle_deg
        while normalized_angle > 180.0:
            normalized_angle -= 360.0
        while normalized_angle < -180.0:
            normalized_angle += 360.0
        
        if abs(normalized_angle - angle_deg) > 0.001:
            print(f"  Schritt 4: Normalisiert von {angle_deg:.2f} zu {normalized_angle:.2f} Grad")
        else:
            print(f"  Schritt 4: Bereits normalisiert: {normalized_angle:.2f} Grad")
        
        # Vektor-Richtung erklären
        if dx > 0 and dy > 0:
            quadrant = "1. Quadrant (rechts oben)"
        elif dx < 0 and dy > 0:
            quadrant = "2. Quadrant (links oben)"
        elif dx < 0 and dy < 0:
            quadrant = "3. Quadrant (links unten)"
        else:
            quadrant = "4. Quadrant (rechts unten)"
        
        print(f"  Ergebnis: Vektor zeigt in {quadrant}")
        print(f"  Target Coordinate Angle: {normalized_angle:.2f} Grad")
    
    print("")
    print("WICHTIGE ERKENNTNISSE:")
    print("- dx ist immer 50 cm (konstant)")
    print("- dy aendert sich je nach Scanner-Position")
    print("- atan2 beruecksichtigt die Vorzeichen von dx und dy")
    print("- Das ergibt den korrekten Quadranten")
    print("- Alle Winkel liegen zwischen -180 und +180 Grad")
    print("")

if __name__ == "__main__":
    debug_target_coord_angle()
