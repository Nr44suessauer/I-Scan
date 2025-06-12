# Software_IScan – Modern 3D Scanner Control GUI

**Author:**
- Marc Nauendorf  
  Email: marc.nauendorf@hs-heilbronn.de  
  Website: DeadlineDriven.dev

---

## Overview
Software_IScan is a comprehensive, extensible GUI application for controlling the I-Scan 3D scanner hardware. Designed for research, industrial, and educational use, it provides a robust, user-friendly interface for all scanning operations, including live hardware control, batch operation management, and advanced angle calculation/visualization integration. The project is modular and ready for large-scale extension.

---

## Project Structure

```
ControlScript/
├── Software_IScan/                  # Main GUI and control logic
│   ├── main.py                      # Main GUI application
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
|                   |                                      |       |
|  Scan Config/     |      Dynamic Image Preview            |       |
|  Command Panel    |  (servo geometry, updates after scan) |       |
|                   |                                      |       |
+-------------------+-------------------+--------------------------+
|                        Log Console (live, scrollable)            |
+------------------------------------------------------------------+
```
- **Calculator Commands**: Configure and execute angle calculations, generate CSVs, and run full visualizations.
- **Scan Config/Command Panel**: Set all scan parameters, view and edit the live command, and execute scans.
- **Dynamic Image Preview**: Shows the latest servo geometry visualization after each scan.
- **Log Console**: Displays all actions, errors, and system messages in real time.

---

## Key Features

- **Unified Hardware Control**: Servo, stepper, and LED management from a single interface.
- **Live Command Display**: See the exact command line that will be executed as you change parameters.
- **Dynamic Image Preview**: Automatically updates with the latest scan geometry after each operation.
- **Calculator_Angle_Maschine Integration**: Run advanced angle calculations and visualizations directly from the GUI.
- **Robust Logging & Error Handling**: All actions and errors are logged in the GUI for transparency and troubleshooting.
- **Compact, Balanced Layout**: Grid-based layout ensures equal space for configuration, image, and logs.
- **Batch Operation Support**: Queue and execute complex scan sequences, import/export CSVs.
- **Extensible API Layer**: REST-based, easily adapted for new hardware endpoints.
- **Async/Threaded Operations**: Non-blocking UI, responsive even during long calculations or scans.

---

## Calculator_Angle_Maschine Integration

- **CSV Silent Mode**: Generate a CSV of scan commands with custom parameters for batch operation.
- **Full Visualization Mode**: Generate all visualizations and CSV in one step; image preview updates automatically.
- **Import CSV**: Load generated CSVs directly into the operation queue.
- **All actions are non-blocking and provide progress feedback in the log.**
- **Presets and Validation**: Use quick presets or custom parameters, with input validation.

---

## API & Extension Points

- **REST API Communication**: All hardware control is performed via REST endpoints (servo, stepper, LED, home, etc.).
- **Modular Design**: Add new hardware or features by extending `device_control.py` and updating the GUI in `main.py`.
- **Operation Queue**: Extendable for new command types; supports batch execution and custom CSV formats.
- **Calculator Integration**: Extend `angle_calculator_commands.py` to add new calculation modes or presets.
- **Visualization Output**: Add new image types or output formats in MathVisualisation.
- **Logging**: Add new log sinks or formats in `logger.py`.

---

## Usage

### Requirements
```bash
pip install tkinter pillow opencv-python requests numpy
```

### Start the Application
```bash
cd Software_IScan
python main.py
```

### Typical Workflow
1. Set scan parameters in the Calculator Commands and Scan Config panels.
2. Use Calculator Commands to generate CSVs or run full visualizations as needed.
3. Execute scans; the image preview and log update automatically.
4. Review logs and images for results and troubleshooting.
5. Extend or automate as needed for your research or production workflow.

---

## Example: Live Command Display

As you adjust parameters, the GUI shows the exact command that will be run, e.g.:
```
python ..\Calculator_Angle_Maschine\MathVisualisation\main.py --csv --csv-name scan1 --target-x 50 --target-y 50 --scan-distance 80 --measurements 5
```

---

## Troubleshooting & Support
- All errors and actions are logged in the GUI log console.
- For advanced integration or calculation details, see the integration and calculation documentation in the parent directory.
- For support, contact the authors or open an issue.

---

## Extending the Application
- Add new hardware: Implement in `device_control.py`, expose controls in `main.py`.
- Add new scan commands: Extend `operation_queue.py` and update the command panel.
- Add new calculation modes: Extend `angle_calculator_commands.py` and update the Calculator Commands panel.
- Add new visualizations: Extend MathVisualisation and update the image preview logic.
- Add new log outputs: Extend `logger.py` for new sinks or formats.

---

## Contributors / Authors
- Marc Nauendorf (lead developer)

---

**This README replaces all previous documentation for Software_IScan. Remove or ignore any outdated references to CSV quick presets, legacy batch modes, or obsolete troubleshooting/configuration steps.**
