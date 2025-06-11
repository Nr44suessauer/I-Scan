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
    print("  --servo-graph, -g  Save only servo geometry graph")
    print("  --help, -h     Show this help")
    print()
    print("CONFIGURATION OPTIONS:")
    print("  --target-x VALUE       Set target X position (cm) [default: 50]")
    print("  --target-y VALUE       Set target Y position (cm) [default: 50]")
    print("  --scanner-x VALUE      Set scanner X position (cm) [default: 0]")
    print("  --scanner-y VALUE      Set scanner Y position (cm) [default: 0]")
    print("  --scan-distance VALUE  Set scan distance (cm) [default: 100]")
    print("  --measurements VALUE   Set number of measurements [default: 10]")
    print("  --servo-min VALUE      Set servo minimum angle (°) [default: 0.0]")
    print("  --servo-max VALUE      Set servo maximum angle (°) [default: 90.0]")
    print("  --servo-neutral VALUE  Set servo neutral angle (°) [default: 45.0]")
    print("  --servo-offset VALUE   Set servo rotation offset (°) [default: 45.0]")
    print()
    print("EXAMPLES:")
    print("  python main.py --csv")
    print("  python main.py --silent --target-x 100 --target-y 75")
    print("  python main.py --math --servo-min 10 --servo-max 80")
    print("  python main.py --csv --scan-distance 80 --measurements 7")
    print()
    print("OUTPUT:")
    print("  📁 output/")
    print("  ├─ 01-07.png (visualizations, if enabled)")
    print("  ├─ iscan_commands_*.csv (CSV export)")
    print("  └─ point_calculations/ (detail visualizations)")


def parse_config_args(args):
    """Parse configuration arguments and return updated config dict"""
    config_updates = {}
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        # Configuration parameters that need values
        config_params = {
            '--target-x': 'TARGET_CENTER_X',
            '--target-y': 'TARGET_CENTER_Y', 
            '--scanner-x': 'SCANNER_MODULE_X',
            '--scanner-y': 'SCANNER_MODULE_Y',
            '--scan-distance': 'SCAN_DISTANCE',
            '--measurements': 'NUMBER_OF_MEASUREMENTS',
            '--servo-min': 'SERVO_MIN_ANGLE',
            '--servo-max': 'SERVO_MAX_ANGLE',
            '--servo-neutral': 'SERVO_NEUTRAL_ANGLE',
            '--servo-offset': 'SERVO_ROTATION_OFFSET'
        }
        
        if arg in config_params:
            if i + 1 < len(args):
                try:
                    value = float(args[i + 1])
                    # NUMBER_OF_MEASUREMENTS should be int
                    if config_params[arg] == 'NUMBER_OF_MEASUREMENTS':
                        value = int(value)
                    config_updates[config_params[arg]] = value
                    i += 2  # Skip the value argument
                except ValueError:
                    print(f"⚠️ Invalid value for {arg}: {args[i + 1]}")
                    i += 1
            else:
                print(f"⚠️ Missing value for {arg}")
                i += 1
        else:
            i += 1
    
    return config_updates


def apply_config_overrides(config_updates):
    """Apply configuration overrides to the config module"""
    import config
    
    # Update basic configuration values
    for key, value in config_updates.items():
        if hasattr(config, key):
            old_value = getattr(config, key)
            setattr(config, key, value)
            print(f"🔧 Config override: {key} = {value} (was {old_value})")
    
    # Recalculate derived servo values if any servo parameters changed
    servo_params = ['SERVO_MIN_ANGLE', 'SERVO_MAX_ANGLE', 'SERVO_NEUTRAL_ANGLE', 'SERVO_ROTATION_OFFSET']
    if any(param in config_updates for param in servo_params):
        print("🔄 Recalculating derived servo coordinate values...")
        
        # Recalculate derived values
        config.COORD_MAX_ANGLE = config._normalize_angle(
            config.SERVO_MIN_ANGLE + config.SERVO_ROTATION_OFFSET + 180.0
        )
        config.COORD_MIN_ANGLE = config._normalize_angle(
            config.SERVO_MAX_ANGLE + config.SERVO_ROTATION_OFFSET + 180.0
        )
        config.COORD_NEUTRAL_ANGLE = config._normalize_angle(
            config.SERVO_NEUTRAL_ANGLE + config.SERVO_ROTATION_OFFSET + 180.0
        )
        
        print(f"   COORD_MAX_ANGLE = {config.COORD_MAX_ANGLE}°")
        print(f"   COORD_MIN_ANGLE = {config.COORD_MIN_ANGLE}°")
        print(f"   COORD_NEUTRAL_ANGLE = {config.COORD_NEUTRAL_ANGLE}°")


def create_csv_with_config(config_updates=None):
    """Create CSV with optional configuration overrides"""
    if config_updates:
        apply_config_overrides(config_updates)
    
    # Import after potential config changes
    from export_commands import create_command_csv
    
    print("📤 CREATING SOFTWARE_ISCAN CSV WITH CUSTOM CONFIGURATION...")
    create_command_csv()


def main_with_config_support(create_csv=False, config_updates=None):
    """Main function with configuration override support"""
    if config_updates:
        apply_config_overrides(config_updates)
    
    # Run standard main function
    main(create_csv=create_csv)


def main_math_csv_with_config(config_updates=None):
    """Mathematics and CSV only with configuration override support"""
    if config_updates:
        apply_config_overrides(config_updates)
    
    # Run math-only mode
    main_math_csv()


def main_math_silent_with_config(config_updates=None):
    """Silent mathematics and CSV with configuration override support"""
    if config_updates:
        apply_config_overrides(config_updates)
    
    # Run silent mode
    main_math_silent()


def save_servo_graph_only_with_config(config_updates=None):
    """Create and save only the servo geometry graph with configuration override support"""
    if config_updates:
        apply_config_overrides(config_updates)
    
    # Import and call the function
    from visualizations.servo_interpolation import save_servo_geometry_graph_only
    return save_servo_geometry_graph_only()

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    args = sys.argv[1:]  # Remove script name
      # Check for flags
    create_csv = "--csv" in args or "-c" in args
    math_only = "--math" in args or "-m" in args
    silent = "--silent" in args or "-s" in args
    show_help_flag = "--help" in args or "-h" in args
    servo_graph_only = "--servo-graph" in args or "-g" in args
    
    # Parse configuration overrides
    config_updates = parse_config_args(args)
    
    # Show current configuration if overrides are provided
    if config_updates:
        print("🔧 CONFIGURATION OVERRIDES DETECTED:")
        for key, value in config_updates.items():
            print(f"   {key} = {value}")
        print()
      # Execute based on flags (priority order: help -> servo-graph -> silent -> math -> csv -> standard)
    if show_help_flag:
        # Show command line usage help
        show_help()
    elif servo_graph_only:
        # Save only the servo geometry graph
        print("🎯 Creating servo geometry graph only...")
        output_path = save_servo_graph_only_with_config(config_updates)
        print(f"✅ Servo geometry graph saved: {output_path}")
    elif silent:
        # Silent mathematics and CSV only (minimal output)
        main_math_silent_with_config(config_updates)
    elif math_only:
        # Mathematics and CSV only mode (no visualizations)
        main_math_csv_with_config(config_updates)
    elif create_csv:
        # Full mode with CSV export
        main_with_config_support(create_csv=True, config_updates=config_updates)
    elif config_updates:
        # If only config updates provided without other flags, create CSV
        print("🎯 Configuration override mode: Creating CSV with custom settings")
        create_csv_with_config(config_updates)
    else:
        # Standard full mode (visualizations only)
        main(create_csv=False)