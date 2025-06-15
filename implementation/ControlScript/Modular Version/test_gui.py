#!/usr/bin/env python3
"""Test GUI initialization and camera grid display"""

import sys
import traceback
import threading
import time

def test_gui():
    try:
        from main_modular import ControlApp
        print("Creating GUI application...")
        
        app = ControlApp()
        print("Application created successfully")
        print(f"Available cameras: {app.available_cameras}")
        print(f"Auto-stream variable: {app.auto_stream_var.get()}")
        
        # Test the camera grid functionality
        if hasattr(app, 'camera_grid_frame'):
            print("Camera grid frame found")
        
        # Start the GUI in a separate thread so we can close it programmatically
        def run_gui():
            app.run()
        
        gui_thread = threading.Thread(target=run_gui, daemon=True)
        gui_thread.start()
        
        # Let the GUI run for a few seconds to test
        time.sleep(3)
        
        print("GUI test completed - shutting down")
        app.root.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()
