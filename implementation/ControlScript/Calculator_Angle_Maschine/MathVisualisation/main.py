#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN COORDINATION MODULE FOR SERVO ANGLE EXPLANATION
====================================================

Main entry point that coordinates the complete servo angle explanation and visualization.
This module orchestrates the calculation and visualization components.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

from calculations import print_step_by_step_explanation
from visualizations import (
    create_geometric_visualization,
    create_angle_progression_visualization,
    create_trigonometry_formulas_visualization,
    create_point_calculation_visualization,
    create_calculation_table_visualization,
    create_complete_visualization
)


def main():
    """
    Main function - executes complete explanation and visualization
    """
    print("\n🚀 STARTING COMPLETE SERVO ANGLE EXPLANATION...\n")
    
    # Step 1: Mathematical explanation
    angles_data = print_step_by_step_explanation()
    
    print("🎨 CREATING VISUALIZATIONS...")
    print("   Please wait while diagrams are being generated...")
    
    # Step 2: Create individual visualizations
    create_geometric_visualization(angles_data)
    create_angle_progression_visualization(angles_data)
    create_trigonometry_formulas_visualization()
    
    # Create individual point calculations
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    
    # Step 3: Create complete visualization
    create_complete_visualization(angles_data)
    
    print("\n✅ COMPLETE ANALYSIS FINISHED!")
    print("   • Mathematical calculation explained")
    print("   • Individual visualizations created:")
    print("     - 01_geometric_representation.png")
    print("     - 02_angle_progression.png")
    print("     - 03_trigonometry_formulas.png")
    print("     - 04_point_1_calculation.png")
    print("     - 04_point_2_calculation.png")
    print("     - 04_point_3_calculation.png")
    print("     - 04_point_4_calculation.png")
    print("     - 05_calculation_table.png")
    print("     - 06_complete_servo_angle_visualization.png")
    print("   • Servo angles ready for hardware implementation")
    print("\n" + "="*80)


def main_silent():
    """
    Silent version of main function - only creates visualizations without explanation text
    """
    from calculations import calculate_servo_angles
    
    print("🎨 Creating servo angle visualizations...")
    
    # Calculate angles without explanations
    angles_data = calculate_servo_angles()
    
    # Create all visualizations
    create_geometric_visualization(angles_data)
    create_angle_progression_visualization(angles_data)
    create_trigonometry_formulas_visualization()
    
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    create_complete_visualization(angles_data)
    
    print("✅ All visualizations created successfully!")
    return angles_data


def get_servo_angles():
    """
    Returns calculated servo angles without creating visualizations or explanations
    """
    from calculations import calculate_servo_angles
    return calculate_servo_angles()


if __name__ == "__main__":
    main()
