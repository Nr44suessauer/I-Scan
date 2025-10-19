#ifndef RELAY_CONTROL_H
#define RELAY_CONTROL_H

#include <Arduino.h>

// Relay configuration
const int RELAY_PIN = 17;

// Function declarations
void setupRelay();
void setRelayState(bool state);
bool getRelayState();
void toggleRelay();

#endif // RELAY_CONTROL_H