import math
import csv
import json
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

# ===== KONFIGURATIONSVARIABLEN =====

# Servo-Winkelgrenzen (Servomotor Begrenzungen)
SERVO_ANGLE_MIN = 0       # Untere Grenze des Servowinkels in Grad
SERVO_ANGLE_MAX = 90      # Obere Grenze des Servowinkels in Grad

# Winkelkorrektur-Referenz (geometrische Berechnung)
ANGLE_CORRECTION_REFERENCE = 90  # Referenzwinkel für die Korrekturberechnung in Grad

# Punkt P (Start-Koordinaten)
P_X = 0                   # X-Koordinate des Startpunkts
P_Y = 0                   # Y-Koordinate des Startpunkts

# Punkt M (End-Koordinaten)
M_X = 0                   # X-Koordinate des Endpunkts
M_Y = 50                 # Y-Koordinate des Endpunkts

# Neues Zentrum (Ziel-Zentrum)
NEW_CENTER_X = 40       # X-Koordinate des neuen Zentrums
NEW_CENTER_Y = 0        # Y-Koordinate des neuen Zentrums

# Altes Zentrum (Ursprungs-Zentrum)
OLD_CENTER_X = 40        # X-Koordinate des alten Zentrums
OLD_CENTER_Y = 0          # Y-Koordinate des alten Zentrums

# Z-Modul Position (Startposition)
Z_MODULE_X = 0            # X-Koordinate des Z-Moduls (bleibt fest)
Z_MODULE_Y = 0            # Y-Koordinate des Z-Moduls (Startposition)

# Scan-Konfiguration
DELTA_SCAN = 50          # Gesamtstrecke des Scans in cm
NUMBER_OF_MEASUREMENTS = 6  # Anzahl der Messpunkte

def calculate_angle(current_y):
    """
    Berechnet den Winkel basierend auf der aktuellen Y-Position
    Geometrie: Bei Y=0 ist der Winkel 90°, bei steigender Y-Position nähert sich der Winkel 0°
    """
    # Abstand zwischen neuem Zentrum und Z-Modul in X-Richtung
    dx = NEW_CENTER_X - Z_MODULE_X
    # Abstand zwischen aktueller Y-Position und neuem Zentrum
    dy = abs(current_y - NEW_CENTER_Y)
    
    # Winkel in Radiant berechnen
    if abs(dx) < 0.001:
        # Vermeide Division durch 0 - wenn dx = 0, ist es ein vertikaler Winkel
        angle = 90.0 if dy == 0 else 0.0
    else:
        # Berechne den Winkel zur X-Achse
        alpha_rad = math.atan(dy / abs(dx))
        # Konvertiere zu Grad
        alpha_deg = alpha_rad * 180 / math.pi
        # Der Komplementärwinkel gibt uns die gewünschte Orientierung:
        # Bei Y=0 (dy=0) -> alpha_deg=0° -> angle = 90° - 0° = 90°
        # Bei großem Y (dy groß) -> alpha_deg nähert sich 90° -> angle nähert sich 0°
        angle = 90.0 - alpha_deg
    
    return angle

def calculate_approximated_angle(current_y):
    """
    Berechnet den approximierten Winkel basierend auf der aktuellen Y-Position
    mit Begrenzung auf den konfigurierbaren Servo-Winkelbereich
    """
    # Ursprünglichen Winkel berechnen
    raw_angle = calculate_angle(current_y)
    
    # Auf den konfigurierbaren Servo-Winkelbereich begrenzen
    if raw_angle < SERVO_ANGLE_MIN:
        approximated_angle = SERVO_ANGLE_MIN
    elif raw_angle > SERVO_ANGLE_MAX:
        approximated_angle = SERVO_ANGLE_MAX
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
    print(f"Servo-Winkelbereich: {SERVO_ANGLE_MIN}° - {SERVO_ANGLE_MAX}°")
    print("=" * 50)    # Messungen berechnen und erfassen
    table_data = []
    
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
    
    # Tabelle ausgeben
    print(tabulate(table_data, 
                  headers=['Messung Nr.', 'Original Winkel (°)', 'Approx. Winkel (°)', 'Z-Modul (Koordinaten)'],
                  tablefmt='grid',
                  numalign='right'))    # CSV-Datei für main.py-Import erstellen (mit JSON-Format für params)
    csv_filename = f'winkeltabelle_{NEW_CENTER_X}x{NEW_CENTER_Y}_{NUMBER_OF_MEASUREMENTS}punkte_approximiert.csv'
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Header im main.py-Format
            writer.writerow(['type', 'params', 'description'])
            
            # Home-Position anfahren (optional)
            writer.writerow([
                'home',
                '{}',
                'Home-Position anfahren'
            ])
            
            for i, (y, approx_angle) in enumerate(zip([P_Y + calculate_step_size() * i for i in range(NUMBER_OF_MEASUREMENTS)], [row[2] for row in table_data])):
                # 1. Servo-Winkel einstellen
                writer.writerow([
                    'servo',
                    json.dumps({"angle": int(approx_angle)}),
                    f"Servo: Winkel auf {int(approx_angle)}° setzen (Y={y:.1f}cm)"
                ])
                
                # 2. Foto aufnehmen
                writer.writerow([
                    'photo',
                    '{}',
                    f"Kamera: Foto aufnehmen bei Y={y:.1f}cm, Winkel={int(approx_angle)}°"
                ])
                
                # 3. Stepper bewegen (außer beim letzten Punkt)
                if i < NUMBER_OF_MEASUREMENTS - 1:
                    # Schrittmotor-Parameter berechnen
                    step_distance = calculate_step_size()  # cm
                    d = 28.0  # Durchmesser der Winde in mm (Standardwert)
                    circumference = 3.141592653589793 * d  # mm
                    step_mm = step_distance * 10  # Umrechnung cm -> mm
                    steps = int((step_mm / circumference) * 4096)  # Schritte für 28BYJ-48
                    direction = 1  # 1 = aufwärts
                    speed = 80  # Standardgeschwindigkeit
                    
                    dir_text = "aufwärts"
                    
                    writer.writerow([
                        'stepper',
                        json.dumps({"steps": steps, "direction": direction, "speed": speed}),
                        f"Stepper: {steps} Schritte, {step_distance:.1f}cm, Richtung {dir_text}, Geschwindigkeit: {speed}"
                    ])
                    
        print(f"\nCSV-Datei für main.py-Import erstellt: {csv_filename}")
        print(f"Format: ['type', 'params', 'description'] - kompatibel mit main.py")
        print(f"Stepper-Geschwindigkeit: 80 (Standard)")
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
    
    # Subplot 2: Detaillierte Rechentabelle
    plt.subplot(2, 3, 2)
    plt.axis('off')  # Achsen ausblenden
    
    # Detaillierte Tabellendaten für die Rechnung vorbereiten
    calc_headers = ['Nr.', 'Y-Pos', 'dx', 'dy', 'α (rad)', 'α (°)', 'Approx.']
    calc_rows = []
    for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
        # Berechnungsschritte nachvollziehen (entsprechend der neuen calculate_angle Logik)
        dx = NEW_CENTER_X - Z_MODULE_X
        dy = abs(y - NEW_CENTER_Y)  # Absolutwert der Distanz
          # Neue Berechnung entsprechend der korrigierten calculate_angle Funktion
        if abs(dx) < 0.001:
            alpha_rad = math.pi / 2 if dy == 0 else 0
            alpha_deg = 90.0 if dy == 0 else 0.0
        else:
            alpha_rad = math.atan(dy / abs(dx))
            alpha_deg = alpha_rad * 180 / math.pi
            # Komplementärwinkel für korrekte Orientierung
            alpha_deg = 90.0 - alpha_deg
        
        calc_rows.append([
            i+1, 
            f"{y:.1f}", 
            f"{dx:.0f}", 
            f"{dy:.1f}", 
            f"{alpha_rad:.3f}", 
            f"{alpha_deg:.1f}°", 
            f"{approx_angle:.1f}°"
        ])
    
    # Tabelle in das Diagramm einfügen
    plt.table(cellText=calc_rows,
             colLabels=calc_headers,
             cellLoc='center',
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('Detaillierte Rechenschritte', fontsize=14)
    
    # Subplot 3: 3D-Visualisierung der Scanpositionen und Winkel
    try:
        from mpl_toolkits.mplot3d import Axes3D
        
        ax = plt.subplot(2, 3, 3, projection='3d')
        
        # Z-Modul-Positionen (Scanpunkte)
        x_scan = [Z_MODULE_X] * len(y_positions)
        z_scan = [0] * len(y_positions)
        ax.scatter(x_scan, y_positions, z_scan, color='blue', s=50, label='Z-Modul Positionen')
        
        # Scanpfad
        ax.plot(x_scan, y_positions, z_scan, color='blue', linewidth=2)
        
        # Neues Zentrum
        ax.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [0], color='red', s=100, label='Neues Zentrum')
        
        # Winkellinien mit Höhe basierend auf approximiertem Winkelwert
        for i, (y, orig_angle, approx_angle) in enumerate(zip(y_positions, original_angles, approximated_angles)):
            # Normalisierter approximierter Winkel für Höhe (z-Achse)
            z_height = approx_angle / 10  # Skalieren für bessere Visualisierung
            
            # Linie von Scanpunkt zum Zentrum mit Höhe
            ax.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], [0, z_height], 
                   '--', color='green', alpha=0.7)
            
            # Punkt, der den approximierten Winkel in der Höhe anzeigt
            ax.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [z_height], 
                      color='red', s=30, alpha=0.7)
            
            # Text für approximierten Winkel
            ax.text(NEW_CENTER_X + 5, NEW_CENTER_Y, z_height, f"{approx_angle:.1f}°", 
                   fontsize=8, color='red')
        
        # Achsen und Labels konfigurieren
        ax.set_title('3D-Darstellung der Winkelbeziehungen', fontsize=14)
        ax.set_xlabel('X-Position (cm)', fontsize=12)
        ax.set_ylabel('Y-Position (cm)', fontsize=12)
        ax.set_zlabel('Winkel (skaliert)', fontsize=12)
        ax.legend(loc='best')
        
        # Ansichtswinkel einstellen
        ax.view_init(elev=30, azim=-60)
        
    except Exception as e:
        # Fallback, falls 3D-Plot nicht funktioniert
        plt.subplot(2, 3, 3)
        plt.text(0.5, 0.5, f"3D-Darstellung nicht verfügbar:\n{e}", 
                ha='center', va='center', fontsize=12, wrap=True)
        plt.axis('off')
    
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
      # Subplot 5: CSV-Export Übersichtstabelle (neues main.py-Format)
    plt.subplot(2, 3, 5)
    plt.axis('off')  # Achsen ausblenden
    
    # CSV-Daten für die Übersichtstabelle vorbereiten (main.py-Format)
    csv_headers = ['Type', 'Params (JSON)', 'Description']
    csv_preview_rows = []
    
    # Home-Zeile
    csv_preview_rows.append(['home', '{}', 'Home-Position anfahren'])
    
    # Erste 3 Messpunkte als Beispiel zeigen
    for i in range(min(3, NUMBER_OF_MEASUREMENTS)):
        y_pos = P_Y + calculate_step_size() * i
        approx_angle = table_data[i][2]  # Approximierter Winkel aus der Tabelle
        
        # Servo-Zeile
        csv_preview_rows.append([
            'servo', 
            f'{{"angle": {int(approx_angle)}}}', 
            f'Servo: {int(approx_angle)}° (Y={y_pos:.1f}cm)'
        ])
        
        # Photo-Zeile
        csv_preview_rows.append([
            'photo', 
            '{}', 
            f'Foto bei Y={y_pos:.1f}cm'
        ])
        
        # Stepper-Zeile (außer beim letzten Punkt)
        if i < NUMBER_OF_MEASUREMENTS - 1:
            step_distance = calculate_step_size()
            steps = int((step_distance * 10 / (3.141592653589793 * 28.0)) * 4096)  # Schritte berechnen
            csv_preview_rows.append([
                'stepper', 
                f'{{"steps": {steps}, "direction": 1, "speed": 80}}', 
                f'{steps} Schritte, {step_distance:.1f}cm'
            ])
    
    # Wenn mehr als 3 Punkte, "..." anzeigen
    if NUMBER_OF_MEASUREMENTS > 3:
        csv_preview_rows.append(['...', '...', '...'])
    
    # Tabelle in das Diagramm einfügen
    plt.table(cellText=csv_preview_rows,
             colLabels=csv_headers,
             cellLoc='left',  # Linksbündig für bessere Lesbarkeit
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.title('CSV-Export Vorschau (main.py-Format)', fontsize=14)
    
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
        f"Servo-Grenzen: {SERVO_ANGLE_MIN}° - {SERVO_ANGLE_MAX}°",
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
