#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVO INTERPOLATION VISUALIZATION - SIMPLIFIED VERSION
======================================================

Creates simplified visualizations for servo motor interpolation calculations.
Shows geometry and a table with color-coded reachability.

Author: I-Scan Team
Version: 2.0
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y,
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    ensure_output_dir
)
from servo_interpolation import (
    calculate_servo_interpolation,
    SERVO_NEUTRAL_ANGLE, COORD_MIN_ANGLE, COORD_MAX_ANGLE, COORD_NEUTRAL_ANGLE,
    SERVO_MIN_ANGLE, SERVO_MAX_ANGLE
)


def create_servo_interpolation_visualization():
    """
    Create a simplified visualization of servo interpolation with geometry and table
    """
    # Get servo data
    servo_data = calculate_servo_interpolation()
    
    # Create figure with 2 subplots: geometry and table
    fig = plt.figure(figsize=(16, 10))
    
    # === SUBPLOT 1: Geometric Setup with Servo Cones ===
    ax1 = plt.subplot(2, 1, 1)
    
    # Plot scanner path
    y_positions = [data['y_pos'] for data in servo_data]
    x_positions = [SCANNER_MODULE_X for _ in servo_data]
    
    ax1.plot(x_positions, y_positions, 'b-', linewidth=3, label='Scanner Path', marker='o', markersize=8)
    
    # Plot target
    ax1.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'ro', markersize=12, label='Target Object')
    
    # Plot lines from each scanner position to target
    for data in servo_data:
        color = 'green' if data['is_reachable'] else 'red'
        linestyle = '-' if data['is_reachable'] else '--'
        ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], 
                [data['y_pos'], TARGET_CENTER_Y], 
                color=color, linestyle=linestyle, alpha=0.7, linewidth=1)    # Draw servo cones from all positions (zeigen in Richtung Target Object)
    for i, data in enumerate(servo_data):
        cone_center_x = SCANNER_MODULE_X
        cone_center_y = data['y_pos']
        cone_radius = 25  # Visual radius for cone display
        
        # Servo cone zeigt in Richtung Target: 1./4. Quadranten (-45° bis +45°)
        coord_min = -45.0  # 4th quadrant boundary
        coord_max = 45.0   # 1st quadrant boundary
        
        # Convert coordinate angles to radians for display
        angle1_rad = math.radians(coord_min)  # -45°
        angle2_rad = math.radians(coord_max)  # +45°
        
        # Create cone visualization
        cone_x1 = cone_center_x + cone_radius * math.cos(angle1_rad)
        cone_y1 = cone_center_y + cone_radius * math.sin(angle1_rad)
        cone_x2 = cone_center_x + cone_radius * math.cos(angle2_rad)
        cone_y2 = cone_center_y + cone_radius * math.sin(angle2_rad)
        
        # Color based on reachability
        cone_color = 'green' if data['is_reachable'] else 'red'
        cone_alpha = 0.3 if data['is_reachable'] else 0.2
        
        # Draw cone boundaries
        if i == 0:  # Only add label once
            ax1.plot([cone_center_x, cone_x1], [cone_center_y, cone_y1], 'purple', linewidth=1, alpha=0.6, label='Servo Cone Boundaries')
            ax1.plot([cone_center_x, cone_x2], [cone_center_y, cone_y2], 'purple', linewidth=1, alpha=0.6)
        else:
            ax1.plot([cone_center_x, cone_x1], [cone_center_y, cone_y1], 'purple', linewidth=1, alpha=0.6)
            ax1.plot([cone_center_x, cone_x2], [cone_center_y, cone_y2], 'purple', linewidth=1, alpha=0.6)
        
        # Fill cone area
        theta = np.linspace(angle1_rad, angle2_rad, 30)
        cone_x = cone_center_x + cone_radius * np.cos(theta)
        cone_y = cone_center_y + cone_radius * np.sin(theta)
        cone_x = np.append([cone_center_x], cone_x)
        cone_y = np.append([cone_center_y], cone_y)
        ax1.fill(cone_x, cone_y, color=cone_color, alpha=cone_alpha)
    
    ax1.set_xlabel('X Position (cm)', fontweight='bold')
    ax1.set_ylabel('Y Position (cm)', fontweight='bold')
    ax1.set_title('3D Scanner Servo Interpolation - Geometric Overview', fontweight='bold', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_aspect('equal', adjustable='box')
    
    # === SUBPLOT 2: Servo Reachability Table ===
    ax2 = plt.subplot(2, 1, 2)
    ax2.axis('off')  # Hide axes for table
    
    # Create table data
    table_data = []
    colors = []    # Table headers
    headers = ['Point', 'Y-Pos\n(cm)', 'Geometric\nAngle (°)', 'Target Coord\nAngle (°)', 'Physical\nServo (°)', 'Reachable']
    
    for data in servo_data:
        # Determine row color based on reachability
        if data['is_reachable']:
            row_color = ['lightgreen'] * 6  # Green for reachable
            reach_text = '✓ YES'
        else:
            row_color = ['lightcoral'] * 6  # Red for unreachable
            reach_text = '✗ NO'
        
        colors.append(row_color)
        
        # Format row data with corrected values
        row = [
            f"{data['point']}",
            f"{data['y_pos']:.1f}",
            f"{data['geometric_angle']:.1f}°",
            f"{data['target_coord_angle']:.1f}°",  # NEW: Target angle in coordinate system
            f"{data['servo_angle']:.1f}°",   # CORRECTED: Physical servo control angle
            reach_text
        ]
        table_data.append(row)
    
    # Create the table
    table = ax2.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)  # Make rows taller
    
    # Style header row
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(0, i)].set_height(0.15)
    
    # Style data rows with colors
    for i, row_colors in enumerate(colors):
        for j, color in enumerate(row_colors):
            table[(i+1, j)].set_facecolor(color)
            table[(i+1, j)].set_height(0.12)
    
    ax2.set_title('Servo Reachability Analysis Table', fontweight='bold', fontsize=14, pad=20)
    
    # Add overall title
    fig.suptitle('3D Scanner Servo Interpolation Analysis', fontsize=16, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    return fig


def save_servo_interpolation_visualization():
    """
    Create and save the servo interpolation visualization
    """
    ensure_output_dir()
    
    print("🎨 Creating servo interpolation visualization...")
    
    fig = create_servo_interpolation_visualization()
    
    # Save the figure
    output_path = "output/06_servo_interpolation.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Servo interpolation visualization saved: {output_path}")
    
    plt.close(fig)
    return output_path


def create_servo_cone_detail():
    """
    Create a detailed visualization of the servo cone concept
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Draw coordinate system
    ax.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax.axvline(x=0, color='black', linewidth=1, alpha=0.5)
    
    # Draw servo position
    servo_x, servo_y = 0, 0
    ax.plot(servo_x, servo_y, 'ko', markersize=12, label='Servo Position')    # Draw servo cone (zeigt in Richtung Target: 1./4. Quadranten -45° bis +45°)
    cone_radius = 5
    coord_min = -45.0  # 4th quadrant boundary
    coord_max = 45.0   # 1st quadrant boundary
    
    # Convert coordinate angles to radians
    angle1_rad = math.radians(coord_min)  # -45°
    angle2_rad = math.radians(coord_max)  # +45°
    
    # Cone boundaries
    cone_x1 = servo_x + cone_radius * math.cos(angle1_rad)
    cone_y1 = servo_y + cone_radius * math.sin(angle1_rad)
    cone_x2 = servo_x + cone_radius * math.cos(angle2_rad)
    cone_y2 = servo_y + cone_radius * math.sin(angle2_rad)
    
    ax.plot([servo_x, cone_x1], [servo_y, cone_y1], 'purple', linewidth=3, label='-45° Limit (4. Quadrant)')
    ax.plot([servo_x, cone_x2], [servo_y, cone_y2], 'purple', linewidth=3, label='+45° Limit (1. Quadrant)')
    
    # Fill cone (1. und 4. Quadrant)
    theta = np.linspace(angle1_rad, angle2_rad, 50)
    cone_x = servo_x + cone_radius * np.cos(theta)
    cone_y = servo_y + cone_radius * np.sin(theta)
    cone_x = np.append([servo_x], cone_x)
    cone_y = np.append([servo_y], cone_y)
    ax.fill(cone_x, cone_y, color='purple', alpha=0.3, label='Servo Reachable Cone (Target-Richtung)')
    
    # Draw neutral position (0° = positive X-axis, Target-Richtung)
    neutral_rad = math.radians(0)  # Positive X-Achse = 0° (Servo 45° position)
    neutral_x = servo_x + cone_radius * 0.7 * math.cos(neutral_rad)
    neutral_y = servo_y + cone_radius * 0.7 * math.sin(neutral_rad)
    ax.plot([servo_x, neutral_x], [servo_y, neutral_y], 'orange', linewidth=3, linestyle='--', label='Neutral Position (0°, Target-Richtung)')
    
    # Add angle annotations
    ax.annotate('-45°', xy=(cone_x1, cone_y1), xytext=(cone_x1+0.5, cone_y1-0.5),
                fontsize=12, fontweight='bold', color='purple')
    ax.annotate('+45°', xy=(cone_x2, cone_y2), xytext=(cone_x2+0.5, cone_y2+0.5),
                fontsize=12, fontweight='bold', color='purple')
    ax.annotate('0°', xy=(neutral_x, neutral_y), xytext=(neutral_x+0.5, neutral_y-0.5),
                fontsize=12, fontweight='bold', color='orange')
    
    # Add coordinate system labels
    ax.text(6, 0.2, '+X', fontsize=12, fontweight='bold')
    ax.text(0.2, 6, '+Y', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_xlabel('X Coordinate', fontweight='bold')
    ax.set_ylabel('Y Coordinate', fontweight='bold')
    ax.set_title('Servo Motor Cone Concept\n(Zeigt in Richtung Target: -45° bis +45°)', fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    
    return fig


def save_servo_cone_detail():
    """
    Create and save the detailed servo cone visualization
    """
    ensure_output_dir()
    
    print("🎨 Creating servo cone detail visualization...")
    
    fig = create_servo_cone_detail()
    
    # Save the figure
    output_path = "output/07_servo_cone_detail.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Servo cone detail visualization saved: {output_path}")
    
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    """Run servo interpolation visualizations when executed directly"""
    save_servo_interpolation_visualization()
    save_servo_cone_detail()
