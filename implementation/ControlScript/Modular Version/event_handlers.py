"""
Event Handlers for I-Scan Application
All callback functions and event handlers in one place.
"""

import threading
from config import *


class EventHandlers:
    """All event handlers and callback functions"""
    
    def __init__(self, app_instance):
        """Initialize with reference to main app instance"""
        self.app = app_instance
    
    def assign_all_callbacks(self):
        """Assign all callback functions to their respective buttons"""
        # Camera callbacks
        self.app.btn_start_camera.config(command=self.on_start_camera)
        self.app.btn_stop_camera.config(command=self.on_stop_camera)
        self.app.btn_take_photo.config(command=self.on_take_photo)
        self.app.btn_add_photo_to_queue.config(command=self.on_add_photo_to_queue)
        self.app.set_camera_device_btn.config(command=self.on_set_camera_device)
        self.app.set_delay_btn.config(command=self.on_set_delay)
        
        # Servo callbacks
        self.app.servo_exec_btn.config(command=self.on_servo_execute)
        self.app.servo_add_btn.config(command=self.on_servo_add_to_queue)
        
        # Stepper callbacks
        self.app.stepper_exec_btn.config(command=self.on_stepper_execute)
        self.app.stepper_add_btn.config(command=self.on_stepper_add_to_queue)
        
        # LED callbacks
        self.app.led_exec_btn.config(command=self.on_led_execute)
        self.app.led_add_btn.config(command=self.on_led_add_to_queue)
        self.app.bright_exec_btn.config(command=self.on_brightness_execute)
        self.app.bright_add_btn.config(command=self.on_brightness_add_to_queue)
        
        # Button callbacks
        self.app.button_exec_btn.config(command=self.on_button_execute)
        self.app.button_add_btn.config(command=self.on_button_add_to_queue)
        
        # Home callbacks
        self.app.home_exec_btn.config(command=self.on_home_execute)
        self.app.home_add_btn.config(command=self.on_home_add_to_queue)
        
        # Angle calculator callbacks
        self.app.show_calc_btn.config(command=self.on_show_angle_calculator)
        self.app.load_csv_btn.config(command=self.on_load_csv)
        self.app.save_csv_btn.config(command=self.on_save_csv)
        
        # Queue callbacks
        self.app.queue_exec_btn.config(command=self.on_execute_queue)
        self.app.queue_clear_btn.config(command=self.on_clear_queue)
        self.app.queue_remove_btn.config(command=self.on_remove_selected_operation)
        self.app.queue_export_btn.config(command=self.on_export_queue)
        self.app.queue_import_btn.config(command=self.on_import_queue)    
    # Camera event handlers
    def on_start_camera(self):
        """Start camera stream"""
        result = self.app.webcam.stream_starten(self.app.camera_label)
        if result:
            self.app.logger.log("Kamera gestartet")
        else:
            self.app.logger.log("Fehler beim Starten der Kamera")
    
    def on_stop_camera(self):
        """Stop camera"""
        self.app.webcam.stoppen()
        self.app.camera_label.config(text="Kamera gestoppt", image="")
        self.app.logger.log("Kamera gestoppt")
    
    def on_take_photo(self):
        """Take photo"""
        success = self.app.webcam.foto_aufnehmen(delay=self.app.global_delay)
        if success:
            self.app.logger.log("Foto aufgenommen")
        else:
            self.app.logger.log("Fehler beim Aufnehmen des Fotos")
    
    def on_add_photo_to_queue(self):
        """Add photo to queue"""
        self.app.queue_ops.add_photo_to_queue()
    
    def on_set_camera_device(self):
        """Set camera device index"""
        try:
            idx = int(self.app.camera_device_index_var.get())
            self.app.webcam.stoppen()
            from webcam_helper import WebcamHelper
            self.app.webcam = WebcamHelper(device_index=idx, frame_size=(320, 240))
            self.app.widgets['webcam'] = self.app.webcam
            self.app.logger.log(f"Kamera Device Index auf {idx} gesetzt. Kamera neu initialisiert.")
        except Exception as e:
            self.app.logger.log(f"Fehler beim Setzen des Kamera Device Index: {e}")
    
    def on_set_delay(self):
        """Set autofocus delay"""
        try:
            self.app.global_delay = float(self.app.camera_delay_var.get())
            self.app.logger.log(f"Globale Autofokus-Delay auf {self.app.global_delay}s gesetzt")
        except ValueError:
            self.app.logger.log("Fehler: Ungültiger Delay-Wert")
      # Servo event handlers
    def on_servo_execute(self):
        """Execute servo command in separate thread to avoid blocking camera"""
        def servo_thread():
            self.app.device_control.servo_cmd()
        
        thread = threading.Thread(target=servo_thread)
        thread.daemon = True
        thread.start()
    
    def on_servo_add_to_queue(self):
        """Add servo to queue"""
        self.app.queue_ops.add_servo_to_queue()
    
    # Stepper event handlers
    def on_stepper_execute(self):
        """Execute stepper command in separate thread to avoid blocking camera"""
        def stepper_thread():
            self.app.device_control.stepper_cmd()
        
        thread = threading.Thread(target=stepper_thread)
        thread.daemon = True
        thread.start()
    
    def on_stepper_add_to_queue(self):
        """Add stepper to queue"""
        self.app.queue_ops.add_stepper_to_queue()
      # LED event handlers
    def on_led_execute(self):
        """Execute LED color command in separate thread to avoid blocking camera"""
        def led_thread():
            self.app.device_control.led_cmd()
        
        thread = threading.Thread(target=led_thread)
        thread.daemon = True
        thread.start()
    
    def on_led_add_to_queue(self):
        """Add LED color to queue"""
        self.app.queue_ops.add_led_color_to_queue()
    
    def on_brightness_execute(self):
        """Execute LED brightness command in separate thread to avoid blocking camera"""
        def brightness_thread():
            self.app.device_control.bright_cmd()
        
        thread = threading.Thread(target=brightness_thread)
        thread.daemon = True
        thread.start()
    
    def on_brightness_add_to_queue(self):
        """Add LED brightness to queue"""
        self.app.queue_ops.add_brightness_to_queue()
      # Button event handlers
    def on_button_execute(self):
        """Execute button status command in separate thread to avoid blocking camera"""
        def button_thread():
            self.app.device_control.button_cmd()
        
        thread = threading.Thread(target=button_thread)
        thread.daemon = True
        thread.start()
    
    def on_button_add_to_queue(self):
        """Add button status to queue"""
        self.app.queue_ops.add_button_to_queue()
    
    # Home event handlers
    def on_home_execute(self):
        """Execute home function in separate thread to avoid blocking camera"""
        def home_thread():
            self.app.device_control.home_func()
        
        thread = threading.Thread(target=home_thread)
        thread.daemon = True
        thread.start()
    
    def on_home_add_to_queue(self):
        """Add home function to queue"""
        self.app.queue_ops.add_home_to_queue()
    
    # Angle calculator event handlers
    def on_show_angle_calculator(self):
        """Show angle calculator dialog"""
        from angle_calculator_commands import show_angle_calculator_dialog
        show_angle_calculator_dialog(self.app.root, self.app.logger)
    
    def on_load_csv(self):
        """Load CSV data"""
        if hasattr(self.app, 'angle_calculator') and self.app.angle_calculator:
            self.app.angle_calculator.load_csv_data()
    
    def on_save_csv(self):
        """Save CSV data"""
        if hasattr(self.app, 'angle_calculator') and self.app.angle_calculator:
            self.app.angle_calculator.save_csv_data()
    
    # Queue event handlers
    def on_execute_queue(self):
        """Execute operation queue"""
        def run_queue_with_repeat():
            while True:
                base_url = self.app.base_url_var.get()
                if not base_url:
                    self.app.logger.log("Keine URL konfiguriert!")
                    break
                
                self.app.logger.log(f"Führe Warteschlange für {base_url} aus...")
                self.app.operation_queue.execute_all(
                    base_url,
                    self.app.widgets,
                    self.app.position,
                    self.app.servo_angle_var,
                    self.app.last_distance_value,
                    run_in_thread=False
                )
                
                if not self.app.repeat_queue.get():
                    break
                
                self.app.logger.log("Wiederhole Warteschlange...")
        
        threading.Thread(target=run_queue_with_repeat, daemon=True).start()
    
    def on_clear_queue(self):
        """Clear operation queue"""
        self.app.operation_queue.clear()
    
    def on_remove_selected_operation(self):
        """Remove selected operation from queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            self.app.operation_queue.remove(selection[0])
    
    def on_export_queue(self):
        """Export queue to CSV"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            # Check if operation_queue has export method
            if hasattr(self.app.operation_queue, 'export_to_csv'):
                self.app.operation_queue.export_to_csv(filename)
                self.app.logger.log(f"Queue exportiert nach: {filename}")
            else:
                self.app.logger.log("Export-Funktion nicht verfügbar")
    
    def on_import_queue(self):
        """Import queue from CSV"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            # Check if operation_queue has import method
            if hasattr(self.app.operation_queue, 'import_from_csv'):
                self.app.operation_queue.import_from_csv(filename)
                self.app.logger.log(f"Queue importiert von: {filename}")
            else:
                self.app.logger.log("Import-Funktion nicht verfügbar")
