#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANGLE PROGRESSION VISUALIZATION MODULE
=====================================

Creates angle progression visualization showing how geometric angles change
across measurement points.

Author: I-Scan Team
Version: 3.0 (Pure geometry implementation)
"""

import matplotlib.pyplot as plt
import os
from config import OUTPUT_DIR, ensure_output_dir


def create_angle_progression_visualization(angles_data):
    """
    Creates angle progression visualization showing how geometric angles change
    across scanner movement points.
    
    Args:
        angles_data: List of angle calculation dictionaries
    """
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle('GEOMETRIC ANGLE PROGRESSION ACROSS MEASUREMENT POINTS', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    ax = plt.subplot(1, 1, 1)
    ax.set_title('Pure Geometric Angles Along Scan Path', 
                 fontsize=12, fontweight='bold', pad=20, color='darkblue')
    
    # Extract data
    y_positions = [data['y_pos'] for data in angles_data]
    geometric_angles = [data['angle'] for data in angles_data]
    
    # Plot line - show geometric angles
    ax.plot(y_positions, geometric_angles, 'o-', color='#2E86AB', 
            linewidth=3, markersize=10, markeredgewidth=2, 
            markeredgecolor='white', label='Geometric Angles')
    
    ax.set_xlabel('Y-Position (cm)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Angle (°)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.4, linestyle='--')
    ax.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    ax.set_facecolor('#f8f9fa')
    
    # Annotations
    for i, (y_pos, angle) in enumerate(zip(y_positions, geometric_angles)):
        ax.annotate(f'{angle:.1f}°', (y_pos, angle), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=8, fontweight='bold', color='#2E86AB')
    
    # Add info text
    info_text = f"""📊 GEOMETRIC ANGLE PROGRESSION
    
Scanner moves vertically from Y=0 to Y={max(y_positions):.0f} cm
Target object at fixed position
Angles calculated using pure trigonometry: atan2(dx, dy)
All angles measured from Y-axis"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, '02_angle_progression.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Angle progression visualization saved: {output_path}")
    plt.close()
