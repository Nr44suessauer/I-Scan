ControlScript/
├── start_modular_version.bat             # Main start script
├── CLEANUP_SUMMARY.md                    # This summary
├── Calculator_Angle_Maschine/            # 🧮 Math & Visualization Module
│   └── MathVisualisation/                # Visualization tools
│       ├── main.py                       # Main application (CSV export)
│       ├── calculations.py               # Core calculations
│       ├── config.py                     # Configuration
│       ├── export_commands.py            # Export functions
│       ├── save_servo_graph.py           # Save servo graph functionality
│       ├── servo_interpolation.py        # Servo interpolation logic
│       ├── README.md                     # Module documentation
│       ├── .gitignore                    # Git ignore file
│       └── visualizations/               # Visualization modules
│           ├── __init__.py               # Module initialization
│           ├── angle_progression.py      # Angle progression visualization
│           ├── calculation_table.py      # Calculation table visualization
│           ├── geometric.py              # Geometric visualization
│           ├── point_calculation.py      # Point calculations visualization
│           └── servo_interpolation.py    # Servo interpolation visualization
└── Modular Version/                      # 📹 Main Camera System
    ├── main_modular.py                   # Main application
    ├── README.md                         # Main documentation
    ├── requirements.txt                  # Python dependencies
    ├── config.py                         # Configuration
    ├── gui_components.py                 # GUI components
    ├── event_handlers.py                 # Event handlers
    ├── webcam_helper.py                  # Camera helper functions
    ├── api_client.py                     # API client
    ├── device_control.py                 # Device control logic
    ├── logger.py                         # Logging utility
    ├── operation_queue.py                # Operations queue management
    ├── queue_operations.py               # Queue operations
    ├── angle_calculator_commands.py      # Angle calculation commands
    ├── servo_angle_calculator.py         # Servo angle calculation
    ├── wizard_icon.png                   # Application icon
    └── camera/                           # Camera System
        ├── cameras_config.json           # JSON configuration for cameras
        ├── json_camera_config.py         # Configuration manager
        ├── json_camera_stream.py         # Stream manager
        ├── README.md                     # Camera documentation
        └── __init__.py                   # Module exports





## To Start the Camera System (Bash):
```bash
./start_modular_version.bat
```

## To Start the Mathematics Tool (Bash):
```bash
cd Calculator_Angle_Maschine/MathVisualisation
python main.py --help         # Display help message
python main.py --csv          # Generate CSV export
python main.py --visualize    # Start with visualization
```