#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"
#include "servo_control.h"  // Servo-Header einbinden

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("RGB LED Controller mit WebServer gestartet");
  
  // LED-Setup
  setupLEDs();
  
  // Servo-Setup
  setupServo();  // Servo initialisieren
  
  // WiFi-Verbindung herstellen
  setupWiFi();
  
  // Webserver einrichten und starten
  setupWebServer();

  // Farbänderung nach WLAN-Verbindung
  setColorByIndex(1);  // Grün für erfolgreiche WLAN-Verbindung
  
  // Servo-Test - bewegt den Servo von der aktuellen Position (standardmäßig 90°) zu 45° und dann zu 135°
  delay(1000);
  sweepServo(45, 20);  // Zu 45° bewegen mit einer Geschwindigkeit von 20ms pro Grad
  delay(1000);
  sweepServo(135, 20);  // Zu 135° bewegen
}

void loop() {
  // Server-Anfragen bearbeiten
  handleWebServerRequests();
  
  // WiFi-Verbindung überprüfen
  checkWiFiConnection();
  
  delay(10); // kurze Pause für Stabilitätsverbesserung
}