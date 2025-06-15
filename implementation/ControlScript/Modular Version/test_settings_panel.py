#!/usr/bin/env python3
"""
Test Settings Panel Implementation
Tests the new Settings Panel with Home, Drive Up, Drive Down controls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_modular import ControlApp

def test_settings_panel():
    """Test the settings panel functionality"""
    print("=" * 50)
    print("I-Scan Settings Panel Test")
    print("=" * 50)
    print("Testing Settings Panel implementation...")
    print("Features: Home Button, Drive Up/Down with + Queue buttons")
    print()
    
    try:
        # Create and start application
        app = ControlApp()
        
        # Verify settings panel exists
        if hasattr(app, 'settings_frame'):
            print("✅ Settings Panel created successfully")
        else:
            print("❌ Settings Panel not found")
            return
            
        # Verify Home controls
        if hasattr(app, 'home_exec_btn') and hasattr(app, 'home_add_btn'):
            print("✅ Home controls found")
        else:
            print("❌ Home controls missing")
            
        # Verify Drive Up controls
        if (hasattr(app, 'drive_up_distance') and 
            hasattr(app, 'drive_up_exec_btn') and 
            hasattr(app, 'drive_up_add_btn')):
            print("✅ Drive Up controls found")
        else:
            print("❌ Drive Up controls missing")
            
        # Verify Drive Down controls
        if (hasattr(app, 'drive_down_distance') and 
            hasattr(app, 'drive_down_exec_btn') and 
            hasattr(app, 'drive_down_add_btn')):
            print("✅ Drive Down controls found")
        else:
            print("❌ Drive Down controls missing")
        
        print()
        print("Settings Panel Test completed!")
        print("You can now test the following features:")
        print("1. Home Button (🏠 Home) - Execute or add to queue")
        print("2. Drive Up (⬆ Drive Up) - Set distance and execute/add to queue")
        print("3. Drive Down (⬇ Drive Down) - Set distance and execute/add to queue")
        print()
        print("The Settings Panel should be visible under the Queue in the GUI.")
        
        # Start the application
        app.run()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_settings_panel()
