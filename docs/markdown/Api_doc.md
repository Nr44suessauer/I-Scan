# I-Scan API Documentation

This documentation describes the available API functions of the I-Scan software based on the modular version.

## API Client Functions

| Function | Description | Parameters | Return Values | Endpoint |
|----------|-------------|------------|---------------|----------|
| `make_request` | Sends an HTTP request to the specified API endpoint | `endpoint` (str): API endpoint<br>`params` (dict, optional): Parameters<br>`base_url` (str): Base URL<br>`timeout` (int): Timeout in seconds | str: API response or error message | Variable |
| `set_servo_angle` | Sets the servo angle via the API | `angle` (int): Angle 0-90 degrees<br>`base_url` (str): Base URL | str: Confirmation message with result | `/setServo` |
| `move_stepper` | Controls the stepper motor via the API | `steps` (int): Number of steps<br>`direction` (int): Direction (1=up, -1=down)<br>`speed` (int, optional): Speed<br>`base_url` (str): Base URL | str: Confirmation message with result | `/setMotor` |
| `set_led_color` | Sets the LED color via the API | `color_hex` (str): Hex color code (e.g. "#FF0000")<br>`base_url` (str): Base URL | str: Confirmation message with result | `/hexcolor` |
| `set_led_brightness` | Sets the LED brightness via the API | `brightness` (int): Brightness 0-100%<br>`base_url` (str): Base URL | str: Confirmation message with result | `/setBrightness` |
| `get_button_state` | Queries the button status via the API | `base_url` (str): Base URL<br>`nocache` (bool): Prevent caching | str: Button status response | `/getButtonState` |
| `is_button_pressed` | Checks if button is pressed based on API response | `response`: API response to check | bool: True if pressed, False otherwise | - |

## Device Control Functions

| Function | Description | Parameters | Return Values | Usage |
|----------|-------------|------------|---------------|-------|
| `servo_cmd` | Executes servo command directly | None (uses GUI values) | None (logs result) | Direct servo control |
| `servo_auto_position_cmd` | Automatic servo positioning based on Y-position | None (uses current position) | None (logs result) | Automatic alignment |
| `update_servo_target_center` | Updates target center for servo calculations | `center_x` (float): X coordinate<br>`center_y` (float): Y coordinate | None | Configuration |
| `stepper_cmd` | Executes stepper motor command directly | None (uses GUI values) | None (logs result) | Direct motor control |
| `led_cmd` | Sets LED color directly | None (uses GUI values) | None (logs result) | LED color control |
| `bright_cmd` | Sets LED brightness directly | None (uses GUI values) | None (logs result) | LED brightness control |
| `button_cmd` | Queries button status directly | None | None (logs status) | Button status query |
| `home_func` | Executes home function (reference movement) | None | None (logs result) | Initialization |

## Servo Angle Calculator Functions

| Function | Description | Parameters | Return Values | Purpose |
|----------|-------------|------------|---------------|---------|
| `calculate_servo_angle_from_position` | Calculates servo angle based on Y-position | `current_y_position` (float): Current Y position | int: Servo angle 0-90° | Position calculation |
| `calculate_targeting_angle` | Calculates direct targeting angle to target center | `current_y_position` (float): Current Y position | tuple: (angle_in_degrees, servo_angle) | Target acquisition |
| `get_angle_info` | Returns detailed information about angle calculation | `current_y_position` (float): Current Y position | dict: Detailed angle information | Debug/Analysis |
| `update_target_center` | Updates target center coordinates | `new_x` (float): New X coordinate<br>`new_y` (float): New Y coordinate | None | Configuration |
| `validate_servo_angle` | Checks if servo angle is valid | `angle` (int): Angle to check | bool: True if valid (0-90°) | Validation |

## Camera Configuration Functions

| Function | Description | Parameters | Return Values | Purpose |
|----------|-------------|------------|---------------|---------|
| `load_config` | Loads configuration from JSON file | None | bool: True on success | Initialization |
| `save_config` | Saves configuration to JSON file | None | bool: True on success | Persistence |
| `create_default_config` | Creates default configuration | None | None | Fallback |
| `get_cameras` | Gets all camera configurations | None | List[Dict]: Camera list | Query |
| `get_enabled_cameras` | Gets only enabled cameras | None | List[Dict]: Enabled cameras | Filtering |
| `get_camera_by_index` | Gets camera by index | `index` (int): Camera index | Optional[Dict]: Camera or None | Single query |
| `add_camera` | Adds new camera | `index` (int): Index<br>`verbindung` (str): Connection<br>`beschreibung` (str): Description<br>`name` (str, optional): Name | bool: True on success | Configuration |
| `update_camera` | Updates camera configuration | `index` (int): Index<br>`**kwargs`: Properties | bool: True on success | Modification |
| `remove_camera` | Removes camera from configuration | `index` (int): Index to remove | bool: True on success | Management |
| `parse_verbindung` | Parses connection string | `verbindung` (str): Connection string | Dict: Parsed connection data | Processing |

## Queue Operations Functions

| Function | Description | Parameters | Return Values | Purpose |
|----------|-------------|------------|---------------|---------|
| `add` | Adds operation to queue | `operation_type` (str): Operation type<br>`params` (dict): Parameters<br>`description` (str): Description | None | Queue management |
| `clear` | Empties the queue | None | None | Reset |
| `import_from_csv` | Imports operations from CSV file | `file_path` (str): Path to CSV file | bool: True on success | Import |
| `export_to_csv` | Exports operations to CSV file | `file_path` (str): Target path | bool: True on success | Export |
| `remove` | Removes operation by index | `index` (int): Index to remove | None | Single removal |
| `execute_all` | Executes all operations in queue | `base_url` (str): API URL<br>`widgets` (dict): GUI widgets<br>`position_var`: Position<br>`servo_angle_var`: Servo angle<br>`last_distance_value`: Last distance<br>`run_in_thread` (bool): Threading | None | Batch execution |
| `execute_single_operation` | Executes single operation | `operation`: Operation<br>`base_url` (str): API URL<br>Additional parameters like `execute_all` | None | Single execution |
| `pause_queue` | Pauses queue execution | None | None | Control |
| `resume_queue` | Resumes queue execution | None | None | Control |
| `stop_queue` | Stops queue execution | None | None | Control |

## Example Usage

```python
# Using the API Client
from api_client import ApiClient

# Set servo to 45°
result = ApiClient.set_servo_angle(45, "http://192.168.137.7")

# Move motor 100 steps upward
result = ApiClient.move_stepper(100, 1, 50, "http://192.168.137.7")

# Set LED to red
result = ApiClient.set_led_color("#FF0000", "http://192.168.137.7")
```