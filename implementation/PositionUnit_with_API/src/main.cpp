#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"
#include "servo_control.h"  // Include servo header
#include "motor.h"          // Include motor header
#include "advanced_motor.h" // Include advanced motor header
#include "button_control.h" // Include button header
#include "relay_control.h"  // Include relay header
#include "realtime_system.h" // Include realtime system header

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("I-Scan Controller started");
  
  // LED setup
  setupLEDs();
  
  // Servo setup
  setupServo();  // Initialize servo
  
  // Motor setup
  setupMotor();  // Initialize stepper motor (legacy)
  setupAdvancedMotor();  // Initialize advanced stepper motor
  
  // Button setup
  setupButton(); // Initialize button
  
  // Relay setup
  setupRelay(); // Initialize relay
  
  // Establish WiFi connection
  setupWiFi();
  
  // Set up and start web server
  setupWebServer();
  
  // Initialize realtime system (5ms interval for all components)
  initRealtimeSystem(5);
  Serial.println("Echtzeit-System für alle Komponenten aktiviert");

  // Change color after WiFi connection
  setColorByIndex(1);  // Green for successful WiFi connection
}

void loop() {
  // HAUPTSCHLEIFE: Echtzeit-Update aller Komponenten
  updateAllComponents();
  
  // Minimale Verzögerung für Stabilität
  delay(1); // 1ms für optimale Echtzeit-Performance
}