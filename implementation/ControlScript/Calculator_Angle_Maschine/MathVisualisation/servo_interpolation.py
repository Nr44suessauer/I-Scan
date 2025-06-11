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

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 1.0 (Servo interpolation implementation - corrected 180° rotation)
"""

import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS,
    SERVO_MIN_ANGLE, SERVO_MAX_ANGLE, SERVO_NEUTRAL_ANGLE,
    COORD_MIN_ANGLE, COORD_MAX_ANGLE, COORD_NEUTRAL_ANGLE
)
from calculations import calculate_geometric_angles


def calculate_servo_interpolation():
    """
    Calculate servo angles for each measurement point based on geometric angles.
    
    Returns:
        list: List of dictionaries containing servo interpolation data
    """
    # Use the corrected calculation
    return calculate_corrected_servo_interpolation()
    # Get geometric angles
    geometric_angles = calculate_geometric_angles()
    
    servo_data = []
    
    for angle_data in geometric_angles:
        geometric_angle = angle_data['angle']        # Convert geometric angle to servo coordinate system
        # The servo is rotated 45° from the Y-axis, then 180° (total transformation)
        servo_coordinate_angle = geometric_angle + 45.0 + 180.0
        
        # Normalize angle to -180° to +180° range
        while servo_coordinate_angle > 180.0:
            servo_coordinate_angle -= 360.0
        while servo_coordinate_angle < -180.0:
            servo_coordinate_angle += 360.0
        
        # Store original coordinate angle for interpolation
        original_servo_coordinate_angle = servo_coordinate_angle
        
        # Check if angle is in reachable range (-135° to -45°)
        is_reachable = (servo_coordinate_angle >= COORD_MAX_ANGLE and 
                       servo_coordinate_angle <= COORD_MIN_ANGLE)
        
        # Always perform interpolation, regardless of reachability
        # Map from coordinate system to servo range using original angle
        # We need to map the full geometric range to the full servo range
        
        # For interpolation, we use the original coordinate angle
        # Map from coordinate system (-135° to -45°) to servo range (0° to 90°)
        # Linear interpolation: -135° → 0°, -45° → 90°
        servo_range = COORD_MIN_ANGLE - COORD_MAX_ANGLE  # 90°
        physical_range = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE  # 90°
        
        # Normalize coordinate angle to 0-1 range (using original angle)
        normalized_angle = (original_servo_coordinate_angle - COORD_MAX_ANGLE) / servo_range
        
        # Map to physical servo range
        servo_angle = SERVO_MIN_ANGLE + (normalized_angle * physical_range)
        
        # Clamp servo angle to physical limits (0° to 90°) only for safety
        if servo_angle < SERVO_MIN_ANGLE:
            servo_angle = SERVO_MIN_ANGLE
        elif servo_angle > SERVO_MAX_ANGLE:
            servo_angle = SERVO_MAX_ANGLE
          # Calculate cone boundaries for visualization
        cone_angle_1 = COORD_MAX_ANGLE  # -135° (upper limit)
        cone_angle_2 = COORD_MIN_ANGLE  # -45° (lower limit)
        
        servo_data.append({
            'point': angle_data['point'],
            'y_pos': angle_data['y_pos'],
            'geometric_angle': geometric_angle,
            'servo_coordinate_angle': original_servo_coordinate_angle,
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
    print(f"   • Neutral position in coordinate system: {COORD_NEUTRAL_ANGLE}° (center of cone)")
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
    print(f"   • Neutral position at {COORD_NEUTRAL_ANGLE}° (center of cone)")
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
    
    # Store original coordinate angle for interpolation
    original_servo_coordinate_angle = servo_coordinate_angle
    
    # Check if angle is in reachable range (-135° to -45°)
    is_reachable = (servo_coordinate_angle >= COORD_MAX_ANGLE and 
                   servo_coordinate_angle <= COORD_MIN_ANGLE)
    
    # Always perform interpolation using original angle
    # Map to physical servo range (-135° → 0°, -45° → 90°)
    servo_range = COORD_MIN_ANGLE - COORD_MAX_ANGLE  # 90°
    physical_range = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE  # 90°
    normalized_angle = (original_servo_coordinate_angle - COORD_MAX_ANGLE) / servo_range
    servo_angle = SERVO_MIN_ANGLE + (normalized_angle * physical_range)
    
    # Clamp servo angle to physical limits (0° to 90°) only for safety
    if servo_angle < SERVO_MIN_ANGLE:
        servo_angle = SERVO_MIN_ANGLE
    elif servo_angle > SERVO_MAX_ANGLE:
        servo_angle = SERVO_MAX_ANGLE
    
    return {
        'geometric_angle': geometric_angle,
        'servo_coordinate_angle': original_servo_coordinate_angle,
        'servo_angle': servo_angle,
        'is_reachable': is_reachable
    }


def print_detailed_reachability_table():
    """
    Prints a detailed table showing target reachability for all measurement points
    """
    servo_data = calculate_servo_interpolation()
    
    print("=" * 80)
    print("   DETAILED TARGET REACHABILITY ANALYSIS")
    print("=" * 80)
    print()
    
    print("📊 SERVO CONE COVERAGE FOR ALL MEASUREMENT POINTS:")
    print("   The servo moves with the scanner - each position has its own cone")
    print()
    
    print("📋 COMPLETE REACHABILITY TABLE:")
    print("   " + "-" * 70)
    print("   Point | Y-Pos | Target  | Geom°  | Servo°  | Phys° | Reachable")
    print("        |  (cm) | Angle   |        |         |       |          ")
    print("   -----|-------|---------|--------|---------|-------|----------")
    
    reachable_count = 0
    unreachable_points = []
    
    for data in servo_data:
        # Calculate angle from each scanner position to target
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - data['y_pos']
        target_angle = math.degrees(math.atan2(dx, dy))
        
        reach_symbol = "✅ YES" if data['is_reachable'] else "❌ NO"
        if data['is_reachable']:
            reachable_count += 1
        else:
            unreachable_points.append({
                'point': data['point'],
                'y_pos': data['y_pos'],
                'reason': 'Outside servo cone range'
            })
        
        print(f"     {data['point']}   | {data['y_pos']:5.1f} | {target_angle:7.2f}° | {data['geometric_angle']:6.1f}° | {data['servo_coordinate_angle']:7.1f}° | {data['servo_angle']:5.1f}° | {reach_symbol}")
    
    print("   " + "-" * 70)
    print()
    
    print("🎯 SUMMARY:")
    print(f"   • Total measurement points: {len(servo_data)}")
    print(f"   • Reachable points: {reachable_count}")
    print(f"   • Unreachable points: {len(unreachable_points)}")
    print(f"   • Coverage: {(reachable_count/len(servo_data)*100):.1f}%")
    print()
    
    if unreachable_points:
        print("❌ UNREACHABLE POINTS DETAILS:")
        print("   " + "-" * 50)
        for point_info in unreachable_points:
            print(f"   • Point {point_info['point']} (Y={point_info['y_pos']}cm): {point_info['reason']}")
        print()
        
        print("💡 EXPLANATION:")
        print(f"   The servo cone spans from {COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°")
        print(f"   Target angles outside this range cannot be reached")
        print(f"   Consider adjusting:")
        print("   - Target position")
        print("   - Scanner path")
        print("   - Servo mounting angle")
    else:
        print("✅ ALL POINTS ARE REACHABLE!")
        print("   The target object can be reached from all measurement positions")
    
    print()
    return servo_data, unreachable_points


def debug_servo_calculation():
    """
    Debug function to check servo angle calculations
    """
    from calculations import calculate_geometric_angles
    
    print("🔍 DEBUG: Servo Angle Calculation Analysis")
    print("=" * 60)
    
    geometric_angles = calculate_geometric_angles()
    
    print(f"COORD_MAX_ANGLE: {COORD_MAX_ANGLE}°")
    print(f"COORD_MIN_ANGLE: {COORD_MIN_ANGLE}°")
    print(f"COORD_NEUTRAL_ANGLE: {COORD_NEUTRAL_ANGLE}°")
    print()
    
    for i, angle_data in enumerate(geometric_angles):
        geometric_angle = angle_data['angle']
        
        # Convert geometric angle to servo coordinate system
        servo_coordinate_angle = geometric_angle + 45.0 + 180.0
        
        # Normalize angle to -180° to +180° range
        while servo_coordinate_angle > 180.0:
            servo_coordinate_angle -= 360.0
        while servo_coordinate_angle < -180.0:
            servo_coordinate_angle += 360.0
        
        # Check reachability with current logic
        is_reachable_current = (servo_coordinate_angle >= COORD_MAX_ANGLE and 
                               servo_coordinate_angle <= COORD_MIN_ANGLE)
        
        print(f"Point {i+1}:")
        print(f"  Geometric angle: {geometric_angle:.2f}°")
        print(f"  Servo coord angle: {servo_coordinate_angle:.2f}°")
        print(f"  Is in range [{COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°]? {is_reachable_current}")
        print(f"  Check: {servo_coordinate_angle:.2f} >= {COORD_MAX_ANGLE} = {servo_coordinate_angle >= COORD_MAX_ANGLE}")
        print(f"  Check: {servo_coordinate_angle:.2f} <= {COORD_MIN_ANGLE} = {servo_coordinate_angle <= COORD_MIN_ANGLE}")
        print()

def debug_target_angles():
    """
    Debug function to check target angles from each scanner position
    """
    from calculations import calculate_geometric_angles
    import math
    
    print("🎯 DEBUG: Target Angles from Scanner Positions")
    print("=" * 60)
    
    # Target position
    target_x = TARGET_CENTER_X  # 50cm
    target_y = TARGET_CENTER_Y  # 25cm
    
    # Scanner position
    scanner_x = SCANNER_MODULE_X  # 0cm
    
    geometric_angles = calculate_geometric_angles()
    
    for i, angle_data in enumerate(geometric_angles):
        scanner_y = angle_data['y_pos']
        
        # Calculate vector from scanner to target
        dx = target_x - scanner_x  # Should be 50cm for all points
        dy = target_y - scanner_y  # Changes with scanner position
        
        # Calculate angle in standard coordinate system (0° = +Y direction)
        angle_to_target = math.degrees(math.atan2(dx, dy))
        
        # The geometric angle from calculations.py
        geometric_angle = angle_data['angle']
        
        print(f"Point {i+1} (Scanner Y = {scanner_y}cm):")
        print(f"  Target at: ({target_x}, {target_y})")
        print(f"  Vector: dx={dx}, dy={dy}")
        print(f"  Standard angle: {angle_to_target:.2f}°")
        print(f"  Geometric angle: {geometric_angle:.2f}°")
        print(f"  Difference: {abs(angle_to_target - geometric_angle):.2f}°")
        print()

def analyze_visual_cone():
    """
    Analyze what the visual cone boundaries should be based on target reachability
    """
    from calculations import calculate_geometric_angles
    import math
    
    print("📐 VISUAL CONE ANALYSIS")
    print("=" * 60)
    
    geometric_angles = calculate_geometric_angles()
    
    # If all points should be reachable, what should the servo cone boundaries be?
    all_servo_angles = []
    
    for i, angle_data in enumerate(geometric_angles):
        geometric_angle = angle_data['angle']
        
        # Current transformation
        servo_coordinate_angle = geometric_angle + 45.0 + 180.0
        while servo_coordinate_angle > 180.0:
            servo_coordinate_angle -= 360.0
        while servo_coordinate_angle < -180.0:
            servo_coordinate_angle += 360.0
            
        all_servo_angles.append(servo_coordinate_angle)
        
        print(f"Point {i+1}: {geometric_angle:.2f}° → {servo_coordinate_angle:.2f}°")
    
    min_angle = min(all_servo_angles)
    max_angle = max(all_servo_angles)
    
    print()
    print(f"Current servo coordinate range: {min_angle:.2f}° to {max_angle:.2f}°")
    print(f"Current config range: {COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°")
    print()
    
    if min_angle < COORD_MAX_ANGLE or max_angle > COORD_MIN_ANGLE:
        print("❌ PROBLEM: Required range exceeds configured servo cone!")
        print(f"   Required: {min_angle:.2f}° to {max_angle:.2f}°")
        print(f"   Configured: {COORD_MAX_ANGLE}° to {COORD_MIN_ANGLE}°")
        print()
        
        # Suggest new boundaries
        margin = 5.0  # Add some margin
        suggested_min = min_angle - margin
        suggested_max = max_angle + margin
        
        print(f"💡 SUGGESTED SERVO CONE BOUNDARIES:")
        print(f"   COORD_MAX_ANGLE = {suggested_min:.1f}°")
        print(f"   COORD_MIN_ANGLE = {suggested_max:.1f}°")
    else:
        print("✅ All points fit within configured servo cone!")

def debug_visual_vs_calculation():
    """
    Compare visual representation with calculations
    """
    from calculations import calculate_geometric_angles
    import math
    
    print("🔍 VISUAL vs CALCULATION ANALYSIS")
    print("=" * 60)
    
    geometric_angles = calculate_geometric_angles()
    
    for i, angle_data in enumerate(geometric_angles):
        y_pos = angle_data['y_pos']
        
        # Calculate actual angle from scanner to target in visual coordinates
        dx = TARGET_CENTER_X - SCANNER_MODULE_X  # 50 - 0 = 50
        dy = TARGET_CENTER_Y - y_pos  # 25 - y_pos
        
        # Standard math angle (0° = +X, counterclockwise)
        visual_angle = math.degrees(math.atan2(dy, dx))
        
        # Convert to "angle from Y-axis" (our geometric angle)
        geometric_angle = angle_data['angle']
        
        print(f"Point {i+1} (Y={y_pos}cm):")
        print(f"  dx={dx}, dy={dy}")
        print(f"  Visual angle (from +X): {visual_angle:.2f}°")
        print(f"  Geometric angle (from +Y): {geometric_angle:.2f}°")
        
        # Now check if this visual angle fits in the servo cone
        # Servo cone in visual coordinates: -45° to +45°
        visual_in_cone = (-45.0 <= visual_angle <= 45.0)
        print(f"  Visual angle in cone [-45° to +45°]? {visual_in_cone}")
        print()

def calculate_corrected_servo_interpolation():
    """
    Calculate servo angles with corrected physical servo mapping
    
    SERVO SYSTEM EXPLANATION:
    - Servo cone zeigt in Richtung Target Object (180° Drehung vom ursprünglichen 2./3. Quadrant)
    - Cone ist im 1./4. Quadranten: -45° bis +45° (oder 315° bis 45°)
    - SERVO_ROTATION_OFFSET = 45° bedeutet: 0° Target-Richtung = 45° Servo-Position
    - Servo 0° → -45° coordinate (4. Quadrant)
    - Servo 45° → 0° coordinate (positive X-Achse, Target-Richtung)  
    - Servo 90° → +45° coordinate (1. Quadrant)
    """
    # Get geometric angles
    geometric_angles = calculate_geometric_angles()
    
    servo_data = []
    
    for angle_data in geometric_angles:
        geometric_angle = angle_data['angle']
        y_pos = angle_data['y_pos']
        
        # Calculate target angle in standard coordinate system (0° = +X, 90° = +Y)
        dx = TARGET_CENTER_X - SCANNER_MODULE_X  # 50
        dy = TARGET_CENTER_Y - y_pos  # 25 - y_pos
        target_coord_angle = math.degrees(math.atan2(dy, dx))
        
        # Normalize to -180° to +180° range (easier for cone check)
        while target_coord_angle > 180.0:
            target_coord_angle -= 360.0
        while target_coord_angle < -180.0:
            target_coord_angle += 360.0
        
        # Check if target is within servo cone (-45° to +45° in coordinate system)
        is_reachable = (-45.0 <= target_coord_angle <= 45.0)
        
        # PHYSICAL SERVO CALCULATION:
        # Map coordinate angle (-45° to +45°) to servo angle (0° to 90°)
        if is_reachable:
            # Linear mapping: -45° → 0°, +45° → 90°
            physical_servo_angle = (target_coord_angle + 45.0) * (90.0 / 90.0)
        else:
            # Clamp to nearest boundary
            if target_coord_angle < -45.0:
                physical_servo_angle = 0.0
            else:
                physical_servo_angle = 90.0
        
        # Keep original servo coordinate system for compatibility
        servo_coordinate_angle = geometric_angle + 45.0 + 180.0
        while servo_coordinate_angle > 180.0:
            servo_coordinate_angle -= 360.0
        while servo_coordinate_angle < -180.0:
            servo_coordinate_angle += 360.0
        
        # Calculate visual angle (for display in table)
        visual_angle = math.degrees(math.atan2(dx, dy))
        
        servo_data.append({
            'point': angle_data['point'],
            'y_pos': angle_data['y_pos'],
            'geometric_angle': geometric_angle,
            'servo_coordinate_angle': servo_coordinate_angle,  # Keep for compatibility
            'servo_angle': physical_servo_angle,  # CORRECTED: actual servo control angle
            'visual_angle': visual_angle,  # Angle relative to Y-axis
            'target_coord_angle': target_coord_angle,  # Target angle in coordinate system
            'is_reachable': is_reachable,
            'cone_angle_1': -45.0,  # 4th quadrant boundary
            'cone_angle_2': 45.0,   # 1st quadrant boundary
            'dx': angle_data['dx'],
            'dy': angle_data['dy'],
            'hypotenuse': angle_data['hypotenuse']
        })
    
    return servo_data
