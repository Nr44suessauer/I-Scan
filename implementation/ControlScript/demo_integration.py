#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: Calculator_Angle_Maschine Integration Test
==============================================

This demo script tests both Calculator_Angle_Maschine commands
integrated into Software_IScan.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""

import os
import sys
import time

# Add Software_IScan to path
software_iscan_path = os.path.join(os.path.dirname(__file__), "Software_IScan")
sys.path.insert(0, software_iscan_path)

try:
    from angle_calculator_commands import AngleCalculatorInterface
except ImportError as e:
    print(f"❌ Could not import AngleCalculatorInterface: {e}")
    print(f"📁 Looking in: {software_iscan_path}")
    sys.exit(1)

class DemoLogger:
    """Simple logger for demo purposes"""
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

def demo_csv_silent_mode():
    """Demo CSV Silent Mode"""
    print("\n" + "="*60)
    print("🔇 DEMO: CSV Silent Mode")
    print("="*60)
    
    logger = DemoLogger()
    interface = AngleCalculatorInterface(logger)
    
    # Test with original I-Scan parameters
    logger.log("Testing with Original I-Scan parameters...")
    csv_path = interface.generate_csv_silent(
        csv_name="demo_silent",
        target_x=33,
        target_y=50,
        scan_distance=80,
        measurements=7
    )
    
    if csv_path:
        logger.log(f"✅ Success! CSV generated: {csv_path}")
        
        # Show first few lines of CSV
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:8]  # First 8 lines
            
            logger.log("📄 CSV Preview:")
            for i, line in enumerate(lines):
                print(f"   {i+1}: {line.strip()}")
            if len(lines) >= 8:
                print(f"   ... (and {sum(1 for _ in open(csv_path)) - 8} more lines)")
                
        except Exception as e:
            logger.log(f"Could not read CSV: {e}")
    else:
        logger.log("❌ Failed to generate CSV")
    
    return csv_path is not None

def demo_full_analysis_mode():
    """Demo Full Analysis Mode"""
    print("\n" + "="*60)
    print("🎨 DEMO: Full Analysis Mode")
    print("="*60)
    
    logger = DemoLogger()
    interface = AngleCalculatorInterface(logger)
    
    # Test with quick test parameters
    logger.log("Testing with Quick Test parameters...")
    csv_path = interface.generate_full_analysis(
        csv_name="demo_full",
        target_x=30,
        target_y=40,
        scan_distance=60,
        measurements=5
    )
    
    if csv_path:
        logger.log(f"✅ Success! Complete analysis finished")
        logger.log(f"📊 Visualizations saved in Calculator_Angle_Maschine/MathVisualisation/output/")
        logger.log(f"📄 CSV file: {csv_path}")
        
        # Count generated files
        output_dir = os.path.dirname(csv_path)
        if os.path.exists(output_dir):
            png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
            csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
            
            logger.log(f"📊 Generated {len(png_files)} visualization files")
            logger.log(f"📄 Generated {len(csv_files)} CSV files")
            
            # Show some file names
            if png_files:
                logger.log("🖼️ Visualization files:")
                for png_file in sorted(png_files)[:3]:  # Show first 3
                    print(f"   - {png_file}")
                if len(png_files) > 3:
                    print(f"   ... and {len(png_files) - 3} more")
    else:
        logger.log("❌ Failed to generate full analysis")
    
    return csv_path is not None

def main():
    """Run the demo"""
    print("🎯 Calculator_Angle_Maschine Integration Demo")
    print("=" * 50)
    
    # Check if Calculator_Angle_Maschine is available
    calc_path = os.path.join(os.path.dirname(__file__), "Calculator_Angle_Maschine", "MathVisualisation")
    if not os.path.exists(calc_path):
        print("❌ Calculator_Angle_Maschine not found!")
        print(f"   Expected path: {calc_path}")
        return False
    
    print("✅ Calculator_Angle_Maschine found")
    print(f"📁 Path: {calc_path}")
    
    # Run demos
    results = []
    
    try:
        # Demo 1: CSV Silent Mode
        results.append(demo_csv_silent_mode())
        
        # Demo 2: Full Analysis Mode  
        results.append(demo_full_analysis_mode())
        
    except KeyboardInterrupt:
        print("\n❌ Demo interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return False
    
    # Summary
    print("\n" + "="*60)
    print("📋 DEMO SUMMARY")
    print("="*60)
    
    if all(results):
        print("✅ All demos completed successfully!")
        print("🎯 Integration is working correctly")
        print("\n📋 Next steps:")
        print("   1. Run Software_IScan: python Software_IScan/main.py")
        print("   2. Look for 'Calculator_Angle_Maschine' section in GUI")
        print("   3. Use 'CSV Silent Mode' or 'Vollanalyse + CSV' buttons")
        print("   4. Configure parameters and generate CSV files")
        print("   5. Import generated CSV into operation queue")
        return True
    else:
        print("❌ Some demos failed")
        failed_demos = []
        if not results[0]:
            failed_demos.append("CSV Silent Mode")
        if not results[1]:
            failed_demos.append("Full Analysis Mode")
        
        print(f"   Failed: {', '.join(failed_demos)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
