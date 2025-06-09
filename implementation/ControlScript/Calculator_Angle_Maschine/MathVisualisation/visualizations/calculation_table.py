#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULATION TABLE VISUALIZATION MODULE
======================================

Creates calculation table visualization showing all measurement point 
calculations in a structured table format.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import os
from config import OUTPUT_DIR, ensure_output_dir


def create_calculation_table_visualization(angles_data):
    """
    Creates calculation table visualization
    """
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle('COMPLETE CALCULATION TABLE', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    ax = plt.subplot(1, 1, 1)
    ax.set_title('Summary of All Measurement Point Calculations', 
                 fontsize=12, fontweight='bold', pad=20, color='darkblue')
    ax.axis('off')    # Prepare table data for pure geometric angles
    table_data = []
    headers = ['Point', 'Y-Position\n(cm)', 'dx\n(cm)', 'dy\n(cm)', 
               'Angle°\n(to Y-axis)', 'Distance\n(cm)']
    
    for data in angles_data:
        row = [
            f"P{data['point']}",
            f"{data['y_pos']:.1f}",
            f"{data['dx']:.0f}",
            f"{data['dy']:.1f}",
            f"{data['angle']:.1f}",
            f"{data['hypotenuse']:.1f}"
        ]
        table_data.append(row)
      # Create table
    table = ax.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.12, 0.15, 0.12, 0.12, 0.20, 0.18, 0.11])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 3.0)
    
    # Format header
    header_colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    for i, color in enumerate(header_colors * 2):
        if i < len(headers):
            table[(0, i)].set_facecolor(color)
            table[(0, i)].set_text_props(weight='bold', color='white', size=10)
            table[(0, i)].set_height(0.25)
    
    # Format data rows
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:            table[(i, j)].set_facecolor('#E8F4FD')
            else:
                table[(i, j)].set_facecolor('#FFFFFF')
            table[(i, j)].set_text_props(weight='bold', size=10)
            table[(i, j)].set_height(0.20)
    
    plt.tight_layout()
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, '05_calculation_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Calculation table visualization saved: {output_path}")
    plt.close()
