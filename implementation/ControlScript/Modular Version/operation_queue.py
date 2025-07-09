"""
Operations-Queue-Modul
Verwaltet die Operationswarteschlange

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""
import time
import threading
import tkinter as tk
from api_client import ApiClient

# Konstante für Berechnungen
PI = 3.141592653589793

class OperationQueue:
    """
    Klasse für die Verwaltung der Operationswarteschlange
    Verarbeitet das Hinzufügen, Entfernen und Ausführen von Operationen in einer Warteschlange.
    """
    
    def __init__(self, logger, queue_list):
        """
        Initialisiert die Operationswarteschlange
        
        Args:
            logger: Die Logger-Instanz für die Protokollierung
            queue_list: Das Listbox-Widget zur Anzeige der Warteschlange
        """
        self.operations = []
        self.logger = logger
        self.queue_list = queue_list
        self.is_paused = False  # Pause-Status für die Warteschlange
        self.is_executing = False  # Ausführungsstatus
    
    def add(self, operation_type, params, description):
        """
        Fügt eine Operation zur Warteschlange hinzu
        
        Args:
            operation_type (str): Der Typ der Operation (servo, stepper usw.)
            params (dict): Die Parameter für die Operation
            description (str): Eine menschenlesbare Beschreibung der Operation
        """
        self.operations.append({
            'type': operation_type,
            'params': params,
            'description': description
        })
        self.update_display()
        self.logger.log(f"Zur Warteschlange hinzugefügt: {description}")
    
    def clear(self):
        """Löscht alle Operationen aus der Warteschlange"""
        self.operations.clear()
        self.update_display()
        self.logger.log("Operationswarteschlange gelöscht")
    
    def import_from_csv(self, file_path):
        """
        Importiert Operationen aus einer CSV-Datei in die Warteschlange
        
        Args:
            file_path (str): Pfad zur CSV-Datei
        """
        try:
            import csv
            import json
            import os
            
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.clear()  # Warteschlange leeren vor Import
                imported_count = 0
                
                for row in reader:
                    op_type = row['type']
                    params = json.loads(row['params'])
                    description = row['description']
                    self.add(op_type, params, description)
                    imported_count += 1
                    
            self.logger.log(f"✅ CSV erfolgreich importiert: {os.path.basename(file_path)}")
            self.logger.log(f"📋 {imported_count} Operationen zur Warteschlange hinzugefügt")
            
            # Optional: Show success message
            from tkinter import messagebox
            messagebox.showinfo("Import erfolgreich", f"CSV wurde erfolgreich importiert!\n{imported_count} Operationen hinzugefügt.")
            
        except Exception as e:
            self.logger.log(f"❌ Fehler beim CSV-Import: {str(e)}")
            from tkinter import messagebox
            messagebox.showerror("Import Fehler", f"Fehler beim Importieren der CSV-Datei:\n{str(e)}")

    def export_to_csv(self, file_path):
        """
        Exportiert die aktuelle Warteschlange als CSV-Datei
        
        Args:
            file_path (str): Pfad zur zu erstellenden CSV-Datei
        """
        try:
            import csv
            import json
            import os
            
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "params", "description"])
                
                for op in self.operations:
                    writer.writerow([
                        op['type'],
                        json.dumps(op['params']),
                        op['description']
                    ])
                    
            self.logger.log(f"✅ CSV erfolgreich exportiert: {os.path.basename(file_path)}")
            
            # Optional: Show success message
            from tkinter import messagebox
            messagebox.showinfo("Export erfolgreich", f"Warteschlange wurde als CSV gespeichert: {os.path.basename(file_path)}")
            
        except Exception as e:
            self.logger.log(f"❌ Fehler beim CSV-Export: {str(e)}")
            from tkinter import messagebox
            messagebox.showerror("Export Fehler", f"Fehler beim Exportieren der CSV-Datei:\n{str(e)}")

    def remove(self, index):
        """
        Entfernt eine Operation aus der Warteschlange nach Index
        
        Args:
            index (int): Der Index der zu entfernenden Operation
        """
        if 0 <= index < len(self.operations):
            removed_op = self.operations.pop(index)
            self.update_display()
            self.logger.log(f"Operation entfernt: {removed_op['description']}")
        else:
            self.logger.log("Ungültiger Index für das Entfernen der Operation")

    def update_display(self):
        """Aktualisiert die Anzeige der Warteschlange in der GUI"""
        self.queue_list.delete(0, tk.END)
        for i, op in enumerate(self.operations):
            self.queue_list.insert(tk.END, f"{i+1}. {op['description']}")

    def execute_all(self, base_url, widgets, position_var, servo_angle_var, last_distance_value, run_in_thread=True):
        """
        Führt alle Operationen in der Warteschlange sequentiell aus
        
        Args:
            base_url (str): Die Basis-URL der API
            widgets (dict): Wörterbuch der für Operationen benötigten UI-Widgets
            position_var: Die DoubleVar zur Verfolgung der aktuellen Position
            servo_angle_var: Die IntVar zur Verfolgung des aktuellen Servo-Winkels
            last_distance_value: Die StringVar für den letzten Distanzwert
            run_in_thread (bool): Ob die Ausführung in einem Thread erfolgen soll (Standard: True)
        """
        if not self.operations:
            self.logger.log("Warteschlange ist leer. Nichts auszuführen.")
            return
        
        self.logger.log("Starte Warteschlangenausführung...")
        self.is_executing = True  # Ausführungsstatus setzen
        
        def run_queue():
            """Führt alle Operationen in der Warteschlange in einem separaten Thread aus"""
            try:
                for idx, op in enumerate(self.operations):
                    # Prüfe, ob die Ausführung gestoppt wurde
                    if not self.is_executing:
                        self.logger.log("Warteschlangenausführung gestoppt")
                        break
                        
                    # Prüfe, ob pausiert
                    if self.is_paused:
                        self.logger.log("Warteschlange pausiert. Warte auf Fortsetzung...")
                        while self.is_paused and self.is_executing:
                            time.sleep(0.1)  # Kurze Pause, um nicht zu blockieren
                        
                        if not self.is_executing:
                            break
                    
                    # Führe die einzelne Operation aus
                    self.logger.log(f"Führe aus {idx+1}/{len(self.operations)}: {op['description']}")
                    self.execute_single_operation(op, base_url, widgets, position_var, servo_angle_var, last_distance_value)
                    
                    # Kleine Pause zwischen Operationen
                    time.sleep(0.1)
                    
            except Exception as e:
                self.logger.log(f"Fehler bei der Warteschlangenausführung: {e}")
            finally:
                self.logger.log("Warteschlangenausführung abgeschlossen!")
                self.is_executing = False  # Ausführungsstatus zurücksetzen
        
        if run_in_thread:
            thread = threading.Thread(target=run_queue, daemon=True)
            thread.start()
        else:
            run_queue()

    def execute_single_operation(self, operation, base_url, widgets, position_var, servo_angle_var, last_distance_value):
        """
        Führt eine einzelne Operation aus
        
        Args:
            operation (dict): Die auszuführende Operation
            base_url (str): Die Basis-URL der API
            widgets (dict): Wörterbuch der für Operationen benötigten UI-Widgets
            position_var: Die DoubleVar zur Verfolgung der aktuellen Position
            servo_angle_var: Die IntVar zur Verfolgung des aktuellen Servo-Winkels
            last_distance_value: Die StringVar für den letzten Distanzwert
        """
        try:
            if operation['type'] == 'servo':
                angle = operation['params']['angle']
                ApiClient.set_servo_angle(angle, base_url)
                self.logger.log(f"Servo: Winkel {angle}°")
                servo_angle_var.set(angle)
                widgets['root'].after(0, lambda: widgets['update_position_label']())

            elif operation['type'] == 'stepper':
                steps = operation['params']['steps']
                direction = operation['params']['direction']
                speed = operation['params'].get('speed')
                d = float(widgets['diameter_entry'].get())
                circumference = PI * d  # mm
                distance_cm = (steps / 4096) * (circumference / 10)
                
                # Motorbefehl ausführen
                ApiClient.move_stepper(steps, direction, speed, base_url)
                self.logger.log(f"Stepper: {steps} Schritte, Richtung {direction}, Geschwindigkeit: {speed}")
                
                # Position aktualisieren
                if direction == 1:
                    position_var.set(position_var.get() + distance_cm)
                else:
                    position_var.set(position_var.get() - distance_cm)
                    
                widgets['root'].after(0, lambda: widgets['update_position_label']())

            elif operation['type'] == 'led_color':
                color_hex = operation['params']['color']
                ApiClient.set_led_color(color_hex, base_url)
                self.logger.log(f"LED: Farbe auf {color_hex} gesetzt")

            elif operation['type'] == 'led_brightness':
                brightness = operation['params']['brightness']
                ApiClient.set_led_brightness(brightness, base_url)
                self.logger.log(f"LED: Helligkeit auf {brightness}% gesetzt")

            elif operation['type'] == 'button':
                button_state = ApiClient.get_button_state(base_url)
                self.logger.log(f"Button-Status: {button_state}")

            elif operation['type'] == 'home':
                self._home_function(base_url, widgets, position_var, servo_angle_var)

            elif operation['type'] == 'photo':
                delay = operation['params'].get('delay', 0.5)
                camera_index = operation['params'].get('camera_index', 0)
                
                # Switch to the correct camera before taking photo
                try:
                    # Find the main app instance and switch camera
                    if 'global_delay' in widgets and hasattr(widgets['global_delay'], 'switch_camera'):
                        main_app = widgets['global_delay']
                        
                        self.logger.log(f"📷 Bereite Foto mit Kamera {camera_index} vor...")
                        
                        # Switch camera and ensure stream is running
                        stream_success = main_app.switch_camera(camera_index)
                        
                        if stream_success:
                            # Use the specific webcam for the selected camera index
                            if camera_index in main_app.webcams:
                                webcam = main_app.webcams[camera_index]
                                self.logger.log(f"📸 Nehme Foto mit Kamera {camera_index} auf (Stream initialisiert)...")
                                foto_path = webcam.shoot_pic(delay=delay)
                            else:
                                self.logger.log(f"❌ Kamera {camera_index} nicht verfügbar")
                                foto_path = None
                        else:
                            self.logger.log(f"❌ Kamera {camera_index} Stream konnte nicht gestartet werden")
                            foto_path = None
                    elif 'webcams' in widgets and camera_index in widgets['webcams']:
                        # Direct camera access if switch fails
                        webcam = widgets['webcams'][camera_index]
                        foto_path = webcam.shoot_pic(delay=delay)
                    else:
                        # Fallback to default webcam
                        foto_path = widgets['webcam'].shoot_pic(delay=delay)
                        
                    if foto_path:
                        self.logger.log(f"✅ Foto gespeichert von Kamera {camera_index}: {foto_path}")
                    else:
                        self.logger.log(f"❌ Fehler beim Aufnehmen des Fotos von Kamera {camera_index}")
                        
                except Exception as e:
                    self.logger.log(f"❌ Fehler bei Foto-Operation: {e}")
                    # Fallback
                    foto_path = widgets['webcam'].shoot_pic(delay=delay)
                    if foto_path:
                        self.logger.log(f"✅ Foto gespeichert (Fallback): {foto_path}")
                    else:
                        self.logger.log(f"❌ Fehler beim Aufnehmen des Fotos (Fallback)")

            else:
                self.logger.log(f"Unbekannter Operationstyp: {operation['type']}")
                
        except Exception as e:
            self.logger.log(f"Fehler bei der Ausführung der Operation: {e}")

    def pause_queue(self):
        """Pausiert die Warteschlangenausführung"""
        self.is_paused = True
        self.logger.log("Warteschlange pausiert")

    def resume_queue(self):
        """Setzt die Warteschlangenausführung fort"""
        self.is_paused = False
        self.logger.log("Warteschlange fortgesetzt")

    def stop_queue(self):
        """Stoppt die Warteschlangenausführung"""
        self.is_executing = False
        self.is_paused = False
        self.logger.log("Warteschlangenausführung gestoppt")

    def _home_function(self, base_url, widgets, position_var, servo_angle_var):
        """
        Führt die Home-Funktion aus (ohne Button-Erkennung)
        """
        try:
            self.logger.log("Starte Home-Funktion...")
            
            # Aktuelle Eingaben lesen
            d = float(widgets['diameter_entry'].get())
            speed = int(widgets['stepper_speed'].get()) if widgets['stepper_speed'].get() else 80
            
            # Home-Bewegung: 500 Schritte nach oben
            params = {"steps": 500, "direction": 1, "speed": speed}
            ApiClient.make_request("setMotor", params, base_url)
            
            # Position berechnen und aktualisieren
            circumference = PI * d
            distance_cm = (500 / 4096) * (circumference / 10)
            pos_cm = position_var.get() + distance_cm
            position_var.set(0)  # Home-Position auf 0 setzen
            
            self.logger.log(f"Home-Funktion: 500 Schritte nach oben, Position auf 0 gesetzt")
            widgets['root'].after(0, lambda: widgets['update_position_label']())
            
        except Exception as e:
            self.logger.log(f"Fehler in der Home-Funktion: {e}")
