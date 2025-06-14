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
        self.logger.log("Warteschlange geleert")
    
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
            removed = self.operations.pop(index)
            self.update_display()
            self.logger.log(f"Aus der Warteschlange entfernt: {removed['description']}")
    
    def update_display(self):
        """
        Aktualisiert die Anzeige der Warteschlange in der Benutzeroberfläche
        Aktualisiert die Liste der Operationen, die in der Warteschlange-Listbox angezeigt werden
        """
        self.queue_list.delete(0, tk.END)  # Aktuelle Einträge löschen
        for idx, op in enumerate(self.operations):
            self.queue_list.insert(tk.END, f"{idx+1}. {op['description']}")
    
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
        
        def run_queue():
            """Führt alle Operationen in der Warteschlange in einem separaten Thread aus"""
            total_distance = 0  # Verfolge die Gesamtdistanz für die Aktualisierung des Distanzfelds
            
            for idx, op in enumerate(self.operations):
                try:
                    self.logger.log(f"Führe aus {idx+1}/{len(self.operations)}: {op['description']}")

                    if op['type'] == 'servo':
                        angle = op['params']['angle']
                        ApiClient.set_servo_angle(angle, base_url)
                        self.logger.log(f"Servo: Winkel {angle}°")
                        servo_angle_var.set(angle)
                        widgets['root'].after(0, lambda: widgets['update_position_label']())

                    elif op['type'] == 'stepper':
                        steps = op['params']['steps']
                        direction = op['params']['direction']
                        speed = op['params'].get('speed')
                        d = float(widgets['diameter_entry'].get())
                        circumference = PI * d  # mm
                        distance_cm = (steps / 4096) * (circumference / 10)
                        if direction == 1:
                            total_distance += distance_cm
                        else:
                            total_distance -= distance_cm
                        # Motorbefehl wirklich ausführen:
                        ApiClient.move_stepper(steps, direction, speed, base_url)
                        self.logger.log(f"Stepper: {steps} Schritte, Richtung {direction}, Geschwindigkeit: {speed}")

                    elif op['type'] == 'led_color':
                        color_hex = op['params']['color']
                        ApiClient.set_led_color(color_hex, base_url)
                        self.logger.log(f"LED: Farbe auf {color_hex} gesetzt")

                    elif op['type'] == 'led_brightness':
                        brightness = op['params']['brightness']
                        ApiClient.set_led_brightness(brightness, base_url)
                        self.logger.log(f"LED: Helligkeit auf {brightness}% gesetzt")

                    elif op['type'] == 'button':
                        response = ApiClient.get_button_state(base_url)
                        self.logger.log(f"Button-Status: {response}")

                    elif op['type'] == 'home':
                        self._execute_home_function(base_url, widgets, position_var, last_distance_value)
                        self.logger.log("Home-Funktion ausgeführt")

                    elif op['type'] == 'photo':
                        # Delay aus den Parametern lesen, oder globale Delay verwenden
                        delay = op['params'].get('delay')
                        if delay is None:
                            # Globale Delay aus widgets verwenden
                            global_delay_obj = widgets.get('global_delay')
                            if global_delay_obj and hasattr(global_delay_obj, 'global_delay'):
                                delay = global_delay_obj.global_delay
                            else:
                                delay = 0.5  # Fallback
                        
                        webcam_helper = widgets.get('webcam', None)
                        if webcam_helper and webcam_helper.running and webcam_helper.current_frame is not None:
                            self.logger.log(f"Foto wird aufgenommen mit {delay}s Autofokus-Delay...")
                            foto_path = webcam_helper.foto_aufnehmen(delay=delay)
                            if foto_path:
                                self.logger.log(f"Foto aufgenommen und gespeichert als: {foto_path}")
                            else:
                                self.logger.log("Fehler: Foto konnte nicht gespeichert werden")
                        else:
                            self.logger.log("Fehler: Kamera nicht aktiv oder kein Bild verfügbar")

                    time.sleep(0.5)
                except Exception as e:
                    self.logger.log(f"Fehler bei der Ausführung von Operation {idx+1}: {e}")
            
            self.logger.log("Warteschlangenausführung abgeschlossen!")
        
        if run_in_thread:
            threading.Thread(target=run_queue).start()
        else:
            run_queue()
    
    def _execute_home_function(self, base_url, widgets, position_var, last_distance_value):
        """
        Führt die Home-Funktion als Teil der Warteschlangenausführung aus
        Bewegt den Schrittmotor nach unten, bis der Button gedrückt wird,
        dann leicht nach oben und setzt die Position auf Null zurück.
        
        Args:
            base_url (str): Die Basis-URL der API
            widgets (dict): Wörterbuch der für Operationen benötigten UI-Widgets
            position_var: Die DoubleVar zur Verfolgung der aktuellen Position
            last_distance_value: Die StringVar für den letzten Distanzwert
        """
        try:
            d = float(widgets['diameter_entry'].get())
            self.logger.log('Starte Home-Funktion...')
            
            # Button-Status zurücksetzen
            self.logger.log("Setze Button-Status zurück...")
            reset_attempts = 0
            max_reset_attempts = 10
            
            # Warten, bis der Button nicht mehr gedrückt ist
            while reset_attempts < max_reset_attempts:
                reset_attempts += 1
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                button_still_pressed = ApiClient.is_button_pressed(btn_response)
                
                if button_still_pressed:
                    self.logger.log(f"Button noch immer gedrückt, warte auf Freigabe (Versuch {reset_attempts})...")
                    time.sleep(1)
                else:
                    self.logger.log(f"Button freigegeben, fahre mit Home-Funktion fort.")
                    break
            
            if reset_attempts >= max_reset_attempts:
                self.logger.log("Warnung: Konnte Button-Status nicht zurücksetzen, fahre trotzdem fort.")
            
            # Mit Home-Funktion fortfahren
            time.sleep(1)
            
            # Anfängliche 100 Schritte nach unten
            speed = int(widgets['stepper_speed'].get())
            params = {"steps": 100, "direction": -1, "speed": speed}
            ApiClient.make_request("setMotor", params, base_url)
            pos_cm = position_var.get() - (100 / 4096 * PI * d / 10)
            distance_cm = (100 / 4096 * PI * d / 10)
            self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction abwärts, Position: {pos_cm:.2f} cm")
            
            # Schleife, bis der Button gedrückt wird - reduzierte Protokollierung
            max_attempts = 100
            attempt = 0
            button_pressed = False
            
            while not button_pressed and attempt < max_attempts:
                attempt += 1
                
                # Button-Status abfragen
                btn_response = ApiClient.get_button_state(base_url, nocache=True)
                
                # Nur bei wichtigen Ereignissen protokollieren
                if attempt % 5 == 0:
                    self.logger.log(f"Button-Überprüfungsversuch {attempt}: Noch nicht gedrückt")
                
                # Button-Status überprüfen
                button_pressed = ApiClient.is_button_pressed(btn_response)
                
                if button_pressed:
                    # Button gedrückt, 100 Schritte nach oben und fertig
                    self.logger.log(f"Button-Druck bei Versuch {attempt} erkannt")
                    params = {"steps": 100, "direction": 1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = position_var.get() + (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction aufwärts, Position: {pos_cm:.2f} cm")
                    break
                else:
                    # Button nicht gedrückt, weitere 100 Schritte nach unten
                    params = {"steps": 100, "direction": -1, "speed": speed}
                    ApiClient.make_request("setMotor", params, base_url)
                    pos_cm = position_var.get() - (100 / 4096 * PI * d / 10)
                    distance_cm = (100 / 4096 * PI * d / 10)
                    self.logger.log(f"Motor: 100 Steps, {distance_cm:.2f} cm, Direction abwärts, Position: {pos_cm:.2f} cm")
                    
                    # Verzögerung nach jedem Schritt
                    time.sleep(0.5)
            
            # Bei Bedarf warnen
            if not button_pressed:
                self.logger.log("Warnung: Maximale Versuche erreicht, ohne Button-Druck zu erkennen.")
                
            # Position auf 0 setzen
            position_var.set(0)
            widgets['root'].after(0, lambda: widgets['update_position_label']())
            self.logger.log("Home-Funktion abgeschlossen, Position auf 0 gesetzt.")
            
            # Distanzfeld zurücksetzen
            widgets['root'].after(0, lambda: (
                widgets['stepper_length_cm'].delete(0, tk.END),
                widgets['stepper_length_cm'].insert(0, "0.00")
            ))
        except Exception as e:
            self.logger.log(f"Fehler in der Home-Funktion: {e}")
