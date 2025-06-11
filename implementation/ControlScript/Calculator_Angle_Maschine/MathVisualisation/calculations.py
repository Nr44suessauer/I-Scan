#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULATION MODULE FOR GEOMETRIC ANGLE CALCULATION
==================================================

Contains pure geometric calculations for the 3D scanner angles.
Only trigonometric calculations - no servo interpolation.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 3.0 (Pure geometry implementation)
"""

import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS
)


def print_step_by_step_explanation():
    """
    Prints a detailed step-by-step explanation of the pure geometric calculation
    and returns the calculated angles data for visualization
    """
    print("=" * 80)
    print("   GEOMETRIC ANGLE CALCULATION FOR 3D SCANNER")
    print("=" * 80)
    print()
    
    print("🎯 PROBLEM:")
    print("   A 3D scanner moves vertically and must always point at a")
    print("   target object. Calculate the geometric angles using trigonometry.")
    print("   The angle is between the line from scanner to target and the Y-axis.")
    print()
    
    print("📊 SETUP:")
    print(f"   • Scanner starts at: ({SCANNER_MODULE_X}, {SCANNER_MODULE_Y}) cm")
    print(f"   • Target object is at: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm")
    print(f"   • Scanner moves {SCAN_DISTANCE} cm vertically")
    print(f"   • {NUMBER_OF_MEASUREMENTS} measurement points are calculated")
    print("   • Using pure trigonometric calculations")
    print()
    
    # Step 1: Calculate step size
    step_size = SCAN_DISTANCE / (NUMBER_OF_MEASUREMENTS - 1)
    print("📏 STEP 1: Calculate step size")
    print("   " + "-" * 45)
    print(f"   Formula: Step size = Total distance ÷ (Number of measurements - 1)")
    print(f"   Step size = {SCAN_DISTANCE} cm ÷ ({NUMBER_OF_MEASUREMENTS} - 1)")
    print(f"   Step size = {step_size:.2f} cm")
    print(f"   → Each measurement point is {step_size:.2f} cm apart")
    print("   → This ensures the last measurement is at the full scan distance")
    print()
    
    # Step 2: Trigonometry for each point
    print("🧮 STEP 2: Geometric angle calculation for each measurement point")
    print("   " + "-" * 65)
    print()
    
    angles = []
    for i in range(NUMBER_OF_MEASUREMENTS):
        y_position = i * step_size
        
        print(f"   📍 MEASUREMENT POINT {i+1} (Y = {y_position} cm):")
        print("   " + "~" * 35)
          # Calculate triangle sides
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - y_position  # Keep direction: positive when target is above scanner
        
        print(f"   • Horizontal distance (dx): {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm")
        print(f"   • Vertical distance (dy): {TARGET_CENTER_Y} - {y_position} = {dy} cm")
        
        # Geometric angle calculation using trigonometry
        if dx > 0.001 and abs(dy) > 0.001:  # Avoid division by zero
            # Angle between line (scanner to target) and Y-axis
            angle_rad = math.atan2(dx, dy)  # Use atan2 for proper quadrant handling
            angle_deg = angle_rad * 180 / math.pi
        elif abs(dy) <= 0.001:  # Horizontal line
            angle_deg = 90.0
        else:  # dx = 0, vertical line
            angle_deg = 0.0
        
        print(f"   • Geometric angle = arctan(dx/dy) = arctan({dx}/{dy:.1f}) = {angle_deg:.2f}°")
        print(f"   • (Angle relative to Y-axis)")
        
        # Calculate hypotenuse for reference
        hypotenuse = math.sqrt(dx*dx + dy*dy)
        print(f"   • Distance to target = √(dx² + dy²) = √({dx}² + {dy:.1f}²) = {hypotenuse:.2f} cm")
        
        angles.append({
            'point': i+1,
            'y_pos': y_position,
            'dx': dx,
            'dy': dy,
            'angle': angle_deg,
            'hypotenuse': hypotenuse
        })
        
        print()
    
    print("📋 SUMMARY OF ALL CALCULATED ANGLES:")
    print("   " + "-" * 60)
    print("   Point | Y-Pos | dx   | dy   | Angle° | Distance")
    print("   ------|-------|------|------|--------|----------")
    for angle in angles:
        print(f"     {angle['point']}   | {angle['y_pos']:5.1f} | {angle['dx']:4.0f} | {angle['dy']:4.1f} | {angle['angle']:6.2f} | {angle['hypotenuse']:8.2f}")
    
    print()
    print("✅ GEOMETRIC CALCULATION COMPLETED!")
    print("   The angles show the pure geometric relationship.")
    print("   Angles are measured from Y-axis to scanner-target line.")
    print()
    
    return angles


def calculate_geometric_angles():
    """
    Performs geometric angle calculations without printing explanations.
    Returns the calculated angles data for programmatic use.
    """
    step_size = SCAN_DISTANCE / (NUMBER_OF_MEASUREMENTS - 1)
    angles = []
    
    for i in range(NUMBER_OF_MEASUREMENTS):
        y_position = i * step_size
          # Calculate triangle sides
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - y_position  # Keep direction: positive when target is above scanner
        
        # Geometric angle calculation using trigonometry
        if dx > 0.001 and abs(dy) > 0.001:  # Avoid division by zero
            # Angle between line (scanner to target) and Y-axis
            angle_rad = math.atan2(dx, dy)  # Use atan2 for proper quadrant handling
            angle_deg = angle_rad * 180 / math.pi
        elif abs(dy) <= 0.001:  # Horizontal line
            angle_deg = 90.0
        else:  # dx = 0, vertical line
            angle_deg = 0.0
        
        # Calculate hypotenuse
        hypotenuse = math.sqrt(dx*dx + dy*dy)
        
        angles.append({
            'point': i+1,
            'y_pos': y_position,
            'dx': dx,
            'dy': dy,
            'angle': angle_deg,
            'hypotenuse': hypotenuse
        })
    
    return angles


# Backward compatibility aliases
def calculate_servo_angles():
    """Legacy function name - redirects to geometric angle calculation"""
    return calculate_geometric_angles()