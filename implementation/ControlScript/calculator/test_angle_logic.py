import math

# Konfigurationswerte aus calculator_simplified.py
NEW_CENTER_X = 40
NEW_CENTER_Y = 0
Z_MODULE_X = 0

def calculate_angle_test(current_y):
    """
    Test der Winkelberechnung
    """
    dx = NEW_CENTER_X - Z_MODULE_X  # = 40 - 0 = 40
    dy = abs(current_y - NEW_CENTER_Y)  # = abs(current_y - 0) = abs(current_y)
    
    print(f"Y={current_y}: dx={dx}, dy={dy}")
    
    if abs(dx) < 0.001:
        angle = 90.0 if dy == 0 else 0.0
    else:
        alpha = math.atan(dy / abs(dx))
        angle = alpha * 180 / math.pi
    
    print(f"  -> Winkel: {angle:.1f}°")
    return angle

print("=== Test der korrigierten Winkelberechnung ===")
print("Erwartung: Bei Y=0 sollte der Winkel 90° sein, bei steigenden Y-Werten sollte er sich 0° nähern")
print()

# Test verschiedener Y-Werte
test_values = [0, 5, 10, 20, 40, 80]
for y in test_values:
    calculate_angle_test(y)
    print()
