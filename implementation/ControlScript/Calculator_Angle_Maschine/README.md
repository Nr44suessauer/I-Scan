# Calculator Angle Machine - Servo Angle Calculator

This module provides precise servo angle calculations for the I-Scan 3D scanner positioning system. 
It calculates optimal servo angles based on geometric positioning and generates scan operation sequences.

## Scripts

### `calculator_simplified.py`
Simplified calculation engine with basic visualization.

### `calculator_Angle_IScan.py`
Comprehensive calculation and visualization engine with the following components:

#### Functions

- **`calculate_angle(current_y)`**: Calculates geometric angle using `angle = 90° - arctan(dy/dx)`
- **`calculate_approximated_angle(current_y)`**: Applies servo hardware constraints (0-90°)
- **`calculate_step_size()`**: Computes distance between measurement points
- **`generate_results_table()`**: Main execution function - generates tables, CSV, and visualizations
- **`main()`**: Entry point with dependency checking

#### Execution Flow

1. **Initialize**: Load configuration, validate parameters
2. **Calculate**: For each measurement point - compute angles and coordinates  
3. **Output**: Generate console table, CSV file, and 6-panel visualization
4. **Save**: Files saved to `ScanConfigs/` directory

#### Hardware Integration

- **Stepper Motor**: 28BYJ-48 specifications, `steps = (distance_mm / circumference) * 4096`
- **CSV Format**: JSON parameters for servo, photo, stepper operations compatible with main.py

## Configuration

```python
SERVO_ANGLE_MIN/MAX = 0/90    # Servo constraints (degrees)
NEW_CENTER_X/Y = 50/0         # Target center coordinates  
Z_MODULE_X/Y = 0/0            # Z-module start position
DELTA_SCAN = 70               # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 4    # Measurement points
```

## Usage

```bash
python calculator_Angle_IScan.py    # Full version with visualizations
python calculator_simplified.py     # Simplified version
```

**Output Files:**
- `angle_table_*_approximated.csv` - Operation sequence for main.py
- `scan_visualization_approximated.png` - Visualization plots

**CSV Format:**
```csv
type,params,description
servo,"{\"angle\": 85}","Set servo to 85°"
photo,{},"Take photograph"
stepper,"{\"steps\": 146, \"direction\": 1, \"speed\": 80}","Move stepper motor"
```

## Dependencies

```bash
pip install pandas tabulate matplotlib numpy
```

## Mathematical Model

Angle calculation: `angle = 90° - arctan(dy/dx)` where Y=0 gives 90°, increasing Y approaches 0°.


