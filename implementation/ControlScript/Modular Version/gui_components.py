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
        """Creates the output text display"""
        output_frame = tk.Frame(parent)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(5,2))
        tk.Label(output_frame, text="Ausgabe:").pack(anchor="w")
        output = scrolledtext.ScrolledText(output_frame, height=10, width=60)
        output.pack(fill="both", expand=True)
        return output_frame, output
    
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
        
        # Queue control buttons
        queue_control_frame = tk.Frame(queue_frame)
        queue_control_frame.pack(fill="x", padx=5, pady=5)
        
        queue_exec_btn = tk.Button(queue_control_frame, text="Queue ausführen", bg="lightgreen")
        queue_exec_btn.pack(side=tk.LEFT, padx=2)
        
        queue_clear_btn = tk.Button(queue_control_frame, text="Queue leeren", bg="lightcoral")
        queue_clear_btn.pack(side=tk.LEFT, padx=2)
        
        queue_remove_btn = tk.Button(queue_control_frame, text="Auswahl löschen")
        queue_remove_btn.pack(side=tk.LEFT, padx=2)
        
        queue_export_btn = tk.Button(queue_control_frame, text="Exportieren")
        queue_export_btn.pack(side=tk.LEFT, padx=2)
        
        queue_import_btn = tk.Button(queue_control_frame, text="Importieren")
        queue_import_btn.pack(side=tk.LEFT, padx=2)
        
        # Repeat checkbox
        repeat_checkbox = tk.Checkbutton(queue_control_frame, text="Wiederholen", 
                                        variable=repeat_queue_var)
        repeat_checkbox.pack(side=tk.RIGHT, padx=5)
        
        return (queue_frame, queue_list, queue_exec_btn, queue_clear_btn, 
                queue_remove_btn, queue_export_btn, queue_import_btn, repeat_checkbox)
