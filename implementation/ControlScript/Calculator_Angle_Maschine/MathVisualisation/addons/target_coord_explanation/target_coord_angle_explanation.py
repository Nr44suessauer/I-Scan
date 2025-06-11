#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TARGET COORDINATE ANGLE CALCULATION EXPLANATION (ADD-ON)
========================================================

OPTIONAL ADD-ON FEATURE - Educational extension

Explains and visualizes the calculation of the Target Coordinate Angle
for the 3D Scanner Servo System with extended student-friendly explanations.

This is an optional add-on feature that provides detailed educational
explanations. It is not part of the core functionality (01-07).

Author: I-Scan Team
Version: 1.0 (Add-on)
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os

# Add parent directory to path for config imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y,
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    ensure_output_dir
)
from calculations import calculate_geometric_angles


def explain_target_coord_angle_calculation():
    """
    Explains the Target Coordinate Angle calculation step by step
    """
    print("=" * 80)
    print("   TARGET COORDINATE ANGLE CALCULATION EXPLANATION")
    print("=" * 80)
    print()
    
    print("🎯 WHAT IS THE TARGET COORDINATE ANGLE?")
    print("   The Target Coordinate Angle is the angle from scanner to target")
    print("   in the standard coordinate system (0° = +X-axis, 90° = +Y-axis)")
    print()
    
    print("📊 COORDINATE SYSTEM:")
    print("   • 0° = +X-axis (right)")
    print("   • 90° = +Y-axis (up)")
    print("   • 180° = -X-axis (left)")
    print("   • 270° = -Y-axis (down)")
    print()
    
    print("🔧 USED VARIABLES:")
    print(f"   • TARGET_CENTER_X = {TARGET_CENTER_X} cm (Target X-Position)")
    print(f"   • TARGET_CENTER_Y = {TARGET_CENTER_Y} cm (Target Y-Position)")
    print(f"   • SCANNER_MODULE_X = {SCANNER_MODULE_X} cm (Scanner X-Position)")
    print(f"   • scanner_y = variable (Scanner Y-Position, changes for each measurement point)")
    print()
    
    print("📐 CALCULATION FORMULA:")
    print("   1. dx = TARGET_CENTER_X - SCANNER_MODULE_X")
    print("   2. dy = TARGET_CENTER_Y - scanner_y")
    print("   3. target_coord_angle = atan2(dy, dx) * (180/π)")
    print("   4. Normalization to -180° to +180° range")
    print()
      # Get geometric angles for calculation
    geometric_angles = calculate_geometric_angles()
    
    print("🧮 STEP-BY-STEP CALCULATION FOR ALL MEASUREMENT POINTS:")
    print("   " + "-" * 75)
    print()
    
    for i, angle_data in enumerate(geometric_angles):
        scanner_y = angle_data['y_pos']
        print(f"   📍 MEASUREMENT POINT {i+1} (Scanner Y = {scanner_y} cm):")
        print("   " + "~" * 50)
        
        # Step 1: calculate dx
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        print(f"   Step 1: dx = {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm")
        
        # Step 2: calculate dy
        dy = TARGET_CENTER_Y - scanner_y
        print(f"   Step 2: dy = {TARGET_CENTER_Y} - {scanner_y} = {dy} cm")
        
        # Step 3: calculate atan2
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        print(f"   Step 3: atan2({dy}, {dx}) = {angle_rad:.4f} rad = {angle_deg:.2f}°")
        
        # Step 4: normalization
        normalized_angle = angle_deg
        while normalized_angle > 180.0:
            normalized_angle -= 360.0
        while normalized_angle < -180.0:
            normalized_angle += 360.0
        
        if abs(normalized_angle - angle_deg) > 0.001:
            print(f"   Step 4: Normalized from {angle_deg:.2f}° to {normalized_angle:.2f}°")
        else:
            print(f"   Step 4: Already in range [-180°, +180°]: {normalized_angle:.2f}°")
          # Explain vector direction
        if dx > 0 and dy > 0:
            quadrant = "1st Quadrant (right up)"
        elif dx < 0 and dy > 0:
            quadrant = "2nd Quadrant (left up)"
        elif dx < 0 and dy < 0:
            quadrant = "3rd Quadrant (left down)"
        else:
            quadrant = "4th Quadrant (right down)"
        
        print(f"   → Vector points to {quadrant}")
        print(f"   → Target Coordinate Angle: {normalized_angle:.2f}°")
        print()
    
    print("✅ TARGET COORDINATE ANGLE CALCULATION COMPLETED!")
    print()
    
    return geometric_angles


def create_target_coord_angle_visualization():
    """
    Creates a visual representation of the Target Coordinate Angle calculation
    """
    # Get measurement data
    geometric_angles = calculate_geometric_angles()
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # === SUBPLOT 1: Koordinatensystem und Vektoren ===
    ax1.set_aspect('equal')
    
    # Draw coordinate system
    ax1.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax1.axvline(x=0, color='black', linewidth=1, alpha=0.5)
    
    # Add coordinate system labels
    ax1.text(60, 2, '+X (0°)', fontsize=12, fontweight='bold', ha='center')
    ax1.text(2, 55, '+Y (90°)', fontsize=12, fontweight='bold', ha='center', rotation=90)
    ax1.text(-60, 2, '-X (180°)', fontsize=12, fontweight='bold', ha='center')
    ax1.text(2, -55, '-Y (270°)', fontsize=12, fontweight='bold', ha='center', rotation=90)
    
    # Plot target
    ax1.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'ro', markersize=12, label=f'Target ({TARGET_CENTER_X}, {TARGET_CENTER_Y})')
    
    # Plot scanner positions and vectors
    colors = plt.cm.viridis(np.linspace(0, 1, len(geometric_angles)))
    
    for i, (angle_data, color) in enumerate(zip(geometric_angles, colors)):
        scanner_y = angle_data['y_pos']
        
        # Plot scanner position
        ax1.plot(SCANNER_MODULE_X, scanner_y, 'bs', markersize=8, color=color)
        ax1.text(SCANNER_MODULE_X-5, scanner_y, f'P{i+1}', fontsize=10, fontweight='bold', 
                ha='right', va='center', color=color)
        
        # Calculate vector components
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - scanner_y
        
        # Draw vector
        ax1.arrow(SCANNER_MODULE_X, scanner_y, dx*0.8, dy*0.8, 
                 head_width=2, head_length=3, fc=color, ec=color, alpha=0.7)
        
        # Calculate target coordinate angle
        target_coord_angle = math.degrees(math.atan2(dy, dx))
        while target_coord_angle > 180.0:
            target_coord_angle -= 360.0
        while target_coord_angle < -180.0:
            target_coord_angle += 360.0
        
        # Add angle annotation
        mid_x = SCANNER_MODULE_X + dx*0.5
        mid_y = scanner_y + dy*0.5
        ax1.text(mid_x, mid_y, f'{target_coord_angle:.1f}°', 
                fontsize=9, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax1.set_xlim(-10, 70)
    ax1.set_ylim(-10, 60)
    ax1.set_xlabel('X Position (cm)', fontweight='bold')
    ax1.set_ylabel('Y Position (cm)', fontweight='bold')
    ax1.set_title('Target Coordinate Angle Vectors\n(Standard-Koordinatensystem)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # === SUBPLOT 2: Berechnungsdetails Tabelle ===
    ax2.axis('off')
    
    # Create calculation table
    table_data = []
    headers = ['Point', 'Scanner Y\n(cm)', 'dx\n(cm)', 'dy\n(cm)', 'atan2(dy,dx)\n(rad)', 'Target Coord\nAngle (°)', 'Quadrant']
    
    for i, angle_data in enumerate(geometric_angles):
        scanner_y = angle_data['y_pos']
        
        # Calculate components
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - scanner_y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Normalize
        normalized_angle = angle_deg
        while normalized_angle > 180.0:
            normalized_angle -= 360.0
        while normalized_angle < -180.0:
            normalized_angle += 360.0
        
        # Determine quadrant
        if dx > 0 and dy >= 0:
            quadrant = "I"
        elif dx <= 0 and dy > 0:
            quadrant = "II"
        elif dx < 0 and dy <= 0:
            quadrant = "III"
        else:
            quadrant = "IV"
        
        row = [
            f"{i+1}",
            f"{scanner_y:.1f}",
            f"{dx}",
            f"{dy:.1f}",
            f"{angle_rad:.3f}",
            f"{normalized_angle:.1f}°",
            quadrant
        ]
        table_data.append(row)
    
    # Create table
    table = ax2.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0.3, 1, 0.6])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
      # Add explanation text
    explanation = """
CALCULATION FORMULA:
1. dx = TARGET_CENTER_X - SCANNER_MODULE_X = 50 - 0 = 50 cm (constant)
2. dy = TARGET_CENTER_Y - scanner_y = 50 - scanner_y (variable)
3. target_coord_angle = atan2(dy, dx) * (180/π)
4. Normalization to [-180°, +180°] range

COORDINATE SYSTEM:
• 0° = +X-axis (right)      • 180° = -X-axis (left)
• 90° = +Y-axis (up)        • 270° = -Y-axis (down)

QUADRANTS:
I: dx>0, dy≥0    II: dx≤0, dy>0    III: dx<0, dy≤0    IV: dx≥0, dy<0
    """
    
    ax2.text(0.05, 0.25, explanation, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    ax2.set_title('Target Coordinate Angle Calculation - Details', fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    return fig


def save_target_coord_angle_visualization():
    """
    Saves the enhanced Target Coordinate Angle visualization
    """
    ensure_output_dir()
    
    print("🎨 Creating enhanced Target Coordinate Angle visualization...")
    
    # Import the enhanced function from subdirectory
    try:
        from target_coord_explanation.target_coord_angle_explanation_new import create_student_friendly_visualization
        fig = create_student_friendly_visualization()
        
        # Save the figure
        output_path = os.path.join(parent_dir, "output", "08_target_coord_angle_explanation.png")
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        print(f"✅ Enhanced Target Coordinate Angle visualization saved: {output_path}")
        
        plt.close(fig)
        return output_path
        
    except ImportError as e:
        print(f"⚠️ Enhanced visualization not available: {e}")
        print("   Using basic visualization instead...")
        
        # Fallback to basic visualization
        fig = create_target_coord_angle_visualization()
        output_path = os.path.join(parent_dir, "output", "08_target_coord_angle_explanation_basic.png")
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        print(f"✅ Basic Target Coordinate Angle visualization saved: {output_path}")
        
        plt.close(fig)
        return output_path


if __name__ == "__main__":
    """Run target coordinate angle explanation when executed directly"""
    explain_target_coord_angle_calculation()
    save_target_coord_angle_visualization()
