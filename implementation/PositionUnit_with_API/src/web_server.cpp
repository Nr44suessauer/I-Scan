#include "web_server.h"
#include "servo_control.h" 
#include "motor.h" 
#include "button_control.h" // Include for button functionality
#include "advanced_motor.h" // Include for advanced motor control
#include "relay_control.h"  // Include for relay control
#include "realtime_system.h" // Include for realtime system
#include <EEPROM.h>         // Include for EEPROM operations

// Function declarations
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();
void handleServoControl(); 
void handleMotorControl(); 
void handleGetButtonState(); // New function declaration for button status
void handleBrightness(); // New function declaration for brightness control
void handleSetHomingMode();     // New function for setting homing mode
void handleRowCounter();        // Row Counter API function declaration
void handleRelayControl();      // Relay control function declaration
void handleRelayState();        // Relay state function declaration
void handleMotorRelay();        // Motor relay control function declaration
void handleRelayInvert();       // Relay invert function declaration
void handleRealtimeSystem();    // Realtime system control function declaration
void handleComponentUpdate();   // Component update control function declaration
void handleGetDescription();    // Get device description from EEPROM
void handleSetDescription();    // Set device description to EEPROM
void initializeEEPROM();       // Initialize EEPROM for device description




// WebServer configuration
const uint16_t HTTP_PORT = 80;
WebServer server(HTTP_PORT);

// Enhanced HTML interface for motor control
const char* html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
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
    
    /* Description Button Styles */
    .desc-btn-save { background-color: #28a745; }
    .desc-btn-save:hover { background-color: #218838; }
    .desc-btn-reload { background-color: #007bff; }
    .desc-btn-reload:hover { background-color: #0056b3; }
    .desc-btn-example { background-color: #ffc107; color: black; }
    .desc-btn-example:hover { background-color: #e0a800; }
    .desc-btn-clear { background-color: #dc3545; }
    .desc-btn-clear:hover { background-color: #c82333; }
    
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
    <h1>ESP32 PositionUnit - Advanced Control</h1>
    
    <!-- Tab Navigation -->
    <div class="tab">
      <button class="tablinks active" onclick="openTab(event, 'MotorTab')">Motor Control</button>
      <button class="tablinks" onclick="openTab(event, 'ServoTab')">Servo Control</button>
      <button class="tablinks" onclick="openTab(event, 'LEDTab')">LED Control</button>
      <button class="tablinks" onclick="openTab(event, 'RelayTab')">Relay Control</button>
      <button class="tablinks" onclick="openTab(event, 'StatusTab')">Status & Info</button>
    </div>

    <!-- Motor Control Tab -->
    <div id="MotorTab" class="tabcontent active">
      <h2>Advanced Stepper Motor Control</h2>
      
      <!-- Motor Status -->
      <div class="control-container">
        <h3>Motor Status</h3>
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
        <h3>Speed Control</h3>
        <div class="slider-wrapper">
          <label>Speed:</label>
          <input type="range" id="speedSlider" min="1" max="120" value="60" oninput="updateSpeedValue(this.value)">
          <span id="speedValue">60</span> RPM
        </div>
      </div>

      <!-- Positioning -->
      <div class="control-container">
        <h3>Absolute Positioning</h3>
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
        <h3>Relative Movement</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="moveRelative(-1000)">- 1000 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(-100)">- 100 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(-10)">- 10 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(10)">+ 10 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(100)">+ 100 Steps</button>
          <button class="btn btn-success" onclick="moveRelative(1000)">+ 1000 Steps</button>
        </div>
      </div>

      <!-- Advanced Functions -->
      <div class="control-container">
        <h3>Advanced Functions</h3>
        <div class="function-row">
          <label class="switch-label">
            <input type="checkbox" id="physicalHomeToggle" checked onchange="toggleHomingMode(this.checked)">
            <span class="slider-toggle"></span>
            <span class="switch-text">Physical Home (Button)</span>
          </label>
          <span class="description">When enabled: Home to button position. When disabled: Home to virtual position (0)</span>
        </div>
        <div class="function-row">
          <label class="switch-label">
            <input type="checkbox" id="motorRelayToggle" onchange="toggleMotorRelay(this.checked)">
            <span class="slider-toggle"></span>
            <span class="switch-text">Motor Control with Relay</span>
          </label>
          <span class="description">When enabled: Relay turns on during motor movement and off when stopped</span>
          <div style="margin-left: 30px; margin-top: 10px;">
            <label class="switch-label">
              <input type="checkbox" id="relayInvertToggle" onchange="toggleRelayInvert(this.checked)">
              <span class="slider-toggle"></span>
              <span class="switch-text">Invert Relay Logic</span>
            </label>
            <span class="description">When enabled: Inverts relay on/off behavior</span>
          </div>
        </div>
        <div class="btn-grid">
          <button class="btn btn-primary" onclick="homeMotor()">Home Position</button>
          <button class="btn btn-warning" onclick="calibrateMotor()">Calibrate</button>
        </div>
      </div>

      <!-- Row Counter Section -->
      <div class="control-container">
        <h3>Row Counter</h3>
        <div class="function-row">
          <span class="description">Moves in small steps and counts rows (Home-Button cycles)</span>
        </div>
        <div class="input-row" style="margin: 15px 0;">
          <label for="rowsInput">Number of Rows:</label>
          <input type="number" id="rowsInput" min="1" max="1000" value="10" style="width: 80px; margin: 0 10px;">
        </div>
        <div class="status-display" style="margin: 15px 0;">
          <div class="status-item">
            <div class="status-label">Current Rows</div>
            <div class="status-value" id="currentRows">0</div>
          </div>
          <div class="status-item">
            <div class="status-label">Target Rows</div>
            <div class="status-value" id="targetRows">0</div>
          </div>
        </div>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="goRowCounter()">Go</button>
        </div>
      </div>




    </div>

    <!-- Servo Control Tab -->
    <div id="ServoTab" class="tabcontent">
      <h2>Servo Control</h2>
      
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
      <h2>LED Control</h2>
      
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

    <!-- Relay Control Tab -->
    <div id="RelayTab" class="tabcontent">
      <h2>Relay Control</h2>
      
      <!-- Relay Status -->
      <div class="control-container">
        <h3>Relay Status (Pin 17)</h3>
        <div class="status-display">
          <div class="status-item">
            <div class="status-label">Current State</div>
            <div class="status-value" id="relayStatus">OFF</div>
          </div>
          <div class="status-item">
            <div class="status-label">Pin</div>
            <div class="status-value">Pin 17</div>
          </div>
        </div>
        <button class="btn btn-secondary" onclick="refreshRelayStatus()">Update Status</button>
      </div>

      <!-- Relay Control -->
      <div class="control-container">
        <h3>Relay Control</h3>
        <div class="btn-grid">
          <button class="btn btn-success" onclick="setRelay(true)">Turn ON</button>
          <button class="btn btn-danger" onclick="setRelay(false)">Turn OFF</button>
          <button class="btn btn-warning" onclick="toggleRelay()">Toggle</button>
        </div>
      </div>

      <!-- Relay Information -->
      <div class="control-container">
        <h3>Information</h3>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #17a2b8;">
          <p><strong>Relay Pin:</strong> GPIO 17</p>
          <p><strong>Control Type:</strong> Active HIGH</p>
          <p><strong>Max Current:</strong> Depends on relay specifications</p>
          <p><strong>Note:</strong> Ensure your relay can handle the load you're switching!</p>
        </div>
      </div>
    </div>

    <!-- Status Tab -->
    <div id="StatusTab" class="tabcontent">
      <h2>System Status & Information</h2>
      
      <!-- Button Status -->
      <div class="control-container">
        <h3>Button Status (Pin 45)</h3>
        <div class="status-display">
          <div class="status-item">
            <div class="status-label">Display Status</div>
            <div class="status-value" id="buttonStatus">Pressed</div>
          </div>
          <div class="status-item">
            <div class="status-label">Hardware State</div>
            <div class="status-value" id="buttonHardwareState">HIGH</div>
          </div>
          <div class="status-item">
            <div class="status-label">Update Rate</div>
            <div class="status-value">Auto (500ms)</div>
          </div>
        </div>
        
        <!-- Button Invert Option -->
        <div class="function-row" style="margin-top: 15px;">
          <label class="switch-label">
            <input type="checkbox" id="buttonInvertToggle" onchange="toggleButtonInvert(this.checked)">
            <span class="slider-toggle"></span>
            <span class="switch-text">Invert Button Logic</span>
          </label>
          <span class="description">When enabled: Inverts pressed/not pressed display logic</span>
        </div>
        
        <button class="btn btn-secondary" onclick="refreshButtonStatus()">Manual Refresh</button>
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
          <div class="status-item">
            <div class="status-label">Relay Pin</div>
            <div class="status-value">Pin 17</div>
          </div>
          <div class="status-item">
            <div class="status-label">IP Address</div>
            <div class="status-value" id="ipAddress">Loading...</div>
          </div>
        </div>
      </div>

      <!-- Device Description -->
      <div class="control-container">
        <h3>Device Description</h3>
        <div class="status-display">
          <div class="status-item">
            <div class="status-value" id="currentDescription">Loading...</div>
          </div>
        </div>
        
        <div style="margin-top: 15px;">
          <div style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
            <label for="modulNumberInput" style="font-weight: bold; min-width: 80px;">Device:</label>
            <input type="text" id="modulNumberInput" 
                   style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
                   placeholder="Enter module number (e.g., ISC-001)">
          </div>
          
          <div style="margin-bottom: 15px;">
            <label for="descriptionInput" style="display: block; margin-bottom: 8px; font-weight: bold;">Description:</label>
            <textarea id="descriptionInput" 
                      rows="6" 
                      style="width: 100%; min-height: 150px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; resize: vertical;"
                      placeholder="Enter device description..."></textarea>
          </div>
          <div style="margin-top: 10px; text-align: left; white-space: nowrap;">
            <button onclick="saveDescription()" class="desc-btn-save" style="display: inline-block; margin: 5px; padding: 10px 15px; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: 0.3s;">Save to EEPROM</button>
            <button onclick="loadDescription()" class="desc-btn-reload" style="display: inline-block; margin: 5px; padding: 10px 15px; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: 0.3s;">Reload</button>
            <button onclick="loadExample()" class="desc-btn-example" style="display: inline-block; margin: 5px; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: 0.3s;">Load Example</button>
            <button onclick="clearDescription()" class="desc-btn-clear" style="display: inline-block; margin: 5px; padding: 10px 15px; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: 0.3s;">Clear</button>
          </div>
          <div id="descriptionStatus" style="margin-top: 10px; padding: 8px; border-radius: 4px; display: none;"></div>
        </div>
      </div>

      <!-- QR Code for Web Interface -->
      <div class="control-container">
        <h3>Web Interface QR Code</h3>
        <div style="text-align: center; margin: 20px 0;">
          <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; display: inline-block;">
            <img id="qrCodeImage" src="" alt="QR Code is being generated..." style="max-width: 200px; height: auto; border: 2px solid #ddd; border-radius: 8px;">
            <div style="margin-top: 10px; font-size: 14px; color: #666;">
              Scan the QR code with your smartphone<br>
              for direct access to the web interface
            </div>
          </div>
          <div style="margin-top: 15px;">
            <button class="btn btn-secondary" onclick="generateQRCode()">Update QR Code</button>
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
    // Global variables
    let motorStatusInterval;
    let buttonUpdateInterval;
    let buttonInverted = false;
    
    // Tab functionality
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
        stopButtonStatusUpdates(); // Stop button updates when not on Status tab
      } else {
        stopMotorStatusUpdates();
      }
      
      // Start button status updates when Status tab is opened
      if (tabName === 'StatusTab') {
        startButtonStatusUpdates();
      } else {
        stopButtonStatusUpdates();
      }
    }
    
    // Update motor status automatically
    function startMotorStatusUpdates() {
      updateMotorStatus();
      if (motorStatusInterval) clearInterval(motorStatusInterval);
      motorStatusInterval = setInterval(updateMotorStatus, 2000);
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
      
      // Restore button invert setting from localStorage
      const savedButtonInvert = localStorage.getItem('buttonInverted');
      if (savedButtonInvert === 'true') {
        buttonInverted = true;
        document.getElementById('buttonInvertToggle').checked = true;
      }
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
          
          // Update toggle status
          document.getElementById('physicalHomeToggle').checked = data.usePhysicalHome || false;
          
          // Update Row Counter status
          document.getElementById('currentRows').textContent = data.currentRows || 0;
          document.getElementById('targetRows').textContent = data.targetRows || 0;
          
          // Status text depending on state
          let statusText = 'Ready';
          
          if (data.isRowCounterActive) {
              statusText = 'Row Counting Active (' + data.currentRows + '/' + data.targetRows + ')';
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
      const speed = parseInt(document.getElementById('speedSlider').value) || 60;
      
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
    
    function homeMotor() {
      document.getElementById('status').innerHTML = 'Status: Motor moving to home position...';
      
      // Get speed from Speed slider
      const speed = document.getElementById('speedSlider').value;
      
      fetch('/motorHome?speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error moving to home';
        });
    }
    
    function calibrateMotor() {
      document.getElementById('status').innerHTML = 'Status: Motor calibrating...';
      
      fetch('/motorCalibrate')
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in calibration';
        });
    }
    

    

    
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
    
    function toggleHomingMode(usePhysical) {
      const mode = usePhysical ? 'physical' : 'virtual';
      document.getElementById('status').innerHTML = `Status: Setting homing mode to ${mode}...`;
      
      fetch(`/setHomingMode?mode=${mode}`)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error setting homing mode';
        });
    }
    
    function toggleMotorRelay(enabled) {
      const mode = enabled ? 'enabled' : 'disabled';
      document.getElementById('status').innerHTML = `Status: Motor relay control ${mode}...`;
      
      fetch(`/motorRelay?enabled=${enabled}`)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error setting motor relay control';
        });
    }
    
    function toggleRelayInvert(inverted) {
      const mode = inverted ? 'inverted' : 'normal';
      document.getElementById('status').innerHTML = `Status: Relay logic ${mode}...`;
      
      fetch(`/relayInvert?inverted=${inverted}`)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error setting relay invert logic';
        });
    }
    
    // Row Counter Functions
    function updateRowsTarget() {
      const targetRows = document.getElementById('rowsInput').value || 10;
      
      if (targetRows < 1 || targetRows > 1000) {
        document.getElementById('status').innerHTML = 'Status: Invalid target rows (1-1000)';
        return;
      }
      
      // Automatically start the row counter with the new target
      fetch('/rowCounter?action=start&targetRows=' + targetRows)
        .then(response => response.text())
        .then(data => {
          document.getElementById('targetRows').textContent = targetRows;
          document.getElementById('status').innerHTML = 'Status: Target rows set to ' + targetRows;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error setting target rows';
        });
    }
    
    function goRowCounter() {
      const targetRows = document.getElementById('rowsInput').value || 10;
      const speed = parseInt(document.getElementById('speedSlider').value) || 60;
      
      if (targetRows < 1 || targetRows > 1000) {
        document.getElementById('status').innerHTML = 'Status: Invalid target rows (1-1000)';
        return;
      }
      
      document.getElementById('status').innerHTML = 'Status: Initializing and starting row counter...';
      
      // First set the target rows (start function)
      fetch('/rowCounter?action=start&targetRows=' + targetRows)
        .then(response => response.text())
        .then(data => {
          // Then immediately start the row counting process (go function)
          return fetch('/rowCounter?action=go&speed=' + speed);
        })
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
          updateMotorStatus();
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in row counting';
        });
    }
    

    
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
          const buttonHardwareState = document.getElementById('buttonHardwareState');
          
          // Show raw hardware state
          buttonHardwareState.textContent = data.pressed ? 'LOW (Active)' : 'HIGH (Idle)';
          buttonHardwareState.style.color = data.pressed ? '#17a2b8' : '#6c757d'; // Blue for active, gray for idle
          
          // Apply invert logic if enabled
          let isPressed = data.pressed;
          if (buttonInverted) {
            isPressed = !isPressed;
          }
          
          if (isPressed) {
            buttonStatus.textContent = buttonInverted ? 'Pressed (inverted)' : 'Pressed';
            buttonStatus.style.color = '#28a745'; // Green for pressed
            buttonStatus.style.fontWeight = 'bold';
          } else {
            buttonStatus.textContent = buttonInverted ? 'Not pressed (inverted)' : 'Not pressed';  
            buttonStatus.style.color = '#6c757d'; // Gray for not pressed
            buttonStatus.style.fontWeight = 'normal';
          }
        })
        .catch(error => {
          console.error('Error retrieving button status:', error);
          const buttonStatus = document.getElementById('buttonStatus');
          buttonStatus.textContent = 'Error reading';
          buttonStatus.style.color = '#dc3545'; // Red for error
        });
    }
    
    // Start automatic button status updates when Status tab is active
    function startButtonStatusUpdates() {
      if (!buttonUpdateInterval) {
        refreshButtonStatus(); // Initial update
        buttonUpdateInterval = setInterval(refreshButtonStatus, 500); // Update every 500ms
      }
    }
    
    // Stop automatic button status updates
    function stopButtonStatusUpdates() {
      if (buttonUpdateInterval) {
        clearInterval(buttonUpdateInterval);
        buttonUpdateInterval = null;
      }
    }
    
    // Toggle button invert logic
    function toggleButtonInvert(inverted) {
      buttonInverted = inverted;
      console.log('Button invert logic:', inverted ? 'enabled' : 'disabled');
      
      // Immediately refresh button status to show the change
      refreshButtonStatus();
      
      // Save the setting to localStorage for persistence
      localStorage.setItem('buttonInverted', inverted.toString());
    }
    
    // QR Code functions
    function generateQRCode() {
      const currentUrl = window.location.href;
      const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(currentUrl)}`;
      
      document.getElementById('qrCodeImage').src = qrCodeUrl;
      document.getElementById('ipAddress').textContent = window.location.host;
    }
    
    // Relay Control Functions
    function setRelay(state) {
      const action = state ? 'on' : 'off';
      fetch(`/relay?action=${action}`)
        .then(response => response.text())
        .then(data => {
          console.log('Relay response:', data);
          refreshRelayStatus();
        })
        .catch(error => {
          console.error('Error controlling relay:', error);
        });
    }
    
    function toggleRelay() {
      fetch('/relay?action=toggle')
        .then(response => response.text())
        .then(data => {
          console.log('Relay toggle response:', data);
          refreshRelayStatus();
        })
        .catch(error => {
          console.error('Error toggling relay:', error);
        });
    }
    
    function refreshRelayStatus() {
      fetch('/relaystate')
        .then(response => response.json())
        .then(data => {
          const relayStatus = document.getElementById('relayStatus');
          relayStatus.textContent = data.state ? 'ON' : 'OFF';
          relayStatus.style.color = data.state ? '#4CAF50' : '#f44336';
        })
        .catch(error => {
          console.error('Error retrieving relay status:', error);
        });
    }
    
    // Device Description Functions
    function loadDescription() {
      fetch('/getDescription')
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            document.getElementById('modulNumberInput').value = data.modulNumber || '';
            document.getElementById('descriptionInput').value = data.description || '';
            
            // Update display
            const displayText = (data.modulNumber ? 'Device: ' + data.modulNumber : '') + 
                               (data.description ? (data.modulNumber ? ' | ' : '') + 'Desc: ' + data.description.substring(0, 50) + (data.description.length > 50 ? '...' : '') : '');
            document.getElementById('currentDescription').textContent = displayText || 'No data set';
          } else {
            document.getElementById('currentDescription').textContent = 'Error loading data';
          }
        })
        .catch(error => {
          console.error('Error loading description:', error);
          document.getElementById('currentDescription').textContent = 'Error loading data';
        });
    }
    
    function saveDescription() {
      const modulNumber = document.getElementById('modulNumberInput').value.trim();
      const description = document.getElementById('descriptionInput').value.trim();
      
      showDescriptionStatus('Saving to EEPROM...', 'info');
      
      // Simple form-encoded POST
      const params = new URLSearchParams();
      params.append('modulNumber', modulNumber);
      params.append('description', description);
      
      fetch('/setDescription', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString()
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showDescriptionStatus('Data saved successfully!', 'success');
          loadDescription(); // Refresh display
        } else {
          showDescriptionStatus('Error saving data: ' + data.message, 'error');
        }
      })
      .catch(error => {
        console.error('Error saving data:', error);
        showDescriptionStatus('Network error while saving data', 'error');
      });
    }
    
    function clearDescription() {
      if (confirm('Are you sure you want to clear the device data?')) {
        document.getElementById('modulNumberInput').value = '';
        document.getElementById('descriptionInput').value = '';
        saveDescription();
      }
    }
    
    function loadExample() {
      document.getElementById('modulNumberInput').value = 'ISC-2024-001';
      document.getElementById('descriptionInput').value = 'I-Scan Device for Laboratory A\nPurpose: Sample scanning and analysis\nOperator: Tech Team\nCalibration: 2024-10-20\nStatus: Ready for operation';
      showDescriptionStatus('Example loaded! You can now modify the values and save.', 'info');
    }
    
    function showDescriptionStatus(message, type) {
      const statusDiv = document.getElementById('descriptionStatus');
      statusDiv.textContent = message;
      statusDiv.style.display = 'block';
      
      // Set color based on type
      switch(type) {
        case 'success':
          statusDiv.style.backgroundColor = '#d4edda';
          statusDiv.style.color = '#155724';
          statusDiv.style.border = '1px solid #c3e6cb';
          break;
        case 'error':
          statusDiv.style.backgroundColor = '#f8d7da';
          statusDiv.style.color = '#721c24';
          statusDiv.style.border = '1px solid #f5c6cb';
          break;
        case 'info':
          statusDiv.style.backgroundColor = '#d1ecf1';
          statusDiv.style.color = '#0c5460';
          statusDiv.style.border = '1px solid #bee5eb';
          break;
      }
      
      // Hide after 5 seconds for success and info messages
      if (type !== 'error') {
        setTimeout(() => {
          statusDiv.style.display = 'none';
        }, 5000);
      }
    }
    
    // Color preview event listener
    document.addEventListener('DOMContentLoaded', function() {
      const hexInput = document.getElementById('hexInput');
      if (hexInput) {
        hexInput.addEventListener('input', updateColorPreview);
      }
      
      // Rows input event listener - automatically update target when value changes
      const rowsInput = document.getElementById('rowsInput');
      if (rowsInput) {
        rowsInput.addEventListener('input', updateRowsTarget);
        rowsInput.addEventListener('change', updateRowsTarget);
      }
      
      // Display IP address and generate QR code
      document.getElementById('ipAddress').textContent = window.location.host;
      generateQRCode();
      
      // Initial status updates
      refreshRelayStatus();
      
      // Load device description on page load
      loadDescription();
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
  server.on("/setHomingMode", HTTP_GET, handleSetHomingMode);               // New route for homing mode
  server.on("/rowCounter", HTTP_GET, handleRowCounter);                     // Row Counter API Route
  server.on("/motorRelay", HTTP_GET, handleMotorRelay);                     // Motor relay control route
  server.on("/relayInvert", HTTP_GET, handleRelayInvert);                   // Relay invert route
  server.on("/realtimeSystem", HTTP_GET, handleRealtimeSystem);             // Realtime system control route
  server.on("/componentUpdate", HTTP_GET, handleComponentUpdate);           // Component update control route
  
  // Relay Routes
  server.on("/relay", HTTP_GET, handleRelayControl);                        // Relay control route
  server.on("/relaystate", HTTP_GET, handleRelayState);                     // Relay state route

  // Device Description Routes
  server.on("/getDescription", HTTP_GET, handleGetDescription);             // Get device description
  server.on("/setDescription", HTTP_POST, handleSetDescription);            // Set device description

  // Initialize EEPROM for device description
  initializeEEPROM();
  
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
    int stepsToMove = abs(position - advancedMotor.getCurrentPosition());
    
    advancedMotor.setSpeed(speed);
    
    // For large movements (>100 steps) use chunked version
    if (stepsToMove > 100) {
      advancedMotor.moveToChunked(position, 50, 10);  // 50 steps per chunk, 10ms pause
      server.send(200, "text/plain", "Motor moving to position " + String(position) + " (chunked)");
    } else {
      advancedMotor.moveTo(position);
      server.send(200, "text/plain", "Motor moved to position " + String(position));
    }
    
  } else if (action == "moveRelative" && server.hasArg("steps")) {
    int steps = server.arg("steps").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.setSpeed(speed);
    
    // For large movements (>100 steps) use chunked version
    if (abs(steps) > 100) {
      advancedMotor.moveRelativeChunked(steps, 50, 10);  // 50 steps per chunk, 10ms pause
      server.send(200, "text/plain", "Motor moving " + String(steps) + " steps (chunked)");
    } else {
      advancedMotor.moveRelative(steps);
      server.send(200, "text/plain", "Motor moved " + String(steps) + " steps");
    }
    
  } else if (action == "moveDegrees" && server.hasArg("degrees")) {
    float degrees = server.arg("degrees").toFloat();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.setSpeed(speed);
    advancedMotor.moveDegrees(degrees);
    
    server.send(200, "text/plain", "Motor moved " + String(degrees) + " degrees");
    
  } else if (action == "moveRevolutions" && server.hasArg("revolutions")) {
    float revolutions = server.arg("revolutions").toFloat();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.setSpeed(speed);
    advancedMotor.moveRevolutions(revolutions);
    
    server.send(200, "text/plain", "Motor moved " + String(revolutions) + " revolutions");
    
  } else if (action == "smoothMove" && server.hasArg("steps")) {
    int steps = server.arg("steps").toInt();
    int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
    
    advancedMotor.moveSmoothly(steps, speed);
    
    server.send(200, "text/plain", "Smooth movement completed");

  } else if (action == "acceleratedMove" && server.hasArg("steps")) {
    int steps = server.arg("steps").toInt();
    int startSpeed = server.hasArg("startSpeed") ? server.arg("startSpeed").toInt() : 20;
    int endSpeed = server.hasArg("endSpeed") ? server.arg("endSpeed").toInt() : 60;
    
    advancedMotor.moveWithAcceleration(steps, startSpeed, endSpeed);
    
    server.send(200, "text/plain", "Accelerated movement completed");
    
  } else if (action == "setHome") {
    advancedMotor.setHome();
    server.send(200, "text/plain", "Home position set");
    
  } else if (action == "emergencyStop") {
    advancedMotor.emergencyStop();
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
    "\"usePhysicalHome\":" + String(status.usePhysicalHome ? "true" : "false") + ","
    "\"isButtonHomingActive\":" + String(status.isButtonHomingActive ? "true" : "false") + ","
    "\"isRowCounterActive\":" + String(advancedMotor.isRowCounterRunning() ? "true" : "false") + ","
    "\"currentRows\":" + String(advancedMotor.getCurrentRows()) + ","
    "\"targetRows\":" + String(advancedMotor.getTargetRows()) + ","
    "\"isChunkedMovementActive\":" + String(advancedMotor.isChunkedMovementRunning() ? "true" : "false") + ""
    "}";
  
  server.send(200, "application/json", jsonResponse);
}

void handleAdvancedMotorStop() {
  advancedMotor.stop();
  server.send(200, "text/plain", "Motor stopped");
}

void handleAdvancedMotorHome() {
  // Get speed from Speed slider if available
  if (server.hasArg("speed")) {
    int speed = server.arg("speed").toInt();
    if (speed > 0 && speed <= 120) {  // Validation according to slider maximum
      advancedMotor.setSpeed(speed);
      Serial.println("Home speed set to " + String(speed) + " RPM");
    }
  }
  
  advancedMotor.home();
  server.send(200, "text/plain", "Motor moved to home position");
}

void handleAdvancedMotorJog() {
  if (!server.hasArg("direction")) {
    server.send(400, "text/plain", "Missing 'direction' parameter");
    return;
  }
  
  bool direction = server.arg("direction").toInt() == 1;
  int speed = server.hasArg("speed") ? server.arg("speed").toInt() : 60;
  
  advancedMotor.jogContinuous(direction, speed);
  
  server.send(200, "text/plain", "Jog started in " + String(direction ? "forward" : "backward") + " direction");
}

void handleAdvancedMotorCalibrate() {
  advancedMotor.calibrate();
  server.send(200, "text/plain", "Motor calibrated");
}

void handleSetHomingMode() {
  String mode = server.arg("mode");
  
  if (mode == "physical") {
    advancedMotor.setUsePhysicalHome(true);
    server.send(200, "text/plain", "Homing mode set to Physical Home (Button)");
  } else if (mode == "virtual") {
    advancedMotor.setUsePhysicalHome(false);
    server.send(200, "text/plain", "Homing mode set to Virtual Home (Position 0)");
  } else {
    server.send(400, "text/plain", "Invalid mode. Use 'physical' or 'virtual'");
  }
}

// Button Homing Handler

// Row Counter API Handler
void handleRowCounter() {
  String action = server.arg("action");
  
  if (action == "start") {
    if (!server.hasArg("targetRows")) {
      server.send(400, "text/plain", "Missing 'targetRows' parameter");
      return;
    }
    
    int targetRows = server.arg("targetRows").toInt();
    if (targetRows <= 0 || targetRows > 1000) {
      server.send(400, "text/plain", "Invalid targetRows. Must be between 1 and 1000");
      return;
    }
    
    bool success = advancedMotor.startRowCounter(targetRows);
    if (success) {
      server.send(200, "text/plain", "Row Counter started with target: " + String(targetRows));
    } else {
      server.send(400, "text/plain", "Cannot start Row Counter. Motor must be homed first");
    }
    
  } else if (action == "go") {
    // Get speed from Speed slider if available
    int speed = 60; // Default speed
    if (server.hasArg("speed")) {
      speed = server.arg("speed").toInt();
      if (speed < 1 || speed > 120) {
        speed = 60; // Fallback to default value for invalid input
      }
    }
    
    bool success = advancedMotor.goRowCounter();
    if (success) {
      // Set speed after start
      advancedMotor.setSpeed(speed);
      server.send(200, "text/plain", "Row Counter started with " + String(speed) + " RPM");
    } else {
      server.send(400, "text/plain", "Row Counter is not ready or already running");
    }
    
  } else if (action == "stop") {
    advancedMotor.stopRowCounter();
    server.send(200, "text/plain", "Row Counter stopped");
    
  } else if (action == "status") {
    String jsonResponse = 
      "{"
      "\"isRunning\":" + String(advancedMotor.isRowCounterRunning() ? "true" : "false") + ","
      "\"currentRows\":" + String(advancedMotor.getCurrentRows()) + ","
      "\"targetRows\":" + String(advancedMotor.getTargetRows()) + ","
      "\"isHomed\":" + String(advancedMotor.getStatus().isHomed ? "true" : "false") + ","
      "\"isEnabled\":" + String(advancedMotor.getStatus().isEnabled ? "true" : "false") + ""
      "}";
    server.send(200, "application/json", jsonResponse);
    
  } else if (action == "debug") {
    // Debug information for troubleshooting
    AdvancedMotorStatus status = advancedMotor.getStatus();
    String debugResponse = 
      "Row Counter Debug Info:\n"
      "- isHomed: " + String(status.isHomed ? "YES" : "NO") + "\n"
      "- isEnabled: " + String(status.isEnabled ? "YES" : "NO") + "\n"
      "- isRowCounterRunning: " + String(advancedMotor.isRowCounterRunning() ? "YES" : "NO") + "\n"
      "- targetRows: " + String(advancedMotor.getTargetRows()) + "\n"
      "- currentRows: " + String(advancedMotor.getCurrentRows()) + "\n"
      "- currentPosition: " + String(status.currentPosition);
    server.send(200, "text/plain", debugResponse);
    
  } else {
    server.send(400, "text/plain", "Invalid action. Use 'start', 'go', 'stop', 'status', or 'debug'");
  }
}

// Handle relay control
void handleRelayControl() {
  if (server.hasArg("action")) {
    String action = server.arg("action");
    
    if (action == "on") {
      setRelayState(true);
      server.send(200, "text/plain", "Relay turned ON");
    } else if (action == "off") {
      setRelayState(false);
      server.send(200, "text/plain", "Relay turned OFF");
    } else if (action == "toggle") {
      toggleRelay();
      String state = getRelayState() ? "ON" : "OFF";
      server.send(200, "text/plain", "Relay toggled - now " + state);
    } else {
      server.send(400, "text/plain", "Invalid action. Use 'on', 'off', or 'toggle'");
    }
  } else {
    server.send(400, "text/plain", "Missing action parameter");
  }
}

// Handle relay state request
void handleRelayState() {
  String jsonResponse = "{\"state\":" + String(getRelayState() ? "true" : "false") + "}";
  server.send(200, "application/json", jsonResponse);
}

// Handle motor relay control
void handleMotorRelay() {
  if (server.hasArg("enabled")) {
    String enabledStr = server.arg("enabled");
    bool enabled = (enabledStr == "true");
    
    // Set motor relay control mode
    advancedMotor.setMotorRelayControl(enabled);
    
    String response = enabled ? 
      "Motor relay control enabled - relay will control motor power" : 
      "Motor relay control disabled - relay independent from motor";
    
    server.send(200, "text/plain", response);
  } else {
    server.send(400, "text/plain", "Missing enabled parameter");
  }
}

// Handle relay invert control
void handleRelayInvert() {
  if (server.hasArg("inverted")) {
    String invertedStr = server.arg("inverted");
    bool inverted = (invertedStr == "true");
    
    // Set relay invert logic
    advancedMotor.setRelayInvert(inverted);
    
    String response = inverted ? 
      "Relay logic inverted - relay OFF when motor runs" : 
      "Relay logic normal - relay ON when motor runs";
    
    server.send(200, "text/plain", response);
  } else {
    server.send(400, "text/plain", "Missing inverted parameter");
  }
}

// Handle realtime system control
void handleRealtimeSystem() {
  if (server.hasArg("action")) {
    String action = server.arg("action");
    
    if (action == "enable") {
      enableRealtimeUpdates();
      server.send(200, "text/plain", "Realtime system enabled");
    } else if (action == "disable") {
      disableRealtimeUpdates();
      server.send(200, "text/plain", "Realtime system disabled");
    } else if (action == "forceUpdate") {
      forceUpdateAllComponents();
      server.send(200, "text/plain", "Force update of all components executed");
    } else if (action == "setInterval" && server.hasArg("interval")) {
      unsigned long interval = server.arg("interval").toInt();
      if (interval >= 1 && interval <= 1000) {
        globalRealtimeInterval = interval;
        server.send(200, "text/plain", "Realtime interval set to " + String(interval) + "ms");
      } else {
        server.send(400, "text/plain", "Invalid interval (1-1000ms)");
      }
    } else {
      server.send(400, "text/plain", "Invalid action. Use 'enable', 'disable', 'forceUpdate', or 'setInterval'");
    }
  } else {
    String status = realtimeSystemEnabled ? "enabled" : "disabled";
    String response = "Realtime system status: " + status + ", interval: " + String(globalRealtimeInterval) + "ms";
    server.send(200, "text/plain", response);
  }
}

// Handle component update control
void handleComponentUpdate() {
  if (server.hasArg("component") && server.hasArg("enabled")) {
    String component = server.arg("component");
    bool enabled = (server.arg("enabled") == "true");
    
    setComponentUpdateFlag(component.c_str(), enabled);
    
    String response = "Component '" + component + "' realtime updates: " + 
                     (enabled ? "enabled" : "disabled");
    server.send(200, "text/plain", response);
  } else {
    String response = "Component update flags:\n";
    response += "Relay: " + String(updateFlags.relayUpdate ? "enabled" : "disabled") + "\n";
    response += "LED: " + String(updateFlags.ledUpdate ? "enabled" : "disabled") + "\n";
    response += "Servo: " + String(updateFlags.servoUpdate ? "enabled" : "disabled") + "\n";
    response += "Motor: " + String(updateFlags.motorUpdate ? "enabled" : "disabled") + "\n";
    response += "Button: " + String(updateFlags.buttonUpdate ? "enabled" : "disabled") + "\n";
    response += "Network: " + String(updateFlags.networkUpdate ? "enabled" : "disabled");
    
    server.send(200, "text/plain", response);
  }
}

// Device description EEPROM addresses
#define EEPROM_MODUL_NUMBER_ADDR 100
#define EEPROM_MODUL_NUMBER_SIZE 50
#define EEPROM_DESCRIPTION_ADDR 150
#define EEPROM_DESCRIPTION_SIZE 400

// Initialize EEPROM for device description
void initializeEEPROM() {
  EEPROM.begin(EEPROM_DESCRIPTION_ADDR + EEPROM_DESCRIPTION_SIZE);
  
  // Check if EEPROM areas are uninitialized (all 0xFF)
  bool needsInit = false;
  char firstByteModul = EEPROM.read(EEPROM_MODUL_NUMBER_ADDR);
  char firstByteDesc = EEPROM.read(EEPROM_DESCRIPTION_ADDR);
  
  if (firstByteModul == 0xFF || firstByteDesc == 0xFF) {
    needsInit = true;
  }
  
  if (needsInit) {
    Serial.println("Initializing EEPROM areas...");
    
    // Clear modul number area
    for (int i = 0; i < EEPROM_MODUL_NUMBER_SIZE; i++) {
      EEPROM.write(EEPROM_MODUL_NUMBER_ADDR + i, 0);
    }
    
    // Clear description area
    for (int i = 0; i < EEPROM_DESCRIPTION_SIZE; i++) {
      EEPROM.write(EEPROM_DESCRIPTION_ADDR + i, 0);
    }
    
    EEPROM.commit();
    Serial.println("EEPROM areas initialized.");
  } else {
    Serial.println("EEPROM areas already initialized.");
  }
}

// Handle get device description
void handleGetDescription() {
  EEPROM.begin(EEPROM_DESCRIPTION_ADDR + EEPROM_DESCRIPTION_SIZE);
  
  String modulNumber = "";
  String description = "";
  
  // Read modul number
  for (int i = 0; i < EEPROM_MODUL_NUMBER_SIZE; i++) {
    char c = EEPROM.read(EEPROM_MODUL_NUMBER_ADDR + i);
    if (c == 0) break; // End of string
    if (c >= 32 && c <= 126) { // Only printable ASCII characters
      modulNumber += c;
    } else {
      break; // Stop at invalid character
    }
  }
  
  // Read description
  for (int i = 0; i < EEPROM_DESCRIPTION_SIZE; i++) {
    char c = EEPROM.read(EEPROM_DESCRIPTION_ADDR + i);
    if (c == 0) break; // End of string
    if (c >= 32 && c <= 126 || c == '\n' || c == '\r' || c == '\t') { // Printable + line breaks
      description += c;
    } else {
      break; // Stop at invalid character
    }
  }
  
  // Create JSON response
  String jsonResponse = "{\"success\":true,\"modulNumber\":\"" + modulNumber + "\",\"description\":\"" + description + "\"}";
  // Escape newlines for JSON
  jsonResponse.replace("\n", "\\n");
  jsonResponse.replace("\r", "\\r");
  jsonResponse.replace("\t", "\\t");
  
  server.send(200, "application/json", jsonResponse);
}

// Handle set device description
void handleSetDescription() {
  if (server.hasArg("modulNumber") && server.hasArg("description")) {
    String modulNumber = server.arg("modulNumber");
    String description = server.arg("description");
    
    // Debug output
    Serial.println("Received data:");
    Serial.println("Modul Number: " + modulNumber);
    Serial.println("Description: " + description);
    
    // Check size limits
    if (modulNumber.length() >= EEPROM_MODUL_NUMBER_SIZE) {
      String jsonResponse = "{\"success\":false,\"message\":\"Module number too long (max " + String(EEPROM_MODUL_NUMBER_SIZE - 1) + " characters)\"}";
      server.send(400, "application/json", jsonResponse);
      return;
    }
    
    if (description.length() >= EEPROM_DESCRIPTION_SIZE) {
      String jsonResponse = "{\"success\":false,\"message\":\"Description too long (max " + String(EEPROM_DESCRIPTION_SIZE - 1) + " characters)\"}";
      server.send(400, "application/json", jsonResponse);
      return;
    }
    
    EEPROM.begin(EEPROM_DESCRIPTION_ADDR + EEPROM_DESCRIPTION_SIZE);
    
    // Clear and write modul number
    for (int i = 0; i < EEPROM_MODUL_NUMBER_SIZE; i++) {
      EEPROM.write(EEPROM_MODUL_NUMBER_ADDR + i, 0);
    }
    for (int i = 0; i < modulNumber.length(); i++) {
      EEPROM.write(EEPROM_MODUL_NUMBER_ADDR + i, modulNumber.charAt(i));
    }
    
    // Clear and write description
    for (int i = 0; i < EEPROM_DESCRIPTION_SIZE; i++) {
      EEPROM.write(EEPROM_DESCRIPTION_ADDR + i, 0);
    }
    for (int i = 0; i < description.length(); i++) {
      EEPROM.write(EEPROM_DESCRIPTION_ADDR + i, description.charAt(i));
    }
    
    // Commit changes to EEPROM
    if (EEPROM.commit()) {
      Serial.println("EEPROM write successful");
      String jsonResponse = "{\"success\":true,\"message\":\"Data saved to EEPROM\"}";
      server.send(200, "application/json", jsonResponse);
    } else {
      Serial.println("EEPROM write failed");
      String jsonResponse = "{\"success\":false,\"message\":\"Failed to save to EEPROM\"}";
      server.send(500, "application/json", jsonResponse);
    }
  } else {
    String jsonResponse = "{\"success\":false,\"message\":\"Missing parameters\"}";
    server.send(400, "application/json", jsonResponse);
  }
}

// Handle not found (404)
void handleNotFound() {
  server.send(404, "text/plain", "404: Not found");
}