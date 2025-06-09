#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVO INTERPOLATION MODULE FOR 3D SCANNER
==========================================

Calculates servo motor angles based on geometric calculations.
The servo is mounted at 45° to the Y-axis and parallel to the X-axis, then rotated 180°.

Servo Configuration:
- Physical range: 0° to 90°
- At 45°: perpendicular to Y-axis, parallel to X-axis
- Coordinate system range: -135° to -45° (rotated by 225° total)

Author: I-Scan Team
Version: 1.0 (Servo interpolation implementation - corrected 180° rotation)
"""

import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS,
    SERVO_MIN_ANGLE, SERVO_MAX_ANGLE, SERVO_NEUTRAL_ANGLE,
    COORD_MIN_ANGLE, COORD_MAX_ANGLE
)
from calculations import calculate_geometric_angles


def calculate_servo_interpolation():
    """
    Calculate servo angles for each measurement point based on geometric angles.
    
    Returns:
        list: List of dictionaries containing servo interpolation data
    """
    # Get geometric angles
    geometric_angles = calculate_geometric_angles()
    
    servo_data = []
    
    for angle_data in geometric_angles:
        geometric_angle = angle_data['angle']
        
        # Convert geometric angle to servo coordinate system
        # The servo is rotated 45° from the Y-axis, then 180° (total transformation)
        servo_coordinate_angle = geometric_angle + 45.0 + 180.0
        
        # Normalize angle to -180° to +180° range
        while servo_coordinate_angle > 180.0:
            servo_coordinate_angle -= 360.0
        while servo_coordinate_angle < -180.0:
            servo_coordinate_angle += 360.0
        
        # Check if angle is in reachable range (-135° to -45°)
        is_reachable = (servo_coordinate_angle >= COORD_MAX_ANGLE and 
                       servo_coordinate_angle <= COORD_MIN_ANGLE)
        
        # Clamp to servo range in coordinate system
        if servo_coordinate_angle < COORD_MAX_ANGLE:
            servo_coordinate_angle = COORD_MAX_ANGLE
        elif servo_coordinate_angle > COORD_MIN_ANGLE:
            servo_coordinate_angle = COORD_MIN_ANGLE
        
        # Map from coordinate system (-135° to -45°) to servo range (0° to 90°)
        # Linear interpolation: -135° → 0°, -45° → 90°
        servo_range = COORD_MIN_ANGLE - COORD_MAX_ANGLE  # 90°
        physical_range = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE  # 90°
        
        # Normalize coordinate angle to 0-1 range
        normalized_angle = (servo_coordinate_angle - COORD_MAX_ANGLE) / servo_range
        
        # Map to physical servo range
        servo_angle = SERVO_MIN_ANGLE + (normalized_angle * physical_range)
        
        # Calculate cone boundaries for visualization
        cone_angle_1 = COORD_MAX_ANGLE  # -135° (upper limit)
        cone_angle_2 = COORD_MIN_ANGLE  # -45° (lower limit)
        
        servo_data.append({
            'point': angle_data['point'],
            'y_pos': angle_data['y_pos'],
            'geometric_angle': geometric_angle,
            'servo_coordinate_angle': servo_coordinate_angle,
            'servo_angle': servo_angle,
            'is_reachable': is_reachable,
            'cone_angle_1': cone_angle_1,
            'cone_angle_2': cone_angle_2,
            'dx': angle_data['dx'],
            'dy': angle_data['dy'],
            'hypotenuse': angle_data['hypotenuse']
        })
    
    return servo_data


def print_servo_interpolation_explanation():
    """
    Prints a detailed step-by-step explanation of servo interpolation calculation
    """
    print("=" * 80)
    print("   SERVO INTERPOLATION FOR 3D SCANNER")
    print("=" * 80)
    print()
    
    print("🔧 SERVO CONFIGURATION:")
    print("   The servo motor is mounted with specific constraints:")
    print(f"   • At {SERVO_NEUTRAL_ANGLE}°: perpendicular to Y-axis, parallel to X-axis")
    print(f"   • Physical range: {SERVO_MIN_ANGLE}° to {SERVO_MAX_ANGLE}°")
    print(f"   • Coordinate system range: {COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°")
    print("   • This creates a cone of possible servo positions")
    print()
    
    print("📐 SERVO INTERPOLATION CONCEPT:")
    print("   1. Take geometric angle from pure trigonometric calculation")
    print("   2. Rotate by 45° + 180° to match servo mounting orientation")
    print("   3. Check if angle is within servo cone (-135° to -45°)")
    print("   4. Map to physical servo range (0° to 90°)")
    print()
    
    # Get servo data
    servo_data = calculate_servo_interpolation()
    
    print("🧮 SERVO ANGLE CALCULATIONS:")
    print("   " + "-" * 75)
    print()
    
    for data in servo_data:
        print(f"   📍 MEASUREMENT POINT {data['point']} (Y = {data['y_pos']} cm):")
        print("   " + "~" * 45)
        print(f"   • Geometric angle: {data['geometric_angle']:.2f}°")
        print(f"   • Servo coordinate angle: {data['geometric_angle']:.2f}° + 45° + 180° = {data['servo_coordinate_angle']:.2f}°")
        print(f"   • Physical servo angle: {data['servo_angle']:.2f}°")
        print(f"   • Reachable: {'✅ Yes' if data['is_reachable'] else '❌ No'}")
        print(f"   • Distance to target: {data['hypotenuse']:.2f} cm")
        print()
    
    print("📋 SERVO INTERPOLATION SUMMARY:")
    print("   " + "-" * 60)
    print("   Point | Y-Pos | Geom° | Servo° | Phys° | Reach")
    print("   ------|-------|-------|--------|-------|-------")
    for data in servo_data:
        reach_symbol = "✅" if data['is_reachable'] else "❌"
        print(f"     {data['point']}   | {data['y_pos']:5.1f} | {data['geometric_angle']:5.1f} | {data['servo_coordinate_angle']:6.1f} | {data['servo_angle']:5.1f} | {reach_symbol}")
    
    print()
    print("🎯 SERVO CONE ANALYSIS:")
    print(f"   • Servo cone spans from {COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°")
    print(f"   • This is a {COORD_MIN_ANGLE - COORD_MAX_ANGLE}° cone centered around the servo axis")
    print("   • Points outside this cone cannot be reached by the servo")
    print()
    print("✅ SERVO INTERPOLATION COMPLETED!")
    print()
    
    return servo_data


def get_servo_cone_boundaries(z_module_pos):
    """
    Calculate the servo cone boundaries for a given Z-module position
    
    Args:
        z_module_pos: Y-position of the Z-module (scanner)
    
    Returns:
        tuple: (angle1, angle2) representing the cone boundaries
    """
    return (COORD_MAX_ANGLE, COORD_MIN_ANGLE)


def map_geometric_to_servo_angle(geometric_angle):
    """
    Map a geometric angle to servo angle
    
    Args:
        geometric_angle: Angle from geometric calculation
    
    Returns:
        dict: Servo angle data
    """
    # Convert to servo coordinate system
    servo_coordinate_angle = geometric_angle + 45.0 + 180.0
    
    # Normalize angle to -180° to +180° range
    while servo_coordinate_angle > 180.0:
        servo_coordinate_angle -= 360.0
    while servo_coordinate_angle < -180.0:
        servo_coordinate_angle += 360.0
    
    # Check if angle is in reachable range (-135° to -45°)
    is_reachable = (servo_coordinate_angle >= COORD_MAX_ANGLE and 
                   servo_coordinate_angle <= COORD_MIN_ANGLE)
    
    # Clamp to servo range
    if servo_coordinate_angle < COORD_MAX_ANGLE:
        servo_coordinate_angle = COORD_MAX_ANGLE
    elif servo_coordinate_angle > COORD_MIN_ANGLE:
        servo_coordinate_angle = COORD_MIN_ANGLE
    
    # Map to physical servo range (-135° → 0°, -45° → 90°)
    servo_range = COORD_MIN_ANGLE - COORD_MAX_ANGLE  # 90°
    physical_range = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE  # 90°
    normalized_angle = (servo_coordinate_angle - COORD_MAX_ANGLE) / servo_range
    servo_angle = SERVO_MIN_ANGLE + (normalized_angle * physical_range)
    
    return {
        'geometric_angle': geometric_angle,
        'servo_coordinate_angle': servo_coordinate_angle,
        'servo_angle': servo_angle,
        'is_reachable': is_reachable
    }
