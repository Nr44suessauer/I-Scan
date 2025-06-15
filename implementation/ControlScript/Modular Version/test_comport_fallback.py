#!/usr/bin/env python3
"""
Test COM-Port Naming ohne CSV (Fallback-Modus)
"""
import os
import shutil
from main_modular import ControlApp

def test_comport_fallback():
    print("=== Test: COM-Port Naming ohne CSV ===")
    
    # CSV temporär sichern
    csv_file = "CamConfig.csv"
    backup_file = "CamConfig_temp_backup.csv"
    
    csv_exists = os.path.exists(csv_file)
    if csv_exists:
        shutil.move(csv_file, backup_file)
        print("CSV temporär entfernt für Fallback-Test")
    
    try:
        app = ControlApp()
        
        print(f"Verfügbare Kameras (Fallback): {app.available_cameras}")
        
        # Teste Fallback-Kamera-Informationen
        for cam_index in app.available_cameras:
            if cam_index in app.webcams:
                webcam = app.webcams[cam_index]
                cam_info = app.get_camera_info(cam_index)
                print(f"Kamera {cam_index} (Fallback):")
                print(f"  - Name: {cam_info['name']}")
                print(f"  - COM-Port: {cam_info['comport']}")
                print(f"  - Webcam COM-Port: {webcam.com_port}")
        
        print("Fallback-Test erfolgreich!")
        
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # CSV wiederherstellen
        if csv_exists:
            shutil.move(backup_file, csv_file)
            print("CSV wiederhergestellt")

if __name__ == "__main__":
    test_comport_fallback()
