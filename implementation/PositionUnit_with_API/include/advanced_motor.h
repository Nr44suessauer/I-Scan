#ifndef ADVANCED_MOTOR_H
#define ADVANCED_MOTOR_H

#include <Arduino.h>

// Pin definitions for stepper motor
#define STEP_PIN 37
#define DIR_PIN 36
#define ENABLE_PIN -1  // Optional: Pin zum Aktivieren/Deaktivieren des Motors

// Motor-Konfiguration
#define STEPS_PER_REVOLUTION 200  // Standard for NEMA23 (1.8° per step)
#define MICROSTEPS 10             // Microstepping-Faktor
#define MAX_SPEED_RPM 300        // Maximale Geschwindigkeit in RPM
#define DEFAULT_SPEED_RPM 100     // Standard-Geschwindigkeit in RPM
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
    
    // Row Counter Variables
    bool isRowCounterActive;    // Row Counter active
    int currentRows;            // Current number of rows
    int targetRows;             // Target number of rows
    bool lastButtonState;       // Last button state for edge detection
    enum RowCounterState {
        ROW_COUNTER_IDLE,
        ROW_COUNTER_MOVING      // Continuous movement until button is pressed
    } rowCounterState;
    
    // Motor Relay Control Variables
    bool motorRelayControlEnabled;  // Motor relay control active
    bool relayInverted;            // Relay logic inverted
    
    // Chunked Movement Variables (for interruptible movements)
    bool isChunkedMovementActive;   // Chunked Movement active
    int remainingSteps;             // Remaining steps
    bool movementDirection;         // Movement direction (true = forward)
    int chunkSize;                  // Size of individual chunks
    unsigned long lastChunkTime;    // Time of last chunk
    unsigned long chunkDelayMs;     // Pause between chunks for other commands
    
    // Global Realtime Update System
    unsigned long lastRealtimeUpdateTime;  // Last realtime update time
    unsigned long realtimeUpdateInterval;  // Interval for realtime updates (ms)

    
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
    void setPinsIdle();  // New function: Set pins to idle state
    
    // Basic Movement Functions
    void setSpeed(int rpm);
    void setDirection(bool clockwise);
    void step();
    void moveSteps(int steps);              // Standard (blocking for small movements)
    void moveTo(int position);              // Standard
    void moveRelative(int steps);           // Standard
    void moveDegrees(float degrees);
    void moveRevolutions(float revolutions);
    
    // Chunked Movement Functions (interruptible large movements)
    void moveStepsChunked(int steps, int chunkSize = 50, int delayMs = 10);
    void moveToChunked(int position, int chunkSize = 50, int delayMs = 10);
    void moveRelativeChunked(int steps, int chunkSize = 50, int delayMs = 10);
    bool isChunkedMovementRunning();
    void stopChunkedMovement();
    void setChunkParameters(int chunkSize, int delayMs);
    
    // Advanced Movement Functions
    void moveWithAcceleration(int steps, int startRPM, int endRPM);
    void moveSmoothly(int steps, int targetRPM);
    void jogContinuous(bool direction, int rpm);
    
    // Control Functions
    void stop();
    void emergencyStop();
    void home();
    void setHome();
    void calibrate();
    void setUsePhysicalHome(bool usePhysical);  // Sets the homing mode
    bool getUsePhysicalHome();     // Returns the current homing mode
    void startButtonHomingMode();  // New function: Moves until button is pressed
    void stopButtonHomingMode();   // Stops the button homing mode
    
    // Row Counter Functions
    bool startRowCounter(int targetRows); // Initializes the row counter with target count
    bool goRowCounter();           // Starts the row counter process
    void stopRowCounter();         // Stops the row counter
    bool isRowCounterRunning();    // Checks if row counter is active
    int getCurrentRows();          // Returns current row count
    int getTargetRows();           // Returns target row count
    
    // Motor Relay Control Functions
    void setMotorRelayControl(bool enabled);  // Enables/disables motor relay control
    void setRelayInvert(bool inverted);       // Inverts relay logic
    bool getMotorRelayControl();              // Returns motor relay status
    bool getRelayInvert();                    // Returns relay invert status
    
    // Realtime Update System
    void setRealtimeUpdateInterval(unsigned long intervalMs);  // Sets update interval
    void forceRealtimeUpdate();               // Forces immediate update of all components
    
    // Status Functions
    int getCurrentPosition();
    int getTargetPosition();
    bool getIsMoving();
    bool getIsEnabled();
    bool getIsHomed();

    int getCurrentSpeed();
    AdvancedMotorStatus getStatus();
    
    // Configuration
    void setStepsPerRevolution(int steps);
    void setMicrostepping(int factor);
    
    // Non-blocking Movement (for continuous movements)
    void update();  // Must be called regularly in loop()
    void startNonBlockingMoveTo(int position);
    void startNonBlockingMoveSteps(int steps);
    
private:
    void updateRealtimeComponents();          // Internal function for realtime updates
};

// Global Instance
extern AdvancedStepperMotor advancedMotor;

// Helper Functions
void setupAdvancedMotor();
void updateMotor();

// Web-API Functions
void handleAdvancedMotorControl();
void handleAdvancedMotorStatus();
void handleAdvancedMotorStop();
void handleAdvancedMotorHome();
void handleAdvancedMotorJog();
void handleAdvancedMotorCalibrate();
void handleRowCounter(); // New Web-API for Row Counter


#endif // ADVANCED_MOTOR_H