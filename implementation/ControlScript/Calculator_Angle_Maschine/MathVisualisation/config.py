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
# Pure geometric configuration
TARGET_CENTER_X = 50      # X-position of target object (cm)
TARGET_CENTER_Y = 25      # Y-position of target object (cm)
SCANNER_MODULE_X = 0      # X-position of scanner (cm)
SCANNER_MODULE_Y = 0      # Y-position of scanner (cm)
SCAN_DISTANCE = 50        # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 6  # Number of measurement points
