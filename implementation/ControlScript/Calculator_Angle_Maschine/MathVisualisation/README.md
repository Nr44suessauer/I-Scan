# 3D Scanner Geometric Angle Calculation System

This project provides comprehensive geometric angle calculations and visualizations for a 3D scanner servo system, organized in a modular structure with core features and optional add-ons.

## 📁 Project Structure

```
MathVisualisation/
├── README.md                          # This documentation
├── config.py                          # Configuration constants & visualization controls
├── calculations.py                    # Core mathematical calculation functions
├── servo_interpolation.py             # Servo angle interpolation
├── main.py                           # Main coordinator with multiple entry points
├── addons/                           # 🎓 Optional add-on features
│   ├── README.md                     # Add-on documentation
│   ├── __init__.py                   # Add-on package initialization
│   ├── target_coord_angle_explanation.py  # Educational explanations
│   └── target_coord_explanation/     # Enhanced visualization modules
├── visualizations/                   # 📊 Core visualization package
│   ├── __init__.py                   # Package initialization
│   ├── geometric.py                  # Geometric representation (01)
│   ├── angle_progression.py          # Angle progression visualization (02)
│   ├── point_calculation.py          # Individual point calculations (04)
│   ├── calculation_table.py          # Summary table (05)
│   └── servo_interpolation.py        # Servo visualizations (06-07)
└── output/                           # Generated PNG visualizations
```

## 🎯 Feature Overview

### 📊 **CORE FEATURES (01-06)** - Always Available
1. **01_geometric_representation.png** - Scanner setup and measurement points
2. **02_angle_progression.png** - How angles change with scanner position  
3. **04_point_X_calculation.png** - Detailed calculations for each point (6 files)
4. **05_calculation_table.png** - Summary table of all results
5. **06_servo_interpolation.png** - Servo angle interpolation
6. **07_servo_cone_detail.png** - Detailed servo cone analysis

### 🎓 **ADD-ON FEATURES (08+)** - Optional Extensions
8. **08_target_coord_angle_explanation.png** - **Student-friendly educational explanation**

## Usage

### 1. Full Explanation Mode (Default)
```python
python main.py
```
- Shows step-by-step mathematical explanation
- Creates all visualizations
- Saves PNG files with detailed diagrams

### 2. Silent Visualization Mode
```python
from main import main_silent
main_silent()
```
- Creates only visualizations without text explanation
- Useful for generating diagrams programmatically

### 3. Calculation Only Mode
```python
from main import get_servo_angles
angles = get_servo_angles()
print(angles)
```
- Returns only the calculated servo angles as a list
- No console output or file generation
- Perfect for integration with other systems

## ⚙️ Configuration

Control which visualizations are generated in `config.py`:

```python
ENABLE_VISUALIZATIONS = {
    # CORE FEATURES (01-07) - Main functionality
    'geometric_representation': True,    # 01_geometric_representation.png
    'angle_progression': True,          # 02_angle_progression.png  
    'trigonometry_formulas': True,      # 03_trigonometry_formulas.png
    'point_calculations': True,         # 04_point_X_calculation.png
    'calculation_table': True,          # 05_calculation_table.png
    'servo_interpolation': True,        # 06_servo_interpolation.png
    'servo_cone_detail': True,          # 07_servo_cone_detail.png
    
    # ADD-ON FEATURES (08+) - Optional educational extensions
    'target_coord_angle_explanation': False,  # 08 (Add-on, disabled by default)
}
```

### Enable Add-on Features
```python
# To enable the educational add-on
ENABLE_VISUALIZATIONS['target_coord_angle_explanation'] = True
```

## Module Descriptions

### `config.py`
- Contains all configuration constants
- Scanner positions, target coordinates
- Matplotlib settings for consistent styling

### `calculations.py`
- `print_step_by_step_explanation()`: Detailed console output with calculations
- `calculate_servo_angles()`: Silent calculation function returning results

### `visualizations/` Package
Each visualization module is self-contained:
- **geometric.py**: Shows scanner setup and measurement points
- **angle_progression.py**: Displays how angles change with position
- **trigonometry_formulas.py**: Explains the mathematical formulas used
- **point_calculation.py**: Detailed breakdown for each measurement point
- **calculation_table.py**: Summary table of all results
- **complete.py**: Comprehensive view combining all elements

### `main.py`
Main coordinator providing three entry points:
- `main()`: Full explanation with visualizations
- `main_silent()`: Only visualizations
- `get_servo_angles()`: Only calculations

## Benefits of Modular Structure

1. **Maintainability**: Each component can be modified independently
2. **Reusability**: Import only the functions you need
3. **Testing**: Each module can be tested separately
4. **Extensibility**: Easy to add new visualization types
5. **Integration**: Clean API for use in larger systems

## Generated Output Files

The system creates an `output/` directory and saves 9 PNG visualization files there:
- `output/01_geometric_representation.png`
- `output/02_angle_progression.png`
- `output/03_trigonometry_formulas.png`
- `output/04_point_1_calculation.png`
- `output/04_point_2_calculation.png`
- `output/04_point_3_calculation.png`
- `output/04_point_4_calculation.png`
- `output/05_calculation_table.png`
- `output/06_complete_servo_angle_visualization.png`

The output directory is automatically created if it doesn't exist.

## Integration Example

```python
# Use in your own project
from main import get_servo_angles
from visualizations.geometric import create_geometric_visualization

# Get calculation results
servo_angles = get_servo_angles()

# Generate specific visualization
create_geometric_visualization()

# Access individual angle data
for angle_data in servo_angles:
    print(f"Point {angle_data['point']}: {angle_data['final']:.2f}°")
```

The modular structure maintains 100% compatibility with the original functionality while providing enhanced flexibility for development and integration.
