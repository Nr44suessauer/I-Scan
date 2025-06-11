#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN COORDINATOR MODULE WITH CSV EXPORT
=======================================

M    
    print(f"\n✅ COMPLETE ANALYSIS FINISHED! ({visualization_count} visualizations created)")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    if TARGET_COORD_ADDON_AVAILABLE and ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        print("   • Target coordinate angle explanation included (Add-on)")
    print("   • Geometric angles and servo interpolation ready for implementation")
    print(f"   • Configuration: {sum(ENABLE_VISUALIZATIONS.values())}/{len(ENABLE_VISUALIZATIONS)} visualizations enabled")
    print("\n" + "="*80) point providing multiple interfaces for the 3D scanner servo angle calculation
with integrated simple CSV export functionality.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 4.0 (Simplified with integrated CSV export)
"""

import csv
import os
import json
import math
from datetime import datetime

from config import (
    ENABLE_VISUALIZATIONS, VISUALIZATION_SETTINGS, ensure_output_dir,
    TARGET_CENTER_X, TARGET_CENTER_Y, SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, NUMBER_OF_MEASUREMENTS, OUTPUT_DIR
)
from calculations import print_step_by_step_explanation
from servo_interpolation import (
    print_servo_interpolation_explanation, 
    print_detailed_reachability_table,
    calculate_servo_interpolation
)
from visualizations.servo_interpolation import (
    save_servo_interpolation_visualization,
    save_servo_cone_detail
)

from visualizations import (
    create_geometric_visualization,
    create_angle_progression_visualization,
    create_point_calculation_visualization,
    create_calculation_table_visualization,
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


def main(create_csv=False):
    """
    Main function - executes complete explanation and visualization including servo interpolation
    
    Args:
        create_csv (bool): If True, also creates a CSV file for Software_IScan import
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
    
    # Ensure fresh output directory (delete old files and create new directory)
    ensure_output_dir()
    
    # Step 3: Create visualizations based on configuration
    visualization_count = 0
    
    # Core geometric visualizations (01-06)
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
    
    if ENABLE_VISUALIZATIONS['point_calculations'] and VISUALIZATION_SETTINGS['save_individual_point_calculations']:
        for i, point_data in enumerate(angles_data):
            create_point_calculation_visualization(point_data, i + 1)
            visualization_count += 1
        print("📊 Point calculation visualizations saved: output\\point_calculations\\04_point_X_calculation.png")
        print("   ✅ 04_point_1-10_calculation.png (in point_calculations subfolder)")
    
    if ENABLE_VISUALIZATIONS['calculation_table']:
        create_calculation_table_visualization(angles_data)
        visualization_count += 1
        print("📊 Calculation table visualization saved: output\\05_calculation_table.png")
        print("   ✅ 05_calculation_table.png")
    
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
    
    # Step 4: Create CSV if requested
    if create_csv:
        print("\n📊 CREATING SOFTWARE_ISCAN CSV FILE...")
        from export_commands import create_command_csv
        create_command_csv()
    
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
    
    print("🎨 Creating geometric angle and servo interpolation visualizations...")
    
    # Ensure fresh output directory (delete old files and create new directory)
    ensure_output_dir()
    
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
        
    if ENABLE_VISUALIZATIONS['point_calculations'] and VISUALIZATION_SETTINGS['save_individual_point_calculations']:
        for i, point_data in enumerate(angles_data):
            create_point_calculation_visualization(point_data, i + 1)
            visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['calculation_table']:
        create_calculation_table_visualization(angles_data)
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['servo_interpolation']:
        save_servo_interpolation_visualization()
        visualization_count += 1
    
    if ENABLE_VISUALIZATIONS['servo_cone_detail']:
        save_servo_cone_detail()
        visualization_count += 1
    
    # Add-on features
    if ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        if TARGET_COORD_ADDON_AVAILABLE and save_target_coord_angle_visualization:
            save_target_coord_angle_visualization()
            visualization_count += 1
    
    print(f"✅ {visualization_count} visualizations created successfully!")


def get_servo_angles():
    """
    Returns only the calculated servo angles as a list - no console output or file generation
    """
    from calculations import calculate_geometric_angles
    
    # Calculate and return only the angles
    angles_data = calculate_geometric_angles()
    return angles_data


def main_math_csv():
    """
    Mathematics and CSV only - executes calculations and exports CSV without visualizations
    Optimized for fast CSV generation without GUI overhead
    """
    print("\n🧮 STARTING MATHEMATICS-ONLY MODE WITH CSV EXPORT...\n")
    
    # Step 1: Mathematical explanation for geometric angles
    print("🔢 Calculating geometric angles...")
    angles_data = print_step_by_step_explanation()
    
    # Step 2: Servo interpolation explanation
    print("\n" + "="*80)
    print("⚙️ Calculating servo interpolation...")
    servo_data = print_servo_interpolation_explanation()
    
    # Step 2.5: Detailed reachability analysis
    print("\n" + "="*80)
    print("📋 Analyzing target reachability...")
    print_detailed_reachability_table()
    
    # Ensure output directory exists (but don't clear it for visualizations)
    ensure_output_dir()
    
    # Step 3: Create CSV file for Software_IScan
    print("\n📤 CREATING SOFTWARE_ISCAN CSV FILE...")
    from export_commands import create_command_csv
    create_command_csv()
    
    print(f"\n✅ MATHEMATICS AND CSV EXPORT COMPLETED!")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    print("   • Target reachability analyzed")
    print("   • CSV file ready for Software_IScan import")
    print("   • No visualizations created (math-only mode)")
    print("\n" + "="*80)


def main_math_silent():
    """
    Silent mathematics and CSV only - minimal output, fast execution
    For automated processing or when only CSV output is needed
    """
    from calculations import calculate_geometric_angles
    from servo_interpolation import calculate_servo_interpolation
    
    print("🔄 Silent math mode: Calculating...")
    
    # Calculate without explanations
    angles_data = calculate_geometric_angles()
    servo_data = calculate_servo_interpolation()
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Create CSV file
    from export_commands import create_command_csv
    create_command_csv()
    
    print("✅ Silent math + CSV completed!")
    return angles_data, servo_data

def show_help():
    """Show usage help for command line options"""
    print("🎯 3D SCANNER GEOMETRIC ANGLE CALCULATOR")
    print("=" * 50)
    print("USAGE:")
    print("  python main.py [OPTIONS]")
    print()
    print("OPTIONS:")
    print("  (no flags)     Full analysis with visualizations")
    print("  --csv, -c      Full analysis + CSV export")
    print("  --math, -m     Mathematics + CSV only (no visualizations)")
    print("  --silent, -s   Silent math + CSV (minimal output)")
    print("  --help, -h     Show this help")
    print()
    print("EXAMPLES:")
    print("  python main.py              # Standard full analysis")
    print("  python main.py --csv        # Full analysis + CSV")
    print("  python main.py --math       # Math + CSV only")
    print("  python main.py --silent     # Silent mode")
    print()
    print("OUTPUT:")
    print("  📁 output/")
    print("  ├─ 01-07.png (visualizations, if enabled)")
    print("  ├─ iscan_commands_*.csv (CSV export)")
    print("  └─ point_calculations/ (detail visualizations)")

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    args = sys.argv[1:]  # Remove script name
    
    # Check for flags
    create_csv = "--csv" in args or "-c" in args
    math_only = "--math" in args or "-m" in args
    silent = "--silent" in args or "-s" in args
    show_help_flag = "--help" in args or "-h" in args
    
    # Execute based on flags (priority order: help -> silent -> math -> csv -> standard)
    if show_help_flag:
        # Show command line usage help
        show_help()
    elif silent:
        # Silent mathematics and CSV only (minimal output)
        main_math_silent()
    elif math_only:
        # Mathematics and CSV only mode (no visualizations)
        main_math_csv()
    elif create_csv:
        # Full mode with CSV export
        main(create_csv=True)
    else:
        # Standard full mode (visualizations only)
        main(create_csv=False)