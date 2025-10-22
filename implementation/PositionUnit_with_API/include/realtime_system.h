#ifndef REALTIME_SYSTEM_H
#define REALTIME_SYSTEM_H

#include <Arduino.h>

// Global Realtime Update Variables
extern unsigned long lastGlobalRealtimeUpdate;
extern unsigned long globalRealtimeInterval;
extern bool realtimeSystemEnabled;

// Component Update Flags
struct ComponentUpdateFlags {
    bool relayUpdate;           // Check relay state
    bool ledUpdate;             // Check LED state  
    bool servoUpdate;           // Check servo position
    bool motorUpdate;           // Check motor state
    bool buttonUpdate;          // Check button state
    bool networkUpdate;         // Check network commands
};

extern ComponentUpdateFlags updateFlags;

// Functions for the Realtime System
void initRealtimeSystem(unsigned long intervalMs = 5);  // Default: 5ms updates
void updateAllComponents();                             // Update all components
void enableRealtimeUpdates();                          // Enables realtime updates
void disableRealtimeUpdates();                         // Disables realtime updates
void setComponentUpdateFlag(const char* component, bool enabled);  // Sets update flag
void forceUpdateAllComponents();                       // Forces immediate update
void setRealtimeInterval(unsigned long intervalMs);    // Sets update interval
unsigned long getRealtimeInterval();                   // Gets current update interval

// Component-specific Update Functions
void updateRelayComponent();                           // Relay realtime update
void updateLedComponent();                             // LED realtime update
void updateServoComponent();                           // Servo realtime update
void updateMotorComponent();                           // Motor realtime update
void updateButtonComponent();                          // Button realtime update
void updateNetworkComponent();                         // Network realtime update

#endif // REALTIME_SYSTEM_H