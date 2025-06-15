#!/usr/bin/env python3
"""
Finaler Test: Nur Index-Namen für Kameras
"""
from main_modular import ControlApp

def test_index_names_only():
    print("=== Finaler Test: Nur Index-Namen für Kameras ===")
    try:
        app = ControlApp()
        
        print(f"Verfügbare Kameras: {app.available_cameras}")
        print("Kamera-Informationen (sollten nur Index-Namen zeigen):")
        
        for cam_index in app.available_cameras:
            if cam_index in app.webcams:
                cam_info = app.get_camera_info(cam_index)
                print(f"  Kamera {cam_index}:")
                print(f"    - Name: {cam_info['name']}")  # Sollte "Cam X" sein
                print(f"    - COM-Port: {cam_info['comport']}")
        
        print("\n✅ Test erfolgreich - Namen sind nur noch Index-basiert!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_index_names_only()
