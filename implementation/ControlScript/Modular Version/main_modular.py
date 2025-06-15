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
from webcam_helper import WebcamHelper
from angle_calculator_commands import AngleCalculatorInterface


class ControlApp:
    """
    Main application class with modular structure
    Easy to understand, debug, and extend
    """
    
    def __init__(self):
        """Initialize the application"""
        # Create main window
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.setup_window_icon()
        
        # Initialize variables
        self.init_variables()
          # Initialize camera configuration (JSON-based)
        self.camera_config = JSONCameraConfig("cameras_config.json")
        print("DEBUG: JSON Config loaded")
        cameras = self.camera_config.get_enabled_cameras()
        print(f"DEBUG: Loaded cameras from JSON: {cameras}")        # Initialize JSON Camera Stream Manager
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
        # Hole verfügbare Kameras aus JSON-Konfiguration
        available_cameras = self.camera_config.get_available_cameras()
        
        print("JSON-Kamera-Setup:")
        for camera in available_cameras:
            hardware_info = camera['hardware_interface']
            print(f"  Index {camera['index']}: {camera['name']} ({camera['verbindung']}) - {camera['beschreibung']}")
            print(f"    Hardware: {hardware_info}")
        
        # Setze verfügbare Kamera-Indices
        self.available_cameras = [cam['index'] for cam in available_cameras]
        print(f"JSON-Konfiguration: {len(available_cameras)} Kameras verfügbar: {self.available_cameras}")

    def setup_webcams_json(self):
        """Setup webcam instances based on JSON configuration (for compatibility)"""
        self.webcams = {}
        self.current_camera_index = 0
        
        available_cameras = self.camera_config.get_available_cameras()
        
        for camera_config in available_cameras:
            cam_index = camera_config['index']
            hardware_info = camera_config['hardware_interface']
            
            if hardware_info.get('type') == 'usb':
                device_index = hardware_info.get('device_index', 0)
                
                print(f"Initialisiere JSON-Kamera Index {cam_index}: {camera_config['name']} (USB-{device_index})")
                  # Erstelle WebcamHelper-Instanz für Kompatibilität
                from webcam_helper import WebcamHelper
                webcam = WebcamHelper(
                    device_index=device_index,
                    frame_size=(150, 150),
                    com_port=f"USB-{device_index}",
                    model=camera_config['name']
                )
                self.webcams[cam_index] = webcam
        
        # Setze primäre Kamera
        if self.available_cameras:
            self.current_camera_index = self.available_cameras[0]
            self.webcam = self.webcams[self.current_camera_index]
    
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
            self.main_container, grid_mode=True)
            
        # Populate photo camera combo box with available cameras
        if self.photo_camera_combo and self.available_cameras:
            camera_indices = [str(idx) for idx in self.available_cameras]
            self.photo_camera_combo['values'] = camera_indices
            if camera_indices:
                self.photo_camera_combo.set(camera_indices[0])  # Set default to first available camera
    
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
                    if webcam.stream_starten(camera_label):
                        # Give stream time to initialize
                        time.sleep(0.5)
                        
                        # Verify stream is running
                        if webcam.running:
                            # Update label to show streaming status
                            cam_info = self.get_camera_info(camera_index)
                            camera_label.config(text=f"{cam_info['usb_label']}\nLIVE", bg="lightgreen")
                            self.logger.log(f"📹 Kamera {camera_index} Stream gestartet und initialisiert")
                            return True
                        else:
                            self.logger.log(f"⚠️ Kamera {camera_index} Stream konnte nicht initialisiert werden")
                            return False
                    else:
                        # Update label to show error status
                        cam_info = self.get_camera_info(camera_index)
                        camera_label.config(text=f"{cam_info['usb_label']}\nERROR", bg="lightcoral")
                        self.logger.log(f"❌ Fehler beim Starten von Kamera {camera_index}")
                        return False
                else:
                    self.logger.log(f"❌ Kein Label für Kamera {camera_index} gefunden")
                    return False
            else:
                self.logger.log(f"❌ Kamera {camera_index} nicht verfügbar")
                return False
                
        except Exception as e:
            self.logger.log(f"❌ Fehler beim Starten der Kamera {camera_index}: {e}")
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
        """
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
            
            print(f"Camera configuration refreshed successfully - {len(self.available_cameras)} cameras available")
            
        except Exception as e:
            print(f"Error during camera configuration refresh: {e}")
            self.logger.log(f"⚠️ Fehler beim Aktualisieren der Kamera-Konfiguration: {e}")

    def safe_refresh_camera_grid(self):
        """Safely refresh the camera grid display"""
        try:
            self.refresh_camera_grid()
        except Exception as e:
            print(f"Error refreshing camera grid: {e}")
            # Try to rebuild the grid completely
            try:
                self.setup_camera_grid()
            except Exception as e2:
                print(f"Error rebuilding camera grid: {e2}")

    def refresh_camera_streams_only(self):
        """Refresh only the camera streams without rebuilding the GUI"""
        try:
            print("Refreshing camera streams only...")
            
            # For each existing camera widget, restart the stream if camera is available
            if hasattr(self, 'camera_labels') and hasattr(self, 'webcams'):
                for cam_index in list(self.camera_labels.keys()):
                    try:
                        # Stop existing stream for this camera
                        if cam_index in self.webcams:
                            webcam = self.webcams[cam_index]
                            if hasattr(webcam, 'stop_stream'):
                                webcam.stop_stream()
                        
                        # Check if camera is still available in new config
                        if cam_index in self.available_cameras and cam_index in self.webcams:
                            # Get the existing label widget
                            camera_label = self.camera_labels[cam_index]
                            
                            # Start the stream for this camera
                            webcam = self.webcams[cam_index]
                            if webcam:
                                success = webcam.stream_starten(camera_label)
                                if success:
                                    camera_info = self.get_camera_info(cam_index)
                                    print(f"Stream restarted for camera {cam_index}: {camera_info['name']}")
                                else:
                                    print(f"Failed to restart stream for camera {cam_index}")
                                    # Update label to show offline status
                                    camera_info = self.get_camera_info(cam_index)
                                    camera_label.config(text=f"{camera_info['usb_label']}\nOFFLINE")
                        else:
                            # Camera no longer available, show offline
                            if cam_index in self.camera_labels:
                                camera_label = self.camera_labels[cam_index]
                                camera_label.config(text=f"Cam {cam_index}\nOFFLINE", bg="gray")
                                
                    except Exception as e:
                        print(f"Error restarting stream for camera {cam_index}: {e}")
            
            print(f"Camera streams refreshed - {len(self.available_cameras)} cameras available")
            
        except Exception as e:
            print(f"Error during camera stream refresh: {e}")
            self.logger.log(f"⚠️ Fehler beim Aktualisieren der Kamera-Streams: {e}")

    # ...existing code...
        self.update_camera_tab_labels()
        self.update_current_camera_info()
        
        # Update camera combo box
        if hasattr(self, 'camera_combo'):
            self.camera_combo['values'] = [str(cam) for cam in self.available_cameras]
            self.camera_combo.set(str(self.current_camera_index) if self.available_cameras else "0")
        
        # Restart auto-streams if enabled
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            self.root.after(500, self.start_auto_streams)
        
        print(f"Camera configuration refreshed. Available cameras: {self.available_cameras}")

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
        """Recreate the camera grid with new configuration"""
        if hasattr(self, 'camera_labels') and hasattr(self, 'camera_frames'):
            # Clear existing camera grid elements
            for cam_index in list(self.camera_frames.keys()):
                try:
                    self.camera_frames[cam_index]['frame'].destroy()
                except:
                    pass
            
            # Clear the dictionaries
            self.camera_labels.clear()
            self.camera_frames.clear()
            
            # Recreate camera grid with new configuration
            if hasattr(self, 'webcam_frame') and self.available_cameras:
                # Clear all children from webcam_frame first
                for child in self.webcam_frame.winfo_children():
                    try:
                        child.destroy()
                    except:
                        pass
                
                # Create new grid container
                grid_container = tk.Frame(self.webcam_frame)
                grid_container.pack(fill="both", expand=True)
                
                # Calculate grid dimensions
                num_cameras = len(self.available_cameras)
                cols = min(4, num_cameras)  # Max 4 columns
                rows = (num_cameras + cols - 1) // cols
                
                # Create new camera tiles using pack layout instead of grid
                for i, cam_index in enumerate(self.available_cameras):
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
                    
                    # Camera display label - zeige USB-Label im Stream
                    camera_label = tk.Label(camera_view_frame, text=f"{camera_info['usb_label']}\nOFFLINE", 
                                           bg="gray", fg="white", relief="sunken", bd=1,
                                           font=("Arial", 8))
                    camera_label.pack(fill="both", expand=True)
                    
                    # Store references
                    self.camera_labels[cam_index] = camera_label
                    self.camera_frames[cam_index] = {
                        'frame': camera_frame,
                        'view_frame': camera_view_frame
                    }

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
        config_window.title("JSON Kamera-Konfiguration Editor")
        config_window.geometry("800x600")
        config_window.resizable(True, True)
        
        # Make window modal
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(config_window, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Kamera-Konfiguration (JSON)", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Instructions
        info_text = """
Bearbeiten Sie die JSON-Konfiguration direkt unten. 
Verfügbare Verbindungstypen:
- USB:0, USB:1, USB:2... für USB-Kameras
- RTSP:rtsp://ip:port/stream für Netzwerk-Kameras
- HTTP:http://ip:port/stream für HTTP-Streams
        """
        info_label = tk.Label(main_frame, text=info_text.strip(), 
                             justify="left", wraplength=760)
        info_label.pack(pady=(0, 10))
        
        # JSON Editor
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        editor_label = tk.Label(editor_frame, text="JSON-Konfiguration:", font=("Arial", 10, "bold"))
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
            text="JSON Validieren", 
            command=lambda: self.validate_json_config(self.json_editor),
            bg="lightblue"
        )
        validate_btn.pack(side="left", padx=(0, 5))
        
        # Add camera button
        add_camera_btn = tk.Button(
            button_frame, 
            text="+ Kamera hinzufügen", 
            command=lambda: self.add_camera_template(self.json_editor),
            bg="lightgreen"
        )
        add_camera_btn.pack(side="left", padx=(0, 5))
        
        # Reset button
        reset_btn = tk.Button(
            button_frame, 
            text="Zurücksetzen", 
            command=lambda: self.reset_json_editor(self.json_editor),
            bg="orange"
        )
        reset_btn.pack(side="left", padx=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Abbrechen", 
            command=config_window.destroy
        )
        cancel_btn.pack(side="right", padx=(5, 0))
          # Save button
        save_btn = tk.Button(
            button_frame, 
            text="Speichern", 
            command=lambda: self.save_json_config(self.json_editor, config_window),
            bg="lightgreen",
            font=("Arial", 10, "bold")
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Save and reload button
        save_reload_btn = tk.Button(
            button_frame, 
            text="Speichern & Live-Reload", 
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
                required_fields = ["index", "verbindung", "name", "enabled"]
                for field in required_fields:
                    if field not in camera:
                        raise ValueError(f"Kamera {i}: Pflichtfeld '{field}' fehlt")
                
                # Validate verbindung format
                verbindung = camera["verbindung"]
                if not any(verbindung.startswith(prefix) for prefix in ["USB:", "RTSP:", "HTTP:"]):
                    raise ValueError(f"Kamera {i}: Ungültiges Verbindungsformat '{verbindung}'. Verwenden Sie USB:, RTSP:, oder HTTP:")
            
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
            
            # Create new camera template with dynamic index
            new_camera = {
                "index": next_index,
                "verbindung": f"USB:{next_index}",
                "beschreibung": f"Neue Kamera Beschreibung {next_index}",
                "name": f"Kamera {next_index + 1}",
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
            
            messagebox.showinfo("Erfolg", f"✅ Neue Kamera mit Index {next_index} hinzugefügt!")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON-Fehler", f"Ungültiges JSON-Format:\n{e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Kamera:\n{e}")
    
    def reset_json_editor(self, editor):
        """Reset JSON editor to current saved configuration"""
        from tkinter import messagebox
        import json
        
        if messagebox.askyesno("Zurücksetzen", "Alle Änderungen verwerfen und zur gespeicherten Konfiguration zurückkehren?"):
            try:
                current_config = self.camera_config.config_data
                json_text = json.dumps(current_config, indent=2, ensure_ascii=False)
                editor.delete("1.0", "end")
                editor.insert("1.0", json_text)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Zurücksetzen: {e}")
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
                messagebox.showinfo("Erfolg", "✅ Konfiguration erfolgreich gespeichert!\n\nDie Änderungen werden beim nächsten Start angewendet.")
                
                # Close the window
                window.destroy()
                  # Just log the change, no immediate refresh to avoid GUI conflicts
                self.logger.log("📷 Kamera-Konfiguration gespeichert. Neustart für Änderungen erforderlich.")
            else:
                messagebox.showerror("Fehler", "❌ Fehler beim Speichern der Konfiguration!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")
    
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
                # Close the window first to avoid widget access issues
                window.destroy()
                
                # Show success message
                messagebox.showinfo("Erfolg", "✅ Konfiguration erfolgreich gespeichert!\n\nDie Änderungen werden sofort angewendet.")
                
                # Apply changes immediately with a small delay to ensure window is closed
                self.root.after(500, self.refresh_camera_configuration)
                
                self.logger.log("📷 Kamera-Konfiguration gespeichert und live angewendet.")
            else:
                messagebox.showerror("Fehler", "❌ Fehler beim Speichern der Konfiguration!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")
    
    def get_camera_info(self, cam_index):
        """Get camera information for display - JSON-based"""
        if hasattr(self, 'camera_config'):
            # Try to get info from JSON config
            camera = self.camera_config.get_camera_by_index(cam_index)
            if camera:
                hardware_info = self.camera_config.parse_verbindung(camera['verbindung'])
                device_index = hardware_info.get('device_index', cam_index) if hardware_info else cam_index
                
                return {
                    'name': camera.get('name', f"Camera {cam_index}"),
                    'bezeichnung': camera.get('name', f"Camera {cam_index}"),
                    'usb_label': f"USB-{device_index}",
                    'beschreibung': camera.get('beschreibung', f"USB Camera {cam_index}")
                }
        
        # Fallback to default values
        return {
            'name': f"Camera {cam_index}",
            'bezeichnung': f"Camera {cam_index}",
            'usb_label': f"USB-{cam_index}",
            'beschreibung': f"USB Camera {cam_index}"
        }
    
    def start_auto_streams(self):
        """Start all camera streams automatically if auto-stream is enabled"""
        print("DEBUG: start_auto_streams called")
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            self.logger.log("🎬 Starte automatische Kamera-Streams...")
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
                    self.logger.log(f"❌ Auto-Stream Fehler Kamera {cam_index}: {e}")
            
            self.logger.log(f"🎬 Auto-Streams: {success_count}/{total_cameras} Kameras gestartet")
        else:
            print("DEBUG: Auto-stream is disabled")

    def stop_auto_streams(self):
        """Stop all camera streams"""
        self.logger.log("⏹️ Stoppe alle Kamera-Streams...")
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
                    self.logger.log(f"❌ Fehler beim Stoppen von Kamera {cam_index}: {e}")
        
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


if __name__ == "__main__":
    app = ControlApp()
    app.run()
