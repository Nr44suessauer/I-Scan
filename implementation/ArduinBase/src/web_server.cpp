#include "web_server.h"
#include "servo_control.h" // Füge diese Zeile zu den bestehenden Includes hinzu
#include "motor.h" // Füge zu den bestehenden Includes hinzu:

// Funktionsdeklarationen
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();
void handleServoControl(); // Füge diese Zeile zu den Funktionsdeklarationen am Anfang der Datei hinzu
void handleMotorControl(); // Füge zur Funktionsdeklaration am Anfang der Datei hinzu:

// WebServer-Konfiguration
const uint16_t HTTP_PORT = 80;
WebServer server(HTTP_PORT);

// HTML-Webseite mit Buttons zur LED-Steuerung
const char* html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RGB LED Steuerung</title>
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
    
    /* Hex-Eingabe Styling */
    .input-container { margin: 30px 0; padding: 15px; background: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .input-container h2 { margin-top: 0; color: #444; }
    .color-preview { width: 50px; height: 50px; border-radius: 50%; margin: 10px auto; border: 1px solid #ddd; }
    .hex-input { padding: 10px; font-size: 16px; width: 140px; text-align: center; border: 1px solid #ddd; border-radius: 4px; }
    .btn-submit { padding: 10px 15px; margin-left: 10px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .btn-submit:hover { background: #0b7dda; }
    
    /* Servo Styling */
    .slider-container { margin: 15px 0; }
    input[type="range"] { width: 80%; max-width: 400px; }
    .angle-display { font-weight: bold; font-size: 18px; margin: 10px 0; }
  </style>
</head>
<body>
  <div class="container">
    <h1>ESP32 I-Scan Steuerung</h1>
    
    <!-- Servo-Steuerung -->
    <div class="input-container">
      <h2>Servo-Positionierung</h2>
      <div class="slider-container">
        <input type="range" id="servoSlider" min="0" max="180" value="90" oninput="updateServoValue(this.value)">
      </div>
      <p class="angle-display">Winkel: <span id="servoValue">90</span>°</p>
      <button class="btn-submit" onclick="setServoAngle()">Servo positionieren</button>
    </div>

    <!-- Motor-Steuerung mit erweitertem Geschwindigkeitsregler -->
    <div class="input-container">
      <h2>Stepper-Motor Steuerung</h2>
      <div class="slider-container">
        <input type="range" id="motorSlider" min="-500" max="500" value="0" oninput="updateMotorValue(this.value)">
      </div>
      <p class="angle-display">Position: <span id="motorValue">0</span></p>
      <button class="btn-submit" onclick="setMotorPosition()">Motor positionieren</button>
      
      <div style="margin-top: 15px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
        <button class="btn-submit" onclick="moveMotorSteps(100, 1)">100 Schritte vorwärts</button>
        <button class="btn-submit" onclick="moveMotorSteps(100, -1)">100 Schritte rückwärts</button>
        <button class="btn-submit" onclick="moveFullRotation(1)">1 Umdrehung vorwärts</button>
        <button class="btn-submit" onclick="moveFullRotation(-1)">1 Umdrehung rückwärts</button>
      </div>
      
      <div style="margin-top: 15px;">
        <label for="speedSlider">Geschwindigkeit:</label>
        <input type="range" id="speedSlider" min="0" max="100" value="70" oninput="updateSpeedValue(this.value)">
        <span id="speedValue">70</span>%
        <div style="margin-top: 5px; font-size: 12px;">
          <span>0% (langsam) bis 100% (Maximalgeschwindigkeit)</span>
        </div>
      </div>
    </div>
    
    <!-- Farbsteuerung -->
    <h2>RGB LED Steuerung</h2>
    
    <div class="input-container">
      <h2>Benutzerdefinierte Farbe</h2>
      <div id="colorPreview" class="color-preview"></div>
      <input type="text" id="hexInput" class="hex-input" placeholder="#FF0000" maxlength="7" value="#FF0000"/>
      <button class="btn-submit" onclick="changeHexColor()">Anwenden</button>
    </div>
    
    <p>Oder wähle eine vordefinierte Farbe:</p>
    <div class="btn-grid">
      <button class="btn btn-red" onclick="changeColor(0)">Rot</button>
      <button class="btn btn-green" onclick="changeColor(1)">Grün</button>
      <button class="btn btn-blue" onclick="changeColor(2)">Blau</button>
      <button class="btn btn-yellow" onclick="changeColor(3)">Gelb</button>
      <button class="btn btn-purple" onclick="changeColor(4)">Lila</button>
      <button class="btn btn-orange" onclick="changeColor(5)">Orange</button>
      <button class="btn btn-white" onclick="changeColor(6)">Weiß</button>
    </div>
    <p id="status">Status: Bereit</p>
  </div>
  
  <script>
    // Update color preview when page loads
    document.addEventListener('DOMContentLoaded', function() {
      updateColorPreview();
    });

    // Update color preview when input changes
    document.getElementById('hexInput').addEventListener('input', function() {
      updateColorPreview();
    });

    // Live-Vorschau der Farbe
    function updateColorPreview() {
      var hexValue = document.getElementById('hexInput').value;
      // Falls kein # vorhanden, hinzufügen
      if (hexValue.charAt(0) !== '#') {
        hexValue = '#' + hexValue;
        document.getElementById('hexInput').value = hexValue;
      }
      document.getElementById('colorPreview').style.backgroundColor = hexValue;
    }

    function changeColor(colorIndex) {
      document.getElementById('status').innerHTML = 'Status: Farbe wird geändert...';
      fetch('/color?index=' + colorIndex)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler beim Ändern der Farbe';
        });
    }
    
    function changeHexColor() {
      var hexValue = document.getElementById('hexInput').value;
      // Falls kein # vorhanden, hinzufügen
      if (hexValue.charAt(0) !== '#') {
        hexValue = '#' + hexValue;
      }
      
      document.getElementById('status').innerHTML = 'Status: Farbe wird geändert...';
      fetch('/hexcolor?hex=' + encodeURIComponent(hexValue))
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler beim Ändern der Farbe';
        });
    }
    
    // Funktion zum Aktualisieren des angezeigten Servo-Winkels
    function updateServoValue(val) {
      document.getElementById('servoValue').textContent = val;
    }
    
    // Funktion zum Setzen des Servo-Winkels
    function setServoAngle() {
      const angle = document.getElementById('servoSlider').value;
      document.getElementById('status').innerHTML = 'Status: Servo wird positioniert...';
      
      fetch('/setServo?angle=' + angle)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler bei der Servo-Steuerung';
        });
    }

    // Funktion zum Aktualisieren des angezeigten Motor-Werts
    function updateMotorValue(val) {
      document.getElementById('motorValue').textContent = val;
    }
    
    // Funktion zum Setzen der Motor-Position
    function setMotorPosition() {
      const position = document.getElementById('motorSlider').value;
      document.getElementById('status').innerHTML = 'Status: Motor wird positioniert...';
      
      fetch('/setMotor?position=' + position)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler bei der Motor-Steuerung';
        });
    }
    
    // Funktion für eine komplette Umdrehung
    function moveFullRotation(direction) {
      document.getElementById('status').innerHTML = 'Status: Motor führt schnelle vollständige Umdrehung durch...';
      
      // Der 28BYJ-48 benötigt 4096 Schritte für eine volle Umdrehung
      const steps = 4096;
      const speed = parseInt(document.getElementById('speedSlider').value);
      
      fetch('/setMotor?steps=' + steps + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler bei der Motor-Steuerung';
        });
    }

    // Funktion zum Aktualisieren des angezeigten Geschwindigkeitswerts
    function updateSpeedValue(val) {
      document.getElementById('speedValue').textContent = val;
    }

    // Funktion zum Bewegen des Motors um bestimmte Schritte mit Geschwindigkeit
    function moveMotorSteps(steps, direction) {
      document.getElementById('status').innerHTML = 'Status: Motor bewegt sich...';
      
      const speed = parseInt(document.getElementById('speedSlider').value);
      
      fetch('/setMotor?steps=' + steps + '&direction=' + direction + '&speed=' + speed)
        .then(response => response.text())
        .then(data => {
          document.getElementById('status').innerHTML = 'Status: ' + data;
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Status: Fehler bei der Motor-Steuerung';
        });
    }
  </script>
</body>
</html>
)rawliteral";

void setupWebServer() {
  // Webserver-Routen einrichten
  server.on("/", HTTP_GET, handleRoot);
  server.on("/color", HTTP_GET, handleColorChange);
  server.on("/hexcolor", HTTP_GET, handleHexColorChange); 
  server.on("/setServo", HTTP_GET, handleServoControl);
  server.on("/setMotor", HTTP_GET, handleMotorControl); // Füge diesen Handler in setupWebServer() ein, vor server.begin():
  server.onNotFound(handleNotFound);

  // Webserver starten
  server.begin();
  Serial.println("HTTP-Server gestartet auf Port " + String(HTTP_PORT));
}

// Neuer Handler für die Servo-Steuerung
void handleServoControl() {
  if (server.hasArg("angle")) {
    int angle = server.arg("angle").toInt();
    // Winkel auf gültigen Bereich beschränken
    angle = constrain(angle, 0, 180);
    // Servo auf den angegebenen Winkel einstellen
    sweepServo(angle, 15);
    
    // Erfolgsantwort senden
    server.send(200, "text/plain", "Servo auf " + String(angle) + "° gesetzt");
  } else {
    // Fehlerantwort, wenn kein Winkel angegeben wurde
    server.send(400, "text/plain", "Parameter 'angle' fehlt");
  }
}

// Füge diese Funktion nach handleServoControl() ein:

// Handler für die Motorsteuerung
void handleMotorControl() {
  if (server.hasArg("position")) {
    int position = server.arg("position").toInt();
    // Position auf einen sinnvollen Bereich beschränken
    position = constrain(position, -4096, 4096);
    
    // Motor zur angegebenen Position bewegen
    moveMotorToPosition(position);
    
    // Erfolgsantwort senden
    server.send(200, "text/plain", "Motor auf Position " + String(position) + " bewegt");
  } else if (server.hasArg("steps") && server.hasArg("direction")) {
    int steps = server.arg("steps").toInt();
    int direction = server.arg("direction").toInt();
    int speed = 70; // Standardgeschwindigkeit auf Skala (0-100)
    
    // Optional: Geschwindigkeit aus Anfrage lesen, falls vorhanden
    if (server.hasArg("speed")) {
      speed = server.arg("speed").toInt();
    }
    
    // Werte auf sinnvolle Bereiche beschränken
    steps = constrain(steps, 0, 4096);
    direction = (direction > 0) ? 1 : -1;
    speed = constrain(speed, 0, 100); // UI zeigt 0-100, aber motor.cpp begrenzt auf 0-90
    
    // Spezielle Nachricht für vollständige Umdrehungen
    String responseMessage;
    if (steps == 4096) {
      responseMessage = "Motor hat " + String(direction > 0 ? "eine" : "eine rückwärtige") + 
                       " vollständige Umdrehung mit Geschwindigkeit " + String(speed) + "% durchgeführt";
    } else {
      responseMessage = "Motor um " + String(steps) + " Schritte in Richtung " + 
                       String(direction) + " mit Geschwindigkeit " + String(speed) + "% bewegt";
    }
    
    // Motor für die angegebenen Schritte mit angegebener Geschwindigkeit bewegen
    moveMotorWithSpeed(steps, direction, speed);
    
    // Erfolgsantwort senden
    server.send(200, "text/plain", responseMessage);
  }
}

void handleWebServerRequests() {
  server.handleClient();
}

// Handler für die Root-Route
void handleRoot() {
  server.send(200, "text/html", html);
}

// Handler zum Ändern der LED-Farbe
void handleColorChange() {
  if (server.hasArg("index")) {
    int colorIndex = server.arg("index").toInt();
    
    // Sicherstellen, dass der Index gültig ist (0-6)
    if (colorIndex >= 0 && colorIndex <= 6) {
      setColorByIndex(colorIndex);
      server.send(200, "text/plain", "Farbe erfolgreich geändert auf Index " + String(colorIndex));
    } else {
      server.send(400, "text/plain", "Ungültiger Farbindex!");
    }
  } else {
    server.send(400, "text/plain", "Kein Farbindex angegeben!");
  }
}

// Handler für Hex-Farbwechsel
void handleHexColorChange() {
  if (server.hasArg("hex")) {
    String hexColor = server.arg("hex");
    
    // '#' entfernen falls vorhanden
    if (hexColor.startsWith("#")) {
      hexColor = hexColor.substring(1);
    }
    
    // Überprüfen, ob es ein gültiger Hex-Farbcode ist (6 Zeichen)
    if (hexColor.length() == 6) {
      // Hex-String in RGB-Werte umwandeln
      uint32_t rgb = strtol(hexColor.c_str(), NULL, 16);
      uint8_t r = (rgb >> 16) & 0xFF;
      uint8_t g = (rgb >> 8) & 0xFF;
      uint8_t b = rgb & 0xFF;
      
      // RGB-Werte an die LED senden
      setColorRGB(r, g, b);
      server.send(200, "text/plain", "Farbe erfolgreich geändert auf #" + hexColor);
    } else {
      server.send(400, "text/plain", "Ungültiger Hex-Farbcode! Format: #RRGGBB");
    }
  } else {
    server.send(400, "text/plain", "Keine Hex-Farbe angegeben!");
  }
}

// Handler für nicht gefundene URLs
void handleNotFound() {
  server.send(404, "text/plain", "404: Seite nicht gefunden");
}