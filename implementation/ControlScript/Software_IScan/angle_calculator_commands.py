#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANGLE CALCULATOR COMMANDS MODULE
===============================

Commands for interfacing with Calculator_Angle_Maschine from Software_IScan.
Provides two main commands:
1. CSV Silent Mode - Generate CSV only with configurable parameters
2. Full Visualization Mode - Generate both graphics and CSV

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""

import os
import sys
import subprocess
import threading
from tkinter import messagebox, filedialog
from datetime import datetime

class AngleCalculatorInterface:
    """Interface for communicating with Calculator_Angle_Maschine module"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.calculator_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "Calculator_Angle_Maschine", 
            "MathVisualisation"
        )
        
    def log(self, message):
        """Log message to logger if available, otherwise print"""
        if self.logger:
            self.logger.log(message)
        else:
            print(message)
    
    def generate_csv_silent(self, csv_name=None, target_x=50, target_y=50, 
                           scanner_x=0, scanner_y=0, scan_distance=100, 
                           measurements=10, servo_min=0.0, servo_max=90.0, 
                           servo_neutral=185.0):
        """
        Command 1: CSV Silent Mode
        
        Generates CSV file only with minimal output and configurable parameters.
        Perfect for automation and background processing.
        
        Args:
            csv_name (str): Custom CSV filename (without extension)
            target_x (float): X-position of target object (cm)
            target_y (float): Y-position of target object (cm)
            scanner_x (float): X-position of scanner (cm)
            scanner_y (float): Y-position of scanner (cm)
            scan_distance (float): Total scan distance (cm)
            measurements (int): Number of measurement points
            servo_min (float): Minimum servo angle (degrees)
            servo_max (float): Maximum servo angle (degrees)
            servo_neutral (float): Servo neutral angle (degrees)
        """
        try:
            self.log("🔇 Starting CSV Silent Mode - Calculator_Angle_Maschine")
            
            # Build command arguments
            cmd = [sys.executable, "main.py", "--silent"]
            
            # Add parameters
            cmd.extend([
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scanner-x", str(scanner_x),
                "--scanner-y", str(scanner_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ])
            
            # Add custom CSV name if provided
            if csv_name:
                cmd.extend(["--csv-name", csv_name])
                self.log(f"📝 Using custom CSV name: {csv_name}.csv")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_name = f"iscan_silent_{timestamp}"
                cmd.extend(["--csv-name", csv_name])
                self.log(f"📝 Using timestamp CSV name: {csv_name}.csv")
            
            # Log configuration
            self.log(f"🎯 Target: ({target_x}, {target_y}) cm")
            self.log(f"📏 Scanner: ({scanner_x}, {scanner_y}) cm")
            self.log(f"📐 Scan distance: {scan_distance} cm, {measurements} points")
            self.log(f"🔧 Servo range: {servo_min}° to {servo_max}° (neutral: {servo_neutral}°)")
            
            # Execute command
            result = subprocess.run(
                cmd, 
                cwd=self.calculator_path,
                capture_output=True, 
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log("✅ CSV generation completed successfully!")
                self.log("📁 CSV file ready for import in operation queue")
                
                # Find the generated CSV file
                csv_file = f"{csv_name}.csv"
                csv_path = os.path.join(self.calculator_path, "output", csv_file)
                
                if os.path.exists(csv_path):
                    self.log(f"📄 Generated: {csv_file}")
                    return csv_path
                else:
                    self.log(f"⚠️ Warning: CSV file not found at expected location: {csv_path}")
                    return None
            else:
                self.log(f"❌ Error in CSV generation: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.log("⏰ Timeout: CSV generation took too long")
            return None
        except Exception as e:
            self.log(f"❌ Exception in CSV generation: {str(e)}")
            return None
    
    def generate_full_analysis(self, csv_name=None, target_x=50, target_y=50,
                              scanner_x=0, scanner_y=0, scan_distance=100,
                              measurements=10, servo_min=0.0, servo_max=90.0,
                              servo_neutral=185.0):
        """
        Command 2: Full Visualization Mode
        
        Generates complete analysis with visualizations AND CSV export.
        Includes all mathematical explanations and graphical representations.
        
        Args:
            csv_name (str): Custom CSV filename (without extension)
            target_x (float): X-position of target object (cm)
            target_y (float): Y-position of target object (cm)
            scanner_x (float): X-position of scanner (cm)
            scanner_y (float): Y-position of scanner (cm)
            scan_distance (float): Total scan distance (cm)
            measurements (int): Number of measurement points
            servo_min (float): Minimum servo angle (degrees)
            servo_max (float): Maximum servo angle (degrees)
            servo_neutral (float): Servo neutral angle (degrees)
        """
        try:
            self.log("🎨 Starting Full Analysis Mode - Calculator_Angle_Maschine")
            self.log("📊 This will generate visualizations AND CSV export...")
            
            # Build command arguments
            cmd = [sys.executable, "main.py", "--csv"]
            
            # Add parameters
            cmd.extend([
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scanner-x", str(scanner_x),
                "--scanner-y", str(scanner_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ])
            
            # Add custom CSV name if provided
            if csv_name:
                cmd.extend(["--csv-name", csv_name])
                self.log(f"📝 Using custom CSV name: {csv_name}.csv")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_name = f"iscan_full_{timestamp}"
                cmd.extend(["--csv-name", csv_name])
                self.log(f"📝 Using timestamp CSV name: {csv_name}.csv")
            
            # Log configuration
            self.log(f"🎯 Target: ({target_x}, {target_y}) cm")
            self.log(f"📏 Scanner: ({scanner_x}, {scanner_y}) cm")
            self.log(f"📐 Scan distance: {scan_distance} cm, {measurements} points")
            self.log(f"🔧 Servo range: {servo_min}° to {servo_max}° (neutral: {servo_neutral}°)")
            
            # Execute command
            result = subprocess.run(
                cmd,
                cwd=self.calculator_path,
                capture_output=True,
                text=True,
                timeout=120  # Longer timeout for visualization generation
            )
            
            if result.returncode == 0:
                self.log("✅ Full analysis completed successfully!")
                self.log("📊 Visualizations and CSV generated")
                self.log("📁 Files ready in Calculator_Angle_Maschine/MathVisualisation/output/")
                
                # Find the generated CSV file
                csv_file = f"{csv_name}.csv"
                csv_path = os.path.join(self.calculator_path, "output", csv_file)
                
                if os.path.exists(csv_path):
                    self.log(f"📄 Generated: {csv_file}")
                    return csv_path
                else:
                    self.log(f"⚠️ Warning: CSV file not found at expected location: {csv_path}")
                    return None
            else:
                self.log(f"❌ Error in full analysis: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.log("⏰ Timeout: Full analysis took too long")
            return None
        except Exception as e:
            self.log(f"❌ Exception in full analysis: {str(e)}")
            return None
    
    def generate_csv_silent_async(self, callback=None, **kwargs):
        """
        Asynchronous version of CSV silent generation
        
        Args:
            callback: Function to call when completed (receives csv_path as argument)
            **kwargs: All parameters for generate_csv_silent
        """
        def run_async():
            csv_path = self.generate_csv_silent(**kwargs)
            if callback:
                callback(csv_path)
        
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        return thread
    
    def generate_full_analysis_async(self, callback=None, **kwargs):
        """
        Asynchronous version of full analysis generation
        
        Args:
            callback: Function to call when completed (receives csv_path as argument)
            **kwargs: All parameters for generate_full_analysis
        """
        def run_async():
            csv_path = self.generate_full_analysis(**kwargs)
            if callback:
                callback(csv_path)
        
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        return thread


class AngleCalculatorDialog:
    """Dialog for configuring angle calculator parameters"""
    
    def __init__(self, parent, title="Angle Calculator Configuration"):
        import tkinter as tk
        from tkinter import ttk
        
        self.result = None
        self.cancelled = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        self.create_widgets()
        
    def create_widgets(self):
        import tkinter as tk
        from tkinter import ttk
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📐 3D Scanner Configuration", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # CSV Name section
        csv_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        csv_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(csv_frame, text="CSV Filename (optional):").pack(anchor="w")
        self.csv_name_var = tk.StringVar()
        self.csv_name_entry = ttk.Entry(csv_frame, textvariable=self.csv_name_var, width=40)
        self.csv_name_entry.pack(fill="x", pady=(5, 0))
        ttk.Label(csv_frame, text="Leave empty for timestamp-based naming", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w")
        
        # Scanner Configuration section
        scanner_frame = ttk.LabelFrame(main_frame, text="Scanner Configuration", padding="10")
        scanner_frame.pack(fill="x", pady=(0, 15))
        
        # Target position
        target_subframe = ttk.Frame(scanner_frame)
        target_subframe.pack(fill="x", pady=(0, 10))
        ttk.Label(target_subframe, text="Target Position (cm):").pack(anchor="w")
        
        target_coord_frame = ttk.Frame(target_subframe)
        target_coord_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(target_coord_frame, text="X:").pack(side="left")
        self.target_x_var = tk.StringVar(value="50")
        ttk.Entry(target_coord_frame, textvariable=self.target_x_var, width=10).pack(side="left", padx=(5, 15))
        
        ttk.Label(target_coord_frame, text="Y:").pack(side="left")
        self.target_y_var = tk.StringVar(value="50")
        ttk.Entry(target_coord_frame, textvariable=self.target_y_var, width=10).pack(side="left", padx=(5, 0))
        
        # Scanner position
        scanner_subframe = ttk.Frame(scanner_frame)
        scanner_subframe.pack(fill="x", pady=(0, 10))
        ttk.Label(scanner_subframe, text="Scanner Position (cm):").pack(anchor="w")
        
        scanner_coord_frame = ttk.Frame(scanner_subframe)
        scanner_coord_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(scanner_coord_frame, text="X:").pack(side="left")
        self.scanner_x_var = tk.StringVar(value="0")
        ttk.Entry(scanner_coord_frame, textvariable=self.scanner_x_var, width=10).pack(side="left", padx=(5, 15))
        
        ttk.Label(scanner_coord_frame, text="Y:").pack(side="left")
        self.scanner_y_var = tk.StringVar(value="0")
        ttk.Entry(scanner_coord_frame, textvariable=self.scanner_y_var, width=10).pack(side="left", padx=(5, 0))
        
        # Scan parameters
        scan_subframe = ttk.Frame(scanner_frame)
        scan_subframe.pack(fill="x", pady=(0, 10))
        
        distance_frame = ttk.Frame(scan_subframe)
        distance_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(distance_frame, text="Scan Distance (cm):").pack(side="left")
        self.scan_distance_var = tk.StringVar(value="100")
        ttk.Entry(distance_frame, textvariable=self.scan_distance_var, width=10).pack(side="left", padx=(5, 0))
        
        measurements_frame = ttk.Frame(scan_subframe)
        measurements_frame.pack(fill="x")
        ttk.Label(measurements_frame, text="Number of Measurements:").pack(side="left")
        self.measurements_var = tk.StringVar(value="10")
        ttk.Entry(measurements_frame, textvariable=self.measurements_var, width=10).pack(side="left", padx=(5, 0))
        
        # Servo Configuration section
        servo_frame = ttk.LabelFrame(main_frame, text="Servo Configuration", padding="10")
        servo_frame.pack(fill="x", pady=(0, 15))
        
        servo_range_frame = ttk.Frame(servo_frame)
        servo_range_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(servo_range_frame, text="Min Angle (°):").pack(side="left")
        self.servo_min_var = tk.StringVar(value="0.0")
        ttk.Entry(servo_range_frame, textvariable=self.servo_min_var, width=8).pack(side="left", padx=(5, 15))
        
        ttk.Label(servo_range_frame, text="Max Angle (°):").pack(side="left")
        self.servo_max_var = tk.StringVar(value="90.0")
        ttk.Entry(servo_range_frame, textvariable=self.servo_max_var, width=8).pack(side="left", padx=(5, 0))
        
        servo_neutral_frame = ttk.Frame(servo_frame)
        servo_neutral_frame.pack(fill="x")
        ttk.Label(servo_neutral_frame, text="Neutral Angle (°):").pack(side="left")
        self.servo_neutral_var = tk.StringVar(value="185.0")
        ttk.Entry(servo_neutral_frame, textvariable=self.servo_neutral_var, width=8).pack(side="left", padx=(5, 0))
        
        # Preset buttons
        preset_frame = ttk.LabelFrame(main_frame, text="Quick Presets", padding="10")
        preset_frame.pack(fill="x", pady=(0, 15))
        
        preset_buttons_frame = ttk.Frame(preset_frame)
        preset_buttons_frame.pack(fill="x")
        
        ttk.Button(preset_buttons_frame, text="Original I-Scan", 
                  command=self.load_original_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_buttons_frame, text="Default", 
                  command=self.load_default_preset).pack(side="left", padx=(0, 10))
        ttk.Button(preset_buttons_frame, text="Quick Test", 
                  command=self.load_test_preset).pack(side="left")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side="right")
        
        # Bind Enter key to OK
        self.dialog.bind('<Return>', lambda e: self.ok())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Focus on first entry
        self.csv_name_entry.focus()
    
    def load_original_preset(self):
        """Load original I-Scan setup (33, 50, 80cm, 7 points)"""
        self.target_x_var.set("33")
        self.target_y_var.set("50")
        self.scanner_x_var.set("0")
        self.scanner_y_var.set("0")
        self.scan_distance_var.set("80")
        self.measurements_var.set("7")
        self.servo_min_var.set("0.0")
        self.servo_max_var.set("90.0")
        self.servo_neutral_var.set("185.0")
    
    def load_default_preset(self):
        """Load default configuration"""
        self.target_x_var.set("50")
        self.target_y_var.set("50")
        self.scanner_x_var.set("0")
        self.scanner_y_var.set("0")
        self.scan_distance_var.set("100")
        self.measurements_var.set("10")
        self.servo_min_var.set("0.0")
        self.servo_max_var.set("90.0")
        self.servo_neutral_var.set("185.0")
    
    def load_test_preset(self):
        """Load quick test configuration"""
        self.target_x_var.set("30")
        self.target_y_var.set("40")
        self.scanner_x_var.set("0")
        self.scanner_y_var.set("0")
        self.scan_distance_var.set("60")
        self.measurements_var.set("5")
        self.servo_min_var.set("0.0")
        self.servo_max_var.set("90.0")
        self.servo_neutral_var.set("185.0")
    
    def ok(self):
        try:
            # Validate and collect all parameters
            self.result = {
                'csv_name': self.csv_name_var.get().strip() or None,
                'target_x': float(self.target_x_var.get()),
                'target_y': float(self.target_y_var.get()),
                'scanner_x': float(self.scanner_x_var.get()),
                'scanner_y': float(self.scanner_y_var.get()),
                'scan_distance': float(self.scan_distance_var.get()),
                'measurements': int(self.measurements_var.get()),
                'servo_min': float(self.servo_min_var.get()),
                'servo_max': float(self.servo_max_var.get()),
                'servo_neutral': float(self.servo_neutral_var.get())
            }
            
            # Basic validation
            if self.result['measurements'] < 2:
                raise ValueError("Number of measurements must be at least 2")
            if self.result['scan_distance'] <= 0:
                raise ValueError("Scan distance must be positive")
            if self.result['servo_min'] >= self.result['servo_max']:
                raise ValueError("Servo min angle must be less than max angle")
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your input:\n{str(e)}")
    
    def cancel(self):
        self.cancelled = True
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        if self.cancelled:
            return None
        return self.result


def show_angle_calculator_dialog(parent, title="Angle Calculator Configuration"):
    """
    Show configuration dialog for angle calculator
    
    Returns:
        dict: Configuration parameters or None if cancelled
    """
    dialog = AngleCalculatorDialog(parent, title)
    return dialog.show()
