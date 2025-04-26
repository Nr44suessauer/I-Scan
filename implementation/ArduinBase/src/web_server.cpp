#include "web_server.h"

// Funktionsdeklarationen
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();

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
    h1 { color: #333; }
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
    .hex-input-container { margin: 30px 0; padding: 15px; background: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .hex-input-container h2 { margin-top: 0; color: #444; }
    .color-preview { width: 50px; height: 50px; border-radius: 50%; margin: 10px auto; border: 1px solid #ddd; }
    .hex-input { padding: 10px; font-size: 16px; width: 140px; text-align: center; border: 1px solid #ddd; border-radius: 4px; }
    .hex-btn { padding: 10px 15px; margin-left: 10px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .hex-btn:hover { background: #0b7dda; }
  </style>
</head>
<body>
  <div class="container">
    <h1>RGB LED Steuerung</h1>
    
    <div class="hex-input-container">
      <h2>Benutzerdefinierte Farbe</h2>
      <div id="colorPreview" class="color-preview"></div>
      <input type="text" id="hexInput" class="hex-input" placeholder="#FF0000" maxlength="7" value="#FF0000"/>
      <button class="hex-btn" onclick="changeHexColor()">Anwenden</button>
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
  </script>
</body>
</html>
)rawliteral";

void setupWebServer() {
  // Webserver-Routen einrichten
  server.on("/", HTTP_GET, handleRoot);
  server.on("/color", HTTP_GET, handleColorChange);
  server.on("/hexcolor", HTTP_GET, handleHexColorChange); 
  server.onNotFound(handleNotFound);
  
  // Webserver starten
  server.begin();
  Serial.println("HTTP-Server gestartet auf Port " + String(HTTP_PORT));
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