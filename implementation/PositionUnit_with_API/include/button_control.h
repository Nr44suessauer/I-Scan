#ifndef BUTTON_CONTROL_H
#define BUTTON_CONTROL_H

#include <Arduino.h>

// Button pin definition
#define BUTTON_PIN 12     // Button input pin

// Function prototypes
void setupButton();
bool getButtonState();

#endif // BUTTON_CONTROL_H