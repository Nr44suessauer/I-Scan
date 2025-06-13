# Calculator_Angle_Maschine – Mathematical Engine & Visualization

**Author:** Marc Nauendorf  
**Email:** marc.nauendorf@hs-heilbronn.de  
**Website:** DeadlineDriven.dev

**Version:** 3.0 - Simplified Transformation & Enhanced Performance

---

## Overview

Calculator_Angle_Maschine is the mathematical core of the I-Scan system. It computes all relevant servo and stepper angles, generates CSV command lists for automated scans, and creates extensive visualizations for analysis and documentation of scan geometry.

### Features
- **Simplified Servo Transformation**: Intuitive `servo_angle = geometric_angle - neutral_angle` formula
- **Inverted Neutral Logic**: Entering -45° rotates cone by +45° (more intuitive)
- **Performance Optimization**: Optional point calculation graphs for faster processing
- **Enhanced CLI**: Complete parameter control via command line
- **User-Configurable Defaults**: All servo parameters configurable in real-time

---

## Mathematical Principles

### Coordinate Transformation
- **Simplified Formula**: `servo_angle = geometric_angle - neutral_angle`
- **Inverted Neutral Logic**: Negative input values produce positive cone rotation
- **Example**: 
  - Input: `neutral_angle = -45°` → Cone rotates +45°
  - Input: `neutral_angle = 45°` → Cone rotates -45°
  - Input: `neutral_angle = 0°` → No rotation

### Angle Calculation Methods
- **Linear Interpolation:**
  - Servo angles calculated linearly between reference points
  - Formula: `angle = MIN_SERVO_ANGLE + progress × (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE)`
  - Progress: `progress = y_position / SCAN_DISTANCE`

- **Trigonometric Calculation:**
  - Exact angle between scanner and target point
  - Formula: `α = arctan(dx/dy)`

- **Dual Mode Comparison:**
  - Both methods calculated and compared
  - Visualizes feasibility and deviations
  - Points outside servo cone automatically filtered

---

## Configuration System

### Servo Parameters (User-Configurable)
```python
SERVO_MIN_ANGLE = 0.0      # Minimum servo angle (degrees)
SERVO_MAX_ANGLE = 90.0     # Maximum servo angle (degrees) 
SERVO_NEUTRAL_ANGLE = 45.0 # Neutral position - direct rotation angle for cone
```

### Scan Configuration
```python
TARGET_CENTER_X = 50       # X-position of target object (cm)
TARGET_CENTER_Y = 50       # Y-position of target object (cm)
SCANNER_MODULE_X = 0       # X-position of scanner (cm)
SCANNER_MODULE_Y = 0       # Y-position of scanner (cm)
SCAN_DISTANCE = 100        # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 10 # Number of measurement points
```

### Visualization Control
```python
ENABLE_VISUALIZATIONS = {
    'geometric_representation': True,  # 01_geometric_representation.png
    'point_calculations': False,       # 04_point_X_calculation.png (DISABLED for performance)
    'calculation_table': True,        # 05_calculation_table.png
    'servo_interpolation': True,      # 06_servo_interpolation.png
    'servo_cone_detail': True,        # 07_servo_cone_detail.png
}
```

---

## Project Structure

```
MathVisualisation/
├── main.py            # Central CLI & program logic
├── calculations.py    # Mathematical core functions
├── config.py          # Configuration parameters
├── export_commands.py # CSV export logic
├── save_servo_graph.py# Single graph export
├── visualizations/    # Visualization modules
│   ├── geometric.py
│   ├── angle_progression.py
│   ├── calculation_table.py
│   ├── point_calculation.py
│   └── servo_interpolation.py
├── output/            # Generated PNGs & CSVs
│   ├── 01_geometric_representation.png
│   ├── ...
│   └── point_calculations/
└── README.md          # This documentation
```

---

## Mathematical Principles

- **Linear Interpolation:**
  - Servo angles are calculated linearly between two reference points (e.g., Y=0cm → 90°, Y=70cm → 0°).
  - Formula:  
    `angle = MIN_SERVO_ANGLE + progress × (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE)`
    with `progress = y_position / SCAN_DISTANCE`
- **Trigonometric Calculation:**
  - Exact calculation of the angle between scanner and target point:
    `α = arctan(dx/dy)`
- **Dual Mode:**
  - Both methods are calculated and compared to visualize feasibility and deviations.
- **Feasibility Check:**
  - Points outside the servo cone are automatically filtered.

---

## Data Flow & Integration

```
+-----------------------------+
| main.py (CLI/GUI wrapper)   |
+-----------------------------+
        |
        v
+-----------------------------+
| calculations.py             |
| config.py                   |
+-----------------------------+
        |
        v
+-----------------------------+
| visualizations/             |
| export_commands.py          |
+-----------------------------+
        |
        v
+-----------------------------+
| output/ (PNGs, CSVs)        |
+-----------------------------+
```

---

## Commands & CLI Options (Enhanced)

### Standard Execution (Full Analysis)
```bash
python main.py
```
- All enabled visualizations and CSV are generated
- Uses default configuration values

### CSV Export (Silent/Batch Mode)
```bash
python main.py --csv --csv-name custom_scan
python main.py --silent --csv-name production_scan
```
- Only CSV generation with minimal console output
- Perfect for automation and batch processing

### Visualization Mode
```bash
python main.py --visualize
python main.py --visualisation  # Alternative spelling
```
- Creates all enabled visualizations
- Updates output directory with latest graphs

### Configuration Override
```bash
python main.py --servo-min 0 --servo-max 90 --servo-neutral 45
python main.py --target-x 30 --target-y 40 --scan-distance 80 --measurements 15
python main.py --csv --servo-neutral -45 --target-x 60
```

### Complete Example
```bash
python main.py --visualize --csv-name research_scan_01 \
  --target-x 30 --target-y 50 --scan-distance 80 --measurements 20 \
  --servo-min 10 --servo-max 80 --servo-neutral -30
```

### Command Reference
```
OPTIONS:
  (no flags)             Full analysis with visualizations
  --csv, -c             Full analysis + CSV export  
  --visualize, -v       Create all visualizations (with custom config)
  --visualisation       Alternative spelling for --visualize
  --math, -m            Mathematics + CSV only (no visualizations)
  --silent, -s          Silent math + CSV (minimal output)
  --servo-graph, -g     Save only servo geometry graph
  --help, -h            Show complete help

CONFIGURATION OPTIONS:
  --target-x VALUE      Set target X position (cm) [default: 50]
  --target-y VALUE      Set target Y position (cm) [default: 50]
  --scanner-x VALUE     Set scanner X position (cm) [default: 0]
  --scanner-y VALUE     Set scanner Y position (cm) [default: 0]
  --scan-distance VALUE Set scan distance (cm) [default: 100]
  --measurements VALUE  Set number of measurements [default: 10]
  --servo-min VALUE     Set servo minimum angle (°) [default: 0.0]
  --servo-max VALUE     Set servo maximum angle (°) [default: 90.0]
  --servo-neutral VALUE Set servo neutral angle (°) [default: 45.0]
  --csv-name VALUE      Set custom CSV filename [default: timestamp]
```

---

## Output Files & Structure

### Generated Visualizations
```
output/
├── 01_geometric_representation.png    # Scanner geometry overview
├── 05_calculation_table.png           # Numerical results table
├── 06_servo_interpolation.png         # Servo angle progression
├── 07_servo_cone_detail.png          # Detailed cone analysis
├── iscan_commands_YYYY-MM-DD_HH-MM-SS.csv  # Generated commands
└── point_calculations/                # Individual point analyses (optional)
    ├── 04_point_1_calculation.png
    ├── 04_point_2_calculation.png
    └── ...
```

### CSV Command Format
```csv
device,command,value
servo,set_angle,45.5
stepper,move_steps,100
led,set_brightness,80
servo,set_angle,42.3
...
```

---

## Integration with Software_IScan

### Real-Time Parameter Control
- GUI passes all servo parameters via command line
- Configuration updated dynamically without file editing
- Real-time command preview in GUI

### Workflow Integration
```
GUI Input → CLI Parameters → Mathematical Engine → CSV/Visualizations → GUI Display
```

### Example Integration Call
```bash
# Called by Software_IScan GUI
python main.py --visualize --csv-name gui_generated_scan \
  --target-x 45 --target-y 55 --scan-distance 90 --measurements 12 \
  --servo-min 5 --servo-max 85 --servo-neutral 40
```

---

## Performance Optimization

### Disabled Features (for Speed)
- **Point Calculations**: Individual point graphs disabled by default
- **Optional Visualizations**: Only essential graphs generated
- **Silent Mode**: Minimal console output for batch processing

### Enable All Features
```python
# In config.py - for detailed analysis
ENABLE_VISUALIZATIONS = {
    'geometric_representation': True,
    'point_calculations': True,        # Enable for detailed analysis
    'calculation_table': True,
    'servo_interpolation': True,
    'servo_cone_detail': True,
}

VISUALIZATION_SETTINGS = {
    'save_individual_point_calculations': True,  # Enable individual point graphs
}
```

---

## Troubleshooting & Tips

### Common Issues
- **Missing Visualizations**: Check `ENABLE_VISUALIZATIONS` in config.py
- **CSV Not Generated**: Ensure write permissions in output directory
- **Servo Angles Out of Range**: Verify min/max angle parameters
- **Performance Issues**: Disable point calculations for faster processing

### Best Practices
- Use `--silent` mode for automated/batch processing
- Enable point calculations only when detailed analysis is needed
- Use custom CSV names for organized file management
- Test configuration with `--visualize` before production runs

---

**This module is the mathematical backbone of the I-Scan system and can be used independently or as an integrated component.**
