#include "motor.h"

/**
 * @brief Half-step sequence for stepper motor control.
 *
 * This 8x4 matrix defines the sequence of signals for controlling a stepper motor.
 * Each sub-array represents the state of the four control signals (phases) for each step.
 * Utilizing 8 steps per phase enhances the precision and torque of the motor by enabling
 * half-stepping, resulting in smoother operation and finer positional control.
 */
int motor_sequence[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 0, 1},
    {1, 0, 0, 1}
};

// Variable zum Speichern der aktuellen Position des Motors
int current_motor_position = 0;
int current_step_index = 0;

/**
 * @brief Initializes GPIO pins for motor control.
 */
void setupMotor() {
    pinMode(MOTOR_PIN_1, OUTPUT);
    pinMode(MOTOR_PIN_2, OUTPUT);
    pinMode(MOTOR_PIN_3, OUTPUT);
    pinMode(MOTOR_PIN_4, OUTPUT);
    
    // Alle Pins initial auf LOW setzen
    digitalWrite(MOTOR_PIN_1, LOW);
    digitalWrite(MOTOR_PIN_2, LOW);
    digitalWrite(MOTOR_PIN_3, LOW);
    digitalWrite(MOTOR_PIN_4, LOW);
    
    Serial.println("Stepper Motor initialisiert");
}

/**
 * @brief Sets the motor GPIO pins based on the specified step.
 *
 * @param step The current step in the motor sequence, determining the GPIO levels.
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
 * @brief Moves the stepper motor by a specified number of steps in a given direction.
 *
 * @param steps The number of steps to move the motor.
 * @param direction The direction to move the motor. Positive values indicate forward movement,
 *                  while negative values indicate reverse movement.
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
        
        // Verzögerung für die Motorbewegung
        delay(STEP_DELAY_MS);
    }
}

/**
 * @brief Moves the motor to a specific position.
 * 
 * @param position The target position to move to.
 */
void moveMotorToPosition(int position) {
    int steps_to_move = position - current_motor_position;
    int direction = (steps_to_move > 0) ? 1 : -1;
    
    moveMotor(abs(steps_to_move), direction);
}