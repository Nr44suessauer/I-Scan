"""
Configuration and Constants for I-Scan Application
All default values and configuration constants in one place.
"""

 # Constants for default values and calculations
PI = 3.141592653589793

 # API Configuration
DEFAULT_BASE_URL = "http://192.168.137.7"

 # Hardware Defaults
DEFAULT_DIAMETER = "28"
DEFAULT_SPEED = "80"
DEFAULT_DISTANCE = "3.0"
DEFAULT_DIRECTION = "1"

 # LED Defaults
DEFAULT_LED_COLOR = "#B00B69"
DEFAULT_LED_BRIGHTNESS = "69"

 # Camera Defaults
DEFAULT_CAMERA_DEVICE = 0
DEFAULT_CAMERA_FRAME_SIZE = (320, 240)
DEFAULT_AUTOFOCUS_DELAY = 0.5

 # GUI Configuration
WINDOW_TITLE = "I-Scan Wizard"
ICON_FILENAME = "wizard_icon.png"

 # Button Colors
BUTTON_ADD_COLOR = "#b0c4de"
BUTTON_ADD_FG = "black"
BUTTON_FONT = ("Arial", 10, "bold")
BUTTON_ADD_WIDTH = 3

 # Queue Configuration
DEFAULT_REPEAT_QUEUE = False

 # File Extensions
CSV_EXTENSIONS = [("CSV files", "*.csv"), ("All files", "*.*")]
JSON_EXTENSIONS = [("JSON files", "*.json"), ("All files", "*.*")]
