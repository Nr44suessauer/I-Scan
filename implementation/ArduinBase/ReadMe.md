# Project Documentation: I-Scan

## Project Overview

This project controls various hardware components (stepper motor, servo, RGB LED, button) using an ESP32-S3 controller. Control is possible both locally and via a network (Wi-Fi), including a web server and API interfaces. Development is done with PlatformIO and the Arduino framework.

---

## Folder and File Structure

The project structure is as follows:

```
I-Scan/
│
├── API-Calls.md                # Documentation of available API endpoints (e.g., for Postman)
├── platformio.ini              # PlatformIO project configuration (board, framework, libraries)
├── ReadMe.md                   # (Location for this project documentation)
│
├── include/                    # Header files (function prototypes, definitions)
│   ├── button_control.h
│   ├── led_control.h
│   ├── motor.h
│   ├── network_client.h
│   ├── servo_control.h
│   ├── web_server.h
│   ├── wifi_manager.h
│   ├── WiFiServer.h
│
├── lib/                        # Custom or external libraries (optional, for larger projects)
│   └── README                  # Notes on using the lib folder
│
├── src/                        # Main logic implementation (C++ source code)
│   ├── button_control.cpp
│   ├── led_control.cpp
│   ├── main.cpp                # Program entry point (setup/loop)
│   ├── motor.cpp
│   ├── network_client.cpp
│   ├── servo_control.cpp
│   ├── web_server.cpp
│   ├── wifi_manager.cpp
│
└── data/                       # (Optional) Files for the SPIFFS file system (e.g., web server assets)
```

---

## Key Files and Their Purpose

- **platformio.ini**  
  Contains all settings for the PlatformIO project: board selection, framework, libraries, build options.

- **API-Calls.md**  
  Overview and examples for all HTTP API endpoints (e.g., control of servo, motor, LED, button status).

- **src/main.cpp**  
  Main program: initialization, setup, and loop. Connects the modules.

- **src/motor.cpp / include/motor.h**  
  Controls the stepper motor (e.g., 28BYJ-48): initialization, step logic, speed control.

- **src/servo_control.cpp / include/servo_control.h**  
  Controls a servo motor (e.g., for camera alignment).

- **src/led_control.cpp / include/led_control.h**  
  Controls an RGB LED (color, brightness, effects).

- **src/button_control.cpp / include/button_control.h**  
  Reads and debounces a button.

- **src/network_client.cpp / include/network_client.h**  
  Network communication as a client (e.g., heartbeat, data reception, reconnect logic).

- **src/web_server.cpp / include/web_server.h**  
  Implements a web server for local control and API endpoints.

- **src/wifi_manager.cpp / include/wifi_manager.h**  
  Wi-Fi management: connection setup, reconnect, status query.

- **data/**  
  (Optional) Static files for the web server (HTML, CSS, JS) to be uploaded to the ESP32 file system (SPIFFS).

---

## Settings & Configuration

- **Board & Framework:**  
  The board (e.g., `esp32-s3-devkitm-1`) and framework (`arduino`) are defined in `platformio.ini`.

- **Libraries:**  
  Dependencies are automatically detected by PlatformIO (see `lib/README`). Additional libraries can be added in `platformio.ini`.

- **Pin Assignment:**  
  Pin definitions for motor, LED, button, etc. can be found in the respective header files (`include/motor.h`, etc.).

- **Speed & Motor Control:**  
  The motor control is optimized for the 28BYJ-48 (e.g., `STEP_DELAY_MS`, `STEPS_PER_REVOLUTION` in `motor.h`).

- **Network:**  
  Wi-Fi credentials and server IP are configured in the code (usually in `wifi_manager.cpp` or `network_client.cpp`).

- **API:**  
  The HTTP API is documented in `API-Calls.md`. It enables control of all components over the network.

---

## Development & Extension

- **New hardware components** can be integrated by creating new modules (e.g., `sensor_control.cpp/h`).
- **Web server assets** are placed in the `data/` folder and uploaded to the ESP32 file system using PlatformIO.

---

## Notes

- Changes to pin assignments or hardware should always be documented in the header files.
- The API documentation (`API-Calls.md`) is essential for external control and should be kept up to date.

## Overview of Main Functions by Module

| Module/File                | Functions                                                                                 |
|---------------------------|------------------------------------------------------------------------------------------|
| **main.cpp**              | setup(), loop()                                                                           |
| **led_control.h/cpp**     | setupLEDs(), updateLEDs(), setColorByIndex(), setColorRGB(), setColorHSV(), setBrightness()|
| **servo_control.h/cpp**   | setupServo(), setServoAngle(), getServoAngle()                                            |
| **motor.h/cpp**           | setupMotor(), setMotorPins(), moveMotor(), moveMotorToPosition(), moveMotorWithSpeed()    |
| **button_control.h/cpp**  | setupButton(), getButtonState()                                                           |
| **wifi_manager.h/cpp**    | setupWiFi(), checkWiFiConnection()                                                        |
| **web_server.h/cpp**      | setupWebServer(), handleWebServerRequests(), handleRoot(), handleColorChange(),           |
|                           | handleHexColorChange(), handleServoControl(), handleMotorControl(),                       |
|                           | handleGetButtonState(), handleBrightness(), handleNotFound()                              |
| **network_client.h/cpp**  | (Network communication functions, e.g., send/receive data)                                |

