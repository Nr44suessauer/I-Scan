#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVO INTERPOLATION VISUALIZATION
=================================

Creates visualizations for servo motor interpolation calculations.
Shows the servo cone, reachable areas, and angle mappings.

Author: I-Scan Team
Version: 1.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y,
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS,
    ensure_output_dir
)
from servo_interpolation import (
    calculate_servo_interpolation,
    SERVO_NEUTRAL_ANGLE, COORD_MIN_ANGLE, COORD_MAX_ANGLE,
    SERVO_MIN_ANGLE, SERVO_MAX_ANGLE
)


def create_servo_interpolation_visualization():
    """
    Create a comprehensive visualization of servo interpolation
    """
    # Get servo data
    servo_data = calculate_servo_interpolation()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # === SUBPLOT 1: Geometric Setup with Servo Cone ===
    ax1 = plt.subplot(2, 2, 1)
    
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
                color=color, linestyle=linestyle, alpha=0.7, linewidth=1)
    
    # Draw servo cone from first position
    cone_center_x = SCANNER_MODULE_X
    cone_center_y = y_positions[0]
    cone_radius = 30  # Visual radius for cone display    # Convert cone angles to cartesian for visualization
    # Note: COORD_MAX_ANGLE = -135°, COORD_MIN_ANGLE = -45° (rotated 180°)
    angle1_rad = math.radians(COORD_MAX_ANGLE + 90)  # -135° + 90° = -45° (upper boundary)
    angle2_rad = math.radians(COORD_MIN_ANGLE + 90)  # -45° + 90° = 45° (lower boundary)
    
    # Create cone visualization
    cone_x1 = cone_center_x + cone_radius * math.cos(angle1_rad)
    cone_y1 = cone_center_y + cone_radius * math.sin(angle1_rad)
    cone_x2 = cone_center_x + cone_radius * math.cos(angle2_rad)
    cone_y2 = cone_center_y + cone_radius * math.sin(angle2_rad)
    
    # Draw cone boundaries
    ax1.plot([cone_center_x, cone_x1], [cone_center_y, cone_y1], 'purple', linewidth=2, alpha=0.8)
    ax1.plot([cone_center_x, cone_x2], [cone_center_y, cone_y2], 'purple', linewidth=2, alpha=0.8)
    
    # Fill cone area
    theta = np.linspace(angle1_rad, angle2_rad, 50)
    cone_x = cone_center_x + cone_radius * np.cos(theta)
    cone_y = cone_center_y + cone_radius * np.sin(theta)
    cone_x = np.append([cone_center_x], cone_x)
    cone_y = np.append([cone_center_y], cone_y)
    ax1.fill(cone_x, cone_y, color='purple', alpha=0.2, label=f'Servo Cone ({COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°)')
    
    ax1.set_xlabel('X Position (cm)', fontweight='bold')
    ax1.set_ylabel('Y Position (cm)', fontweight='bold')
    ax1.set_title('Servo Cone and Reachable Area', fontweight='bold', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_aspect('equal')
    
    # === SUBPLOT 2: Angle Progression ===
    ax2 = plt.subplot(2, 2, 2)
    
    points = [data['point'] for data in servo_data]
    geometric_angles = [data['geometric_angle'] for data in servo_data]
    servo_coordinate_angles = [data['servo_coordinate_angle'] for data in servo_data]
    servo_physical_angles = [data['servo_angle'] for data in servo_data]
    
    ax2.plot(points, geometric_angles, 'b-o', label='Geometric Angle', linewidth=2, markersize=6)
    ax2.plot(points, servo_coordinate_angles, 'g-s', label='Servo Coordinate Angle', linewidth=2, markersize=6)
    ax2.plot(points, servo_physical_angles, 'r-^', label='Physical Servo Angle', linewidth=2, markersize=6)
    
    # Add horizontal lines for servo limits
    ax2.axhline(y=COORD_MIN_ANGLE, color='purple', linestyle='--', alpha=0.7, label=f'Servo Limit {COORD_MIN_ANGLE}°')
    ax2.axhline(y=COORD_MAX_ANGLE, color='purple', linestyle='--', alpha=0.7, label=f'Servo Limit {COORD_MAX_ANGLE}°')
    ax2.axhline(y=SERVO_MIN_ANGLE, color='orange', linestyle=':', alpha=0.7, label=f'Physical Limit {SERVO_MIN_ANGLE}°')
    ax2.axhline(y=SERVO_MAX_ANGLE, color='orange', linestyle=':', alpha=0.7, label=f'Physical Limit {SERVO_MAX_ANGLE}°')
    
    ax2.set_xlabel('Measurement Point', fontweight='bold')
    ax2.set_ylabel('Angle (degrees)', fontweight='bold')
    ax2.set_title('Angle Progression: Geometric → Servo', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8)
    
    # === SUBPLOT 3: Servo Mapping Diagram ===
    ax3 = plt.subplot(2, 2, 3)
    
    # Create servo mapping visualization
    coord_angles = np.linspace(COORD_MIN_ANGLE, COORD_MAX_ANGLE, 100)
    physical_angles = []
    
    for coord_angle in coord_angles:
        # Map coordinate angle to physical angle
        servo_range = COORD_MAX_ANGLE - COORD_MIN_ANGLE
        physical_range = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE
        normalized = (coord_angle - COORD_MIN_ANGLE) / servo_range
        physical_angle = SERVO_MIN_ANGLE + (normalized * physical_range)
        physical_angles.append(physical_angle)
    
    ax3.plot(coord_angles, physical_angles, 'b-', linewidth=3, label='Coordinate → Physical Mapping')
    
    # Plot actual measurement points
    for data in servo_data:
        color = 'green' if data['is_reachable'] else 'red'
        marker = 'o' if data['is_reachable'] else 'x'
        ax3.plot(data['servo_coordinate_angle'], data['servo_angle'], 
                color=color, marker=marker, markersize=8, 
                label=f'Point {data["point"]}' if data['point'] <= 3 else "")
    
    ax3.set_xlabel('Servo Coordinate Angle (degrees)', fontweight='bold')
    ax3.set_ylabel('Physical Servo Angle (degrees)', fontweight='bold')
    ax3.set_title('Servo Angle Mapping', fontweight='bold', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=8)
    
    # === SUBPLOT 4: Reachability Analysis ===
    ax4 = plt.subplot(2, 2, 4)
    
    # Create reachability chart
    reachable_points = [data['point'] for data in servo_data if data['is_reachable']]
    unreachable_points = [data['point'] for data in servo_data if not data['is_reachable']]
    
    reachable_y = [data['y_pos'] for data in servo_data if data['is_reachable']]
    unreachable_y = [data['y_pos'] for data in servo_data if not data['is_reachable']]
    
    if reachable_points:
        ax4.bar(reachable_points, [1]*len(reachable_points), color='green', alpha=0.7, label='Reachable')
    if unreachable_points:
        ax4.bar(unreachable_points, [1]*len(unreachable_points), color='red', alpha=0.7, label='Unreachable')
    
    # Add text annotations
    for data in servo_data:
        ax4.text(data['point'], 0.5, f"{data['servo_angle']:.1f}°", 
                ha='center', va='center', fontweight='bold', fontsize=8)
    
    ax4.set_xlabel('Measurement Point', fontweight='bold')
    ax4.set_ylabel('Reachability', fontweight='bold')
    ax4.set_title('Servo Reachability Analysis', fontweight='bold', fontsize=12)
    ax4.set_ylim(0, 1.2)
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.legend()
    
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
    ax.plot(servo_x, servo_y, 'ko', markersize=12, label='Servo Position')
      # Draw servo cone
    cone_radius = 5
    angle1_rad = math.radians(COORD_MAX_ANGLE + 90)  # Convert to standard math coordinates (-135° + 90° = -45°)
    angle2_rad = math.radians(COORD_MIN_ANGLE + 90)  # (-45° + 90° = 45°)
      # Cone boundaries
    cone_x1 = servo_x + cone_radius * math.cos(angle1_rad)
    cone_y1 = servo_y + cone_radius * math.sin(angle1_rad)
    cone_x2 = servo_x + cone_radius * math.cos(angle2_rad)
    cone_y2 = servo_y + cone_radius * math.sin(angle2_rad)
    
    ax.plot([servo_x, cone_x1], [servo_y, cone_y1], 'purple', linewidth=3, label=f'{COORD_MAX_ANGLE}° Limit')
    ax.plot([servo_x, cone_x2], [servo_y, cone_y2], 'purple', linewidth=3, label=f'{COORD_MIN_ANGLE}° Limit')
    
    # Fill cone
    theta = np.linspace(angle1_rad, angle2_rad, 50)
    cone_x = servo_x + cone_radius * np.cos(theta)
    cone_y = servo_y + cone_radius * np.sin(theta)
    cone_x = np.append([servo_x], cone_x)
    cone_y = np.append([servo_y], cone_y)
    ax.fill(cone_x, cone_y, color='purple', alpha=0.3, label='Servo Reachable Cone')
    
    # Draw neutral position (45° from Y-axis)
    neutral_rad = math.radians(45 + 90)  # 45° from Y-axis = 135° in math coordinates
    neutral_x = servo_x + cone_radius * 0.7 * math.cos(neutral_rad)
    neutral_y = servo_y + cone_radius * 0.7 * math.sin(neutral_rad)
    ax.plot([servo_x, neutral_x], [servo_y, neutral_y], 'orange', linewidth=3, linestyle='--', label='Neutral Position (45°)')
      # Add angle annotations
    ax.annotate(f'{COORD_MAX_ANGLE}°', xy=(cone_x1, cone_y1), xytext=(cone_x1-1, cone_y1-0.5),
                fontsize=12, fontweight='bold', color='purple')
    ax.annotate(f'{COORD_MIN_ANGLE}°', xy=(cone_x2, cone_y2), xytext=(cone_x2+0.5, cone_y2+0.5),
                fontsize=12, fontweight='bold', color='purple')
    ax.annotate('45°', xy=(neutral_x, neutral_y), xytext=(neutral_x+0.5, neutral_y-0.5),
                fontsize=12, fontweight='bold', color='orange')
    
    # Add coordinate system labels
    ax.text(6, 0.2, '+X', fontsize=12, fontweight='bold')
    ax.text(0.2, 6, '+Y', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_xlabel('X Coordinate', fontweight='bold')
    ax.set_ylabel('Y Coordinate', fontweight='bold')
    ax.set_title('Servo Motor Cone Concept\n(Rotated 45° from Y-axis)', fontweight='bold', fontsize=14)
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
