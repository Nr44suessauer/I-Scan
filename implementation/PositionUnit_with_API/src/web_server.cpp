#include "web_server.h"
#include "servo_control.h" 
#include "motor.h" 
#include "button_control.h" // Include for button functionality
#include "advanced_motor.h" // Include for advanced motor control

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
  advancedMotor.passButtonTimes(count);
  
  server.send(200, "text/plain", "Motor passing button " + String(count) + " times");
}

// Button Homing Handler






// Handle not found (404)
void handleNotFound() {
  server.send(404, "text/plain", "404: Not found");
}