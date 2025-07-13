"""
WEBCAM HELPER MODULE
====================
Provides functions for controlling and displaying a webcam stream.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 1.1 - Improved thread safety for GUI updates
"""
import os
import cv2
import time
import threading
from datetime import datetime
from PIL import Image, ImageTk
import numpy as np


class CameraHelper:
    """
    Class for controlling a webcam via OpenCV
    Provides methods for displaying the camera stream and capturing images
    """
    
    @staticmethod
    def detect_available_cameras(max_cameras=10):
        """
        Detect all available cameras in the system
        
        Args:
            max_cameras (int): Maximum number of camera indices to test
        Returns:
            list: List of available camera indices
        """
        available_cameras = []
        
        # Suppress OpenCV error messages
        cv2.setLogLevel(0)  # 0 = silent
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Test if we can actually read frames
                ret, frame = cap.read()
                if ret and frame is not None:
                    available_cameras.append(i)
                cap.release()
        # Reset OpenCV logging to default
        cv2.setLogLevel(1)  # 1 = error level
        
        return available_cameras if available_cameras else [0]  # Fallback to index 0
    
    def __init__(self, device_index=0, frame_size=(320, 240), com_port=None, model=None):
        """
        Initialize the webcam with the given device index and frame size
        
        Args:
            device_index (int): Index of the camera to use (default: 0)
            frame_size (tuple): Size of the displayed frame (width, height)
            com_port (str, optional): COM port of the camera
            model (str, optional): Model name of the camera
        """
        self.device_index = device_index
        self.frame_size = frame_size
        self.com_port = com_port or f"COM{device_index + 1}"  # Fallback
        self.model = model or f"Camera {device_index}"  # Fallback
        self.cap = None
        self.running = False
        self.current_frame = None
        self.thread = None
        self.image_counter = 0
    
    def start_camera(self):
        """
        Start and initialize the camera
        
        Returns:
            bool: True if successfully initialized, else False
        """
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            return False
        self.running = True
        return True
    
    def stop_camera(self):
        """
        Stop the camera stream and release resources
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
        self.cap = None
    
    def read_frame(self):
        """
        Read a single frame from the camera
        
        Returns:
            numpy.ndarray: The read frame or None on error
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
    
    def stream_loop(self, panel, fps=30):
        """
        Main loop for the camera stream
        Runs in a separate thread to avoid blocking the GUI
        
        Args:
            panel: The label widget for displaying the stream
            fps (int): Desired frame rate for the stream
        """
        delay = max(1, int(1000 / fps))
        while self.running:
            try:
                frame = self.read_frame()
                if frame is not None:
                    # Scale frame to square for display
                    self.current_frame = frame.copy()  # Copy original frame
                    frame_square = self._make_square_frame(frame, self.frame_size)
                    # Convert from BGR to RGB for tkinter
                    frame_rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)
                    # Convert to Pillow format
                    img = Image.fromarray(frame_rgb)
                    # Convert to Tkinter-compatible format
                    img_tk = ImageTk.PhotoImage(image=img)
                    # GUI update via after() for thread safety
                    panel.after(0, self._update_panel, panel, img_tk)
                # Short wait to achieve desired framerate
                time.sleep(delay / 1000.0)
            except Exception as e:
                print(f"Unexpected error in stream loop: {e}")
                break
    
    def _update_panel(self, panel, img_tk):
        """
        Thread-safe GUI update method
        Executed by the main thread
        """
        try:
            # Check several conditions before updating
            if (self.running and 
                hasattr(panel, 'winfo_exists') and 
                panel.winfo_exists() and
                hasattr(panel, 'config')):
                panel.config(image=img_tk)
                panel.image = img_tk  # Keep reference to prevent garbage collection
        except Exception as e:
            # Stop stream if widget no longer exists or is invalid
            error_msg = str(e).lower()
            if any(x in error_msg for x in ["invalid command name", "application has been destroyed", "bad window path"]):
                self.running = False  # Stop stream
            else:
                print(f"Unexpected GUI update error: {e}")
                self.running = False

    def start_stream(self, panel):
        """
        Start camera stream in a separate thread
        
        Args:
            panel: The label widget for displaying the stream
        Returns:
            bool: True if successfully initialized, else False
        """
        if self.start_camera():
            self.thread = threading.Thread(target=self.stream_loop, args=(panel,))
            self.thread.daemon = True  # Set thread as daemon so it ends with main program
            self.thread.start()
            return True
        return False
    
    def capture_image(self, delay=0.2):
        """
        Capture the current camera image and save it as a PNG file in the 'pictures' folder.
        Performs a delay after capture.
        Returns the path to the saved file.
        
        Args:
            delay (float): Pause after capture in seconds (default: 0.2)
        """
        # Short delay before capture so camera can provide a new frame
        time.sleep(delay)
        # Try to read a current frame directly from the camera
        frame = self.read_frame()
        if frame is not None:
            pictures_dir = os.path.join(os.getcwd(), "pictures")
            os.makedirs(pictures_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.png"
            filepath = os.path.join(pictures_dir, filename)
            cv2.imwrite(filepath, frame)
            return filepath
        return None
    
    def _make_square_frame(self, frame, target_size):
        """
        Create a square frame from the input frame
        Maintains aspect ratio and adds black bars if needed
        
        Args:
            frame: Input frame from the camera
            target_size: Tuple (width, height) for target size
        Returns:
            Square frame with black bars if needed
        """
        height, width = frame.shape[:2]
        target_width, target_height = target_size
        
        # Determine the smaller dimension for square scaling
        min_target = min(target_width, target_height)
        # Calculate scale factor based on the larger original dimension
        scale_factor = min_target / max(width, height)
        # Calculate new dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        # Scale frame
        resized_frame = cv2.resize(frame, (new_width, new_height))
        # Create square background (black)
        square_frame = np.zeros((min_target, min_target, 3), dtype=np.uint8)
        # Calculate centered position
        start_x = (min_target - new_width) // 2
        start_y = (min_target - new_height) // 2
        # Place resized frame in the center of the square frame
        square_frame[start_y:start_y + new_height, start_x:start_x + new_width] = resized_frame
        return square_frame
    
    def stop_stream(self):
        """
        Safely stop the camera stream
        """
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)  # Wait max 1 second
    
    def release(self):
        """
        Release all camera resources
        """
        self.stop_stream()
        if self.cap:
            self.cap.release()
            self.cap = None
