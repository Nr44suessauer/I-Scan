#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN COORDINATION MODULE FOR GEOMETRIC ANGLE EXPLANATION
========================================================

Main entry point that coordinates the complete geometric angle explanation and visualization.
This module orchestrates the calculation and visualization components for pure geometric calculations.

Author: I-Scan Team
Version: 3.0 (Pure geometry implementation with Add-on support)
"""

from calculations import print_step_by_step_explanation
from servo_interpolation import print_servo_interpolation_explanation, print_detailed_reachability_table
from config import ENABLE_VISUALIZATIONS, VISUALIZATION_SETTINGS
from visualizations import (
    create_geometric_visualization,
    create_angle_progression_visualization,
    create_trigonometry_formulas_visualization,
    create_point_calculation_visualization,
    create_calculation_table_visualization,
)
from visualizations.servo_interpolation import (
    save_servo_interpolation_visualization,
    save_servo_cone_detail
)

# Optional add-on imports
try:
    from addons import TARGET_COORD_ADDON_AVAILABLE
    if TARGET_COORD_ADDON_AVAILABLE:
        from addons.target_coord_angle_explanation import save_target_coord_angle_visualization
    else:
        save_target_coord_angle_visualization = None
except ImportError:
    TARGET_COORD_ADDON_AVAILABLE = False
    save_target_coord_angle_visualization = None
    print("⚠️ Add-ons package not available - target coordinate explanation will be skipped")


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
    
    # Step 2.5: Detailed reachability analysis
    print("\n" + "="*80)
    print_detailed_reachability_table()
    
    print("🎨 CREATING VISUALIZATIONS...")
    print("   Please wait while diagrams are being generated...")
    
    # Step 3: Create visualizations based on configuration
    visualization_count = 0
    
    # Core geometric visualizations (01-05)
    if ENABLE_VISUALIZATIONS['geometric_representation']:
        create_geometric_visualization(angles_data)
        visualization_count += 1
        print("📊 Geometric visualization saved: output\\01_geometric_representation.png")
        print("   ✅ 01_geometric_representation.png")
    
    if ENABLE_VISUALIZATIONS['angle_progression']:
        create_angle_progression_visualization(angles_data)
        visualization_count += 1
        print("📊 Angle progression visualization saved: output\\02_angle_progression.png")
        print("   ✅ 02_angle_progression.png")
    
    if ENABLE_VISUALIZATIONS['trigonometry_formulas']:
        create_trigonometry_formulas_visualization()
        visualization_count += 1
        print("📊 Trigonometry formulas visualization saved: output\\03_trigonometry_formulas.png")
        print("   ✅ 03_trigonometry_formulas.png")
    
    if ENABLE_VISUALIZATIONS['point_calculations'] and VISUALIZATION_SETTINGS['save_individual_point_calculations']:
        for i, point_data in enumerate(angles_data):
            create_point_calculation_visualization(point_data, i + 1)
            visualization_count += 1
        print("📊 Point calculation visualizations saved: output\\04_point_X_calculation.png")
        print("   ✅ 04_point_1-6_calculation.png (6 files)")
    
    if ENABLE_VISUALIZATIONS['calculation_table']:
        create_calculation_table_visualization(angles_data)
        visualization_count += 1
        print("📊 Calculation table visualization saved: output\\05_calculation_table.png")
        print("   ✅ 05_calculation_table.png")
    
    # Advanced servo and coordinate analysis (06-08)
    if ENABLE_VISUALIZATIONS['servo_interpolation']:
        save_servo_interpolation_visualization()
        visualization_count += 1
        print("🎨 Creating servo interpolation visualization...")
        print("✅ Servo interpolation visualization saved: output/06_servo_interpolation.png")
        print("   ✅ 06_servo_interpolation.png")
    
    if ENABLE_VISUALIZATIONS['servo_cone_detail']:
        save_servo_cone_detail()
        visualization_count += 1
        print("🎨 Creating servo cone detail visualization...")
        print("✅ Servo cone detail visualization saved: output/07_servo_cone_detail.png")
        print("   ✅ 07_servo_cone_detail.png")
    
    # Add-on features (08+)
    if ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        if TARGET_COORD_ADDON_AVAILABLE and save_target_coord_angle_visualization:
            save_target_coord_angle_visualization()
            visualization_count += 1
            print("   ✅ 08_target_coord_angle_explanation.png (Add-on)")
        else:
            print("   ⚠️ 08_target_coord_angle_explanation.png (Add-on not available)")
    
    print(f"\n✅ COMPLETE ANALYSIS FINISHED! ({visualization_count} visualizations created)")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    if TARGET_COORD_ADDON_AVAILABLE and ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        print("   • Target coordinate angle explanation included (Add-on)")
    print("   • Geometric angles and servo interpolation ready for implementation")
    print(f"   • Configuration: {sum(ENABLE_VISUALIZATIONS.values())}/{len(ENABLE_VISUALIZATIONS)} visualizations enabled")
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
    
    # Create visualizations based on configuration
    visualization_count = 0
    
    if ENABLE_VISUALIZATIONS['geometric_representation']:
        create_geometric_visualization(angles_data)
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['angle_progression']:
        create_angle_progression_visualization(angles_data)
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['trigonometry_formulas']:
        create_trigonometry_formulas_visualization()
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['point_calculations'] and VISUALIZATION_SETTINGS['save_individual_point_calculations']:
        for i, point_data in enumerate(angles_data):
            create_point_calculation_visualization(point_data, i + 1)
            visualization_count += 6
    
    if ENABLE_VISUALIZATIONS['calculation_table']:
        create_calculation_table_visualization(angles_data)
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['servo_interpolation']:
        save_servo_interpolation_visualization()
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['servo_cone_detail']:
        save_servo_cone_detail()
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        if TARGET_COORD_ADDON_AVAILABLE and save_target_coord_angle_visualization:
            save_target_coord_angle_visualization()
            visualization_count += 1
        # Silent mode - no warning messages
    
    print(f"✅ {visualization_count} visualizations created successfully!")
    return angles_data, servo_data


def get_servo_angles():
    """
    Returns only the servo angles for integration with other systems
    """
    from calculations import calculate_geometric_angles
    angles_data = calculate_geometric_angles()
    return [point_data['servo_angle'] for point_data in angles_data]


if __name__ == "__main__":
    """Run complete explanation when executed directly"""
    main()
