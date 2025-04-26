#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

// Motor-Pin-Definitionen
#define MOTOR_PIN_1 19    // IN1
#define MOTOR_PIN_2 20    // IN2
#define MOTOR_PIN_3 21    // IN3
#define MOTOR_PIN_4 47    // IN4
#define STEP_DELAY_MS 2   // Zeit zwischen Schritten (2ms für eine angemessene Geschwindigkeit)

// Funktionsprototypen
void setupMotor();
void setMotorPins(int step);
void moveMotor(int steps, int direction);
void moveMotorToPosition(int position);

#endif // MOTOR_H