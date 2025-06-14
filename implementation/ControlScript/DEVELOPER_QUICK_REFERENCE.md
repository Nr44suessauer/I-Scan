# I-Scan Control Software - Developer Quick Reference

**Purpose:** Fast lookup for developers working with either version  
**Format:** Condensed technical reference  
**Last Updated:** June 2025

---

## Quick Start Commands

```bash
# Original Version
cd Software_IScan
python main.py

# Modular Version  
cd "Modular Version"
python main_modular.py

# Batch Files
start_original_version.bat      # Original
start_modular_version.bat       # Modular
```

## File Structure Quick Map

```
┌─────────────────────────────────────────────────────────────────┐
│                      FILE ORGANIZATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ORIGINAL VERSION (Software_IScan/)                            │
│  ├── main.py                    # 🎯 Main app (1200+ lines)    │
│  ├── api_client.py             # 🌐 HTTP communication         │
│  ├── device_control.py         # 🔧 Hardware abstraction       │
│  ├── operation_queue.py        # 📋 Batch operations           │
│  ├── logger.py                 # 📝 Logging system             │
│  ├── webcam_helper.py          # 📷 Camera handling            │
│  ├── servo_angle_calculator.py # 📐 Angle calculations         │
│  └── angle_calculator_commands.py # 🧮 Calculator integration  │
│                                                                 │
│  MODULAR VERSION (Modular Version/)                            │
│  ├── main_modular.py           # 🎯 App controller (220 lines) │
│  ├── config.py                 # ⚙️ Configuration (43 lines)   │
│  ├── gui_components.py         # 🖼️ GUI factory (307 lines)    │
│  ├── event_handlers.py         # 🎮 Events (268 lines)         │
│  ├── queue_operations.py       # 📋 Queue logic (extracted)    │
│  └── [same support modules as original]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Common Tasks Cheat Sheet

### Adding New Hardware Component

#### Original Version:
```python
# In main.py (around line 200-300)
def setup_new_device_frame(self):
    # Create GUI elements
    pass

def on_new_device_execute(self):
    # Handle device operation  
    pass
```

#### Modular Version:
```python
# 1. config.py
DEFAULT_NEW_DEVICE_VALUE = "100"

# 2. gui_components.py
@staticmethod
def create_new_device_frame(parent, variables):
    # Create GUI elements
    return frame, widgets, vars

# 3. event_handlers.py
def on_new_device_execute(self):
    # Handle device operation
    pass

# 4. main_modular.py
self.new_device_frame = GUIBuilder.create_new_device_frame(...)
```

### Debug Locations

#### Original Version:
```python
# All debugging in main.py
def debug_issue(self):
    print(f"Debug: {self.variable}")
    self.logger.log("Debug message")
```

#### Modular Version:
```python
# Component-specific debugging
# config.py         → Settings issues
# gui_components.py → GUI problems  
# event_handlers.py → User interactions
# main_modular.py   → Application flow
```

## API Quick Reference

### Hardware Control Commands
```python
# Servo Control
api_client.send_servo_command(angle, speed)

# Stepper Control  
api_client.send_stepper_command(diameter, speed, distance, direction)

# LED Control
api_client.send_led_command(color_hex)
api_client.send_brightness_command(brightness_percent)

# Button Control
api_client.send_button_command(button_id)

# Home Command
api_client.send_home_command()
```

### Queue Operations
```python
# Add to queue
self.operation_queue.add_operation(command_dict)

# Execute queue
self.operation_queue.execute_all()

# Import/Export
self.operation_queue.import_from_csv(filename)
self.operation_queue.export_to_csv(filename)
```

## Common Patterns

### Error Handling
```python
# Both versions use similar pattern
try:
    response = api_client.send_command(params)
    if response.get('success'):
        self.update_status("Success")
    else:
        self.update_status(f"Error: {response.get('error')}")
except Exception as e:
    self.logger.log(f"Exception: {e}")
    self.update_status("Connection error")
```

### GUI Updates
```python
# Original Version
def update_gui_element(self, value):
    self.some_widget.config(text=value)
    self.status_var.set(f"Updated: {value}")

# Modular Version  
def update_gui_element(self, value):
    self.app.some_widget.config(text=value)
    self.app.status_var.set(f"Updated: {value}")
```

## Debugging Tips

### Original Version:
```python
# Add debug prints in main.py
print(f"DEBUG: Variable state = {self.variable}")

# Use logger
self.logger.log("Debug message")

# Check GUI state
print(f"GUI state: {self.some_var.get()}")
```

### Modular Version:
```python
# Component-specific debugging
# In event_handlers.py
def on_button_click(self):
    print(f"DEBUG: Button clicked, state = {self.app.variable}")

# In gui_components.py  
@staticmethod
def create_frame():
    print("DEBUG: Creating frame")
    # ...

# In main_modular.py
def init_components(self):
    print("DEBUG: Initializing components")
```

## Configuration Quick Ref

### Default Values (both versions):
```python
API_URL = "http://192.168.137.7"
STEPPER_DIAMETER = "28"
SERVO_SPEED = "80"  
LED_COLOR = "#B00B69"
LED_BRIGHTNESS = "69"
CAMERA_DEVICE = 0
```

### Modular Version Config Access:
```python
from config import DEFAULT_BASE_URL, DEFAULT_SPEED
# Use constants instead of hardcoded values
```

## Testing Strategies

### Original Version:
```python
# Integration testing only
python main.py  # Test full application
```

### Modular Version:
```python
# Unit testing possible
python -c "from gui_components import GUIBuilder; print('GUI OK')"
python -c "from config import *; print('Config OK')"

# Component testing
python -c "
import tkinter as tk
from gui_components import GUIBuilder
root = tk.Tk()
frame = GUIBuilder.create_servo_frame(root, {})
print('Servo frame created successfully')
"
```

## Performance Monitoring

### Memory Usage Check:
```python
import psutil
import os

# Get current process
process = psutil.Process(os.getpid())

# Memory info
memory_info = process.memory_info()
print(f"Memory: {memory_info.rss / 1024 / 1024:.1f} MB")
```

### Startup Time Measurement:
```python
import time
start_time = time.time()

# Application initialization here

init_time = time.time() - start_time
print(f"Startup time: {init_time:.2f} seconds")
```

## Common Issues & Solutions

### GUI Not Responding:
```python
# Both versions: Check for blocking operations
# Solution: Use threading for long operations
import threading
threading.Thread(target=long_operation, daemon=True).start()
```

### API Connection Issues:
```python
# Check network connectivity
import requests
try:
    response = requests.get(f"{base_url}/status", timeout=5)
    print(f"API Status: {response.status_code}")
except:
    print("API not reachable")
```

### Camera Issues:
```python
# Test camera availability
import cv2
cap = cv2.VideoCapture(0)  # Try device 0, 1, 2...
if cap.isOpened():
    print("Camera available")
    cap.release()
else:
    print("Camera not available")
```

---

## Emergency Contacts & Resources

- **Main Documentation:** `README.md` files in each version folder
- **Technical Docs:** `TECHNICAL_DOCUMENTATION.md` files
- **Architecture:** `ARCHITECTURE_COMPARISON.md`
- **Issue Tracking:** Check console output and log files
- **Hardware API:** Check device documentation for endpoint details
