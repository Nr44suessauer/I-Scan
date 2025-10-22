#include "advanced_motor.h"

// Globale Instanz
AdvancedStepperMotor advancedMotor(STEP_PIN, DIR_PIN, ENABLE_PIN, ADVANCED_STEPS_PER_REVOLUTION);

// Konstruktor
AdvancedStepperMotor::AdvancedStepperMotor(int stepPin, int dirPin, int enablePin, int stepsPerRevolution)
    : stepPin(stepPin), dirPin(dirPin), enablePin(enablePin), stepsPerRevolution(stepsPerRevolution) {
    currentPosition = 0;
    targetPosition = 0;
    isMoving = false;
    isEnabled = false;
    isHomed = false;
    currentSpeedRPM = DEFAULT_SPEED_RPM;
    stepDelayMicros = 0;
    lastStepTime = 0;
    calculateStepDelay();
}

void AdvancedStepperMotor::begin() {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    if (enablePin >= 0) {
        pinMode(enablePin, OUTPUT);
        digitalWrite(enablePin, HIGH);
    }
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
    enable();
    Serial.println("Erweiterter Motor initialisiert");
}

void AdvancedStepperMotor::enable() {
    if (enablePin >= 0) digitalWrite(enablePin, LOW);
    isEnabled = true;
}

void AdvancedStepperMotor::disable() {
    if (enablePin >= 0) digitalWrite(enablePin, HIGH);
    isEnabled = false;
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::setPinsIdle() {
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
}

void AdvancedStepperMotor::setSpeed(int rpm) {
    rpm = constrain(rpm, 1, MAX_SPEED_RPM);
    currentSpeedRPM = rpm;
    calculateStepDelay();
    Serial.printf("Motor-Geschwindigkeit: %d RPM\n", rpm);
}

void AdvancedStepperMotor::calculateStepDelay() {
    stepDelayMicros = (60000000L) / (currentSpeedRPM * stepsPerRevolution * 2);
}

void AdvancedStepperMotor::setDirection(bool clockwise) {
    digitalWrite(dirPin, clockwise ? HIGH : LOW);
    delayMicroseconds(5);
}

void AdvancedStepperMotor::step() {
    if (!isEnabled) return;
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicros);
}

void AdvancedStepperMotor::moveSteps(int steps) {
    if (!isEnabled || steps == 0) return;
    isMoving = true;
    setDirection(steps > 0);
    int absSteps = abs(steps);
    for (int i = 0; i < absSteps; i++) {
        step();
    }
    currentPosition += steps;
    targetPosition = currentPosition;
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::moveTo(int position) {
    moveSteps(position - currentPosition);
}

void AdvancedStepperMotor::moveRelative(int steps) {
    moveSteps(steps);
}

void AdvancedStepperMotor::stop() {
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::setHome() {
    currentPosition = 0;
    targetPosition = 0;
    isHomed = true;
}

int AdvancedStepperMotor::getCurrentPosition() { return currentPosition; }
int AdvancedStepperMotor::getTargetPosition() { return targetPosition; }
bool AdvancedStepperMotor::getIsMoving() { return isMoving; }
bool AdvancedStepperMotor::getIsEnabled() { return isEnabled; }
int AdvancedStepperMotor::getCurrentSpeed() { return currentSpeedRPM; }
bool AdvancedStepperMotor::getIsHomed() { return isHomed; }

AdvancedMotorStatus AdvancedStepperMotor::getStatus() {
    AdvancedMotorStatus status;
    status.currentPosition = currentPosition;
    status.targetPosition = targetPosition;
    status.isMoving = isMoving;
    status.currentSpeed = currentSpeedRPM;
    status.isHomed = isHomed;
    status.isEnabled = isEnabled;
    return status;
}

void AdvancedStepperMotor::update() {
    if (!isMoving) return;
    
    unsigned long currentTime = micros();
    if (currentTime - lastStepTime >= stepDelayMicros) {
        if (currentPosition != targetPosition) {
            step();
            lastStepTime = currentTime;
        } else {
            isMoving = false;
        }
    }
}

// Globale Setup-Funktion
void setupAdvancedMotor() {
    advancedMotor.begin();
    advancedMotor.setSpeed(60);  // Default speed 60 RPM
    advancedMotor.enable();
}

// Globale Update-Funktion für main loop
void updateMotor() {
    advancedMotor.update();
}
