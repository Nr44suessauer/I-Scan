import math
import pandas as pd
from tabulate import tabulate

# ===== KONFIGURATIONSVARIABLEN =====

# Punkt P (Start-Koordinaten)
P_X = 0                   # X-Koordinate des Startpunkts
P_Y = 0                   # Y-Koordinate des Startpunkts

# Punkt M (End-Koordinaten)
M_X = 0                   # X-Koordinate des Endpunkts
M_Y = 150                 # Y-Koordinate des Endpunkts

# Neues Zentrum (Ziel-Zentrum)
NEW_CENTER_X = 150        # X-Koordinate des neuen Zentrums
NEW_CENTER_Y = 75         # Y-Koordinate des neuen Zentrums

# Altes Zentrum (Ursprungs-Zentrum)
OLD_CENTER_X = 150        # X-Koordinate des alten Zentrums
OLD_CENTER_Y = 0          # Y-Koordinate des alten Zentrums

# Z-Modul Position (Startposition)
Z_MODULE_X = 0            # X-Koordinate des Z-Moduls (bleibt fest)
Z_MODULE_Y = 0            # Y-Koordinate des Z-Moduls (Startposition)

# Scan-Konfiguration
DELTA_SCAN = 100          # Gesamtstrecke des Scans in cm
NUMBER_OF_MEASUREMENTS = 10  # Anzahl der Messpunkte

    def set_point_p(self, x, y):
        """Setzt die Koordinaten von Punkt P"""
        self.pX = x
        self.pY = y

    def set_point_m(self, x, y):
        """Setzt die Koordinaten von Punkt M"""
        self.mX = x
        self.mY = y

    def set_new_center(self, x, y):
        """Setzt die Koordinaten des neuen Zentrums"""
        self.nX = x
        self.nY = y

    def set_old_center(self, x, y):
        """Setzt die Koordinaten des alten Zentrums"""
        self.oX = x
        self.oY = y

    def set_z_module(self, x, y):
        """Setzt die Koordinaten des Z-Moduls"""
        self.zX = x
        self.zY = y

    def set_scan_config(self, delta_scan, number_of_measurements):
        """Setzt die Scan-Konfiguration"""
        self.deltaScan = delta_scan
        self.numberOfMeasurements = number_of_measurements

    def calculate_angle(self, current_y):
        """
        Berechnet den Winkel basierend auf der aktuellen Y-Position
        """
        dx = self.nX - self.zX
        dy = self.nY - current_y
        
        # Winkel in Radiant berechnen
        alpha = math.atan2(dy, dx)
        
        # In Grad umwandeln
        alpha_degrees = alpha * 180 / math.pi
        
        # Winkelkorrektur anwenden
        angle = abs(90 - alpha_degrees)
        
        return angle

    def calculate_step_size(self):
        """Berechnet die Schrittgröße für die Messungen"""
        if self.numberOfMeasurements > 0:
            return self.deltaScan / self.numberOfMeasurements
        return 0

    def generate_results_table(self):
        """
        Generiert die Ergebnistabelle mit Winkeln und Z-Modul-Koordinaten
        """
        if self.numberOfMeasurements <= 0:
            print("Fehler: Anzahl der Messungen muss größer als 0 sein!")
            return None

        step_size = self.calculate_step_size()
        results = []

        print(f"\n=== Scan Calculator Ergebnisse ===")
        print(f"Delta Scan: {self.deltaScan}")
        print(f"Anzahl Messungen: {self.numberOfMeasurements}")
        print(f"Schrittgröße: {step_size:.2f} cm")
        print(f"Z-Modul X-Position (fest): {self.zX}")
        print(f"Startposition Y: {self.pY}")
        print(f"Neues Zentrum: ({self.nX}, {self.nY})")
        print("=" * 50)

        for i in range(self.numberOfMeasurements):
            # Aktuelle Y-Position berechnen
            current_y = self.pY + step_size * i
            
            # Winkel für diese Position berechnen
            angle = self.calculate_angle(current_y)
            
            # Z-Modul Koordinaten (X bleibt fest, Y variiert)
            z_coords = (self.zX, current_y)
            
            results.append({
                'Messung': i + 1,
                'Winkel (°)': round(angle, 1),
                'Z-Modul X': self.zX,
                'Z-Modul Y': round(current_y, 1),
                'Z-Modul Koordinaten': f"({self.zX}, {round(current_y, 1)})"
            })

        # Tabelle erstellen und anzeigen
        df = pd.DataFrame(results)
          # Kompakte Tabelle für die Ausgabe
        table_data = []
        for result in results:
            table_data.append([
                result['Winkel (°)'],
                result['Z-Modul Koordinaten']
            ])
        
        print(tabulate(table_data, 
                      headers=['Winkel (°)', 'Z-Modul (Koordinaten)'],
                      tablefmt='grid',
                      numalign='right'))
        
        return df

    def print_current_config(self):
        """Zeigt die aktuelle Konfiguration an"""
        print("\n=== Aktuelle Konfiguration ===")
        print(f"Punkt P: ({self.pX}, {self.pY})")
        print(f"Punkt M: ({self.mX}, {self.mY})")
        print(f"Neues Zentrum: ({self.nX}, {self.nY})")
        print(f"Altes Zentrum: ({self.oX}, {self.oY})")
        print(f"Z-Modul: ({self.zX}, {self.zY})")
        print(f"Delta Scan: {self.deltaScan}")
        print(f"Anzahl Messungen: {self.numberOfMeasurements}")
        
        # Aktuellen Winkel berechnen
        current_angle = self.calculate_angle(self.zY)
        print(f"Aktueller Winkel: {current_angle:.1f}°")


def main():
    """Hauptfunktion mit Beispielverwendung"""
    # Calculator initialisieren
    calc = ScanCalculator()
    
    # Beispielkonfiguration (entspricht den Standardwerten aus dem JavaScript)
    calc.set_point_p(0, 0)          # Punkt P
    calc.set_point_m(0, 150)        # Punkt M
    calc.set_new_center(150, 75)    # Neues Zentrum
    calc.set_old_center(150, 0)     # Altes Zentrum
    calc.set_z_module(0, 0)         # Z-Modul
    calc.set_scan_config(100, 10)   # Delta Scan = 100, 10 Messungen
    
    # Aktuelle Konfiguration anzeigen
    calc.print_current_config()
    
    # Ergebnistabelle generieren
    results_df = calc.generate_results_table()
    
    # Zusätzliche Beispiele
    print("\n" + "="*60)
    print("BEISPIEL 2: Andere Konfiguration")
    print("="*60)
    
    calc2 = ScanCalculator()
    calc2.set_point_p(10, 20)
    calc2.set_new_center(120, 90)
    calc2.set_z_module(5, 20)
    calc2.set_scan_config(50, 8)
    
    calc2.print_current_config()
    calc2.generate_results_table()


if __name__ == "__main__":
    # Erforderliche Bibliotheken prüfen
    try:
        import pandas as pd
        from tabulate import tabulate
    except ImportError as e:
        print("Fehlende Bibliothek! Bitte installieren Sie:")
        print("pip install pandas tabulate")
        print(f"Fehler: {e}")
        exit(1)
    
    main()