#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION MODULE FOR GEOMETRIC ANGLE CALCULATION
====================================================

Contains all configuration constants used across the 3D scanner geometric angle calculation system.
Pure geometric calculations without servo interpolation.

Author: I-Scan Team
Version: 3.0 (Pure geometry - no servo interpolation)
"""

import matplotlib.pyplot as plt
import os
import shutil

# === 3D SCANNER CONFIGURATION ===
# Pure geometric configuration
TARGET_CENTER_X = 33      # X-position of target object (cm)
TARGET_CENTER_Y = 50      # Y-position of target object (cm)
SCANNER_MODULE_X = 0      # X-position of scanner (cm)
SCANNER_MODULE_Y = 0      # Y-position of scanner (cm)
SCAN_DISTANCE = 80       # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 7 # Number of measurement points

# === SERVO MOTOR CONFIGURATION ===
# Servo interpolation parameters for 3D scanner
SERVO_MIN_ANGLE = 0.0      # Minimum servo angle (degrees)
SERVO_MAX_ANGLE = 90.0     # Maximum servo angle (degrees)
SERVO_NEUTRAL_ANGLE = 45.0 # Servo neutral position at 45° physical angle

# Coordinate system mapping (servo rotated by 45° from Y-axis, then 180°)
# When servo is at 0°: coordinate angle = 225° (or -135°) (upper limit)
# When servo is at 90°: coordinate angle = 315° (or -45°) (lower limit)
COORD_MAX_ANGLE = -135.0   # Upper limit in coordinate system (servo at 0°)
COORD_MIN_ANGLE = -45.0    # Lower limit in coordinate system (servo at 90°)
COORD_NEUTRAL_ANGLE = -90.0 # Neutral position in coordinate system (center of cone)

# Servo mounting information
SERVO_ROTATION_OFFSET = 45.0  # Servo rotation offset from Y-axis (degrees)

# === VISUALIZATION CONFIGURATION ===
# Control which visualizations are generated when running main.py
ENABLE_VISUALIZATIONS = {
    # CORE FEATURES (01-07) - Main functionality
    'geometric_representation': True,    # 01_geometric_representation.png
    'angle_progression': True,          # 02_angle_progression.png  
    # 'trigonometry_formulas': False,      # 03_trigonometry_formulas.png (DELETED)
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
    'show_detailed_explanations': True,         # Include detailed explanations in images
    'use_color_coding': True,                   # Use color coding for reachability analysis
    'export_high_resolution': True,            # Export in high resolution (300 DPI)
}

# === ADD-ON CONFIGURATION ===
# Settings for optional add-on features
ADDON_SETTINGS = {
    'enable_educational_extensions': True,      # Allow educational add-ons to load
    'fallback_to_basic_on_error': True,        # Use basic versions if enhanced add-ons fail
    'show_addon_status_messages': True,        # Display status messages for add-ons
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

