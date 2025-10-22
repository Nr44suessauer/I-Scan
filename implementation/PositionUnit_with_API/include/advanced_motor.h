#ifndef ADVANCED_MOTOR_H
#define ADVANCED_MOTOR_H

#include <Arduino.h>

// Pin-Definitionen für Schrittmotor
#define STEP_PIN 37
#define DIR_PIN 36
#define ENABLE_PIN -1  // Optional: Pin zum Aktivieren/Deaktivieren des Motors

// Motor-Konfiguration
#define ADVANCED_STEPS_PER_REVOLUTION 200  // Standard für NEMA17 (1.8° pro Schritt)
#define MICROSTEPS 1                       // Microstepping-Faktor
#define MAX_SPEED_RPM 500                  // Maximale Geschwindigkeit in RPM
#define DEFAULT_SPEED_RPM 100              // Standard-Geschwindigkeit in RPM
#define ACCELERATION_STEPS 50    // Schritte für Beschleunigung/Verzögerung

// Debug-Konfiguration
#define MOTOR_DEBUG_ENABLED true           // Debug-Ausgaben ein/ausschalten (zur Compile-Zeit)

// Globale Debug-Variable (zur Laufzeit änderbar)
extern bool motorDebugEnabled;

// Debug-Makros mit Laufzeit-Check
#if MOTOR_DEBUG_ENABLED
  #define MOTOR_DEBUG_PRINT(x) do { if (motorDebugEnabled) Serial.print(x); } while(0)
  #define MOTOR_DEBUG_PRINTLN(x) do { if (motorDebugEnabled) Serial.println(x); } while(0)
  #define MOTOR_DEBUG_PRINTF(format, ...) do { if (motorDebugEnabled) Serial.printf(format, __VA_ARGS__); } while(0)
#else
  #define MOTOR_DEBUG_PRINT(x)
  #define MOTOR_DEBUG_PRINTLN(x)
  #define MOTOR_DEBUG_PRINTF(format, ...)
#endif

// Motor-Status-Struktur (vereinfacht)
typedef struct {
    int currentPosition;
    int targetPosition;
    int virtualHomePosition;
    bool isMoving;
    int currentSpeed;
    bool isHomed;
    bool isEnabled;
} AdvancedMotorStatus;

// Klasse für erweiterte Schrittmotorsteuerung
class AdvancedStepperMotor {
private:
    int stepPin;
    int dirPin;
    int enablePin;
    
    int currentPosition;
    int targetPosition;
    int virtualHomePosition; // Virtuelle Home-Position
    bool isMoving;
    bool isEnabled;
    bool isHomed;

    
    int stepsPerRevolution;
    int currentSpeedRPM;
    unsigned long stepDelayMicros;
    unsigned long lastStepTime;
    
    void calculateStepDelay();
    
public:
    AdvancedStepperMotor(int stepPin, int dirPin, int enablePin = -1, int stepsPerRevolution = 200);
    
    // Initialisierung
    void begin();
    void enable();
    void disable();
    void setPinsIdle();  // Neue Funktion: Pins in Ruhezustand setzen
    
    // Grundlegende Bewegungsfunktionen
    void setSpeed(int rpm);
    void setDirection(bool clockwise);
    void step();
    void moveSteps(int steps);
    // Basis-Bewegungsfunktionen (nur von UI verwendet)
    void moveTo(int position);
    void moveRelative(int steps);
    
    // Steuerungsfunktionen (nur von UI verwendet)  
    void stop();
    void setHome();
    void homeToButton();  // Neue Funktion: Fahre zur Button-Position als Home
    void setVirtualHome(); // Neue Funktion: Setze aktuelle Position als virtuelle Home
    void moveToVirtualHome(); // Neue Funktion: Fahre zur virtuellen Home-Position

    
    // Status-Funktionen
    int getCurrentPosition();
    int getTargetPosition();
    int getVirtualHomePosition(); // Getter für virtuelle Home-Position
    bool getIsMoving();
    bool getIsEnabled();
    bool getIsHomed();

    int getCurrentSpeed();
    AdvancedMotorStatus getStatus();
    
    // Konfiguration
    void setStepsPerRevolution(int steps);
    void setMicrostepping(int factor);
    
    // Non-blocking Bewegung (für kontinuierliche Bewegungen)
    void update();  // Muss regelmäßig in loop() aufgerufen werden
    void startNonBlockingMoveTo(int position);
    void startNonBlockingMoveSteps(int steps);
};

// Globale Instanz
extern AdvancedStepperMotor advancedMotor;

// Hilfsfunktionen
void setupAdvancedMotor();
void updateMotor();
void homeMotorToButton();  // Home-Fahrt zum Button
void calibrateVirtualHome(); // Setze virtuelle Home-Position
void moveToVirtualHome(); // Fahre zur virtuellen Home-Position

// Debug-Funktionen
void setMotorDebug(bool enabled);     // Debug ein/ausschalten
bool getMotorDebugStatus();          // Debug-Status abfragen

// Web-API Funktionen
void handleAdvancedMotorControl();
void handleAdvancedMotorStatus();
void handleAdvancedMotorStop();
void handleAdvancedMotorHome();
void handleAdvancedMotorJog();
void handleAdvancedMotorCalibrate();


#endif // ADVANCED_MOTOR_H