# Calculator_Angle_Maschine – Mathematical Engine & Visualization

**Author:** Marc Nauendorf  
**Project Start:** 2023–2025

---

## Overview

Calculator_Angle_Maschine is the mathematical core of the I-Scan system. It computes all relevant servo and stepper angles, generates CSV command lists for automated scans, and creates extensive visualizations for analysis and documentation of scan geometry.

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

## Commands & CLI Options

### Standard Execution (Full Analysis)
```bash
python main.py
```
- All visualizations and CSV are generated.

### CSV Export (Silent/Batch)
```bash
python main.py --csv --csv-name <name> --target-x <x> --target-y <y> --scan-distance <d> --measurements <n>
```
- Only CSV and minimal console output (for automation/batch).

### Visualization Only
```bash
python main.py --visualize --target-x <x> --target-y <y> --scan-distance <d> --measurements <n>
```
- Only PNG visualizations, no CSV.

### Mathematical Analysis (No Graphics)
```bash
python main.py --math --csv-name <name> --servo-min <min> --servo-max <max> --servo-neutral <neutral>
```
- Only mathematical evaluation and CSV.

### Help
```bash
python main.py --help
```
- Shows all available parameters and options.

---

## Important Parameters

- `--csv-name`      Name of the CSV file (without extension)
- `--target-x/y`    Target coordinates (cm)
- `--scan-distance` Total scan distance (cm)
- `--measurements`  Number of measurement points
- `--servo-min/max/neutral` Servo limits (°)

---

## Visualizations (Examples)

1. **01_geometric_representation.png** – Geometry & scan path
2. **02_angle_progression.png** – Angle progression
3. **05_calculation_table.png** – Results table
4. **06_servo_interpolation.png** – Interpolation curve
5. **06_servo_geometry_graph_only.png** – Servo cone
6. **point_calculations/** – Single point analyses

---

## Example: Results Table (ASCII)

```
+---------+----------+-----------+-----------+----------+
| Point # |   Y [cm] |  Exact α  | Interpol. | Feasible?|
+---------+----------+-----------+-----------+----------+
|   1     |   0.0    |   65°     |   90°     |   ✓      |
|   2     |  23.3    |   90°     |   60°     |   ✓      |
|   3     |  46.7    |   65°     |   30°     |   ✓      |
|   4     |  70.0    |   47°     |    0°     |   ✗      |
+---------+----------+-----------+-----------+----------+
```

---

## Extensibility

- New mathematical models: Add to `calculations.py`
- New visualizations: Add as a module in `visualizations/`
- New export formats: Extend `export_commands.py`
- Parameters/presets: Adjust in `config.py`

---

## Support & Notes

- For integration into the GUI, see the README in the main directory and in `Software_IScan/`.
- For questions: See source code comments or contact in the main project.

---

**This module is the mathematical backbone of the I-Scan system and can be used independently or as an integrated component.**
