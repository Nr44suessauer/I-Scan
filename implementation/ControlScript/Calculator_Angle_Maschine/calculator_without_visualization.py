import math
import csv
import json
import os
from tabulate import tabulate

# ===== CONFIGURATION VARIABLES =====

# Servo angle limits (servo motor constraints)
SERVO_ANGLE_MIN = 0       # Lower limit of servo angle in degrees
SERVO_ANGLE_MAX = 90      # Upper limit of servo angle in degrees

# Angle correction reference (mechanical calibration)
ANGLE_CORRECTION_REFERENCE = 70  # Real servo angle when theoretical angle is 90°

# Point P (start coordinates)
P_X = 0                   # X-coordinate of start point
P_Y = 0                   # Y-coordinate of start point

# Point M (end coordinates)
M_X = 0                   # X-coordinate of end point
M_Y = 50                  # Y-coordinate of end point

# New center (target center)
NEW_CENTER_X = 50         # X-coordinate of new center
NEW_CENTER_Y = 0          # Y-coordinate of new center

# Old center (original center)
OLD_CENTER_X = 40         # X-coordinate of old center
OLD_CENTER_Y = 0          # Y-coordinate of old center

# Z-module position (start position)
Z_MODULE_X = 0            # X-coordinate of Z-module (remains fixed)
Z_MODULE_Y = 0            # Y-coordinate of Z-module (start position)

# Scan configuration
DELTA_SCAN = 70           # Total scan distance in cm
NUMBER_OF_MEASUREMENTS = 4  # Number of measurement points

def calculate_angle(current_y):
    """
    Calculates the angle based on the current Y position
    Geometry: At Y=0 the angle is 90°, with increasing Y position the angle approaches 0°
    """
    # Distance between new center and Z-module in X direction
    dx = NEW_CENTER_X - Z_MODULE_X
    # Distance between current Y position and new center
    dy = abs(current_y - NEW_CENTER_Y)
    
    # Calculate angle in radians
    if abs(dx) < 0.001:
        # Avoid division by 0 - if dx = 0, it's a vertical angle
        angle = 90.0 if dy == 0 else 0.0
    else:
        # Calculate angle to X-axis
        alpha_rad = math.atan(dy / abs(dx))
        # Convert to degrees
        alpha_deg = alpha_rad * 180 / math.pi
        # The complementary angle gives us the desired orientation:
        # At Y=0 (dy=0) -> alpha_deg=0° -> angle = 90° - 0° = 90°
        # At large Y (dy large) -> alpha_deg approaches 90° -> angle approaches 0°
        angle = 90.0 - alpha_deg
    
    return angle

def calculate_approximated_angle(current_y):
    """
    Calculates the approximated angle based on the current Y position
    with limitation to the configurable servo angle range and mechanical correction
    """
    # Calculate original angle
    raw_angle = calculate_angle(current_y)
    
    # Apply mechanical correction
    # Correction = ANGLE_CORRECTION_REFERENCE - 90°
    # Real angle = Theoretical angle + Correction
    angle_correction = ANGLE_CORRECTION_REFERENCE - 90.0
    corrected_angle = raw_angle + angle_correction
    
    # Limit to configurable servo angle range
    if corrected_angle < SERVO_ANGLE_MIN:
        approximated_angle = SERVO_ANGLE_MIN
    elif corrected_angle > SERVO_ANGLE_MAX:
        approximated_angle = SERVO_ANGLE_MAX
    else:
        approximated_angle = corrected_angle
    
    return approximated_angle

def calculate_step_size():
    """Calculates the step size for measurements"""
    if NUMBER_OF_MEASUREMENTS > 0:
        return DELTA_SCAN / NUMBER_OF_MEASUREMENTS
    return 0

def explain_angle_correction():
    """
    Explains the angle correction calculation and displays correction values
    """
    angle_correction = ANGLE_CORRECTION_REFERENCE - 90.0
    
    print(f"\n=== Angle Correction Explanation ===")
    print(f"Problem: Servo mechanical misalignment")
    print(f"Reference: At theoretical 90°, servo is actually at {ANGLE_CORRECTION_REFERENCE}°")
    print(f"")
    print(f"Calculation:")
    print(f"  Correction = {ANGLE_CORRECTION_REFERENCE}° - 90° = {angle_correction:+.1f}°")
    print(f"  Real_Angle = Theoretical_Angle + ({angle_correction:+.1f}°)")
    print(f"")
    print(f"Examples:")
    test_angles = [90, 75, 60, 45, 30, 15, 0]
    for theoretical in test_angles:
        real = theoretical + angle_correction
        print(f"  Theoretical {theoretical:2.0f}° → Real {real:4.1f}°")
    print("=" * 50)

def generate_results_table():
    """
    Generates the results table with original and approximated angles
    Creates CSV file and displays results in command line
    """
    if NUMBER_OF_MEASUREMENTS <= 0:
        print("Error: Number of measurements must be greater than 0!")
        return None

    step_size = calculate_step_size()
      # Display configuration information
    print("\n=== Scan Calculator Configuration ===")
    print(f"Start coordinates (P): ({P_X}, {P_Y})")
    print(f"End coordinates (M): ({M_X}, {M_Y})")
    print(f"New center: ({NEW_CENTER_X}, {NEW_CENTER_Y})")
    print(f"Old center: ({OLD_CENTER_X}, {OLD_CENTER_Y})")
    print(f"Z-module start: ({Z_MODULE_X}, {Z_MODULE_Y})")
    print(f"Delta scan: {DELTA_SCAN}")
    print(f"Number of measurements: {NUMBER_OF_MEASUREMENTS}")
    print(f"Step size: {step_size:.2f} cm")
    print(f"Servo angle range: {SERVO_ANGLE_MIN}° - {SERVO_ANGLE_MAX}°")
    print(f"Angle correction reference: {ANGLE_CORRECTION_REFERENCE}° (offset: {ANGLE_CORRECTION_REFERENCE - 90.0:+.1f}°)")
    print("=" * 50)
      # Calculate and record measurements
    table_data = []
    
    for i in range(NUMBER_OF_MEASUREMENTS):
        # Calculate current Y position
        current_y = P_Y + step_size * i
        
        # Calculate all angle values for this position
        theoretical_angle = calculate_angle(current_y)
        corrected_angle = calculate_approximated_angle(current_y)
        
        # Format Z-module coordinates (X remains fixed, Y varies)
        z_coords = f"({Z_MODULE_X}, {round(current_y, 1)})"
        
        # Add data to table (showing theoretical vs corrected angle)
        table_data.append([
            i + 1,                              # Measurement number
            round(theoretical_angle, 1),        # Theoretical angle
            round(corrected_angle, 1),          # Corrected angle (with mechanical adjustment)
            z_coords                            # Z-module coordinates
        ])
    
    # Output table to command line
    print("\n=== Calculation Results ===")
    print(tabulate(table_data, 
                  headers=['Measurement No.', 'Theoretical Angle (°)', 'Corrected Angle (°)', 'Z-Module (Coordinates)'],
                  tablefmt='grid',
                  numalign='right'))
    
    # Create CSV file for main.py import (with JSON format for params)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scan_configs_dir = os.path.join(script_dir, 'ScanConfigs')
    
    # Create ScanConfigs directory if it doesn't exist
    if not os.path.exists(scan_configs_dir):
        os.makedirs(scan_configs_dir)
    
    csv_filename = os.path.join(scan_configs_dir, f'angle_table_{NEW_CENTER_X}x{NEW_CENTER_Y}_{NUMBER_OF_MEASUREMENTS}points_approximated.csv')
    
    # Prepare CSV content for display
    csv_content = []
    csv_content.append(['type', 'params', 'description'])
    
    # Move to home position
    csv_content.append([
        'home',
        '{}',
        'Move to home position'
    ])
    
    # Generate CSV operations
    for i, (y, approx_angle) in enumerate(zip([P_Y + calculate_step_size() * i for i in range(NUMBER_OF_MEASUREMENTS)], [row[2] for row in table_data])):
        # 1. Set servo angle
        csv_content.append([
            'servo',
            json.dumps({"angle": int(approx_angle)}),
            f"Servo: Set angle to {int(approx_angle)}° (Y={y:.1f}cm)"
        ])
        
        # 2. Take photo
        csv_content.append([
            'photo',
            '{}',
            f"Camera: Take photo at Y={y:.1f}cm, Angle={int(approx_angle)}°"
        ])
        
        # 3. Move stepper (except for last point)
        if i < NUMBER_OF_MEASUREMENTS - 1:
            # Calculate stepper motor parameters
            step_distance = calculate_step_size()  # cm
            d = 28.0  # Winch diameter in mm (default value)
            circumference = 3.141592653589793 * d  # mm
            step_mm = step_distance * 10  # Convert cm -> mm
            steps = int((step_mm / circumference) * 4096)  # Steps for 28BYJ-48
            direction = 1  # 1 = upward
            speed = 80  # Default speed
            
            csv_content.append([
                'stepper',
                json.dumps({"steps": steps, "direction": direction, "speed": speed}),
                f"Stepper: {steps} steps, {step_distance:.1f}cm, Direction upward, Speed: {speed}"
            ])
    
    # Write CSV file
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in csv_content:
                writer.writerow(row)
                
        print(f"\n=== CSV File Created ===")
        print(f"File: {csv_filename}")
        print(f"Format: ['type', 'params', 'description'] - compatible with main.py")
        
        # Display CSV content in command line
        print(f"\n=== CSV Content Preview ===")
        print(tabulate(csv_content, 
                      headers=['Type', 'Params', 'Description'],
                      tablefmt='grid',
                      numalign='left'))
        
        print(f"\nStepper motor settings: Speed=80, Direction=1 (upward)")
        print(f"Total CSV operations: {len(csv_content)-1} (excluding header)")
        
    except Exception as e:
        print(f"Error creating CSV file: {e}")
        return None
    
    return table_data

def main():
    """Main function to execute the program"""
    print("=== Servo Angle Calculator (Simplified) ===")
    print("Calculating angles and generating CSV file without visualization...")
    
    # Explain angle correction system first
    explain_angle_correction()
    
    # Generate and display results table
    result = generate_results_table()
    
    if result:
        print(f"\n=== Summary ===")
        print(f"[OK] Configuration loaded")
        print(f"[OK] {len(result)} measurement points calculated")
        print(f"[OK] Angles computed and limited to servo range ({SERVO_ANGLE_MIN}°-{SERVO_ANGLE_MAX}°)")
        print(f"[OK] CSV file created in ScanConfigs directory")
        print(f"[OK] Results displayed in command line")
        print("\nCalculation completed successfully!")
    else:
        print("[ERROR] Calculation failed!")

if __name__ == "__main__":
    # Check required libraries
    try:
        from tabulate import tabulate
    except ImportError as e:
        print("Missing library! Please install:")
        print("pip install tabulate")
        print(f"Error: {e}")
        exit(1)
    
    main()
