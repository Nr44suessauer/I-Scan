"""
Logger-Modul
Verwaltet die Protokollierung und Anzeige von Nachrichten

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
"""
import re
import tkinter as tk


class Logger:
    """
    Klasse für die Protokollierung und Anzeige von Nachrichten
    Verwaltet die Ausgabeanzeige und verarbeitet Protokollnachrichten zur Aktualisierung
    von Positions- und Servo-Winkelwerten aus dem Protokollinhalt.
    """
    
    def __init__(self, output_widget, position_var, servo_angle_var, update_callback):
        """
        Initialisiert den Logger mit UI-Elementen und zu überwachenden Variablen
        
        Args:
            output_widget: Das ScrolledText-Widget, in dem Protokolle angezeigt werden
            position_var: Die DoubleVar zur Verfolgung der aktuellen Position
            servo_angle_var: Die IntVar zur Verfolgung des aktuellen Servo-Winkels
            update_callback: Funktion, die nach der Aktualisierung von Position oder Winkel aufgerufen wird
        """
        self.output = output_widget
        self.position = position_var
        self.servo_angle_var = servo_angle_var
        self.update_callback = update_callback
    
    def log(self, msg):
        """
        Zeigt eine Nachricht im Protokoll mit entsprechender Formatierung und Farbe an
        Analysiert auch die Nachricht, um Positions- und Servo-Winkelwerte zu aktualisieren
        
        Args:
            msg (str): Die zu protokollierende Nachricht
        """
        # Nachrichtentyp bestimmen und Farbe basierend auf dem Inhalt auswählen
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["motor", "stepper", "schrittmotor", "steps"]):
            color = "#1e90ff"  # Blau für Motor-/Stepper-Nachrichten
        elif "servo" in msg_lower:
            color = "#228B22"  # Grün für Servo-Nachrichten
        elif "button" in msg_lower:
            color = "#ff8800"  # Orange für Button-Nachrichten
        elif "led" in msg_lower or "color" in msg_lower or "brightness" in msg_lower:
            color = "#c71585"  # Magenta für LED-Nachrichten
        else:
            color = "#000000"  # Schwarz für andere Nachrichten
            
        # Nachricht zum Ausgabe-Widget mit der ausgewählten Farbe hinzufügen
        self.output.config(state='normal')
        self.output.insert(tk.END, msg + "\n\n", (color,))
        self.output.tag_config(color, foreground=color)
        self.output.see(tk.END)
        self.output.config(state='disabled')
        
        # GUI nach jeder Protokollausgabe aktualisieren
        try:
            self.update_callback()
        except Exception:
            pass
            
        # Protokollnachricht analysieren, um Position und Servo-Winkel zu aktualisieren
        self._update_from_log(msg)
    
    def _update_from_log(self, msg):
        """
        Aktualisiert Position und Servo-Winkel basierend auf Protokollnachrichten
        Analysiert verschiedene Formate von Protokollnachrichten, um die relevanten Werte zu extrahieren
        
        Args:
            msg (str): Die zu analysierende Protokollnachricht
        """
        # Format 1: Standardformat mit Positionsfeld
        # "Motor: 100 Steps, 0.21 cm, Direction down, Position: 10.50 cm"
        try:
            motor_match = re.search(r"Motor:.*Steps,.*cm, Direction .*, Position: ([-\d\.]+) cm", msg)
            if motor_match:
                new_pos = float(motor_match.group(1))
                self.position.set(new_pos)
                self.update_callback()
                return
        except Exception:
            pass
            
        # Format 2: Legacy-Format (für Abwärtskompatibilität)
        # "3.5 cm → 1234 Steps (Gear 28.5 mm)...direction 1"
        try:
            match = re.search(r"([\d,.]+) cm → (\d+) Steps \(Gear ([\d,.]+) mm\).*direction ([-]?[1])", msg)
            if match:
                dist_cm = float(match.group(1).replace(",", "."))
                direction = int(match.group(4))
                pos_cm = self.position.get()
                if direction == 1:
                    self.position.set(pos_cm + dist_cm)
                else:
                    self.position.set(pos_cm - dist_cm)
                self.update_callback()
                return
        except Exception:
            pass
            
        # Servo-Log-Format: "Servo set to 45 degrees. Response: ..."
        try:
            servo_match = re.search(r"Servo: Angle (\d+)°", msg)
            if servo_match:
                angle = int(servo_match.group(1))
                self.servo_angle_var.set(angle)
                self.update_callback()
        except Exception:
            pass
