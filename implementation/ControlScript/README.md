# I-Scan Control Script System – Top-Level Documentation

**Author:**
- Marc Nauendorf  
  Email: marc.nauendorf@hs-heilbronn.de  
  Website: DeadlineDriven.dev

**Version:** 3.0 - Modernized & Unified System

---

## Overview & Architecture

The I-Scan Control Script System is a modular, extensible platform for controlling, automating, and mathematically analyzing 3D scanner hardware. It consists of two tightly integrated main projects:

### 1. Software_IScan (GUI & Hardware Control)
- **Path:** `Software_IScan/`
- **Purpose:** Provides a modern, user-friendly graphical interface for controlling all hardware components (servo, stepper, LED, camera, etc.) via a REST API.
- **Features:**
  - Live control and status display with real-time command preview
  - Batch operations (queue) with CSV import/export
  - Integration of mathematical calculations and visualizations
  - Tabbed image viewer with automatic scaling
  - Logging, error handling, camera preview
  - **NEW:** User-configurable servo parameters (min, max, neutral angles)
  - **NEW:** Real-time visualization updates with dual-image tabs

### 2. Calculator_Angle_Maschine (Mathematical Engine)
- **Path:** `Calculator_Angle_Maschine/MathVisualisation/`
- **Purpose:** Performs all mathematical calculations for optimal scanner control, generates CSV command lists, and creates visualizations (PNG).
- **Features:**
  - Linear and trigonometric angle calculation
  - Generation of CSV files for automated scans
  - Graphical analysis and visualization of scan geometry
  - Flexible configuration and presets
  - **NEW:** Simplified servo coordinate transformation
  - **NEW:** Inverted neutral angle for intuitive operation
  - **NEW:** Optimized visualization generation (point calculations optional)

---

## Recent Improvements (Version 3.0)

### Servo Configuration System
- **User-Configurable Parameters:** All servo angles (min, max, neutral) can now be set directly in the GUI
- **Simplified Transformation:** New formula `servo_angle = geometric_angle - neutral_angle` for intuitive operation
- **Real-Time Updates:** Command display updates instantly when parameters change
- **Default Values:** Neutral angle defaults to 45° for optimal operation

### Enhanced GUI Experience
- **Tabbed Image Viewer:** Switch between "Servo Graph" and "Cone Detail" visualizations
- **Proportional Scaling:** Images maintain aspect ratio and scale with window size
- **Real-Time Preview:** Visualizations update automatically after calculations
- **Streamlined Interface:** Removed preset buttons for cleaner, more flexible interface
- **Modular Architecture:** GUI components separated into maintainable modules

### Mathematical Engine Optimization
- **Inverted Neutral Logic:** Entering -45° rotates cone by +45° (more intuitive)
- **Performance Optimization:** Point calculation graphs can be disabled for faster processing
- **Enhanced Documentation:** All functions and parameters fully documented in English
- **CSV Integration:** Seamless export/import between calculator and GUI

### GUI Architecture - Modular Design
The Software_IScan GUI has been refactored with a modular architecture:

- **`gui/main_window.py`:** Main window coordinator and component orchestrator
- **`gui/servo_controls.py`:** Servo motor control interface
- **`gui/stepper_controls.py`:** Stepper motor control interface  
- **`gui/led_controls.py`:** LED color and brightness control
- **`gui/webcam_display.py`:** Camera display and control interface
- **`gui/angle_calculator_gui.py`:** Calculator integration with tabbed image viewer
- **`gui/queue_management.py`:** Operation queue management interface
- **`gui/status_display.py`:** Status information and basic settings

**Benefits:**
- Better maintainability and code organization
- Reusable components for future development
- Independent testing of GUI components
- Easier extension with new features

---

## Quick Start

### Option 1: Use Start Scripts (Recommended)
- **For Original Version:** Double-click `start_original_version.bat`
- **For Modular Version:** Double-click `start_modular_version.bat`

### Option 2: Manual Launch

#### Launch Original Version
```bash
cd Software_IScan
python main.py
```

#### Launch Modular Version (Recommended)
```bash
cd "Modular Version"
python main_modular.py
```

**Note:** The modular version provides the same functionality with better code organization and maintainability.

### 2. Configure Scan Parameters
- Set target position (X, Y coordinates)
- Adjust scan distance and number of measurements
- Configure servo angles (min: 0°, max: 90°, neutral: 45°)

### 3. Generate Scan Commands
- Click "Execute Visualisation Mode" to create visualizations
- Click "Execute Silent Mode" to generate CSV only
- Import generated CSV into operation queue

### 4. Direct Calculator Access
```bash
cd Calculator_Angle_Maschine/MathVisualisation
python main.py --help                    # Show all options
python main.py --csv --csv-name scan_01  # Generate CSV
python main.py --visualize               # Create visualizations
```

---

## Project Interaction

```
+-------------------+        REST API        +-------------------+
|   Software_IScan  | <-------------------> |   Scanner HW/API  |
+-------------------+                       +-------------------+
|  main.py (GUI)    |
|  device_control   |
|  operation_queue  |
|  logger           |
|  angle_calculator |
+-------------------+
        |
        |  (subprocess call)
        v
+-------------------------------+
| Calculator_Angle_Maschine     |
|   (MathVisualisation/main.py) |
+-------------------------------+
```

- **Software_IScan** calls the mathematical engine (`Calculator_Angle_Maschine`) as a subprocess to generate optimal scan commands and visualizations for the current configuration.
- The generated **CSV files** are directly imported into the GUI queue and can be executed immediately.
- The **visualizations** (e.g., servo geometry) are automatically updated after each scan and displayed in the GUI.
- Changes to parameters in the GUI immediately update the displayed commands, enabling seamless integration of mathematics and hardware control.

---

## Target Audience & Extensibility

- **Research & Development:** Rapid adaptation to new hardware, experimentation with scan strategies and mathematical models.
- **Production & Automation:** Robust, repeatable workflows through batch operations and automated command generation.
- **Education & Demonstration:** Visualization and documentation of all mathematical and technical processes.

The system is designed so that new hardware, mathematical methods, or visualizations can be easily added (see the respective README.md in the subprojects).

---

## Getting Started & Documentation

- **Software_IScan/README.md:** Details on the GUI, hardware control, and extension
- **Calculator_Angle_Maschine/MathVisualisation/README.md:** Details on mathematical methods, parameters, and visualizations
- **BEFEHLE_UND_PARAMETER.md:** Overview of all available commands and parameters
- **SOFTWARE_ISCAN_INTEGRATION.md:** Technical details on the integration of both systems

---

**Note:**
This file is the central entry point documentation for the entire I-Scan Control Script System. For details on individual modules, please refer to the respective sub-README.md files.

---

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
