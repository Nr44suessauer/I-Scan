#include "realtime_system.h"
#include "relay_control.h"
#include "led_control.h"
#include "servo_control.h"
#include "advanced_motor.h"
#include "button_control.h"
#include "web_server.h"

// Globale Variablen
unsigned long lastGlobalRealtimeUpdate = 0;
unsigned long globalRealtimeInterval = 5;  // 5ms Standard-Intervall
bool realtimeSystemEnabled = true;

// Komponenten-Update-Flags
ComponentUpdateFlags updateFlags = {
    true,   // relayUpdate
    true,   // ledUpdate
    true,   // servoUpdate
    true,   // motorUpdate
    true,   // buttonUpdate
    true    // networkUpdate
};

// Initialisierung des Echtzeit-Systems
void initRealtimeSystem(unsigned long intervalMs) {
    globalRealtimeInterval = intervalMs;
    lastGlobalRealtimeUpdate = 0;
    realtimeSystemEnabled = true;
    
    Serial.printf("Realtime system initialized with %lums interval\n", intervalMs);
}

// Main update function for all components
void updateAllComponents() {
    if (!realtimeSystemEnabled) return;
    
    unsigned long currentTime = millis();
    
    // Check if update interval has been reached
    if (currentTime - lastGlobalRealtimeUpdate >= globalRealtimeInterval) {
        // Update einzelne Komponenten basierend auf Flags
        if (updateFlags.relayUpdate) {
            updateRelayComponent();
        }
        
        if (updateFlags.ledUpdate) {
            updateLedComponent();
        }
        
        if (updateFlags.servoUpdate) {
            updateServoComponent();
        }
        
        if (updateFlags.motorUpdate) {
            updateMotorComponent();
        }
        
        if (updateFlags.buttonUpdate) {
            updateButtonComponent();
        }
        
        if (updateFlags.networkUpdate) {
            updateNetworkComponent();
        }
        
        lastGlobalRealtimeUpdate = currentTime;
    }
}

// Aktiviert/Deaktiviert Echtzeit-Updates
void enableRealtimeUpdates() {
    realtimeSystemEnabled = true;
    Serial.println("Echtzeit-Updates aktiviert");
}

void disableRealtimeUpdates() {
    realtimeSystemEnabled = false;
    Serial.println("Realtime updates disabled");
}

// Sets update flag for specific component
void setComponentUpdateFlag(const char* component, bool enabled) {
    if (strcmp(component, "relay") == 0) {
        updateFlags.relayUpdate = enabled;
    } else if (strcmp(component, "led") == 0) {
        updateFlags.ledUpdate = enabled;
    } else if (strcmp(component, "servo") == 0) {
        updateFlags.servoUpdate = enabled;
    } else if (strcmp(component, "motor") == 0) {
        updateFlags.motorUpdate = enabled;
    } else if (strcmp(component, "button") == 0) {
        updateFlags.buttonUpdate = enabled;
    } else if (strcmp(component, "network") == 0) {
        updateFlags.networkUpdate = enabled;
    }
    
    Serial.printf("Komponente '%s' Echtzeit-Update: %s\n", component, enabled ? "aktiviert" : "deaktiviert");
}

// Erzwingt sofortiges Update aller Komponenten
void forceUpdateAllComponents() {
    Serial.println("Erzwinge sofortiges Update aller Komponenten...");
    updateRelayComponent();
    updateLedComponent();
    updateServoComponent();
    updateMotorComponent();
    updateButtonComponent();
    updateNetworkComponent();
}

// Sets the realtime update interval
void setRealtimeInterval(unsigned long intervalMs) {
    // Validate interval range (1ms to 1000ms)
    if (intervalMs < 1) intervalMs = 1;
    if (intervalMs > 1000) intervalMs = 1000;
    
    globalRealtimeInterval = intervalMs;
    Serial.printf("Realtime update interval set to %lums\n", intervalMs);
}

// Gets the current realtime update interval
unsigned long getRealtimeInterval() {
    return globalRealtimeInterval;
}

// Component-specific update functions
void updateRelayComponent() {
    // Check for pending relay changes
    // This function can be extended for pending relay commands
    static bool lastRelayState = false;
    bool currentRelayState = getRelayState();
    
    if (currentRelayState != lastRelayState) {
        // Relay state has changed - possible actions
        lastRelayState = currentRelayState;
    }
}

void updateLedComponent() {
    // Check for pending LED changes
    // This function can be extended for LED animations, fading, etc.
    static unsigned long lastLedUpdate = 0;
    unsigned long currentTime = millis();
    
    // Example: LED heartbeat every 1000ms
    if (currentTime - lastLedUpdate >= 1000) {
        // LED heartbeat logic here
        lastLedUpdate = currentTime;
    }
}

void updateServoComponent() {
    // Check for pending servo movements
    // This function can be extended for smooth servo movements
    static int lastServoPosition = -1;
    // Here we could check the current servo state
}

void updateMotorComponent() {
    // Motor-specific realtime updates
    // This is covered by the AdvancedStepperMotor::update() function
    advancedMotor.update();
}

void updateButtonComponent() {
    // Check button state changes for immediate reaction
    static bool lastButtonState = true;
    bool currentButtonState = getButtonState();
    
    if (currentButtonState != lastButtonState) {
        // Button state has changed
        Serial.printf("Button state change detected: %s\n", 
                     currentButtonState ? "released" : "pressed");
        lastButtonState = currentButtonState;
        
        // Immediate button reactions can be implemented here
        // e.g. emergency stop, pause, etc.
    }
}

void updateNetworkComponent() {
    // Check for pending network commands
    // Web server requests are processed here
    handleWebServerRequests();
}