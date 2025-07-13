"""
IScan-ControlScript - Main Program (Modular Structure with JSON Camera System)
A GUI application for controlling hardware via an API interface.
This version uses a modular, maintainable structure that's easy to extend.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""

import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

 # Import configuration and components
from config import *
from gui_components import GUIBuilder
from event_handlers import EventHandlers
from queue_operations import QueueOperations
from camera import JSONCameraConfig, JSONCameraStreamManager

# Import existing modules
from api_client import ApiClient
from logger import Logger
from device_control import DeviceControl
from operation_queue import OperationQueue
from webcam_helper import CameraHelper
from angle_calculator_commands import AngleCalculatorInterface


class ControlApp:
    """
    Main application class with modular structure
    Easy to understand, debug, and extend
    """
    
    def __init__(self):
        # ...existing code...
        self.refresh_pending = False  # Debounce flag for camera config refresh
        """Initialize the application"""
        # Create main window
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.setup_window_icon()

        # Initialize variables
        self.init_variables()

        # Initialize camera configuration (JSON-based)
        self.camera_config = JSONCameraConfig("cameras_config.json")
        print("DEBUG: JSON config loaded")
        cameras = self.camera_config.get_enabled_cameras()
        print(f"DEBUG: Loaded cameras from JSON: {cameras}")

        # Initialize JSON Camera Stream Manager
        self.camera_stream_manager = JSONCameraStreamManager("cameras_config.json")

        # Setup available cameras based on JSON config
        self.setup_available_cameras_json()

        # Initialize webcams based on available cameras (before GUI creation)
        self.setup_webcams_json()

        # Create GUI components with the determined camera list
        self.create_all_widgets()

        # Set default camera
        if self.available_cameras:
            self.current_camera_index = self.available_cameras[0]
            self.webcam = self.webcams[self.current_camera_index]

        # Initialize backend modules
        self.init_backend_modules()

        # Initialize helper classes
        self.event_handlers = EventHandlers(self)
        self.queue_ops = QueueOperations(self)

        # Assign all callbacks
        self.event_handlers.assign_all_callbacks()
        
        # Initialize calculator display and load images
        self.initialize_calculator_display()
        
        # Setup close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start JSON file monitoring
        self.start_json_monitoring()
        
        # Start auto-streams if enabled (delayed to ensure GUI is ready)
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            self.root.after(500, self.start_auto_streams)  # Reduced to 0.5 second delay
    
    def setup_window_icon(self):
        """Set up the window icon"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, ICON_FILENAME)
            
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
                self.root.icon_image = icon  # Keep reference
            else:
                print(f"Warning: Icon not found at {icon_path}")
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
    
    def init_variables(self):
        """Initialize all tkinter variables"""
        self.position = tk.DoubleVar(value=0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.base_url_var = tk.StringVar(value=DEFAULT_BASE_URL)
        self.last_distance_value = tk.StringVar(value=DEFAULT_DISTANCE)
        self.repeat_queue = tk.BooleanVar(value=DEFAULT_REPEAT_QUEUE)
        self.global_delay = DEFAULT_AUTOFOCUS_DELAY
    
    def setup_available_cameras_json(self):
        """Setup available cameras based on JSON config"""
        # Get all enabled cameras from JSON configuration (including offline)
        enabled_cameras = self.camera_config.get_enabled_cameras()
        
        print("JSON camera setup:")
        for camera in enabled_cameras:
            connection_info = self.camera_config.parse_connection(camera['connection'])
            print(f"  Index {camera['index']}: {camera['name']} ({camera['connection']}) - {camera['description']}")
            if connection_info:
                print(f"    Hardware: {connection_info}")
        
        # Set available camera indices to all enabled cameras from JSON
        self.available_cameras = [cam['index'] for cam in enabled_cameras]
        print(f"JSON configuration: {len(enabled_cameras)} cameras configured: {self.available_cameras}")
        print(f"JSON configuration: {len(enabled_cameras)} cameras configured: {self.available_cameras}")
        
        # Additionally: Detect physically available cameras for online status
        from webcam_helper import CameraHelper
        physically_available = CameraHelper.detect_available_cameras()
        self.physically_available_cameras = physically_available
        print(f"Physically available cameras: {physically_available}")
        print(f"Physically available cameras: {physically_available}")

    def start_json_monitoring(self):
        """Start monitoring the JSON configuration file for changes"""
        self.json_monitoring_active = True
        self.json_last_modified = self.get_json_modification_time()        
        # Start monitoring thread
        monitoring_thread = threading.Thread(target=self.monitor_json_file, daemon=True)
        monitoring_thread.start()
        
    def get_json_modification_time(self):
        """Get the last modification time of the JSON config file"""
        try:
            # Get the script directory and build absolute path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "camera", "cameras_config.json")
            return os.path.getmtime(config_path)
        except Exception as e:
            print(f"Error getting JSON modification time: {e}")
            return 0
    
    def monitor_json_file(self):
        """Monitor JSON config file for changes in background thread"""
        while self.json_monitoring_active:
            try:
                current_modified = self.get_json_modification_time()
                
                if current_modified > self.json_last_modified:
                    print("JSON configuration changed - updating GUI...")
                    self.json_last_modified = current_modified
                    # Schedule GUI update in main thread
                    self.root.after(100, self.reload_configuration)
                    
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"Error in JSON monitoring: {e}")
                time.sleep(5)  # Wait longer on error
    
    def reload_configuration(self):
        """Reload JSON configuration and completely reinitialize camera system"""
        try:
            print("JSON configuration changed - Performing complete re-initialization...")
            
            # Complete re-initialization of the camera system
            self.reinitialize_camera_streams()
            
            print("Camera system successfully re-initialized after JSON change")
            
        except Exception as e:
            print(f"Error reloading configuration: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Configuration error", 
                               f"Error loading JSON configuration:\n{e}")
    
    def stop_json_monitoring(self):
        """Stop JSON file monitoring"""
        self.json_monitoring_active = False
    
    def update_photo_camera_combo(self):
        """Update photo camera combo box with only online cameras"""
        if hasattr(self, 'photo_camera_combo'):
            try:
                # Clear current values
                self.photo_camera_combo['values'] = ()
                
                # Get online cameras only
                online_cameras = []
                for cam_index in self.available_cameras:
                    # Check if camera is physically available
                    camera_info = self.camera_config.get_camera_by_index(cam_index)
                    hardware_info = self.camera_config.parse_connection(camera_info['connection'])
                    
                    if hardware_info:
                        device_index = hardware_info.get('device_index', cam_index)
                        if device_index in getattr(self, 'physically_available_cameras', []):
                            # Camera is online - add to combo
                            camera_display = f"Cam {cam_index}: {camera_info['name']}"
                            online_cameras.append(camera_display)
                
                # Update combo box values
                if online_cameras:
                    self.photo_camera_combo['values'] = tuple(online_cameras)
                    # Set first online camera as default if nothing selected
                    if not self.photo_camera_combo.get():
                        self.photo_camera_combo.current(0)
                else:
                    self.photo_camera_combo['values'] = ("No online cameras available",)
                    self.photo_camera_combo.current(0)
                
                print(f"Photo combo updated: {len(online_cameras)} online cameras")
                
            except Exception as e:
                print(f"Error updating photo camera combo: {e}")
    
    def refresh_camera_streams_only(self):
        """Refresh camera streams without rebuilding the entire GUI"""
        try:
            print("Refreshing camera streams...")
            
            # Start streams for available cameras
            for cam_index in self.available_cameras:
                if cam_index in self.webcams:
                    webcam = self.webcams[cam_index]
                    if hasattr(webcam, 'start_stream'):
                        try:
                            # Pass the correct panel (camera label) to start_stream
                            panel = self.camera_labels.get(cam_index)
                            if panel is not None:
                                webcam.start_stream(panel)
                                print(f"Stream started for camera {cam_index}")
                            else:
                                print(f"No panel found for camera {cam_index}, cannot start stream.")
                        except Exception as e:
                            print(f"Error starting stream for camera {cam_index}: {e}")
            
            print("Camera streams updated")
            
        except Exception as e:
            print(f"Error updating camera streams: {e}")
    
    def setup_webcams_json(self):
        """Setup webcam instances based on JSON configuration (only for physically available cameras)"""
        self.webcams = {}
        self.current_camera_index = None

        # Get all enabled cameras from JSON
        enabled_cameras = self.camera_config.get_enabled_cameras()

        from webcam_helper import CameraHelper
        for camera in enabled_cameras:
            cam_index = camera.get('index')
            connection_info = self.camera_config.parse_connection(camera.get('connection', ''))
            if not connection_info:
                print(f"Camera index {cam_index}: {camera.get('name', 'Unknown')} - OFFLINE - No connection info")
                continue

            cam_type = connection_info.get('type')
            if cam_type == 'usb':
                device_index = connection_info.get('device_index', None)
                # Only add webcam if device_index is physically available
                if device_index is not None and device_index in getattr(self, 'physically_available_cameras', []):
                    print(f"Initialized JSON camera index {cam_index}: {camera.get('name', 'Unknown')} (USB-{device_index}) - ONLINE")
                    webcam = CameraHelper(
                        device_index=device_index,
                        frame_size=(150, 150),
                        com_port=f"USB-{device_index}",
                        model=camera.get('name', f"Camera {cam_index}")
                    )
                    self.webcams[cam_index] = webcam
                else:
                    print(f"Camera index {cam_index}: {camera.get('name', 'Unknown')} (USB-{device_index}) - OFFLINE - No webcam instance created")
            elif cam_type in ['http', 'rtsp']:
                url = connection_info.get('url', None)
                if url:
                    print(f"Initialized JSON camera index {cam_index}: {camera.get('name', 'Unknown')} ({cam_type.upper()}:{url}) - ONLINE")
                    webcam = CameraHelper(
                        device_index=url,
                        frame_size=(150, 150),
                        com_port=url,
                        model=camera.get('name', f"Camera {cam_index}")
                    )
                    self.webcams[cam_index] = webcam
                else:
                    print(f"Camera index {cam_index}: {camera.get('name', 'Unknown')} ({cam_type}) - OFFLINE - No URL provided")
            else:
                print(f"Camera index {cam_index}: {camera.get('name', 'Unknown')} - Unsupported type '{cam_type}'")

        # Set primary camera to first available online camera
        self.current_camera_index = None
        self.webcam = None
        if self.available_cameras and self.webcams:
            for cam_index in self.available_cameras:
                if cam_index in self.webcams:
                    self.current_camera_index = cam_index
                    self.webcam = self.webcams[cam_index]
                    break
    
    def create_all_widgets(self):
        """Create all GUI widgets using GUIBuilder"""
        # URL input
        self.url_frame, self.base_url_entry = GUIBuilder.create_url_frame(
            self.root, self.base_url_var)
        
        # Camera settings
        (self.camera_settings_frame, self.camera_device_index_var, 
         self.camera_device_entry, self.set_camera_device_btn,
         self.camera_delay_var, self.camera_delay_entry, 
         self.set_delay_btn) = GUIBuilder.create_camera_settings_frame(self.root)
        
        # Diameter input
        self.diameter_frame, self.diameter_entry = GUIBuilder.create_diameter_frame(self.root)
        
        # Position display
        (self.position_frame, self.position_label, 
         self.servo_angle_label) = GUIBuilder.create_position_display(
            self.root, self.position, self.servo_angle_var)
        
        # Main container for 3-column grid layout (Log | Configuration | Queue) + Camera row
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid configuration for 3 columns in first row, camera in bottom left
        self.main_container.columnconfigure(0, weight=1, minsize=300)  # Log console (top) / Camera grid (bottom)
        self.main_container.columnconfigure(1, weight=1, minsize=400)  # Calculator/Config (wider)
        self.main_container.columnconfigure(2, weight=1, minsize=300)  # Queue
        self.main_container.rowconfigure(0, weight=2)  # Main controls row (larger)
        self.main_container.rowconfigure(1, weight=1)  # Camera row (smaller)
        
        # Row 0, Column 0: Log console
        self.log_frame = tk.LabelFrame(self.main_container, text="Log Console", font=("Arial", 10, "bold"))
        self.log_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        self.output = scrolledtext.ScrolledText(self.log_frame, width=35, height=20, state='disabled')
        self.output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Row 0, Column 1: Calculator Commands Panel (Configuration)
        (self.calc_panel, self.calc_vars, 
         self.calc_widgets) = GUIBuilder.create_calculator_commands_panel(
            self.main_container, grid_mode=True)
        
        # Row 0, Column 2: Operation Queue
        (self.queue_frame, self.queue_list, self.queue_exec_btn, self.queue_pause_btn, 
         self.queue_exec_selected_btn, self.queue_clear_btn, self.queue_remove_btn,
         self.queue_duplicate_btn, self.queue_edit_btn, self.queue_settings_btn,
         self.queue_move_up_btn, self.queue_move_down_btn,
         self.queue_export_btn, self.queue_import_btn, self.repeat_checkbox) = GUIBuilder.create_queue_frame(
            self.main_container, self.repeat_queue, grid_mode=True)
        
        # Row 1, Column 0: Camera Grid Display (left bottom)
        (self.webcam_frame, self.camera_labels, self.camera_combo, self.camera_frames,
         self.btn_start_camera, self.btn_stop_camera, self.btn_add_photo_to_queue, 
         self.current_camera_label, self.available_cameras_gui, self.auto_stream_var, 
         self.btn_refresh_cameras) = GUIBuilder.create_webcam_frame(
             self.main_container, 
             available_cameras=self.available_cameras,
             webcams_dict=self.webcams,
             grid_mode=True,
             position="bottom_left")
             
        # Row 1, Column 2: Settings Panel (under Queue)
        (self.settings_frame, self.home_exec_btn, self.home_add_btn,
         self.drive_up_distance, self.drive_up_speed, self.drive_up_exec_btn, self.drive_up_add_btn,
         self.drive_down_distance, self.drive_down_speed, self.drive_down_exec_btn, self.drive_down_add_btn,
         self.photo_camera_combo, self.photo_exec_btn, self.photo_add_btn, self.photo_config_btn) = GUIBuilder.create_settings_panel(
            self.main_container, grid_mode=True)        # Populate photo camera combo box with available cameras from JSON configuration will be done after logger initialization
    
    def init_backend_modules(self):
        """Initialize backend modules (logger, device control, etc.)"""
        # Logger
        self.logger = Logger(
            self.output, 
            self.position, 
            self.servo_angle_var, 
            None  # update_position_label wird nicht verwendet
        )
        
        # Widget dictionary for device control - create necessary control variables
        # Since controls are now in Calculator panel, we need to define these here
        self.servo_angle = tk.DoubleVar(value=0.0)
        self.stepper_length_cm = tk.DoubleVar(value=1.0)
        self.stepper_dir = tk.StringVar(value="forward")
        self.stepper_speed = tk.IntVar(value=int(DEFAULT_SPEED))
        self.led_color = tk.StringVar(value="red")
        self.led_bright = tk.IntVar(value=int(DEFAULT_LED_BRIGHTNESS))
        
        self.widgets = {
            'root': self.root,
            'diameter_entry': self.diameter_entry,
            'servo_angle': self.servo_angle,
            'stepper_length_cm': self.stepper_length_cm,
            'stepper_dir': self.stepper_dir,
            'stepper_speed': self.stepper_speed,
            'led_color': self.led_color,
            'led_bright': self.led_bright,
            'webcam': self.webcam,
            'webcams': self.webcams,  # Add all webcams for camera-specific operations
            'camera_combo': self.camera_combo,  # Add camera combo for switching
            'global_delay': self
        }
        
        # Operation queue
        self.operation_queue = OperationQueue(self.logger, self.queue_list)
        
        # Device control
        self.device_control = DeviceControl(
            self.logger,
            self.base_url_var,
            self.widgets,
            self.position,
            self.servo_angle_var
        )
          # Angle calculator interface
        self.angle_calculator = AngleCalculatorInterface(self.logger)
        
        # Update photo camera combo box now that logger is initialized
        self.update_photo_camera_combo()
    
    def initialize_calculator_display(self):
        """Initialize the calculator display with current values and load images"""
        if hasattr(self, 'event_handlers'):
            # Update command display with initial values
            self.event_handlers.update_command_display()
            # Load initial servo images
            self.event_handlers.load_servo_images()
        
        # Update camera tab labels and info after everything is initialized
        self.update_camera_tab_labels()
        self.update_current_camera_info()
        
    def update_camera_tab_labels(self):
        """Update camera frame labels to show camera configuration information"""
        if hasattr(self, 'camera_frames'):
            for cam_index in self.available_cameras:
                if cam_index in self.camera_frames:
                    camera_frame_info = self.camera_frames[cam_index]
                    # Get camera info from JSON config
                    camera_info = self.get_camera_info(cam_index)
                    
                    # Update frame title
                    frame_title = f"{camera_info['name']}"
                    camera_frame_info['frame'].config(text=frame_title)
    
    def update_current_camera_info(self):
        """Update the current camera info label with detailed information"""
        if hasattr(self, 'current_camera_label') and hasattr(self, 'current_camera_index'):
            camera_info = self.get_camera_info(self.current_camera_index)
            info_text = f"{camera_info['name']} ({camera_info['usb_label']})"
            self.current_camera_label.config(text=info_text)

    def start_camera_stream(self, camera_index):
        """
        Start stream for a specific camera index and ensure it's properly initialized
        """
        import time
        
        try:
            if camera_index in self.available_cameras and camera_index in self.webcams:
                webcam = self.webcams[camera_index]
                
                # Check if stream is already running
                if webcam.running:
                    self.logger.log(f"📹 Kamera {camera_index} Stream bereits aktiv")
                    return True
                  # Start the stream
                if camera_index in self.camera_labels:
                    camera_label = self.camera_labels[camera_index]
                    if webcam.start_stream(camera_label):
                        # Give stream time to initialize
                        time.sleep(0.5)
                        # Verify stream is running
                        if webcam.running:
                            # Don't override the label - let the stream display video frames
                            # The stream_loop in webcam_helper will update the label with video
                            self.logger.log(f"📹 Camera {camera_index} stream started and initialized")
                            return True
                        else:
                            # Show network error for HTTP/RTSP cameras
                            cam_info = self.get_camera_info(camera_index)
                            connection_info = self.camera_config.parse_connection(cam_info.get('connection', ''))
                            cam_type = connection_info.get('type') if connection_info else None
                            if cam_type in ['http', 'rtsp']:
                                camera_label.config(text=f"{cam_info['usb_label']}\nNETWORK ERROR", bg="orange")
                            else:
                                camera_label.config(text=f"{cam_info['usb_label']}\nERROR", bg="lightcoral")
                            self.logger.log(f"⚠️ Camera {camera_index} stream could not be initialized")
                            return False
                    else:
                        # Update label to show error status
                        cam_info = self.get_camera_info(camera_index)
                        connection_info = self.camera_config.parse_connection(cam_info.get('connection', ''))
                        cam_type = connection_info.get('type') if connection_info else None
                        if cam_type in ['http', 'rtsp']:
                            camera_label.config(text=f"{cam_info['usb_label']}\nNETWORK ERROR", bg="orange")
                        else:
                            camera_label.config(text=f"{cam_info['usb_label']}\nERROR", bg="lightcoral")
                        self.logger.log(f"❌ Error starting camera {camera_index}")
                        return False
                else:
                    self.logger.log(f"❌ No label found for camera {camera_index}")
                    return False
            else:
                self.logger.log(f"❌ Camera {camera_index} not available")
                return False
        except Exception as e:
            self.logger.log(f"❌ Error starting camera {camera_index}: {e}")
            return False

    def switch_camera(self, camera_index):
        """
        Switch to the specified camera index for queue operations and ensure stream is running
        """
        try:
            if camera_index in self.available_cameras:
                # First, start the camera stream if not already running
                stream_started = self.start_camera_stream(camera_index)
                
                # Update the current camera index
                self.current_camera_index = camera_index
                
                # Update the camera combo box
                if hasattr(self, 'camera_combo') and self.camera_combo:
                    self.camera_combo.set(str(camera_index))
                
                # Update camera info display
                self.update_current_camera_info()
                
                # Switch the active webcam if available
                if camera_index in self.webcams:
                    self.webcam = self.webcams[camera_index]
                    if stream_started:
                        self.logger.log(f"🎥 Kamera gewechselt zu Index {camera_index} (Stream aktiv)")
                    else:
                        self.logger.log(f"🎥 Kamera gewechselt zu Index {camera_index} (Stream-Fehler)")
                else:
                    self.logger.log(f"⚠️ Kamera {camera_index} nicht verfügbar, verwende aktuelle Kamera")
                    
                return stream_started
                    
            else:
                self.logger.log(f"❌ Ungültiger Kamera-Index: {camera_index}")
                return False
                
        except Exception as e:
            self.logger.log(f"❌ Fehler beim Kamera-Wechsel: {e}")
            return False
    
    def refresh_camera_configuration(self):
        """
        Refresh camera configuration after JSON changes
        This method is called as a callback when the JSON is updated
        Debounced: Only one refresh allowed per event window.
        """
        if self.refresh_pending:
            print("Camera config refresh already pending, skipping duplicate call.")
            return
        self.refresh_pending = True
        try:
            print("Refreshing camera configuration after JSON change...")
            # Stop all current camera streams first
            self.stop_all_camera_streams()
            # Reload camera configuration from JSON
            self.camera_config = JSONCameraConfig("cameras_config.json")
            # Determine new available cameras based on JSON config
            self.setup_available_cameras_json()
            # Recreate webcam instances with new configuration
            self.setup_webcams_json()
            # Refresh only camera streams without rebuilding GUI
            self.root.after(100, self.refresh_camera_streams_only)
            # Update current camera selection if needed
            if self.available_cameras:
                # If current camera is still available, keep it
                if self.current_camera_index not in self.available_cameras:
                    # Switch to first available camera
                    self.current_camera_index = self.available_cameras[0]
                    self.webcam = self.webcams[self.current_camera_index]
            # Update photo camera combo box with new configuration
            self.update_photo_camera_combo()
            print(f"Camera configuration refreshed successfully - {len(self.available_cameras)} cameras available")
        except Exception as e:
            print(f"Error during camera configuration refresh: {e}")
            self.logger.log(f"⚠️ Fehler beim Aktualisieren der Kamera-Konfiguration: {e}")
        finally:
            # Reset flag after a short delay to allow future refreshs
            self.root.after(1000, self._reset_refresh_flag)

    def _reset_refresh_flag(self):
        self.refresh_pending = False

    def stop_all_camera_streams(self):
        """Stop all running camera streams before reconfiguration"""
        if hasattr(self, 'webcams'):
            for cam_index, webcam in self.webcams.items():
                try:
                    if hasattr(webcam, 'stop_stream'):
                        webcam.stop_stream()
                    if hasattr(webcam, 'release'):
                        webcam.release()
                except Exception as e:
                    print(f"Error stopping camera {cam_index}: {e}")

    def refresh_camera_grid(self):
        """Recreate the camera grid with new configuration using grid() layout"""
        if hasattr(self, 'camera_labels') and hasattr(self, 'camera_frames'):
            # Stop all running streams before destroying labels
            print("Stoppe laufende Streams vor Grid-Refresh...")
            for cam_index in list(self.camera_labels.keys()):
                if cam_index in self.webcams:
                    webcam = self.webcams[cam_index]
                    try:
                        if hasattr(webcam, 'running') and webcam.running:
                            webcam.stop_stream()
                            print(f"Stream für Kamera {cam_index} gestoppt")
                    except Exception as e:
                        print(f"Error stopping stream for camera {cam_index}: {e}")
            
            # Clear existing camera grid elements
            for cam_index in list(self.camera_frames.keys()):
                try:
                    self.camera_frames[cam_index]['frame'].destroy()
                except:
                    pass
            self.camera_labels.clear()
            self.camera_frames.clear()

            # Recreate camera grid with new configuration
            if hasattr(self, 'webcam_frame') and self.available_cameras:
                # Find the grid_container (assume it's the first child of webcam_frame)
                grid_container = None
                for child in self.webcam_frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        grid_container = child
                        break
                if grid_container is None:
                    grid_container = tk.Frame(self.webcam_frame)
                    grid_container.pack(fill="both", expand=True)

                # Clear all children from grid_container
                for child in grid_container.winfo_children():
                    child.destroy()

                # Calculate grid dimensions
                num_cameras = len(self.available_cameras)
                cols = min(4, num_cameras)  # Max 4 columns
                rows = (num_cameras + cols - 1) // cols

                # Create new camera tiles using grid layout
                for i, cam_index in enumerate(self.available_cameras):
                    camera_info = self.get_camera_info(cam_index)
                    row = i // cols
                    col = i % cols

                    camera_frame = tk.LabelFrame(grid_container, text=f"Cam {cam_index}", 
                                                font=("Arial", 8, "bold"), relief="ridge", bd=1)
                    camera_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

                    camera_view_frame = tk.Frame(camera_frame, bg="black", width=150, height=150)
                    camera_view_frame.pack_propagate(False)
                    camera_view_frame.pack(padx=2, pady=2)

                    camera_obj = self.camera_config.get_camera_by_index(cam_index)
                    if camera_obj and 'connection' in camera_obj:
                        hardware_info = self.camera_config.parse_connection(camera_obj['connection'])
                        device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                        is_online = device_index in getattr(self, 'physically_available_cameras', [])
                    else:
                        hardware_info = None
                        device_index = cam_index
                        is_online = False


                    # Show only raw video stream, no banner or status text
                    camera_label = tk.Label(camera_view_frame, bg="black", relief="sunken", bd=1)
                    camera_label.pack(fill="both", expand=True)

                    self.camera_labels[cam_index] = camera_label
                    self.camera_frames[cam_index] = {
                        'frame': camera_frame,
                        'view_frame': camera_view_frame
                    }

                # Configure grid weights for even scaling
                for c in range(cols):
                    grid_container.grid_columnconfigure(c, weight=1)
                for r in range(rows):
                    grid_container.grid_rowconfigure(r, weight=1)
    
    def open_camera_config(self):
        """Open camera configuration editor (JSON-based)"""
        self.create_camera_config_editor()
    
    def create_camera_config_editor(self):
        """Create a GUI window for editing JSON camera configuration"""
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext
        import json
        
        # Create configuration window
        config_window = tk.Toplevel(self.root)
        config_window.title("JSON Camera Configuration Editor")
        config_window.geometry("800x600")
        config_window.resizable(True, True)
        
        # Make window modal
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(config_window, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Camera Configuration (JSON)", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Instructions
        info_text = """
Edit the JSON configuration directly below.
Available connection types:
- USB:0, USB:1, USB:2... for USB cameras
- RTSP:rtsp://ip:port/stream for network cameras
- HTTP:http://ip:port/stream for HTTP streams
        """
        info_label = tk.Label(main_frame, text=info_text.strip(), 
                             justify="left", wraplength=760)
        info_label.pack(pady=(0, 10))
        
        # JSON Editor
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        editor_label = tk.Label(editor_frame, text="JSON Configuration:", font=("Arial", 10, "bold"))
        editor_label.pack(anchor="w")
        
        # Text editor with scrollbar
        self.json_editor = scrolledtext.ScrolledText(
            editor_frame, 
            width=80, 
            height=20,
            font=("Consolas", 10),
            wrap="none"
        )
        self.json_editor.pack(fill="both", expand=True, pady=(5, 0))
        
        # Load current configuration
        try:
            current_config = self.camera_config.config_data
            json_text = json.dumps(current_config, indent=2, ensure_ascii=False)
            self.json_editor.insert("1.0", json_text)
        except Exception as e:
            self.json_editor.insert("1.0", f"Fehler beim Laden der Konfiguration: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Validate button
        validate_btn = tk.Button(
            button_frame, 
            text="Validate JSON", 
            command=lambda: self.validate_json_config(self.json_editor),
            bg="lightblue"
        )
        validate_btn.pack(side="left", padx=(0, 5))
        
        # Add camera button
        add_camera_btn = tk.Button(
            button_frame, 
            text="+ Add Camera", 
            command=lambda: self.add_camera_template(self.json_editor),
            bg="lightgreen"
        )
        add_camera_btn.pack(side="left", padx=(0, 5))
        
        # Reset button
        reset_btn = tk.Button(
            button_frame, 
            text="Reset", 
            command=lambda: self.reset_json_editor(self.json_editor),
            bg="orange"
        )
        reset_btn.pack(side="left", padx=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel", 
            command=config_window.destroy
        )
        cancel_btn.pack(side="right", padx=(5, 0))
          # Save button
        save_btn = tk.Button(
            button_frame, 
            text="Save", 
            command=lambda: self.save_json_config(self.json_editor, config_window),
            bg="lightgreen",
            font=("Arial", 10, "bold")
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Save and reload button
        save_reload_btn = tk.Button(
            button_frame, 
            text="Save & Live-Reload", 
            command=lambda: self.save_and_reload_json_config(self.json_editor, config_window),
            bg="orange",
            font=("Arial", 9)
        )
        save_reload_btn.pack(side="right", padx=(5, 0))
          # Center window
        config_window.update_idletasks()
        x = (config_window.winfo_screenwidth() // 2) - (config_window.winfo_width() // 2)
        y = (config_window.winfo_screenheight() // 2) - (config_window.winfo_height() // 2)
        config_window.geometry(f"+{x}+{y}")
    
    def validate_json_config(self, editor):
        """Validate JSON configuration"""
        import json
        from tkinter import messagebox
        
        try:
            json_text = editor.get("1.0", "end-1c")
            config_data = json.loads(json_text)
            
            # Basic structure validation
            if "cameras" not in config_data:
                raise ValueError("'cameras' Schlüssel fehlt in der Konfiguration")
            
            if not isinstance(config_data["cameras"], list):
                raise ValueError("'cameras' muss eine Liste sein")
            
            # Validate each camera
            for i, camera in enumerate(config_data["cameras"]):
                required_fields = ["index", "connection", "name", "enabled"]
                for field in required_fields:
                    if field not in camera:
                        raise ValueError(f"Kamera {i}: Pflichtfeld '{field}' fehlt")
                
                # Validate connection format
                connection = camera["connection"]
                if not any(connection.startswith(prefix) for prefix in ["USB:", "RTSP:", "HTTP:"]):
                    raise ValueError(f"Camera {i}: Invalid connection format '{connection}'. Use USB:, RTSP:, or HTTP:")
            
            messagebox.showinfo("Validierung", "✅ JSON-Konfiguration ist gültig!")
            return True
            
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON-Fehler", f"Ungültiges JSON-Format:\n{e}")
            return False
        except ValueError as e:
            messagebox.showerror("Konfigurationsfehler", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Fehler", f"Unerwarteter Fehler:\n{e}")
            return False
    
    def add_camera_template(self, editor):
        """Add a new camera template to the JSON editor"""
        import json
        from tkinter import messagebox
        
        try:
            # Get current content and parse it
            content = editor.get("1.0", "end-1c")
            config_data = json.loads(content)
            # Find the next available index
            existing_indices = [cam.get('index', 0) for cam in config_data.get('cameras', [])]
            next_index = max(existing_indices) + 1 if existing_indices else 0
            # Create new camera template with dynamic index (all keys in English)
            new_camera = {
                "index": next_index,
                "connection": f"USB:{next_index}",
                "description": f"New camera description {next_index}",
                "name": f"Camera {next_index + 1}",
                "enabled": True,
                "resolution": [640, 480],
                "fps": 30
            }
            # Add the new camera to the config
            if 'cameras' not in config_data:
                config_data['cameras'] = []
            config_data['cameras'].append(new_camera)
            # Convert back to JSON with proper formatting
            new_content = json.dumps(config_data, indent=2, ensure_ascii=False)
            # Update the editor
            editor.delete("1.0", "end")
            editor.insert("1.0", new_content)
            # Scroll to the end to show the new camera
            editor.see("end")
            messagebox.showinfo("Success", f"✅ New camera with index {next_index} added!")
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"Invalid JSON format:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding camera:\n{e}")
    
    def reset_json_editor(self, editor):
        """Reset JSON editor to current saved configuration"""
        from tkinter import messagebox
        import json
        
        if messagebox.askyesno("Reset", "Discard all changes and revert to the saved configuration?"):
            try:
                current_config = self.camera_config.config_data
                json_text = json.dumps(current_config, indent=2, ensure_ascii=False)
                editor.delete("1.0", "end")
                editor.insert("1.0", json_text)
            except Exception as e:
                messagebox.showerror("Error", f"Error during reset: {e}")
    def save_json_config(self, editor, window):
        """Save JSON configuration and apply changes"""
        import json
        from tkinter import messagebox
        
        # First validate
        if not self.validate_json_config(editor):
            return
        
        try:
            # Get the JSON text
            json_text = editor.get("1.0", "end-1c")
            config_data = json.loads(json_text)
            
            # Save to file
            self.camera_config.config_data = config_data
            success = self.camera_config.save_config()
            
            if success:
                # Success messagebox removed as requested
                window.destroy()
                # Just log the change, no immediate refresh to avoid GUI conflicts
                self.logger.log("📷 Camera configuration saved. Restart required for changes.")
            else:
                messagebox.showerror("Error", "❌ Error saving configuration!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving:\n{e}")
    
    def save_and_reload_json_config(self, editor, window):
        """Save JSON configuration and apply changes immediately (live-reload)"""
        import json
        from tkinter import messagebox

        # First validate
        if not self.validate_json_config(editor):
            return

        try:
            # Get the JSON text
            json_text = editor.get("1.0", "end-1c")
            config_data = json.loads(json_text)

            # Save to file
            self.camera_config.config_data = config_data
            success = self.camera_config.save_config()

            if success:
                window.destroy()
                # Only trigger one refresh after saving
                self.refresh_pending = False
                self.root.after(500, self.refresh_camera_configuration)
                self.logger.log("📷 Camera configuration saved and applied live.")
            else:
                messagebox.showerror("Error", "❌ Error saving configuration!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving:\n{e}")
    
    def get_camera_info(self, cam_index):
        """Get camera information for display - JSON-based"""
        if hasattr(self, 'camera_config'):
            # Try to get info from JSON config
            camera = self.camera_config.get_camera_by_index(cam_index)
            if camera:
                hardware_info = self.camera_config.parse_connection(camera['connection'])
                device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                
                return {
                    'name': camera.get('name', f"Camera {cam_index}"),
                    'bezeichnung': camera.get('name', f"Camera {cam_index}"),
                    'usb_label': f"USB-{device_index}",
                    'description': camera.get('description', f"USB Camera {cam_index}")
                }
        
        # Fallback to default values
        return {
            'name': f"Camera {cam_index}",
            'bezeichnung': f"Camera {cam_index}",
            'usb_label': f"USB-{cam_index}",
            'description': f"USB Camera {cam_index}"
        }
    
    def start_auto_streams(self):
        """Start all camera streams automatically if auto-stream is enabled"""
        print("DEBUG: start_auto_streams called")
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            self.logger.log("🎬 Starting automatic camera streams...")
            success_count = 0
            total_cameras = len(self.available_cameras)
            
            for cam_index in self.available_cameras:
                try:
                    print(f"DEBUG: Starting auto-stream for camera {cam_index}")
                    if self.start_camera_stream(cam_index):
                        success_count += 1
                        print(f"DEBUG: Auto-stream started successfully for camera {cam_index}")
                    else:
                        print(f"DEBUG: Failed to start auto-stream for camera {cam_index}")
                except Exception as e:
                    print(f"DEBUG: Exception starting auto-stream for camera {cam_index}: {e}")
                    self.logger.log(f"❌ Auto-stream error camera {cam_index}: {e}")
            
            self.logger.log(f"🎬 Auto-streams: {success_count}/{total_cameras} cameras started")
        else:
            print("DEBUG: Auto-stream is disabled")

    def stop_auto_streams(self):
        """Stop all camera streams"""
        self.logger.log("⏹️ Stopping all camera streams...")
        stopped_count = 0
        
        for cam_index in self.available_cameras:
            if cam_index in self.webcams:
                webcam = self.webcams[cam_index]
                try:
                    if webcam.running:
                        webcam.stop_stream()
                        stopped_count += 1
                        # Update label to show offline status
                        if cam_index in self.camera_labels:
                            cam_info = self.get_camera_info(cam_index)
                            self.camera_labels[cam_index].config(text=f"{cam_info['usb_label']}\nOFFLINE", bg="gray")
                except Exception as e:
                    self.logger.log(f"❌ Error stopping camera {cam_index}: {e}")
        
        self.logger.log(f"⏹️ {stopped_count} Kamera-Streams gestoppt")

    def toggle_auto_streams(self):
        """Toggle auto-streams on/off"""
        if hasattr(self, 'auto_stream_var'):
            if self.auto_stream_var.get():
                self.start_auto_streams()
            else:
                self.stop_auto_streams()

    def refresh_cameras(self):
        """Refresh camera list and restart streams if auto-stream is enabled"""
        self.logger.log("🔄 Aktualisiere Kamera-Liste...")
        
        # Stop current streams
        self.stop_auto_streams()
        
        # Refresh configuration
        self.refresh_camera_configuration()
          # If auto-stream was enabled, restart streams
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            self.root.after(1000, self.start_auto_streams)  # Give time for camera release
        
        self.logger.log(f"🔄 Kamera-Liste aktualisiert: {len(self.available_cameras)} Kameras verfügbar")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop JSON monitoring
            if hasattr(self, 'json_monitoring_active'):
                self.stop_json_monitoring()
            
            # Stop all camera streams first
            if hasattr(self, 'webcams'):
                for cam_index, webcam in self.webcams.items():
                    try:
                        if hasattr(webcam, 'stop_stream'):
                            webcam.stop_stream()
                        if hasattr(webcam, 'release'):
                            webcam.release()
                    except Exception as e:
                        print(f"Error stopping camera {cam_index}: {e}")
            
            # Try to log closure, but don't fail if widgets are destroyed
            try:
                if hasattr(self, 'logger'):
                    self.logger.log("Schließe Anwendung...")
            except:
                print("Schließe Anwendung...")
            
            # Close the application
            try:
                self.root.quit()
            except:
                pass
            
            try:
                self.root.destroy()
            except:
                pass
                
        except Exception as e:
            print(f"Error during closing: {e}")
            try:
                self.root.destroy()
            except:
                pass

    def run(self):
        """Start the main application loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Anwendung beendet durch Benutzer")
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
        finally:
            self.on_closing()

    def update_camera_tiles_gentle(self):
        """Gently update camera tiles without destroying the entire grid"""
        if not hasattr(self, 'camera_labels') or not hasattr(self, 'camera_frames'):
            # If no existing grid, create it from scratch
            self.refresh_camera_grid()
            return
        
        # Get current enabled cameras from JSON
        current_enabled_cameras = set(self.available_cameras)
        
        # Get cameras that currently have tiles
        existing_cameras = set(self.camera_frames.keys())
        
        # Find cameras to add and remove
        cameras_to_add = current_enabled_cameras - existing_cameras
        cameras_to_remove = existing_cameras - current_enabled_cameras
        
        print(f"Sanfte Kachel-Aktualisierung:")
        print(f"  Zu entfernen: {cameras_to_remove}")
        print(f"  Hinzuzufügen: {cameras_to_add}")
        print(f"  Bleiben: {existing_cameras & current_enabled_cameras}")
        
        # Remove tiles for disabled cameras
        for cam_index in cameras_to_remove:
            if cam_index in self.camera_frames:
                try:
                    # Destroy the camera frame
                    self.camera_frames[cam_index]['frame'].destroy()
                    # Remove from dictionaries
                    del self.camera_frames[cam_index]
                    if cam_index in self.camera_labels:
                        del self.camera_labels[cam_index]
                    print(f"  Kachel für Kamera {cam_index} entfernt")
                except Exception as e:
                    print(f"  Fehler beim Entfernen der Kachel {cam_index}: {e}")
        
        # Add tiles for new cameras
        if cameras_to_add and hasattr(self, 'webcam_frame'):
            # Find or create grid container
            grid_container = None
            for child in self.webcam_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    grid_container = child
                    break
            
            if not grid_container:
                grid_container = tk.Frame(self.webcam_frame)
                grid_container.pack(fill="both", expand=True)
            
            # Add new camera tiles
            for cam_index in cameras_to_add:
                self.add_single_camera_tile(grid_container, cam_index)
                print(f"  Kachel für Kamera {cam_index} hinzugefügt")
        
        # Update status of existing tiles (online/offline)
        for cam_index in (existing_cameras & current_enabled_cameras):
            self.update_camera_tile_status(cam_index)
    
    def add_single_camera_tile(self, grid_container, cam_index):
        """Add a single camera tile to the grid"""
        try:
            # Get camera info
            camera_info = self.get_camera_info(cam_index)
            
            # Create a frame for this camera
            camera_row_frame = tk.Frame(grid_container)
            camera_row_frame.pack(side='top', fill='x', padx=2, pady=2)
            
            # Individual camera frame - compact size
            camera_frame = tk.LabelFrame(camera_row_frame, text=f"Cam {cam_index}", 
                                        font=("Arial", 8, "bold"), relief="ridge", bd=1)
            camera_frame.pack(side='left', padx=2, pady=2)
            
            # Camera view area - 150x150 max size
            camera_view_frame = tk.Frame(camera_frame, bg="black", width=150, height=150)
            camera_view_frame.pack_propagate(False)  # Keep fixed size
            camera_view_frame.pack(padx=2, pady=2)
            
            # Check if camera is physically available
            camera_obj = self.camera_config.get_camera_by_index(cam_index)
            if camera_obj and 'connection' in camera_obj:
                hardware_info = self.camera_config.parse_connection(camera_obj['connection'])
                device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                is_online = device_index in getattr(self, 'physically_available_cameras', [])
            else:
                hardware_info = None
                device_index = cam_index
                is_online = False
            
            # Camera display label with online/offline status
            if is_online:
                bg_color = "gray"
                status_text = "OFFLINE"  # Will be updated when stream starts
                fg_color = "white"
            else:
                bg_color = "#8B0000"  # Dark red
                status_text = "NICHT VERFÜGBAR"
                fg_color = "white"
            
            camera_label = tk.Label(camera_view_frame, 
                                   text=f"{camera_info['usb_label']}\n{status_text}", 
                                   bg=bg_color, fg=fg_color, relief="sunken", bd=1,
                                   font=("Arial", 8))
            camera_label.pack(fill="both", expand=True)
              # Store references
            self.camera_labels[cam_index] = camera_label
            self.camera_frames[cam_index] = {
                'frame': camera_frame,
                'view_frame': camera_view_frame
            }
            
        except Exception as e:
            print(f"Fehler beim Hinzufügen der Kachel {cam_index}: {e}")
    
    def update_camera_tile_status(self, cam_index):
        """Update the status of an existing camera tile"""
        if cam_index not in self.camera_labels:
            return
        
        try:
            # Check if camera is physically available
            camera_obj = self.camera_config.get_camera_by_index(cam_index)
            if camera_obj and 'connection' in camera_obj:
                hardware_info = self.camera_config.parse_connection(camera_obj['connection'])
                device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                is_online = device_index in getattr(self, 'physically_available_cameras', [])
            else:
                hardware_info = None
                device_index = cam_index
                is_online = False

            camera_info = self.get_camera_info(cam_index)
            camera_label = self.camera_labels[cam_index]

            # Check if camera stream is running - don't override video display
            if cam_index in self.webcams:
                webcam = self.webcams[cam_index]
                if hasattr(webcam, 'running') and webcam.running:
                    # Stream is running - don't override the video display
                    return

            # Update color and text based on online status only if stream is not running
            if is_online:
                bg_color = "gray"
                status_text = "OFFLINE"  # Will be updated when stream starts
                fg_color = "white"
            else:
                bg_color = "#8B0000"  # Dark red
                status_text = "NICHT VERFÜGBAR"
                fg_color = "white"

            camera_label.configure(
                text=f"{camera_info['usb_label']}\n{status_text}",
                bg=bg_color,
                fg=fg_color
            )

        except Exception as e:
            print(f"Error updating tile {cam_index}: {e}")

    def reinitialize_camera_streams(self):
        """
        Komplette Neu-Initialisierung des Kamera-Stream-Bereichs
        Funktioniert wie ein Neustart des Kamera-Systems mit neuen JSON-Daten
        """
        print("=== KOMPLETTE NEU-INITIALISIERUNG DES KAMERA-SYSTEMS ===")
        
        try:
            # Step 1: Stop all running streams and release camera instances
            print("Schritt 1: Stoppe alle Streams und gebe Ressourcen frei...")
            if hasattr(self, 'webcams'):
                for cam_index, webcam in self.webcams.items():
                    try:
                        if hasattr(webcam, 'running') and webcam.running:
                            webcam.stop_stream()
                            print(f"  Stream für Kamera {cam_index} gestoppt")
                        if hasattr(webcam, 'release'):
                            webcam.release()
                            print(f"  Ressourcen für Kamera {cam_index} freigegeben")
                    except Exception as e:
                        print(f"  Error stopping/releasing camera {cam_index}: {e}")
            
            # Schritt 2: Alle Kamera-GUI-Elemente entfernen
            print("Schritt 2: Entferne alle Kamera-GUI-Elemente...")
            if hasattr(self, 'camera_labels'):
                self.camera_labels.clear()
            if hasattr(self, 'camera_frames'):
                for cam_index, frame_data in self.camera_frames.items():
                    try:
                        frame_data['frame'].destroy()
                    except:
                        pass
                self.camera_frames.clear()
            
            # Webcam-Frame komplett leeren
            if hasattr(self, 'webcam_frame'):
                for child in self.webcam_frame.winfo_children():
                    try:
                        child.destroy()
                    except:
                        pass
            
            # Schritt 3: Kamera-System komplett neu aufbauen (wie beim Programmstart)
            print("Schritt 3: Baue Kamera-System neu auf...")
            
            # JSON-Konfiguration neu laden
            self.camera_config = JSONCameraConfig("cameras_config.json")
            
            # Verfügbare Kameras neu ermitteln
            self.setup_available_cameras_json()
            
            # Webcam-Instanzen neu erstellen
            self.setup_webcams_json()
            
            # Schritt 4: GUI komplett neu erstellen
            print("Schritt 4: Erstelle Kamera-GUI neu...")
            self.recreate_camera_gui_completely()
            
            # Schritt 5: Photo-Combo aktualisieren
            self.update_photo_camera_combo()
            
            # Step 6: Start auto-streams (if enabled)
            if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
                print("Schritt 6: Starte Auto-Streams...")
                self.root.after(1000, self.start_auto_streams)  # 1 Sekunde warten für GUI-Setup
            
            print("=== KAMERA-SYSTEM NEU-INITIALISIERUNG ABGESCHLOSSEN ===")
            
        except Exception as e:
            print(f"Fehler bei der Kamera-System Neu-Initialisierung: {e}")
            import traceback
            traceback.print_exc()
    
    def recreate_camera_gui_completely(self):
        """
        Erstellt die Kamera-GUI komplett neu, basierend auf aktueller JSON-Konfiguration
        Simuliert die ursprüngliche GUI-Erstellung beim Programmstart
        """
        print("Erstelle Kamera-GUI komplett neu...")
        
        if not hasattr(self, 'webcam_frame') or not self.available_cameras:
            print("Keine Kameras verfügbar oder webcam_frame nicht vorhanden")
            return
        
        # Haupt-Container für das Kamera-Grid erstellen
        main_container = tk.Frame(self.webcam_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Grid-Container erstellen
        grid_container = tk.Frame(main_container)
        grid_container.pack(fill="both", expand=True)
        
        # Grid-Dimensionen berechnen
        num_cameras = len(self.available_cameras)
        cols = min(4, num_cameras)  # Maximal 4 Spalten
        rows = (num_cameras + cols - 1) // cols
        
        print(f"Erstelle Grid für {num_cameras} Kameras: {rows}x{cols}")
        
        # Kamera-Kacheln erstellen (basierend auf JSON-Konfiguration)
        for i, cam_index in enumerate(self.available_cameras):
            row = i // cols
            col = i % cols
            
            # Kamera-Info aus JSON holen
            camera_info = self.get_camera_info(cam_index)
            
            # Kamera-Frame erstellen
            camera_frame = tk.LabelFrame(grid_container, text=f"Cam {cam_index}", 
                                        font=("Arial", 8, "bold"), relief="ridge", bd=1)
            camera_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Kamera-Ansichts-Frame erstellen
            camera_view_frame = tk.Frame(camera_frame, bg="black", width=150, height=150)
            camera_view_frame.pack_propagate(False)
            camera_view_frame.pack(padx=2, pady=2)
            
            # Online/Offline-Status prüfen
            camera_obj = self.camera_config.get_camera_by_index(cam_index)
            if camera_obj and 'connection' in camera_obj:
                hardware_info = self.camera_config.parse_connection(camera_obj['connection'])
                device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                is_online = device_index in getattr(self, 'physically_available_cameras', [])
            else:
                hardware_info = None
                device_index = cam_index
                is_online = False
            
            # Kamera-Label mit initialem Status erstellen

            # Show only raw video stream, no banner or status text
            camera_label = tk.Label(camera_view_frame, bg="black", relief="sunken", bd=1)
            camera_label.pack(fill="both", expand=True)

            # Store references
            if not hasattr(self, 'camera_labels'):
                self.camera_labels = {}
            if not hasattr(self, 'camera_frames'):
                self.camera_frames = {}

            self.camera_labels[cam_index] = camera_label
            self.camera_frames[cam_index] = {
                'frame': camera_frame,
                'view_frame': camera_view_frame
            }

            print(f"  Camera {cam_index} GUI created - {'ONLINE' if is_online else 'OFFLINE'}")
        
        # Grid-Gewichte für gleichmäßige Skalierung setzen
        for c in range(cols):
            grid_container.grid_columnconfigure(c, weight=1)
        for r in range(rows):
            grid_container.grid_rowconfigure(r, weight=1)
        
        # Kontroll-Buttons-Frame erstellen (falls nicht vorhanden)
        control_frame = tk.Frame(main_container)
        control_frame.pack(fill="x", pady=(5, 0))
        
        # Auto-Stream-Checkbox (falls nicht vorhanden)
        if not hasattr(self, 'auto_stream_var'):
            self.auto_stream_var = tk.BooleanVar(value=True)
        
        auto_stream_check = tk.Checkbutton(control_frame, text="Auto-Stream", 
                                         variable=self.auto_stream_var, font=("Arial", 9))
        auto_stream_check.pack(side=tk.LEFT)
        
        print("Kamera-GUI komplett neu erstellt")


# Entry point for the application
if __name__ == "__main__":
    print("=" * 48)
    print("I-Scan Control Software - Modular Version")
    print("=" * 48)
    print("Starting modular I-Scan application...")
    print("Features: Thread-safe camera, Non-blocking operations")
    print()
    
    try:
        # Create and run the application
        app = ControlApp()
        app.root.mainloop()
        
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
        input("Application closed. Press any key to exit...")
        
    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user")
        
    finally:
        print("Application closed. Press any key to exit...")
        input()
