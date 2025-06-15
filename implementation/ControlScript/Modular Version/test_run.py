#!/usr/bin/env python3
"""
Test script to run the main application with error catching
"""
import sys
import traceback

try:
    from main_modular import ControlApp
    print("Successfully imported ControlApp")
    
    # Create the app
    app = ControlApp()
    print("Successfully created app instance")
    
    print("Available cameras:", app.available_cameras)
    print("Camera config loaded:", bool(app.camera_config.get_all_cameras()))
    
    if app.camera_config.get_all_cameras():
        cameras = app.camera_config.get_all_cameras()
        print("Configured cameras:")
        for cam in cameras:
            print(f"  Index {cam['indexnummer']}: {cam['bezeichnung']} ({cam['comport']})")
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
