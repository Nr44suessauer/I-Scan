"""
WEBCAM HELPER MODULE
====================
Provides functions for controlling and displaying a webcam stream.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 1.1 - Improved thread safety for GUI updates
"""
import os
import cv2
import time
import threading
from datetime import datetime
from PIL import Image, ImageTk
import numpy as np


class WebcamHelper:
    """
    Klasse zur Steuerung einer Webcam über OpenCV
    Bietet Methoden zum Anzeigen des Kamera-Streams und Aufnehmen von Bildern
    """
    
    @staticmethod
    def detect_available_cameras(max_cameras=10):
        """
        Erkennt alle verfügbaren Kameras im System
        
        Args:
            max_cameras (int): Maximale Anzahl zu testender Kamera-Indizes
            
        Returns:
            list: Liste der verfügbaren Kamera-Indizes
        """
        available_cameras = []
        
        # OpenCV-Fehlermeldungen unterdrücken
        cv2.setLogLevel(0)  # 0 = silent
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Teste ob wir tatsächlich Frames lesen können
                ret, frame = cap.read()
                if ret and frame is not None:
                    available_cameras.append(i)
                cap.release()
          # OpenCV-Logging wieder auf Standard setzen
        cv2.setLogLevel(1)  # 1 = error level
        
        return available_cameras if available_cameras else [0]  # Fallback auf Index 0
    
    def __init__(self, device_index=0, frame_size=(320, 240), com_port=None, model=None):
        """
        Initialisiert die Webcam mit dem angegebenen Geräteindex und Framegröße
        
        Args:
            device_index (int): Index der zu verwendenden Kamera (Standard: 0)
            frame_size (tuple): Größe des angezeigten Frames (Breite, Höhe)
            com_port (str, optional): COM-Port der Kamera
            model (str, optional): Modellbezeichnung der Kamera
        """
        self.device_index = device_index
        self.frame_size = frame_size
        self.com_port = com_port or f"COM{device_index + 1}"  # Fallback
        self.model = model or f"Camera {device_index}"  # Fallback
        self.cap = None
        self.running = False
        self.current_frame = None
        self.thread = None
        self.bild_zaehler = 0
    
    def starten(self):
        """
        Kamera starten und initialisieren
        
        Returns:
            bool: True bei erfolgreicher Initialisierung, sonst False
        """
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            return False
        
        self.running = True
        return True
    
    def stoppen(self):
        """
        Kamera-Stream stoppen und Ressourcen freigeben
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        if self.cap:
            self.cap.release()
        
        self.cap = None
    
    def frame_lesen(self):
        """
        Einzelnes Frame von der Kamera lesen
        
        Returns:
            numpy.ndarray: Das gelesene Frame oder None bei Fehler
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
    
    def stream_loop(self, panel, fps=30):
        """
        Haupt-Loop für den Kamera-Stream
        Läuft in einem separaten Thread, um die GUI nicht zu blockieren
        
        Args:
            panel: Das Label-Widget zur Anzeige des Streams
            fps (int): Gewünschte Bildrate für den Stream        """
        delay = max(1, int(1000 / fps))
        
        while self.running:
            try:
                frame = self.frame_lesen()
                if frame is not None:
                    # Frame für die Anzeige quadratisch skalieren
                    self.current_frame = frame.copy()  # Original-Frame kopieren
                    frame_square = self._make_square_frame(frame, self.frame_size)
                    
                    # Von BGR zu RGB für tkinter konvertieren
                    frame_rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)
                    
                    # In Pillow-Format konvertieren
                    img = Image.fromarray(frame_rgb)
                    
                    # In Tkinter-kompatibles Format konvertieren
                    img_tk = ImageTk.PhotoImage(image=img)
                    
                    # GUI-Update über after() für Thread-Sicherheit
                    panel.after(0, self._update_panel, panel, img_tk)
                  # Kurz warten, um die gewünschte Framerate zu erreichen
                time.sleep(delay / 1000.0)
            except Exception as e:
                print(f"Fehler im Stream-Loop: {e}")
                break
    
    def _update_panel(self, panel, img_tk):
        """
        Thread-sichere GUI-Update-Methode
        Wird vom Haupt-Thread ausgeführt
        """
        try:
            # Prüfe mehrere Bedingungen bevor Update
            if (self.running and 
                hasattr(panel, 'winfo_exists') and 
                panel.winfo_exists() and
                hasattr(panel, 'config')):
                panel.config(image=img_tk)
                panel.image = img_tk  # Referenz behalten, um Garbage Collection zu verhindern
        except Exception as e:
            # Stream stoppen wenn Widget nicht mehr existiert oder ungültig ist
            error_msg = str(e).lower()
            if any(x in error_msg for x in ["invalid command name", "application has been destroyed", "bad window path"]):
                self.running = False  # Stream stoppen
            else:
                print(f"Unerwarteter GUI-Update-Fehler: {e}")
                self.running = False

    def stream_starten(self, panel):
        """
        Kamerastream in einem separaten Thread starten
        
        Args:
            panel: Das Label-Widget zur Anzeige des Streams
            
        Returns:
            bool: True bei erfolgreicher Initialisierung, sonst False
        """
        if self.starten():
            self.thread = threading.Thread(target=self.stream_loop, args=(panel,))
            self.thread.daemon = True  # Thread als Daemon setzen, damit er mit dem Hauptprogramm beendet wird
            self.thread.start()
            return True
        return False
    
    def shoot_pic(self, delay=0.2):
        """
        Nimmt das aktuelle Kamerabild auf und speichert es als PNG-Datei im Ordner 'pictures'.
        Führt nach der Aufnahme ein Delay aus.
        Gibt den Pfad zur gespeicherten Datei zurück.
        
        Args:
            delay (float): Pause nach der Aufnahme in Sekunden (Standard: 0.2)
        """
        # Kurzes Delay vor der Aufnahme, damit die Kamera ein neues Frame liefern kann
        time.sleep(delay)
        # Versuche, ein aktuelles Frame direkt von der Kamera zu lesen
        frame = self.frame_lesen()
        if frame is not None:
            pictures_dir = os.path.join(os.getcwd(), "pictures")
            os.makedirs(pictures_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"foto_{timestamp}.png"
            filepath = os.path.join(pictures_dir, filename)
            cv2.imwrite(filepath, frame)
            return filepath
        return None
    
    def _make_square_frame(self, frame, target_size):
        """
        Erstellt einen quadratischen Frame aus dem Input-Frame
        Behält das Seitenverhältnis bei und fügt schwarze Balken hinzu
        
        Args:
            frame: Input-Frame von der Kamera
            target_size: Tuple (width, height) für die Zielgröße
            
        Returns:
            Square frame mit schwarzen Balken falls nötig
        """
        height, width = frame.shape[:2]
        target_width, target_height = target_size
        
        # Bestimme die kleinere Dimension für quadratische Skalierung  
        min_target = min(target_width, target_height)
        
        # Berechne Skalierungsfaktor basierend auf der größeren Dimension des Originals
        scale_factor = min_target / max(width, height)
        
        # Neue Dimensionen berechnen
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Frame skalieren
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        # Quadratischen Hintergrund erstellen (schwarz)
        square_frame = np.zeros((min_target, min_target, 3), dtype=np.uint8)
          # Zentrierte Position berechnen
        start_x = (min_target - new_width) // 2
        start_y = (min_target - new_height) // 2
        
        # Resized frame in die Mitte des quadratischen Frames platzieren
        square_frame[start_y:start_y + new_height, start_x:start_x + new_width] = resized_frame
        
        return square_frame
    
    def stop_stream(self):
        """
        Stoppe den Kamerastream sicher
        """
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)  # Warte max 1 Sekunde
    
    def release(self):
        """
        Gib alle Kamera-Ressourcen frei
        """
        self.stop_stream()
        if self.cap:
            self.cap.release()
            self.cap = None
