#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION MODULE FOR GEOMETRIC ANGLE CALCULATION
====================================================

Contains all configuration constants used across the 3D scanner geometric angle calculation system.
Pure geometric calculations without servo interpolation.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 3.0 (Pure geometry - no servo interpolation)
"""

import matplotlib.pyplot as plt
import os
import shutil

# === 3D SCANNER CONFIGURATION ===
# Pure geometric configuration
TARGET_CENTER_X = 50      # X-position of target object (cm)
TARGET_CENTER_Y = 50      # Y-position of target object (cm)
SCANNER_MODULE_X = 0      # X-position of scanner (cm)
SCANNER_MODULE_Y = 0      # Y-position of scanner (cm)
SCAN_DISTANCE = 100       # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 10 # Number of measurement points

# === SERVO MOTOR CONFIGURATION ===
# Servo interpolation parameters for 3D scanner
SERVO_MIN_ANGLE = 0.0      # Minimum servo angle (degrees)
SERVO_MAX_ANGLE = 90.0     # Maximum servo angle (degrees)
SERVO_NEUTRAL_ANGLE = 135.0 # Servo neutral position at 30° physical angle
SERVO_ROTATION_OFFSET = SERVO_NEUTRAL_ANGLE  # Servo rotation offset from Y-axis (degrees)

# Coordinate system mapping (automatically calculated from servo parameters)
# Formula: servo_angle + SERVO_ROTATION_OFFSET + 180° → normalized to [-180°, 180°]
def _normalize_angle(angle):
    """Normalize angle to range [-180°, 180°]"""
    while angle > 180:
        angle -= 360
    while angle <= -180:
        angle += 360
    return angle

# Calculated coordinate system angles
COORD_MAX_ANGLE = _normalize_angle(SERVO_MIN_ANGLE + SERVO_ROTATION_OFFSET + 180.0)  # -135.0°
COORD_MIN_ANGLE = _normalize_angle(SERVO_MAX_ANGLE + SERVO_ROTATION_OFFSET + 180.0)  # -45.0°
COORD_NEUTRAL_ANGLE = _normalize_angle(SERVO_NEUTRAL_ANGLE + SERVO_ROTATION_OFFSET + 180.0)  # -90.0°

# === VISUALIZATION CONFIGURATION ===
# Control which visualizations are generated when running main.py
ENABLE_VISUALIZATIONS = {
    # CORE FEATURES (01-07) - Main functionality
    'geometric_representation': True,    # 01_geometric_representation.png
    'angle_progression': False,         # 02_angle_progression.png (DISABLED)
    'point_calculations': True,         # 04_point_X_calculation.png (all points)
    'calculation_table': True,          # 05_calculation_table.png
    'servo_interpolation': True,        # 06_servo_interpolation.png
    'servo_cone_detail': True,          # 07_servo_cone_detail.png
    
    # ADD-ON FEATURES (08+) - Optional educational extensions
    'target_coord_angle_explanation': False,  # 08_target_coord_angle_explanation.png (Add-on)
}

# Visualization settings
VISUALIZATION_SETTINGS = {
    'save_individual_point_calculations': True,  # Save individual point calculation images
}


# Global flag to track if directory has been refreshed this session
_directory_refreshed = False

# Configure matplotlib for clean, high-resolution images
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 8
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'



# === OUTPUT CONFIGURATION ===
OUTPUT_DIR = "output"  # Directory for saving generated images
POINT_CALCULATIONS_SUBDIR = "point_calculations"  # Subfolder for 04_point_X_calculation.png files

def ensure_output_dir():
    """Delete existing output directory and create a fresh one - only once per session."""
    global _directory_refreshed
    import time
    
    # If already refreshed this session, just ensure directory exists
    if _directory_refreshed:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        # Also ensure point calculations subfolder exists
        point_calc_dir = os.path.join(OUTPUT_DIR, POINT_CALCULATIONS_SUBDIR)
        if not os.path.exists(point_calc_dir):
            os.makedirs(point_calc_dir)
        return
    
    if os.path.exists(OUTPUT_DIR):
        # Try to remove the directory, with retries for Windows file locking issues
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                shutil.rmtree(OUTPUT_DIR)
                print(f"🗑️ Deleted existing output directory: {OUTPUT_DIR}")
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    print(f"⚠️ Directory in use, waiting... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(1)
                else:
                    print(f"⚠️ Could not delete directory (files may be open). Clearing contents instead...")
                    # If we can't delete the directory, clear its contents
                    try:
                        for filename in os.listdir(OUTPUT_DIR):
                            file_path = os.path.join(OUTPUT_DIR, filename)
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                        print(f"🗑️ Cleared contents of output directory: {OUTPUT_DIR}")
                    except Exception as e:
                        print(f"⚠️ Warning: Could not clear all files from output directory: {e}")
                    _directory_refreshed = True  # Mark as refreshed even if we only cleared contents
                    return  # Don't try to create the directory again
            except Exception as e:
                print(f"⚠️ Warning: Could not delete output directory: {e}")
                _directory_refreshed = True
                return
    
    # Create the directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Created fresh output directory: {OUTPUT_DIR}")
    else:
        print(f"📁 Output directory ready: {OUTPUT_DIR}")
    
    # Create point calculations subfolder
    point_calc_dir = os.path.join(OUTPUT_DIR, POINT_CALCULATIONS_SUBDIR)
    if not os.path.exists(point_calc_dir):
        os.makedirs(point_calc_dir)
        print(f"📁 Created point calculations subfolder: {point_calc_dir}")
    
    # Mark as refreshed
    _directory_refreshed = True

