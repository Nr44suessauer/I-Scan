#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TARGET COORDINATE ANGLE CALCULATION EXPLANATION - ENHANCED VERSION
================================================================

Creates a comprehensive, student-friendly explanation of the Target Coordinate Angle 
calculation with all different angles and detailed explanations.

Author: I-Scan Team
Version: 2.0 (Enhanced Student-Friendly Version)
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y,
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    ensure_output_dir
)
from calculations import calculate_geometric_angles


def create_student_friendly_visualization():
    """
    Creates a comprehensive, student-friendly representation of the Target Coordinate Angle calculation
    with all different angles and detailed explanations
    """
    # Get measurement data
    geometric_angles = calculate_geometric_angles()
    
    # Create figure with subplots - larger for more content
    fig = plt.figure(figsize=(20, 12))
    
    # Create a 2x3 grid layout
    gs = fig.add_gridspec(3, 3, height_ratios=[2, 1.5, 1], width_ratios=[1.5, 1, 1])
    
    # === MAIN PLOT: Coordinate system and vectors (top left, large) ===
    ax_main = fig.add_subplot(gs[0, :2])
    ax_main.set_aspect('equal')
    
    # Draw coordinate system with axes
    ax_main.axhline(y=0, color='black', linewidth=2, alpha=0.8)
    ax_main.axvline(x=0, color='black', linewidth=2, alpha=0.8)
    
    # Add coordinate system labels with angles
    ax_main.text(65, 3, '+X (0°)', fontsize=14, fontweight='bold', ha='center', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue'))
    ax_main.text(3, 60, '+Y (90°)', fontsize=14, fontweight='bold', ha='center', rotation=90,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen'))
    ax_main.text(-65, 3, '-X (180°)', fontsize=14, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral'))
    ax_main.text(3, -60, '-Y (270°)', fontsize=14, fontweight='bold', ha='center', rotation=90,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow'))
    
    # Plot target with prominent marker
    ax_main.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'ro', markersize=15, 
                label=f'🎯 Target ({TARGET_CENTER_X}, {TARGET_CENTER_Y})', markeredgecolor='darkred', markeredgewidth=2)
    
    # Plot scanner positions and vectors with detailed annotations
    colors = plt.cm.viridis(np.linspace(0, 1, len(geometric_angles)))
    
    for i, (angle_data, color) in enumerate(zip(geometric_angles, colors)):
        scanner_y = angle_data['y_pos']
        
        # Plot scanner position with larger markers
        ax_main.plot(SCANNER_MODULE_X, scanner_y, 's', markersize=12, color=color, 
                    markeredgecolor='black', markeredgewidth=2)
        ax_main.text(SCANNER_MODULE_X-8, scanner_y, f'P{i+1}', fontsize=12, fontweight='bold', 
                    ha='right', va='center', color='black',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        # Calculate vector components
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - scanner_y
        
        # Draw vector with arrow
        ax_main.arrow(SCANNER_MODULE_X, scanner_y, dx*0.75, dy*0.75, 
                     head_width=3, head_length=4, fc=color, ec=color, alpha=0.8, linewidth=2)
        
        # Calculate target coordinate angle
        target_coord_angle = math.degrees(math.atan2(dy, dx))
        
        # Normalize angle
        while target_coord_angle > 180.0:
            target_coord_angle -= 360.0
        while target_coord_angle < -180.0:
            target_coord_angle += 360.0
        
        # Add angle annotation with background
        mid_x = SCANNER_MODULE_X + dx*0.4
        mid_y = scanner_y + dy*0.4
        ax_main.text(mid_x, mid_y, f'{target_coord_angle:.1f}°', 
                    fontsize=11, fontweight='bold', color='white',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.9))
        
        # Draw angle arc for first 3 points (to avoid clutter)
        if i < 3:
            # Draw angle arc from X-axis
            angle_rad = math.atan2(dy, dx)
            arc_angles = np.linspace(0, angle_rad, 50)
            arc_radius = 15
            arc_x = SCANNER_MODULE_X + arc_radius * np.cos(arc_angles)
            arc_y = scanner_y + arc_radius * np.sin(arc_angles)
            ax_main.plot(arc_x, arc_y, color=color, linewidth=3, alpha=0.7)
    
    # Add grid and formatting
    ax_main.grid(True, alpha=0.3, linestyle='--')
    ax_main.set_xlim(-75, 75)
    ax_main.set_ylim(-70, 70)
    ax_main.set_xlabel('X Position (cm)', fontweight='bold', fontsize=12)
    ax_main.set_ylabel('Y Position (cm)', fontweight='bold', fontsize=12)
    ax_main.set_title('Target Coordinate Angle Vectors\n(Standard-Koordinatensystem mit Winkel-Beispielen)', 
                     fontweight='bold', fontsize=14)
    ax_main.legend(loc='upper right', fontsize=11)
    
    # === ERKLÄRUNGSTEXT (oben rechts) ===
    ax_explanation = fig.add_subplot(gs[0, 2])
    ax_explanation.axis('off')
    
    explanation_text = """
📚 STUDENTENFREUNDLICHE ERKLÄRUNG

🎯 WAS BERECHNEN WIR?
Den Winkel vom Scanner zum Target im 
Standard-Koordinatensystem.

📐 KOORDINATENSYSTEM:
• 0° = +X-Achse (rechts) 
• 90° = +Y-Achse (oben)
• 180° = -X-Achse (links)
• 270° = -Y-Achse (unten)

🔢 EINFACHE FORMEL:
target_angle = atan2(dy, dx)

WO:
• dx = Target_X - Scanner_X
• dy = Target_Y - Scanner_Y

🎨 IM DIAGRAMM:
• Quadrate = Scanner-Positionen
• Roter Kreis = Target-Objekt
• Pfeile = Richtungsvektoren
• Zahlen = Berechnete Winkel

💡 WARUM atan2()?
atan2 berücksichtigt die Vorzeichen 
von dx und dy und gibt den korrekten 
Quadranten zurück!

✅ ERGEBNIS:
Alle Winkel liegen zwischen 
-180° und +180°
"""
    
    ax_explanation.text(0.05, 0.95, explanation_text, transform=ax_explanation.transAxes, 
                       fontsize=11, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.9))
    
    # === BERECHNUNGSTABELLE (unten links) ===
    ax_table = fig.add_subplot(gs[1, :2])
    ax_table.axis('off')
    
    # Create detailed calculation table
    table_data = []
    headers = ['Point', 'Scanner Y\n(cm)', 'dx\n(cm)', 'dy\n(cm)', 'atan2(dy,dx)\n(radians)', 
               'Target Angle\n(degrees)', 'Quadrant', 'Erklärung']
    
    for i, angle_data in enumerate(geometric_angles):
        scanner_y = angle_data['y_pos']
        
        # Calculate components
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = TARGET_CENTER_Y - scanner_y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Normalize
        normalized_angle = angle_deg
        while normalized_angle > 180.0:
            normalized_angle -= 360.0
        while normalized_angle < -180.0:
            normalized_angle += 360.0
        
        # Determine quadrant and explanation
        if dx > 0 and dy >= 0:
            quadrant = "I"
            explanation = "rechts-oben"
        elif dx <= 0 and dy > 0:
            quadrant = "II"
            explanation = "links-oben"
        elif dx < 0 and dy <= 0:
            quadrant = "III"
            explanation = "links-unten"
        else:
            quadrant = "IV"
            explanation = "rechts-unten"
        
        row = [
            f"{i+1}",
            f"{scanner_y:.1f}",
            f"{dx}",
            f"{dy:.1f}",
            f"{angle_rad:.3f}",
            f"{normalized_angle:.1f}°",
            quadrant,
            explanation
        ]
        table_data.append(row)
    
    # Create and style table
    table = ax_table.table(cellText=table_data,
                          colLabels=headers,
                          cellLoc='center',
                          loc='center',
                          bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    # Style header
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Color-code quadrants
    for i in range(len(table_data)):
        row_idx = i + 1
        quadrant = table_data[i][6]
        if quadrant == "I":
            color = '#E8F5E8'  # Light green
        elif quadrant == "II":
            color = '#E8E8F5'  # Light blue
        elif quadrant == "III":
            color = '#F5E8E8'  # Light red
        else:  # IV
            color = '#F5F5E8'  # Light yellow
        
        for j in range(len(headers)):
            table[(row_idx, j)].set_facecolor(color)
    
    ax_table.set_title('Detaillierte Berechnungstabelle - Schritt für Schritt', 
                      fontweight='bold', fontsize=14, pad=20)
    
    # === FORMEL-ERKLÄRUNG (unten rechts) ===
    ax_formula = fig.add_subplot(gs[1, 2])
    ax_formula.axis('off')
    
    formula_explanation = """
🧮 SCHRITT-FÜR-SCHRITT:

1️⃣ KOMPONENTEN BERECHNEN:
   dx = 50 - 0 = 50 cm (konstant)
   dy = 25 - scanner_y (variabel)

2️⃣ ATAN2 ANWENDEN:
   angle_rad = atan2(dy, dx)
   
3️⃣ IN GRAD UMWANDELN:
   angle_deg = angle_rad × (180/π)
   
4️⃣ NORMALISIEREN:
   Bereich: [-180°, +180°]

💡 WARUM DIESE FORMEL?
• atan2 berücksichtigt Vorzeichen
• Korrekte Quadranten-Zuordnung
• Standard-Koordinatensystem
• Mathematisch eindeutig

🎯 PRAXIS-TIPP:
Positive Winkel = Target über Scanner
Negative Winkel = Target unter Scanner
"""
    
    ax_formula.text(0.05, 0.95, formula_explanation, transform=ax_formula.transAxes, 
                   fontsize=10, verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    # === BEISPIELRECHNUNG (ganz unten) ===
    ax_example = fig.add_subplot(gs[2, :])
    ax_example.axis('off')
    
    # Take first point as example
    first_point = geometric_angles[0]
    scanner_y = first_point['y_pos']
    dx = TARGET_CENTER_X - SCANNER_MODULE_X
    dy = TARGET_CENTER_Y - scanner_y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
      example_text = f"""
🎓 DETAILED EXAMPLE CALCULATION FOR POINT 1:

Given: Target at ({TARGET_CENTER_X}, {TARGET_CENTER_Y}), Scanner at ({SCANNER_MODULE_X}, {scanner_y})

Step 1: dx = {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm
Step 2: dy = {TARGET_CENTER_Y} - {scanner_y} = {dy} cm  
Step 3: angle_rad = atan2({dy}, {dx}) = {angle_rad:.4f} radians
Step 4: angle_deg = {angle_rad:.4f} × (180/π) = {angle_deg:.2f}°
Step 5: Normalized = {angle_deg:.2f}° (already in correct range)

✅ Ergebnis: Der Scanner muss sich um {angle_deg:.2f}° zum Target ausrichten (Quadrant I - rechts oben)
"""
    
    ax_example.text(0.02, 0.8, example_text, transform=ax_example.transAxes, 
                   fontsize=12, verticalalignment='top', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', 
                            edgecolor='orange', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    return fig


def save_enhanced_target_coord_angle_visualization():
    """
    Speichert die erweiterte Target Coordinate Angle Visualisierung
    """
    ensure_output_dir()
    
    print("🎨 Erstelle erweiterte Target Coordinate Angle Visualisierung...")
    
    fig = create_student_friendly_visualization()
    
    # Save the figure
    output_path = "output/08_target_coord_angle_explanation.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Erweiterte Target Coordinate Angle Visualisierung gespeichert: {output_path}")
    
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    """Run enhanced target coordinate angle explanation when executed directly"""
    save_enhanced_target_coord_angle_visualization()
