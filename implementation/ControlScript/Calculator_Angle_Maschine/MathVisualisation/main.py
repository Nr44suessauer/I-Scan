#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN COORDINATION MODULE FOR GEOMETRIC ANGLE EXPLANATION
========================================================

Main entry point that coordinates the complete geometric angle explanation and visualization.
This module orchestrates the calculation and visualization components for pure geometric calculations.

Author: I-Scan Team
Version: 3.0 (Pure geometry implementation)
"""

from calculations import print_step_by_step_explanation
from servo_interpolation import print_servo_interpolation_explanation
from visualizations import (
    create_geometric_visualization,
    # create_angle_progression_visualization,  # Temporarily disabled
    create_trigonometry_formulas_visualization,
    create_point_calculation_visualization,
    create_calculation_table_visualization,
    # create_complete_visualization  # Temporarily disabled
)
from visualizations.servo_interpolation import (
    save_servo_interpolation_visualization,
    save_servo_cone_detail
)


def main():
    """
    Main function - executes complete explanation and visualization including servo interpolation
    """
    print("\n🚀 STARTING COMPLETE GEOMETRIC ANGLE AND SERVO INTERPOLATION EXPLANATION...\n")
    
    # Step 1: Mathematical explanation for geometric angles
    angles_data = print_step_by_step_explanation()
    
    # Step 2: Servo interpolation explanation
    print("\n" + "="*80)
    servo_data = print_servo_interpolation_explanation()
    
    print("🎨 CREATING VISUALIZATIONS...")
    print("   Please wait while diagrams are being generated...")
    
    # Step 3: Create geometric visualizations
    create_geometric_visualization(angles_data)
    # create_angle_progression_visualization(angles_data)  # Temporarily disabled
    create_trigonometry_formulas_visualization()
    
    # Create individual point calculations
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    
    # Step 4: Create servo interpolation visualizations
    save_servo_interpolation_visualization()
    save_servo_cone_detail()
    
    # Step 5: Create complete visualization
    # create_complete_visualization(angles_data)  # Temporarily disabled    
    print("\n✅ COMPLETE ANALYSIS FINISHED!")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    print("   • Individual visualizations created:")
    print("     - 01_geometric_representation.png")
    print("     - 02_angle_progression.png")
    print("     - 03_trigonometry_formulas.png")
    print("     - 04_point_1_calculation.png")
    print("     - 04_point_2_calculation.png")
    print("     - 04_point_3_calculation.png")
    print("     - 04_point_4_calculation.png")
    print("     - 05_calculation_table.png")
    print("     - 06_servo_interpolation.png")
    print("     - 07_servo_cone_detail.png")
    print("   • Geometric angles and servo interpolation ready for implementation")
    print("\n" + "="*80)


def main_silent():
    """
    Silent version of main function - only creates visualizations without explanation text
    """
    from calculations import calculate_geometric_angles
    from servo_interpolation import calculate_servo_interpolation
    
    print("🎨 Creating geometric angle and servo interpolation visualizations...")
    
    # Calculate angles without explanations
    angles_data = calculate_geometric_angles()
    servo_data = calculate_servo_interpolation()
    
    # Create all visualizations
    create_geometric_visualization(angles_data)
    # create_angle_progression_visualization(angles_data)  # Temporarily disabled
    create_trigonometry_formulas_visualization()
    
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    
    # Create servo visualizations
    save_servo_interpolation_visualization()
    save_servo_cone_detail()
    
    # create_complete_visualization(angles_data)  # Temporarily disabled
    
    print("✅ All visualizations created successfully!")
    return angles_data, servo_data


def get_geometric_angles():
    """
    Returns calculated geometric angles without creating visualizations or explanations
    """
    from calculations import calculate_geometric_angles
    return calculate_geometric_angles()


def get_servo_angles():
    """
    Returns calculated servo interpolation data without creating visualizations or explanations
    """
    from servo_interpolation import calculate_servo_interpolation
    return calculate_servo_interpolation()


# Backward compatibility aliases
def main_servo():
    """Legacy function name - redirects to main calculation including servo interpolation"""
    return main()


if __name__ == "__main__":
    main()
