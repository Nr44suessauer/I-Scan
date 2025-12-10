import cv2

def list_cameras():
    # Try indices 0 through 10 to find cameras
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow on Windows
        if cap.isOpened():
            # Get camera info
            ret, frame = cap.read()
            if ret:
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                print(f"\nFound camera at index {i}:")
                print(f"Resolution: {width}x{height}")
                # Try to get camera name (Windows only)
                backend = cv2.CAP_DSHOW
                cap_backend = cv2.VideoCapture(i + backend)
                if cap_backend.isOpened():
                    print(f"Camera name: {cap_backend.getBackendName()}")
                cap_backend.release()
            else:
                print(f"\nCamera at index {i} found but cannot read frames")
            cap.release()
        else:
            print(f"No camera at index {i}")

if __name__ == "__main__":
    print("Scanning for connected cameras...")
    print("Note: USB:X in cameras_config.json should use the index number shown below")
    print("=" * 50)
    list_cameras()
    print("\nPress Enter to exit...")
    input()