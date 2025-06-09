#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POINT CALCULATION VISUALIZATION MODULE
======================================

Creates individual point calculation visualization with coordinate system
for each measurement point.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import os
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    ANGLE_CORRECTION_REFERENCE, OUTPUT_DIR, ensure_output_dir
)


def create_point_calculation_visualization(point_data, point_number):
    """
    Creates individual point calculation visualization with coordinate system
    """
    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle(f'CALCULATION FOR MEASUREMENT POINT {point_number}', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    # Left side: Coordinate system with highlighted point
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_title(f'Coordinate System - Point {point_number}', 
                  fontsize=12, fontweight='bold', pad=20, color='darkblue')
    
    # Grid and axes
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-10, 110)
    ax1.set_ylim(-10, 110)
    ax1.set_xlabel('X Position (cm)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Y Position (cm)', fontsize=10, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.set_facecolor('#f8f9fa')
    
    # Coordinate axes
    ax1.axhline(y=0, color='black', linewidth=1.5, alpha=0.8)
    ax1.axvline(x=0, color='black', linewidth=1.5, alpha=0.8)
    
    # Scanner position (current point)
    ax1.plot(SCANNER_MODULE_X, point_data['y_pos'], 'ro', markersize=15, 
             markeredgewidth=3, markeredgecolor='darkred', zorder=10,
             label=f'Scanner at Point {point_number}')
    
    # Target position
    ax1.add_patch(patches.Rectangle((TARGET_CENTER_X-2, TARGET_CENTER_Y-2), 4, 4, 
                      facecolor='blue', edgecolor='darkblue', linewidth=2, alpha=0.8))
    ax1.text(TARGET_CENTER_X + 5, TARGET_CENTER_Y, f'TARGET\n({TARGET_CENTER_X}, {TARGET_CENTER_Y})', 
             ha='left', va='center', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", 
                      edgecolor='blue', linewidth=2, alpha=0.9))
    
    # Triangle visualization
    ax1.add_patch(patches.Circle((SCANNER_MODULE_X, point_data['y_pos']), 1.5, 
                      facecolor='red', edgecolor='red', linewidth=2, alpha=0.9))
    
    # Connection line (triangle visualization)
    ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [point_data['y_pos'], TARGET_CENTER_Y], 
             'r--', linewidth=3, alpha=0.8, label=f'Line to target')
    
    # Distance annotations
    mid_x = (SCANNER_MODULE_X + TARGET_CENTER_X) / 2
    mid_y = (point_data['y_pos'] + TARGET_CENTER_Y) / 2
    distance = math.sqrt(point_data['dx']**2 + point_data['dy']**2)
    ax1.text(mid_x, mid_y, f'{distance:.1f} cm', ha='center', va='bottom', 
             fontsize=8, fontweight='bold', rotation=point_data['alpha'],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", 
                      edgecolor='red', linewidth=1, alpha=0.9))
    
    # dx and dy lines
    if point_data['dx'] > 0:
        ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [point_data['y_pos'], point_data['y_pos']], 
                 'green', linewidth=2, alpha=0.7)
        ax1.text(mid_x, point_data['y_pos'] - 5, f'dx = {point_data["dx"]} cm', 
                 ha='center', va='top', fontsize=8, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="lightgreen", alpha=0.7))
    
    if point_data['dy'] > 0:
        ax1.plot([TARGET_CENTER_X, TARGET_CENTER_X], [point_data['y_pos'], TARGET_CENTER_Y], 
                 'purple', linewidth=2, alpha=0.7)
        ax1.text(TARGET_CENTER_X + 2, (point_data['y_pos'] + TARGET_CENTER_Y)/2, 
                 f'dy = {point_data["dy"]:.1f} cm', ha='left', va='center', fontsize=8, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="purple", alpha=0.7))
    
    ax1.legend(loc='upper left', fontsize=8)
    
    # Right side: Calculation text
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_title(f'Step-by-Step Calculation', 
                  fontsize=12, fontweight='bold', pad=20, color='darkblue')
    ax2.axis('off')
    ax2.set_facecolor('#f8f9fa')
    
    # Calculation details
    calculation_text = f"""MEASUREMENT POINT {point_number} CALCULATION:

📍 POSITION DATA:
• Scanner position: ({SCANNER_MODULE_X}, {point_data['y_pos']:.1f}) cm
• Target position: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm

📏 DISTANCE CALCULATION:
• dx = {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {point_data['dx']} cm
• dy = |{point_data['y_pos']:.1f} - {TARGET_CENTER_Y}| = {point_data['dy']:.1f} cm
• Distance = √(dx² + dy²) = √({point_data['dx']}² + {point_data['dy']:.1f}²) = {math.sqrt(point_data['dx']**2 + point_data['dy']**2):.1f} cm

🧮 TRIGONOMETRIC CALCULATION:
• α = arctan(dy ÷ dx)
• α = arctan({point_data['dy']:.1f} ÷ {point_data['dx']})
• α = {point_data['alpha']:.2f}°

⚙️ SERVO ANGLE CALCULATION:
• Theoretical angle = 90° - α
• Theoretical angle = 90° - {point_data['alpha']:.2f}°
• Theoretical angle = {point_data['theoretical']:.2f}°

🔧 MECHANICAL CORRECTION:
• Correction = {ANGLE_CORRECTION_REFERENCE} - 90 = {ANGLE_CORRECTION_REFERENCE - 90}°
• Final servo angle = {point_data['theoretical']:.2f}° + {ANGLE_CORRECTION_REFERENCE - 90}°
• Final servo angle = {point_data['final']:.2f}°

✅ RESULT: {point_data['final']:.2f}° servo angle for Point {point_number}"""
    
    ax2.text(0.05, 0.95, calculation_text, transform=ax2.transAxes, fontsize=10,            verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.6", facecolor="lightcyan", 
                     edgecolor='teal', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, f'04_point_{point_number}_calculation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Point {point_number} calculation visualization saved: {output_path}")
    plt.close()
