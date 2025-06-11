# ADD-ONS DIRECTORY
==================

This directory contains **optional add-on features** that extend the core functionality of the MathVisualisation system.

## 🎯 CORE vs ADD-ON Features

### 📊 **CORE FEATURES (01-07)** - Always Available
These are the main visualizations that form the essential functionality:

1. **01_geometric_representation.png** - Basic geometric setup
2. **02_angle_progression.png** - Angle progression analysis  
3. **03_trigonometry_formulas.png** - Mathematical formulas
4. **04_point_X_calculation.png** - Individual point calculations (6 files)
5. **05_calculation_table.png** - Summary table
6. **06_servo_interpolation.png** - Servo interpolation
7. **07_servo_cone_detail.png** - Servo cone analysis

### 🎓 **ADD-ON FEATURES (08+)** - Optional Extensions
These are educational extensions and specialized tools:

8. **08_target_coord_angle_explanation.png** - **Student-friendly educational explanation**

## 📁 ADD-ON Structure

```
addons/
├── __init__.py                           # Add-on package initialization
├── target_coord_angle_explanation.py    # Educational target coordinate explanation
└── target_coord_explanation/            # Enhanced visualization modules
    ├── target_coord_angle_explanation_new.py
    └── debug_target_coord_angle.py
```

## ⚙️ Configuration

Add-ons are controlled in `config.py`:

```python
# Core features - always enabled in main functionality
ENABLE_VISUALIZATIONS = {
    'geometric_representation': True,     # Core
    'angle_progression': True,            # Core
    # ... other core features
    
    # Add-on features - optional
    'target_coord_angle_explanation': False,  # Add-on (disabled by default)
}

# Add-on specific settings
ADDON_SETTINGS = {
    'enable_educational_extensions': True,
    'fallback_to_basic_on_error': True,
    'show_addon_status_messages': True,
}
```

## 🎨 Usage

### Enable Add-on
```python
# In config.py
ENABLE_VISUALIZATIONS['target_coord_angle_explanation'] = True
```

### Import Add-on
```python
# Graceful import with fallback
try:
    from addons import TARGET_COORD_ADDON_AVAILABLE
    if TARGET_COORD_ADDON_AVAILABLE:
        from addons.target_coord_angle_explanation import save_target_coord_angle_visualization
except ImportError:
    # Add-on not available - continue with core features only
    pass
```

## 🔧 Creating New Add-ons

1. **Create your add-on module** in this directory
2. **Add import to `__init__.py`** with graceful error handling
3. **Add configuration option** in `config.py`
4. **Update main.py** with optional import and execution
5. **Document your add-on** in this README

## 📝 Design Philosophy

- **Core features** (01-07) should always work and be reliable
- **Add-ons** (08+) are optional enhancements that can fail gracefully
- **Educational add-ons** provide student-friendly explanations
- **Specialized add-ons** offer advanced analysis for specific use cases
- **Graceful degradation** - system works even if add-ons fail

---
*This structure ensures the core system remains stable while allowing for educational and specialized extensions.*
