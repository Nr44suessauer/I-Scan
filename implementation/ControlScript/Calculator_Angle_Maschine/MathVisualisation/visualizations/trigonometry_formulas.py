#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIGONOMETRY FORMULAS VISUALIZATION MODULE
==========================================

Creates visualization explaining the trigonometric formulas used 
in the servo angle calculation.

Author: I-Scan Team
Version: 2.0 (Modular split from complete_servo_angle_explanation.py)
"""

import matplotlib.pyplot as plt
import os
from config import OUTPUT_DIR, ensure_output_dir
from config import ANGLE_CORRECTION_REFERENCE, TARGET_CENTER_X, TARGET_CENTER_Y


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
    ax.set_facecolor('#f8f9fa')
    
    # Formula text
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
    
    ax.text(0.05, 0.95, formula_text, transform=ax.transAxes, fontsize=12,            verticalalignment='top', fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", 
                     edgecolor='orange', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    ensure_output_dir()
    output_path = os.path.join(OUTPUT_DIR, '03_trigonometry_formulas.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    print(f"📊 Trigonometry formulas visualization saved: {output_path}")
    plt.close()
