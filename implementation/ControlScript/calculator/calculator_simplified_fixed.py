import math
import csv
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

# ===== KONFIGURATIONSVARIABLEN =====

# Punkt P (Start-Koordinaten)
P_X = 0                   # X-Koordinate des Startpunkts
P_Y = 0                   # Y-Koordinate des Startpunkts

# Punkt M (End-Koordinaten)
M_X = 0                   # X-Koordinate des Endpunkts
M_Y = 150                 # Y-Koordinate des Endpunkts

# Neues Zentrum (Ziel-Zentrum)
NEW_CENTER_X = 150        # X-Koordinate des neuen Zentrums
NEW_CENTER_Y = 25         # Y-Koordinate des neuen Zentrums

# Altes Zentrum (Ursprungs-Zentrum)
OLD_CENTER_X = 150        # X-Koordinate des alten Zentrums
OLD_CENTER_Y = 0          # Y-Koordinate des alten Zentrums

# Z-Modul Position (Startposition)
Z_MODULE_X = 0            # X-Koordinate des Z-Moduls (bleibt fest)
Z_MODULE_Y = 0            # Y-Koordinate des Z-Moduls (Startposition)

# Scan-Konfiguration
DELTA_SCAN = 100          # Gesamtstrecke des Scans in cm
NUMBER_OF_MEASUREMENTS = 10  # Anzahl der Messpunkte

def calculate_angle(current_y):
    """
    Berechnet den Winkel basierend auf der aktuellen Y-Position
    """
    # Abstand zwischen neuem Zentrum und Z-Modul in X-Richtung
    dx = NEW_CENTER_X - Z_MODULE_X
    # Abstand zwischen neuem Zentrum und aktueller Y-Position
    dy = NEW_CENTER_Y - current_y
    
    # Winkel in Radiant berechnen
    alpha = math.atan2(dy, dx)
    
    # In Grad umwandeln
    alpha_degrees = alpha * 180 / math.pi
    
    # Winkelkorrektur anwenden: 90° - berechneter Winkel (als absoluter Wert)
    angle = abs(90 - alpha_degrees)
    
    return angle

def calculate_approximated_angle(current_y):
    """
    Berechnet den approximierten Winkel basierend auf der aktuellen Y-Position
    mit Begrenzung auf den Bereich 0-90 Grad
    """
    # Ursprünglichen Winkel berechnen
    raw_angle = calculate_angle(current_y)
    
    # Auf den Bereich 0-90 Grad begrenzen
    if raw_angle < 0:
        approximated_angle = 0
    elif raw_angle > 90:
        approximated_angle = 90
    else:
        approximated_angle = raw_angle
    
    return approximated_angle

def calculate_step_size():
    """Berechnet die Schrittgröße für die Messungen"""
    if NUMBER_OF_MEASUREMENTS > 0:
        return DELTA_SCAN / NUMBER_OF_MEASUREMENTS
    return 0

def generate_results_table():
    """
    Generiert die Ergebnistabelle mit ursprünglichen und approximierten Winkeln
    """
    if NUMBER_OF_MEASUREMENTS <= 0:
        print("Fehler: Anzahl der Messungen muss größer als 0 sein!")
        return None

    step_size = calculate_step_size()
    
    # Konfigurations-Informationen anzeigen
    print("\n=== Scan Calculator Konfiguration ===")
    print(f"Start Koordinaten (P): ({P_X}, {P_Y})")
    print(f"End Koordinaten (M): ({M_X}, {M_Y})")
    print(f"Neues Zentrum: ({NEW_CENTER_X}, {NEW_CENTER_Y})")
    print(f"Altes Zentrum: ({OLD_CENTER_X}, {OLD_CENTER_Y})")
    print(f"Z-Modul Start: ({Z_MODULE_X}, {Z_MODULE_Y})")
    print(f"Delta Scan: {DELTA_SCAN}")
    print(f"Anzahl Messungen: {NUMBER_OF_MEASUREMENTS}")
    print(f"Schrittgröße: {step_size:.2f} cm")
    print("=" * 50)

    # Messungen berechnen und erfassen
    table_data = []
    csv_data = []  # Separate Daten für CSV-Export
    
    for i in range(NUMBER_OF_MEASUREMENTS):
        # Aktuelle Y-Position berechnen
        current_y = P_Y + step_size * i
        
        # Ursprünglichen und approximierten Winkel für diese Position berechnen
        original_angle = calculate_angle(current_y)
        approximated_angle = calculate_approximated_angle(current_y)
        
        # Z-Modul Koordinaten formatieren (X bleibt fest, Y variiert)
        z_coords = f"({Z_MODULE_X}, {round(current_y, 1)})"
        
        # Daten für die Tabelle hinzufügen (mit beiden Winkelwerten)
        table_data.append([
            i + 1,                              # Messungsnummer
            round(original_angle, 1),           # Ursprünglicher Winkel
            round(approximated_angle, 1),       # Approximierter Winkel (0-90°)
            z_coords                            # Z-Modul Koordinaten
        ])
        
        # Daten für CSV (mit approximierten Winkeln)
        csv_data.append([
            i + 1,
            round(current_y, 1),
            round(approximated_angle, 1),
            Z_MODULE_X,
            round(current_y, 1)
        ])
    
    # Tabelle ausgeben
    print(tabulate(table_data, 
                  headers=['Messung Nr.', 'Original Winkel (°)', 'Approx. Winkel (°)', 'Z-Modul (Koordinaten)'],
                  tablefmt='grid',
                  numalign='right'))
    
    # CSV-Datei erstellen
    csv_filename = f'winkeltabelle_{NEW_CENTER_X}x{NEW_CENTER_Y}_{NUMBER_OF_MEASUREMENTS}punkte_approximiert.csv'
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Messung_Nr', 'Y_Position_cm', 'Approximierter_Winkel_Grad', 'X_Koordinate', 'Y_Koordinate'])
            writer.writerows(csv_data)
        print(f"\nCSV-Datei mit approximierten Winkeln erstellt: {csv_filename}")
    except Exception as e:
        print(f"Fehler beim Erstellen der CSV-Datei: {e}")
    
    # Daten für die Grafiken extrahieren
    measurements = [row[0] for row in table_data]  # Messungsnummern
    original_angles = [row[1] for row in table_data]        # Ursprüngliche Winkel
    approximated_angles = [row[2] for row in table_data]    # Approximierte Winkel
    y_positions = [P_Y + step_size * i for i in range(NUMBER_OF_MEASUREMENTS)]  # Y-Positionen
    
    # Mehrere Grafiken erstellen
    plt.figure(figsize=(20, 16))
    
    # Subplot 1: Tabelle mit Werten
    plt.subplot(2, 3, 1)
    plt.axis('off')  # Achsen ausblenden
    
    # Tabellendaten für die grafische Darstellung vorbereiten
    table_headers = ['Nr.', 'Original (°)', 'Approx. (°)', 'Y-Pos (cm)', 'Koordinaten']
    table_rows = []
    for i, (orig_angle, approx_angle, y) in enumerate(zip(original_angles, approximated_angles, y_positions)):
        table_rows.append([i+1, f"{orig_angle:.1f}°", f"{approx_angle:.1f}°", f"{y:.1f}", f"({Z_MODULE_X}, {y:.1f})"])
    
    # Tabelle in das Diagramm einfügen
    plt.table(cellText=table_rows,
             colLabels=table_headers,
             cellLoc='center',
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('Messwerte Tabelle (Original vs. Approximiert)', fontsize=14)
    
    # Subplot 2: Winkel vs. Messung - Vergleich Original vs. Approximiert
    plt.subplot(2, 3, 2)
    plt.plot(measurements, original_angles, 'o-', color='blue', linewidth=2, markersize=8, label='Original Winkel')
    plt.plot(measurements, approximated_angles, 's-', color='red', linewidth=2, markersize=8, label='Approximierter Winkel (0-90°)')
    plt.title('Winkel pro Messung - Vergleich', fontsize=14)
    plt.xlabel('Messung Nr.', fontsize=12)
    plt.ylabel('Winkel (°)', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.ylim(-5, 95)  # Y-Achse erweitern für bessere Sicht
    
    # Subplot 3: Winkel vs. Y-Position - Vergleich Original vs. Approximiert
    plt.subplot(2, 3, 3)
    plt.plot(y_positions, original_angles, 'o-', color='blue', linewidth=2, markersize=8, label='Original Winkel')
    plt.plot(y_positions, approximated_angles, 's-', color='red', linewidth=2, markersize=8, label='Approximierter Winkel (0-90°)')
    plt.title('Winkel vs. Y-Position - Vergleich', fontsize=14)
    plt.xlabel('Y-Position (cm)', fontsize=12)
    plt.ylabel('Winkel (°)', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.ylim(-5, 95)  # Y-Achse erweitern für bessere Sicht
    
    # Subplot 4: Visuelle Darstellung des Scan-Pfades und Winkels (2D)
    plt.subplot(2, 3, 4)
    
    # Z-Modul-Positionen darstellen
    for i, y in enumerate(y_positions):
        plt.plot(Z_MODULE_X, y, 'o', color='blue', markersize=8)
    
    # Scanpfad darstellen
    plt.plot([Z_MODULE_X] * len(y_positions), y_positions, '-', color='blue', linewidth=2, label='Scan-Pfad')
    
    # Neues Zentrum darstellen
    plt.plot(NEW_CENTER_X, NEW_CENTER_Y, 'ro', markersize=10, label='Neues Zentrum')
    
    # Winkellinien und Winkeltext für alle Messungen (mit approximierten Winkeln)
    for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
        color_intensity = 0.3 + (i / len(y_positions)) * 0.7  # Farbverlauf
        # Linie vom Z-Modul zum neuen Zentrum zeichnen
        plt.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], '--', 
                color=(0, color_intensity, 0), linewidth=1.5, 
                alpha=0.7)
        
        # Approximierten Winkel als Text anzeigen
        text_x = (Z_MODULE_X + NEW_CENTER_X) / 2 - 15
        text_y = (y + NEW_CENTER_Y) / 2 + 5
        
        # Winkelwert anzeigen (approximiert)
        plt.text(text_x, text_y, f"{approx_angle:.1f}°", 
                color='red', fontsize=9, fontweight='bold',
                bbox=dict(facecolor='yellow', alpha=0.7, boxstyle='round,pad=0.3'))
    
    plt.title('2D-Darstellung mit approximierten Winkeln', fontsize=14)
    plt.xlabel('X-Position (cm)', fontsize=12)
    plt.ylabel('Y-Position (cm)', fontsize=12)
    plt.grid(True)
    plt.legend(loc='best')
    
    # Achsenlänge anpassen
    max_x = max(NEW_CENTER_X, Z_MODULE_X) * 1.2
    max_y = max(NEW_CENTER_Y, max(y_positions)) * 1.2
    min_x = min(0, Z_MODULE_X) - 10
    min_y = min(0, min(y_positions)) - 10
    plt.axis([min_x, max_x, min_y, max_y])
    
    # Subplot 5: Differenz zwischen Original und Approximiert
    plt.subplot(2, 3, 5)
    differences = [orig - approx for orig, approx in zip(original_angles, approximated_angles)]
    plt.plot(measurements, differences, 'o-', color='purple', linewidth=2, markersize=8)
    plt.title('Differenz: Original - Approximiert', fontsize=14)
    plt.xlabel('Messung Nr.', fontsize=12)
    plt.ylabel('Winkeldifferenz (°)', fontsize=12)
    plt.grid(True)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Subplot 6: Konfigurations-Informationen
    plt.subplot(2, 3, 6)
    plt.axis('off')  # Achsen ausblenden
    
    # Text-Informationen zur Konfiguration
    config_info = [
        f"Konfiguration:",
        f"",
        f"Neues Zentrum: ({NEW_CENTER_X}, {NEW_CENTER_Y})",
        f"Altes Zentrum: ({OLD_CENTER_X}, {OLD_CENTER_Y})",
        f"Z-Modul Start: ({Z_MODULE_X}, {Z_MODULE_Y})",
        f"Delta Scan: {DELTA_SCAN} cm",
        f"Anzahl Messungen: {NUMBER_OF_MEASUREMENTS}",
        f"Schrittgröße: {calculate_step_size():.1f} cm",
        f"",
        f"Original Winkelbereich: {min(original_angles):.1f}° - {max(original_angles):.1f}°",
        f"Approximiert Winkelbereich: {min(approximated_angles):.1f}° - {max(approximated_angles):.1f}°",
        f"",
        f"CSV-Datei: {csv_filename}"
    ]
    
    plt.text(0.5, 0.5, "\n".join(config_info),
            ha='center', va='center', fontsize=10,
            bbox=dict(facecolor='lightgray', alpha=0.5, boxstyle='round,pad=1'))
    plt.title('Konfigurations-Informationen', fontsize=14)
    
    plt.tight_layout()
    
    # Grafiken speichern
    visualization_path = 'scan_visualization_approximated.png'
    plt.savefig(visualization_path, dpi=300, bbox_inches='tight')
    print(f"\nGrafische Darstellung wurde gespeichert unter: {visualization_path}")
    
    # Versuche Grafik anzuzeigen, wenn möglich
    try:
        plt.show()
    except Exception as e:
        print(f"Hinweis: Die Grafik konnte nicht angezeigt werden ({e}), wurde aber unter '{visualization_path}' gespeichert.")

def main():
    """Hauptfunktion zur Ausführung des Programms"""
    # Ergebnistabelle generieren und anzeigen
    generate_results_table()

if __name__ == "__main__":
    # Erforderliche Bibliotheken prüfen
    try:
        import pandas as pd
        from tabulate import tabulate
    except ImportError as e:
        print("Fehlende Bibliothek! Bitte installieren Sie:")
        print("pip install pandas tabulate matplotlib")
        print(f"Fehler: {e}")
        exit(1)
    
    main()
