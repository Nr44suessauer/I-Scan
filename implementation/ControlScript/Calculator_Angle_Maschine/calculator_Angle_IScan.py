import math
import csv
import json
import os
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

# ===== CONFIGURATION VARIABLES =====

# Servo angle limits (servo motor constraints)
SERVO_ANGLE_MIN = 0       # Lower limit of servo angle in degrees
SERVO_ANGLE_MAX = 90      # Upper limit of servo angle in degrees

# Angle correction reference (geometric calculation)
ANGLE_CORRECTION_REFERENCE = 80  # Reference angle for correction calculation in degrees

# Point P (start coordinates)
P_X = 0                   # X-coordinate of start point
P_Y = 0                   # Y-coordinate of start point

# Point M (end coordinates)
M_X = 0                   # X-coordinate of end point
M_Y = 50                 # Y-coordinate of end point

# New center (target center)
NEW_CENTER_X = 50       # X-coordinate of new center
NEW_CENTER_Y = 0        # Y-coordinate of new center

# Old center (original center)
OLD_CENTER_X = 40        # X-coordinate of old center
OLD_CENTER_Y = 0          # Y-coordinate of old center

# Z-module position (start position)
Z_MODULE_X = 0            # X-coordinate of Z-module (remains fixed)
Z_MODULE_Y = 0            # Y-coordinate of Z-module (start position)

# Scan configuration
DELTA_SCAN = 70         # Total scan distance in cm
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
    with limitation to the configurable servo angle range
    """
    # Calculate original angle
    raw_angle = calculate_angle(current_y)
    
    # Limit to configurable servo angle range
    if raw_angle < SERVO_ANGLE_MIN:
        approximated_angle = SERVO_ANGLE_MIN
    elif raw_angle > SERVO_ANGLE_MAX:
        approximated_angle = SERVO_ANGLE_MAX
    else:
        approximated_angle = raw_angle
    
    return approximated_angle

def calculate_step_size():
    """Calculates the step size for measurements"""
    if NUMBER_OF_MEASUREMENTS > 0:
        return DELTA_SCAN / NUMBER_OF_MEASUREMENTS
    return 0

def generate_results_table():
    """
    Generates the results table with original and approximated angles
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
    print("=" * 50)
    
    # Calculate and record measurements
    table_data = []
    
    for i in range(NUMBER_OF_MEASUREMENTS):
        # Calculate current Y position
        current_y = P_Y + step_size * i
        
        # Calculate original and approximated angle for this position
        original_angle = calculate_angle(current_y)
        approximated_angle = calculate_approximated_angle(current_y)
        
        # Format Z-module coordinates (X remains fixed, Y varies)
        z_coords = f"({Z_MODULE_X}, {round(current_y, 1)})"
        
        # Add data to table (with both angle values)
        table_data.append([
            i + 1,                              # Measurement number
            round(original_angle, 1),           # Original angle
            round(approximated_angle, 1),       # Approximated angle (0-90°)
            z_coords                            # Z-module coordinates
        ])
      # Output table
    print(tabulate(table_data, 
                  headers=['Measurement No.', 'Original Angle (°)', 'Approx. Angle (°)', 'Z-Module (Coordinates)'],
                  tablefmt='grid',
                  numalign='right'))
      # Create CSV file for main.py import (with JSON format for params)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scan_configs_dir = os.path.join(script_dir, 'ScanConfigs')
    
    # Create ScanConfigs directory if it doesn't exist
    if not os.path.exists(scan_configs_dir):
        os.makedirs(scan_configs_dir)
    
    csv_filename = os.path.join(scan_configs_dir, f'angle_table_{NEW_CENTER_X}x{NEW_CENTER_Y}_{NUMBER_OF_MEASUREMENTS}points_approximated.csv')
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Header in main.py format
            writer.writerow(['type', 'params', 'description'])
            
            # Move to home position (optional)
            writer.writerow([
                'home',
                '{}',
                'Move to home position'
            ])
            
            for i, (y, approx_angle) in enumerate(zip([P_Y + calculate_step_size() * i for i in range(NUMBER_OF_MEASUREMENTS)], [row[2] for row in table_data])):
                # 1. Set servo angle
                writer.writerow([
                    'servo',
                    json.dumps({"angle": int(approx_angle)}),
                    f"Servo: Set angle to {int(approx_angle)}° (Y={y:.1f}cm)"
                ])
                
                # 2. Take photo
                writer.writerow([
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
                    
                    dir_text = "upward"
                    
                    writer.writerow([
                        'stepper',
                        json.dumps({"steps": steps, "direction": direction, "speed": speed}),
                        f"Stepper: {steps} steps, {step_distance:.1f}cm, Direction {dir_text}, Speed: {speed}"
                    ])
                    
        print(f"\nCSV file for main.py import created: {csv_filename}")
        print(f"Format: ['type', 'params', 'description'] - compatible with main.py")
        print(f"Stepper speed: 80 (default)")
    except Exception as e:
        print(f"Error creating CSV file: {e}")
    
    # Extract data for graphs
    measurements = [row[0] for row in table_data]  # Measurement numbers
    original_angles = [row[1] for row in table_data]        # Original angles
    approximated_angles = [row[2] for row in table_data]    # Approximated angles
    y_positions = [P_Y + step_size * i for i in range(NUMBER_OF_MEASUREMENTS)]  # Y positions
    
    # Create multiple graphs
    plt.figure(figsize=(20, 16))
    
    # Subplot 1: Table with values
    plt.subplot(2, 3, 1)
    plt.axis('off')  # Hide axes
    
    # Prepare table data for graphical representation
    table_headers = ['No.', 'Original (°)', 'Approx. (°)', 'Y-Pos (cm)', 'Coordinates']
    table_rows = []
    for i, (orig_angle, approx_angle, y) in enumerate(zip(original_angles, approximated_angles, y_positions)):
        table_rows.append([i+1, f"{orig_angle:.1f}°", f"{approx_angle:.1f}°", f"{y:.1f}", f"({Z_MODULE_X}, {y:.1f})"])
    
    # Insert table into diagram
    plt.table(cellText=table_rows,
             colLabels=table_headers,
             cellLoc='center',
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('Measurement Values Table (Original vs. Approximated)', fontsize=14)
    
    # Subplot 2: Detailed calculation table
    plt.subplot(2, 3, 2)
    plt.axis('off')  # Hide axes
    
    # Prepare detailed table data for calculation
    calc_headers = ['No.', 'Y-Pos', 'dx', 'dy', 'α (rad)', 'α (°)', 'Approx.']
    calc_rows = []
    for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
        # Retrace calculation steps (according to new calculate_angle logic)
        dx = NEW_CENTER_X - Z_MODULE_X
        dy = abs(y - NEW_CENTER_Y)  # Absolute value of distance
        
        # New calculation according to corrected calculate_angle function
        if abs(dx) < 0.001:
            alpha_rad = math.pi / 2 if dy == 0 else 0
            alpha_deg = 90.0 if dy == 0 else 0.0
        else:
            alpha_rad = math.atan(dy / abs(dx))
            alpha_deg = alpha_rad * 180 / math.pi
            # Complementary angle for correct orientation
            alpha_deg = 90.0 - alpha_deg
        
        calc_rows.append([
            i+1, 
            f"{y:.1f}", 
            f"{dx:.0f}", 
            f"{dy:.1f}", 
            f"{alpha_rad:.3f}", 
            f"{alpha_deg:.1f}°", 
            f"{approx_angle:.1f}°"
        ])
    
    # Insert table into diagram
    plt.table(cellText=calc_rows,
             colLabels=calc_headers,
             cellLoc='center',
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('Detailed Calculation Steps', fontsize=14)
    
    # Subplot 3: 3D visualization of scan positions and angles
    try:
        from mpl_toolkits.mplot3d import Axes3D
        
        ax = plt.subplot(2, 3, 3, projection='3d')
        
        # Z-module positions (scan points)
        x_scan = [Z_MODULE_X] * len(y_positions)
        z_scan = [0] * len(y_positions)
        ax.scatter(x_scan, y_positions, z_scan, color='blue', s=50, label='Z-Module Positions')
        
        # Scan path
        ax.plot(x_scan, y_positions, z_scan, color='blue', linewidth=2)
        
        # New center
        ax.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [0], color='red', s=100, label='New Center')
        
        # Angle lines with height based on approximated angle value
        for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
            # Normalized approximated angle for height (z-axis)
            z_height = approx_angle / 10  # Scale for better visualization
            
            # Line from scan point to center with height
            ax.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], [0, z_height], 
                   '--', color='green', alpha=0.7)
            
            # Point showing approximated angle in height
            ax.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [z_height], 
                      color='red', s=30, alpha=0.7)
            
            # Text for approximated angle
            ax.text(NEW_CENTER_X + 5, NEW_CENTER_Y, z_height, f"{approx_angle:.1f}°", 
                   fontsize=8, color='red')
        
        # Configure axes and labels
        ax.set_title('3D Representation of Angle Relationships', fontsize=14)
        ax.set_xlabel('X-Position (cm)', fontsize=12)
        ax.set_ylabel('Y-Position (cm)', fontsize=12)
        ax.set_zlabel('Angle (scaled)', fontsize=12)
        ax.legend(loc='best')
        
        # Set viewing angle
        ax.view_init(elev=30, azim=-60)
        
    except Exception as e:
        # Fallback if 3D plot doesn't work
        plt.subplot(2, 3, 3)
        plt.text(0.5, 0.5, f"3D representation not available:\n{e}", 
                ha='center', va='center', fontsize=12, wrap=True)
        plt.axis('off')
    
    # Subplot 4: Visual representation of scan path and angle (2D)
    plt.subplot(2, 3, 4)
    
    # Display Z-module positions
    for i, y in enumerate(y_positions):
        plt.plot(Z_MODULE_X, y, 'o', color='blue', markersize=8)
    
    # Display scan path
    plt.plot([Z_MODULE_X] * len(y_positions), y_positions, '-', color='blue', linewidth=2, label='Scan Path')
    
    # Display new center
    plt.plot(NEW_CENTER_X, NEW_CENTER_Y, 'ro', markersize=10, label='New Center')
    
    # Angle lines and angle text for all measurements (with approximated angles)
    for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
        color_intensity = 0.3 + (i / len(y_positions)) * 0.7  # Color gradient
        # Draw line from Z-module to new center
        plt.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], '--', 
                color=(0, color_intensity, 0), linewidth=1.5, 
                alpha=0.7)
        
        # Display approximated angle as text
        text_x = (Z_MODULE_X + NEW_CENTER_X) / 2 - 15
        text_y = (y + NEW_CENTER_Y) / 2 + 5
        
        # Display angle value (approximated)
        plt.text(text_x, text_y, f"{approx_angle:.1f}°", 
                color='red', fontsize=9, fontweight='bold',
                bbox=dict(facecolor='yellow', alpha=0.7, boxstyle='round,pad=0.3'))
    
    plt.title('2D Representation with Approximated Angles', fontsize=14)
    plt.xlabel('X-Position (cm)', fontsize=12)
    plt.ylabel('Y-Position (cm)', fontsize=12)
    plt.grid(True)
    plt.legend(loc='best')
    
    # Adjust axis length
    max_x = max(NEW_CENTER_X, Z_MODULE_X) * 1.2
    max_y = max(NEW_CENTER_Y, max(y_positions)) * 1.2
    min_x = min(0, Z_MODULE_X) - 10
    min_y = min(0, min(y_positions)) - 10
    plt.axis([min_x, max_x, min_y, max_y])
    
    # Subplot 5: CSV export overview table (new main.py format)
    plt.subplot(2, 3, 5)
    plt.axis('off')  # Hide axes
    
    # Prepare CSV data for overview table (main.py format)
    csv_headers = ['Type', 'Params (JSON)', 'Description']
    csv_preview_rows = []
    
    # Home line
    csv_preview_rows.append(['home', '{}', 'Move to home position'])
    
    # Show first 3 measurement points as example
    for i in range(min(3, NUMBER_OF_MEASUREMENTS)):
        y_pos = P_Y + calculate_step_size() * i
        approx_angle = table_data[i][2]  # Approximated angle from table
        
        # Servo line
        csv_preview_rows.append([
            'servo', 
            f'{{"angle": {int(approx_angle)}}}', 
            f'Servo: {int(approx_angle)}° (Y={y_pos:.1f}cm)'
        ])
        
        # Photo line
        csv_preview_rows.append([
            'photo', 
            '{}', 
            f'Photo at Y={y_pos:.1f}cm'
        ])
        
        # Stepper line (except for last point)
        if i < NUMBER_OF_MEASUREMENTS - 1:
            step_distance = calculate_step_size()
            steps = int((step_distance * 10 / (3.141592653589793 * 28.0)) * 4096)  # Calculate steps
            csv_preview_rows.append([
                'stepper', 
                f'{{"steps": {steps}, "direction": 1, "speed": 80}}', 
                f'{steps} steps, {step_distance:.1f}cm'
            ])
    
    # If more than 3 points, show "..."
    if NUMBER_OF_MEASUREMENTS > 3:
        csv_preview_rows.append(['...', '...', '...'])
    
    # Insert table into diagram
    plt.table(cellText=csv_preview_rows,
             colLabels=csv_headers,
             cellLoc='left',  # Left-aligned for better readability
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('CSV Export Preview (main.py Format)', fontsize=14)
    
    # Subplot 6: Configuration information
    plt.subplot(2, 3, 6)
    plt.axis('off')  # Hide axes
    
    # Text information about configuration
    config_info = [
        f"Configuration:",
        f"",
        f"New center: ({NEW_CENTER_X}, {NEW_CENTER_Y})",
        f"Old center: ({OLD_CENTER_X}, {OLD_CENTER_Y})",
        f"Z-module start: ({Z_MODULE_X}, {Z_MODULE_Y})",
        f"Delta scan: {DELTA_SCAN} cm",
        f"Number of measurements: {NUMBER_OF_MEASUREMENTS}",
        f"Step size: {calculate_step_size():.1f} cm",
        f"Servo limits: {SERVO_ANGLE_MIN}° - {SERVO_ANGLE_MAX}°",
        f"",
        f"Original angle range: {min(original_angles):.1f}° - {max(original_angles):.1f}°",
        f"Approximated angle range: {min(approximated_angles):.1f}° - {max(approximated_angles):.1f}°",
        f"",
        f"CSV file: {os.path.basename(csv_filename)}"
    ]
    
    plt.text(0.5, 0.5, "\n".join(config_info),
            ha='center', va='center', fontsize=10,            bbox=dict(facecolor='lightgray', alpha=0.5, boxstyle='round,pad=1'))
    plt.title('Configuration Information', fontsize=14)
    
    plt.tight_layout()
    
    # Save graphics
    visualization_path = os.path.join(scan_configs_dir, 'scan_visualization_approximated.png')
    plt.savefig(visualization_path, dpi=300, bbox_inches='tight')
    print(f"\nGraphical representation saved as: {visualization_path}")
    
    # Try to display graphic if possible
    try:
        plt.show()
    except Exception as e:
        print(f"Note: The graphic could not be displayed ({e}), but was saved as '{visualization_path}'.")

def main():
    """Main function to execute the program"""
    # Generate and display results table
    generate_results_table()

if __name__ == "__main__":
    # Check required libraries
    try:
        import pandas as pd
        from tabulate import tabulate
    except ImportError as e:
        print("Missing library! Please install:")
        print("pip install pandas tabulate matplotlib")
        print(f"Error: {e}")
        exit(1)
    
    main()
