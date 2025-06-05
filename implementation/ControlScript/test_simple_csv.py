#!/usr/bin/env python3
"""
Vereinfachter Test für CSV-Export im main.py-Format
"""

import csv
import json
import math

# Konfiguration für Test
NEW_CENTER_X = 40
NEW_CENTER_Y = 0
Z_MODULE_X = 0
P_Y = 0
NUMBER_OF_MEASUREMENTS = 5
DELTA_SCAN = 25

def calculate_angle(current_y):
    """Berechnet den Winkel basierend auf der aktuellen Y-Position"""
    dx = NEW_CENTER_X - Z_MODULE_X
    dy = abs(current_y - NEW_CENTER_Y)
    
    if abs(dx) < 0.001:
        angle = 90.0 if dy == 0 else 0.0
    else:
        alpha_rad = math.atan(dy / abs(dx))
        alpha_deg = alpha_rad * 180 / math.pi
        angle = 90.0 - alpha_deg
    
    return angle

def calculate_approximated_angle(current_y):
    """Berechnet approximierten Winkel mit Begrenzung auf 0-90°"""
    raw_angle = calculate_angle(current_y)
    return max(0, min(90, raw_angle))

def calculate_step_size():
    """Berechnet die Schrittgröße"""
    return DELTA_SCAN / NUMBER_OF_MEASUREMENTS if NUMBER_OF_MEASUREMENTS > 0 else 0

def test_csv_export():
    """Test der CSV-Export-Funktionalität"""
    print("=== CSV-Export Test ===")
    
    csv_filename = 'test_main_format.csv'
    step_size = calculate_step_size()
    
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['type', 'params', 'description'])
            
            # Home-Position
            writer.writerow(['home', '{}', 'Home-Position anfahren'])
            
            for i in range(NUMBER_OF_MEASUREMENTS):
                y = P_Y + step_size * i
                approx_angle = calculate_approximated_angle(y)
                
                # Servo setzen
                writer.writerow([
                    'servo',
                    json.dumps({"angle": int(approx_angle)}),
                    f"Servo: Winkel auf {int(approx_angle)}° setzen (Y={y:.1f}cm)"
                ])
                
                # Photo
                writer.writerow([
                    'photo',
                    '{}',
                    f"Kamera: Foto aufnehmen bei Y={y:.1f}cm, Winkel={int(approx_angle)}°"
                ])
                
                # Stepper (außer letzter Punkt)
                if i < NUMBER_OF_MEASUREMENTS - 1:
                    d = 28.0  # mm
                    circumference = 3.141592653589793 * d
                    step_mm = step_size * 10
                    steps = int((step_mm / circumference) * 4096)
                    
                    writer.writerow([
                        'stepper',
                        json.dumps({"steps": steps, "direction": 1, "speed": 80}),
                        f"Stepper: {steps} Schritte, {step_size:.1f}cm, Richtung aufwärts, Geschwindigkeit: 80"
                    ])
        
        print(f"✅ CSV-Datei erstellt: {csv_filename}")
        
        # Datei lesen und validieren
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                count += 1
                try:
                    params = json.loads(row['params'])
                    print(f"Zeile {count}: {row['type']} - {params}")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON-Fehler in Zeile {count}: {e}")
                    
        print(f"✅ Alle {count} Zeilen erfolgreich validiert!")
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    test_csv_export()
