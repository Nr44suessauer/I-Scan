## Concept of a Movable Camera Setup in the Z-Axis

This concept outlines a movable camera setup in the Z-axis, consisting of **three movable modules**, each equipped with a camera. The angle of each camera can be individually adjusted for flexible and precise recording.

### Components
1. **Movable Modules**: Three modules that can move along the Z-axis.
2. **Cameras**: Each unit is equipped with a camera of choice.
3. **Angle Adjustment**: Mechanism to change the camera angle.

### Functionality
- **Movement Along the Z-Axis**: The modules can move independently along the Z-axis to cover different heights and positions.
- **Adjustable Camera Angle**: The angle of each camera can be adjusted manually or automatically to ensure the optimal viewing angle for recording.

### Advantages
- **Flexibility**: The movable modules and adjustable camera angles allow the setup to adapt to various scenarios and requirements.

### Goals
- **3D Recording of Large Objects**: The setup aims to enable precise 3D recording of large objects and be compatible with various scenarios, regardless of size or measurement concept.
- **Scalability**: Four of these setups or a turntable tailored to the use case's size can be used.

<div style="display: flex; align-items: center; margin-top: 20px;">
    <p></p>
</div>

### Module Orientation

These modules will receive their "tasks" wirelessly. An external system will handle the creation and transmission of these tasks to the relevant module.

<div style="display: flex; align-items: center; margin-top: 20px;">
    <p></p>
</div>

<div style="display: flex;">
    <div style="flex: 1; padding-left: 10px;">
        <img src="https://github.com/Nr44suessauer/nr44suessauer.github.io/blob/main/assets/img/I-Scan/AufbauUndTeile.jpg?raw=true" alt="Setup and Components" style="width: 300px;">
    </div>
    <div style="flex: 1; padding-left: 0px;">
        To align the modules, three parameters are required: 
        <div style="display: flex; align-items: center; margin-top: 0px;">
    <p></p>
</div>
        <ul>
            <li>The absolute height of a module</li>
            <li>The relative height of the modules to each other (error prevention)</li>
            <li>Camera angle</li>
        </ul>
        These parameters are obtained through:
        <div style="display: flex; align-items: left; margin-top: 0px;">
    <p></p>
</div>
        <ul>
            <li>Lidar sensors mounted on each module or on the central one alone.</li>
            <li>End-stop switches at the bottom of each module, combined with stepper motors.</li>
        </ul>
        <div style="display: flex; align-items: center; margin-top: 0px;">
    <p></p>
</div>
        This requires an initialization process where all modules move to position 0 (end-stop = true).  
    </div>
</div>

### Connection and Control

The cameras will be connected via USB to the main system, which serves as the central control unit. The movement of the modules will also be controlled from this system, allowing for coordinated and efficient management of the entire camera setup.

### Subsystems and Management

The execution of individual processes for both the cameras and the modules can be handled by subsystems. These subsystems are designed as Docker containers that save the images on a shared partition.

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Architecture</title>
    <style>
        .container {
            display: flex;
            align-items: center;
        }
        .text {
            flex: 1;
            padding-right: 10px;
        }
        .image {
            flex: 1;
            padding-left: 0px;
        }
        img {
            width: 400px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image">
            <img src="https://github.com/Nr44suessauer/I-Scan/blob/main/docs/diagram/Architecture_Diagram/SystemArchitecture%20V2.0%20%20Bluetooth.png?raw=true" alt="Setup and Components">
        </div>
        <div class="text">
            <p>The execution of individual processes for both the cameras and the modules can be handled by subsystems. These subsystems are designed as Docker containers that save the images on a shared partition.</p>
            <p>A web server will allow configuration of the processes and the hardware used. The web server also provides access to the saved data. This management solution enables the integration of cameras with different requirements. In the long term, the system should also be usable for other measurement tools.</p>
        </div>
    </div>
</body>

