# Servo Angle Calculation - Modular Structure

This project has been refactored from a single 791-line file into a modular structure for better maintainability and reusability.

## File Structure

```
MathVisualisation/
├── README.md                                    # This documentation
├── complete_servo_angle_explanation.py         # Original file (791 lines)
├── complete_servo_angle_explanation_backup.py  # Backup of original file
├── config.py                                   # Configuration constants
├── calculations.py                              # Mathematical calculation functions
├── main.py                                      # Main coordinator with multiple entry points
└── visualizations/                              # Visualization package
    ├── __init__.py                             # Package initialization
    ├── geometric.py                            # Geometric representation
    ├── angle_progression.py                    # Angle progression visualization
    ├── trigonometry_formulas.py                # Formula explanations
    ├── point_calculation.py                    # Individual point calculations
    ├── calculation_table.py                    # Summary table
    └── complete.py                             # Comprehensive visualization
```

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
