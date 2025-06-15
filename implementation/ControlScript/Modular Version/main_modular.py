"""
IScan-ControlScript - Main Program (Modular Structure)
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
from camera_config import CameraConfig, CameraConfigDialog

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
        self.setup_window_icon()        # Initialize variables
        self.init_variables()
        
        # Initialize camera configuration FIRST
        self.camera_config = CameraConfig()
        config_loaded = self.camera_config.load_from_csv()  # Lade bestehende Konfiguration
        
        # Setup available cameras based on CSV config
        self.setup_available_cameras(config_loaded)
        
        # Initialize webcams based on available cameras (before GUI creation)
        self.setup_webcams(config_loaded)
        
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
    
    def setup_available_cameras(self, config_loaded):
        """Setup available cameras based on CSV config or auto-detection"""
        # Zuerst physisch verfügbare Kameras erkennen
        from webcam_helper import WebcamHelper
        physically_available = WebcamHelper.detect_available_cameras()
        print(f"Physisch erkannte Kameras: {physically_available}")
        
        if config_loaded and self.camera_config.get_all_cameras():
            # Verwende CSV-Konfiguration, aber nur für physisch verfügbare Kameras
            configured_cameras = self.camera_config.get_all_cameras()
            configured_cameras.sort(key=lambda x: x['indexnummer'])
            
            # Filtere nur die Kameras, die sowohl konfiguriert als auch physisch verfügbar sind
            available_configured = []
            for cam in configured_cameras:
                if cam['indexnummer'] in physically_available:
                    available_configured.append(cam)
                    print(f"  Index {cam['indexnummer']}: {cam['bezeichnung']} ({cam['comport']}) - VERFÜGBAR")
                else:
                    print(f"  Index {cam['indexnummer']}: {cam['bezeichnung']} ({cam['comport']}) - NICHT VERFÜGBAR")
            
            self.available_cameras = [cam['indexnummer'] for cam in available_configured]
            print(f"CSV-Konfiguration: {len(available_configured)} von {len(configured_cameras)} Kameras verfügbar")
        else:
            # Fallback: Auto-Detection
            self.available_cameras = physically_available
            print(f"Auto-Detection: {len(self.available_cameras)} Kameras gefunden: {self.available_cameras}")
    
    def setup_webcams(self, config_loaded):
        """Setup webcam instances based on configuration"""
        self.webcams = {}
        self.current_camera_index = 0
        
        if config_loaded and self.camera_config.get_all_cameras():
            # Verwende CSV-Konfiguration für verfügbare Kameras
            configured_cameras = self.camera_config.get_all_cameras()
            configured_cameras.sort(key=lambda x: x['indexnummer'])  # Sortiere nach Index
            
            # Nur die verfügbaren Kameras initialisieren
            for cam_index in self.available_cameras:
                # Finde die Konfiguration für diese Kamera
                camera_info = None
                for cam_config in configured_cameras:
                    if cam_config['indexnummer'] == cam_index:
                        camera_info = cam_config
                        break
                
                if camera_info:
                    com_port = camera_info['comport']
                    bezeichnung = camera_info['bezeichnung']
                    print(f"Initialisiere Kamera Index {cam_index}: {bezeichnung} ({com_port})")
                    
                    self.webcams[cam_index] = WebcamHelper(
                        device_index=cam_index, 
                        frame_size=(150, 150),  # Compact size for grid display
                        com_port=com_port,
                        model=bezeichnung
                    )
        else:
            # Fallback: Automatisch erkannte Kameras
            for cam_index in self.available_cameras:
                com_port = f"COM{cam_index + 1}"  # Fallback
                bezeichnung = f"Camera {cam_index}"    # Fallback
                print(f"Initialisiere Fallback-Kamera Index {cam_index}: {bezeichnung} ({com_port})")
                
                self.webcams[cam_index] = WebcamHelper(
                    device_index=cam_index, 
                    frame_size=(150, 150),  # Compact size for grid display
                    com_port=com_port,
                    model=bezeichnung
                )
    
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
        self.diameter_frame, self.diameter_entry = GUIBuilder.create_diameter_frame(self.root)        # Position display
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
         self.queue_move_up_btn, self.queue_move_down_btn,         self.queue_export_btn, self.queue_import_btn, self.repeat_checkbox) = GUIBuilder.create_queue_frame(
            self.main_container, self.repeat_queue, grid_mode=True)        # Row 1, Column 0: Camera Grid Display (left bottom)
        (self.webcam_frame, self.camera_labels, self.camera_combo, self.camera_frames,
         self.btn_start_camera, self.btn_stop_camera, self.btn_take_photo, 
         self.btn_add_photo_to_queue, self.btn_camera_config, self.current_camera_label, 
         self.available_cameras_gui, self.auto_stream_var) = GUIBuilder.create_webcam_frame(
             self.main_container, 
             available_cameras=self.available_cameras,
             webcams_dict=self.webcams,
             grid_mode=True, 
             position="bottom_left"         )        # Row 1, Column 2: Settings Panel (under Queue)
        (self.settings_frame, self.home_exec_btn, self.home_add_btn,
         self.drive_up_distance, self.drive_up_speed, self.drive_up_exec_btn, self.drive_up_add_btn,
         self.drive_down_distance, self.drive_down_speed, self.drive_down_exec_btn, self.drive_down_add_btn) = GUIBuilder.create_settings_panel(
            self.main_container, grid_mode=True)
    
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
            'stepper_length_cm': self.stepper_length_cm,            'stepper_dir': self.stepper_dir,
            'stepper_speed': self.stepper_speed,
            'led_color': self.led_color,
            'led_bright': self.led_bright,
            'webcam': self.webcam,
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
            self.servo_angle_var        )
        # Angle calculator interface
        self.angle_calculator = AngleCalculatorInterface(self.logger)
    
    def initialize_calculator_display(self):
        """Initialize the calculator display with current values and load images"""
        if hasattr(self, 'event_handlers'):
            # Update command display with initial values            self.event_handlers.update_command_display()
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
                    # Prüfe ob es eine Konfiguration für diese Kamera gibt
                    camera_info = self.camera_config.get_camera_by_index(cam_index)
                    if camera_info:
                        # Verwende die Bezeichnung aus der Konfiguration
                        frame_title = f"{camera_info['bezeichnung']}"
                        info_text = f"{camera_info['comport']}"
                    else:
                        # Fallback: Standard-Format mit Hinweis auf nicht konfigurierte Kamera
                        frame_title = f"Camera {cam_index}"
                        if hasattr(self, 'webcams') and cam_index in self.webcams:
                            info_text = f"{self.webcams[cam_index].com_port}*"
                        else:
                            info_text = f"COM{cam_index + 1}*"
                      # Update frame title (info_label entfernt, da nur Index verwendet wird)
                    camera_frame_info['frame'].config(text=frame_title)
    
    def update_current_camera_info(self):
        """Update the current camera info label with detailed information"""
        if hasattr(self, 'current_camera_label') and hasattr(self, 'current_camera_index'):
            # Prüfe ob es eine Konfiguration für diese Kamera gibt
            camera_info = self.camera_config.get_camera_by_index(self.current_camera_index)
            if camera_info:
                # Verwende die Bezeichnung aus der Konfiguration
                info_text = f"{camera_info['bezeichnung']} ({camera_info['comport']})"
            else:
                # Fallback: Standard-Format mit Hinweis auf nicht konfigurierte Kamera
                if hasattr(self, 'webcam') and self.webcam:
                    info_text = f"Cam {self.current_camera_index} ({self.webcam.com_port}*)"
                else:
                    info_text = f"Cam {self.current_camera_index} (COM{self.current_camera_index + 1}*)"
            
            self.current_camera_label.config(text=info_text)

    def refresh_camera_configuration(self):
        """
        Refresh camera configuration after CSV changes
        This method is called as a callback when the CSV is saved
        """
        print("Refreshing camera configuration after CSV save...")
        
        # Reload camera configuration from CSV
        config_loaded = self.camera_config.load_from_csv()
        
        # Determine new available cameras based on CSV config and physical availability
        self.setup_available_cameras(config_loaded)
        
        # Stop all current camera streams
        self.stop_all_camera_streams()
        
        # Recreate webcam instances with new configuration
        self.setup_webcams(config_loaded)
        
        # Refresh the camera grid display
        self.refresh_camera_grid()
        
        # Update current camera selection if needed
        if self.available_cameras:
            # If current camera is still available, keep it
            if self.current_camera_index not in self.available_cameras:
                # Switch to first available camera
                self.current_camera_index = self.available_cameras[0]
                self.webcam = self.webcams[self.current_camera_index]
        
        # Update GUI elements
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
                # Find the grid container
                for child in self.webcam_frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        # This should be our grid_container
                        grid_container = child
                        break
                else:
                    # Create new grid container if not found
                    grid_container = tk.Frame(self.webcam_frame)
                    grid_container.pack(fill="both", expand=True)
                
                # Calculate grid dimensions
                num_cameras = len(self.available_cameras)
                cols = min(4, num_cameras)  # Max 4 columns
                rows = (num_cameras + cols - 1) // cols
                
                # Create new camera tiles
                for i, cam_index in enumerate(self.available_cameras):
                    row = i // cols
                    col = i % cols
                    
                    # Get camera info
                    com_port = f"COM{cam_index + 1}"  # Default
                    if cam_index in self.webcams:
                        webcam = self.webcams[cam_index]
                        if hasattr(webcam, 'com_port') and webcam.com_port:
                            com_port = webcam.com_port
                    
                    # Individual camera frame - compact size, Index als Titel
                    camera_frame = tk.LabelFrame(grid_container, text=f"Cam {cam_index}", 
                                                font=("Arial", 8, "bold"), relief="ridge", bd=1)
                    camera_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                    
                    # Camera view area - 150x150 max size
                    camera_view_frame = tk.Frame(camera_frame, bg="black", width=150, height=150)
                    camera_view_frame.pack_propagate(False)  # Keep fixed size
                    camera_view_frame.pack(padx=2, pady=2)
                    
                    # Camera display label - zeige COM-Port im Stream
                    camera_label = tk.Label(camera_view_frame, text=f"{com_port}\nOFFLINE", 
                                           bg="gray", fg="white", relief="sunken", bd=1,
                                           font=("Arial", 8))
                    camera_label.pack(fill="both", expand=True)
                    
                    # Store references
                    self.camera_labels[cam_index] = camera_label
                    self.camera_frames[cam_index] = {
                        'frame': camera_frame,
                        'view_frame': camera_view_frame
                    }
                
                # Configure grid weights for responsive layout
                for i in range(cols):
                    grid_container.grid_columnconfigure(i, weight=1)
                for i in range(rows):
                    grid_container.grid_rowconfigure(i, weight=1)
    
    # ...existing code...    
    def open_camera_config(self):
        """Open camera configuration dialog"""
        dialog = CameraConfigDialog(self.root, self.camera_config, self.logger, self.refresh_camera_configuration)
        dialog.open_dialog()
    
    def get_camera_info(self, cam_index):
        """Get camera information for display - uses only index as name"""
        if hasattr(self, 'camera_config') and self.camera_config.get_all_cameras():
            # Try to get COM port from CSV config
            cameras = self.camera_config.get_all_cameras()
            for cam in cameras:
                if cam['indexnummer'] == cam_index:
                    return {
                        'name': f"Cam {cam_index}",  # Nur Index als Name
                        'comport': cam['comport']
                    }
        
        # Fallback to default values
        return {
            'name': f"Cam {cam_index}",  # Nur Index als Name
            'comport': f"COM{cam_index + 1}"
        }
    
    def start_auto_streams(self):
        """Start all camera streams automatically if auto-stream is enabled"""
        print("DEBUG: start_auto_streams called")
        print(f"DEBUG: auto_stream_var exists: {hasattr(self, 'auto_stream_var')}")
        if hasattr(self, 'auto_stream_var'):
            print(f"DEBUG: auto_stream_var value: {self.auto_stream_var.get()}")
        
        if hasattr(self, 'auto_stream_var') and self.auto_stream_var.get():
            print(f"DEBUG: Available cameras: {self.available_cameras}")
            print(f"DEBUG: Webcams keys: {list(self.webcams.keys())}")
            print(f"DEBUG: Camera labels keys: {list(self.camera_labels.keys())}")
            
            for cam_index in self.available_cameras:
                if cam_index in self.webcams:
                    webcam = self.webcams[cam_index]
                    print(f"DEBUG: Camera {cam_index} - running: {webcam.running}")
                    if not webcam.running:
                        # Get the camera label for this camera
                        if cam_index in self.camera_labels:
                            camera_label = self.camera_labels[cam_index]
                            print(f"DEBUG: Starting stream for camera {cam_index}")                            # Start streaming to the label
                            if webcam.stream_starten(camera_label):
                                print(f"DEBUG: Successfully started camera {cam_index}")                                # Update label to show streaming status
                                cam_info = self.get_camera_info(cam_index)
                                camera_label.config(text=f"{cam_info['comport']}\nLIVE", 
                                                   bg="lightgreen")
                                self.logger.log(f"Auto-started stream for Camera {cam_index}")
                            else:
                                print(f"DEBUG: Failed to start camera {cam_index}")
                                # Update label to show error status
                                cam_info = self.get_camera_info(cam_index)
                                camera_label.config(text=f"{cam_info['comport']}\nERROR", 
                                                   bg="lightcoral")
                                self.logger.log(f"Failed to start Camera {cam_index}")
                        else:
                            print(f"DEBUG: No label found for camera {cam_index}")
                            self.logger.log(f"No label found for Camera {cam_index}")
                    else:
                        print(f"DEBUG: Camera {cam_index} already running")
                        self.logger.log(f"Camera {cam_index} already running")
                else:
                    print(f"DEBUG: Camera {cam_index} not in webcams dict")
    
    def stop_auto_streams(self):
        """Stop all camera streams"""
        for cam_index in self.available_cameras:
            if cam_index in self.webcams:
                webcam = self.webcams[cam_index]
                if webcam.running:
                    webcam.stoppen()                    # Update label to show offline status
                    if cam_index in self.camera_labels:
                        cam_info = self.get_camera_info(cam_index)
                        self.camera_labels[cam_index].config(text=f"{cam_info['comport']}\nOFFLINE", 
                                                           bg="gray", image="")
                    self.logger.log(f"Stopped stream for Camera {cam_index}")
    
    def toggle_auto_streams(self):
        """Toggle auto-stream mode on/off"""
        if hasattr(self, 'auto_stream_var'):
            if self.auto_stream_var.get():
                self.start_auto_streams()
            else:
                self.stop_auto_streams()
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop all camera streams
            if hasattr(self, 'webcams'):
                for cam_index, webcam in self.webcams.items():
                    try:
                        if hasattr(webcam, 'stop_stream'):
                            webcam.stop_stream()
                        if hasattr(webcam, 'release'):
                            webcam.release()
                    except Exception as e:
                        print(f"Error stopping camera {cam_index}: {e}")
            
            # Close the application
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during closing: {e}")
            self.root.destroy()

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
