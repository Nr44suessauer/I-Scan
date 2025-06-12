# I-Scan Control Script System

# Hands on control script
python Calculator_Angle_Maschine\MathVisualisation\main.py --csv --csv-name custom_name --target-x 50 --target-y 50 --scan-distance 80 --measurements 5

python Calculator_Angle_Maschine\MathVisualisation\main.py --visualize --target-x 40 --target-y 30 --measurements 20

--- 

Clean, modern servo angle calculation system for the I-Scan 3D scanner.

**Author:** Marc Nauendorf  
**Email:** marc.nauendorf@hs-heilbronn.de  
**Website:** deadlinedriven.dev

## 🎯 System Overview

The I-Scan system has been streamlined to use **linear interpolation** between 90°-0° instead of the old trigonometric correction system. This provides better predictability and easier calibration.

## 📁 Directory Structure

```
ControlScript/
├── Calculator_Angle_Maschine/          # Modern angle calculation system
│   └── MathVisualisation/              # Complete visualization & calculation
│       ├── calculations.py             # Core calculation engine
│       ├── config.py                   # System configuration
│       ├── main.py                     # Main execution entry point
│       ├── README.md                   # Detailed documentation
│       ├── output/                     # Generated visualizations
│       └── visualizations/             # Modular visualization components
├── Software_IScan/                     # Runtime control system
│   ├── main.py                         # Scanner execution control
│   ├── servo_angle_calculator.py       # Live angle calculations
│   └── [other runtime components]
└── output/                             # Generated output files
```

## 🔄 Calculation Method

### NEW: Linear Interpolation System
- **Y=0cm**: Servo angle = 90° (MIN_SERVO_ANGLE)
- **Y=70cm**: Servo angle = 0° (MAX_SERVO_ANGLE)
- **Linear interpolation** between these points
- **Dual calculation**: Both exact trigonometric AND interpolated values
- **Feasibility indicators**: Shows when exact angles fall outside achievable range

### Removed: Old ANGLE_CORRECTION_REFERENCE System
- ❌ Constant mechanical correction (ANGLE_CORRECTION_REFERENCE = 70°)
- ❌ Complex trigonometric adjustments
- ❌ Position-dependent approximations

## 🚀 Usage

### Run Complete Calculation & Visualization
```bash
cd Calculator_Angle_Maschine/MathVisualisation
python main.py
```

This generates:
- 6 comprehensive PNG visualizations
- Step-by-step calculation explanations  
- Comparison between exact and interpolated angles
- Feasibility analysis for each measurement point

### Live Scanner Operation
```bash
cd Software_IScan
python main.py
```

## 🔗 NEW: Calculator_Angle_Maschine Integration with Software_IScan

Two powerful commands are now available in Software_IScan for seamless angle calculation:

### 🔇 CSV Silent Mode
```bash
# Direct integration in Software_IScan GUI - no command line needed
Button: "CSV Silent Mode" → Configure parameters → Generate CSV → Auto-import
```

### 🎨 Full Visualization Mode  
```bash
# Complete analysis with visualizations + CSV
Button: "Vollanalyse + CSV" → Configure parameters → Generate all files
```

**📋 See `SOFTWARE_ISCAN_INTEGRATION.md` for complete integration documentation.**

---

## 🚀 Command Line Usage (Advanced)

### Calculator_Angle_Maschine Direct Commands:
```bash
python Calculator_Angle_Maschine/MathVisualisation/main.py --csv --csv-name custom_name --target-x 50 --target-y 50 --scan-distance 80 --measurements 5
python Calculator_Angle_Maschine/MathVisualisation/main.py --visualize --target-x 40 --target-y 30 --measurements 20
```

### Software_IScan Direct Commands:
```bash
python Software_IScan/main.py --angle-calculation --csv-output
python Software_IScan/main.py --angle-calculation --visualization-output
```

## 📊 Key Configuration

```python
# File: Calculator_Angle_Maschine/MathVisualisation/config.py
TARGET_CENTER_X = 50        # Target object X-coordinate (cm)
TARGET_CENTER_Y = 35        # Target object Y-coordinate (cm)
SCAN_DISTANCE = 70          # Total scan distance (cm)
NUMBER_OF_MEASUREMENTS = 4  # Number of measurement points

# Interpolation parameters
MIN_SERVO_ANGLE = 90        # Servo angle at Y=0 (degrees)
MAX_SERVO_ANGLE = 0         # Servo angle at Y=max (degrees)
USE_APPROXIMATION = True    # Use linear interpolation vs exact calculation
```

## 🎨 Generated Visualizations

1. **01_geometric_representation.png** - Coordinate system and scan path
2. **02_angle_progression.png** - Angle changes along scan path
3. **03_trigonometry_formulas.png** - Mathematical formulas used
4. **04_point_X_calculation.png** - Individual point calculations
5. **05_calculation_table.png** - Summary table with all results
6. **06_complete_servo_angle_visualization.png** - Complete overview

## 🔧 Technical Details

### Angle Calculation Formula
- **Exact**: `α = arctan(dx/dy)` (angle between line and Y-axis)
- **Interpolated**: `angle = MIN_SERVO_ANGLE + progress × (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE)`
- **Progress**: `progress = y_position / SCAN_DISTANCE` (0.0 to 1.0)

### Example Results
```
Point 1 (Y=0cm):    Exact=65°, Interpolated=90° ✓ MACHBAR
Point 2 (Y=23.3cm): Exact=90°, Interpolated=60° 
Point 3 (Y=46.7cm): Exact=65°, Interpolated=30°
Point 4 (Y=70cm):   Exact=47°, Interpolated=0°  ✗ NICHT MACHBAR
```

## 📋 System Benefits

- ✅ **Predictable**: Linear interpolation provides consistent behavior
- ✅ **Simple**: No complex mechanical corrections needed
- ✅ **Visual**: Comprehensive visualization system
- ✅ **Modular**: Clean separation of calculation and visualization
- ✅ **Flexible**: Easy configuration changes
- ✅ **Validated**: Shows both theoretical and practical angles

## 🗂️ Cleaned Up Files

The following legacy files were removed to streamline the system:
- `calculator/` directory (old trigonometric system)
- `calculator_Angle_IScan.py` (old ANGLE_CORRECTION_REFERENCE system)
- `calculator_without_visualization.py` (redundant)
- `ScanConfigs/` (old CSV files)
- Various test and backup files

The new system in `MathVisualisation/` provides all necessary functionality with improved clarity and maintainability.
