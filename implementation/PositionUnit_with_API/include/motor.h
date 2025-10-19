#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

// Motor-Pin-Definitionen
#define MOTOR_PIN_1 19    // IN1
#define MOTOR_PIN_2 20    // IN2
#define MOTOR_PIN_3 21    // IN3
#define MOTOR_PIN_4 47    // IN4

// Button-Pin-Definition
#define BUTTON_PIN 45     // Button Input Pin

// Optimized values for the 28BYJ-48 motor - faster speed
#define STEP_DELAY_MS 1     // Reduced to 1ms for higher base speed
#define STEPS_PER_REVOLUTION 4096  // The 28BYJ-48 requires 4096 steps for a full revolution
#define MAX_SPEED_DELAY 0.5   // Minimum delay for highest speed
#define MIN_SPEED_DELAY 10    // Reduced for overall faster movement

// Funktionsprototypen
void setupMotor();
void setMotorPins(int step);
void moveMotor(int steps, int direction);
void moveMotorToPosition(int position);
void moveMotorWithSpeed(int steps, int direction, int speed);

// Erweiterte Motor-Funktionen
void stopMotor();
void homeMotor();
int getCurrentMotorPosition();
bool isMotorMoving();
void setMotorSpeed(int speed);
void moveMotorDegrees(float degrees, int direction);
void calibrateMotor();

// Geschwindigkeitsprofile
void moveMotorWithAcceleration(int steps, int direction, int startSpeed, int endSpeed);
void moveMotorSmoothly(int steps, int direction, int speed);

// Motor-Status-Funktionen
typedef struct {
    int currentPosition;
    int targetPosition;
    bool isMoving;
    int currentSpeed;
    bool isHomed;
} MotorStatus;

MotorStatus getMotorStatus();

// Button Funktionsprototypen
void setupButton();
bool getButtonState();

#endif // MOTOR_H