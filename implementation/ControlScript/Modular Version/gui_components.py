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
        output_container.columnconfigure(1, weight=1, minsize=350)  # Scan configuration + image
        output_container.rowconfigure(0, weight=1)

        # Log console (left)
        log_frame = tk.Frame(output_container)
        log_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(log_frame, text="Log-Konsole", font=("Arial", 10, "bold")).pack(anchor='w')
        output = scrolledtext.ScrolledText(log_frame, width=45, height=16, state='disabled')
        output.pack(fill="both", expand=True)

        return output_container, output, log_frame
    
    @staticmethod
    def create_webcam_frame(parent):
        """Creates webcam display frame"""
        webcam_frame = tk.LabelFrame(parent, text="Camera")
        webcam_frame.pack(fill="both", expand=True, padx=10, pady=5, side=tk.LEFT)
        
        # Camera view frame
        camera_view_frame = tk.Frame(webcam_frame)
        camera_view_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Camera display label
        camera_label = tk.Label(camera_view_frame, text="Kamera nicht verfügbar", 
                               bg="gray", width=40, height=20)
        camera_label.pack(fill="both", expand=True)
        
        # Camera control buttons
        camera_control_frame = tk.Frame(webcam_frame)
        camera_control_frame.pack(fill="x", padx=5, pady=5)
        
        btn_start_camera = tk.Button(camera_control_frame, text="Kamera starten")
        btn_start_camera.pack(side=tk.LEFT, padx=2)
        
        btn_stop_camera = tk.Button(camera_control_frame, text="Kamera stoppen")
        btn_stop_camera.pack(side=tk.LEFT, padx=2)
        
        btn_take_photo = tk.Button(camera_control_frame, text="Foto aufnehmen")
        btn_take_photo.pack(side=tk.LEFT, padx=2)
        
        btn_add_photo_to_queue = tk.Button(camera_control_frame, text="+", 
                                          bg=BUTTON_ADD_COLOR, fg=BUTTON_ADD_FG,
                                          font=BUTTON_FONT, width=BUTTON_ADD_WIDTH)
        btn_add_photo_to_queue.pack(side=tk.LEFT, padx=2)
        
        return (webcam_frame, camera_label, btn_start_camera, btn_stop_camera, 
                btn_take_photo, btn_add_photo_to_queue)
    
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
    def create_queue_frame(parent, repeat_queue_var):
        """Creates operation queue frame"""
        queue_frame = tk.LabelFrame(parent, text="Operationswarteschlange")
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
            'tab2_frame': tab2_frame
        }
        
        return calc_panel, calc_vars, calc_widgets

    @staticmethod
    def create_calculator_commands_panel(parent, grid_mode=False):
        """
        Creates the comprehensive Calculator Commands Panel with visualization
        Shows parameters, buttons, and image tabs for servo geometry visualization
        """
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
            'tab2_frame': tab2_frame
        }
        
        return calc_panel, calc_vars, calc_widgets
