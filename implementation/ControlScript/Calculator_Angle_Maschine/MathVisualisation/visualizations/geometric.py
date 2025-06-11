#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEOMETRIC VISUALIZATION MODULE
=============================

Creates geometric representation visualization of the 3D scanner system.
Shows the scanner path, target position, and measurement points.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import os
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, OUTPUT_DIR, ensure_output_dir
)


def create_geometric_visualization(angles_data):
    """
    Creates geometric representation visualization
    """
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('white')
    
    ax = plt.subplot(1, 1, 1)
    
    # Setup axes - dynamically adapt to SCAN_DISTANCE and target position
    max_x = max(TARGET_CENTER_X + 20, 90)  # Ensure target is visible with margin
    max_y = max(SCAN_DISTANCE + 10, TARGET_CENTER_Y + 20)  # Adapt to scan distance
    
    ax.set_xlim(-25, max_x)
    ax.set_ylim(-15, max_y)
    ax.grid(True, alpha=0.3, linewidth=0.6, linestyle='--')
    ax.set_aspect('equal')
    ax.set_xlabel('X-Position (cm)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y-Position (cm)', fontsize=10, fontweight='bold')
    ax.set_facecolor('#f8f9fa')
    
    # Coordinate system
    ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.8)
    ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.8)
    
    # Scanner path
    scan_y = np.linspace(0, SCAN_DISTANCE, 100)
    ax.plot([SCANNER_MODULE_X] * len(scan_y), scan_y, 'g-', 
            linewidth=8, alpha=0.6, label='Scanner Movement Path', solid_capstyle='round')
    
    # Target object
    ax.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'bs', markersize=16, 
            markeredgewidth=3, markeredgecolor='navy', zorder=10)
    ax.text(TARGET_CENTER_X + 5, TARGET_CENTER_Y - 3, f'TARGET OBJECT\n({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm', 
            ha='left', va='top', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor="lightblue", 
                     edgecolor='navy', linewidth=1.5, alpha=0.95))
    
    # Measurement points with EXACT and INTERPOLATED angles
    for i, data in enumerate(angles_data):
        y_pos = data['y_pos']
          # Different colors for pure geometric calculations
        point_color = 'green'
        edge_color = 'darkgreen'
        
        # Measurement point
        ax.plot(SCANNER_MODULE_X, y_pos, 'o', color=point_color, markersize=14, 
                markeredgewidth=3, markeredgecolor=edge_color, zorder=15)
          # Connection line to target using ONLY exact trigonometric angle
        # (Physical servo uses interpolated angle, but visualization shows exact geometry)
        line_length = 35
          # EXAKTER trigonometrischer Winkel - zeigt echte geometrische Richtung
        geometric_angle_rad = math.radians(data['angle'])
        dx_exact = line_length * math.sin(geometric_angle_rad)
        dy_exact = line_length * math.cos(geometric_angle_rad)
        ax.plot([SCANNER_MODULE_X, SCANNER_MODULE_X + dx_exact], 
                [y_pos, y_pos + dy_exact], 
                '-', color='darkblue', linewidth=3, alpha=0.8,                label='Geometric Direction' if i == 0 else "")
        
        # Point labels with geometric angle information
        label_text = f'P{data["point"]} Y={y_pos:.1f}cm\n' \
                    f'Angle: {data["angle"]:.1f}°\n' \
                    f'Distance: {data["hypotenuse"]:.1f}cm'
        
        ax.text(SCANNER_MODULE_X - 12, y_pos, label_text,
                ha='right', va='center', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=point_color,                         edgecolor=edge_color, linewidth=1, alpha=0.8))

    ax.legend(fontsize=10, loc='upper right', frameon=True, 
              fancybox=True, shadow=True, framealpha=0.9)
    
    plt.tight_layout()
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, '01_geometric_representation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Geometric visualization saved: {output_path}")
    plt.close()
