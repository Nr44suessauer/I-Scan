#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"
#include "servo_control.h"  // Servo-Header einbinden
#include "motor.h"          // Motor-Header einbinden

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("I-Scan Controller gestartet");
  
  // LED-Setup
  setupLEDs();
  
  // Servo-Setup
  setupServo();  // Servo initialisieren
  
  // Motor-Setup
  setupMotor();  // Stepper-Motor initialisieren
  
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