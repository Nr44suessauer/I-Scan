# Api-Window Documentation

## Feature Overview

- Control of a servo motor (0-90°)
- Control of a stepper motor with precise position determination
- LED control (color and brightness)
- Button status query
- Home function for calibrating the zero position
- Operation queue for longer sequences
- Real-time position display and status logging

---


## Code Structure

```
+---------------------+
|    ControlApp       |      Main class that manages the GUI and component coordination
+---------------------+
         |
         | uses
         v
+---------------------+
|      Logger         |      Logging of messages and status updates
+---------------------+
         ^
         | used by
         |
+---------------------+     +---------------------+
|   DeviceControl     |---->|     ApiClient       |      Hardware communication via REST API
+---------------------+     +---------------------+
         ^
         | used by
         |
+---------------------+
|   OperationQueue    |      Management of the operation queue
+---------------------+


+----------------------------------------------------------+
|                   Main Components                         |
+----------------------------------------------------------+
| ControlApp       | GUI and application coordination      |
| ApiClient        | Implements REST API calls             |
| Logger           | Logging & status tracking             |
| OperationQueue   | Queue for operations                  |
| DeviceControl    | Control of hardware components        |
+----------------------------------------------------------+

+----------------------------------------------------------+
|                 Hardware Control                          |
+----------------------------------------------------------+
| Servo           | Angle control (0-90°)                  |
| Stepper motor   | Precise positioning (steps)            |
| LED             | Color and brightness                   |
| Button          | Status query                           |
| Home function   | Calibration of zero position           |
+----------------------------------------------------------+
```

---


## Functions

```
ApiClient:
├── make_request()                  - Sends HTTP requests to the API
├── set_servo_angle()               - Controls servo motor
├── move_stepper()                  - Controls stepper motor
├── set_led_color()                 - Sets LED color
├── set_led_brightness()            - Sets LED brightness
├── get_button_state()              - Queries button status
└── is_button_pressed()             - Checks if button is pressed

Logger:
├── log()                           - Displays message in log window
└── _update_from_log()              - Updates position/angle from log messages

OperationQueue:
├── add()                           - Adds operation to queue
├── clear()                         - Clears queue
├── remove()                        - Removes operation from queue
├── update_display()                - Updates queue display
├── execute_all()                   - Executes all operations sequentially
└── _execute_home_function()        - Home function as part of queue

DeviceControl:
├── servo_cmd()                     - Executes servo command directly
├── stepper_cmd()                   - Executes stepper motor command directly
├── led_cmd()                       - Sets LED color directly
├── bright_cmd()                    - Sets LED brightness directly
├── button_cmd()                    - Queries button status directly
└── home_func()                     - Executes home function directly

ControlApp:
├── create_widgets()                - Creates GUI elements
├── create_*_frame()                - Creates various GUI frames
├── assign_callbacks()              - Assigns callback functions
├── update_position_label()         - Updates position display
├── add_*_to_queue()                - Adds operations to queue
├── execute_queue()                 - Executes queue
├── remove_selected_operation()     - Removes selected operation
└── run()                           - Starts main application loop
```



## Usage
0. Run the application
1. Configure API address
2. Set gear diameter (mm)
3. Execute individual commands directly or
4. Add operations to the queue and execute them sequentially