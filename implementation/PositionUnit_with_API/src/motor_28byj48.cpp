#include "motor_28byj48.h"

// Globale Pin-Variablen (können zur Laufzeit geändert werden)
int motor_28byj48_pin_1 = MOTOR_28BYJ48_DEFAULT_PIN_1;
int motor_28byj48_pin_2 = MOTOR_28BYJ48_DEFAULT_PIN_2;
int motor_28byj48_pin_3 = MOTOR_28BYJ48_DEFAULT_PIN_3;
int motor_28byj48_pin_4 = MOTOR_28BYJ48_DEFAULT_PIN_4;

/**
 * @brief Half-step sequence for 28BYJ-48 stepper motor control.
 */
int motor_28byj48_sequence[8][4] = {
    {1, 0, 0, 0},  // Schritt 1
    {1, 1, 0, 0},  // Schritt 2
    {0, 1, 0, 0},  // Schritt 3
    {0, 1, 1, 0},  // Schritt 4
    {0, 0, 1, 0},  // Schritt 5
    {0, 0, 1, 1},  // Schritt 6
    {0, 0, 0, 1},  // Schritt 7
    {1, 0, 0, 1}   // Schritt 8
};

// Variable zum Speichern der aktuellen Position des Motors
int current_28byj48_motor_position = 0;
int current_28byj48_step_index = 0;
bool motor_28byj48_is_moving = false;
int current_28byj48_motor_speed = 50;
bool motor_28byj48_is_homed = false;
int target_28byj48_motor_position = 0;

// Variablen für Auto-Test-Feedback
bool waiting_for_pin_test_feedback = false;
bool pin_test_confirmed = false;
int test_pin_combination[4] = {0, 0, 0, 0};
unsigned long test_feedback_timeout = 0;

void setup28BYJ48Motor() {
    pinMode(motor_28byj48_pin_1, OUTPUT);
    pinMode(motor_28byj48_pin_2, OUTPUT);
    pinMode(motor_28byj48_pin_3, OUTPUT);
    pinMode(motor_28byj48_pin_4, OUTPUT);
    
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
    
    Serial.printf("28BYJ-48 Stepper Motor initialisiert - Pins: %d, %d, %d, %d\n", 
                  motor_28byj48_pin_1, motor_28byj48_pin_2, motor_28byj48_pin_3, motor_28byj48_pin_4);
}

void setup28BYJ48MotorWithPins(int pin1, int pin2, int pin3, int pin4) {
    motor_28byj48_pin_1 = pin1;
    motor_28byj48_pin_2 = pin2;
    motor_28byj48_pin_3 = pin3;
    motor_28byj48_pin_4 = pin4;
    
    setup28BYJ48Motor();
}

void set28BYJ48PinConfiguration(int pin1, int pin2, int pin3, int pin4) {
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
    
    motor_28byj48_pin_1 = pin1;
    motor_28byj48_pin_2 = pin2;
    motor_28byj48_pin_3 = pin3;
    motor_28byj48_pin_4 = pin4;
    
    pinMode(motor_28byj48_pin_1, OUTPUT);
    pinMode(motor_28byj48_pin_2, OUTPUT);
    pinMode(motor_28byj48_pin_3, OUTPUT);
    pinMode(motor_28byj48_pin_4, OUTPUT);
    
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
    
    Serial.printf("28BYJ-48 Pin-Konfiguration geändert - Neue Pins: %d, %d, %d, %d\n", 
                  pin1, pin2, pin3, pin4);
}

void get28BYJ48PinConfiguration(int* pin1, int* pin2, int* pin3, int* pin4) {
    *pin1 = motor_28byj48_pin_1;
    *pin2 = motor_28byj48_pin_2;
    *pin3 = motor_28byj48_pin_3;
    *pin4 = motor_28byj48_pin_4;
}

void set28BYJ48MotorPins(int step) {
    digitalWrite(motor_28byj48_pin_1, motor_28byj48_sequence[step][0]);
    digitalWrite(motor_28byj48_pin_2, motor_28byj48_sequence[step][1]);
    digitalWrite(motor_28byj48_pin_3, motor_28byj48_sequence[step][2]);
    digitalWrite(motor_28byj48_pin_4, motor_28byj48_sequence[step][3]);
    current_28byj48_step_index = step;
}

void move28BYJ48Motor(int steps, int direction) {
    for (int i = 0; i < steps; i++) {
        int step_index;
        
        if (direction > 0) {
            step_index = (current_28byj48_step_index + 1) % 8;
        } else {
            step_index = (current_28byj48_step_index - 1 + 8) % 8;
        }
        
        set28BYJ48MotorPins(step_index);
        current_28byj48_motor_position += direction;
        delay(MOTOR_28BYJ48_STEP_DELAY_MS);
    }
    
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
}

void move28BYJ48MotorWithSpeed(int steps, int direction, int speed) {
    speed = constrain(speed, 0, 90);
    int delayMs;
    
    if (speed < 30) {
        delayMs = map(speed, 0, 29, 50, 20);
        
        for (int i = 0; i < steps; i++) {
            if (direction > 0) {
                current_28byj48_step_index = (current_28byj48_step_index + 1) % 8;
            } else {
                current_28byj48_step_index = (current_28byj48_step_index - 1 + 8) % 8;
            }
            
            digitalWrite(motor_28byj48_pin_1, motor_28byj48_sequence[current_28byj48_step_index][0]);
            digitalWrite(motor_28byj48_pin_2, motor_28byj48_sequence[current_28byj48_step_index][1]);
            digitalWrite(motor_28byj48_pin_3, motor_28byj48_sequence[current_28byj48_step_index][2]);
            digitalWrite(motor_28byj48_pin_4, motor_28byj48_sequence[current_28byj48_step_index][3]);
            
            current_28byj48_motor_position += direction;
            delay(delayMs);
        }
    } 
    else if (speed < 70) {
        delayMs = map(speed, 30, 69, 20, 3);
        
        for (int i = 0; i < steps; i++) {
            if (direction > 0) {
                current_28byj48_step_index = (current_28byj48_step_index + 1) % 8;
            } else {
                current_28byj48_step_index = (current_28byj48_step_index - 1 + 8) % 8;
            }
            
            digitalWrite(motor_28byj48_pin_1, motor_28byj48_sequence[current_28byj48_step_index][0]);
            digitalWrite(motor_28byj48_pin_2, motor_28byj48_sequence[current_28byj48_step_index][1]);
            digitalWrite(motor_28byj48_pin_3, motor_28byj48_sequence[current_28byj48_step_index][2]);
            digitalWrite(motor_28byj48_pin_4, motor_28byj48_sequence[current_28byj48_step_index][3]);
            
            current_28byj48_motor_position += direction;
            delay(delayMs);
        }
    }
    else {
        int delayMicros = map(speed, 70, 90, 3000, 500);
        
        for (int i = 0; i < steps; i++) {
            if (direction > 0) {
                current_28byj48_step_index = (current_28byj48_step_index + 1) % 8;
            } else {
                current_28byj48_step_index = (current_28byj48_step_index - 1 + 8) % 8;
            }
            
            digitalWrite(motor_28byj48_pin_1, motor_28byj48_sequence[current_28byj48_step_index][0]);
            digitalWrite(motor_28byj48_pin_2, motor_28byj48_sequence[current_28byj48_step_index][1]);
            digitalWrite(motor_28byj48_pin_3, motor_28byj48_sequence[current_28byj48_step_index][2]);
            digitalWrite(motor_28byj48_pin_4, motor_28byj48_sequence[current_28byj48_step_index][3]);
            
            current_28byj48_motor_position += direction;
            delayMicroseconds(delayMicros);
        }
    }
    
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
}

void move28BYJ48MotorToPosition(int position) {
    target_28byj48_motor_position = position;
    int steps_to_move = position - current_28byj48_motor_position;
    int direction = (steps_to_move > 0) ? 1 : -1;
    
    motor_28byj48_is_moving = true;
    move28BYJ48Motor(abs(steps_to_move), direction);
    motor_28byj48_is_moving = false;
}

void stop28BYJ48Motor() {
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
    
    motor_28byj48_is_moving = false;
    target_28byj48_motor_position = current_28byj48_motor_position;
    
    Serial.println("28BYJ-48 Motor gestoppt");
}

void test28BYJ48PinCombination(int pin1, int pin2, int pin3, int pin4, int testSteps, int delayMs) {
    Serial.printf("\n=== Test Pin-Kombination: %d, %d, %d, %d ===\n", pin1, pin2, pin3, pin4);
    
    digitalWrite(motor_28byj48_pin_1, LOW);
    digitalWrite(motor_28byj48_pin_2, LOW);
    digitalWrite(motor_28byj48_pin_3, LOW);
    digitalWrite(motor_28byj48_pin_4, LOW);
    
    pinMode(pin1, OUTPUT);
    pinMode(pin2, OUTPUT);
    pinMode(pin3, OUTPUT);
    pinMode(pin4, OUTPUT);
    
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, LOW);
    
    int test_step_index = 0;
    
    Serial.printf("Starte Test mit %d Schritten, %d ms Verzögerung\n", testSteps, delayMs);
    
    for (int i = 0; i < testSteps; i++) {
        test_step_index = (test_step_index + 1) % 8;
        
        digitalWrite(pin1, motor_28byj48_sequence[test_step_index][0]);
        digitalWrite(pin2, motor_28byj48_sequence[test_step_index][1]);
        digitalWrite(pin3, motor_28byj48_sequence[test_step_index][2]);
        digitalWrite(pin4, motor_28byj48_sequence[test_step_index][3]);
        
        delay(delayMs);
    }
    
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, LOW);
    
    Serial.println("Test abgeschlossen\n");
}

void autoTest28BYJ48PinCombinations(int basePins[], int pinCount, int testSteps, int delayMs, int betweenDelayMs, int timeoutSeconds) {
    Serial.println("\n========================================");
    Serial.println("=== AUTO-TEST: Alle Pin-Kombinationen ===");
    Serial.println("========================================\n");
    Serial.printf("Anzahl Pins: %d\n", pinCount);
    Serial.printf("Test-Schritte: %d\n", testSteps);
    Serial.printf("Step Delay: %d ms\n", delayMs);
    Serial.printf("Pause zwischen Tests: %d ms\n", betweenDelayMs);
    Serial.printf("Timeout pro Test: %d Sekunden\n\n", timeoutSeconds);
    
    // Alle möglichen Permutationen der 4 Pins aus der Liste testen
    for (int i1 = 0; i1 < pinCount; i1++) {
        for (int i2 = 0; i2 < pinCount; i2++) {
            if (i2 == i1) continue; // Gleicher Pin nicht zweimal verwenden
            
            for (int i3 = 0; i3 < pinCount; i3++) {
                if (i3 == i1 || i3 == i2) continue;
                
                for (int i4 = 0; i4 < pinCount; i4++) {
                    if (i4 == i1 || i4 == i2 || i4 == i3) continue;
                    
                    int pin1 = basePins[i1];
                    int pin2 = basePins[i2];
                    int pin3 = basePins[i3];
                    int pin4 = basePins[i4];
                    
                    Serial.println("\n----------------------------------------");
                    Serial.printf(">>> TESTE KOMBINATION: %d, %d, %d, %d <<<\n", pin1, pin2, pin3, pin4);
                    Serial.println("----------------------------------------");
                    
                    // Test durchführen
                    test28BYJ48PinCombination(pin1, pin2, pin3, pin4, testSteps, delayMs);
                    
                    // Warte auf Benutzer-Feedback über Webserver
                    Serial.println("\n>>> WARTE AUF BESTÄTIGUNG <<<");
                    Serial.println("Webserver: Hat sich der Motor korrekt bewegt?");
                    Serial.println("- JA: Diese Pins werden gespeichert");
                    Serial.println("- NEIN: Nächste Kombination wird getestet");
                    Serial.printf("Timeout: %d Sekunden\n\n", timeoutSeconds);
                    
                    // Markiere, dass auf Feedback gewartet wird
                    extern bool waiting_for_pin_test_feedback;
                    extern int test_pin_combination[4];
                    extern unsigned long test_feedback_timeout;
                    
                    waiting_for_pin_test_feedback = true;
                    test_pin_combination[0] = pin1;
                    test_pin_combination[1] = pin2;
                    test_pin_combination[2] = pin3;
                    test_pin_combination[3] = pin4;
                    test_feedback_timeout = millis() + (timeoutSeconds * 1000); // Konfigurierbares Timeout
                    
                    // Warte auf Feedback oder Timeout
                    while (waiting_for_pin_test_feedback && millis() < test_feedback_timeout) {
                        delay(100);
                    }
                    
                    // Prüfe ob bestätigt wurde
                    extern bool pin_test_confirmed;
                    if (pin_test_confirmed) {
                        Serial.println("\n✓ KOMBINATION BESTÄTIGT!");
                        Serial.printf("✓ Korrekte Pins: %d, %d, %d, %d\n", pin1, pin2, pin3, pin4);
                        Serial.println("✓ Pin-Konfiguration wird übernommen\n");
                        
                        set28BYJ48PinConfiguration(pin1, pin2, pin3, pin4);
                        
                        Serial.println("========================================");
                        Serial.println("=== AUTO-TEST ABGESCHLOSSEN (ERFOLG) ===");
                        Serial.println("========================================\n");
                        return; // Erfolg - Test beenden
                    }
                    
                    if (!waiting_for_pin_test_feedback) {
                        Serial.println("✗ Kombination abgelehnt - nächste Kombination wird getestet\n");
                    } else {
                        Serial.println("⏱ Timeout - nächste Kombination wird getestet\n");
                    }
                    
                    delay(betweenDelayMs); // Pause zwischen Tests
                }
            }
        }
    }
    
    Serial.println("\n========================================");
    Serial.println("=== AUTO-TEST ABGESCHLOSSEN ===");
    Serial.println("!!! KEINE KORREKTE KOMBINATION GEFUNDEN !!!");
    Serial.println("========================================\n");
}

void home28BYJ48Motor() {
    Serial.println("28BYJ-48 Motor wird zur Home-Position bewegt...");
    move28BYJ48MotorToPosition(0);
    current_28byj48_motor_position = 0;
    target_28byj48_motor_position = 0;
    motor_28byj48_is_homed = true;
    Serial.println("28BYJ-48 Motor ist in Home-Position");
}

int get28BYJ48CurrentMotorPosition() {
    return current_28byj48_motor_position;
}

bool is28BYJ48MotorMoving() {
    return motor_28byj48_is_moving;
}

void set28BYJ48MotorSpeed(int speed) {
    current_28byj48_motor_speed = constrain(speed, 0, 100);
    Serial.printf("28BYJ-48 Motor-Geschwindigkeit auf %d%% gesetzt\n", current_28byj48_motor_speed);
}

void move28BYJ48MotorDegrees(float degrees, int direction) {
    int steps = (int)((degrees / 360.0) * MOTOR_28BYJ48_STEPS_PER_REVOLUTION);
    
    Serial.printf("Bewege 28BYJ-48 Motor um %.1f Grad (%d Schritte)\n", degrees, steps);
    
    motor_28byj48_is_moving = true;
    move28BYJ48MotorWithSpeed(steps, direction, current_28byj48_motor_speed);
    motor_28byj48_is_moving = false;
}

void calibrate28BYJ48Motor() {
    Serial.println("28BYJ-48 Motor wird kalibriert...");
    current_28byj48_motor_position = 0;
    target_28byj48_motor_position = 0;
    current_28byj48_step_index = 0;
    motor_28byj48_is_homed = true;
    Serial.println("28BYJ-48 Motor kalibriert - aktuelle Position ist jetzt 0");
}

void move28BYJ48MotorWithAcceleration(int steps, int direction, int startSpeed, int endSpeed) {
    motor_28byj48_is_moving = true;
    
    startSpeed = constrain(startSpeed, 1, 100);
    endSpeed = constrain(endSpeed, 1, 100);
    
    Serial.printf("28BYJ-48 Motor bewegt %d Schritte mit Beschleunigung von %d%% auf %d%%\n", 
                  steps, startSpeed, endSpeed);
    
    for (int i = 0; i < steps; i++) {
        int currentSpeed = startSpeed + ((endSpeed - startSpeed) * i) / steps;
        
        if (direction > 0) {
            current_28byj48_step_index = (current_28byj48_step_index + 1) % 8;
        } else {
            current_28byj48_step_index = (current_28byj48_step_index - 1 + 8) % 8;
        }
        
        set28BYJ48MotorPins(current_28byj48_step_index);
        current_28byj48_motor_position += direction;
        
        int delayMs = map(currentSpeed, 1, 100, 20, 1);
        delay(delayMs);
    }
    
    stop28BYJ48Motor();
}

void move28BYJ48MotorSmoothly(int steps, int direction, int speed) {
    motor_28byj48_is_moving = true;
    
    speed = constrain(speed, 1, 100);
    int accelSteps = steps / 4;
    
    Serial.printf("28BYJ-48 Motor bewegt %d Schritte sanft mit Zielgeschwindigkeit %d%%\n", steps, speed);
    
    for (int i = 0; i < steps; i++) {
        int currentSpeed;
        
        if (i < accelSteps) {
            currentSpeed = map(i, 0, accelSteps, 10, speed);
        } else if (i >= steps - accelSteps) {
            currentSpeed = map(i, steps - accelSteps, steps, speed, 10);
        } else {
            currentSpeed = speed;
        }
        
        if (direction > 0) {
            current_28byj48_step_index = (current_28byj48_step_index + 1) % 8;
        } else {
            current_28byj48_step_index = (current_28byj48_step_index - 1 + 8) % 8;
        }
        
        set28BYJ48MotorPins(current_28byj48_step_index);
        current_28byj48_motor_position += direction;
        
        int delayMs = map(currentSpeed, 1, 100, 20, 1);
        delay(delayMs);
    }
    
    stop28BYJ48Motor();
}

Motor28BYJ48Status get28BYJ48MotorStatus() {
    Motor28BYJ48Status status;
    status.currentPosition = current_28byj48_motor_position;
    status.targetPosition = target_28byj48_motor_position;
    status.isMoving = motor_28byj48_is_moving;
    status.currentSpeed = current_28byj48_motor_speed;
    status.isHomed = motor_28byj48_is_homed;
    
    return status;
}
