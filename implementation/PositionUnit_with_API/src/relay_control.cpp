#include "relay_control.h"

// Global variable to track relay state
bool relayState = false;

/**
 * Initialize the relay pin
 */
void setupRelay() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Start with relay OFF
  relayState = false;
  Serial.println("Relay control initialized on pin " + String(RELAY_PIN));
}

/**
 * Set the relay state
 * @param state - true for ON, false for OFF
 */
void setRelayState(bool state) {
  relayState = state;
  digitalWrite(RELAY_PIN, state ? HIGH : LOW);
  Serial.println("Relay turned " + String(state ? "ON" : "OFF"));
}

/**
 * Get the current relay state
 * @return current relay state (true = ON, false = OFF)
 */
bool getRelayState() {
  return relayState;
}

/**
 * Toggle the relay state
 */
void toggleRelay() {
  setRelayState(!relayState);
}