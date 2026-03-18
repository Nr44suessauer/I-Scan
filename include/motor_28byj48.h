#ifndef MOTOR_28BYJ48_H
#define MOTOR_28BYJ48_H

#include <Arduino.h>

// Motor-Pin-Definitionen für 28BYJ-48 (Standardwerte)
#define MOTOR_28BYJ48_DEFAULT_PIN_1 6     // GPIO6 = IN1
#define MOTOR_28BYJ48_DEFAULT_PIN_2 4     // GPIO4 = IN2
#define MOTOR_28BYJ48_DEFAULT_PIN_3 7     // GPIO7 = IN3
#define MOTOR_28BYJ48_DEFAULT_PIN_4 5     // GPIO5 = IN4

// Globale Pin-Variablen (können zur Laufzeit geändert werden)
extern int motor_28byj48_pin_1;
extern int motor_28byj48_pin_2;
extern int motor_28byj48_pin_3;
extern int motor_28byj48_pin_4;

// Optimierte Werte für den 28BYJ-48 Motor
#define MOTOR_28BYJ48_STEP_DELAY_MS 1     // Reduziert auf 1ms für höhere Grundgeschwindigkeit
#define MOTOR_28BYJ48_STEPS_PER_REVOLUTION 4096  // Der 28BYJ-48 benötigt 4096 Schritte für eine volle Umdrehung
#define MOTOR_28BYJ48_MAX_SPEED_DELAY 0.5   // Minimale Verzögerung für höchste Geschwindigkeit
#define MOTOR_28BYJ48_MIN_SPEED_DELAY 10    // Reduziert für insgesamt schnellere Bewegung

// Funktionsprototypen
void setup28BYJ48Motor();
void setup28BYJ48MotorWithPins(int pin1, int pin2, int pin3, int pin4); // Setup mit benutzerdefinierten Pins
void set28BYJ48PinConfiguration(int pin1, int pin2, int pin3, int pin4); // Ändert Pin-Konfiguration zur Laufzeit
void get28BYJ48PinConfiguration(int* pin1, int* pin2, int* pin3, int* pin4); // Gibt aktuelle Pin-Konfiguration zurück
void set28BYJ48MotorPins(int step);
void move28BYJ48Motor(int steps, int direction);
void move28BYJ48MotorToPosition(int position);
void move28BYJ48MotorWithSpeed(int steps, int direction, int speed);
void test28BYJ48PinCombination(int pin1, int pin2, int pin3, int pin4, int testSteps, int delayMs); // Testet eine Pin-Kombination
void autoTest28BYJ48PinCombinations(int basePins[], int pinCount, int testSteps, int delayMs, int betweenDelayMs, int timeoutSeconds = 10); // Testet alle Pin-Kombinationen automatisch
// Funktionsprototypen
void setup28BYJ48Motor();
void set28BYJ48MotorPins(int step);
void move28BYJ48Motor(int steps, int direction);
void move28BYJ48MotorToPosition(int position);
void move28BYJ48MotorWithSpeed(int steps, int direction, int speed);

// Erweiterte Motor-Funktionen
void stop28BYJ48Motor();
void home28BYJ48Motor();
int get28BYJ48CurrentMotorPosition();
bool is28BYJ48MotorMoving();
void set28BYJ48MotorSpeed(int speed);
void move28BYJ48MotorDegrees(float degrees, int direction);
void calibrate28BYJ48Motor();

// Geschwindigkeitsprofile
void move28BYJ48MotorWithAcceleration(int steps, int direction, int startSpeed, int endSpeed);
void move28BYJ48MotorSmoothly(int steps, int direction, int speed);

// Motor-Status-Funktionen
typedef struct {
    int currentPosition;
    int targetPosition;
    bool isMoving;
    int currentSpeed;
    bool isHomed;
} Motor28BYJ48Status;

Motor28BYJ48Status get28BYJ48MotorStatus();

#endif // MOTOR_28BYJ48_H
