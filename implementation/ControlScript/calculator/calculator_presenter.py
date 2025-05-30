import math
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D

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

def calculate_step_size():
    """Berechnet die Schrittgröße für die Messungen"""
    if NUMBER_OF_MEASUREMENTS > 0:
        return DELTA_SCAN / NUMBER_OF_MEASUREMENTS
    return 0

def generate_presentation_view():
    """
    Generiert eine kompakte Präsentationsansicht mit Tabelle und Visualisierung in einem Bild
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
    
    # Y-Positionen und Winkel berechnen
    y_positions = [P_Y + step_size * i for i in range(NUMBER_OF_MEASUREMENTS)]
    angles = [calculate_angle(y) for y in y_positions]
    
    for i, (y, angle) in enumerate(zip(y_positions, angles)):
        # Z-Modul Koordinaten formatieren (X bleibt fest, Y variiert)
        z_coords = f"({Z_MODULE_X}, {round(y, 1)})"
        
        # Daten für die Tabelle hinzufügen
        table_data.append([
            i + 1,                       # Messungsnummer
            round(angle, 1),             # Winkel (gerundet auf 1 Dezimalstelle)
            round(y, 1),                 # Y-Position
            z_coords                      # Z-Modul Koordinaten
        ])
    
    # Tabelle ausgeben
    print(tabulate(table_data, 
                  headers=['Messung Nr.', 'Winkel (°)', 'Y-Position (cm)', 'Z-Modul (Koordinaten)'],
                  tablefmt='grid',
                  numalign='right'))
    
    # Große Grafik mit Tabelle und Visualisierung erstellen
    plt.figure(figsize=(16, 10))
    
    # Layout definieren: Grid mit 2 Spalten, links Tabelle, rechts Visualisierungen
    gs = plt.GridSpec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1])
    
    # Tabelle erstellen (oben links)
    ax_table = plt.subplot(gs[0, 0])
    ax_table.axis('off')
    
    # Tabellendaten formatieren
    table_headers = ['Nr.', 'Winkel (°)', 'Y (cm)', 'Koordinaten']
    table_rows = []
    for row in table_data:
        table_rows.append([row[0], f"{row[1]}°", f"{row[2]}", row[3]])
    
    # Tabelle mit angepasstem Style
    table = plt.table(cellText=table_rows,
                     colLabels=table_headers,
                     cellLoc='center',
                     loc='center',
                     cellColours=[['#f2f2f2']*4 for _ in range(len(table_rows))],
                     colColours=['#e6e6e6']*4,
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Tabellenhöhe anpassen
    
    ax_table.set_title('Messwerte', fontsize=14, pad=20, fontweight='bold')
    
    # Konfigurationsbox (unten links)
    ax_config = plt.subplot(gs[1, 0])
    ax_config.axis('off')
    
    # Text-Informationen zur Konfiguration
    config_info = [
        f"Konfiguration",
        f"─────────────────────",
        f"Neues Zentrum: ({NEW_CENTER_X}, {NEW_CENTER_Y})",
        f"Z-Modul Start: ({Z_MODULE_X}, {Z_MODULE_Y})",
        f"Delta Scan: {DELTA_SCAN} cm",
        f"Messungen: {NUMBER_OF_MEASUREMENTS}",
        f"Schrittgröße: {calculate_step_size():.1f} cm",
        f"─────────────────────",
        f"Winkelbereich:",
        f"{min(angles):.1f}° - {max(angles):.1f}°"
    ]
    
    # Formatierte Konfigurationsbox
    ax_config.text(0.5, 0.5, "\n".join(config_info),
                  ha='center', va='center', fontsize=11,
                  bbox=dict(facecolor='#f9f9f9', edgecolor='gray', 
                          boxstyle='round,pad=1', alpha=0.8))
    ax_config.set_title('Parameter', fontsize=14, pad=20, fontweight='bold')
    
    # 2D-Visualisierung des Scan-Pfades (oben rechts)
    ax_2d = plt.subplot(gs[0, 1])
    
    # Z-Modul-Positionen darstellen
    for i, y in enumerate(y_positions):
        ax_2d.plot(Z_MODULE_X, y, 'o', color='blue', markersize=8, 
                  label=f'Messung {i+1}' if i == 0 else "")
    
    # Scanpfad darstellen
    ax_2d.plot([Z_MODULE_X] * len(y_positions), y_positions, '-', 
              color='blue', linewidth=2, label='Scan-Pfad')
    
    # Neues Zentrum darstellen
    ax_2d.plot(NEW_CENTER_X, NEW_CENTER_Y, 'ro', markersize=10, label='Neues Zentrum')
    
    # Winkellinien und Winkeltext für alle Messungen
    for i, (y, angle) in enumerate(zip(y_positions, angles)):
        color_intensity = 0.3 + (i / len(y_positions)) * 0.7  # Farbverlauf
        
        # Linie vom Z-Modul zum neuen Zentrum zeichnen
        ax_2d.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], '--', 
                  color=(0, color_intensity, 0), linewidth=1.5, 
                  alpha=0.7, label='Winkelbeziehung' if i == 0 else "")
        
        # Winkel als Text anzeigen
        text_x = (Z_MODULE_X + NEW_CENTER_X) / 2 - 15
        text_y = (y + NEW_CENTER_Y) / 2 + 5
        
        ax_2d.text(text_x, text_y, f"{angle:.1f}°", 
                  color='black', fontsize=9, fontweight='bold',
                  bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3'))
        
        # Winkel-Bogen
        angle_radius = 20
        dx = NEW_CENTER_X - Z_MODULE_X
        dy = NEW_CENTER_Y - y
        angle_rad = math.atan2(dy, dx)
        
        start_angle = 90 * math.pi / 180
        end_angle = angle_rad
        
        # Winkel-Bogen als Kreisbogen darstellen
        arc = patches.Arc((Z_MODULE_X, y), angle_radius, angle_radius,
                         theta1=math.degrees(start_angle), 
                         theta2=math.degrees(end_angle),
                         color='red', linewidth=1.5)
        ax_2d.add_patch(arc)
    
    # Achsen konfigurieren
    ax_2d.set_title('2D-Darstellung des Scan-Pfades', fontsize=14, fontweight='bold')
    ax_2d.set_xlabel('X-Position (cm)', fontsize=12)
    ax_2d.set_ylabel('Y-Position (cm)', fontsize=12)
    ax_2d.grid(True, alpha=0.3)
    ax_2d.legend(loc='upper right')
    
    # Achsenlänge anpassen
    max_x = max(NEW_CENTER_X, Z_MODULE_X) * 1.2
    max_y = max(NEW_CENTER_Y, max(y_positions)) * 1.2
    min_x = min(0, Z_MODULE_X) - 10
    min_y = min(0, min(y_positions)) - 10
    ax_2d.axis([min_x, max_x, min_y, max_y])
    
    # 3D-Visualisierung (unten rechts)
    try:
        ax_3d = plt.subplot(gs[1, 1], projection='3d')
        
        # Z-Modul-Positionen
        x_scan = [Z_MODULE_X] * len(y_positions)
        z_scan = [0] * len(y_positions)
        ax_3d.scatter(x_scan, y_positions, z_scan, color='blue', s=50, label='Z-Modul')
        
        # Scanpfad
        ax_3d.plot(x_scan, y_positions, z_scan, color='blue', linewidth=2)
        
        # Neues Zentrum
        ax_3d.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [0], color='red', s=100, label='Zentrum')
        
        # Winkellinien mit Höhe
        for i, (y, angle) in enumerate(zip(y_positions, angles)):
            z_height = angle / 10
            
            # Linie von Scanpunkt zum Zentrum mit Höhe
            ax_3d.plot([Z_MODULE_X, NEW_CENTER_X], [y, NEW_CENTER_Y], [0, z_height], 
                      '--', color='green', alpha=0.7)
            
            # Punkt für Winkel in der Höhe
            ax_3d.scatter([NEW_CENTER_X], [NEW_CENTER_Y], [z_height], 
                         color='green', s=30, alpha=0.7)
            
            # Text für Winkel in 3D
            ax_3d.text(NEW_CENTER_X+5, NEW_CENTER_Y, z_height, f"{angle:.1f}°", 
                      color='darkgreen', size=8)
        
        # Achsen konfigurieren
        ax_3d.set_title('3D-Darstellung der Winkelbeziehungen', fontsize=14, fontweight='bold')
        ax_3d.set_xlabel('X-Position (cm)')
        ax_3d.set_ylabel('Y-Position (cm)')
        ax_3d.set_zlabel('Winkel (skaliert)')
        ax_3d.legend(loc='upper right')
        
        # Ansichtswinkel
        ax_3d.view_init(elev=30, azim=-60)
        
    except Exception as e:
        # Fallback
        ax_3d = plt.subplot(gs[1, 1])
        ax_3d.text(0.5, 0.5, f"3D-Darstellung nicht verfügbar:\n{e}", 
                  ha='center', va='center', fontsize=12)
        ax_3d.axis('off')
    
    # Titel über gesamtem Plot
    plt.suptitle('I-Scan Winkel-Visualisierung', fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Anpassung für den Gesamttitel
    
    # Bild speichern
    visualization_path = 'scan_visualization_presenter.png'
    plt.savefig(visualization_path, dpi=150)
    print(f"\nKompakte Präsentationsansicht wurde gespeichert unter: {visualization_path}")
    
    try:
        plt.show()
    except Exception as e:
        print(f"Hinweis: Die Grafik konnte nicht angezeigt werden ({e}), wurde aber unter '{visualization_path}' gespeichert.")

def main():
    """Hauptfunktion zur Ausführung des Programms"""
    # Präsentationsansicht generieren und anzeigen
    generate_presentation_view()

if __name__ == "__main__":
    # Erforderliche Bibliotheken prüfen
    try:
        import pandas as pd
        from tabulate import tabulate
        import matplotlib.pyplot as plt
    except ImportError as e:
        print("Fehlende Bibliothek! Bitte installieren Sie:")
        print("pip install pandas tabulate matplotlib")
        print(f"Fehler: {e}")
        exit(1)
    
    main()
