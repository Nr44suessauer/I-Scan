#!/usr/bin/env python3
"""
Script to detect and test available cameras
"""
import cv2
import sys

def test_available_cameras():
    """Test which camera indices are actually available"""
    print("Testing available cameras...")
    available_cameras = []
    
    # Test camera indices 0-9
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                print(f"Camera {i}: Available - Resolution: {width}x{height}")
                available_cameras.append(i)
            else:
                print(f"Camera {i}: Device exists but can't read frame")
            cap.release()
        else:
            print(f"Camera {i}: Not available")
    
    print(f"\nTotal available cameras: {available_cameras}")
    return available_cameras

def test_webcam_helper():
    """Test the WebcamHelper detection"""
    try:
        from webcam_helper import WebcamHelper
        cameras = WebcamHelper.detect_available_cameras()
        print(f"WebcamHelper detected cameras: {cameras}")
          # Try to create a WebcamHelper instance for each camera
        for cam_idx in cameras:
            try:
                webcam = WebcamHelper(device_index=cam_idx)
                print(f"WebcamHelper {cam_idx}: Created successfully")
                # Try to start the camera
                if webcam.starten():
                    print(f"WebcamHelper {cam_idx}: Started successfully")
                    # Try to get a frame
                    frame = webcam.frame_lesen()
                    if frame is not None:
                        print(f"WebcamHelper {cam_idx}: Frame captured successfully - Shape: {frame.shape}")
                    else:
                        print(f"WebcamHelper {cam_idx}: No frame captured")
                    webcam.stoppen()
                else:
                    print(f"WebcamHelper {cam_idx}: Failed to start")
            except Exception as e:
                print(f"WebcamHelper {cam_idx}: Error - {e}")
                
    except Exception as e:
        print(f"Error importing WebcamHelper: {e}")

if __name__ == "__main__":
    print("=== Camera Detection Test ===")
    available = test_available_cameras()
    print("\n=== WebcamHelper Test ===")
    test_webcam_helper()
