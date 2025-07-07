# I-Scan System Documentation - English Version

## Coding Standards and Patterns:

### Modular Architecture
The application is divided into small, specialized Python files, 
each fulfilling a specific task (GUI creation, event handling, API communication, camera management, etc.). 

This improves readability, maintainability, and testability.

### Class-Based Structure
Most functionalities are encapsulated in classes, promoting object-orientation.

### Static Methods
For utility functions that don't require instance state 
(e.g., `GUIBuilder`, `ApiClient`, `WebcamHelper.detect_available_cameras`), 
static methods are used.

### Tkinter Variables
The use of `tk.StringVar`, `tk.IntVar`, `tk.DoubleVar` for GUI inputs and displays 
ensures clean data binding between GUI and logic.

### Threading
Long-running operations (e.g., camera streams, queue execution, API calls) 
are executed in separate threads to keep the GUI responsive.

### Configuration Centralization
All constants and default values are consolidated in `config.py`, 
facilitating customization and maintenance.

### JSON for Configuration
Camera configuration is stored in a JSON file, 
enabling flexible and extensible camera definitions.

### Error Handling
`try-except` blocks are used to catch exceptions and log them in the Logger, 
facilitating debugging.

### Logging
A dedicated `Logger` class centralizes log output and enables color formatting 
and parsing of status information.

## 5.5. Setup & Development Environment

To run and develop the I-Scan ControlScript program, 
the following steps and dependencies are required:

### Prerequisites

**Python:** Version 3.x (tested with 3.9+).

**Pip:** Python package manager (usually installed with Python).

**Git:** For cloning the repository (optional if code is provided manually).

**Hardware API:** A running hardware API that provides the endpoints defined in `api_client.py` 
(e.g., on an ESP32 or similar microcontroller). 

The default URL is `http://192.168.137.7`.

### Required Python Libraries

Install the libraries via pip:

```bash
pip install opencv-python-headless requests Pillow numpy
```

**opencv-python-headless:** For camera control and image processing (OpenCV). 
The headless version is often sufficient when no GUI features from OpenCV itself are needed.

**requests:** For HTTP requests to the hardware API.

**Pillow:** For image processing and conversion of OpenCV frames for Tkinter.

**numpy:** For numerical operations, especially in image processing.

### Development Environment Setup

#### Code Retrieval

**If using Git:** 
```bash
git clone <repository-url>
```
(Replace `<repository-url>` with the actual URL once accessible).

**If code is provided manually:** 
Ensure all .py files are in the `implementation/ControlScript/Modular Version/` directory.

#### Configuration File (cameras_config.json)

Ensure a `cameras_config.json` file exists in the `camera/` subdirectory 
(e.g., `implementation/ControlScript/Modular Version/camera/cameras_config.json`). 

If not present, a default file will be created.

#### Example cameras_config.json:

```json
{
  "cameras": [
    {
      "index": 0,
      "verbindung": "USB:0",
      "beschreibung": "Primary USB Camera",
      "name": "Camera 1",
      "enabled": true,
      "resolution": [640, 480],
      "fps": 30
    },
    {
      "index": 1,
      "verbindung": "USB:1",
      "beschreibung": "Second USB Camera",
      "name": "Camera 2",
      "enabled": true,
      "resolution": [640, 480],
      "fps": 30
    }
  ],
  "settings": {
    "auto_start_streams": true,
    "stream_timeout": 5,
    "reconnect_attempts": 3
  }
}
```

Adjust the `verbindung` strings to your actual camera indices or IP addresses.

#### Running the Application

Navigate in the terminal to the `implementation/ControlScript/Modular Version/` directory.

Run the main application:

```bash
python main.py
```

The Tkinter GUI window should appear.

### Environment Requirements Table

| Software/Tool | Specific Version (if critical) | Purpose |
|---------------|--------------------------------|---------|
| Python | 3.9+ | Runtime environment |
| pip | Current | Package manager |
| Git | Current (optional) | Version control |
| opencv-python-headless | Current | Camera control, image processing |
| requests | Current | HTTP communication with API |
| Pillow | Current | Image processing for GUI |
| numpy | Current | Numerical operations |

## 5.6. Extension & Contribution Guide

The modular structure of the I-Scan ControlScript program facilitates extensions and contributions.

### Adding New Operations

#### Definition in queue_operations.py

Create a new method in QueueOperations (e.g., `add_new_operation_to_queue`).

This method should collect parameters for the new operation and call `self.app.operation_queue.add()` 
to add the operation to the queue.

#### Execution in operation_queue.py

Add a new `elif` block in the `execute_single_operation` method of the OperationQueue class.

Implement the logic for executing the new operation here by calling appropriate ApiClient methods 
or using other modules.

#### GUI Integration in gui_components.py

Add new widgets (buttons, input fields) in GUIBuilder to represent the new operation in the GUI.

#### Event Binding in event_handlers.py

Bind the new GUI widgets to the corresponding method in QueueOperations 
(e.g., `on_new_operation_add_to_queue`) in the `assign_all_callbacks` method.

### Extending the GUI

**gui_components.py:** Add new static methods to create new GUI elements or entire panels.

**main.py:** Call the new GUIBuilder methods in `create_all_widgets` 
to integrate the new elements into the layout.

**event_handlers.py:** Create new event handler methods and bind them to the new GUI elements.

### Adding New Camera Types

#### json_camera_config.py

Extend the `parse_verbindung` method to interpret new connection types 
(e.g., "GigE:192.168.1.200").

Ensure that the `create_default_config` and `add_camera` methods can accommodate the new types.

#### json_camera_stream_manager.py

The CameraStream class may need to be extended to support connection and streaming 
for the new camera type (e.g., by adding logic in the `connect` method).

### Contribution Process

**Branching:** Create a new branch for your changes (e.g., `feature/new-function` or `bugfix/fix-issue`).

**Code Changes:** Implement your changes and ensure the code follows existing coding standards.

**Testing:** Perform local tests to verify the functionality of your changes.

**Commit:** Commit your changes with meaningful messages.

**Pull Request:** Create a Pull Request (PR) in the GitHub repository to propose your changes for review. 
Describe your changes in detail and reference relevant issues.

## 5.7. Known Issues & Future Considerations

### Known Issues

#### Initial GitHub Access
The problem of direct access to the GitHub repository via automated tools persists, 
although the code could be provided manually. 

This could impact future automated builds or CI/CD pipelines that rely on direct repository access.

#### Missing AngleCalculator_Commands.py
The file AngleCalculator_Commands.py was imported in main.py but not provided. 

This could indicate missing functionality in the angle calculator area or an outdated import statement.

#### Redundancy in Camera Control
There are both JSONCameraStreamManager/CameraStream and WebcamHelper. 

Although they serve different purposes (Manager for JSON configuration, Helper for low-level access), 
further consolidation or clear separation of responsibilities could simplify the codebase.

#### Missing update_position_label Callback
In Logger.__init__, an update_callback is expected, but None is passed in ControlApp.init_backend_modules. 

This could mean that the position and servo angle labels in the GUI are not automatically updated 
when the Logger processes a message containing these values. 

This should be checked and fixed by passing an appropriate callback 
(e.g., a method in ControlApp that updates the labels).

### Future Considerations

#### More Robust API Client
Implementation of retry mechanisms and exponential backoff for API requests 
to improve robustness with temporary network problems or hardware response times.

#### Extended Error Handling
More detailed error logging and user notifications for hardware errors or API problems.

#### Configurable Paths
External configuration of paths for images and configuration files 
instead of using hardcoded paths.

#### Custom Operations
A way for users to define their own operations via the GUI and add them to the queue 
without having to modify the code.

#### Servo Angle Calculator Visualization
Integration of ServoAngleCalculator visualization functions directly into the GUI 
to make geometric calculations more understandable.

#### Unit Tests
Creation of unit tests for critical modules 
(e.g., ServoAngleCalculator, OperationQueue, ApiClient) 
to ensure code quality and stability.

#### Hardware API Documentation
Separate documentation of expected API endpoints and their parameters 
would benefit development of the hardware side of the system.
