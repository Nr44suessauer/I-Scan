#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVO GRAPH EXTRACTOR
====================
Saves only the geometric graph from servo interpolation visualization.

Usage: python save_servo_graph.py [--target-x X] [--target-y Y] [--scan-distance D] [--measurements N]

Author: Marc Nauendorf
"""

import sys
from main import parse_config_args, apply_config_overrides
from visualizations.servo_interpolation import save_servo_geometry_graph_only


def main():
    """
    Save the servo geometry graph with optional configuration parameters
    """
    # Parse command line arguments for configuration
    config_updates = parse_config_args(sys.argv[1:])
    
    if config_updates:
        print("🔧 CONFIGURATION OVERRIDES DETECTED:")
        for key, value in config_updates.items():
            print(f"   {key} = {value}")
        
        # Apply configuration overrides
        apply_config_overrides(config_updates)
        print("📊 Creating servo geometry graph with custom configuration...")
    else:
        print("📊 Creating servo geometry graph with default configuration...")
    
    # Create and save the servo geometry graph
    output_path = save_servo_geometry_graph_only()
    
    print(f"✅ Servo geometry graph saved successfully!")
    print(f"📁 File: {output_path}")


if __name__ == "__main__":
    main()
