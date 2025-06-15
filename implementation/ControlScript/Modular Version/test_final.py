#!/usr/bin/env python3
"""
Final test to verify camera streams work in the GUI
"""
from main_modular import ControlApp

def final_test():
    print("Starting final camera stream test...")
    try:
        app = ControlApp()
        print(f"Available cameras: {app.available_cameras}")
        print(f"Auto-stream enabled: {app.auto_stream_var.get()}")
        
        # Run the application
        print("Starting application... Check if camera streams are visible!")
        app.root.after(15000, app.root.quit)  # Auto-close after 15 seconds for testing
        app.run()
        
        print("Test completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_test()
