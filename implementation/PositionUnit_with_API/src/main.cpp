#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"
#include "servo_control.h"  // Include servo header
#include "motor.h"          // Include motor header
#include "button_control.h" // Include button header

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("I-Scan Controller started");
  
  // LED setup
  setupLEDs();
  
  // Servo setup
  setupServo();  // Initialize servo
  
  // Motor setup
  setupMotor();  // Initialize stepper motor
  
  // Button setup
  setupButton(); // Initialize button
  
  // Establish WiFi connection
  setupWiFi();
  
  // Set up and start web server
  setupWebServer();

  // Change color after WiFi connection
  setColorByIndex(1);  // Green for successful WiFi connection
}

void loop() {
  // Handle server requests
  handleWebServerRequests();
  
  // Check WiFi connection
  checkWiFiConnection();
  
  delay(10); // Short pause for stability improvement
}