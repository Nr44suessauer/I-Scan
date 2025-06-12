#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLE CSV EXPORT FOR SOFTWARE_ISCAN
=====================================
Creates a CSV file compatible with Software_IScan operation queue.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 3.0 (Minimal standalone version)
"""

import csv
import os
import json
import math
import glob
from datetime import datetime
import config
from servo_interpolation import calculate_servo_interpolation


def delete_old_csv_files():
    """Delete all existing CSV files in the output directory"""
    output_dir = config.OUTPUT_DIR
    csv_pattern = os.path.join(output_dir, "iscan_commands_*.csv")
    
    old_csv_files = glob.glob(csv_pattern)
    
    for old_file in old_csv_files:
        try:
            os.remove(old_file)
            print(f"🗑️ Deleted old CSV: {os.path.basename(old_file)}")
        except OSError as e:
            print(f"⚠️ Could not delete {os.path.basename(old_file)}: {e}")
    
    if old_csv_files:
        print(f"✅ Cleaned up {len(old_csv_files)} old CSV file(s)")


def create_command_csv(custom_name=None):
    """Creates a simple command CSV file for Software_IScan import
    
    Args:
        custom_name (str, optional): Custom name for the CSV file (without extension)
    """
    print("🚀 Creating Software_IScan command CSV...")
    
    # Delete old CSV files first
    delete_old_csv_files()
    
    # Generate filename
    if custom_name:
        filename = f"{custom_name}.csv"
        print(f"📝 Using custom filename: {filename}")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"iscan_commands_{timestamp}.csv"
    
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    # Ensure output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Get servo data
    servo_data = calculate_servo_interpolation()
    
    # Calculate stepper distance using current config values
    stepper_distance_cm = config.SCAN_DISTANCE / (config.NUMBER_OF_MEASUREMENTS - 1)
    
    # Prepare commands
    commands = []
      # Add home command
    commands.append(['home', '{}', 'Execute home function'])
    
    # Process each servo data point
    for i, data in enumerate(servo_data):
        point_num = data['point']
        y_position = data['y_pos']
        is_reachable = data['is_reachable']
        
        if is_reachable:
            # Add servo command
            servo_angle = int(round(data['servo_angle']))
            commands.append([
                'servo',
                json.dumps({'angle': servo_angle}),
                f'Point {point_num}: Set servo to {servo_angle}° (Y={y_position:.1f}cm)'
            ])
            
            # Add photo command
            commands.append([
                'photo',
                json.dumps({'delay': 2.0}),
                f'Point {point_num}: Capture photo'
            ])
        
        # Add stepper movement for all points except the last one (regardless of reachability)
        if i < len(servo_data) - 1:
            # Calculate steps for 28BYJ-48 stepper motor
            steps = int(round((stepper_distance_cm * 10) / (math.pi * 28) * 4096))
            commands.append([
                'stepper',
                json.dumps({'steps': steps, 'direction': 1, 'speed': 80}),
                f'Move {stepper_distance_cm:.2f}cm forward ({steps} steps)'
            ])
    
    # Write CSV file
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['type', 'params', 'description'])
        
        # Write commands
        writer.writerows(commands)
    
    print(f"✅ CSV created: {filename}")
    print(f"📁 Full path: {filepath}")
    return filepath


if __name__ == "__main__":
    create_command_csv()
