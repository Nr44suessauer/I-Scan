#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("RGB LED Controller mit WebServer gestartet");
  
  // LED-Setup
  setupLEDs();
  
  // WiFi-Verbindung herstellen
  setupWiFi();
  
  // Webserver einrichten und starten
  setupWebServer();

  // Farbänderung nach WLAN-Verbindung
  setColorByIndex(1);  // Grün für erfolgreiche WLAN-Verbindung
}

void loop() {
  // Server-Anfragen bearbeiten
  handleWebServerRequests();
  
  // WiFi-Verbindung überprüfen
  checkWiFiConnection();
  
  delay(10); // kurze Pause für Stabilitätsverbesserung
}