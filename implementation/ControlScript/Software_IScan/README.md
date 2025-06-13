# Software_IScan – Modern 3D Scanner Control GUI

**Author:**
- Marc Nauendorf  
  Email: marc.nauendorf@hs-heilbronn.de  
  Website: DeadlineDriven.dev

**Version:** 4.0 - Modular Architecture & Enhanced Maintainability

---

## What's New in Version 4.0

### 🏗️ Modular GUI Architecture
- **Complete GUI Refactor:** All GUI components separated into individual, reusable modules
- **Better Code Organization:** Clear separation of concerns and responsibilities
- **Enhanced Maintainability:** Independent testing and modification of components
- **Future-Proof Design:** Easy extension with new features and hardware support

### 📁 New File Structure
- **`main_modular.py`:** New recommended entry point with modular architecture
- **`gui/` Module:** Complete set of specialized GUI components
- **Component Isolation:** Each GUI element (servo, stepper, LED, etc.) in separate files
- **Backward Compatibility:** Original `main.py` remains available for legacy support

### 🔧 Technical Improvements
- **Callback System:** Centralized callback management for better event handling
- **Widget Access Management:** Structured widget dictionary for external access
- **Error Handling:** Improved error handling and logging throughout components
- **Documentation:** Comprehensive architecture documentation in `GUI_ARCHITECTURE.md`

---

## Overview
Software_IScan is a comprehensive, extensible GUI application for controlling the I-Scan 3D scanner hardware. Designed for research, industrial, and educational use, it provides a robust, user-friendly interface for all scanning operations, including live hardware control, batch operation management, and advanced angle calculation/visualization integration. 

### Features
- **User-Configurable Servo Parameters:** Direct control over min, max, and neutral servo angles
- **Enhanced Image Viewer:** Tabbed interface with proportional scaling for multiple visualizations
- **Real-Time Command Display:** Live preview of exact commands as parameters change
- **Streamlined Interface:** Cleaner design with optimized workflow

---

## Project Structure

```
ControlScript/
├── Software_IScan/                  # Main GUI and control logic
│   ├── main.py                      # Original monolithic GUI application
│   ├── main_modular.py              # New modular GUI application (recommended)
│   ├── gui/                         # Modular GUI components (NEW)
│   │   ├── __init__.py              # GUI module initialization
│   │   ├── main_window.py           # Main window coordinator
│   │   ├── servo_controls.py        # Servo control interface
│   │   ├── stepper_controls.py      # Stepper motor control interface
│   │   ├── led_controls.py          # LED control interface
│   │   ├── webcam_display.py        # Camera display and controls
│   │   ├── angle_calculator_gui.py  # Angle calculator interface
│   │   ├── queue_management.py      # Operation queue management
│   │   └── status_display.py        # Status display and basic settings
│   ├── angle_calculator_commands.py # Calculator_Angle_Maschine integration
│   ├── device_control.py            # Hardware abstraction and control
│   ├── operation_queue.py           # Operation queue and batch execution
│   ├── logger.py                    # Logging utilities
│   ├── api_client.py                # REST API communication
│   ├── webcam_helper.py             # Camera integration
│   └── ... (other modules)
│
├── Calculator_Angle_Maschine/       # Advanced calculation engine
│   └── MathVisualisation/
│       ├── main.py                  # Angle calculation & visualization
│       ├── calculations.py          # Core math logic
│       ├── config.py                # Calculation config
│       ├── output/                  # Generated images/CSVs
│       └── visualizations/          # Modular visualization components
│
├── output/                          # Scan and calculation results
└── ... (integration, docs, etc.)
```

---

## Architecture & Extensibility

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
        |  (subprocess)
        v
+-------------------------------+
| Calculator_Angle_Maschine     |
|   (MathVisualisation/main.py) |
+-------------------------------+
```
- **Modular GUI**: All panels/components are easily extendable in `main.py`.
- **Device Abstraction**: Add new hardware by extending `device_control.py` and updating the API client.
- **Operation Queue**: Supports new command types and batch logic in `operation_queue.py`.
- **Calculation Engine**: Extend `angle_calculator_commands.py` and the MathVisualisation package for new math/visualization features.
- **Logging**: Centralized, extensible logging in `logger.py`.

---

## GUI Layout

```
+-------------------------------------------------------------------+
| [Calculator Commands] [Home] [Queue] [Scan Config]                |
+-------------------+-------------------+--------------------------+
| Servo Parameters  |    Tabbed Image Viewer                |       |
| • Min Angle       |  ┌─[Servo Graph]─[Cone Detail]─┐    |       |
| • Max Angle       |  │                              │    |       |
| • Neutral Angle   |  │     [Visualization Area]     │    |       |
| • Target X/Y      |  │   (Proportional Scaling)     │    |       |
| • Scan Distance   |  └──────────────────────────────┘    |       |
| • Measurements    |                                      |       |
+-------------------+-------------------+--------------------------+
|                Live Command Display & Execution                   |
+-------------------+-------------------+--------------------------+
|                     Log Console (live, scrollable)               |
+------------------------------------------------------------------+
```
- **Calculator Commands**: Configure and execute angle calculations, generate CSVs, and run full visualizations.
- **Scan Config/Command Panel**: Set all scan parameters, view and edit the live command, and execute scans.
- **Dynamic Image Preview**: Shows the latest servo geometry visualization after each scan.
- **Log Console**: Displays all actions, errors, and system messages in real time.

---

## Key Features

### Hardware Control & Integration
- **Unified Hardware Control**: Servo, stepper, and LED management from a single interface
- **REST API Communication**: Robust communication with scanner hardware
- **Real-Time Status Updates**: Live feedback from all connected devices
- **Batch Operation Support**: Queue and execute complex scan sequences

### User Interface Enhancements
- **Tabbed Image Viewer**: Switch between "Servo Graph" and "Cone Detail" visualizations
- **Fixed Image Scaling**: Images maintain aspect ratio with optimal size (no permanent window resize tracking)
- **Live Command Display**: See the exact command line that will be executed as you change parameters
- **Calculator Integration**: Run advanced angle calculations directly from the GUI

### Servo Configuration System
- **Min/Max/Neutral Angles**: Configure all servo parameters directly in the GUI
- **Real-Time Updates**: Command display updates instantly when parameters change
- **Intuitive Operation**: Simplified coordinate transformation for easier use
- **Default Values**: Optimized defaults (min: 0°, max: 90°, neutral: 45°)

### Advanced Features
- **CSV Import/Export**: Seamless integration with calculation engine
- **Robust Logging**: All actions and errors logged for transparency
- **Camera Integration**: Live camera preview with configurable settings
- **Error Handling**: Comprehensive error reporting and recovery

---

## GUI Layout & Workflow

```
+-------------------------------------------------------------------+
| [Calculator Commands] [Home] [Queue] [Scan Config]                |
+-------------------+-------------------+--------------------------+
| Servo Parameters  |    Tabbed Image Viewer                |       |
| • Min Angle       |  ┌─[Servo Graph]─[Cone Detail]─┐    |       |
| • Max Angle       |  │                              │    |       |
| • Neutral Angle   |  │     [Visualization Area]     │    |       |
| • Target X/Y      |  │   (Proportional Scaling)     │    |       |
| • Scan Distance   |  └──────────────────────────────┘    |       |
| • Measurements    |                                      |       |
+-------------------+-------------------+--------------------------+
|                Live Command Display & Execution                   |
+-------------------+-------------------+--------------------------+
|                     Log Console (live, scrollable)               |
+------------------------------------------------------------------+
```

### Workflow
1. **Configure Parameters**: Set servo angles, target position, scan distance
2. **Preview Commands**: See live command updates as you change parameters
3. **Generate Results**: Execute visualization or silent mode
4. **View Results**: Switch between servo graph and cone detail in tabbed viewer
5. **Execute Scan**: Import CSV to queue and run automated scan

---

## Configuration Parameters

### Servo Motor Settings
- **Servo Min Angle**: Minimum servo position (default: 0°)
- **Servo Max Angle**: Maximum servo position (default: 90°)
- **Servo Neutral Angle**: Neutral position for cone rotation (default: 45°)

### Scan Configuration
- **Target X/Y**: Target object position in coordinate system
- **Scan Distance**: Total scanning distance
- **Number of Measurements**: Points along scan path

### Advanced Options
- **CSV Name**: Custom name for generated command files
- **Camera Settings**: Device index and autofocus delay
- **Visualization Options**: Enable/disable specific graph types

---

## Getting Started

### Option A: Modular Architecture (Recommended)
```bash
# Install required dependencies
pip install tkinter pillow

# Navigate to project directory
cd Software_IScan

# Launch modular GUI application
python main_modular.py
```

### Option B: Legacy Application
```bash
# Navigate to project directory
cd Software_IScan

# Launch legacy GUI application
python main.py
```

### Quick Configuration
1. **Set servo parameters** (min: 0°, max: 90°, neutral: 45°)
2. **Configure target position** and scan distance
3. **Adjust number of measurement points**
4. **Generate scan commands** with visualizations
5. **Execute scan** through operation queue

---

## GUI Component Guide (Modular Architecture)

When using `main_modular.py`, the interface is organized into specialized components:

### Servo Controls
- Angle input field (0-90°)
- Direct execution and queue addition
- Real-time validation

### Stepper Controls  
- Distance, direction, and speed configuration
- Flexible parameter input
- Immediate or queued execution

### LED Controls
- Color selection with hex codes
- Brightness control (0-100%)
- Separate color and brightness frames

### Camera Display
- Live camera feed
- Device selection and autofocus settings
- Photo capture with queue integration

### Angle Calculator Integration
- Parameter input for all calculation variables
- Real-time command preview
- Tabbed image viewer for results
- Direct visualization and silent mode execution

### Queue Management
- Visual operation queue with scrolling
- Import/export CSV functionality
- Batch execution with repeat option

For detailed component documentation, see `GUI_ARCHITECTURE.md`.
