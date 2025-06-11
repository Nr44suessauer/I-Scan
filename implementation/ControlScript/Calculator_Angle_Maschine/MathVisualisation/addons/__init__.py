#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADD-ONS PACKAGE FOR MATHVISUALISATION
====================================

This package contains optional add-on features and extended explanations
that are not part of the core functionality.

Core features (01-07):
- Geometric representation
- Angle progression  
- Trigonometry formulas
- Point calculations
- Calculation table
- Servo interpolation
- Servo cone detail

Add-on features (08+):
- Target coordinate angle explanation (educational)

Author: I-Scan Team
Version: 1.0
"""

# Optional imports - fail gracefully if dependencies are missing
try:
    from .target_coord_angle_explanation import (
        explain_target_coord_angle_calculation,
        create_target_coord_angle_visualization,
        save_target_coord_angle_visualization
    )
    TARGET_COORD_ADDON_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Target coordinate add-on not available: {e}")
    TARGET_COORD_ADDON_AVAILABLE = False

__all__ = [
    'TARGET_COORD_ADDON_AVAILABLE',
]

if TARGET_COORD_ADDON_AVAILABLE:
    __all__.extend([
        'explain_target_coord_angle_calculation',
        'create_target_coord_angle_visualization', 
        'save_target_coord_angle_visualization'
    ])
