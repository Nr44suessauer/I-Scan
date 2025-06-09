#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPLETE VISUALIZATION MODULE
=============================

Creates comprehensive visualization with multiple diagrams showing
all aspects of the servo angle calculation in one integrated view.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import os
from config import (
    TARGET_CENTER_X, TARGET_CENTER_Y, 
    SCANNER_MODULE_X, SCANNER_MODULE_Y,
    SCAN_DISTANCE, MIN_SERVO_ANGLE, MAX_SERVO_ANGLE,
    OUTPUT_DIR, ensure_output_dir
)


def create_complete_visualization(angles_data):
    """
    Creates comprehensive visualization with multiple diagrams
    """
    # Create main figure with compact layout for better space utilization
    fig = plt.figure(figsize=(24, 18))
    fig.patch.set_facecolor('white')
    fig.suptitle('SERVO ANGLE CALCULATION - MATHEMATICAL VISUALIZATION', 
                 fontsize=18, fontweight='bold', y=0.97, color='navy')

    # === MAIN DIAGRAM: Geometric representation ===
    ax1 = plt.subplot2grid((5, 4), (0, 0), colspan=2, rowspan=3)
    ax1.set_title('Geometric Representation of 3D Scanner System', 
                  fontsize=11, fontweight='bold', pad=15, color='darkblue')
    
    # Setup axes with compact style
    ax1.set_xlim(-25, 90)
    ax1.set_ylim(-15, 80)
    ax1.grid(True, alpha=0.3, linewidth=0.6, linestyle='--')
    ax1.set_aspect('equal')
    ax1.set_xlabel('X-Position (cm)', fontsize=9, fontweight='bold')
    ax1.set_ylabel('Y-Position (cm)', fontsize=9, fontweight='bold')
    ax1.set_facecolor('#f8f9fa')
    
    # Coordinate system with stronger axes
    ax1.axhline(y=0, color='black', linewidth=1.5, alpha=0.8)
    ax1.axvline(x=0, color='black', linewidth=1.5, alpha=0.8)
    
    # Scanner path with compact design
    scan_y = np.linspace(0, SCAN_DISTANCE, 100)
    ax1.plot([SCANNER_MODULE_X] * len(scan_y), scan_y, 'g-', 
             linewidth=8, alpha=0.6, label='Scanner Movement Path', solid_capstyle='round')
    
    # Target object compact highlighting
    ax1.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'bs', markersize=16, 
             markeredgewidth=3, markeredgecolor='navy', zorder=10)
    ax1.text(TARGET_CENTER_X + 5, TARGET_CENTER_Y - 3, f'TARGET OBJECT\n({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm',
             ha='left', va='top', fontsize=8, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.4", facecolor="lightblue", 
                      edgecolor='navy', linewidth=1.5, alpha=0.95))
    
    # Measurement points with improved display
    colors = ['#FF4444', '#FF8800', '#8844FF', '#AA4400']
    marker_styles = ['o', 's', '^', 'D']
    
    for i, data in enumerate(angles_data):
        color = colors[i % len(colors)]
        marker = marker_styles[i % len(marker_styles)]
        y_pos = data['y_pos']
        
        # Measurement point with compact marker
        ax1.plot(SCANNER_MODULE_X, y_pos, marker, color=color, markersize=12, 
                markeredgewidth=2, markeredgecolor='black', zorder=8)
        
        # Sight lines to target
        ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [y_pos, TARGET_CENTER_Y], 
                 '--', color=color, linewidth=2, alpha=0.7, zorder=3)
        
        # Detailed triangle for point 2 (better visibility)
        if i == 1:
            # Right-angled triangle compact
            triangle_x = [SCANNER_MODULE_X, TARGET_CENTER_X, TARGET_CENTER_X, SCANNER_MODULE_X]
            triangle_y = [y_pos, y_pos, TARGET_CENTER_Y, y_pos]
            ax1.plot(triangle_x, triangle_y, 'b-', linewidth=3, alpha=0.9, zorder=5)
            ax1.fill([SCANNER_MODULE_X, TARGET_CENTER_X, TARGET_CENTER_X], 
                     [y_pos, y_pos, TARGET_CENTER_Y], 
                     alpha=0.15, color='lightblue', zorder=2)
            
            # Right angle marking compact
            corner_size = 3
            ax1.plot([TARGET_CENTER_X-corner_size, TARGET_CENTER_X-corner_size, TARGET_CENTER_X], 
                     [TARGET_CENTER_Y, TARGET_CENTER_Y+corner_size, TARGET_CENTER_Y+corner_size], 
                     'b-', linewidth=2)
            
            # Side labels compact positioning
            mid_x = (SCANNER_MODULE_X + TARGET_CENTER_X) / 2
            ax1.text(mid_x, y_pos + 3, f'dx = {data["dx"]} cm\n(Adjacent)', 
                     ha='center', va='bottom', fontsize=7, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", 
                              edgecolor='orange', linewidth=1, alpha=0.95))
            
            ax1.text(TARGET_CENTER_X + 3, (y_pos + TARGET_CENTER_Y) / 2, 
                     f'dy = {data["dy"]:.1f} cm\n(Opposite)', 
                     ha='left', va='center', fontsize=7, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", 
                              edgecolor='darkgreen', linewidth=1, alpha=0.95))
            
            # Hypotenuse compact labeling
            hyp_length = math.sqrt(data['dx']**2 + data['dy']**2)
            hyp_mid_x = (SCANNER_MODULE_X + TARGET_CENTER_X) / 2 + 2
            hyp_mid_y = (y_pos + TARGET_CENTER_Y) / 2 + 2
            ax1.text(hyp_mid_x, hyp_mid_y, f'Hyp.\n{hyp_length:.1f} cm', 
                     ha='center', va='center', fontsize=7, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="lightcoral", 
                              edgecolor='darkred', linewidth=1, alpha=0.9),
                     rotation=-20)
            
            # Angle arc compact
            alpha_rad = data['alpha'] * math.pi / 180
            angle_arc = np.linspace(0, alpha_rad, 40)
            arc_r = 12
            arc_x = SCANNER_MODULE_X + arc_r * np.cos(angle_arc)
            arc_y = y_pos - arc_r * np.sin(angle_arc)
            ax1.plot(arc_x, arc_y, 'r-', linewidth=3, zorder=6)
            ax1.text(SCANNER_MODULE_X + arc_r + 3, y_pos - arc_r/2 - 2, 
                     f'α = {data["alpha"]:.1f}°', 
                     fontsize=8, color='darkred', fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="white", 
                              edgecolor='red', linewidth=1, alpha=0.95))
          # Point labeling compact - show geometry and servo angles
        ax1.text(SCANNER_MODULE_X - 12, y_pos, 
                 f'P{data["point"]}\nY={y_pos:.1f}\nGeo={data["exact_angle"]:.1f}°\nServo={data["interpolated_angle"]:.1f}°', 
                 ha='right', va='center', fontsize=7, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor=color, 
                          edgecolor='black', linewidth=1, alpha=0.9))
    
    # Legend compact
    ax1.legend(fontsize=8, loc='upper right', frameon=True, 
               fancybox=True, shadow=True, framealpha=0.9)    # === DIAGRAM 2: Angle progression ===
    ax2 = plt.subplot2grid((5, 4), (0, 2), colspan=2, rowspan=1)
    ax2.set_title('Servo Angle Progression over Scan Position', 
                  fontsize=10, fontweight='bold', pad=15, color='darkblue')
    
    y_positions = [data['y_pos'] for data in angles_data]
    exact_angles = [data['exact_angle'] for data in angles_data]
    interpolated_angles = [data['interpolated_angle'] for data in angles_data]
    
    # Lines with compact markers - show geometric vs servo angles
    line1 = ax2.plot(y_positions, exact_angles, 'o-', color='#2E86AB', 
                     linewidth=3, markersize=7, markeredgewidth=2, 
                     markeredgecolor='white', label='Geometric Angles')
    line2 = ax2.plot(y_positions, interpolated_angles, 's-', color='#A23B72', 
                     linewidth=3, markersize=7, markeredgewidth=2, 
                     markeredgecolor='white', label='Servo Angles')
    
    ax2.set_xlabel('Y-Position (cm)', fontsize=9, fontweight='bold')
    ax2.set_ylabel('Angle (°)', fontsize=9, fontweight='bold')
    ax2.grid(True, alpha=0.4, linestyle='--')
    ax2.legend(fontsize=8, frameon=True, fancybox=True, shadow=True)
    ax2.set_facecolor('#f8f9fa')
    
    # Show values at points with smaller font
    for i, (y_pos, exact, interp) in enumerate(zip(y_positions, exact_angles, interpolated_angles)):
        ax2.annotate(f'{exact:.1f}°', (y_pos, exact), textcoords="offset points", 
                     xytext=(0,8), ha='center', fontsize=6, fontweight='bold', color='#2E86AB')
        ax2.annotate(f'{interp:.1f}°', (y_pos, interp), textcoords="offset points", 
                     xytext=(0,-12), ha='center', fontsize=6, fontweight='bold', color='#A23B72')

    # === DIAGRAM 3: Trigonometry explanation ===
    ax3 = plt.subplot2grid((5, 4), (1, 2), colspan=2, rowspan=2)
    ax3.set_title('Trigonometry Formulas', fontsize=12, fontweight='bold', 
                  pad=20, color='darkblue')
    ax3.axis('off')
    ax3.set_facecolor('#f8f9fa')

    # Formula text with enlarged formatting
    formula_text = """TRIGONOMETRY FUNDAMENTALS:

• tan(α) = Opposite side ÷ Adjacent side
• tan(α) = dy ÷ dx
• α = arctan(dy ÷ dx)

SERVO ANGLE CALCULATION:
• Exact angle = arctan(dx/dy) 
• Interpolated angle = MIN_SERVO + progress × (MAX_SERVO - MIN_SERVO)
• Range: {MIN_SERVO_ANGLE}° → {MAX_SERVO_ANGLE}°

FINAL ANGLE:
• Used angle = Interpolated angle (for smooth scanning)
• No mechanical correction needed"""
    
    ax3.text(0.03, 0.97, formula_text, transform=ax3.transAxes, fontsize=10,
             verticalalignment='top', fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", 
                      edgecolor='orange', linewidth=1, alpha=0.95))

    # === DIAGRAM 4: Example calculation ===
    ax4 = plt.subplot2grid((5, 4), (3, 2), colspan=2, rowspan=1)
    ax4.set_title('Example Calculation for Point 2', fontsize=12, fontweight='bold', 
                  pad=20, color='darkblue')
    ax4.axis('off')
    ax4.set_facecolor('#f8f9fa')    # Example calculation for point 2 enlarged
    example_data = angles_data[1]  # Point 2
    example_text = f"""STEP-BY-STEP CALCULATION:

Given:
• Scanner: (0, {example_data['y_pos']:.1f}) cm
• Target: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm

Calculation:
• dx = {TARGET_CENTER_X} - 0 = {example_data['dx']} cm
• dy = |{example_data['y_pos']:.1f} - 0| = {example_data['dy']:.1f} cm
• Exact angle = arctan({example_data['dx']}/{example_data['dy']:.1f}) = {example_data['exact_angle']:.2f}°
• Progress = {example_data['progress']:.3f}
• Interpolated = {MIN_SERVO_ANGLE}° + {example_data['progress']:.3f} × ({MAX_SERVO_ANGLE}° - {MIN_SERVO_ANGLE}°) = {example_data['interpolated_angle']:.2f}°
• Final = {example_data['final']:.2f}° (interpolated value used)"""
    
    ax4.text(0.03, 0.97, example_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan", 
                      edgecolor='teal', linewidth=1, alpha=0.95))
    
    # === DIAGRAM 5: Values table ===
    ax5 = plt.subplot2grid((5, 4), (4, 0), colspan=4, rowspan=1)
    ax5.set_title('Complete Calculation Table', fontsize=12, fontweight='bold', 
                  pad=20, color='darkblue')
    ax5.axis('off')
      # Prepare table data
    table_data = []
    headers = ['Point', 'Y-Position\n(cm)', 'dx\n(cm)', 'dy\n(cm)', 
               'Exact°', 'Interp°', 'Feasible', 'Final°']
    
    for data in angles_data:
        feasible_symbol = '✓' if data['is_feasible'] else '✗'
        row = [
            f"P{data['point']}",
            f"{data['y_pos']:.1f}",
            f"{data['dx']:.0f}",
            f"{data['dy']:.1f}",
            f"{data['exact_angle']:.1f}",
            f"{data['interpolated_angle']:.1f}",
            feasible_symbol,
            f"{data['final']:.1f}"
        ]
        table_data.append(row)    # Create table with compact design
    table = ax5.table(cellText=table_data, colLabels=headers,
                      cellLoc='center', loc='center',
                      colWidths=[0.12, 0.15, 0.11, 0.11, 0.12, 0.12, 0.09, 0.12])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.8)

    # Format header with compact design
    header_colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    for i, color in enumerate(header_colors * 2):  # Repeat colors
        if i < len(headers):
            table[(0, i)].set_facecolor(color)
            table[(0, i)].set_text_props(weight='bold', color='white', size=9)
            table[(0, i)].set_height(0.20)
    
    # Format data rows with alternating colors
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E8F4FD')
            else:
                table[(i, j)].set_facecolor('#FFFFFF')
            table[(i, j)].set_text_props(weight='bold', size=9)
            table[(i, j)].set_height(0.15)

    # Optimize layout with larger spacing to avoid overlaps
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.06, left=0.05, right=0.95, 
                        hspace=0.6, wspace=0.4)
      # Save the diagram
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, '06_complete_servo_angle_visualization.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    
    print(f"📊 Complete visualization saved: {output_path}")
    
    # Show the diagram
    plt.show()
    plt.close()
