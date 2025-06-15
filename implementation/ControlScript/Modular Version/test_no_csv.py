#!/usr/bin/env python3
"""
Test script to verify camera detection without CSV configuration
"""
import sys
import os
import traceback

def test_camera_detection():
    try:
        # Test ohne CSV-Konfiguration
        print("=== Test: Kamera-Erkennung ohne CSV-Konfiguration ===")
          # CSV temporär umbenennen um den Fallback zu testen
        import shutil
        csv_file = "CamConfig.csv"
        backup_file = "CamConfig_backup.csv"
        
        csv_exists = os.path.exists(csv_file)
        if csv_exists:
            print(f"CSV-Datei gefunden, erstelle Backup...")
            shutil.copy(csv_file, backup_file)
            os.remove(csv_file)
            print(f"CSV-Datei temporär entfernt")
        
        try:
            from main_modular import ControlApp
            print("ControlApp importiert")
            
            app = ControlApp()
            print("App erstellt")
            
            print(f"Verfügbare Kameras (auto-detect): {app.available_cameras}")
            print(f"Webcam-Instanzen: {list(app.webcams.keys())}")
            
            # Teste Webcam-Erkennung direkt
            from webcam_helper import WebcamHelper
            detected = WebcamHelper.detect_available_cameras()
            print(f"Direkte Webcam-Erkennung: {detected}")
            
            if len(app.available_cameras) > 0:
                print("✅ SUCCESS: Kameras wurden ohne CSV-Konfiguration erkannt")
            else:
                print("❌ PROBLEM: Keine Kameras ohne CSV-Konfiguration erkannt")
            
        finally:
            # CSV-Datei wiederherstellen
            if csv_exists and os.path.exists(backup_file):
                shutil.copy(backup_file, csv_file)
                os.remove(backup_file)
                print("CSV-Datei wiederhergestellt")
        
    except Exception as e:
        print(f"Fehler: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_camera_detection()
