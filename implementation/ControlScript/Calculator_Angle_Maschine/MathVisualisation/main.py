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
from visualizations import (
    create_geometric_visualization,
    # create_angle_progression_visualization,  # Temporarily disabled
    create_trigonometry_formulas_visualization,
    create_point_calculation_visualization,
    create_calculation_table_visualization,
    # create_complete_visualization  # Temporarily disabled
)


def main():
    """
    Main function - executes complete explanation and visualization
    """
    print("\n🚀 STARTING COMPLETE GEOMETRIC ANGLE EXPLANATION...\n")
    
    # Step 1: Mathematical explanation
    angles_data = print_step_by_step_explanation()
    
    print("🎨 CREATING VISUALIZATIONS...")
    print("   Please wait while diagrams are being generated...")
      # Step 2: Create individual visualizations
    create_geometric_visualization(angles_data)
    # create_angle_progression_visualization(angles_data)  # Temporarily disabled
    create_trigonometry_formulas_visualization()
    
    # Create individual point calculations
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    
    # Step 3: Create complete visualization
    # create_complete_visualization(angles_data)  # Temporarily disabled
    
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
    print("     - 06_complete_geometric_angle_visualization.png")
    print("   • Geometric angles ready for implementation")
    print("\n" + "="*80)


def main_silent():
    """
    Silent version of main function - only creates visualizations without explanation text
    """
    from calculations import calculate_geometric_angles
    
    print("🎨 Creating geometric angle visualizations...")
    
    # Calculate angles without explanations
    angles_data = calculate_geometric_angles()
      # Create all visualizations
    create_geometric_visualization(angles_data)
    # create_angle_progression_visualization(angles_data)  # Temporarily disabled
    create_trigonometry_formulas_visualization()
    
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    # create_complete_visualization(angles_data)  # Temporarily disabled
    
    print("✅ All visualizations created successfully!")
    return angles_data


def get_geometric_angles():
    """
    Returns calculated geometric angles without creating visualizations or explanations
    """
    from calculations import calculate_geometric_angles
    return calculate_geometric_angles()


# Backward compatibility aliases
def main_servo():
    """Legacy function name - redirects to main geometric calculation"""
    return main()

def get_servo_angles():
    """Legacy function name - redirects to geometric angle calculation"""
    return get_geometric_angles()


if __name__ == "__main__":
    main()



# ALTERNATIVE CONFIGURATION WITH BASE_SERVO_ANGLE = 45°
BASE_SERVO_ANGLE = 45    # Basis-Servowinkel für Approximation (Grad) - wird als MIN_SERVO_ANGLE verwendet
MIN_SERVO_ANGLE = 90     # Minimaler Servowinkel bei Y=0 (Grad)
MAX_SERVO_ANGLE = 0      # Maximaler Servowinkel bei Y=max (Grad) - für rückwärts Interpolation
USE_APPROXIMATION = True # Verwende lineare Interpolation 90°-0° statt exakter Berechnung
