#!/usr/bin/env python3
"""
Test script to debug camera stream issues
"""
import tkinter as tk
from main_modular import ControlApp
import time

def debug_camera_streams():
    try:
        print("=== DEBUG: Camera Stream Test ===")
        app = ControlApp()
        
        print(f"Available cameras: {app.available_cameras}")
        print(f"Webcams: {list(app.webcams.keys())}")
        print(f"Camera labels: {list(app.camera_labels.keys())}")
        print(f"Auto-stream enabled: {app.auto_stream_var.get()}")
        
        # Test manual stream start
        print("\n=== Manual Stream Start Test ===")
        for cam_index in [0, 1]:  # Only test physically available cameras
            if cam_index in app.webcams and cam_index in app.camera_labels:
                webcam = app.webcams[cam_index]
                label = app.camera_labels[cam_index]
                
                print(f"Testing camera {cam_index}:")
                print(f"  - Webcam running: {webcam.running}")
                print(f"  - Label exists: {label is not None}")
                
                if not webcam.running:
                    success = webcam.stream_starten(label)
                    print(f"  - Stream start result: {success}")
                    if success:
                        print(f"  ✓ Camera {cam_index} stream started")
                    else:
                        print(f"  ✗ Camera {cam_index} stream failed")
                else:
                    print(f"  - Camera {cam_index} already running")
        
        # Let GUI run for 5 seconds to see streams
        print("\n=== Starting GUI for 5 seconds ===")
        app.root.after(5000, app.root.quit)
        app.root.mainloop()
        
        print("Debug test completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_camera_streams()
