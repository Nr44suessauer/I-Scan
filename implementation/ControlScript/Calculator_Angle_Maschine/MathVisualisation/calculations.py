#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULATION MODULE FOR SERVO ANGLE CALCULATION
==============================================

Contains the core mathematical calculations for the 3D scanner servo angles.
Includes step-by-step explanation printing and trigonometric computations.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import math
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS, 
    ANGLE_CORRECTION_REFERENCE
)


def print_step_by_step_explanation():
    """
    Prints a detailed step-by-step explanation of the calculation
    and returns the calculated angles data for visualization
    """
    print("=" * 80)
    print("   SERVO ANGLE CALCULATION - COMPLETE EXPLANATION")
    print("=" * 80)
    print()
    
    print("🎯 PROBLEM:")
    print("   A 3D scanner moves vertically and must always point at a")
    print("   target object. For this, servo angles must be calculated.")
    print()
    
    print("📊 SETUP:")
    print(f"   • Scanner starts at: ({SCANNER_MODULE_X}, {SCANNER_MODULE_Y}) cm")
    print(f"   • Target object is at: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm") 
    print(f"   • Scanner moves {SCAN_DISTANCE} cm vertically")
    print(f"   • {NUMBER_OF_MEASUREMENTS} measurement points are calculated")
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
    print("🧮 STEP 2: Trigonometric calculation for each measurement point")
    print("   " + "-" * 65)
    print()
    
    angles = []
    for i in range(NUMBER_OF_MEASUREMENTS):
        y_position = i * step_size
        
        print(f"   📍 MEASUREMENT POINT {i+1} (Y = {y_position} cm):")
        print("   " + "~" * 35)
        
        # Calculate triangle sides
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = abs(y_position - TARGET_CENTER_Y)
        
        print(f"   • Horizontal distance (dx): {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm")
        print(f"   • Vertical distance (dy): |{y_position} - {TARGET_CENTER_Y}| = {dy} cm")
        
        # Trigonometric calculation
        if dx > 0.001:  # Avoid division by zero
            alpha_rad = math.atan(dy / dx)
            alpha_deg = alpha_rad * 180 / math.pi
            theoretical_angle = 90.0 - alpha_deg
        else:
            alpha_deg = 0.0
            theoretical_angle = 90.0
            
        print(f"   • Angle α = arctan(dy/dx) = arctan({dy}/{dx}) = {alpha_deg:.2f}°")
        print(f"   • Theoretical servo angle = 90° - α = 90° - {alpha_deg:.2f}° = {theoretical_angle:.2f}°")
        
        # Mechanical correction
        corrected_angle = theoretical_angle + (ANGLE_CORRECTION_REFERENCE - 90.0)
        print(f"   • Correction = {ANGLE_CORRECTION_REFERENCE} - 90 = {ANGLE_CORRECTION_REFERENCE - 90}°")
        print(f"   • Final servo angle = {theoretical_angle:.2f}° + {ANGLE_CORRECTION_REFERENCE - 90}° = {corrected_angle:.2f}°")
        
        angles.append({
            'point': i+1,
            'y_pos': y_position,
            'dx': dx,
            'dy': dy,
            'alpha': alpha_deg,
            'theoretical': theoretical_angle,
            'final': corrected_angle
        })
        
        print()
    
    print("📋 SUMMARY OF ALL CALCULATED ANGLES:")
    print("   " + "-" * 50)
    print("   Point | Y-Pos | dx   | dy   | α      | Theo° | Final°")
    print("   ------|-------|------|------|--------|-------|-------")
    for angle in angles:
        print(f"     {angle['point']}   | {angle['y_pos']:5.1f} | {angle['dx']:4.0f} | {angle['dy']:4.1f} | {angle['alpha']:6.2f} | {angle['theoretical']:5.1f} | {angle['final']:6.1f}")
    
    print()
    print("✅ CALCULATION COMPLETED!")
    print("   The servo angles are ready for hardware control.")
    print()
    
    return angles


def calculate_servo_angles():
    """
    Performs servo angle calculations without printing explanations.
    Returns the calculated angles data for programmatic use.
    """
    step_size = SCAN_DISTANCE / (NUMBER_OF_MEASUREMENTS - 1)
    angles = []
    
    for i in range(NUMBER_OF_MEASUREMENTS):
        y_position = i * step_size
        
        # Calculate triangle sides
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = abs(y_position - TARGET_CENTER_Y)
        
        # Trigonometric calculation
        if dx > 0.001:  # Avoid division by zero
            alpha_rad = math.atan(dy / dx)
            alpha_deg = alpha_rad * 180 / math.pi
            theoretical_angle = 90.0 - alpha_deg
        else:
            alpha_deg = 0.0
            theoretical_angle = 90.0
            
        # Mechanical correction
        corrected_angle = theoretical_angle + (ANGLE_CORRECTION_REFERENCE - 90.0)
        
        angles.append({
            'point': i+1,
            'y_pos': y_position,
            'dx': dx,
            'dy': dy,
            'alpha': alpha_deg,
            'theoretical': theoretical_angle,
            'final': corrected_angle
        })
    
    return angles
