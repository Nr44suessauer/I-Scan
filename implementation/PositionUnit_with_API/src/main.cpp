#include <Arduino.h>
#include "wifi_manager.h"
#include "web_server.h"
#include "led_control.h"
#include "servo_control.h"  // Include servo header
#include "motor.h"          // Include motor header
#include "advanced_motor.h" // Include advanced motor header
#include "button_control.h" // Include button header
#include "motor_28byj48.h"  // Include 28BYJ-48 motor header

// Auto-Test Variablen
bool auto_test_running = false;
int auto_test_pins[10];
int auto_test_pin_count = 0;
int auto_test_steps = 50;
int auto_test_delay = 5;
int auto_test_between_delay = 1000;
int auto_test_timeout = 10; // Sekunden

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
  setup28BYJ48Motor();  // Initialize 28BYJ-48 motor (GPIO 4-7)
  
  // Button setup
  setupButton(); // Initialize button
  
  // Establish WiFi connection
  setupWiFi();
  
  // Start web server
  setupWebServer();
}

void loop() {
  // Handle server requests
  handleWebServerRequests();
  
  // Update motor (für non-blocking Operationen)
  updateMotor();
  
  // Update button state (for continuous monitoring)
  getButtonState();
  
  // Check WiFi connection
  checkWiFiConnection();
  
  // Auto-Test Handler
  if (auto_test_running) {
    auto_test_running = false; // Setze Flag zurück
    autoTest28BYJ48PinCombinations(auto_test_pins, auto_test_pin_count, auto_test_steps, auto_test_delay, auto_test_between_delay, auto_test_timeout);
  }
  
  delay(1); // Minimaler Delay für Stabilität - reduziert von 10ms auf 1ms für bessere Motor-Performance
}