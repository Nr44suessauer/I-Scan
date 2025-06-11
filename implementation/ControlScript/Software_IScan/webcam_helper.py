"""
WEBCAM HELPER MODULE
====================
Provides functions for controlling and displaying a webcam stream.

Author: Marc Nauendorf
Email: marc.nauendorf@hs-heilbronn.de
Website: deadlinedriven.dev
Version: 1.0
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
    
    def __init__(self, device_index=0, frame_size=(320, 240)):
        """
        Initialisiert die Webcam mit dem angegebenen Geräteindex und Framegröße
        
        Args:
            device_index (int): Index der zu verwendenden Kamera (Standard: 0)
            frame_size (tuple): Größe des angezeigten Frames (Breite, Höhe)
        """
        self.device_index = device_index
        self.frame_size = frame_size
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
        
        Args:
            panel: Das Label-Widget zur Anzeige des Streams
            fps (int): Gewünschte Bildrate für den Stream
        """
        delay = max(1, int(1000 / fps))
        
        while self.running:
            frame = self.frame_lesen()
            if frame is not None:
                # Frame für die Anzeige skalieren
                self.current_frame = frame.copy()  # Original-Frame kopieren
                frame_resized = cv2.resize(frame, self.frame_size)
                
                # Von BGR zu RGB für tkinter konvertieren
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                
                # In Pillow-Format konvertieren
                img = Image.fromarray(frame_rgb)
                
                # In Tkinter-kompatibles Format konvertieren
                img_tk = ImageTk.PhotoImage(image=img)
                
                # Im Panel anzeigen
                panel.config(image=img_tk)
                panel.image = img_tk  # Referenz behalten, um Garbage Collection zu verhindern
            
            # Kurz warten, um die gewünschte Framerate zu erreichen
            time.sleep(delay / 1000.0)
    
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
    
    def foto_aufnehmen(self, delay=0.2):
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
