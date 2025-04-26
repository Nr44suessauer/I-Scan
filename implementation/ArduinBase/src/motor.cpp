#include "motor.h"

/**
 * @brief Half-step sequence for 28BYJ-48 stepper motor control.
 *
 * Der 28BYJ-48 arbeitet am besten mit der folgenden Halbschritt-Sequenz.
 * Die Sequenz verwendet 8 Schritte für eine volle Erregungssequenz und ermöglicht
 * präzisere Bewegungen aufgrund der kleineren Schrittwinkel.
 */
int motor_sequence[8][4] = {
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
int current_motor_position = 0;
int current_step_index = 0;

/**
 * @brief Initialisiert die GPIO-Pins für die Motorsteuerung.
 */
void setupMotor() {
    pinMode(MOTOR_PIN_1, OUTPUT);
    pinMode(MOTOR_PIN_2, OUTPUT);
    pinMode(MOTOR_PIN_3, OUTPUT);
    pinMode(MOTOR_PIN_4, OUTPUT);
    
    // Alle Pins initial auf LOW setzen - Motor im Ruhezustand
    digitalWrite(MOTOR_PIN_1, LOW);
    digitalWrite(MOTOR_PIN_2, LOW);
    digitalWrite(MOTOR_PIN_3, LOW);
    digitalWrite(MOTOR_PIN_4, LOW);
    
    Serial.println("28BYJ-48 Stepper Motor initialisiert");
}

/**
 * @brief Setzt die Motor-Pins basierend auf dem angegebenen Schritt.
 *
 * @param step Der aktuelle Schritt in der Motorsequenz
 */
void setMotorPins(int step) {
    digitalWrite(MOTOR_PIN_1, motor_sequence[step][0]);
    digitalWrite(MOTOR_PIN_2, motor_sequence[step][1]);
    digitalWrite(MOTOR_PIN_3, motor_sequence[step][2]);
    digitalWrite(MOTOR_PIN_4, motor_sequence[step][3]);

    // Aktuelle Schrittposition merken
    current_step_index = step;

    // Debug-Ausgabe für jeden Schritt
    Serial.printf("Step: %d -> Pins: [%d, %d, %d, %d]\n",
           step,
           motor_sequence[step][0],
           motor_sequence[step][1],
           motor_sequence[step][2],
           motor_sequence[step][3]);
}

/**
 * @brief Bewegt den Schrittmotor um die angegebene Anzahl von Schritten in die angegebene Richtung.
 *
 * @param steps Die Anzahl der zu bewegenden Schritte.
 * @param direction Die Bewegungsrichtung. Positive Werte bedeuten Vorwärtsbewegung,
 *                  negative Werte bedeuten Rückwärtsbewegung.
 */
void moveMotor(int steps, int direction) {
    for (int i = 0; i < steps; i++) {
        // Aktuellen Schritt berechnen (vorwärts oder rückwärts)
        int step_index;
        
        if (direction > 0) {
            step_index = (current_step_index + 1) % 8;
        } else {
            step_index = (current_step_index - 1 + 8) % 8;
        }
        
        setMotorPins(step_index);
        
        // Position aktualisieren
        current_motor_position += direction;
        
        // Verzögerung für die Motorbewegung - optimiert für den 28BYJ-48
        delay(STEP_DELAY_MS);
    }
    
    // Nach der Bewegung alle Pins auf LOW setzen, um Stromverbrauch zu reduzieren und Überhitzung zu vermeiden
    // Der 28BYJ-48 behält seine Position auch ohne aktive Spulen
    digitalWrite(MOTOR_PIN_1, LOW);
    digitalWrite(MOTOR_PIN_2, LOW);
    digitalWrite(MOTOR_PIN_3, LOW);
    digitalWrite(MOTOR_PIN_4, LOW);
}

/**
 * @brief Bewegt den Motor mit variabler Geschwindigkeit.
 *
 * @param steps Die Anzahl der zu bewegenden Schritte.
 * @param direction Die Bewegungsrichtung (1 für vorwärts, -1 für rückwärts).
 * @param speed Die Geschwindigkeit (0-100, wobei 90 als Maximum verwendet wird).
 */
void moveMotorWithSpeed(int steps, int direction, int speed) {
    // Geschwindigkeit auf 0-90 Skala begrenzen (90% ist das Maximum)
    speed = constrain(speed, 0, 90);
    
    // Auf den Wertebereich für die Verzögerungszeit umrechnen
    // Bei 0% -> 50ms Verzögerung (sehr langsam)
    // Bei 90% -> 0.5ms Verzögerung (maximale Geschwindigkeit)
    int delayMs;
    
    // Geschwindigkeitsbereich in drei Segmente unterteilen für bessere Kontrolle
    if (speed < 30) {
        // Niedrige Geschwindigkeiten: 50ms bis 20ms
        delayMs = map(speed, 0, 29, 50, 20);
        
        for (int i = 0; i < steps; i++) {
            // Aktuellen Schritt berechnen
            if (direction > 0) {
                current_step_index = (current_step_index + 1) % 8;
            } else {
                current_step_index = (current_step_index - 1 + 8) % 8;
            }
            
            // Motor-Pins setzen
            digitalWrite(MOTOR_PIN_1, motor_sequence[current_step_index][0]);
            digitalWrite(MOTOR_PIN_2, motor_sequence[current_step_index][1]);
            digitalWrite(MOTOR_PIN_3, motor_sequence[current_step_index][2]);
            digitalWrite(MOTOR_PIN_4, motor_sequence[current_step_index][3]);
            
            current_motor_position += direction;
            
            // Lange Verzögerungen für niedrige Geschwindigkeiten
            delay(delayMs);
        }
    } 
    else if (speed < 70) {
        // Mittlere Geschwindigkeiten: 20ms bis 3ms
        delayMs = map(speed, 30, 69, 20, 3);
        
        for (int i = 0; i < steps; i++) {
            // Aktuellen Schritt berechnen
            if (direction > 0) {
                current_step_index = (current_step_index + 1) % 8;
            } else {
                current_step_index = (current_step_index - 1 + 8) % 8;
            }
            
            // Motor-Pins setzen
            digitalWrite(MOTOR_PIN_1, motor_sequence[current_step_index][0]);
            digitalWrite(MOTOR_PIN_2, motor_sequence[current_step_index][1]);
            digitalWrite(MOTOR_PIN_3, motor_sequence[current_step_index][2]);
            digitalWrite(MOTOR_PIN_4, motor_sequence[current_step_index][3]);
            
            current_motor_position += direction;
            
            // Mittlere Verzögerungen
            delay(delayMs);
        }
    }
    else {
        // Hohe Geschwindigkeiten: 3ms bis 500µs
        // Konvertiere von ms zu µs für hohe Genauigkeit bei hohen Geschwindigkeiten
        int delayMicros = map(speed, 70, 90, 3000, 500);
        
        for (int i = 0; i < steps; i++) {
            // Aktuellen Schritt berechnen
            if (direction > 0) {
                current_step_index = (current_step_index + 1) % 8;
            } else {
                current_step_index = (current_step_index - 1 + 8) % 8;
            }
            
            // Motor-Pins setzen
            digitalWrite(MOTOR_PIN_1, motor_sequence[current_step_index][0]);
            digitalWrite(MOTOR_PIN_2, motor_sequence[current_step_index][1]);
            digitalWrite(MOTOR_PIN_3, motor_sequence[current_step_index][2]);
            digitalWrite(MOTOR_PIN_4, motor_sequence[current_step_index][3]);
            
            current_motor_position += direction;
            
            // Mikrosekunden-Verzögerung für höchste Geschwindigkeiten
            delayMicroseconds(delayMicros);
        }
    }
    
    // Nach der Bewegung alle Pins auf LOW setzen
    digitalWrite(MOTOR_PIN_1, LOW);
    digitalWrite(MOTOR_PIN_2, LOW);
    digitalWrite(MOTOR_PIN_3, LOW);
    digitalWrite(MOTOR_PIN_4, LOW);
}

/**
 * @brief Bewegt den Motor zu einer bestimmten Position.
 * 
 * @param position Die Zielposition, zu der der Motor bewegt werden soll.
 */
void moveMotorToPosition(int position) {
    int steps_to_move = position - current_motor_position;
    int direction = (steps_to_move > 0) ? 1 : -1;
    
    moveMotor(abs(steps_to_move), direction);
}