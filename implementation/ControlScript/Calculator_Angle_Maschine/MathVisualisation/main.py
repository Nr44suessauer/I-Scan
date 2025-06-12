#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN COORDINATOR MODULE WITH CSV EXPORT
=======================================

Main entry point providing multiple interfaces for the 3D scanner servo angle calculation
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


def main(create_csv=False, csv_name=None):
    """
    Main function - executes complete explanation and visualization including servo interpolation
    
    Args:
        create_csv (bool): If True, also creates a CSV file for Software_IScan import
        csv_name (str, optional): Custom name for the CSV file (without extension)
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
        print("   ✅ 02_angle_progression.png")    # Point-specific calculations (04_point_X_calculation.png)
    if ENABLE_VISUALIZATIONS['point_calculations']:
        # Create individual point calculation visualizations
        print("📊 Creating individual point calculation visualizations...")
        count = 0
        for i, point in enumerate(angles_data, 1):
            create_point_calculation_visualization(point, i)
            count += 1
        visualization_count += count
        print(f"📊 Individual point calculation visualizations saved: output\\point_calculations\\")
        print(f"   ✅ {count} point calculation diagrams (04_point_X_calculation.png)")

    # Calculation table visualization (05)
    if ENABLE_VISUALIZATIONS['calculation_table']:
        create_calculation_table_visualization(angles_data)
        visualization_count += 1
        print("📊 Calculation table visualization saved: output\\05_calculation_table.png")
        print("   ✅ 05_calculation_table.png")

    # Servo interpolation visualization (06)
    if ENABLE_VISUALIZATIONS['servo_interpolation']:
        save_servo_interpolation_visualization()
        visualization_count += 1
        print("📊 Servo interpolation visualization saved: output\\06_servo_interpolation.png")
        print("   ✅ 06_servo_interpolation.png")

    # Servo cone detail visualization (07)
    if ENABLE_VISUALIZATIONS['servo_cone_detail']:
        save_servo_cone_detail()
        visualization_count += 1
        print("📊 Servo cone detail visualization saved: output\\07_servo_cone_detail.png")
        print("   ✅ 07_servo_cone_detail.png")

    # Optional add-on visualization (if available)
    if TARGET_COORD_ADDON_AVAILABLE and ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        if save_target_coord_angle_visualization:
            save_target_coord_angle_visualization()
            visualization_count += 1
            print("📊 Target coord angle explanation saved: output\\target_coord_angle_explanation.png")
            print("   ✅ target_coord_angle_explanation.png (Add-on)")    # Step 4: Optional CSV export for Software_IScan import
    if create_csv:
        print("\n📤 CREATING SOFTWARE_ISCAN IMPORT CSV...")
        from export_commands import create_command_csv
        create_command_csv(custom_name=csv_name)

    # Final summary
    print(f"\n✅ COMPLETE ANALYSIS FINISHED! ({visualization_count} visualizations created)")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    if TARGET_COORD_ADDON_AVAILABLE and ENABLE_VISUALIZATIONS['target_coord_angle_explanation']:
        print("   • Target coordinate angle explanation included (Add-on)")
    print("   • Geometric angles and servo interpolation ready for implementation")
    print(f"   • Configuration: {sum(ENABLE_VISUALIZATIONS.values())}/{len(ENABLE_VISUALIZATIONS)} visualizations enabled")
    print("\n" + "="*80)


def main_math_csv(csv_name=None):
    """
    Mathematics and CSV only - no visualizations
    
    Creates mathematical explanation, servo interpolation calculation 
    and CSV export without any visualizations.
    
    Args:
        csv_name (str, optional): Custom name for the CSV file (without extension)
    """
    print("\n🧮 STARTING MATHEMATICS + CSV MODE (no visualizations)...\n")
    
    # Step 1: Mathematical explanation for geometric angles
    angles_data = print_step_by_step_explanation()
    
    # Step 2: Servo interpolation explanation
    print("\n" + "="*80)
    servo_data = print_servo_interpolation_explanation()
    
    # Step 2.5: Detailed reachability analysis
    print("\n" + "="*80)
    print_detailed_reachability_table()
      # Step 3: CSV export for Software_IScan import
    print("\n📤 CREATING SOFTWARE_ISCAN IMPORT CSV...")
    from export_commands import create_command_csv
    create_command_csv(custom_name=csv_name)
    
    # Final summary
    print("\n✅ MATHEMATICS + CSV COMPLETED!")
    print("   • Mathematical calculation explained")
    print("   • Servo interpolation calculated")
    print("   • CSV export ready for Software_IScan import")
    print("   • No visualizations created (use --csv for full mode)")
    print("\n" + "="*80)
    
    return angles_data, servo_data


def main_math_silent(csv_name=None):
    """
    Silent mathematics and CSV only - minimal output
    
    Args:
        csv_name (str, optional): Custom name for the CSV file (without extension)
    """
    print("🔇 Silent mode: Mathematics + CSV...")
    
    # Step 1: Mathematical calculation (silent)
    angles_data = print_step_by_step_explanation()
    
    # Step 2: Servo interpolation (silent)
    servo_data = print_servo_interpolation_explanation()
      # Step 3: CSV export
    from export_commands import create_command_csv
    create_command_csv(custom_name=csv_name)
    
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
    print("  --visualize, -v  Create all visualizations (with custom config)")
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
    print("  --csv-name VALUE       Set custom CSV filename (without extension) [default: timestamp]")
    print()
    print("EXAMPLES:")
    print("  python main.py --csv")
    print("  python main.py --csv --csv-name custom_scan_results")
    print("  python main.py --visualize --target-x 90 --target-y 50 --scan-distance 80 --measurements 30")
    print("  python main.py --silent --target-x 100 --target-y 75")
    print("  python main.py --math --servo-min 10 --servo-max 80")
    print("  python main.py --csv --scan-distance 80 --measurements 7")
    print("  python main.py --csv --csv-name my_3d_scan --target-x 30 --target-y 50 --scan-distance 80 --measurements 5")
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
        
        # Special string parameter for CSV name
        if arg == '--csv-name':
            if i + 1 < len(args):
                config_updates['CSV_NAME'] = args[i + 1]
                i += 2  # Skip the next argument as it's the value
            else:
                print(f"⚠️ Missing value for {arg}")
                i += 1
        elif arg in config_params:
            if i + 1 < len(args):
                try:
                    value = float(args[i + 1])
                    # NUMBER_OF_MEASUREMENTS should be int
                    if config_params[arg] == 'NUMBER_OF_MEASUREMENTS':
                        value = int(value)
                    config_updates[config_params[arg]] = value
                    i += 2  # Skip the next argument as it's the value
                except (ValueError, IndexError):
                    print(f"⚠️ Invalid value for {arg}")
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
    
    for key, value in config_updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
            print(f"   ✅ {key} updated to {value}")
        else:
            print(f"   ⚠️ Unknown configuration key: {key}")


def create_csv_with_config(config_updates=None):
    """Create CSV with optional configuration overrides"""
    csv_name = None
    if config_updates:
        # Extract CSV name if provided
        csv_name = config_updates.pop('CSV_NAME', None)
        apply_config_overrides(config_updates)
    
    # Import after potential config changes
    from export_commands import create_command_csv
    
    print("📤 CREATING SOFTWARE_ISCAN CSV WITH CUSTOM CONFIGURATION...")
    create_command_csv(custom_name=csv_name)


def main_with_config_support(create_csv=False, config_updates=None):
    """Main function with configuration override support"""
    csv_name = None
    if config_updates:
        # Extract CSV name if provided
        csv_name = config_updates.pop('CSV_NAME', None)
        apply_config_overrides(config_updates)
    
    # Run standard main function
    main(create_csv=create_csv, csv_name=csv_name)


def main_math_csv_with_config(config_updates=None):
    """Mathematics and CSV only with configuration override support"""
    csv_name = None
    if config_updates:
        # Extract CSV name if provided
        csv_name = config_updates.pop('CSV_NAME', None)
        apply_config_overrides(config_updates)
    
    # Run math-only mode with CSV name
    main_math_csv(csv_name=csv_name)


def main_math_silent_with_config(config_updates=None):
    """Silent mathematics and CSV with configuration override support"""
    csv_name = None
    if config_updates:
        # Extract CSV name if provided
        csv_name = config_updates.pop('CSV_NAME', None)
        apply_config_overrides(config_updates)
    
    # Run silent mode with CSV name
    main_math_silent(csv_name=csv_name)


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
    visualize_only = "--visualize" in args or "-v" in args
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
    
    # Execute based on flags (priority order: help -> servo-graph -> visualize -> silent -> math -> csv -> standard)
    if show_help_flag:
        # Show command line usage help
        show_help()
    elif servo_graph_only:
        # Save only the servo geometry graph
        print("🎯 Creating servo geometry graph only...")
        output_path = save_servo_graph_only_with_config(config_updates)
        print(f"✅ Servo geometry graph saved: {output_path}")
    elif visualize_only:
        # Create all visualizations with custom configuration (no CSV)
        print("🎨 Creating all visualizations with custom configuration...")
        main_with_config_support(create_csv=False, config_updates=config_updates)
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