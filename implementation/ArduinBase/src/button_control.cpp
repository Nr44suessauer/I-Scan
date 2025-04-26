#include "button_control.h"

// Variables for faster debouncing
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 20;    // Debounce delay reduced to 20ms for faster response
int lastButtonState = HIGH;          // Last known state of the button
int buttonState = HIGH;              // Current stable state of the button
bool buttonStateChanged = false;     // Flag for state change

/**
 * @brief Initializes the button pin as input with pull-up resistor.
 */
void setupButton() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    Serial.println("Button at pin " + String(BUTTON_PIN) + " initialized");
    
    // Initially read and output button status
    int initialState = digitalRead(BUTTON_PIN);
    Serial.println("Initial button status: " + String(initialState == HIGH ? "HIGH (not pressed)" : "LOW (pressed)"));
}

/**
 * @brief Reads the current state of the button with optimized debouncing.
 * 
 * Since INPUT_PULLUP is used, the function would normally return true when the button
 * is pressed (LOW) and false when it's not pressed (HIGH).
 * 
 * This version inverts the normal button status: true when not pressed, false when pressed.
 * 
 * @return bool - true when the button is NOT pressed, false when pressed
 */
bool getButtonState() {
    // Read current button state directly
    int reading = digitalRead(BUTTON_PIN);
    unsigned long currentTime = millis();
    
    // Periodic debug output (every 5 seconds instead of 2 seconds)
    static unsigned long lastDebugTime = 0;
    if (currentTime - lastDebugTime > 5000) {
        Serial.println("Button pin " + String(BUTTON_PIN) + " status: " + 
                      String(reading == HIGH ? "HIGH (not pressed)" : "LOW (pressed)"));
        lastDebugTime = currentTime;
    }
    
    // If input has changed since last reading
    if (reading != lastButtonState) {
        lastDebounceTime = currentTime;  // Store time of state change
        buttonStateChanged = true;       // Mark change
    }
    
    // If enough time has passed since last change
    if ((currentTime - lastDebounceTime) > debounceDelay && buttonStateChanged) {
        // If state is stable and has changed
        if (reading != buttonState) {
            buttonState = reading;
            
            // Debug output on state change
            Serial.println("Button status changed to: " + 
                         String(buttonState == HIGH ? "HIGH (not pressed)" : "LOW (pressed)"));
        }
        buttonStateChanged = false;  // Reset change flag
    }
    
    // Save current state for next iteration
    lastButtonState = reading;
    
    // With INPUT_PULLUP, LOW = pressed, HIGH = not pressed
    // Return button state directly (inverted behavior)
    return buttonState;
}