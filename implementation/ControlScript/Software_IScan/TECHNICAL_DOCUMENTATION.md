# I-Scan Control Software - Original Version Documentation

**Version:** 1.0 (Original/Monolithic)  
**Entry Point:** `main.py`  
**Architecture:** Single-file GUI application  
**Last Updated:** June 2025

---

## Overview

The Original Version is a complete, monolithic GUI application that provides hardware control functionality for the I-Scan 3D scanner through a unified interface. All GUI components and business logic are contained within a single main file.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Original Version                        │
│                     (Monolithic Design)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    main.py                              │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌─────────────┐  │   │
│  │  │ GUI Components│  │ Event Handlers│  │ Business    │  │   │
│  │  │               │  │               │  │ Logic       │  │   │
│  │  │ • Servo       │  │ • Button      │  │             │  │   │
│  │  │ • Stepper     │  │   Callbacks   │  │ • Validation│  │   │
│  │  │ • LED         │  │ • Menu        │  │ • Commands  │  │   │
│  │  │ • Camera      │  │   Actions     │  │ • Queue Mgmt│  │   │
│  │  │ • Calculator  │  │ • API Calls   │  │             │  │   │
│  │  │ • Queue       │  │               │  │             │  │   │
│  │  └───────────────┘  └───────────────┘  └─────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Support Modules                          │   │
│  │                                                         │   │
│  │  api_client.py          device_control.py              │   │
│  │  logger.py              operation_queue.py             │   │
│  │  webcam_helper.py       servo_angle_calculator.py      │   │
│  │  angle_calculator_commands.py                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Main Application (`main.py`)

**Class:** `ControlApp`  
**Purpose:** Central GUI application managing all user interactions and hardware control

**Key Methods:**
- `__init__()` - Application initialization and GUI setup
- `setup_gui()` - Creates the complete user interface
- `setup_*_frame()` - Individual component frame creation
- `handle_*_action()` - Event handlers for user interactions

**GUI Structure:**
```
┌─────────────────────────────────────────────────────────────────┐
│                     I-Scan Wizard                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Servo     │  │   Stepper   │  │     LED     │             │
│  │   Control   │  │   Control   │  │   Control   │             │
│  │             │  │             │  │             │             │
│  │ • Angle     │  │ • Diameter  │  │ • Color     │             │
│  │ • Speed     │  │ • Speed     │  │ • Brightness│             │
│  │ • Position  │  │ • Distance  │  │ • Toggle    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Camera    │  │ Calculator  │  │   Queue     │             │
│  │   Preview   │  │ Integration │  │ Management  │             │
│  │             │  │             │  │             │             │
│  │ • Live Feed │  │ • Visualize │  │ • Operations│             │
│  │ • Capture   │  │ • Generate  │  │ • Import    │             │
│  │ • Settings  │  │ • Export    │  │ • Execute   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                     Status & Logging                           │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Support Modules

#### API Client (`api_client.py`)
- HTTP communication with hardware API
- Request/response handling
- Error management

#### Device Control (`device_control.py`)
- Hardware abstraction layer
- Command validation
- Status monitoring

#### Operation Queue (`operation_queue.py`)
- Batch operation management
- CSV import/export
- Execution control

#### Webcam Helper (`webcam_helper.py`)
- Camera initialization
- Frame capture
- Display management

#### Logger (`logger.py`)
- Event logging
- Error tracking
- Debug information

## Data Flow

```
User Input → GUI Event → Validation → API Call → Hardware Response
    ↓                                                    ↓
Status Update ← GUI Update ← Response Processing ← JSON Response
```

**Detailed Flow:**
1. User interacts with GUI component
2. Event handler validates input
3. Command sent to API via `api_client`
4. Hardware executes command
5. Response processed and GUI updated
6. Status logged

## Configuration

**Default Values:**
- API Base URL: `http://192.168.137.7`
- Stepper Diameter: `28mm`
- Default Speed: `80`
- LED Color: `#B00B69`
- LED Brightness: `69%`

**Runtime Configuration:**
All parameters can be modified through the GUI interface during runtime.

## File Structure

```
Software_IScan/
├── main.py                      # Main application (1200+ lines)
├── api_client.py               # HTTP API communication
├── device_control.py           # Hardware abstraction
├── operation_queue.py          # Batch operations
├── logger.py                   # Logging system
├── webcam_helper.py            # Camera handling
├── servo_angle_calculator.py   # Servo calculations
├── angle_calculator_commands.py # Calculator integration
├── requirements.txt            # Dependencies
├── wizard_icon.png            # Application icon
└── README.md                  # Version-specific documentation
```

## Key Features

### ✅ Complete Hardware Control
- Servo motor positioning with angle/speed control
- Stepper motor movement with precise distance control
- LED color and brightness adjustment
- Camera preview and capture functionality

### ✅ Batch Operations
- CSV-based operation queues
- Import/export functionality
- Sequential execution with status tracking

### ✅ Mathematical Integration
- Direct integration with angle calculator
- Automatic visualization generation
- Parameter-based scan planning

### ✅ User Experience
- Real-time hardware status display
- Comprehensive logging system
- Intuitive GUI layout

## Advantages

- **Simplicity:** All functionality in one place
- **Self-contained:** Minimal file dependencies
- **Proven:** Stable, well-tested implementation
- **Complete:** All features accessible from single interface

## Limitations

- **Maintainability:** Large single file (1200+ lines)
- **Extensibility:** Difficult to add new features
- **Testing:** Hard to test individual components
- **Code Reuse:** Limited component reusability

## Usage

### Startup
```bash
cd Software_IScan
python main.py
```

### Or via batch file:
```batch
start_original_version.bat
```

### Basic Operation
1. Configure API endpoint in GUI
2. Set hardware parameters
3. Execute individual commands or batch operations
4. Monitor status and logs

## Dependencies

```
tkinter          # GUI framework
PIL/Pillow       # Image processing
requests         # HTTP client
opencv-python    # Camera handling
matplotlib       # Visualization
```

See `requirements.txt` for complete dependency list.

## Development Notes

- All GUI components are created procedurally in `setup_gui()`
- Event handlers are defined as methods of `ControlApp` class
- State management through instance variables
- Direct API calls without abstraction layers
- Inline error handling and validation

This version serves as the foundation and reference implementation for the I-Scan control system.
