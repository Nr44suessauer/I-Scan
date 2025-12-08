#include "web_server.h"
#include "servo_control.h" 
#include "motor.h" 
#include "button_control.h" // Include for button functionality
#include "advanced_motor.h" // Include for advanced motor control
#include "motor_28byj48.h" // Include for 28BYJ-48 motor control

// Function declarations
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();
void handleServoControl(); 
void handleMotorControl(); 
void handleGetButtonState(); // New function declaration for button status
void handleBrightness(); // New function declaration for brightness control
void handleSetHomingMode();     // Neue Funktion für Homing-Modus setzen
void handlePassButton(); // New function declaration for button pass functionality
void handle28BYJ48MotorControl(); // 28BYJ-48 motor control handler
void handle28BYJ48MotorStatus(); // 28BYJ-48 motor status handler




// WebServer configuration
const uint16_t HTTP_PORT = 80;
WebServer server(HTTP_PORT);

// Enhanced HTML interface for motor control
const char* html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ESP32 Advanced Motor Control</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 20px; background: #f4f4f4; }
    h1, h2, h3 { color: #333; }
    .container { max-width: 800px; margin: 0 auto; }
    
    /* Tab-Styling */
    .tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; border-radius: 5px 5px 0 0; }
    .tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; }
    .tab button:hover { background-color: #ddd; }
    .tab button.active { background-color: #ccc; }
    .tabcontent { display: none; padding: 20px; border: 1px solid #ccc; border-top: none; background-color: white; border-radius: 0 0 5px 5px; }
    .tabcontent.active { display: block; }
    
    /* Button-Styling */
    .btn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 20px 0; }
    .btn { display: block; width: 100%; padding: 15px; border: none; border-radius: 5px; color: white; font-size: 14px; cursor: pointer; transition: 0.3s; }
    .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .btn-primary { background-color: #2196F3; }
    .btn-success { background-color: #4CAF50; }
    .btn-warning { background-color: #FF9800; }
    .btn-danger { background-color: #f44336; }
    .btn-secondary { background-color: #6c757d; }
    
    /* Container-Styling */
    .control-container { margin: 20px 0; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .control-container h3 { margin-top: 0; color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
    
    /* Slider-Styling */
    .slider-container { margin: 15px 0; }
    .slider-wrapper { display: flex; align-items: center; justify-content: center; gap: 15px; flex-wrap: wrap; }
    input[type="range"] { flex: 1; min-width: 200px; max-width: 400px; height: 8px; border-radius: 5px; background: #ddd; outline: none; }
    input[type="range"]::-webkit-slider-thumb { appearance: none; width: 20px; height: 20px; border-radius: 50%; background: #2196F3; cursor: pointer; }
    input[type="range"]::-moz-range-thumb { width: 20px; height: 20px; border-radius: 50%; background: #2196F3; cursor: pointer; border: none; }
    
    /* Status Display */
    .status-display { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
    .status-item { background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3; }
    .status-label { font-weight: bold; color: #666; margin-bottom: 5px; }
    .status-value { font-size: 18px; color: #333; }
    
    /* Motor-specific Styles */
    .position-input { padding: 10px; font-size: 16px; width: 100px; text-align: center; border: 1px solid #ddd; border-radius: 4px; }
    
    /* LED Control Styles */
    .btn-red { background-color: #f44336; }
    .btn-green { background-color: #4CAF50; }
    .btn-blue { background-color: #2196F3; }
    .btn-yellow { background-color: #FFEB3B; color: black; }
    .btn-purple { background-color: #9C27B0; }
    .btn-orange { background-color: #FF9800; }
    .btn-white { background-color: #FFFFFF; color: black; border: 1px solid #ddd; }
    
    .color-preview { width: 50px; height: 50px; border-radius: 50%; margin: 10px auto; border: 1px solid #ddd; }
    .hex-input { padding: 10px; font-size: 16px; width: 140px; text-align: center; border: 1px solid #ddd; border-radius: 4px; }
    
    /* Toggle Switch Styles */
    .function-row { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }
    .switch-label { display: flex; align-items: center; gap: 10px; cursor: pointer; }
    .switch-text { font-weight: bold; color: #333; }
    .description { display: block; margin-top: 8px; font-size: 12px; color: #666; font-style: italic; }
    
    .slider-toggle { position: relative; width: 50px; height: 25px; background: #ccc; border-radius: 25px; transition: 0.3s; }
    .slider-toggle:before { content: ""; position: absolute; width: 21px; height: 21px; background: white; border-radius: 50%; top: 2px; left: 2px; transition: 0.3s; }
    input[type="checkbox"] { display: none; }
    input[type="checkbox"]:checked + .slider-toggle { background: #2196F3; }
    input[type="checkbox"]:checked + .slider-toggle:before { transform: translateX(25px); }
    
    /* Responsive Design */
    @media (max-width: 768px) {
      .container { padding: 10px; }
      .btn-grid { grid-template-columns: 1fr; }
      .status-display { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔧 ESP32 PositionUnit - Advanced Control</h1>
    
    <!-- Tab Navigation -->
    <div class="tab">
      <button class="tablinks active" onclick="openTab(event, 'MotorTab')">🔩 Motor Control</button>
      <button class="tablinks" onclick="openTab(event, 'Motor28BYJ48Tab')">⚙️ 28BYJ-48 Motor</button>
      <button class="tablinks" onclick="openTab(event, 'ServoTab')">🔄 Servo Control</button>
      <button class="tablinks" onclick="openTab(event, 'LEDTab')">💡 LED Control</button>
      <button class="tablinks" onclick="openTab(event, 'StatusTab')">📊 Status & Info</button>
    </div>

    <!-- Motor Control Tab -->
    <div id="MotorTab" class="tabcontent active">
      <h2>🔩 Advanced Stepper Motor Control</h2>
      
      <!-- Motor Status -->
      <div class="control-container">
        <h3>📊 Motor Status</h3>
        <div class="status-display" id="motorStatusDisplay">
          <div class="status-item">
            <div class="status-label">Position</div>
            <div class="status-value" id="currentPosition">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Target Position</div>
            <div class="status-value" id="targetPosition">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Speed</div>
            <div class="status-value" id="currentSpeed">60 RPM</div>
          </div>
          <div class="status-item">
            <div class="status-label">Status</div>
            <div class="status-value" id="motorStatus">Ready</div>
          </div>
        </div>
        <button class="btn btn-secondary" onclick="updateMotorStatus()">Update Status</button>
      </div>

      <!-- Speed Control -->
      <div class="control-container">
        <h3>⚡ Speed Control</h3>
        <div class="slider-wrapper">
          <label>Speed:</label>
          <input type="range" id="speedSlider" min="1" max="500" value="150" oninput="updateSpeedValue(this.value)">
          <span id="speedValue">100</span> RPM
        </div>
      </div>

      <!-- Positioning -->
      <div class="control-container">
        <h3>🎯 Absolute Positioning</h3>
        <div class="slider-wrapper">
          <label>Position:</label>
          <input type="range" id="positionSlider" min="-5000" max="5000" value="0" oninput="updatePositionValue(this.value)">
          <span id="positionValue">0</span> Steps
        </div>
        <div style="margin: 15px 0;">
          <input type="number" id="positionInput" class="position-input" placeholder="Position" value="0">
          <button class="btn btn-primary" onclick="moveToPosition()">Move to Position</button>
        </div>
      </div>

      <!-- Relative Movement -->
      <div class="control-container">
        <h3>➡️ Relative Movement</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="moveRelative(-1000)">⬅️ 1000 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(-100)">⬅️ 100 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(-10)">⬅️ 10 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(10)">➡️ 10 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(100)">➡️ 100 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(1000)">➡️ 1000 Steps</button>
        </div>
      </div>

      <!-- Advanced Functions -->
      <div class="control-container">
        <h3>🔧 Advanced Functions</h3>
        <div class="function-row">
          <span class="description">🏠 Home to Button: Motor homes to physical button</span>
        </div>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="homeToButton()">🏠 Home to Button</button>
        </div>
      </div>

      <!-- Button Pass Function -->
      <div class="control-container">
        <h3>🔄 Button Pass Function</h3>
        <div class="function-row">
          <span class="description">🎯 Pass Button Multiple Times: Motor passes the button a specified number of times</span>
        </div>
        <div style="margin: 15px 0; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: center;">
          <label>Pass Count:</label>
          <input type="number" id="passCountInput" class="position-input" placeholder="10" value="10" min="1" max="100">
          <button class="btn btn-warning" onclick="passButtonTimes()">🔄 Pass Button</button>
        </div>
        
        <!-- Pass Progress Display -->
        <div class="status-display">
          <div class="status-item">
            <div class="status-label">Target Passes</div>
            <div class="status-value" id="targetPassCount">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Current Passes</div>
            <div class="status-value" id="currentPassCount">0</div>
          </div>
        </div>
      </div>




    </div>

    <!-- 28BYJ-48 Motor Control Tab -->
    <div id="Motor28BYJ48Tab" class="tabcontent">
      <h2>⚙️ 28BYJ-48 Stepper Motor Control (GPIO 4-7)</h2>
      
      <!-- Motor Status -->
      <div class="control-container">
        <h3>📊 Motor Status</h3>
        <div class="status-display" id="motor28byj48StatusDisplay">
          <div class="status-item">
            <div class="status-label">Position</div>
            <div class="status-value" id="current28byj48Position">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Target Position</div>
            <div class="status-value" id="target28byj48Position">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Speed</div>
            <div class="status-value" id="current28byj48Speed">50%</div>
          </div>
          <div class="status-item">
            <div class="status-label">Status</div>
            <div class="status-value" id="motor28byj48Status">Ready</div>
          </div>
        </div>
        <button class="btn btn-secondary" onclick="update28BYJ48MotorStatus()">Update Status</button>
      </div>

      <!-- Speed Control -->
      <div class="control-container">
        <h3>⚡ Speed Control</h3>
        <div class="slider-wrapper">
          <label>Speed:</label>
          <input type="range" id="speed28byj48Slider" min="0" max="90" value="50" oninput="update28BYJ48SpeedValue(this.value)">
          <span id="speed28byj48Value">50</span>%
        </div>
      </div>

      <!-- Positioning -->
      <div class="control-container">
        <h3>🎯 Absolute Positioning</h3>
        <div class="slider-wrapper">
          <label>Position:</label>
          <input type="range" id="position28byj48Slider" min="-5000" max="5000" value="0" oninput="update28BYJ48PositionValue(this.value)">
          <span id="position28byj48Value">0</span> Steps
        </div>
        <div style="margin: 15px 0;">
          <input type="number" id="position28byj48Input" class="position-input" placeholder="Position" value="0">
          <button class="btn btn-primary" onclick="move28BYJ48ToPosition()">Move to Position</button>
        </div>
      </div>

      <!-- Relative Movement -->
      <div class="control-container">
        <h3>➡️ Relative Movement</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="move28BYJ48Relative(-1000)">⬅️ 1000 Steps</button>
          <button class="btn btn-success" onclick="move28BYJ48Relative(-100)">⬅️ 100 Steps</button>
          <button class="btn btn-success" onclick="move28BYJ48Relative(-10)">⬅️ 10 Steps</button>
          <button class="btn btn-success" onclick="move28BYJ48Relative(10)">➡️ 10 Steps</button>
          <button class="btn btn-success" onclick="move28BYJ48Relative(100)">➡️ 100 Steps</button>
          <button class="btn btn-success" onclick="move28BYJ48Relative(1000)">➡️ 1000 Steps</button>
        </div>
      </div>

      <!-- Degree Movement -->
      <div class="control-container">
        <h3>🔄 Degree Movement</h3>
        <div style="margin: 15px 0; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: center;">
          <label>Degrees:</label>
          <input type="number" id="degrees28byj48Input" class="position-input" placeholder="360" value="360" min="0" max="3600">
          <button class="btn btn-warning" onclick="move28BYJ48Degrees(1)">↻ Clockwise</button>
          <button class="btn btn-warning" onclick="move28BYJ48Degrees(-1)">↺ Counter-Clockwise</button>
        </div>
      </div>

      <!-- Advanced Functions -->
      <div class="control-container">
        <h3>🔧 Advanced Functions</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="home28BYJ48Motor()">🏠 Home Motor</button>
          <button class="btn btn-primary" onclick="calibrate28BYJ48Motor()">⚙️ Calibrate (Set as 0)</button>
          <button class="btn btn-danger" onclick="stop28BYJ48Motor()">⛔ Stop Motor</button>
        </div>
      </div>

      <!-- Pin Configuration -->
      <div class="control-container">
        <h3>📌 Pin Configuration</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 15px 0;">
          <div>
            <label>IN1 (GPIO):</label>
            <input type="number" id="pin28byj48_1" class="position-input" value="6" min="0" max="48" style="width: 80px;">
          </div>
          <div>
            <label>IN2 (GPIO):</label>
            <input type="number" id="pin28byj48_2" class="position-input" value="4" min="0" max="48" style="width: 80px;">
          </div>
          <div>
            <label>IN3 (GPIO):</label>
            <input type="number" id="pin28byj48_3" class="position-input" value="7" min="0" max="48" style="width: 80px;">
          </div>
          <div>
            <label>IN4 (GPIO):</label>
            <input type="number" id="pin28byj48_4" class="position-input" value="5" min="0" max="48" style="width: 80px;">
          </div>
        </div>
        <button class="btn btn-warning" onclick="apply28BYJ48PinConfig()">✅ Apply Pin Configuration</button>
        <div style="margin-top: 10px; font-size: 12px; color: #666;">
          Current Pins: <span id="current28byj48Pins">4, 5, 6, 7</span>
        </div>
      </div>
    </div>

    <!-- Servo Control Tab -->
    <div id="ServoTab" class="tabcontent">
      <h2>🔄 Servo Control</h2>
      
      <div class="control-container">
        <h3>Servo Positioning</h3>
        <div class="slider-wrapper">
          <label>Angle:</label>
          <input type="range" id="servoSlider" min="0" max="180" value="90" oninput="updateServoValue(this.value)">
          <span id="servoValue">90</span>°
        </div>
        <button class="btn btn-primary" onclick="setServoAngle()">Set Position</button>
      </div>
      
      <div class="control-container">
        <h3>Predefined Positions</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="setServoPreset(0)">0° (Left)</button>
          <button class="btn btn-success" onclick="setServoPreset(45)">45°</button>
          <button class="btn btn-success" onclick="setServoPreset(90)">90° (Center)</button>
          <button class="btn btn-success" onclick="setServoPreset(135)">135°</button>
          <button class="btn btn-success" onclick="setServoPreset(180)">180° (Right)</button>
        </div>
      </div>
    </div>

    <!-- LED Control Tab -->
    <div id="LEDTab" class="tabcontent">
      <h2>💡 LED Control</h2>
      
      <!-- Brightness -->
      <div class="control-container">
        <h3>Brightness</h3>
        <div class="slider-wrapper">
          <label>Brightness:</label>
          <input type="range" id="brightnessSlider" min="0" max="255" value="5" oninput="updateBrightnessValue(this.value)">
          <span id="brightnessValue">5</span>
        </div>
        <button class="btn btn-primary" onclick="setBrightness()">Set Brightness</button>
      </div>

      <!-- Custom Color -->
      <div class="control-container">
        <h3>Custom Color</h3>
        <div id="colorPreview" class="color-preview"></div>
        <input type="text" id="hexInput" class="hex-input" placeholder="#FF0000" maxlength="7" value="#FF0000"/>
        <button class="btn btn-primary" onclick="changeHexColor()">Set Color</button>
      </div>

      <!-- Predefined Colors -->
      <div class="control-container">
        <h3>Predefined Colors</h3>
        <div class="btn-grid">
          <button class="btn btn-red" onclick="changeColor(0)">Red</button>
          <button class="btn btn-green" onclick="changeColor(1)">Green</button>
          <button class="btn btn-blue" onclick="changeColor(2)">Blue</button>
          <button class="btn btn-yellow" onclick="changeColor(3)">Yellow</button>
          <button class="btn btn-purple" onclick="changeColor(4)">Purple</button>
          <button class="btn btn-orange" onclick="changeColor(5)">Orange</button>
          <button class="btn btn-white" onclick="changeColor(6)">White</button>
        </div>
      </div>
    </div>

    <!-- Status Tab -->
    <div id="StatusTab" class="tabcontent">
      <h2>📊 System Status & Information</h2>
      
      <!-- Button Status -->
      <div class="control-container">
        <h3>Button Status (Pin 45)</h3>
        <div class="status-display">
          <div class="status-item">
            <div class="status-label">Status</div>
            <div class="status-value" id="buttonStatus">Not pressed</div>
          </div>
        </div>
        <button class="btn btn-secondary" onclick="refreshButtonStatus()">Update Status</button>
      </div>

      <!-- System Information -->
      <div class="control-container">
        <h3>System Information</h3>
        <div class="status-display">
          <div class="status-item">
            <div class="status-label">Motor Pins</div>
            <div class="status-value">Dir: 36, Step: 37</div>
          </div>
          <div class="status-item">
            <div class="status-label">Servo Pin</div>
            <div class="status-value">Pin 2</div>
          </div>
          <div class="status-item">
            <div class="status-label">LED Pins</div>
            <div class="status-value">R:48, G:35, B:36</div>
          </div>
          <div class="status-item">
            <div class="status-label">Button Pin</div>
            <div class="status-value">Pin 45</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Display -->
    <div style="position: fixed; bottom: 20px; left: 20px; right: 20px; background: #333; color: white; padding: 10px; border-radius: 5px; z-index: 1000;">
      <span id="status">Status: System ready</span>
    </div>
  </div>
  
  <script>
    // Globale Variablen
    let motorStatusInterval;
    let isPassingActive = false;
    
    // Tab-Funktionalität
    function openTab(evt, tabName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
      }
      document.getElementById(tabName).classList.add("active");
      evt.currentTarget.classList.add("active");
      
      // Update motor status automatically when Motor tab is opened
      if (tabName === 'MotorTab') {
        startMotorStatusUpdates();
      } else {
        stopMotorStatusUpdates();
      }
    }
    
    // Update motor status automatically with dynamic interval
    function startMotorStatusUpdates() {
      updateMotorStatus();
      if (motorStatusInterval) clearInterval(motorStatusInterval);
      // Verwende schnelleres Intervall wenn Button-Pass aktiv ist
      const interval = isPassingActive ? 500 : 2000; // 500ms vs 2000ms
      motorStatusInterval = setInterval(updateMotorStatus, interval);
    }
    
    // Restart updates with new interval
    function restartMotorStatusUpdates() {
      if (motorStatusInterval) {
        startMotorStatusUpdates();
      }
    }
    
    function stopMotorStatusUpdates() {
      if (motorStatusInterval) {
        clearInterval(motorStatusInterval);
        motorStatusInterval = null;
      }
    }
    
    // Page Load Event
    document.addEventListener('DOMContentLoaded', function() {
      updateColorPreview();
      refreshButtonStatus();
      updateMotorStatus();
      startMotorStatusUpdates();
    });
    
    // Motor Functions
    function updateSpeedValue(val) {
      document.getElementById('speedValue').textContent = val;
    }
    
    function updatePositionValue(val) {
      document.getElementById('positionValue').textContent = val;
      document.getElementById('positionInput').value = val;
    }
    
    function updateMotorStatus() {
      fetch('/motorStatus')
        .then(response => response.json())
        .then(data => {
          document.getElementById('currentPosition').textContent = data.currentPosition || 0;
          document.getElementById('targetPosition').textContent = data.targetPosition || 0;
          document.getElementById('currentSpeed').textContent = (data.currentSpeed || 60) + ' RPM';
          
          // Pass-Status aktualisieren
          document.getElementById('targetPassCount').textContent = data.targetPassCount || 0;
          document.getElementById('currentPassCount').textContent = data.currentPassCount || 0;
          
          // Prüfe ob sich der Pass-Status geändert hat
          const wasPassingActive = isPassingActive;
          isPassingActive = data.isPassingButton || false;
          
          // Restart updates with new interval if status changed
          if (wasPassingActive !== isPassingActive) {
            restartMotorStatusUpdates();
          }
          
          // Status-Text je nach Zustand
          let statusText = 'Ready';
          
          if (data.isPassingButton) {
              statusText = 'Passing Button (' + (data.currentPassCount || 0) + '/' + (data.targetPassCount || 0) + ')';
          } else if (data.isMoving) {
              statusText = 'Moving';
          } else if (data.isHomed) {
              statusText = 'Ready (Home)';
          }
          
          document.getElementById('motorStatus').textContent = statusText;
        })
        .catch(error => {
          console.error('Error retrieving motor status:', error);
        });
    }
    
    function moveToPosition() {
      const position = parseInt(document.getElementById('positionInput').value) || 0;
      const speed = parseInt(document.getElementById('speedSlider').value) || 60;
      
      document.getElementById('status').innerHTML = 'Status: Motor moving to position ' + position + '...';
      
      fetch('/advancedMotor?action=moveTo&position=' + position + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in positioning';
        });
    }
    
    function moveRelative(steps) {
      const speed = parseInt(document.getElementById('speedSlider').value); 
      
      document.getElementById('status').innerHTML = 'Status: Motor moving ' + steps + ' steps...';
      
      fetch('/advancedMotor?action=moveRelative&steps=' + steps + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in relative movement';
        });
    }
    
    // function homeMotor() {
    //   document.getElementById('status').innerHTML = 'Status: Motor moving to home position...';
    //   
    //   // Geschwindigkeit vom Speed-Slider übernehmen
    //   const speed = document.getElementById('speedSlider').value;
    //   
    //   fetch('/motorHome?speed=' + speed)
    //     .then(response => response.text())
    //     .then(data => {
    //       document.getElementById('status').innerHTML = 'Status: ' + data;
    //       updateMotorStatus();
    //     })
    //     .catch(error => {
    //       document.getElementById('status').innerHTML = 'Status: Error moving to home';
    //     });
    // }
    
    function homeToButton() {
      document.getElementById('status').innerHTML = 'Status: Motor homing to button position...';
      
      // Geschwindigkeit vom Speed-Slider übernehmen
      const speed = document.getElementById('speedSlider').value;
      
      fetch('/motorHome?speed=' + speed + '&type=button')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error homing to button';
        });
    }
    
    function passButtonTimes() {
      const count = parseInt(document.getElementById('passCountInput').value) || 10;
      const speed = document.getElementById('speedSlider').value;
      
      if (count < 1 || count > 100) {
        document.getElementById('status').innerHTML = 'Status: Pass count must be between 1 and 100';
        return;
      }
      
      document.getElementById('status').innerHTML = 'Status: Motor passing button ' + count + ' times...';
      
      // Aktiviere sofort den schnellen Aktualisierungsmodus
      isPassingActive = true;
      restartMotorStatusUpdates();
      
      fetch('/passButton?count=' + count + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          // Force immediate update after completion
          setTimeout(updateMotorStatus, 100);
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error passing button';
          // Reset passing state on error
          isPassingActive = false;
          restartMotorStatusUpdates();
        });
    }
    
    // function calibrateMotor() {
    //   document.getElementById('status').innerHTML = 'Status: Setting virtual home position...';
    //   
    //   fetch('/motorCalibrate')
    //     .then(response => response.text())
    //     .then(data => {
    //       document.getElementById('status').innerHTML = 'Status: ' + data;
    //       updateMotorStatus();
    //     })
    //     .catch(error => {
    //       document.getElementById('status').innerHTML = 'Status: Error setting virtual home';
    //     });
    // }
    

    

    

    
    function stopMotor() {
      document.getElementById('status').innerHTML = 'Status: Motor stopping...';
      
      fetch('/motorStop')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error stopping motor';
        });
    }
    
    // Homing mode toggle removed - using virtual home only
    

    
    // Servo Functions
    function updateServoValue(val) {
      document.getElementById('servoValue').textContent = val;
    }
    
    function setServoAngle() {
      const angle = document.getElementById('servoSlider').value;
      document.getElementById('status').innerHTML = 'Status: Servo positioning...';
      
      fetch('/setServo?angle=' + angle)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in servo control';
        });
    }
    
    function setServoPreset(angle) {
      document.getElementById('servoSlider').value = angle;
      document.getElementById('servoValue').textContent = angle;
      setServoAngle();
    }
    
    // LED Functions
    function updateBrightnessValue(val) {
      document.getElementById('brightnessValue').textContent = val;
    }
    
    function setBrightness() {
      const brightness = document.getElementById('brightnessSlider').value;
      document.getElementById('status').innerHTML = 'Status: Setting brightness...';
      
      fetch('/setBrightness?value=' + brightness)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error setting brightness';
        });
    }
    
    function updateColorPreview() {
      var hexValue = document.getElementById('hexInput').value;
      if (hexValue.charAt(0) !== '#') {
        hexValue = '#' + hexValue;
        document.getElementById('hexInput').value = hexValue;
      }
      document.getElementById('colorPreview').style.backgroundColor = hexValue;
    }
    
    function changeColor(colorIndex) {
      document.getElementById('status').innerHTML = 'Status: Changing color...';
      fetch('/color?index=' + colorIndex)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error changing color';
        });
    }
    
    function changeHexColor() {
      var hexValue = document.getElementById('hexInput').value;
      if (hexValue.charAt(0) !== '#') {
        hexValue = '#' + hexValue;
      }
      
      document.getElementById('status').innerHTML = 'Status: Changing color...';
      fetch('/hexcolor?hex=' + encodeURIComponent(hexValue))
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error changing color';
        });
    }
    
    // Button Status
    function refreshButtonStatus() {
      fetch('/getButtonState')
        .then(response => response.json())
        .then(data => {
          const buttonStatus = document.getElementById('buttonStatus');
          buttonStatus.textContent = data.pressed ? 'Pressed' : 'Not pressed';
        })
        .catch(error => {
          console.error('Error retrieving button status:', error);
        });
    }
    
    // Color preview event listener
    document.addEventListener('DOMContentLoaded', function() {
      const hexInput = document.getElementById('hexInput');
      if (hexInput) {
        hexInput.addEventListener('input', updateColorPreview);
      }
    });
    
    // 28BYJ-48 Motor Functions
    function update28BYJ48SpeedValue(val) {
      document.getElementById('speed28byj48Value').textContent = val;
    }
    
    function update28BYJ48PositionValue(val) {
      document.getElementById('position28byj48Value').textContent = val;
      document.getElementById('position28byj48Input').value = val;
    }
    
    function update28BYJ48MotorStatus() {
      fetch('/motor28byj48Status')
        .then(response => response.json())
        .then(data => {
          document.getElementById('current28byj48Position').textContent = data.currentPosition || 0;
          document.getElementById('target28byj48Position').textContent = data.targetPosition || 0;
          document.getElementById('current28byj48Speed').textContent = (data.currentSpeed || 50) + '%';
          
          // Update pin display and inputs
          if (data.pin1 !== undefined) {
            document.getElementById('current28byj48Pins').textContent = 
              data.pin1 + ', ' + data.pin2 + ', ' + data.pin3 + ', ' + data.pin4;
            document.getElementById('pin28byj48_1').value = data.pin1;
            document.getElementById('pin28byj48_2').value = data.pin2;
            document.getElementById('pin28byj48_3').value = data.pin3;
            document.getElementById('pin28byj48_4').value = data.pin4;
          }
          
          let statusText = 'Ready';
          if (data.isMoving) {
              statusText = 'Moving';
          } else if (data.isHomed) {
              statusText = 'Ready (Homed)';
          }
          
          document.getElementById('motor28byj48Status').textContent = statusText;
        })
        .catch(error => {
          console.error('Error retrieving 28BYJ-48 motor status:', error);
        });
    }
    
    function move28BYJ48ToPosition() {
      const position = parseInt(document.getElementById('position28byj48Input').value) || 0;
      
      document.getElementById('status').innerHTML = 'Status: 28BYJ-48 Motor moving to position ' + position + '...';
      
      fetch('/motor28byj48?action=moveToPosition&position=' + position)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in 28BYJ-48 positioning';
        });
    }
    
    function move28BYJ48Relative(steps) {
      const speed = parseInt(document.getElementById('speed28byj48Slider').value);
      const direction = steps > 0 ? 1 : -1;
      
      document.getElementById('status').innerHTML = 'Status: 28BYJ-48 Motor moving ' + steps + ' steps...';
      
      fetch('/motor28byj48?action=moveRelative&steps=' + Math.abs(steps) + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in 28BYJ-48 relative movement';
        });
    }
    
    function move28BYJ48Degrees(direction) {
      const degrees = parseFloat(document.getElementById('degrees28byj48Input').value) || 360;
      const speed = parseInt(document.getElementById('speed28byj48Slider').value);
      
      document.getElementById('status').innerHTML = 'Status: 28BYJ-48 Motor rotating ' + degrees + ' degrees...';
      
      fetch('/motor28byj48?action=moveDegrees&degrees=' + degrees + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in 28BYJ-48 degree movement';
        });
    }
    
    function home28BYJ48Motor() {
      document.getElementById('status').innerHTML = 'Status: 28BYJ-48 Motor moving to home position...';
      
      fetch('/motor28byj48?action=home')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error homing 28BYJ-48 motor';
        });
    }
    
    function calibrate28BYJ48Motor() {
      document.getElementById('status').innerHTML = 'Status: Calibrating 28BYJ-48 Motor...';
      
      fetch('/motor28byj48?action=calibrate')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error calibrating 28BYJ-48 motor';
        });
    }
    
    function stop28BYJ48Motor() {
      document.getElementById('status').innerHTML = 'Status: Stopping 28BYJ-48 Motor...';
      
      fetch('/motor28byj48?action=stop')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          update28BYJ48MotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error stopping 28BYJ-48 motor';
        });
    }
    
    function apply28BYJ48PinConfig() {
      const pin1 = parseInt(document.getElementById('pin28byj48_1').value);
      const pin2 = parseInt(document.getElementById('pin28byj48_2').value);
      const pin3 = parseInt(document.getElementById('pin28byj48_3').value);
      const pin4 = parseInt(document.getElementById('pin28byj48_4').value);
      
      if (pin1 < 0 || pin1 > 48 || pin2 < 0 || pin2 > 48 || 
          pin3 < 0 || pin3 > 48 || pin4 < 0 || pin4 > 48) {
        document.getElementById('status').innerHTML = 'Status: Invalid pin numbers (0-48)';
        return;
      }
      
      document.getElementById('status').innerHTML = 'Status: Applying pin configuration...';
      
      fetch('/motor28byj48?action=setPins&pin1=' + pin1 + '&pin2=' + pin2 + '&pin3=' + pin3 + '&pin4=' + pin4)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          document.getElementById('current28byj48Pins').textContent = pin1 + ', ' + pin2 + ', ' + pin3 + ', ' + pin4;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error applying pin configuration';
        });
    }
    
    function test28BYJ48CurrentPins() {
      const pin1 = parseInt(document.getElementById('pin28byj48_1').value);
      const pin2 = parseInt(document.getElementById('pin28byj48_2').value);
      const pin3 = parseInt(document.getElementById('pin28byj48_3').value);
      const pin4 = parseInt(document.getElementById('pin28byj48_4').value);
      const testSteps = parseInt(document.getElementById('testSteps28byj48').value) || 50;
      const testDelay = parseInt(document.getElementById('testDelay28byj48').value) || 5;
      
      document.getElementById('status').innerHTML = 'Status: Testing pins ' + pin1 + ', ' + pin2 + ', ' + pin3 + ', ' + pin4 + '...';
      
      fetch('/motor28byj48?action=testPins&pin1=' + pin1 + '&pin2=' + pin2 + '&pin3=' + pin3 + '&pin4=' + pin4 + 
            '&testSteps=' + testSteps + '&testDelay=' + testDelay)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data + ' - Hat sich der Motor bewegt?';
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error testing pins';
        });
    }
    
    function confirmPinConfiguration() {
      const pin1 = parseInt(document.getElementById('pin28byj48_1').value);
      const pin2 = parseInt(document.getElementById('pin28byj48_2').value);
      const pin3 = parseInt(document.getElementById('pin28byj48_3').value);
      const pin4 = parseInt(document.getElementById('pin28byj48_4').value);
      
      if (confirm('Bestätige Pins ' + pin1 + ', ' + pin2 + ', ' + pin3 + ', ' + pin4 + ' als korrekte Konfiguration?')) {
        apply28BYJ48PinConfig();
      }
    }
    
    // Auto-Test Funktionen
    let autoTestInterval = null;
    let testResults = [];
    let currentTestNumber = 0;
    
    function startAutoTest28BYJ48() {
      const pinList = document.getElementById('autoPinList28byj48').value;
      const testSteps = parseInt(document.getElementById('autoTestSteps28byj48').value) || 50;
      const testDelay = parseInt(document.getElementById('autoTestDelay28byj48').value) || 5;
      const betweenDelay = parseInt(document.getElementById('autoTestBetweenDelay28byj48').value) || 1000;
      const timeout = parseInt(document.getElementById('autoTestTimeout28byj48').value) || 10;
      
      if (!pinList) {
        document.getElementById('status').innerHTML = 'Status: Bitte Pin-Liste eingeben';
        return;
      }
      
      // Reset results
      testResults = [];
      currentTestNumber = 0;
      document.getElementById('testResultsBody').innerHTML = '';
      
      document.getElementById('status').innerHTML = 'Status: Starte Auto-Test...';
      document.getElementById('autoTestBtn').disabled = true;
      
      fetch('/motor28byj48?action=autoTest&pins=' + encodeURIComponent(pinList) + 
            '&testSteps=' + testSteps + '&testDelay=' + testDelay + '&betweenDelay=' + betweenDelay +
            '&timeout=' + timeout)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          // Starte Polling für Feedback-Anfragen
          startAutoTestPolling();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error starting auto-test';
          document.getElementById('autoTestBtn').disabled = false;
        });
    }
    
    function startAutoTestPolling() {
      autoTestInterval = setInterval(checkAutoTestStatus, 500);
    }
    
    function addManualPinCombo() {
      const pin1 = parseInt(document.getElementById('manualPin1').value);
      const pin2 = parseInt(document.getElementById('manualPin2').value);
      const pin3 = parseInt(document.getElementById('manualPin3').value);
      const pin4 = parseInt(document.getElementById('manualPin4').value);
      
      if (isNaN(pin1) || isNaN(pin2) || isNaN(pin3) || isNaN(pin4)) {
        alert('Bitte alle Pin-Nummern eingeben');
        return;
      }
      
      if (pin1 < 0 || pin1 > 48 || pin2 < 0 || pin2 > 48 || 
          pin3 < 0 || pin3 > 48 || pin4 < 0 || pin4 > 48) {
        alert('Pin-Nummern müssen zwischen 0 und 48 liegen');
        return;
      }
      
      addTestResult(pin1, pin2, pin3, pin4, 'Manuell');
      document.getElementById('status').innerHTML = 'Status: Kombination zur Liste hinzugefügt';
    }
    
    function addManualPinCombo() {
      const pin1 = parseInt(document.getElementById('manualPin1').value);
      const pin2 = parseInt(document.getElementById('manualPin2').value);
      const pin3 = parseInt(document.getElementById('manualPin3').value);
      const pin4 = parseInt(document.getElementById('manualPin4').value);
      
      if (isNaN(pin1) || isNaN(pin2) || isNaN(pin3) || isNaN(pin4)) {
        alert('Bitte alle Pin-Nummern eingeben');
        return;
      }
      
      if (pin1 < 0 || pin1 > 48 || pin2 < 0 || pin2 > 48 || 
          pin3 < 0 || pin3 > 48 || pin4 < 0 || pin4 > 48) {
        alert('Pin-Nummern müssen zwischen 0 und 48 liegen');
        return;
      }
      
      addTestResult(pin1, pin2, pin3, pin4, 'Manuell');
      document.getElementById('status').innerHTML = 'Status: Kombination zur Liste hinzugefügt';
    }
    
    function addDefaultCombos() {
      clearTestResults();
      addTestResult(6, 4, 7, 5, 'Standard');
      addTestResult(5, 7, 4, 6, 'Umgekehrt');
      addTestResult(6, 7, 4, 5, 'Variante 1');
      addTestResult(5, 4, 7, 6, 'Variante 2');
      addTestResult(4, 6, 5, 7, 'Variante 3');
      addTestResult(7, 5, 6, 4, 'Variante 4');
      document.getElementById('status').innerHTML = 'Status: Standard-Kombinationen geladen';
    }
    
    function addTestResult(pin1, pin2, pin3, pin4, status) {
      currentTestNumber++;
      testResults.push({num: currentTestNumber, pin1, pin2, pin3, pin4, status});
      
      const tbody = document.getElementById('testResultsBody');
      const row = tbody.insertRow();
      row.style.cursor = 'pointer';
      row.style.borderBottom = '1px solid #eee';
      row.onmouseover = function() { this.style.background = '#f5f5f5'; };
      row.onmouseout = function() { this.style.background = 'white'; };
      
      const statusColor = status === 'Erfolgreich' ? '#4CAF50' : 
                          status === 'Abgelehnt' ? '#f44336' : 
                          status === 'Manuell' ? '#2196F3' : '#ff9800';
      const statusIcon = status === 'Erfolgreich' ? '✓' : 
                         status === 'Abgelehnt' ? '✗' : 
                         status === 'Manuell' ? '✏️' : '⏱';
      
      row.innerHTML = 
        '<td style="padding: 8px;">' + currentTestNumber + '</td>' +
        '<td style="padding: 8px; text-align: center; font-weight: bold;">' + pin1 + '</td>' +
        '<td style="padding: 8px; text-align: center; font-weight: bold;">' + pin2 + '</td>' +
        '<td style="padding: 8px; text-align: center; font-weight: bold;">' + pin3 + '</td>' +
        '<td style="padding: 8px; text-align: center; font-weight: bold;">' + pin4 + '</td>' +
        '<td style="padding: 8px; text-align: center; color: ' + statusColor + ';">' + statusIcon + ' ' + status + '</td>' +
        '<td style="padding: 8px; text-align: center;">' +
        '<button class="btn btn-primary" style="padding: 5px 10px; font-size: 12px;" onclick="selectPinCombination(' + 
        pin1 + ',' + pin2 + ',' + pin3 + ',' + pin4 + ')">Übernehmen</button></td>';
    }
    
    function clearTestResults() {
      testResults = [];
      currentTestNumber = 0;
      document.getElementById('testResultsBody').innerHTML = '';
      document.getElementById('status').innerHTML = 'Status: Ergebnisse gelöscht';
    }
    
    function selectPinCombination(pin1, pin2, pin3, pin4) {
      document.getElementById('pin28byj48_1').value = pin1;
      document.getElementById('pin28byj48_2').value = pin2;
      document.getElementById('pin28byj48_3').value = pin3;
      document.getElementById('pin28byj48_4').value = pin4;
      
      if (confirm('Pins ' + pin1 + ', ' + pin2 + ', ' + pin3 + ', ' + pin4 + ' übernehmen und anwenden?')) {
        apply28BYJ48PinConfig();
      }
    }
    
    function checkAutoTestStatus() {
      fetch('/motor28byj48?action=checkAutoTest')
        .then(response => response.json())
        .then(data => {
          if (data.waitingForFeedback) {
            // Zeige Feedback-Dialog
            document.getElementById('currentTestPins').textContent = 
              data.pin1 + ', ' + data.pin2 + ', ' + data.pin3 + ', ' + data.pin4;
            document.getElementById('autoTestFeedback').style.display = 'block';
            
            // Store current combination for results table
            window.currentTestCombo = {pin1: data.pin1, pin2: data.pin2, pin3: data.pin3, pin4: data.pin4};
          } else if (data.testComplete) {
            // Test abgeschlossen
            clearInterval(autoTestInterval);
            document.getElementById('autoTestFeedback').style.display = 'none';
            document.getElementById('autoTestBtn').disabled = false;
            
            if (data.success) {
              document.getElementById('status').innerHTML = 
                'Status: ✓ Auto-Test erfolgreich! Pins: ' + 
                data.pin1 + ', ' + data.pin2 + ', ' + data.pin3 + ', ' + data.pin4;
              update28BYJ48MotorStatus();
            } else {
              document.getElementById('status').innerHTML = 
                'Status: Auto-Test abgeschlossen - keine korrekte Kombination gefunden';
            }
          }
        })
        .catch(error => {
          console.error('Error checking auto-test status:', error);
        });
    }
    
    function confirmAutoTest() {
      if (window.currentTestCombo) {
        addTestResult(window.currentTestCombo.pin1, window.currentTestCombo.pin2, 
                      window.currentTestCombo.pin3, window.currentTestCombo.pin4, 'Erfolgreich');
      }
      fetch('/motor28byj48?action=confirmAutoTest')
        .then(response => response.text())
        .then(data => {
          document.getElementById('autoTestFeedback').style.display = 'none';
        });
    }
    
    function rejectAutoTest() {
      if (window.currentTestCombo) {
        addTestResult(window.currentTestCombo.pin1, window.currentTestCombo.pin2, 
                      window.currentTestCombo.pin3, window.currentTestCombo.pin4, 'Abgelehnt');
      }
      fetch('/motor28byj48?action=rejectAutoTest')
        .then(response => response.text())
        .then(data => {
          document.getElementById('autoTestFeedback').style.display = 'none';
        });
    }
    
    // Keyboard shortcuts for quick feedback
    document.addEventListener('keydown', function(event) {
      const feedbackVisible = document.getElementById('autoTestFeedback').style.display === 'block';
      if (!feedbackVisible) return;
      
      if (event.key === 'y' || event.key === 'Y' || event.key === 'j' || event.key === 'J') {
        confirmAutoTest();
        event.preventDefault();
      } else if (event.key === 'n' || event.key === 'N') {
        rejectAutoTest();
        event.preventDefault();
      }
    });
  </script>
</body>
</html>
)rawliteral";

void setupWebServer() {
  // Set up web server routes
  server.on("/", HTTP_GET, handleRoot);
  server.on("/color", HTTP_GET, handleColorChange);
  server.on("/hexcolor", HTTP_GET, handleHexColorChange); 
  server.on("/setServo", HTTP_GET, handleServoControl);
  server.on("/setMotor", HTTP_GET, handleMotorControl);
  server.on("/getButtonState", HTTP_GET, handleGetButtonState); // Button status handler
  server.on("/setBrightness", HTTP_GET, handleBrightness); // New brightness handler
  
  // Advanced Motor Routes
  server.on("/advancedMotor", HTTP_GET, handleAdvancedMotorControl);
  server.on("/motorStatus", HTTP_GET, handleAdvancedMotorStatus);
  server.on("/motorStop", HTTP_GET, handleAdvancedMotorStop);
  server.on("/motorHome", HTTP_GET, handleAdvancedMotorHome);
  server.on("/motorJog", HTTP_GET, handleAdvancedMotorJog);
  server.on("/motorCalibrate", HTTP_GET, handleAdvancedMotorCalibrate);
  server.on("/setHomingMode", HTTP_GET, handleSetHomingMode);               // Neue Route für Homing-Modus
  server.on("/passButton", HTTP_GET, handlePassButton);                      // Neue Route für Button-Passagen

  // 28BYJ-48 Motor Routes
  server.on("/motor28byj48", HTTP_GET, handle28BYJ48MotorControl);
  server.on("/motor28byj48Status", HTTP_GET, handle28BYJ48MotorStatus);

  
  server.onNotFound(handleNotFound);

  // Start web server
  server.begin();
  Serial.println("HTTP server started on port " + String(HTTP_PORT));
}

// Handle incoming client requests
void handleWebServerRequests() {
  server.handleClient();
}

// Handle root route
void handleRoot() {
  server.send(200, "text/html", html);
}

// Handle color change request with predefined colors
void handleColorChange() {
  if (server.hasArg("index")) {
    int colorIndex = server.arg("index").toInt();
    setColorByIndex(colorIndex);
    server.send(200, "text/plain", "Color changed to index " + String(colorIndex));
  } else {
    server.send(400, "text/plain", "Missing 'index' parameter");
  }
}

// Handle hex color change request
void handleHexColorChange() {
  if (server.hasArg("hex")) {
    String hexColor = server.arg("hex");
    
    // Remove # if present
    if (hexColor.startsWith("#")) {
      hexColor = hexColor.substring(1);
    }
    
    // Parse hex values
    uint32_t rgbColor = strtoul(hexColor.c_str(), NULL, 16);
    int r = (rgbColor >> 16) & 0xFF;
    int g = (rgbColor >> 8) & 0xFF;
    int b = rgbColor & 0xFF;
    
    // Set color
    setColorRGB(r, g, b);
    
    server.send(200, "text/plain", "Color changed to #" + hexColor);
  } else {
    server.send(400, "text/plain", "Missing 'hex' parameter");
  }
}

// Handle servo control request
void handleServoControl() {
  if (server.hasArg("angle")) {
    int angle = server.arg("angle").toInt();
    setServoAngle(angle);  // Function from servo_control.h
    server.send(200, "text/plain", "Servo positioned to " + String(angle) + " degrees");
  } else {
    server.send(400, "text/plain", "Missing 'angle' parameter");
  }
}

// Handle motor control request (legacy)
void handleMotorControl() {
  // For absolute position
  if (server.hasArg("position")) {
    int position = server.arg("position").toInt();
    moveMotorToPosition(position);
    server.send(200, "text/plain", "Motor positioned to " + String(position));
    return;
  }
  
  // For stepping by number of steps
  if (server.hasArg("steps") && server.hasArg("direction")) {
    int steps = server.arg("steps").toInt();
    int direction = server.arg("direction").toInt();
    
    int speed = 100;
    if (server.hasArg("speed")) {
      speed = server.arg("speed").toInt();
    }
    
    moveMotorWithSpeed(steps, direction, speed);
    
    server.send(200, "text/plain", "Motor moved " + String(steps) + 
                " steps in direction " + String(direction) + 
                " with speed " + String(speed) + "%");
    return;
  }
  
  server.send(400, "text/plain", "Missing or invalid parameters");
}

// Handle button state request
void handleGetButtonState() {
  bool isButtonPressed = getButtonState();
  String jsonResponse = "{\"pressed\":" + String(isButtonPressed ? "true" : "false") + "}";
  server.send(200, "application/json", jsonResponse);
}

// Handle LED brightness control
void handleBrightness() {
  if (server.hasArg("value")) {
    int brightness = server.arg("value").toInt();
    brightness = constrain(brightness, 0, 255);
    setBrightness(brightness);
    server.send(200, "text/plain", "Brightness set to " + String(brightness));
  } else {
    server.send(400, "text/plain", "Missing 'value' parameter");
  }
}

// Advanced Motor Handler
void handleAdvancedMotorControl() {
  if (!server.hasArg("action")) {
    server.send(400, "text/plain", "Missing 'action' parameter");
    return;
  }
  
  String action = server.arg("action");
  
  if (action == "moveTo" && server.hasArg("position")) {
    int position = server.arg("position").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.setSpeed(speed);
    advancedMotor.moveTo(position);
    
    server.send(200, "text/plain", "Motor moved to position " + String(position));
    
  } else if (action == "moveRelative" && server.hasArg("steps")) {
    int steps = server.arg("steps").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.setSpeed(speed);
    advancedMotor.moveRelative(steps);
    
    server.send(200, "text/plain", "Motor moved " + String(steps) + " steps");
    
  } else if (action == "setHome") {
    advancedMotor.setHome();
    server.send(200, "text/plain", "Home position set");
    server.send(200, "text/plain", "Emergency stop executed");
    
  } else {
    server.send(400, "text/plain", "Invalid action or missing parameters");
  }
}

void handleAdvancedMotorStatus() {
  AdvancedMotorStatus status = advancedMotor.getStatus();
  
  String jsonResponse = "{"
    "\"currentPosition\":" + String(status.currentPosition) + ","
    "\"targetPosition\":" + String(status.targetPosition) + ","
    "\"isMoving\":" + String(status.isMoving ? "true" : "false") + ","
    "\"currentSpeed\":" + String(status.currentSpeed) + ","
    "\"isHomed\":" + String(status.isHomed ? "true" : "false") + ","
    "\"isEnabled\":" + String(status.isEnabled ? "true" : "false") + ","
    "\"targetPassCount\":" + String(status.targetPassCount) + ","
    "\"currentPassCount\":" + String(status.currentPassCount) + ","
    "\"isPassingButton\":" + String(status.isPassingButton ? "true" : "false") +
    "}";
  
  server.send(200, "application/json", jsonResponse);
}

void handleAdvancedMotorStop() {
  advancedMotor.stop();
  server.send(200, "text/plain", "Motor stopped");
}

void handleAdvancedMotorHome() {
  // Geschwindigkeit setzen (gleiche Logik wie moveRelative)
  int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
  
  // Prüfe ob Button-Home angefordert wird
  String homeType = server.hasArg("type") ? server.arg("type") : "position";
  
  Serial.println("Home mit Speed: " + String(speed) + " RPM, Type: " + homeType);
  
  advancedMotor.setSpeed(speed);
  
  if (homeType == "button") {
    // Neue Button-basierte Home-Fahrt
    Serial.println("Starte Button-basierte Home-Fahrt");
    advancedMotor.homeToButton();
    server.send(200, "text/plain", "Motor homed to button position");
  } else {
    // Alte Methode: Vereinfachte Home-Position: Fahre zu Position 0
    int currentPos = advancedMotor.getCurrentPosition();
    int stepsToHome = -currentPos;  // Anzahl Schritte zu Position 0
    Serial.println("Fahre zur Home-Position (0): " + String(stepsToHome) + " Schritte");
    advancedMotor.moveRelative(stepsToHome);
    advancedMotor.setHome();  // Position als Home markieren
    server.send(200, "text/plain", "Motor moved to home position");
  }
}

void handleAdvancedMotorJog() {
  server.send(400, "text/plain", "Jog function removed - use relative movement instead");
}

void handleAdvancedMotorCalibrate() {
  server.send(400, "text/plain", "Calibration function removed");
}

void handleSetHomingMode() {
  // Homing mode functionality removed - using simple virtual home only
  server.send(200, "text/plain", "Homing mode set to Virtual Home (Position 0)");
}

void handlePassButton() {
  // Überprüfe ob count Parameter vorhanden ist
  if (!server.hasArg("count")) {
    server.send(400, "text/plain", "Missing count parameter");
    return;
  }
  
  int count = server.arg("count").toInt();
  int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
  
  // Validierung
  if (count <= 0) {
    server.send(400, "text/plain", "Count must be greater than 0");
    return;
  }
  
  if (count > 100) {
    server.send(400, "text/plain", "Count must be 100 or less for safety");
    return;
  }
  
  Serial.println("Button-Pass-Fahrt mit Count: " + String(count) + ", Speed: " + String(speed) + " RPM");
  
  // Geschwindigkeit setzen und Button-Pass-Fahrt starten
  advancedMotor.setSpeed(speed);
  server.send(200, "text/plain", "Pass button command received");
}

// 28BYJ-48 Motor Control Handler
void handle28BYJ48MotorControl() {
  if (!server.hasArg("action")) {
    server.send(400, "text/plain", "Missing action parameter");
    return;
  }
  
  String action = server.arg("action");
  
  if (action == "setPins" && server.hasArg("pin1") && server.hasArg("pin2") && 
      server.hasArg("pin3") && server.hasArg("pin4")) {
    int pin1 = server.arg("pin1").toInt();
    int pin2 = server.arg("pin2").toInt();
    int pin3 = server.arg("pin3").toInt();
    int pin4 = server.arg("pin4").toInt();
    
    Serial.printf("28BYJ-48: Setting pins to %d, %d, %d, %d\n", pin1, pin2, pin3, pin4);
    set28BYJ48PinConfiguration(pin1, pin2, pin3, pin4);
    
    server.send(200, "text/plain", "Pins configured: " + String(pin1) + ", " + 
                String(pin2) + ", " + String(pin3) + ", " + String(pin4));
    
  } else if (action == "testPins" && server.hasArg("pin1") && server.hasArg("pin2") && 
             server.hasArg("pin3") && server.hasArg("pin4")) {
    int pin1 = server.arg("pin1").toInt();
    int pin2 = server.arg("pin2").toInt();
    int pin3 = server.arg("pin3").toInt();
    int pin4 = server.arg("pin4").toInt();
    int testSteps = server.hasArg("testSteps") ? server.arg("testSteps").toInt() : 50;
    int testDelay = server.hasArg("testDelay") ? server.arg("testDelay").toInt() : 5;
    
    Serial.printf("28BYJ-48: Testing pin combination %d, %d, %d, %d\n", pin1, pin2, pin3, pin4);
    test28BYJ48PinCombination(pin1, pin2, pin3, pin4, testSteps, testDelay);
    
    server.send(200, "text/plain", "Pin test completed: " + String(pin1) + ", " + 
                String(pin2) + ", " + String(pin3) + ", " + String(pin4));
    
  } else if (action == "autoTest" && server.hasArg("pins")) {
    String pinListStr = server.arg("pins");
    int testSteps = server.hasArg("testSteps") ? server.arg("testSteps").toInt() : 50;
    int testDelay = server.hasArg("testDelay") ? server.arg("testDelay").toInt() : 5;
    int betweenDelay = server.hasArg("betweenDelay") ? server.arg("betweenDelay").toInt() : 1000;
    int timeout = server.hasArg("timeout") ? server.arg("timeout").toInt() : 10;
    
    // Parse Pin-Liste
    int pins[10];
    int pinCount = 0;
    int startIdx = 0;
    
    for (int i = 0; i <= pinListStr.length(); i++) {
      if (i == pinListStr.length() || pinListStr.charAt(i) == ',') {
        if (i > startIdx && pinCount < 10) {
          pins[pinCount++] = pinListStr.substring(startIdx, i).toInt();
        }
        startIdx = i + 1;
      }
    }
    
    if (pinCount < 4) {
      server.send(400, "text/plain", "Mindestens 4 Pins erforderlich");
      return;
    }
    
    Serial.printf("28BYJ-48: Starting auto-test with %d pins\n", pinCount);
    
    // Starte Auto-Test in separatem Thread (simuliert durch Flag)
    extern bool auto_test_running;
    extern int auto_test_pins[10];
    extern int auto_test_pin_count;
    extern int auto_test_steps;
    extern int auto_test_delay;
    extern int auto_test_between_delay;
    extern int auto_test_timeout;
    
    auto_test_running = true;
    auto_test_pin_count = pinCount;
    auto_test_steps = testSteps;
    auto_test_delay = testDelay;
    auto_test_between_delay = betweenDelay;
    auto_test_timeout = timeout;
    
    for (int i = 0; i < pinCount; i++) {
      auto_test_pins[i] = pins[i];
    }
    
    server.send(200, "text/plain", "Auto-Test gestartet mit " + String(pinCount) + " Pins");
    
  } else if (action == "checkAutoTest") {
    extern bool waiting_for_pin_test_feedback;
    extern bool auto_test_running;
    extern int test_pin_combination[4];
    extern bool pin_test_confirmed;
    
    String jsonResponse = "{";
    
    if (waiting_for_pin_test_feedback) {
      jsonResponse += "\"waitingForFeedback\":true,";
      jsonResponse += "\"pin1\":" + String(test_pin_combination[0]) + ",";
      jsonResponse += "\"pin2\":" + String(test_pin_combination[1]) + ",";
      jsonResponse += "\"pin3\":" + String(test_pin_combination[2]) + ",";
      jsonResponse += "\"pin4\":" + String(test_pin_combination[3]) + ",";
      jsonResponse += "\"testComplete\":false";
    } else if (!auto_test_running) {
      jsonResponse += "\"waitingForFeedback\":false,";
      jsonResponse += "\"testComplete\":true,";
      jsonResponse += "\"success\":" + String(pin_test_confirmed ? "true" : "false");
      
      if (pin_test_confirmed) {
        int p1, p2, p3, p4;
        get28BYJ48PinConfiguration(&p1, &p2, &p3, &p4);
        jsonResponse += ",\"pin1\":" + String(p1);
        jsonResponse += ",\"pin2\":" + String(p2);
        jsonResponse += ",\"pin3\":" + String(p3);
        jsonResponse += ",\"pin4\":" + String(p4);
      }
    } else {
      jsonResponse += "\"waitingForFeedback\":false,";
      jsonResponse += "\"testComplete\":false";
    }
    
    jsonResponse += "}";
    server.send(200, "application/json", jsonResponse);
    
  } else if (action == "confirmAutoTest") {
    extern bool waiting_for_pin_test_feedback;
    extern bool pin_test_confirmed;
    
    waiting_for_pin_test_feedback = false;
    pin_test_confirmed = true;
    
    Serial.println("✓ Benutzer hat Kombination bestätigt");
    server.send(200, "text/plain", "Confirmed");
    
  } else if (action == "rejectAutoTest") {
    extern bool waiting_for_pin_test_feedback;
    extern bool pin_test_confirmed;
    
    waiting_for_pin_test_feedback = false;
    pin_test_confirmed = false;
    
    Serial.println("✗ Benutzer hat Kombination abgelehnt");
    server.send(200, "text/plain", "Rejected");
    
  } else if (action == "moveToPosition" && server.hasArg("position")) {
    int position = server.arg("position").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 50;
    
    Serial.printf("28BYJ-48: Moving to position %d at speed %d%%\n", position, speed);
    set28BYJ48MotorSpeed(speed);
    move28BYJ48MotorToPosition(position);
    
    server.send(200, "text/plain", "Moving to position: " + String(position));
    
  } else if (action == "moveRelative" && server.hasArg("steps")) {
    int steps = server.arg("steps").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 50;
    
    Serial.printf("28BYJ-48: Moving %d steps at speed %d%%\n", steps, speed);
    int direction = (steps >= 0) ? 1 : 0;
    int absSteps = abs(steps);
    set28BYJ48MotorSpeed(speed);
    move28BYJ48MotorWithSpeed(absSteps, direction, speed);
    
    server.send(200, "text/plain", "Moving " + String(steps) + " steps");
    
  } else if (action == "moveDegrees" && server.hasArg("degrees")) {
    int degrees = server.arg("degrees").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 50;
    
    Serial.printf("28BYJ-48: Rotating %d degrees at speed %d%%\n", degrees, speed);
    int direction = (degrees >= 0) ? 1 : 0;
    float absDegrees = abs(degrees);
    set28BYJ48MotorSpeed(speed);
    move28BYJ48MotorDegrees(absDegrees, direction);
    
    server.send(200, "text/plain", "Rotating " + String(degrees) + " degrees");
    
  } else if (action == "home") {
    Serial.println("28BYJ-48: Homing motor");
    home28BYJ48Motor();
    server.send(200, "text/plain", "Motor homed");
    
  } else if (action == "calibrate") {
    Serial.println("28BYJ-48: Calibrating motor");
    calibrate28BYJ48Motor();
    server.send(200, "text/plain", "Motor calibrated");
    
  } else {
    server.send(400, "text/plain", "Invalid action or missing parameters");
  }
}

// 28BYJ-48 Motor Status Handler
void handle28BYJ48MotorStatus() {
  Motor28BYJ48Status status = get28BYJ48MotorStatus();
  
  // Get current pin configuration
  int pin1, pin2, pin3, pin4;
  get28BYJ48PinConfiguration(&pin1, &pin2, &pin3, &pin4);
  
  String jsonResponse = "{"
    "\"currentPosition\":" + String(status.currentPosition) + ","
    "\"targetPosition\":" + String(status.targetPosition) + ","
    "\"isMoving\":" + String(status.isMoving ? "true" : "false") + ","
    "\"currentSpeed\":" + String(status.currentSpeed) + ","
    "\"isHomed\":" + String(status.isHomed ? "true" : "false") + ","
    "\"pin1\":" + String(pin1) + ","
    "\"pin2\":" + String(pin2) + ","
    "\"pin3\":" + String(pin3) + ","
    "\"pin4\":" + String(pin4) +
    "}";
  
  server.send(200, "application/json", jsonResponse);
}

// Handle not found (404)
void handleNotFound() {
  server.send(404, "text/plain", "404: Not found");
}