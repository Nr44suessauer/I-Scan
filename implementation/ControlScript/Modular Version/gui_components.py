"""
GUI Components for I-Scan Application
All GUI creation methods in one place for easy extension and maintenance.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from config import *


class GUIBuilder:
    """Static methods for creating GUI components"""
    
    @staticmethod
    def create_url_frame(parent, base_url_var):
        """Creates the URL input frame"""
        url_frame = tk.Frame(parent)
        url_frame.pack(fill="x", padx=10, pady=(10,2))
        tk.Label(url_frame, text="API-Adresse:").pack(side=tk.LEFT)
        base_url_entry = tk.Entry(url_frame, textvariable=base_url_var, width=30)
        base_url_entry.pack(side=tk.LEFT, padx=5)
        return url_frame, base_url_entry
    
    @staticmethod
    def create_camera_settings_frame(parent):
        """Creates camera settings frame"""
        camera_settings_frame = tk.Frame(parent)
        camera_settings_frame.pack(fill="x", padx=10, pady=(2,2))
        tk.Label(camera_settings_frame, text="Kamera Device Index (z.B. 0, 1, 2):").pack(side=tk.LEFT)
        
        camera_device_index_var = tk.StringVar(value=str(DEFAULT_CAMERA_DEVICE))
        camera_device_entry = tk.Entry(camera_settings_frame, width=5, textvariable=camera_device_index_var)
        camera_device_entry.pack(side=tk.LEFT)
        
        set_camera_device_btn = tk.Button(camera_settings_frame, text="Setzen")
        set_camera_device_btn.pack(side=tk.LEFT, padx=5)
        
        # Autofocus delay
        tk.Label(camera_settings_frame, text="  Autofokus-Delay (s):").pack(side=tk.LEFT, padx=(20,0))
        camera_delay_var = tk.StringVar(value=str(DEFAULT_AUTOFOCUS_DELAY))
        camera_delay_entry = tk.Entry(camera_settings_frame, width=5, textvariable=camera_delay_var)
        camera_delay_entry.pack(side=tk.LEFT)
        
        set_delay_btn = tk.Button(camera_settings_frame, text="set")
        set_delay_btn.pack(side=tk.LEFT, padx=5)
        
        return (camera_settings_frame, camera_device_index_var, camera_device_entry, 
                set_camera_device_btn, camera_delay_var, camera_delay_entry, set_delay_btn)
    
    @staticmethod
    def create_diameter_frame(parent):
        """Creates diameter input frame"""
        diameter_frame = tk.Frame(parent)
        diameter_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(diameter_frame, text="Zahnraddurchmesser (mm):").pack(side=tk.LEFT)
        diameter_entry = tk.Entry(diameter_frame, width=10)
        diameter_entry.insert(0, DEFAULT_DIAMETER)
        diameter_entry.pack(side=tk.LEFT, padx=5)
        return diameter_frame, diameter_entry
    
    @staticmethod
    def create_position_display(parent, position_var, servo_angle_var):
        """Creates position and servo angle display"""
        position_frame = tk.Frame(parent)
        position_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(position_frame, text="Position (mm):").pack(side=tk.LEFT)
        position_label = tk.Label(position_frame, text="0.00", relief="sunken", width=10)
        position_label.pack(side=tk.LEFT, padx=5)        
        tk.Label(position_frame, text="Servo Winkel (°):").pack(side=tk.LEFT, padx=(20,0))
        servo_angle_label = tk.Label(position_frame, text="0", relief="sunken", width=10)
        servo_angle_label.pack(side=tk.LEFT, padx=5)
        
        return position_frame, position_label, servo_angle_label
    
    @staticmethod
    def create_output_display(parent):
        """
        Creates the output text display with calculator commands panel
        Shows log console and calculator commands side by side in grid layout
        """
        # Main container for Output and Calculator Commands
        output_container = tk.Frame(parent)
        output_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Grid layout for equal distribution
        output_container.columnconfigure(0, weight=1, minsize=350)  # Log console narrower
        output_container.columnconfigure(1, weight=1, minsize=350)  # Scan configuration + image        output_container.rowconfigure(0, weight=1)
        
        # Log console (left)
        log_frame = tk.Frame(output_container)
        log_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(log_frame, text="Log-Konsole", font=("Arial", 10, "bold")).pack(anchor='w')
        output = scrolledtext.ScrolledText(log_frame, width=45, height=16, state='disabled')
        output.pack(fill="both", expand=True)

        return output_container, output, log_frame    @staticmethod
    def create_webcam_frame(parent, available_cameras=None, webcams_dict=None, grid_mode=False, position="full"):
        """Creates webcam display frame with compact grid layout for multiple cameras"""
        from webcam_helper import WebcamHelper
        from tkinter import ttk
        
        webcam_frame = tk.LabelFrame(parent, text="Camera Streams", font=("Arial", 9, "bold"))
        if grid_mode:
            if position == "bottom_left":
                # Position in row 1, column 0 (bottom left)
                webcam_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            else:
                # Position in row 1, span all columns for grid layout
                webcam_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        else:
            webcam_frame.pack(fill="both", expand=True, padx=10, pady=5)
          # Main container for layout - compact design
        main_container = tk.Frame(webcam_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Auto-stream control variable (nur für interne Verwendung)
        auto_stream_var = tk.BooleanVar(value=True)
        
        # Detect available cameras - use provided list or auto-detect
        if available_cameras is None:
            available_cameras = WebcamHelper.detect_available_cameras()
        
        if not available_cameras:
            # If no cameras detected, try to detect at least one
            available_cameras = WebcamHelper.detect_available_cameras()
            if not available_cameras:
                available_cameras = [0]  # Fallback to index 0
        
        # Calculate compact grid dimensions
        num_cameras = len(available_cameras)
        
        # Prefer horizontal layout for compact display
        import math
        cols = min(4, num_cameras)  # Max 4 columns for compact layout
        rows = math.ceil(num_cameras / cols)
        
        # Camera grid container
        grid_container = tk.Frame(main_container)
        grid_container.pack(fill="both", expand=True)
        
        # Store camera components
        camera_labels = {}
        camera_frames = {}
        
        # Create compact grid of camera displays
        for i, cam_index in enumerate(available_cameras):
            row = i // cols
            col = i % cols
              # Get camera info from webcams_dict if available
            cam_name = f"Cam {cam_index}"
            com_port = f"COM{cam_index + 1}"
            
            if webcams_dict and cam_index in webcams_dict:
                webcam = webcams_dict[cam_index]
                if hasattr(webcam, 'model') and webcam.model:
                    cam_name = webcam.model
                if hasattr(webcam, 'com_port') and webcam.com_port:
                    com_port = webcam.com_port

            # Individual camera frame - use model name from webcam if available
            camera_frame = tk.LabelFrame(grid_container, text=cam_name, 
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
            camera_labels[cam_index] = camera_label
            camera_frames[cam_index] = {
                'frame': camera_frame,
                'view_frame': camera_view_frame
            }        # Configure grid weights for responsive layout
        for i in range(cols):
            grid_container.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            grid_container.grid_rowconfigure(i, weight=1)
        
        # Control buttons frame
        control_frame = tk.Frame(main_container)
        control_frame.pack(fill="x", pady=(5, 0))
        
        # Refresh cameras button
        btn_refresh_cameras = tk.Button(control_frame, text="🔄 Kameras Neu Laden", 
                                       font=("Arial", 9), bg="#4CAF50", fg="white")
        btn_refresh_cameras.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto-stream toggle (moved here for better layout)
        auto_stream_check = tk.Checkbutton(control_frame, text="Auto-Stream", 
                                         variable=auto_stream_var, font=("Arial", 9))
        auto_stream_check.pack(side=tk.LEFT)
        
        # Hidden elements for compatibility (not displayed - settings are in settings panel)
        btn_start_camera = tk.Button(webcam_frame)  # Hidden
        btn_stop_camera = tk.Button(webcam_frame)   # Hidden  
        btn_add_photo_to_queue = tk.Button(webcam_frame)  # Hidden
        
        # Dummy variables for compatibility
        current_camera_combo = None
        current_camera_label = tk.Label(webcam_frame, text="")  # Hidden        
        return (webcam_frame, camera_labels, current_camera_combo, camera_frames,
                btn_start_camera, btn_stop_camera, btn_add_photo_to_queue,
                current_camera_label, available_cameras, auto_stream_var, btn_refresh_cameras)
    
    @staticmethod
    def create_servo_frame(parent):
        """Creates servo control frame"""
        servo_frame = tk.LabelFrame(parent, text="Servo-Steuerung")
        servo_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(servo_frame, text="Winkel (0-180°):").pack(side=tk.LEFT)
        servo_angle = tk.Entry(servo_frame, width=5)
        servo_angle.insert(0, "0")
        servo_angle.pack(side=tk.LEFT)
        
        servo_exec_btn = tk.Button(servo_frame, text="Servo ausführen")
        servo_exec_btn.pack(side=tk.LEFT, padx=5)
        
        servo_add_btn = tk.Button(servo_frame, text="+", 
                                 bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                 font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        servo_add_btn.pack(side=tk.LEFT)
        
        return servo_frame, servo_angle, servo_exec_btn, servo_add_btn
    
    @staticmethod
    def create_stepper_frame(parent, last_distance_value):
        """Creates stepper motor control frame"""
        stepper_frame = tk.LabelFrame(parent, text="Schrittmotor-Steuerung")
        stepper_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(stepper_frame, text="Distanz (cm):").pack(side=tk.LEFT)
        stepper_length_cm = tk.Entry(stepper_frame, width=8, textvariable=last_distance_value)
        stepper_length_cm.pack(side=tk.LEFT)
        
        tk.Label(stepper_frame, text="Richtung:").pack(side=tk.LEFT, padx=(10,0))
        stepper_dir = tk.Entry(stepper_frame, width=5)
        stepper_dir.insert(0, DEFAULT_DIRECTION)
        stepper_dir.pack(side=tk.LEFT)
        
        tk.Label(stepper_frame, text="Geschwindigkeit:").pack(side=tk.LEFT, padx=(10,0))
        stepper_speed = tk.Entry(stepper_frame, width=5)
        stepper_speed.insert(0, DEFAULT_SPEED)
        stepper_speed.pack(side=tk.LEFT)
        
        stepper_exec_btn = tk.Button(stepper_frame, text="Stepper ausführen")
        stepper_exec_btn.pack(side=tk.LEFT, padx=5)
        
        stepper_add_btn = tk.Button(stepper_frame, text="+", 
                                   bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                   font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        stepper_add_btn.pack(side=tk.LEFT)
        
        return (stepper_frame, stepper_length_cm, stepper_dir, stepper_speed, 
                stepper_exec_btn, stepper_add_btn)
    
    @staticmethod
    def create_led_color_frame(parent):
        """Creates LED color control frame"""
        led_color_frame = tk.LabelFrame(parent, text="LED-Farbe setzen")
        led_color_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(led_color_frame, text="Farbe (z.B. #FF0000):").pack(side=tk.LEFT)
        led_color = tk.Entry(led_color_frame, width=10)
        led_color.insert(0, DEFAULT_LED_COLOR)
        led_color.pack(side=tk.LEFT)
        
        led_exec_btn = tk.Button(led_color_frame, text="LED ausführen")
        led_exec_btn.pack(side=tk.LEFT, padx=5)
        
        led_add_btn = tk.Button(led_color_frame, text="+", 
                               bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                               font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        led_add_btn.pack(side=tk.LEFT)
        
        return led_color_frame, led_color, led_exec_btn, led_add_btn
    
    @staticmethod
    def create_led_brightness_frame(parent):
        """Creates LED brightness control frame"""
        led_brightness_frame = tk.LabelFrame(parent, text="LED-Helligkeit setzen")
        led_brightness_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(led_brightness_frame, text="Helligkeit (0-100):").pack(side=tk.LEFT)
        led_bright = tk.Entry(led_brightness_frame, width=5)
        led_bright.insert(0, DEFAULT_LED_BRIGHTNESS)
        led_bright.pack(side=tk.LEFT)
        
        bright_exec_btn = tk.Button(led_brightness_frame, text="Helligkeit ausführen")
        bright_exec_btn.pack(side=tk.LEFT, padx=5)
        
        bright_add_btn = tk.Button(led_brightness_frame, text="+", 
                                  bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                  font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        bright_add_btn.pack(side=tk.LEFT)
        
        return led_brightness_frame, led_bright, bright_exec_btn, bright_add_btn
    
    @staticmethod
    def create_button_frame(parent):
        """Creates button status frame"""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(button_frame, text="Button Status:").pack(side=tk.LEFT)
        
        button_exec_btn = tk.Button(button_frame, text="Ausführen")
        button_exec_btn.pack(side=tk.LEFT, padx=5)
        
        button_add_btn = tk.Button(button_frame, text="Zur Queue")
        button_add_btn.pack(side=tk.LEFT)
        
        return button_frame, button_exec_btn, button_add_btn
    
    @staticmethod
    def create_home_frame(parent):
        """Creates home function frame"""
        home_frame = tk.Frame(parent)
        home_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(home_frame, text="Home:").pack(side=tk.LEFT)
        
        home_exec_btn = tk.Button(home_frame, text="Ausführen")
        home_exec_btn.pack(side=tk.LEFT, padx=5)
        
        home_add_btn = tk.Button(home_frame, text="Zur Queue")
        home_add_btn.pack(side=tk.LEFT)
        
        return home_frame, home_exec_btn, home_add_btn
    
    @staticmethod
    def create_angle_calculator_frame(parent):
        """Creates angle calculator frame"""
        angle_calc_frame = tk.LabelFrame(parent, text="Angle Calculator Commands")
        angle_calc_frame.pack(fill="x", padx=10, pady=2)
        
        show_calc_btn = tk.Button(angle_calc_frame, text="Angle Calculator anzeigen")
        show_calc_btn.pack(side=tk.LEFT, padx=5)
        
        load_csv_btn = tk.Button(angle_calc_frame, text="CSV laden")
        load_csv_btn.pack(side=tk.LEFT, padx=5)
        
        save_csv_btn = tk.Button(angle_calc_frame, text="CSV speichern")
        save_csv_btn.pack(side=tk.LEFT, padx=5)        
        return angle_calc_frame, show_calc_btn, load_csv_btn, save_csv_btn    
    @staticmethod
    def create_queue_frame(parent, repeat_queue_var, grid_mode=False):
        """Creates operation queue frame"""
        queue_frame = tk.LabelFrame(parent, text="Queue", font=("Arial", 10, "bold"))
        if grid_mode:
            queue_frame.grid(row=0, column=2, sticky="nsew", padx=5)  # Changed from column=3 to column=2
        else:
            queue_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Queue list
        queue_list_frame = tk.Frame(queue_frame)
        queue_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        queue_scrollbar = tk.Scrollbar(queue_list_frame)
        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        queue_list = tk.Listbox(queue_list_frame, yscrollcommand=queue_scrollbar.set, height=8)
        queue_list.pack(fill="both", expand=True)
        queue_scrollbar.config(command=queue_list.yview)
        
        # Queue control buttons - Row 1
        queue_control_frame1 = tk.Frame(queue_frame)
        queue_control_frame1.pack(fill="x", padx=5, pady=2)
        
        queue_exec_btn = tk.Button(queue_control_frame1, text="Queue ausführen", bg="lightgreen", font=("Arial", 9, "bold"))
        queue_exec_btn.pack(side=tk.LEFT, padx=2)
        
        queue_pause_btn = tk.Button(queue_control_frame1, text="Pausieren", bg="orange")
        queue_pause_btn.pack(side=tk.LEFT, padx=2)
        
        queue_exec_selected_btn = tk.Button(queue_control_frame1, text="Auswahl ausführen", bg="lightblue")
        queue_exec_selected_btn.pack(side=tk.LEFT, padx=2)
        
        queue_clear_btn = tk.Button(queue_control_frame1, text="Queue leeren", bg="lightcoral")
        queue_clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Queue control buttons - Row 2
        queue_control_frame2 = tk.Frame(queue_frame)
        queue_control_frame2.pack(fill="x", padx=5, pady=2)
        
        queue_remove_btn = tk.Button(queue_control_frame2, text="Auswahl löschen", bg="salmon")
        queue_remove_btn.pack(side=tk.LEFT, padx=2)        
        queue_duplicate_btn = tk.Button(queue_control_frame2, text="Auswahl kopieren", bg="lightyellow")
        queue_duplicate_btn.pack(side=tk.LEFT, padx=2)
        
        queue_edit_btn = tk.Button(queue_control_frame2, text="✎ Edit", width=8, bg="lightsteelblue", font=("Arial", 9, "bold"))
        queue_edit_btn.pack(side=tk.LEFT, padx=2)
        
        queue_settings_btn = tk.Button(queue_control_frame2, text="⚙ Opt", width=8, bg="lightgray", font=("Arial", 9, "bold"))
        queue_settings_btn.pack(side=tk.LEFT, padx=2)
        
        queue_move_up_btn = tk.Button(queue_control_frame2, text="▲ Nach oben")
        queue_move_up_btn.pack(side=tk.LEFT, padx=2)
        
        queue_move_down_btn = tk.Button(queue_control_frame2, text="▼ Nach unten")
        queue_move_down_btn.pack(side=tk.LEFT, padx=2)
          # Queue control buttons - Row 3
        queue_control_frame3 = tk.Frame(queue_frame)
        queue_control_frame3.pack(fill="x", padx=5, pady=2)
        
        queue_export_btn = tk.Button(queue_control_frame3, text="Warteschlange exportieren (CSV)", bg="#b0c4de", fg="black")
        queue_export_btn.pack(side=tk.LEFT, padx=2)
        
        queue_import_btn = tk.Button(queue_control_frame3, text="Warteschlange importieren (CSV)", bg="#b0c4de", fg="black")
        queue_import_btn.pack(side=tk.LEFT, padx=2)
        
        # Repeat checkbox
        repeat_checkbox = tk.Checkbutton(queue_control_frame3, text="Wiederholen", 
                                        variable=repeat_queue_var)
        repeat_checkbox.pack(side=tk.RIGHT, padx=5)
        
        return (queue_frame, queue_list, queue_exec_btn, queue_pause_btn, queue_exec_selected_btn,
                queue_clear_btn, queue_remove_btn, queue_duplicate_btn, queue_edit_btn, queue_settings_btn, 
                queue_move_up_btn, queue_move_down_btn, queue_export_btn, queue_import_btn, repeat_checkbox)

    @staticmethod
    def create_calculator_commands_panel(parent, grid_mode=False):
        """
        Creates the comprehensive Calculator Commands Panel with visualization
        Shows parameters, buttons, and image tabs for servo geometry visualization
        """
        from tkinter import ttk
        
        calc_panel = tk.LabelFrame(parent, text="Calculator Commands", font=("Arial", 10, "bold"))
        if grid_mode:
            calc_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        else:
            calc_panel.pack(side=tk.RIGHT, fill="y", padx=(10, 0))

        # Frame for parameters and image side by side
        content_frame = tk.Frame(calc_panel)
        content_frame.pack(fill="both", expand=True)

        # Parameters for both modes (left side)
        params_frame = tk.Frame(content_frame)
        params_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # CSV Name
        tk.Label(params_frame, text="CSV Name:", font=("Arial", 8)).grid(row=0, column=0, sticky="w", padx=2, pady=1)
        calc_csv_name = tk.Entry(params_frame, width=18, font=("Arial", 8))
        calc_csv_name.insert(0, "original_iscan")
        calc_csv_name.grid(row=0, column=1, padx=2, pady=1)
        
        # Target X
        tk.Label(params_frame, text="Target X (cm):", font=("Arial", 8)).grid(row=1, column=0, sticky="w", padx=2, pady=1)
        calc_target_x = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_target_x.insert(0, "33")
        calc_target_x.grid(row=1, column=1, sticky="w", padx=2, pady=1)
        
        # Target Y
        tk.Label(params_frame, text="Target Y (cm):", font=("Arial", 8)).grid(row=2, column=0, sticky="w", padx=2, pady=1)
        calc_target_y = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_target_y.insert(0, "50")
        calc_target_y.grid(row=2, column=1, sticky="w", padx=2, pady=1)
        
        # Scan Distance
        tk.Label(params_frame, text="Scan Distance (cm):", font=("Arial", 8)).grid(row=3, column=0, sticky="w", padx=2, pady=1)
        calc_scan_distance = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_scan_distance.insert(0, "80")
        calc_scan_distance.grid(row=3, column=1, sticky="w", padx=2, pady=1)
        
        # Measurements
        tk.Label(params_frame, text="Measurements:", font=("Arial", 8)).grid(row=4, column=0, sticky="w", padx=2, pady=1)
        calc_measurements = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_measurements.insert(0, "7")
        calc_measurements.grid(row=4, column=1, sticky="w", padx=2, pady=1)
        
        # Servo Configuration Section Header
        servo_header = tk.Label(params_frame, text="Servo Configuration:", font=("Arial", 8, "bold"), fg="darkblue")
        servo_header.grid(row=5, column=0, columnspan=2, sticky="w", padx=2, pady=(8, 2))
        
        # Servo Min Angle
        tk.Label(params_frame, text="Servo Min Angle:", font=("Arial", 8)).grid(row=6, column=0, sticky="w", padx=2, pady=1)
        calc_servo_min = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_servo_min.insert(0, "0.0")
        calc_servo_min.grid(row=6, column=1, sticky="w", padx=2, pady=1)
        
        # Servo Max Angle
        tk.Label(params_frame, text="Servo Max Angle:", font=("Arial", 8)).grid(row=7, column=0, sticky="w", padx=2, pady=1)
        calc_servo_max = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_servo_max.insert(0, "90.0")
        calc_servo_max.grid(row=7, column=1, sticky="w", padx=2, pady=1)
        
        # Servo Neutral Angle
        tk.Label(params_frame, text="Servo Neutral Angle:", font=("Arial", 8)).grid(row=8, column=0, sticky="w", padx=2, pady=1)
        calc_servo_neutral = tk.Entry(params_frame, width=8, font=("Arial", 8))
        calc_servo_neutral.insert(0, "45.0")
        calc_servo_neutral.grid(row=8, column=1, sticky="w", padx=2, pady=1)
        
        # Separator
        separator = tk.Frame(params_frame, height=2, bg="gray")
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", pady=8)

        # Command Buttons
        commands_frame = tk.LabelFrame(params_frame, text="Execute Commands", font=("Arial", 8, "bold"))
        commands_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=2)
        
        visual_btn = tk.Button(commands_frame, text="Visualisation Mode\n(--visualize)", 
                              bg="#FFD700", fg="black", font=("Arial", 8, "bold"), width=15, height=2)
        visual_btn.pack(fill="x", padx=2, pady=2)
        
        silent_btn = tk.Button(commands_frame, text="Silent Mode\n(--silent)", 
                              bg="#98FB98", fg="black", font=("Arial", 8, "bold"), width=15, height=2)
        silent_btn.pack(fill="x", padx=2, pady=2)

        # Current Command Display
        current_cmd_frame = tk.LabelFrame(params_frame, text="Current Command", font=("Arial", 8, "bold"))
        current_cmd_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=5)
        current_command_label = tk.Label(current_cmd_frame, 
                                        text="python main.py --visualize --csv-name original_iscan --target-x 33 --target-y 50 --scan-distance 80 --measurements 7",
                                        wraplength=200, justify="left", font=("Arial", 7), fg="blue")
        current_command_label.pack(padx=2, pady=2)
        
        # Image display with tabs (right side)
        image_frame = tk.Frame(content_frame)
        image_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Tab-Notebook for image switching
        image_notebook = ttk.Notebook(image_frame)
        image_notebook.pack(fill="both", expand=True)
        
        # Tab 1: Servo Geometry Graph
        tab1_frame = tk.Frame(image_notebook)
        image_notebook.add(tab1_frame, text="Servo Graph")
        
        # Tab 2: Servo Cone Detail
        tab2_frame = tk.Frame(image_notebook)
        image_notebook.add(tab2_frame, text="Cone Detail")
        
        # Image Labels for both tabs
        servo_graph_img_label = tk.Label(tab1_frame)
        servo_graph_img_label.pack(fill="both", expand=True)
        
        servo_cone_img_label = tk.Label(tab2_frame)
        servo_cone_img_label.pack(fill="both", expand=True)
        
        # Return all components and variables
        calc_vars = {
            'csv_name': calc_csv_name,
            'target_x': calc_target_x,
            'target_y': calc_target_y,
            'scan_distance': calc_scan_distance,
            'measurements': calc_measurements,
            'servo_min': calc_servo_min,
            'servo_max': calc_servo_max,
            'servo_neutral': calc_servo_neutral
        }
        
        calc_widgets = {
            'visual_btn': visual_btn,
            'silent_btn': silent_btn,
            'current_command_label': current_command_label,
            'image_notebook': image_notebook,
            'servo_graph_img_label': servo_graph_img_label,
            'servo_cone_img_label': servo_cone_img_label,
            'tab1_frame': tab1_frame,
            'tab2_frame': tab2_frame        }
        
        return calc_panel, calc_vars, calc_widgets

    @staticmethod
    def create_image_display_frame(parent_container):
        """
        Creates separate image display frame for grid layout (column 2)
        Shows servo visualization images permanently visible with tabs
        """
        from tkinter import ttk
        
        # Image display frame positioned in grid (column 2)
        image_frame = tk.LabelFrame(parent_container, text="Pictures", font=("Arial", 10, "bold"))
        image_frame.grid(row=0, column=2, sticky="nsew", padx=5)
        
        # Tab-Notebook für Bildwechsel
        image_notebook = ttk.Notebook(image_frame)
        image_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tab 1: Servo Geometry Graph
        tab1_frame = tk.Frame(image_notebook)
        image_notebook.add(tab1_frame, text="Servo Graph")
        
        # Tab 2: Servo Cone Detail
        tab2_frame = tk.Frame(image_notebook)
        image_notebook.add(tab2_frame, text="Cone Detail")
        
        # Image Labels für beide Tabs
        servo_graph_img_label = tk.Label(tab1_frame, text="Servo Graph wird geladen...", 
                                        bg="lightgray", width=25, height=12)
        servo_graph_img_label.pack(fill="both", expand=True)
        
        servo_cone_img_label = tk.Label(tab2_frame, text="Servo Cone wird geladen...", 
                                       bg="lightgray", width=25, height=12)
        servo_cone_img_label.pack(fill="both", expand=True)
        
        # Image control buttons
        image_controls = tk.Frame(image_frame)
        image_controls.pack(fill="x", padx=5, pady=5)
        
        load_csv_btn = tk.Button(image_controls, text="CSV Load", font=("Arial", 8))
        load_csv_btn.pack(side=tk.LEFT, padx=2)
        
        save_csv_btn = tk.Button(image_controls, text="CSV Save", font=("Arial", 8))
        save_csv_btn.pack(side=tk.LEFT, padx=2)
        
        return (image_frame, image_notebook, servo_graph_img_label, 
                servo_cone_img_label, tab1_frame, tab2_frame, 
                load_csv_btn, save_csv_btn)
    
    @staticmethod
    def create_settings_panel(parent, grid_mode=False):
        """Creates a settings panel with Home, Drive Up/Down controls"""
        settings_frame = tk.LabelFrame(parent, text="Einstellungen", font=("Arial", 10, "bold"))
        if grid_mode:
            settings_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=(5,0))
        else:
            settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Home Control Section
        home_section = tk.LabelFrame(settings_frame, text="Home Control", font=("Arial", 9, "bold"))
        home_section.pack(fill="x", padx=5, pady=3)
        
        home_control_frame = tk.Frame(home_section)
        home_control_frame.pack(fill="x", padx=5, pady=3)
        
        home_exec_btn = tk.Button(home_control_frame, text="🏠 Home", 
                                 bg="lightblue", fg="black", font=("Arial", 9, "bold"), width=10)
        home_exec_btn.pack(side=tk.LEFT, padx=2)
        
        home_add_btn = tk.Button(home_control_frame, text="+", 
                                bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        home_add_btn.pack(side=tk.LEFT, padx=2)
        
        # Drive Control Section
        drive_section = tk.LabelFrame(settings_frame, text="Drive Control", font=("Arial", 9, "bold"))
        drive_section.pack(fill="x", padx=5, pady=3)
          # Drive Up Controls
        drive_up_frame = tk.Frame(drive_section)
        drive_up_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Label(drive_up_frame, text="Up Distance (cm):", font=("Arial", 8)).pack(side=tk.LEFT)
        drive_up_distance = tk.Entry(drive_up_frame, width=6, font=("Arial", 8))
        drive_up_distance.insert(0, "1.0")
        drive_up_distance.pack(side=tk.LEFT, padx=(5,5))
        
        tk.Label(drive_up_frame, text="Speed:", font=("Arial", 8)).pack(side=tk.LEFT, padx=(5,0))
        drive_up_speed = tk.Entry(drive_up_frame, width=4, font=("Arial", 8))
        drive_up_speed.insert(0, "80")
        drive_up_speed.pack(side=tk.LEFT, padx=(5,5))
        
        drive_up_exec_btn = tk.Button(drive_up_frame, text="⬆ Up (1)", 
                                     bg="lightgreen", fg="black", font=("Arial", 8, "bold"), width=8)
        drive_up_exec_btn.pack(side=tk.LEFT, padx=2)
        
        drive_up_add_btn = tk.Button(drive_up_frame, text="+", 
                                    bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                    font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        drive_up_add_btn.pack(side=tk.LEFT, padx=2)        # Drive Down Controls
        drive_down_frame = tk.Frame(drive_section)
        drive_down_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Label(drive_down_frame, text="Down Distance (cm):", font=("Arial", 8)).pack(side=tk.LEFT)
        drive_down_distance = tk.Entry(drive_down_frame, width=6, font=("Arial", 8))
        drive_down_distance.insert(0, "1.0")
        drive_down_distance.pack(side=tk.LEFT, padx=(5,5))
        
        tk.Label(drive_down_frame, text="Speed:", font=("Arial", 8)).pack(side=tk.LEFT, padx=(5,0))
        drive_down_speed = tk.Entry(drive_down_frame, width=4, font=("Arial", 8))
        drive_down_speed.insert(0, "80")
        drive_down_speed.pack(side=tk.LEFT, padx=(5,5))
        
        drive_down_exec_btn = tk.Button(drive_down_frame, text="⬇ Down (-1)", 
                                       bg="orange", fg="black", font=("Arial", 8, "bold"), width=8)
        drive_down_exec_btn.pack(side=tk.LEFT, padx=2)
        
        drive_down_add_btn = tk.Button(drive_down_frame, text="+", 
                                      bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                      font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        drive_down_add_btn.pack(side=tk.LEFT, padx=2)
          # Photo Control Section
        photo_section = tk.LabelFrame(settings_frame, text="Photo Control", font=("Arial", 9, "bold"))
        photo_section.pack(fill="x", padx=5, pady=3)
        
        photo_frame = tk.Frame(photo_section)
        photo_frame.pack(fill="x", padx=5, pady=2)
        
        # Camera selection for photo
        tk.Label(photo_frame, text="Aktiv:", font=("Arial", 8)).pack(side=tk.LEFT)
        photo_camera_var = tk.StringVar(value="0")
        photo_camera_combo = ttk.Combobox(photo_frame, textvariable=photo_camera_var,
                                         width=5, font=("Arial", 8), state="readonly")
        photo_camera_combo.pack(side=tk.LEFT, padx=(2, 10))
        
        # Photo action buttons
        photo_exec_btn = tk.Button(photo_frame, text="📷 Foto", 
                                  bg="lightcyan", fg="black", font=("Arial", 8, "bold"), width=8)
        photo_exec_btn.pack(side=tk.LEFT, padx=2)
        
        photo_add_btn = tk.Button(photo_frame, text="+", 
                                 bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                 font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        photo_add_btn.pack(side=tk.LEFT, padx=2)
        
        # Camera config button
        photo_config_btn = tk.Button(photo_frame, text="⚙ Config", font=("Arial", 8), width=8)
        photo_config_btn.pack(side=tk.LEFT, padx=2)        
        return (settings_frame, home_exec_btn, home_add_btn,
                drive_up_distance, drive_up_speed, drive_up_exec_btn, drive_up_add_btn,
                drive_down_distance, drive_down_speed, drive_down_exec_btn, drive_down_add_btn,
                photo_camera_combo, photo_exec_btn, photo_add_btn, photo_config_btn)
