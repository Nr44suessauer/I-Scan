#!/usr/bin/env python3
"""
Test der verbesserten Servo-Winkel-Berechnung
Zeigt die Servo-Winkel für verschiedene Y-Positionen mit physischen Grenzen (0-90°)
"""

from servo_angle_calculator import ServoAngleCalculator

def test_servo_calculations():
    """Test die Servo-Berechnungen für verschiedene Y-Positionen"""
    
    # Konfiguration wie in calculator_angle_table.py
    servo_calculator = ServoAngleCalculator(
        target_center_x=150,
        target_center_y=75,
        z_module_x=0
    )
    
    print("=== Servo-Winkel Test (Physische Grenzen: 0-90°) ===")
    print("Servo 90° = parallel zur X-Achse (horizontal)")
    print("Servo 0° = parallel zur Y-Achse (vertikal)")
    print("=" * 70)
    
    # Test Y-Positionen von 0 bis 150 (wie in der Tabelle)
    test_positions = [i * 15 for i in range(11)]  # 0, 15, 30, ..., 150
    
    print(f"{'Y-Pos':<6} {'Ziel-Winkel':<12} {'Servo-Winkel':<12} {'Status':<15} {'Begrenzung'}")
    print("-" * 70)
    
    for y_pos in test_positions:
        angle_info = servo_calculator.get_angle_info(y_pos)
        
        status = "✓ Normal" if not angle_info['servo_limited'] else "⚠ Begrenzt"
        
        print(f"{y_pos:<6} {angle_info['angle_to_target_deg']:<12.1f} "
              f"{angle_info['servo_angle_deg']:<12} {status:<15} "
              f"{angle_info['servo_limit_reason']}")
    
    print("\n=== Grenzfall-Analyse ===")
    
    # Finde kritische Y-Positionen
    critical_positions = []
    for y in range(0, 151, 1):  # Teste jede Y-Position
        info = servo_calculator.get_angle_info(y)
        if info['servo_limited']:
            critical_positions.append((y, info))
    
    if critical_positions:
        print(f"Kritische Y-Positionen gefunden: {len(critical_positions)}")
        print(f"Erste kritische Position: Y={critical_positions[0][0]}")
        print(f"Letzte kritische Position: Y={critical_positions[-1][0]}")
    else:
        print("Keine kritischen Positionen im Bereich Y=0-150 gefunden.")
    
    print("\n=== Empfohlener Scan-Bereich ===")
    valid_range = []
    for y in range(0, 151, 1):
        info = servo_calculator.get_angle_info(y)
        if not info['servo_limited']:
            valid_range.append(y)
    
    if valid_range:
        print(f"Optimaler Y-Bereich: {min(valid_range)} - {max(valid_range)} cm")
        print(f"Verfügbare Länge: {max(valid_range) - min(valid_range)} cm")
    else:
        print("Warnung: Kein gültiger Bereich gefunden!")

if __name__ == "__main__":
    test_servo_calculations()
