# 3D Scanner Geometric Angle Calculator 📐

**Author:** Marc Nauendorf  
**Email:** marc.nauendorf@hs-heilbronn.de  
**Website:** deadlinedriven.dev  
**Version:** 4.0 - Complete Mathematics Engine with CSV Export

Comprehensive mathematics engine for 3D scanner control with advanced visualizations and Software_IScan integration.

## 🚀 Quick Start Examples

### Basic Usage
```bash
# Standard analysis with visualizations
python main.py

# Full analysis + CSV export for Software_IScan
python main.py --csv

# Mathematics + CSV only (no visualizations, faster)
python main.py --math

# Silent mode for automation
python main.py --silent
```

### Custom CSV Naming
```bash
# Custom CSV filename
python main.py --csv --csv-name my_scan_results

# Math mode with custom name
python main.py --math --csv-name production_scan

# Silent mode with custom name  
python main.py --silent --csv-name automated_scan
```

### Configuration Override Examples
```bash
# Original I-Scan setup recreation
python main.py --csv --target-x 33 --target-y 50 --scan-distance 80 --measurements 7

# Custom target with CSV export
python main.py --csv --csv-name custom_target --target-x 30 --target-y 50 --scan-distance 80 --measurements 5

# Quick custom scan
python main.py --math --target-x 100 --target-y 75 --measurements 5

# Custom servo parameters
python main.py --silent --servo-min 10 --servo-max 80 --servo-neutral 45

# Help and usage information
python main.py --help
```

## 🎯 System Concept

```
                3D SCANNER SYSTEM
    ┌─────────────────────────────────────────┐
    │  Scanner(0,0) ───────────► Target(33,50)│
    │      │                                  │
    │      ▼ 80cm scan distance               │
    │  ┌───────┐                              │
    │  │Point 1│ ◄── Calculate angles         │
    │  │Point 2│                              │
    │  │  ...  │                              │
    │  │Point 7│                              │
    │  └───────┘                              │
    └─────────────────────────────────────────┘
         ▼ PROCESSING FLOW ▼
    ┌─────────────────────────────────────────┐
    │ 1. Geometric Calculation                │
    │    atan2(dx,dy) → angle                 │
    │ 2. Servo Interpolation                  │
    │    angle + 45° + 180° → servo_angle     │
    │ 3. Visualization Generation             │
    │    PNG files in output/ + subfolder/    │
    └─────────────────────────────────────────┘
```

## 📂 Function Mapping

### CORE MODULE: `config.py`
```
🔧 ensure_output_dir()         ← Directory Management
📊 OUTPUT_DIR                  ← "output"
📁 POINT_CALCULATIONS_SUBDIR   ← "point_calculations"
⚙️  TARGET_CENTER_X/Y          ← Scanner Coordinates
📏 SCAN_DISTANCE               ← 80cm
🎛️  ENABLE_VISUALIZATIONS      ← Feature Control
```

### MATH ENGINE: `calculations.py`
```
🧮 print_step_by_step_explanation()  ← Complete Output
🔢 calculate_geometric_angles()      ← Silent Calculation
📐 Algorithm:
   for point in range(7):
       y = point * step_size
       dx = target_x - scanner_x
       dy = target_y - y
       angle = atan2(dx, dy) * 180/π
```

### SERVO LOGIC: `servo_interpolation.py`
```
🎯 print_servo_interpolation_explanation()  ← Servo Details
⚙️  calculate_servo_interpolation()         ← Servo Angles
🔄 print_detailed_reachability_table()     ← Reachability Analysis
📊 Servo Mapping:
   geometric_angle + 45° + 180° = servo_coord_angle
   if -135° ≤ servo_coord_angle ≤ -45°: REACHABLE
```

### CSV EXPORT: `export_commands.py`
```
📤 create_command_csv()        ← Software_IScan CSV Export
🎯 Features:
   • Custom naming support    ← --csv-name parameter
   • Timestamp-based naming   ← Default behavior
   • Only reachable points    ← Smart filtering
   • Ready for import         ← Direct Software_IScan compatibility
   • Command sequence         ← home → stepper → servo → photo
   • 28BYJ-48 stepper motor   ← Precise step calculations
```

### COORDINATOR: `main.py`
```
🚀 main()                    ← Full Mode (Explanation + Visualizations)
🔇 main_silent()             ← Visualizations Only (Silent processing)
📊 get_servo_angles()        ← Return Data Only
📤 main(create_csv=True)     ← Full Mode + CSV Export for Software_IScan
🧮 main_math_csv()           ← Mathematics + CSV Only (No visualizations)
🤫 main_math_silent()        ← Silent Math + CSV (Minimal output)
❓ show_help()               ← Command line usage help
⚙️  Configuration Override  ← Command line parameter override system

Command Line Interface:
python main.py              ← Standard full analysis
python main.py --csv/-c     ← Full analysis + CSV export
python main.py --math/-m    ← Math + CSV only (fast)
python main.py --silent/-s  ← Silent mode (automation)
python main.py --help/-h    ← Usage help
python main.py --csv-name   ← Custom CSV filename

Configuration Override System:
python main.py --target-x 33 --target-y 50 --scan-distance 80 --measurements 7  ← Original I-Scan Setup
python main.py --target-x 100 --target-y 75 --measurements 5                     ← Custom Configuration
python main.py --servo-min 10 --servo-max 80 --servo-neutral 45                  ← Servo Parameters
```

## 📊 Visualization Pipeline

```
VISUALIZATION MODULES (visualizations/)
├── geometric.py ────────────► 01_geometric_representation.png
├── angle_progression.py ────► 02_angle_progression.png
├── point_calculation.py ────► 04_point_X_calculation.png (subfolder)
├── calculation_table.py ───► 05_calculation_table.png
└── servo_interpolation.py ─► 06_servo_interpolation.png
                            └► 07_servo_cone_detail.png

CSV EXPORT PIPELINE
└── export_commands.py ─────► Custom or timestamp-based CSV files
    ├── Software_IScan compatible format
    ├── Only reachable points included
    ├── Custom naming support (--csv-name parameter)
    └── Ready for direct import
```

### CSV Export System:
```
📤 export_commands.py          ← CSV Export for Software_IScan
🎯 Command: python main.py --csv / python main.py -c
📁 Naming: Custom (--csv-name) or iscan_commands_YYYY-MM-DD_HH-MM-SS.csv
📊 Format: type,params,description (Software_IScan compatible)
⚡ Features: Reachable points only, flexible naming, direct import ready
```

### Subfolder System:
```
output/
├── 01_geometric_representation.png
├── 02_angle_progression.png
├── 05_calculation_table.png
├── 06_servo_interpolation.png
├── 07_servo_cone_detail.png
├── [custom_name].csv or iscan_commands_YYYY-MM-DD_HH-MM-SS.csv  ← Software_IScan Commands
└── point_calculations/          ← Detailed point analysis
    ├── 04_point_1_calculation.png
    ├── 04_point_2_calculation.png
    ├── ...
    └── 04_point_N_calculation.png
```

## 🔄 Data Flow Diagram

```
    ┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │   CONFIG    │───▶│   CALCULATIONS   │───▶│ SERVO_INTERP    │
    │             │    │                  │    │                 │
    │ - Scanner   │    │ 1. Step size     │    │ 1. Coord mapping│
    │ - Target    │    │ 2. For each pt:  │    │ 2. Reachability │
    │ - Distance  │    │   • dx, dy       │    │ 3. Physical ang │
    │             │    │   • atan2()      │    │                 │
    └─────────────┘    └──────────────────┘    └─────────────────┘
            │                    │                        │
            ▼                    ▼                        ▼
    ┌─────────────────────────────────────────────────────────────┐                    │                    MAIN COORDINATOR                         │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
    │  │    MATH     │  │    SERVO    │  │    VISUALIZATIONS   │  │
    │  │   ENGINE    │  │   ENGINE    │  │                     │  │
    │  │             │  │             │  │ ├─ geometric.py     │  │
    │  │ Geometric   │──┤ Interpolate │──┤ ├─ progression.py   │  │
    │  │ Angles      │  │ & Check     │  │ ├─ point_calc.py    │  │
    │  │             │  │ Limits      │  │ ├─ table.py         │  │
    │  │             │  │             │  │ └─ servo_vis.py     │  │
    │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
                              │                              ▼
                    ┌─────────────────┐
                    │  OUTPUT FILES   │
                    │                 │
                    │ 📁 output/      │
                    │ ├─ 01-07.png    │
                    │ ├─ [name].csv   │ ← Software_IScan Commands (custom or timestamp)
                    │ └─ point_calc/  │
                    │    └─ 04_X.png  │
                    └─────────────────┘
```

## ⚙️ Core Algorithm

```
INPUT: Scanner(0,0), Target(33,50), Distance=80cm, Points=7

STEP 1: Geometric Calculation
step = distance / (points - 1)  // 13.33cm
for i in range(points):
    y = i * step
    dx = target_x - scanner_x    // 33
    dy = target_y - y            // 50 to -30
    angle = atan2(dx, dy) * 180/π  // 33° to 132°

STEP 2: Servo Mapping
servo_coord = angle + 45 + 180  // -101° to -2°
if -135° ≤ servo_coord ≤ -45°:
    physical = servo_coord + 135  // 0° to 90°
    status = REACHABLE
else:
    status = UNREACHABLE

STEP 3: Visualization
save main files to output/
save point calcs to output/point_calculations/
```

## 🚀 Quick Start

### Standard Usage (Visualizations Only)
```bash
python main.py
```
**Output:** Complete mathematical explanation + 6 visualizations

### Full Analysis with CSV Export
```bash
python main.py --csv
# or short version:
python main.py -c
```
**Output:** Complete analysis + visualizations + CSV file for Software_IScan

### Mathematics + CSV Only (No Visualizations) 
```bash
python main.py --math
# or short version:
python main.py -m
```
**Output:** Complete mathematical explanation + CSV file (no visualizations, faster execution)

### Silent Mode (Minimal Output)
```bash
python main.py --silent
# or short version:
python main.py -s
```
**Output:** CSV file only with minimal console output (fastest execution for automation)

### Custom Configuration Parameters
```bash
# Original I-Scan setup recreation
python main.py --target-x 33 --target-y 50 --scan-distance 80 --measurements 7

# Custom target position with math mode
python main.py --math --target-x 100 --target-y 75 --measurements 5

# Custom servo parameters
python main.py --silent --servo-min 10 --servo-max 80 --servo-neutral 45

# Combined custom parameters
python main.py --target-x 33 --target-y 50 --scan-distance 80 --measurements 7 --servo-neutral 45
```

### Help
```bash
python main.py --help
# or short version:
python main.py -h
```

## 🎯 Available Configuration Parameters

The command-line interface allows you to override default configuration values dynamically:

### Scan Parameters
- `--target-x X`: Target X coordinate (default: 50.0)
- `--target-y Y`: Target Y coordinate (default: 50.0)  
- `--scanner-x X`: Scanner X coordinate (default: 0.0)
- `--scanner-y Y`: Scanner Y coordinate (default: 0.0)
- `--scan-distance D`: Maximum scan distance (default: 100.0)
- `--measurements N`: Number of measurements (default: 10)

### Servo Parameters
- `--servo-min ANGLE`: Minimum servo angle in degrees (default: 0.0)
- `--servo-max ANGLE`: Maximum servo angle in degrees (default: 90.0)
- `--servo-neutral ANGLE`: Neutral servo angle in degrees (default: 45.0)
- `--servo-offset ANGLE`: Servo rotation offset (default: 45.0)

### Export Parameters
- `--csv-name NAME`: Custom CSV filename without extension (default: timestamp-based)

### Real-World Examples

#### Original I-Scan Setup Recreation
```bash
python main.py --target-x 33 --target-y 50 --scan-distance 80 --measurements 7
```
This recreates the exact setup from the original I-Scan project with:
- Target at (33, 50) mm
- Maximum scan distance of 80 mm  
- 7 measurement points
- Results in angles: -135°, -120°, -105°, -90°, -75°, -60°, -45°

#### Custom Servo Range
```bash
python main.py --math --servo-min 10 --servo-max 80 --servo-neutral 45
```
This uses a custom servo with:
- Range: 10° to 80° (instead of 0° to 90°)
- Neutral position at 45°
- Coordinate system automatically recalculated

#### Quick Custom Scan
```bash
python main.py --silent --target-x 100 --target-y 75 --measurements 5
```
Fast execution with:
- Target at (100, 75) mm
- 5 measurement points
- Silent mode (CSV only)

### Advanced Usage (Python API)
```python
# Complete Analysis
python main.py

# Complete Analysis + CSV Export for Software_IScan
python main.py --csv
python main.py -c

# Calculations Only
from main import get_servo_angles
angles = get_servo_angles()

# Specific Visualization
from visualizations.geometric import create_geometric_visualization
create_geometric_visualization(angles)

# Direct CSV Export
from export_commands import create_command_csv
create_command_csv()
```

## 📤 CSV Export for Software_IScan

The system can export commands directly compatible with Software_IScan:

```bash
# Export with calculations and visualizations
python main.py --csv

# Export with short flag
python main.py -c

# Standalone CSV export
python export_commands.py
```

### CSV Output Format
```csv
type,params,description
home,{},Execute home function
stepper,"{""steps"": 6209, ""direction"": 1, ""speed"": 80}",Move 13.33cm forward
servo,"{""angle"": 80}",Point 3: Set servo to 80° (Y=26.7cm)
photo,"{""delay"": 2.0}",Point 3: Capture photo
...
```

### Key Features:
- ✅ **Only reachable points** included (unreachable points skipped)
- ✅ **Custom naming support** with --csv-name parameter
- ✅ **Timestamp-based naming** as default fallback
- ✅ **Software_IScan compatible** format
- ✅ **Direct import ready** for operation queue
- ✅ **Intelligent command sequence** (home → stepper → servo → photo)
- ✅ **28BYJ-48 stepper motor** calculations (4096 steps/revolution)

## 📋 Feature Control (config.py)

```python
ENABLE_VISUALIZATIONS = {
    'geometric_representation': True,   # Scanner Setup
    'angle_progression': True,         # Angle Progression  
    'point_calculations': True,        # Detail Calculations
    'calculation_table': True,         # Result Table
    'servo_interpolation': True,       # Servo Diagram
    'servo_cone_detail': True,         # Servo Cone
}
```

**Current Status: Mathematics Engine v4.0 - Complete with CSV Export and Custom Naming** ✅

## 📤 CSV Export Technical Details

### Command Sequence Logic:
```
1. HOME command                    ← Initialize system
2. STEPPER movements (6x)          ← Move between measurement points
3. SERVO + PHOTO (5x)              ← Only for reachable points (3,4,5,6,7)
   - Point 1: SKIPPED (unreachable)
   - Point 2: SKIPPED (unreachable)
   - Point 3-7: INCLUDED (reachable)
```

### Stepper Motor Calculations:
```
Motor: 28BYJ-48 (4096 steps/revolution)
Gear Diameter: 28mm (configurable)
Distance per step: (π × 28mm) / 4096 = 0.0215mm
For 13.33cm movement: 6209 steps
```

### File Naming Convention:
```
Custom naming: [custom_name].csv (with --csv-name parameter)
Timestamp naming: iscan_commands_YYYY-MM-DD_HH-MM-SS.csv (default)
Example custom: production_scan.csv
Example timestamp: iscan_commands_2025-06-12_14-30-15.csv
Location: output/ directory
```

### Integration with Software_IScan:
1. Export CSV using `python main.py --csv` or `python main.py --csv --csv-name [name]`
2. Import in Software_IScan operation queue
3. Execute automated 3D scanning sequence
4. Photos saved with automatic timestamps

## 📋 System Features

### Core Capabilities
- **Geometric angle calculation** using trigonometric functions
- **Servo interpolation** with reachability analysis
- **Advanced visualizations** with subfolder organization
- **CSV export** for direct Software_IScan integration
- **Command-line interface** with parameter override
- **Custom naming support** for organized project management

### Visualization Suite
- Geometric representation diagrams
- Angle progression charts
- Individual point calculation details
- Servo interpolation visualizations
- Calculation result tables
- Servo cone analysis diagrams

### Export & Integration
- Software_IScan compatible CSV format
- Custom filename support
- Automatic old file cleanup
- Reachability filtering
- Stepper motor calculations
- Direct import compatibility

## 🎓 ADD-ONS: `addons/`

```
🏫 target_coord_explanation/
└── target_coord_angle_explanation.py  ← Extended Explanations
```

## 🔧 Integration & API

```python
# Direct Integration
from main import get_servo_angles
from visualizations.geometric import create_geometric_visualization

angles = get_servo_angles()         # Data Only
create_geometric_visualization()    # Specific Visualization

# Data Structure
angle_data = {
    'point': 1,
    'y_position': 0.0,
    'dx': 100, 'dy': 0.0,
    'angle': 90.0,
    'distance': 100.0
}
```

---

**Comprehensive mathematics engine for precise 3D scanner servo control**  
*Developed by Marc Nauendorf - Hochschule Heilbronn* 🎯
