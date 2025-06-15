#!/usr/bin/env python3
"""
Test verfügbare Kameras - nur die tatsächlich verfügbaren anzeigen
"""
from main_modular import ControlApp

def test_available_only():
    print("=== Test: Nur verfügbare Kameras anzeigen ===")
    try:
        app = ControlApp()
        
        print(f"Verfügbare Kameras: {app.available_cameras}")
        print(f"Webcams erstellt: {list(app.webcams.keys())}")
        print(f"Camera Labels erstellt: {list(app.camera_labels.keys())}")
        
        # Vergleiche verfügbare vs. erstellte
        expected = set(app.available_cameras)
        webcams_created = set(app.webcams.keys())
        labels_created = set(app.camera_labels.keys())
        
        print(f"\nErwartet: {expected}")
        print(f"Webcams: {webcams_created}")
        print(f"Labels: {labels_created}")
        
        if expected == webcams_created == labels_created:
            print("✅ SUCCESS: Nur verfügbare Kameras wurden erstellt!")
        else:
            print("❌ FEHLER: Unterschied zwischen verfügbaren und erstellten Kameras")
        
        print("Test abgeschlossen!")
        
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_available_only()
