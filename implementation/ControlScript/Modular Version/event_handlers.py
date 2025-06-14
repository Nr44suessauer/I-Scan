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
          # Calculator Commands Panel callbacks
        if hasattr(self.app, 'calc_widgets'):
            self.app.calc_widgets['visual_btn'].config(command=self.execute_visualisation_mode)
            self.app.calc_widgets['silent_btn'].config(command=self.execute_silent_mode)
        
        # Bind calculator parameter events for real-time command update
        if hasattr(self.app, 'calc_vars'):
            for var_name, entry_widget in self.app.calc_vars.items():
                entry_widget.bind('<KeyRelease>', self.update_command_display)
                entry_widget.bind('<FocusOut>', self.update_command_display)
        
        # Queue callbacks
        self.app.queue_exec_btn.config(command=self.on_execute_queue)
        self.app.queue_pause_btn.config(command=self.on_pause_queue)
        self.app.queue_exec_selected_btn.config(command=self.on_execute_selected_operation)
        self.app.queue_clear_btn.config(command=self.on_clear_queue)
        self.app.queue_remove_btn.config(command=self.on_remove_selected_operation)
        self.app.queue_duplicate_btn.config(command=self.on_duplicate_selected_operation)
        self.app.queue_edit_btn.config(command=self.on_edit_selected_operation)
        self.app.queue_settings_btn.config(command=self.on_queue_settings)
        self.app.queue_move_up_btn.config(command=self.on_move_operation_up)
        self.app.queue_move_down_btn.config(command=self.on_move_operation_down)
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
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]        )
        if filename:
            # Check if operation_queue has import method
            if hasattr(self.app.operation_queue, 'import_from_csv'):
                self.app.operation_queue.import_from_csv(filename)
                self.app.logger.log(f"Queue importiert von: {filename}")
            else:
                self.app.logger.log("Import-Funktion nicht verfügbar")
    
    def on_pause_queue(self):
        """Pause/Resume queue execution"""
        if hasattr(self.app.operation_queue, 'is_paused'):
            if self.app.operation_queue.is_paused:
                self.app.operation_queue.is_paused = False
                self.app.queue_pause_btn.config(text="Pausieren", bg="orange")
                self.app.logger.log("Queue-Ausführung fortgesetzt")
            else:
                self.app.operation_queue.is_paused = True
                self.app.queue_pause_btn.config(text="Fortsetzen", bg="lightblue")
                self.app.logger.log("Queue-Ausführung pausiert")
        else:
            # Add pause functionality to operation queue if not available
            self.app.operation_queue.is_paused = True
            self.app.queue_pause_btn.config(text="Fortsetzen", bg="lightblue")
            self.app.logger.log("Queue-Ausführung pausiert")
    
    def on_execute_selected_operation(self):
        """Execute only the selected operation from queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            selected_index = selection[0]
            base_url = self.app.base_url_var.get()
            if not base_url:
                self.app.logger.log("Keine URL konfiguriert!")
                return
            
            # Get the operation from the queue
            if hasattr(self.app.operation_queue, 'operations') and selected_index < len(self.app.operation_queue.operations):
                operation = self.app.operation_queue.operations[selected_index]
                self.app.logger.log(f"Führe ausgewählte Operation aus: {operation}")
                
                # Execute single operation
                def execute_single():
                    self.app.operation_queue.execute_single_operation(
                        operation,
                        base_url,
                        self.app.widgets,
                        self.app.position,
                        self.app.servo_angle_var,
                        self.app.last_distance_value
                    )
                
                threading.Thread(target=execute_single, daemon=True).start()
            else:
                self.app.logger.log("Fehler beim Zugriff auf die ausgewählte Operation")
        else:
            self.app.logger.log("Keine Operation ausgewählt")
    
    def on_duplicate_selected_operation(self):
        """Duplicate the selected operation in queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            selected_index = selection[0]
            if hasattr(self.app.operation_queue, 'operations') and selected_index < len(self.app.operation_queue.operations):
                operation = self.app.operation_queue.operations[selected_index]
                # Add copy of the operation
                self.app.operation_queue.operations.insert(selected_index + 1, operation.copy() if hasattr(operation, 'copy') else operation)
                self.app.operation_queue.update_display()
                self.app.logger.log("Operation kopiert")
            else:
                self.app.logger.log("Fehler beim Kopieren der Operation")
        else:
            self.app.logger.log("Keine Operation zum Kopieren ausgewählt")
    
    def on_move_operation_up(self):
        """Move selected operation up in queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            selected_index = selection[0]
            if selected_index > 0 and hasattr(self.app.operation_queue, 'operations'):
                # Swap operations
                operations = self.app.operation_queue.operations
                operations[selected_index], operations[selected_index - 1] = operations[selected_index - 1], operations[selected_index]
                self.app.operation_queue.update_display()
                # Keep selection on the moved item
                self.app.queue_list.selection_set(selected_index - 1)
                self.app.logger.log("Operation nach oben verschoben")
            else:
                self.app.logger.log("Operation kann nicht weiter nach oben verschoben werden")
        else:
            self.app.logger.log("Keine Operation zum Verschieben ausgewählt")
    
    def on_move_operation_down(self):
        """Move selected operation down in queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            selected_index = selection[0]
            if hasattr(self.app.operation_queue, 'operations') and selected_index < len(self.app.operation_queue.operations) - 1:
                # Swap operations
                operations = self.app.operation_queue.operations
                operations[selected_index], operations[selected_index + 1] = operations[selected_index + 1], operations[selected_index]
                self.app.operation_queue.update_display()
                # Keep selection on the moved item                self.app.queue_list.selection_set(selected_index + 1)
                self.app.logger.log("Operation nach unten verschoben")
            else:
                self.app.logger.log("Operation kann nicht weiter nach unten verschoben werden")
        else:
            self.app.logger.log("Keine Operation zum Verschieben ausgewählt")

    def on_edit_selected_operation(self):
        """Edit selected operation in queue"""
        selection = self.app.queue_list.curselection()
        if selection:
            selected_index = selection[0]
            if hasattr(self.app.operation_queue, 'operations') and selected_index < len(self.app.operation_queue.operations):
                operation = self.app.operation_queue.operations[selected_index]
                self._show_edit_dialog(operation, selected_index)
            else:
                self.app.logger.log("Fehler beim Zugriff auf die Operation")
        else:
            self.app.logger.log("Keine Operation zum Bearbeiten ausgewählt")
    
    def on_queue_settings(self):
        """Show queue execution settings"""
        self._show_queue_settings_dialog()
    
    def _show_edit_dialog(self, operation, index):
        """Show edit dialog for operation"""
        import tkinter as tk
        from tkinter import messagebox
        
        edit_window = tk.Toplevel(self.app.root)
        edit_window.title(f"Operation {index + 1} bearbeiten")
        edit_window.geometry("350x300")
        edit_window.transient(self.app.root)
        edit_window.grab_set()
        
        # Info
        tk.Label(edit_window, text=f"Typ: {operation['type']}", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(edit_window, text=operation['description'], wraplength=300).pack(pady=5)
        
        # Parameters
        params_frame = tk.LabelFrame(edit_window, text="Parameter")
        params_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        param_vars = {}
        for param_name, param_value in operation['params'].items():
            if param_name in ['delay', 'repeat_count']:
                continue
            
            frame = tk.Frame(params_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            tk.Label(frame, text=f"{param_name}:", width=12, anchor="w").pack(side="left")
            param_vars[param_name] = tk.StringVar(value=str(param_value))
            tk.Entry(frame, textvariable=param_vars[param_name]).pack(side="left", fill="x", expand=True, padx=5)
        
        # Execution settings
        exec_frame = tk.LabelFrame(edit_window, text="Ausführung")
        exec_frame.pack(fill="x", padx=10, pady=5)
        
        exec_row = tk.Frame(exec_frame)
        exec_row.pack(fill="x", padx=5, pady=5)
        
        tk.Label(exec_row, text="Verzögerung (s):").pack(side="left")
        delay_var = tk.StringVar(value=str(operation['params'].get('delay', 0.5)))
        tk.Entry(exec_row, textvariable=delay_var, width=6).pack(side="left", padx=5)
        
        tk.Label(exec_row, text="Wiederh.:").pack(side="left", padx=(20, 0))
        repeat_var = tk.StringVar(value=str(operation['params'].get('repeat_count', 1)))
        tk.Entry(exec_row, textvariable=repeat_var, width=6).pack(side="left", padx=5)
        
        # Buttons
        btn_frame = tk.Frame(edit_window)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def save_changes():
            try:
                new_params = {}
                for param_name, var in param_vars.items():
                    value = var.get()
                    original = operation['params'][param_name]
                    if isinstance(original, int):
                        new_params[param_name] = int(value)
                    elif isinstance(original, float):
                        new_params[param_name] = float(value)
                    else:
                        new_params[param_name] = value
                
                new_params['delay'] = float(delay_var.get()) if delay_var.get() else 0.5
                new_params['repeat_count'] = int(repeat_var.get()) if repeat_var.get() else 1
                
                self.app.operation_queue.operations[index]['params'] = new_params
                self.app.operation_queue.update_display()
                edit_window.destroy()
                self.app.logger.log(f"Operation {index + 1} bearbeitet")
            except Exception as e:
                messagebox.showerror("Fehler", f"Speichern fehlgeschlagen:\n{str(e)}")
        
        tk.Button(btn_frame, text="Speichern", command=save_changes, bg="lightgreen", width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Abbrechen", command=edit_window.destroy, bg="lightcoral", width=10).pack(side="left", padx=5)
    
    def _show_queue_settings_dialog(self):
        """Show queue settings dialog"""
        import tkinter as tk
        
        settings_window = tk.Toplevel(self.app.root)
        settings_window.title("Queue-Einstellungen")
        settings_window.geometry("300x200")
        settings_window.transient(self.app.root)
        settings_window.grab_set()
        
        # Global settings
        global_frame = tk.LabelFrame(settings_window, text="Globale Einstellungen")
        global_frame.pack(fill="x", padx=10, pady=10)
        
        auto_repeat_var = tk.BooleanVar(value=self.app.repeat_queue.get())
        tk.Checkbutton(global_frame, text="Auto-Wiederholung der Queue", 
                      variable=auto_repeat_var).pack(anchor="w", padx=5, pady=5)
        
        # Batch operations
        batch_frame = tk.LabelFrame(settings_window, text="Batch-Operationen")
        batch_frame.pack(fill="x", padx=10, pady=5)
        
        apply_frame = tk.Frame(batch_frame)
        apply_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(apply_frame, text="Verzögerung für alle:").pack(side="left")
        batch_delay_var = tk.StringVar(value="0.5")
        tk.Entry(apply_frame, textvariable=batch_delay_var, width=8).pack(side="left", padx=5)
        
        def apply_to_all():
            try:
                delay = float(batch_delay_var.get())
                for op in self.app.operation_queue.operations:
                    op['params']['delay'] = delay
                self.app.operation_queue.update_display()
                self.app.logger.log(f"Verzögerung von {delay}s auf alle Operationen angewendet")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Fehler", f"Anwenden fehlgeschlagen:\n{str(e)}")
        
        tk.Button(apply_frame, text="Anwenden", command=apply_to_all, bg="lightyellow").pack(side="left", padx=5)
        
        # Buttons
        btn_frame = tk.Frame(settings_window)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def save_settings():
            self.app.repeat_queue.set(auto_repeat_var.get())
            settings_window.destroy()
            self.app.logger.log("Queue-Einstellungen gespeichert")
        
        tk.Button(btn_frame, text="OK", command=save_settings, bg="lightgreen", width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Abbrechen", command=settings_window.destroy, bg="lightcoral", width=10).pack(side="left", padx=5)

    # Calculator Commands Panel Methods
    def update_command_display(self, event=None):
        """
        Update the display of the current command
        """
        try:
            if not hasattr(self.app, 'calc_vars'):
                return
                
            csv_name = self.app.calc_vars['csv_name'].get()
            target_x = self.app.calc_vars['target_x'].get()
            target_y = self.app.calc_vars['target_y'].get()
            scan_distance = self.app.calc_vars['scan_distance'].get()
            measurements = self.app.calc_vars['measurements'].get()
            servo_min = self.app.calc_vars['servo_min'].get()
            servo_max = self.app.calc_vars['servo_max'].get()
            servo_neutral = self.app.calc_vars['servo_neutral'].get()
            
            command = f"python main.py --visualize --csv-name {csv_name} --target-x {target_x} --target-y {target_y} --scan-distance {scan_distance} --measurements {measurements} --servo-min {servo_min} --servo-max {servo_max} --servo-neutral {servo_neutral}"
            self.app.calc_widgets['current_command_label'].config(text=command)
        except Exception:
            pass
    
    def execute_visualisation_mode(self):
        """
        Execute the Visualisation Mode with current parameters
        """
        import subprocess
        import os
        try:
            if not hasattr(self.app, 'calc_vars'):
                return
                
            csv_name = self.app.calc_vars['csv_name'].get()
            target_x = float(self.app.calc_vars['target_x'].get())
            target_y = float(self.app.calc_vars['target_y'].get())
            scan_distance = float(self.app.calc_vars['scan_distance'].get())
            measurements = int(self.app.calc_vars['measurements'].get())
            servo_min = float(self.app.calc_vars['servo_min'].get())
            servo_max = float(self.app.calc_vars['servo_max'].get())
            servo_neutral = float(self.app.calc_vars['servo_neutral'].get())
            
            self.app.logger.log(f"🖼️ Starte Visualisation Mode: {csv_name}")
            self.app.logger.log(f"📍 Target: ({target_x}, {target_y}), Distance: {scan_distance}, Measurements: {measurements}")
            self.app.logger.log(f"🔧 Servo: Min={servo_min}°, Max={servo_max}°, Neutral={servo_neutral}°")

            calc_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Calculator_Angle_Maschine", "MathVisualisation")
            command = [
                "python", "main.py", "--visualize",
                "--csv-name", csv_name,
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ]

            def run_command():
                try:
                    result = subprocess.run(command, cwd=calc_dir, capture_output=True, text=True, encoding="utf-8")
                    if result.returncode == 0:
                        self.app.logger.log(f"✅ Visualisation Mode erfolgreich abgeschlossen")
                        self.app.logger.log("📊 Visualisierungen wurden im Calculator_Angle_Maschine/MathVisualisation/output/ Ordner gespeichert")
                        self.update_servo_graph_image()
                    else:
                        self.app.logger.log(f"❌ Visualisation Mode fehlgeschlagen: {result.stderr}")
                except Exception as e:
                    self.app.logger.log(f"❌ Fehler bei Visualisation Mode: {e}")

            threading.Thread(target=run_command).start()

        except Exception as e:
            self.app.logger.log(f"❌ Fehler bei Visualisation Mode: {e}")
            from tkinter import messagebox
            messagebox.showerror("Fehler", f"Fehler bei der Visualisation Mode Ausführung:\n{e}")
    
    def execute_silent_mode(self):
        """
        Execute the Silent Mode with current parameters
        """
        import subprocess
        import os
        try:
            if not hasattr(self.app, 'calc_vars'):
                return
                
            csv_name = self.app.calc_vars['csv_name'].get()
            target_x = float(self.app.calc_vars['target_x'].get())
            target_y = float(self.app.calc_vars['target_y'].get())
            scan_distance = float(self.app.calc_vars['scan_distance'].get())
            measurements = int(self.app.calc_vars['measurements'].get())
            servo_min = float(self.app.calc_vars['servo_min'].get())
            servo_max = float(self.app.calc_vars['servo_max'].get())
            servo_neutral = float(self.app.calc_vars['servo_neutral'].get())
            
            self.app.logger.log(f"🔇 Starte Silent Mode: {csv_name}")
            self.app.logger.log(f"📍 Target: ({target_x}, {target_y}), Distance: {scan_distance}, Measurements: {measurements}")
            self.app.logger.log(f"🔧 Servo: Min={servo_min}°, Max={servo_max}°, Neutral={servo_neutral}°")
            
            calc_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Calculator_Angle_Maschine", "MathVisualisation")
            command = [
                "python", "main.py", "--silent",
                "--csv-name", csv_name,
                "--target-x", str(target_x),
                "--target-y", str(target_y),
                "--scan-distance", str(scan_distance),
                "--measurements", str(measurements),
                "--servo-min", str(servo_min),
                "--servo-max", str(servo_max),
                "--servo-neutral", str(servo_neutral)
            ]
            
            def run_command():
                try:
                    result = subprocess.run(command, cwd=calc_dir, capture_output=True, text=True, encoding="utf-8")
                    if result.returncode == 0:
                        self.app.logger.log(f"✅ Silent Mode erfolgreich abgeschlossen")
                        # Search for generated CSV file
                        output_dir = os.path.join(calc_dir, "output")
                        csv_file = os.path.join(output_dir, f"{csv_name}.csv")
                        if os.path.exists(csv_file):
                            from tkinter import messagebox
                            if messagebox.askyesno("CSV Import", "CSV wurde erfolgreich generiert. Soll die CSV-Datei sofort in die Warteschlange importiert werden?"):
                                self.import_specific_csv(csv_file)
                    else:
                        self.app.logger.log(f"❌ Silent Mode fehlgeschlagen: {result.stderr}")
                except Exception as e:
                    self.app.logger.log(f"❌ Fehler bei Silent Mode: {e}")
            
            threading.Thread(target=run_command).start()
            
        except Exception as e:
            self.app.logger.log(f"❌ Fehler bei Silent Mode: {e}")
            from tkinter import messagebox
            messagebox.showerror("Fehler", f"Fehler bei der Silent Mode Ausführung:\n{e}")

    def import_specific_csv(self, csv_file):
        """Import a specific CSV file to the queue"""
        try:
            if hasattr(self.app.operation_queue, 'import_from_csv'):
                self.app.operation_queue.import_from_csv(csv_file)
                self.app.logger.log(f"CSV importiert: {csv_file}")
            else:
                self.app.logger.log("Import-Funktion nicht verfügbar")
        except Exception as e:
            self.app.logger.log(f"Fehler beim CSV Import: {e}")

    def update_servo_graph_image(self):
        """
        Update the servo graph image in the Calculator Commands Panel
        """
        self.load_servo_images()

    def load_servo_images(self):
        """
        Load both servo images (Graph and Cone Detail) with fixed size
        """
        try:
            if not hasattr(self.app, 'calc_widgets'):
                return
                
            import os
            from PIL import Image, ImageTk
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Path to Servo Graph
            graph_path = os.path.join(script_dir, "..", "Calculator_Angle_Maschine", "MathVisualisation", "output", "06_servo_geometry_graph_only.png")
            graph_path = os.path.normpath(graph_path)
            
            # Path to Cone Detail
            cone_path = os.path.join(script_dir, "..", "Calculator_Angle_Maschine", "MathVisualisation", "output", "07_servo_cone_detail.png")
            cone_path = os.path.normpath(cone_path)
            
            # Fixed image size (no permanent adjustment)
            max_width, max_height = 500, 400
            
            # Load Servo Graph with uniform scaling
            if os.path.exists(graph_path):
                img = Image.open(graph_path)
                # Calculate uniform scaling (maintain aspect ratio)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.app.servo_graph_img = ImageTk.PhotoImage(img)
                self.app.calc_widgets['servo_graph_img_label'].config(image=self.app.servo_graph_img, text="")
            else:
                self.app.calc_widgets['servo_graph_img_label'].config(image="", text=f"Servo Graph nicht gefunden:\n{graph_path}")
            
            # Load Cone Detail with uniform scaling
            if os.path.exists(cone_path):
                img = Image.open(cone_path)
                # Calculate uniform scaling (maintain aspect ratio)
                img_width, img_height = img.size
                scale_factor = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.app.servo_cone_img = ImageTk.PhotoImage(img)
                self.app.calc_widgets['servo_cone_img_label'].config(image=self.app.servo_cone_img, text="")
            else:
                self.app.calc_widgets['servo_cone_img_label'].config(image="", text=f"Cone Detail nicht gefunden:\n{cone_path}")
                
        except Exception as e:
            if hasattr(self.app, 'calc_widgets'):
                if 'servo_graph_img_label' in self.app.calc_widgets:
                    self.app.calc_widgets['servo_graph_img_label'].config(image="", text=f"Fehler beim Laden des Servo Graphs: {e}")
                if 'servo_cone_img_label' in self.app.calc_widgets:
                    self.app.calc_widgets['servo_cone_img_label'].config(image="", text=f"Fehler beim Laden des Cone Details: {e}")
