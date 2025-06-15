#!/usr/bin/env python3
"""
Simple GUI test to check camera streams
"""
import tkinter as tk
from main_modular import ControlApp

def simple_test():
    try:
        print("Starting simple camera stream test...")
        app = ControlApp()
        
        print(f"Available cameras: {app.available_cameras}")
        print(f"Webcams created: {list(app.webcams.keys())}")
        print(f"Camera labels: {list(app.camera_labels.keys())}")
        print(f"Auto-stream enabled: {app.auto_stream_var.get()}")
        
        # Manually start streams for each camera
        print("\nStarting camera streams manually...")
        for cam_index in app.available_cameras:
            if cam_index in app.webcams and cam_index in app.camera_labels:
                webcam = app.webcams[cam_index]
                camera_label = app.camera_labels[cam_index]
                
                print(f"Starting camera {cam_index}...")
                if webcam.stream_starten(camera_label):
                    print(f"✓ Camera {cam_index} started successfully")
                else:
                    print(f"✗ Camera {cam_index} failed to start")
            else:
                print(f"✗ Camera {cam_index} missing webcam or label")
        
        print("\nStarting GUI...")
        # Start GUI with a 10 second timeout for testing
        app.root.after(10000, app.root.quit)  # Auto-close after 10 seconds
        app.root.mainloop()
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
