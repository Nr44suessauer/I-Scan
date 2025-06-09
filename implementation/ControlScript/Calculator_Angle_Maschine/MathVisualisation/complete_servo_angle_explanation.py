#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPLETE SERVO ANGLE EXPLANATION AND VISUALIZATION
=================================================

This script explains step by step the mathematical calculation 
of servo angles for the 3D scanner and creates detailed visualizations.

OPTIMIZATIONS:
- Avoided overlaps between text and diagrams
- Improved layout alignment with optimized spacing
- High-resolution PNG output (300 DPI)
- Professional color scheme and typography

Author: I-Scan Team
Version: 2.0 (English translation with individual visualizations)
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import os

# Configure matplotlib for clean, high-resolution images
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 8
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# === 3D SCANNER CONFIGURATION ===
TARGET_CENTER_X = 50      # X-position of target object (cm)
TARGET_CENTER_Y = 15       # Y-position of target object (cm) 
SCANNER_MODULE_X = 0      # X-position of scanner (cm)
SCANNER_MODULE_Y = 0      # Y-position of scanner (cm)
SCAN_DISTANCE = 50       # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 4  # Number of measurement points
ANGLE_CORRECTION_REFERENCE = 60  # Mechanical correction (degrees)

def print_step_by_step_explanation():
    """
    Prints a detailed step-by-step explanation of the calculation
    """
    print("=" * 80)
    print("   SERVO ANGLE CALCULATION - COMPLETE EXPLANATION")
    print("=" * 80)
    print()
    
    print("🎯 PROBLEM:")
    print("   A 3D scanner moves vertically and must always point at a")
    print("   target object. For this, servo angles must be calculated.")
    print()
    
    print("📊 SETUP:")
    print(f"   • Scanner starts at: ({SCANNER_MODULE_X}, {SCANNER_MODULE_Y}) cm")
    print(f"   • Target object is at: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm") 
    print(f"   • Scanner moves {SCAN_DISTANCE} cm vertically")
    print(f"   • {NUMBER_OF_MEASUREMENTS} measurement points are calculated")
    print()
      # Step 1: Calculate step size
    step_size = SCAN_DISTANCE / (NUMBER_OF_MEASUREMENTS - 1)
    print("📏 STEP 1: Calculate step size")
    print("   " + "-" * 45)
    print(f"   Formula: Step size = Total distance ÷ (Number of measurements - 1)")
    print(f"   Step size = {SCAN_DISTANCE} cm ÷ ({NUMBER_OF_MEASUREMENTS} - 1)")
    print(f"   Step size = {step_size:.2f} cm")
    print(f"   → Each measurement point is {step_size:.2f} cm apart")
    print("   → This ensures the last measurement is at the full scan distance")
    print()
    
    # Step 2: Trigonometry for each point
    print("🧮 STEP 2: Trigonometric calculation for each measurement point")
    print("   " + "-" * 65)
    print()
    
    angles = []
    for i in range(NUMBER_OF_MEASUREMENTS):
        y_position = i * step_size
        
        print(f"   📍 MEASUREMENT POINT {i+1} (Y = {y_position} cm):")
        print("   " + "~" * 35)
        
        # Calculate triangle sides
        dx = TARGET_CENTER_X - SCANNER_MODULE_X
        dy = abs(y_position - TARGET_CENTER_Y)
        
        print(f"   • Horizontal distance (dx): {TARGET_CENTER_X} - {SCANNER_MODULE_X} = {dx} cm")
        print(f"   • Vertical distance (dy): |{y_position} - {TARGET_CENTER_Y}| = {dy} cm")
        
        # Trigonometric calculation
        if dx > 0.001:  # Avoid division by zero
            alpha_rad = math.atan(dy / dx)
            alpha_deg = alpha_rad * 180 / math.pi
            theoretical_angle = 90.0 - alpha_deg
        else:
            alpha_deg = 0.0
            theoretical_angle = 90.0
            
        print(f"   • Angle α = arctan(dy/dx) = arctan({dy}/{dx}) = {alpha_deg:.2f}°")
        print(f"   • Theoretical servo angle = 90° - α = 90° - {alpha_deg:.2f}° = {theoretical_angle:.2f}°")
        
        # Mechanical correction
        corrected_angle = theoretical_angle + (ANGLE_CORRECTION_REFERENCE - 90.0)
        print(f"   • Correction = {ANGLE_CORRECTION_REFERENCE} - 90 = {ANGLE_CORRECTION_REFERENCE - 90}°")
        print(f"   • Final servo angle = {theoretical_angle:.2f}° + {ANGLE_CORRECTION_REFERENCE - 90}° = {corrected_angle:.2f}°")
        
        angles.append({
            'point': i+1,
            'y_pos': y_position,
            'dx': dx,
            'dy': dy,
            'alpha': alpha_deg,
            'theoretical': theoretical_angle,
            'final': corrected_angle
        })
        
        print()
    
    print("📋 SUMMARY OF ALL CALCULATED ANGLES:")
    print("   " + "-" * 50)
    print("   Point | Y-Pos | dx   | dy   | α      | Theo° | Final°")
    print("   ------|-------|------|------|--------|-------|-------")
    for angle in angles:
        print(f"     {angle['point']}   | {angle['y_pos']:5.1f} | {angle['dx']:4.0f} | {angle['dy']:4.1f} | {angle['alpha']:6.2f} | {angle['theoretical']:5.1f} | {angle['final']:6.1f}")
    
    print()
    print("✅ CALCULATION COMPLETED!")
    print("   The servo angles are ready for hardware control.")
    print()
    
    return angles

def create_geometric_visualization(angles_data):
    """
    Creates geometric representation visualization
    """
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('white')
    fig.suptitle('GEOMETRIC REPRESENTATION OF 3D SCANNER SYSTEM', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    ax = plt.subplot(1, 1, 1)
    ax.set_title('Scanner Movement Path and Target Positioning', 
                 fontsize=12, fontweight='bold', pad=20, color='darkblue')
    
    # Setup axes
    ax.set_xlim(-25, 90)
    ax.set_ylim(-15, 80)
    ax.grid(True, alpha=0.3, linewidth=0.6, linestyle='--')
    ax.set_aspect('equal')
    ax.set_xlabel('X-Position (cm)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y-Position (cm)', fontsize=10, fontweight='bold')
    ax.set_facecolor('#f8f9fa')
    
    # Coordinate system
    ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.8)
    ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.8)
    
    # Scanner path
    scan_y = np.linspace(0, SCAN_DISTANCE, 100)
    ax.plot([SCANNER_MODULE_X] * len(scan_y), scan_y, 'g-', 
            linewidth=8, alpha=0.6, label='Scanner Movement Path', solid_capstyle='round')
      # Target object
    ax.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'bs', markersize=16, 
            markeredgewidth=3, markeredgecolor='navy', zorder=10)
    ax.text(TARGET_CENTER_X + 5, TARGET_CENTER_Y - 3, f'TARGET OBJECT\n({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm', 
            ha='left', va='top', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor="lightblue", 
                     edgecolor='navy', linewidth=1.5, alpha=0.95))
    
    # Measurement points
    colors = ['#FF4444', '#FF8800', '#8844FF', '#AA4400']
    marker_styles = ['o', 's', '^', 'D']
    
    for i, data in enumerate(angles_data):
        color = colors[i % len(colors)]
        marker = marker_styles[i % len(marker_styles)]
        y_pos = data['y_pos']
        
        # Measurement point
        ax.plot(SCANNER_MODULE_X, y_pos, marker, color=color, markersize=12, 
               markeredgewidth=2, markeredgecolor='black', zorder=8)
        
        # Sight lines to target
        ax.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [y_pos, TARGET_CENTER_Y], 
                '--', color=color, linewidth=2, alpha=0.7, zorder=3)
        
        # Point labels
        ax.text(SCANNER_MODULE_X - 12, y_pos, 
                f'P{data["point"]}\nY={y_pos:.1f}\nS={data["final"]:.1f}°', 
                ha='right', va='center', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, 
                         edgecolor='black', linewidth=1, alpha=0.9))
    
    ax.legend(fontsize=10, loc='upper right', frameon=True, 
              fancybox=True, shadow=True, framealpha=0.9)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '01_geometric_representation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Geometric visualization saved: {output_path}")
    plt.close()

def create_angle_progression_visualization(angles_data):
    """
    Creates angle progression visualization
    """
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle('SERVO ANGLE PROGRESSION OVER SCAN POSITION', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    ax = plt.subplot(1, 1, 1)
    ax.set_title('Theoretical vs Corrected Servo Angles', 
                 fontsize=12, fontweight='bold', pad=20, color='darkblue')
    
    y_positions = [data['y_pos'] for data in angles_data]
    final_angles = [data['final'] for data in angles_data]
    theoretical_angles = [data['theoretical'] for data in angles_data]
    
    # Plot lines
    line1 = ax.plot(y_positions, theoretical_angles, 'o-', color='#2E86AB', 
                    linewidth=3, markersize=8, markeredgewidth=2, 
                    markeredgecolor='white', label='Theoretical Angles')
    line2 = ax.plot(y_positions, final_angles, 's-', color='#A23B72', 
                    linewidth=3, markersize=8, markeredgewidth=2, 
                    markeredgecolor='white', label='Corrected Angles')
    
    ax.set_xlabel('Y-Position (cm)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Servo Angle (°)', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.4, linestyle='--')
    ax.legend(fontsize=10, frameon=True, fancybox=True, shadow=True)
    ax.set_facecolor('#f8f9fa')
    
    # Annotate values at points
    for i, (y_pos, theo, final) in enumerate(zip(y_positions, theoretical_angles, final_angles)):
        ax.annotate(f'{theo:.1f}°', (y_pos, theo), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=8, fontweight='bold')
        ax.annotate(f'{final:.1f}°', (y_pos, final), textcoords="offset points", 
                    xytext=(0,-15), ha='center', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '02_angle_progression.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Angle progression visualization saved: {output_path}")
    plt.close()

def create_trigonometry_formulas_visualization():
    """
    Creates trigonometry formulas visualization
    """
    fig = plt.figure(figsize=(12, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle('TRIGONOMETRY FORMULAS FOR SERVO ANGLE CALCULATION', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    ax = plt.subplot(1, 1, 1)
    ax.set_title('Mathematical Foundation', 
                 fontsize=12, fontweight='bold', pad=20, color='darkblue')
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')    # Formula text
    formula_text = f"""TRIGONOMETRY FUNDAMENTALS:

• tan(α) = Opposite side ÷ Adjacent side
• tan(α) = dy ÷ dx
• α = arctan(dy ÷ dx)

SERVO ANGLE:
• Servo° = 90° - α

CORRECTION:
• Final° = Servo° + Correction
• Correction = {ANGLE_CORRECTION_REFERENCE - 90}°

MEASUREMENT SETUP:
• dx = Target X - Scanner X
• dy = |Scanner Y - Target Y|
• Scanner moves vertically along Y-axis
• Target remains fixed at ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm"""
    
    ax.text(0.05, 0.95, formula_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", 
                     edgecolor='orange', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '03_trigonometry_formulas.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Trigonometry formulas visualization saved: {output_path}")
    plt.close()

def create_point_calculation_visualization(point_data, point_number):
    """
    Creates individual point calculation visualization with coordinate system
    """
    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle(f'CALCULATION FOR MEASUREMENT POINT {point_number}', 
                 fontsize=16, fontweight='bold', y=0.95, color='navy')
    
    # Left side: Coordinate system with highlighted point
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_title(f'Coordinate System - Point {point_number}', 
                  fontsize=12, fontweight='bold', pad=20, color='darkblue')
    
    # Grid and axes
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-10, 110)
    ax1.set_ylim(-10, 110)
    ax1.set_xlabel('X Position (cm)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Y Position (cm)', fontsize=10, fontweight='bold')
    ax1.set_aspect('equal')
    
    # Scanner path
    scan_y = np.linspace(0, SCAN_DISTANCE, 100)
    ax1.plot([SCANNER_MODULE_X] * len(scan_y), scan_y, 'g-', 
             linewidth=6, alpha=0.6, label='Scanner Path', solid_capstyle='round')
    
    # Target object
    ax1.plot(TARGET_CENTER_X, TARGET_CENTER_Y, 'bs', markersize=14, 
             markeredgewidth=2, markeredgecolor='navy', zorder=10)
    ax1.text(TARGET_CENTER_X + 3, TARGET_CENTER_Y - 2, f'TARGET\n({TARGET_CENTER_X}, {TARGET_CENTER_Y})', 
             ha='left', va='top', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", 
                      edgecolor='navy', linewidth=1, alpha=0.9))
    
    # Current measurement point (highlighted)
    ax1.plot(SCANNER_MODULE_X, point_data['y_pos'], 'ro', markersize=16, 
             markeredgewidth=3, markeredgecolor='darkred', zorder=15)
    ax1.text(SCANNER_MODULE_X - 8, point_data['y_pos'], f'POINT {point_number}\n(0, {point_data["y_pos"]:.1f})', 
             ha='right', va='center', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", 
                      edgecolor='red', linewidth=2, alpha=0.9))
    
    # Connection line (triangle visualization)
    ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [point_data['y_pos'], TARGET_CENTER_Y], 
             'r--', linewidth=3, alpha=0.8, label=f'Line to target')
    
    # Distance annotations
    mid_x = (SCANNER_MODULE_X + TARGET_CENTER_X) / 2
    mid_y = (point_data['y_pos'] + TARGET_CENTER_Y) / 2
    distance = math.sqrt(point_data['dx']**2 + point_data['dy']**2)
    ax1.text(mid_x, mid_y, f'{distance:.1f} cm', ha='center', va='bottom', 
             fontsize=8, fontweight='bold', rotation=point_data['alpha'],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", 
                      edgecolor='red', alpha=0.8))
    
    # Right angle visualization
    if point_data['dy'] > 0:  # Only show if there's a vertical distance
        # Horizontal line
        ax1.plot([SCANNER_MODULE_X, TARGET_CENTER_X], [point_data['y_pos'], point_data['y_pos']], 
                 'orange', linewidth=2, alpha=0.7)
        ax1.text(TARGET_CENTER_X/2, point_data['y_pos'] - 3, f'dx = {point_data["dx"]} cm', 
                 ha='center', va='top', fontsize=8, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="orange", alpha=0.7))
        
        # Vertical line
        ax1.plot([TARGET_CENTER_X, TARGET_CENTER_X], [point_data['y_pos'], TARGET_CENTER_Y], 
                 'purple', linewidth=2, alpha=0.7)
        ax1.text(TARGET_CENTER_X + 2, (point_data['y_pos'] + TARGET_CENTER_Y)/2, 
                 f'dy = {point_data["dy"]:.1f} cm', ha='left', va='center', fontsize=8, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="purple", alpha=0.7))
    
    ax1.legend(loc='upper left', fontsize=8)
    
    # Right side: Calculation text
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_title(f'Step-by-Step Calculation', 
                  fontsize=12, fontweight='bold', pad=20, color='darkblue')
    ax2.axis('off')
    ax2.set_facecolor('#f8f9fa')

    calculation_text = f"""STEP-BY-STEP CALCULATION:

Given:
• Scanner position: (0, {point_data['y_pos']:.1f}) cm
• Target position: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm

Calculation:
• dx = {TARGET_CENTER_X} - 0 = {point_data['dx']} cm
• dy = |{point_data['y_pos']:.1f} - {TARGET_CENTER_Y}| = {point_data['dy']:.1f} cm
• α = arctan({point_data['dy']:.1f}/{point_data['dx']}) = {point_data['alpha']:.2f}°
• Servo = 90° - {point_data['alpha']:.2f}° = {point_data['theoretical']:.2f}°
• Final = {point_data['theoretical']:.2f}° + ({ANGLE_CORRECTION_REFERENCE - 90}°) = {point_data['final']:.2f}°

RESULT:
• Final servo angle for point {point_number}: {point_data['final']:.2f}°

TRIANGLE PROPERTIES:
• Adjacent side (dx): {point_data['dx']} cm
• Opposite side (dy): {point_data['dy']:.1f} cm
• Hypotenuse: {math.sqrt(point_data['dx']**2 + point_data['dy']**2):.2f} cm
• Angle α: {point_data['alpha']:.2f}°"""
    
    ax2.text(0.05, 0.95, calculation_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.6", facecolor="lightcyan", 
                     edgecolor='teal', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), f'04_point_{point_number}_calculation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Point {point_number} calculation visualization saved: {output_path}")
    plt.close()

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
    ax.axis('off')
    
    # Prepare table data
    table_data = []
    headers = ['Point', 'Y-Position\n(cm)', 'dx\n(cm)', 'dy\n(cm)', 
               'Angle α\n(°)', 'Theoretical\n(°)', 'Final\n(°)']
    
    for data in angles_data:
        row = [
            f"P{data['point']}",
            f"{data['y_pos']:.1f}",
            f"{data['dx']:.0f}",
            f"{data['dy']:.1f}",
            f"{data['alpha']:.2f}",
            f"{data['theoretical']:.1f}",
            f"{data['final']:.1f}"
        ]
        table_data.append(row)
    
    # Create table
    table = ax.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.12, 0.15, 0.12, 0.12, 0.15, 0.15, 0.15])
    
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
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E8F4FD')
            else:
                table[(i, j)].set_facecolor('#FFFFFF')
            table[(i, j)].set_text_props(weight='bold', size=10)
            table[(i, j)].set_height(0.20)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '05_calculation_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Calculation table visualization saved: {output_path}")
    plt.close()

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
        
        # Point labeling compact
        ax1.text(SCANNER_MODULE_X - 12, y_pos, 
                 f'P{data["point"]}\nY={y_pos:.1f}\nS={data["final"]:.1f}°', 
                 ha='right', va='center', fontsize=7, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor=color, 
                          edgecolor='black', linewidth=1, alpha=0.9))
    
    # Legend compact
    ax1.legend(fontsize=8, loc='upper right', frameon=True, 
               fancybox=True, shadow=True, framealpha=0.9)

    # === DIAGRAM 2: Angle progression ===
    ax2 = plt.subplot2grid((5, 4), (0, 2), colspan=2, rowspan=1)
    ax2.set_title('Servo Angle Progression over Scan Position', 
                  fontsize=10, fontweight='bold', pad=15, color='darkblue')
    
    y_positions = [data['y_pos'] for data in angles_data]
    final_angles = [data['final'] for data in angles_data]
    theoretical_angles = [data['theoretical'] for data in angles_data]
    
    # Lines with compact markers
    line1 = ax2.plot(y_positions, theoretical_angles, 'o-', color='#2E86AB', 
                     linewidth=3, markersize=7, markeredgewidth=2, 
                     markeredgecolor='white', label='Theoretical Angles')
    line2 = ax2.plot(y_positions, final_angles, 's-', color='#A23B72', 
                     linewidth=3, markersize=7, markeredgewidth=2, 
                     markeredgecolor='white', label='Corrected Angles')
    
    ax2.set_xlabel('Y-Position (cm)', fontsize=9, fontweight='bold')
    ax2.set_ylabel('Servo Angle (°)', fontsize=9, fontweight='bold')
    ax2.grid(True, alpha=0.4, linestyle='--')
    ax2.legend(fontsize=8, frameon=True, fancybox=True, shadow=True)
    ax2.set_facecolor('#f8f9fa')
    
    # Show values at points with smaller font
    for i, (y_pos, theo, final) in enumerate(zip(y_positions, theoretical_angles, final_angles)):
        ax2.annotate(f'{theo:.1f}°', (y_pos, theo), textcoords="offset points", 
                     xytext=(0,8), ha='center', fontsize=6, fontweight='bold')
        ax2.annotate(f'{final:.1f}°', (y_pos, final), textcoords="offset points", 
                     xytext=(0,-12), ha='center', fontsize=6, fontweight='bold')

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

SERVO ANGLE:
• Servo° = 90° - α

CORRECTION:
• Final° = Servo° + Correction
• Correction = {ANGLE_CORRECTION_REFERENCE - 90}°"""
    
    ax3.text(0.03, 0.97, formula_text, transform=ax3.transAxes, fontsize=10,
             verticalalignment='top', fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", 
                      edgecolor='orange', linewidth=1, alpha=0.95))

    # === DIAGRAM 4: Example calculation ===
    ax4 = plt.subplot2grid((5, 4), (3, 2), colspan=2, rowspan=1)
    ax4.set_title('Example Calculation for Point 2', fontsize=12, fontweight='bold', 
                  pad=20, color='darkblue')
    ax4.axis('off')
    ax4.set_facecolor('#f8f9fa')

    # Example calculation for point 2 enlarged
    example_data = angles_data[1]  # Point 2
    example_text = f"""STEP-BY-STEP CALCULATION:

Given:
• Scanner: (0, {example_data['y_pos']:.1f}) cm
• Target: ({TARGET_CENTER_X}, {TARGET_CENTER_Y}) cm

Calculation:
• dx = {TARGET_CENTER_X} - 0 = {example_data['dx']} cm
• dy = |{example_data['y_pos']:.1f} - 0| = {example_data['dy']:.1f} cm
• α = arctan({example_data['dy']:.1f}/{example_data['dx']}) = {example_data['alpha']:.2f}°
• Servo = 90° - {example_data['alpha']:.2f}° = {example_data['theoretical']:.2f}°
• Final = {example_data['theoretical']:.2f}° + ({ANGLE_CORRECTION_REFERENCE - 90}°) = {example_data['final']:.2f}°"""
    
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
               'Angle α\n(°)', 'Theoretical\n(°)', 'Final\n(°)']
    
    for data in angles_data:
        row = [
            f"P{data['point']}",
            f"{data['y_pos']:.1f}",
            f"{data['dx']:.0f}",
            f"{data['dy']:.1f}",
            f"{data['alpha']:.2f}",
            f"{data['theoretical']:.1f}",
            f"{data['final']:.1f}"
        ]
        table_data.append(row)

    # Create table with compact design
    table = ax5.table(cellText=table_data, colLabels=headers,
                      cellLoc='center', loc='center',
                      colWidths=[0.12, 0.15, 0.12, 0.12, 0.15, 0.15, 0.15])
    
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
    output_path = os.path.join(os.path.dirname(__file__), '06_complete_servo_angle_visualization.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    
    print(f"📊 Complete visualization saved: {output_path}")
    
    # Show the diagram
    plt.show()

def main():
    """
    Main function - executes complete explanation and visualization
    """
    print("\n🚀 STARTING COMPLETE SERVO ANGLE EXPLANATION...\n")
    
    # Step 1: Mathematical explanation
    angles_data = print_step_by_step_explanation()
    
    print("🎨 CREATING VISUALIZATIONS...")
    print("   Please wait while diagrams are being generated...")
    
    # Step 2: Create individual visualizations
    create_geometric_visualization(angles_data)
    create_angle_progression_visualization(angles_data)
    create_trigonometry_formulas_visualization()
    
    # Create individual point calculations
    for i, point_data in enumerate(angles_data):
        create_point_calculation_visualization(point_data, i + 1)
    
    create_calculation_table_visualization(angles_data)
    
    # Step 3: Create complete visualization
    create_complete_visualization(angles_data)
    
    print("\n✅ COMPLETE ANALYSIS FINISHED!")
    print("   • Mathematical calculation explained")
    print("   • Individual visualizations created:")
    print("     - 01_geometric_representation.png")
    print("     - 02_angle_progression.png")
    print("     - 03_trigonometry_formulas.png")
    print("     - 04_point_1_calculation.png")
    print("     - 04_point_2_calculation.png")
    print("     - 04_point_3_calculation.png")
    print("     - 04_point_4_calculation.png")
    print("     - 05_calculation_table.png")
    print("     - 06_complete_servo_angle_visualization.png")
    print("   • Servo angles ready for hardware implementation")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
