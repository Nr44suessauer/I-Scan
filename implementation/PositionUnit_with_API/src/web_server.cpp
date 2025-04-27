#include "web_server.h"
#include "servo_control.h" 
#include "motor.h" 
#include "button_control.h" // Include for button functionality

// Function declarations
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();
void handleServoControl(); 
void handleMotorControl(); 
void handleGetButtonState(); // New function declaration for button status
void handleBrightness(); // New function declaration for brightness control

// WebServer configuration
const uint16_t HTTP_PORT = 80;
WebServer server(HTTP_PORT);

// HTML webpage with buttons for LED control
const char* html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RGB LED Control</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 20px; background: #f4f4f4; }
    h1, h2 { color: #333; }
    .container { max-width: 600px; margin: 0 auto; }
    .btn-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 20px 0; }
    .btn { display: block; width: 100%; padding: 20px 0; border: none; border-radius: 5px; color: white; font-size: 16px; cursor: pointer; }
    .btn-red { background-color: #f44336; }
    .btn-green { background-color: #4CAF50; }
    .btn-blue { background-color: #2196F3; }
    .btn-yellow { background-color: #FFEB3B; color: black; }
    .btn-purple { background-color: #9C27B0; }
    .btn-orange { background-color: #FF9800; }
    .btn-white { background-color: #FFFFFF; color: black; border: 1px solid #ddd; }
    
    /* Hex input styling */
    .input-container { margin: 30px 0; padding: 15px; background: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .input-container h2 { margin-top: 0; color: #444; }
    .color-preview { width: 50px; height: 50px; border-radius: 50%; margin: 10px auto; border: 1px solid #ddd; }
    .hex-input { padding: 10px; font-size: 16px; width: 140px; text-align: center; border: 1px solid #ddd; border-radius: 4px; }
    .btn-submit { padding: 10px 15px; margin-left: 10px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .btn-submit:hover { background: #0b7dda; }
    
    /* Servo styling */
    .slider-container { margin: 15px 0; }
    input[type="range"] { width: 80%; max-width: 400px; }
    .angle-display { font-weight: bold; font-size: 18px; margin: 10px 0; }
    
    /* Button status styling */
    .button-status-container { margin: 30px 0; padding: 15px; background: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .status-indicator { width: 20px; height: 20px; border-radius: 50%; display: inline-block; margin-right: 10px; }
    .status-on { background-color: #4CAF50; }
    .status-off { background-color: #f44336; }
    .status-text { font-weight: bold; font-size: 18px; display: inline-block; vertical-align: middle; }
    
    /* Brightness slider styling */
    .brightness-container { margin: 15px 0; }
    .brightness-value { font-weight: bold; font-size: 18px; display: inline-block; width: 40px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>ESP32 PositionUnit Control</h1>
    
    <!-- Button status -->
    <div class="button-status-container">
      <h2>Button Status (Pin 12)</h2>
      <div>
        <span id="buttonIndicator" class="status-indicator status-off"></span>
        <span id="buttonStatus" class="status-text">Not pressed</span>
      </div>
      <button class="btn-submit" style="margin-top: 10px;" onclick="refreshButtonStatus()">Refresh Status</button>
    </div>
    
    <!-- Servo control -->
    <div class="input-container">
      <h2>Servo Positioning</h2>
      <div class="slider-container">
        <input type="range" id="servoSlider" min="0" max="180" value="90" oninput="updateServoValue(this.value)">
      </div>
      <p class="angle-display">Angle: <span id="servoValue">90</span>°</p>
      <button class="btn-submit" onclick="setServoAngle()">Position Servo</button>
    </div>

    <!-- Motor control with extended speed control -->
    <div class="input-container">
      <h2>Stepper Motor Control</h2>
      <div class="slider-container">
        <input type="range" id="motorSlider" min="-500" max="500" value="0" oninput="updateMotorValue(this.value)">
      </div>
      <p class="angle-display">Position: <span id="motorValue">0</span></p>
      <button class="btn-submit" onclick="setMotorPosition()">Position Motor</button>
      
      <div style="margin-top: 15px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
        <button class="btn-submit" onclick="moveMotorSteps(100, 1)">100 steps forward</button>
        <button class="btn-submit" onclick="moveMotorSteps(100, -1)">100 steps backward</button>
        <button class="btn-submit" onclick="moveFullRotation(1)">1 rotation forward</button>
        <button class="btn-submit" onclick="moveFullRotation(-1)">1 rotation backward</button>
      </div>
      
      <div style="margin-top: 15px;">
        <label for="speedSlider">Speed:</label>
        <input type="range" id="speedSlider" min="0" max="100" value="70" oninput="updateSpeedValue(this.value)">
        <span id="speedValue">70</span>%
        <div style="margin-top: 5px; font-size: 12px;">
          <span>0% (slow) to 100% (maximum speed)</span>
        </div>
      </div>
    </div>
    
    <!-- Color control -->
    <h2>RGB LED Control</h2>
    
    <!-- New: Brightness slider -->
    <div class="input-container">
      <h2>LED Brightness</h2>
      <div class="brightness-container">
        <input type="range" id="brightnessSlider" min="0" max="255" value="5" oninput="updateBrightnessValue(this.value)">
        <span class="brightness-value" id="brightnessValue">5</span>
      </div>
      <button class="btn-submit" onclick="setBrightness()">Apply Brightness</button>
    </div>
    
    <div class="input-container">
      <h2>Custom Color</h2>
      <div id="colorPreview" class="color-preview"></div>
      <input type="text" id="hexInput" class="hex-input" placeholder="#FF0000" maxlength="7" value="#FF0000"/>
      <button class="btn-submit" onclick="changeHexColor()">Apply</button>
    </div>
    
    <p>Or choose a predefined color:</p>
    <div class="btn-grid">
      <button class="btn btn-red" onclick="changeColor(0)">Red</button>
      <button class="btn btn-green" onclick="changeColor(1)">Green</button>
      <button class="btn btn-blue" onclick="changeColor(2)">Blue</button>
      <button class="btn btn-yellow" onclick="changeColor(3)">Yellow</button>
      <button class="btn btn-purple" onclick="changeColor(4)">Purple</button>
      <button class="btn btn-orange" onclick="changeColor(5)">Orange</button>
      <button class="btn btn-white" onclick="changeColor(6)">White</button>
    </div>
    <p id="status">Status: Ready</p>
  </div>
  
  <script>
    // Button status variables
    let buttonPollingActive = true;
    let lastButtonState = false;
    
    // Query button status on page load
    document.addEventListener('DOMContentLoaded', function() {
      updateColorPreview();
      refreshButtonStatus();
    });

    // Faster button status polling (every 200ms instead of 1 second)
    setInterval(function() {
      if (buttonPollingActive) {
        refreshButtonStatus();
      }
    }, 200);
    
    // Fetch button status from server
    function refreshButtonStatus() {
      fetch('/getButtonState')
        .then(response => response.json())
        .then(data => {
          const buttonIndicator = document.getElementById('buttonIndicator');
          const buttonStatus = document.getElementById('buttonStatus');
          
          // Update only if the status has changed
          if (data.pressed !== lastButtonState) {
            // INVERTED: We show the opposite of the actual status
            if (!data.pressed) {  // If button is NOT pressed (data.pressed = false)
              buttonIndicator.className = 'status-indicator status-off';
              buttonStatus.textContent = 'Not pressed';
            } else {  // If button is pressed (data.pressed = true)
              buttonIndicator.className = 'status-indicator status-on';
              buttonStatus.textContent = 'Pressed';
            }
            lastButtonState = data.pressed;
          }
        })
        .catch(error => {
          console.error('Error fetching button status:', error);
          buttonPollingActive = false; // Stop polling on error
          setTimeout(() => { buttonPollingActive = true; }, 5000); // Retry after 5 seconds
        });
    }

    // Update color preview when input changes
    document.getElementById('hexInput').addEventListener('input', function() {
      updateColorPreview();
    });

    // Live color preview
    function updateColorPreview() {
      var hexValue = document.getElementById('hexInput').value;
      // Add # if not present
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
      // Add # if not present
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
    
    // New functions for brightness control
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
    
    // Function to update displayed servo angle
    function updateServoValue(val) {
      document.getElementById('servoValue').textContent = val;
    }
    
    // Function to set servo angle
    function setServoAngle() {
      const angle = document.getElementById('servoSlider').value;
      document.getElementById('status').innerHTML = 'Status: Positioning servo...';
      
      fetch('/setServo?angle=' + angle)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in servo control';
        });
    }

    // Function to update displayed motor value
    function updateMotorValue(val) {
      document.getElementById('motorValue').textContent = val;
    }
    
    // Function to set motor position
    function setMotorPosition() {
      const position = document.getElementById('motorSlider').value;
      document.getElementById('status').innerHTML = 'Status: Positioning motor...';
      
      fetch('/setMotor?position=' + position)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in motor control';
        });
    }
    
    // Function for a full rotation
    function moveFullRotation(direction) {
      document.getElementById('status').innerHTML = 'Status: Motor is performing a fast full rotation...';
      
      // The 28BYJ-48 requires 4096 steps for a full revolution
      const steps = 4096;
      const speed = parseInt(document.getElementById('speedSlider').value);
      
      fetch('/setMotor?steps=' + steps + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in motor control';
        });
    }

    // Function to update displayed speed value
    function updateSpeedValue(val) {
      document.getElementById('speedValue').textContent = val;
    }

    // Function to move motor by specific steps with speed
    function moveMotorSteps(steps, direction) {
      document.getElementById('status').innerHTML = 'Status: Motor is moving...';
      
      const speed = parseInt(document.getElementById('speedSlider').value);
      
      fetch('/setMotor?steps=' + steps + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Error in motor control';
        });
    }
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

// Handle motor control request
void handleMotorControl() {
  // For absolute position
  if (server.hasArg("position")) {
    int position = server.arg("position").toInt();
    moveMotorToPosition(position);  // Korrigiert von setMotorPosition zu moveMotorToPosition
    server.send(200, "text/plain", "Motor positioned to " + String(position));
    return;
  }
  
  // For stepping by number of steps
  if (server.hasArg("steps") && server.hasArg("direction")) {
    int steps = server.arg("steps").toInt();
    int direction = server.arg("direction").toInt();
    
    // Optional speed parameter (default 100% if not specified)
    int speed = 100;
    if (server.hasArg("speed")) {
      speed = server.arg("speed").toInt();
    }
    
    // Move motor with speed - verwende moveMotorWithSpeed statt moveMotor
    moveMotorWithSpeed(steps, direction, speed);
    
    server.send(200, "text/plain", "Motor moved " + String(steps) + 
                " steps in direction " + String(direction) + 
                " with speed " + String(speed) + "%");
    return;
  }
  
  // If no valid parameters
  server.send(400, "text/plain", "Missing or invalid parameters");
}

// Handle button state request
void handleGetButtonState() {
  bool isButtonPressed = getButtonState();  // Function from button_control.h
  
  // Create JSON response
  String jsonResponse = "{\"pressed\":" + String(isButtonPressed ? "true" : "false") + "}";
  
  server.send(200, "application/json", jsonResponse);
}

// New handler for LED brightness control
void handleBrightness() {
  if (server.hasArg("value")) {
    int brightness = server.arg("value").toInt();
    
    // Ensure brightness is valid (0-255)
    brightness = constrain(brightness, 0, 255);
    
    // Set LED brightness using the function from led_control.h
    setBrightness(brightness);
    
    // Send success response
    server.send(200, "text/plain", "Brightness set to " + String(brightness));
  } else {
    // Send error response if no value was specified
    server.send(400, "text/plain", "Missing 'value' parameter");
  }
}

// Handle not found (404)
void handleNotFound() {
  server.send(404, "text/plain", "404: Not found");
}