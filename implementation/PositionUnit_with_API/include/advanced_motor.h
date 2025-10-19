#ifndef ADVANCED_MOTOR_H
#define ADVANCED_MOTOR_H

#include <Arduino.h>

// Pin definitions for stepper motor
#define STEP_PIN 37
#define DIR_PIN 36
#define ENABLE_PIN -1  // Optional: Pin zum Aktivieren/Deaktivieren des Motors

// Motor-Konfiguration
#define STEPS_PER_REVOLUTION 200  // Standard for NEMA17 (1.8° per step)
#define MICROSTEPS 1             // Microstepping-Faktor
#define MAX_SPEED_RPM 300        // Maximale Geschwindigkeit in RPM
#define DEFAULT_SPEED_RPM 60     // Standard-Geschwindigkeit in RPM
#define ACCELERATION_STEPS 50    // Steps for acceleration/deceleration

// Motor-Status-Struktur
typedef struct {
    int currentPosition;
    int targetPosition;
    bool isMoving;
    int currentSpeed;
    bool isHomed;
    bool isEnabled;
    bool usePhysicalHome;       // Status for homing mode
    bool isButtonHomingActive;  // New status for button homing mode
    bool isRowCounterActive;    // Row Counter aktiv
    int currentRows;            // Aktuelle Anzahl Rows
    int targetRows;             // Ziel-Anzahl Rows

    unsigned long lastMoveTime;
} AdvancedMotorStatus;

// Class for advanced stepper motor control
class AdvancedStepperMotor {
private:
    int stepPin;
    int dirPin;
    int enablePin;
    
    int currentPosition;
    int targetPosition;
    bool isMoving;
    bool isEnabled;
    bool isHomed;
    bool usePhysicalHome;       // True: Physisches Home mit Button, False: Virtuelles Home
    bool isButtonHomingActive;  // Button-Homing-Modus aktiv
    
    // Row Counter Variablen
    bool isRowCounterActive;    // Row Counter aktiv
    int currentRows;            // Aktuelle Anzahl Rows
    int targetRows;             // Ziel-Anzahl Rows
    bool lastButtonState;       // Last button state for edge detection
    enum RowCounterState {
        ROW_COUNTER_IDLE,
        ROW_COUNTER_MOVING      // Kontinuierliche Bewegung bis Button gedrückt wird
    } rowCounterState;

    
    int stepsPerRevolution;
    int currentSpeedRPM;
    unsigned long stepDelayMicros;
    unsigned long lastStepTime;
    
    void calculateStepDelay();
    void performStep();
    
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
    void moveTo(int position);
    void moveRelative(int steps);
    void moveDegrees(float degrees);
    void moveRevolutions(float revolutions);
    
    // Erweiterte Bewegungsfunktionen
    void moveWithAcceleration(int steps, int startRPM, int endRPM);
    void moveSmoothly(int steps, int targetRPM);
    void jogContinuous(bool direction, int rpm);
    
    // Steuerungsfunktionen
    void stop();
    void emergencyStop();
    void home();
    void setHome();
    void calibrate();
    void setUsePhysicalHome(bool usePhysical);  // Setzt den Homing-Modus
    bool getUsePhysicalHome();     // Gibt den aktuellen Homing-Modus zurück
    void startButtonHomingMode();  // Neue Funktion: Fährt bis Button gedrückt wird
    void stopButtonHomingMode();   // Stoppt den Button-Homing-Modus
    
    // Row Counter Funktionen
    bool startRowCounter(int targetRows); // Initialisiert den Row Counter mit Ziel-Anzahl
    bool goRowCounter();           // Startet den Row Counter Prozess
    void stopRowCounter();         // Stoppt den Row Counter
    bool isRowCounterRunning();    // Prüft ob Row Counter aktiv ist
    int getCurrentRows();          // Gibt aktuelle Row-Anzahl zurück
    int getTargetRows();           // Gibt Ziel-Row-Anzahl zurück

    
    // Status-Funktionen
    int getCurrentPosition();
    int getTargetPosition();
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

// Web-API Funktionen
void handleAdvancedMotorControl();
void handleAdvancedMotorStatus();
void handleAdvancedMotorStop();
void handleAdvancedMotorHome();
void handleAdvancedMotorJog();
void handleAdvancedMotorCalibrate();
void handleRowCounter(); // Neue Web-API für Row Counter


#endif // ADVANCED_MOTOR_H