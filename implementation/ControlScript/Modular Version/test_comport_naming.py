#!/usr/bin/env python3
"""
Test Kamera-Indexnummern als Überschriften
"""
from main_modular import ControlApp

def test_camera_indexnumbers():
    print("=== Test: Kamera-Indexnummern als Überschriften ===")
    try:
        app = ControlApp()
        
        print(f"Verfügbare Kameras: {app.available_cameras}")
        
        # Teste Kamera-Informationen
        for cam_index in app.available_cameras:
            if cam_index in app.webcams:
                webcam = app.webcams[cam_index]
                cam_info = app.get_camera_info(cam_index)
                print(f"Kamera {cam_index}:")
                print(f"  - Name: {cam_info['name']}")
                print(f"  - COM-Port: {cam_info['comport']}")
                print(f"  - Überschrift sollte sein: 'Cam {cam_index}'")
        
        # Kurzer GUI-Test
        print("\nStarting GUI test for 8 seconds...")
        print("Überprüfen Sie, ob die Kamerafelder 'Cam 0', 'Cam 1' etc. als Überschrift zeigen!")
        app.root.after(8000, app.root.quit)
        app.root.mainloop()
        
        print("Test abgeschlossen!")
        
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_camera_indexnumbers()
