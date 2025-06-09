#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION MODULE FOR SERVO ANGLE CALCULATION
================================================

Contains all configuration constants used across the 3D scanner angle calculation system.
These values are aligned with calculator_Angle_IScan.py for consistency.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import os

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

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Created output directory: {OUTPUT_DIR}")

# === 3D SCANNER CONFIGURATION ===
# ALIGNED WITH calculator_Angle_IScan.py for consistency
TARGET_CENTER_X = 50      # X-position of target object (cm) - matches NEW_CENTER_X
TARGET_CENTER_Y = 20      # Y-position of target object (cm) - matches NEW_CENTER_Y
SCANNER_MODULE_X = 0      # X-position of scanner (cm) - matches Z_MODULE_X
SCANNER_MODULE_Y = 0      # Y-position of scanner (cm) - matches Z_MODULE_Y
SCAN_DISTANCE = 70       # Total scan distance (cm) - matches DELTA_SCAN
NUMBER_OF_MEASUREMENTS = 4  # Number of measurement points
ANGLE_CORRECTION_REFERENCE = 70  # Mechanical correction (degrees) - matches main calculator
