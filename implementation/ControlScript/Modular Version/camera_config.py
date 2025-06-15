import csv
import os
from typing import List, Dict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CameraConfig:
    """
    Klasse zur Verwaltung der Kamera-Konfiguration
    Ermöglicht das Hinzufügen, Bearbeiten und Entfernen von Kameras
    """
    
    def __init__(self):
        self.cameras = []  # Liste der Kamera-Konfigurationen
        self.next_index = 0
        self.config_file = "CamConfig.csv"
    def add_camera(self, comport: str, device_index: int, bezeichnung: str, beschreibung: str = "", indexnummer: int = None) -> int:
        """
        Fügt eine neue Kamera zur Konfiguration hinzu
        
        Args:
            comport (str): COM-Port der Kamera
            device_index (int): Physischer Geräte-Index der Kamera
            bezeichnung (str): Bezeichnung der Kamera
            beschreibung (str): Beschreibung der Kamera
            indexnummer (int, optional): Spezifische Indexnummer, falls None wird automatisch vergeben
            
        Returns:
            int: Index der hinzugefügten Kamera
        """
        if indexnummer is None:
            indexnummer = self.next_index
            self.next_index += 1
        else:
            # Stelle sicher, dass next_index größer ist als die manuelle Indexnummer
            self.next_index = max(self.next_index, indexnummer + 1)
            
        camera = {
            'indexnummer': indexnummer,
            'comport': comport,
            'device_index': device_index,
            'bezeichnung': bezeichnung,
            'beschreibung': beschreibung
        }
        self.cameras.append(camera)
        return camera['indexnummer']
    
    def remove_camera(self, indexnummer: int) -> bool:
        """
        Entfernt eine Kamera aus der Konfiguration
        
        Args:
            indexnummer (int): Indexnummer der zu entfernenden Kamera
            
        Returns:
            bool: True wenn erfolgreich entfernt, False wenn nicht gefunden
        """
        for i, camera in enumerate(self.cameras):
            if camera['indexnummer'] == indexnummer:
                self.cameras.pop(i)
                return True
        return False
    def update_camera(self, indexnummer: int, comport: str = None, device_index: int = None, bezeichnung: str = None, beschreibung: str = None) -> bool:
        """
        Aktualisiert eine Kamera-Konfiguration
        
        Args:
            indexnummer (int): Indexnummer der zu aktualisierenden Kamera
            comport (str, optional): Neuer COM-Port
            device_index (int, optional): Neuer Geräte-Index
            bezeichnung (str, optional): Neue Bezeichnung
            beschreibung (str, optional): Neue Beschreibung
            
        Returns:
            bool: True wenn erfolgreich aktualisiert
        """
        for camera in self.cameras:
            if camera['indexnummer'] == indexnummer:
                if comport is not None:
                    camera['comport'] = comport
                if device_index is not None:
                    camera['device_index'] = device_index
                if bezeichnung is not None:
                    camera['bezeichnung'] = bezeichnung
                if beschreibung is not None:
                    camera['beschreibung'] = beschreibung
                return True
        return False
    
    def get_all_cameras(self) -> List[Dict]:
        """
        Gibt alle Kamera-Konfigurationen zurück
        
        Returns:
            List[Dict]: Liste aller Kamera-Konfigurationen
        """
        return self.cameras.copy()
    
    def get_camera_by_index(self, indexnummer: int) -> Dict:
        """
        Gibt eine Kamera-Konfiguration nach Indexnummer zurück
        
        Args:
            indexnummer (int): Indexnummer der gesuchten Kamera
            
        Returns:
            Dict: Kamera-Konfiguration oder None wenn nicht gefunden
        """
        for camera in self.cameras:
            if camera['indexnummer'] == indexnummer:
                return camera.copy()
        return None
    
    def get_camera_by_comport(self, comport: str) -> Dict:
        """
        Gibt eine Kamera-Konfiguration nach COM-Port zurück
        
        Args:
            comport (str): COM-Port der gesuchten Kamera
            
        Returns:
            Dict: Kamera-Konfiguration oder None wenn nicht gefunden
        """
        for camera in self.cameras:
            if camera['comport'] == comport:
                return camera.copy()
        return None
    
    def save_to_csv(self, filename: str = None, callback=None) -> bool:
        """
        Speichert die Kamera-Konfiguration in eine CSV-Datei
        
        Args:
            filename (str, optional): Dateiname. Standard: CamConfig.csv
            callback (callable, optional): Callback-Funktion die nach dem Speichern aufgerufen wird
            
        Returns:
            bool: True wenn erfolgreich gespeichert
        """
        if filename is None:
            filename = self.config_file
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['indexnummer', 'comport', 'device_index', 'bezeichnung', 'beschreibung']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
                
                writer.writeheader()
                for camera in self.cameras:
                    writer.writerow({
                        'indexnummer': camera['indexnummer'],
                        'comport': camera['comport'],
                        'device_index': camera['device_index'],
                        'bezeichnung': camera['bezeichnung'],
                        'beschreibung': camera['beschreibung']
                    })
            
            # Callback aufrufen nach erfolgreichem Speichern
            if callback and callable(callback):
                callback()
                
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der CSV-Datei: {e}")
            return False
    
    def load_from_csv(self, filename: str = None) -> bool:
        """
        Lädt die Kamera-Konfiguration aus einer CSV-Datei
        
        Args:
            filename (str, optional): Dateiname. Standard: CamConfig.csv
            
        Returns:
            bool: True wenn erfolgreich geladen
        """
        if filename is None:
            filename = self.config_file
            
        if not os.path.exists(filename):
            return False
            
        try:
            self.cameras = []
            max_index = -1
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='|')
                for row in reader:                    # Prüfe ob alle erforderlichen Spalten vorhanden sind
                    required_fields = ['indexnummer', 'comport', 'device_index', 'bezeichnung', 'beschreibung']
                    if not all(field in row for field in required_fields):
                        print(f"CSV-Datei hat nicht das erwartete Format. Gefundene Spalten: {list(row.keys())}")
                        return False
                    
                    indexnummer = int(row['indexnummer'])
                    camera = {
                        'indexnummer': indexnummer,
                        'comport': row['comport'],
                        'device_index': int(row['device_index']),
                        'bezeichnung': row['bezeichnung'],
                        'beschreibung': row['beschreibung']
                    }
                    self.cameras.append(camera)
                    max_index = max(max_index, indexnummer)
                    
            # Sortiere Kameras nach Indexnummer
            self.cameras.sort(key=lambda x: x['indexnummer'])
            self.next_index = max_index + 1
            return True
        except Exception as e:
            print(f"Fehler beim Laden der CSV-Datei: {e}")
            return False


class CameraConfigDialog:
    """
    Dialog zur Bearbeitung der Kamera-Konfiguration
    """
    
    def __init__(self, parent, camera_config: CameraConfig, logger=None, refresh_callback=None):
        self.parent = parent
        self.camera_config = camera_config
        self.logger = logger
        self.refresh_callback = refresh_callback
        self.dialog = None
        self.tree = None
        
    def open_dialog(self):
        """Öffnet den Kamera-Konfiguration-Dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Kamera-Konfiguration")
        self.dialog.geometry("800x500")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Hauptframe
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview für Kamera-Liste
        self.create_treeview(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
        
        # Lade aktuelle Konfiguration
        self.refresh_tree()
        
        # Zentriere Dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_treeview(self, parent):
        """Erstellt die Treeview für die Kamera-Liste"""
        # Frame für Treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
          # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                columns=('indexnummer', 'comport', 'device_index', 'bezeichnung', 'beschreibung'),
                                show='headings',
                                yscrollcommand=v_scrollbar.set,
                                xscrollcommand=h_scrollbar.set)
        
        # Spalten konfigurieren
        self.tree.heading('indexnummer', text='Index')
        self.tree.heading('comport', text='COM-Port')
        self.tree.heading('device_index', text='Device')
        self.tree.heading('bezeichnung', text='Bezeichnung')
        self.tree.heading('beschreibung', text='Beschreibung')
        
        self.tree.column('indexnummer', width=60, anchor=tk.CENTER)
        self.tree.column('comport', width=80, anchor=tk.CENTER)
        self.tree.column('device_index', width=60, anchor=tk.CENTER)
        self.tree.column('bezeichnung', width=150, anchor=tk.W)
        self.tree.column('beschreibung', width=250, anchor=tk.W)
        
        # Scrollbars konfigurieren
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def create_buttons(self, parent):
        """Erstellt die Button-Leiste"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        ttk.Button(button_frame, text="Hinzufügen", command=self.add_camera).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Bearbeiten", command=self.edit_camera).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Entfernen", command=self.remove_camera).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(button_frame, text="CSV Importieren", command=self.import_csv).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="CSV Exportieren", command=self.export_csv).pack(side=tk.LEFT, padx=(0, 5))
        
        # Schließen Button rechts
        ttk.Button(button_frame, text="Schließen", command=self.close_dialog).pack(side=tk.RIGHT)
        
    def refresh_tree(self):
        """Aktualisiert die Treeview mit aktuellen Kamera-Daten"""
        # Lösche alle Einträge
        for item in self.tree.get_children():
            self.tree.delete(item)
              # Füge Kamera-Daten hinzu
        for camera in self.camera_config.get_all_cameras():
            self.tree.insert('', tk.END, values=(
                camera['indexnummer'],
                camera['comport'],
                camera['device_index'],
                camera['bezeichnung'],
                camera['beschreibung']
            ))
    
    def add_camera(self):
        """Öffnet Dialog zum Hinzufügen einer neuen Kamera"""
        self.open_camera_edit_dialog()
        
    def edit_camera(self):
        """Öffnet Dialog zum Bearbeiten der ausgewählten Kamera"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Kamera zum Bearbeiten aus.")
            return
            
        item = self.tree.item(selection[0])
        indexnummer = int(item['values'][0])
        camera = self.camera_config.get_camera_by_index(indexnummer)
        
        if camera:
            self.open_camera_edit_dialog(camera)
    
    def remove_camera(self):
        """Entfernt die ausgewählte Kamera"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Kamera zum Entfernen aus.")
            return
            
        item = self.tree.item(selection[0])
        indexnummer = int(item['values'][0])
        bezeichnung = item['values'][2]
        
        if messagebox.askyesno("Kamera entfernen", f"Möchten Sie die Kamera '{bezeichnung}' wirklich entfernen?"):
            if self.camera_config.remove_camera(indexnummer):
                self.refresh_tree()
                # Speichere Änderungen automatisch in CSV mit Callback
                if self.camera_config.save_to_csv(callback=self.refresh_callback):
                    if self.logger:
                        self.logger.log(f"Kamera '{bezeichnung}' entfernt und Konfiguration gespeichert")
                else:
                    if self.logger:
                        self.logger.log(f"Kamera '{bezeichnung}' entfernt, aber Fehler beim Speichern der Konfiguration")
    
    def open_camera_edit_dialog(self, camera=None):
        """Öffnet Dialog zum Hinzufügen/Bearbeiten einer Kamera"""
        edit_dialog = tk.Toplevel(self.dialog)
        edit_dialog.title("Kamera bearbeiten" if camera else "Kamera hinzufügen")
        edit_dialog.geometry("400x300")
        edit_dialog.transient(self.dialog)
        edit_dialog.grab_set()
          # Eingabefelder
        ttk.Label(edit_dialog, text="Indexnummer:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        index_var = tk.StringVar(value=str(camera['indexnummer']) if camera else "")
        index_entry = ttk.Entry(edit_dialog, textvariable=index_var)
        index_entry.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(edit_dialog, text="COM-Port:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        comport_var = tk.StringVar(value=camera['comport'] if camera else "")
        comport_entry = ttk.Entry(edit_dialog, textvariable=comport_var)
        comport_entry.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(edit_dialog, text="Device Index:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        device_index_var = tk.StringVar(value=str(camera['device_index']) if camera else "")
        device_index_entry = ttk.Entry(edit_dialog, textvariable=device_index_var)
        device_index_entry.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(edit_dialog, text="Bezeichnung:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        bezeichnung_var = tk.StringVar(value=camera['bezeichnung'] if camera else "")
        bezeichnung_entry = ttk.Entry(edit_dialog, textvariable=bezeichnung_var)
        bezeichnung_entry.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(edit_dialog, text="Beschreibung:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        beschreibung_var = tk.StringVar(value=camera['beschreibung'] if camera else "")
        beschreibung_text = tk.Text(edit_dialog, height=4, width=30)
        beschreibung_text.grid(row=4, column=1, sticky=tk.EW, padx=10, pady=5)
        if camera:
            beschreibung_text.insert(tk.END, camera['beschreibung'])
          # Buttons
        button_frame = ttk.Frame(edit_dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        def save_camera():
            try:
                indexnummer = int(index_var.get()) if index_var.get() else None
                comport = comport_var.get().strip()
                device_index = int(device_index_var.get()) if device_index_var.get() else 0
                bezeichnung = bezeichnung_var.get().strip()
                beschreibung = beschreibung_text.get(1.0, tk.END).strip()
                
                if not comport or not bezeichnung:
                    messagebox.showerror("Fehler", "COM-Port und Bezeichnung sind erforderlich.")
                    return
                
                if camera:
                    # Bearbeiten
                    if indexnummer != camera['indexnummer']:
                        # Index geändert - entfernen und neu hinzufügen
                        self.camera_config.remove_camera(camera['indexnummer'])
                        self.camera_config.add_camera(comport, device_index, bezeichnung, beschreibung, indexnummer)
                    else:
                        # Nur andere Felder aktualisieren
                        self.camera_config.update_camera(indexnummer, comport, device_index, bezeichnung, beschreibung)
                else:
                    # Hinzufügen
                    self.camera_config.add_camera(comport, device_index, bezeichnung, beschreibung, indexnummer)
                
                self.refresh_tree()
                edit_dialog.destroy()
                
                # Speichere Änderungen automatisch in CSV mit Callback
                if self.camera_config.save_to_csv(callback=self.refresh_callback):
                    if self.logger:
                        action = "bearbeitet" if camera else "hinzugefügt"
                        self.logger.log(f"Kamera '{bezeichnung}' {action} und Konfiguration gespeichert")
                else:
                    if self.logger:
                        self.logger.log(f"Fehler beim Speichern der Kamera-Konfiguration")
                        
            except ValueError:
                messagebox.showerror("Fehler", "Indexnummer und Device Index müssen Zahlen sein.")
        
        ttk.Button(button_frame, text="Speichern", command=save_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=edit_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Spalte 1 dehnen
        edit_dialog.grid_columnconfigure(1, weight=1)
        
        # Zentriere Dialog
        edit_dialog.update_idletasks()
        x = (edit_dialog.winfo_screenwidth() // 2) - (edit_dialog.winfo_width() // 2)
        y = (edit_dialog.winfo_screenheight() // 2) - (edit_dialog.winfo_height() // 2)
        edit_dialog.geometry(f"+{x}+{y}")
    
    def import_csv(self):
        """Importiert Kamera-Konfiguration aus CSV-Datei"""
        filename = filedialog.askopenfilename(
            title="CSV-Datei importieren",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            if self.camera_config.load_from_csv(filename):
                self.refresh_tree()
                messagebox.showinfo("Import erfolgreich", f"Kamera-Konfiguration aus '{filename}' geladen.")
                if self.logger:
                    self.logger.log(f"Kamera-Konfiguration aus '{filename}' importiert")
            else:
                messagebox.showerror("Import fehlgeschlagen", "Fehler beim Laden der CSV-Datei.")
    
    def export_csv(self):
        """Exportiert Kamera-Konfiguration in CSV-Datei"""
        filename = filedialog.asksaveasfilename(
            title="CSV-Datei exportieren",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            if self.camera_config.save_to_csv(filename):
                messagebox.showinfo("Export erfolgreich", f"Kamera-Konfiguration nach '{filename}' gespeichert.")
                if self.logger:
                    self.logger.log(f"Kamera-Konfiguration nach '{filename}' exportiert")
            else:
                messagebox.showerror("Export fehlgeschlagen", "Fehler beim Speichern der CSV-Datei.")
    
    def close_dialog(self):
        """Schließt den Dialog"""
        self.dialog.destroy()
