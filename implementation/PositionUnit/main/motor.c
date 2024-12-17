#include "include/motor.h"

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

/**
 * @brief Initializes GPIO pins for motor control.
 *
 * This function configures the GPIO pins MOTOR_PIN_1, MOTOR_PIN_2, MOTOR_PIN_3, and
 * MOTOR_PIN_4 as output pins. The configuration settings applied are:
 * 
 * - **Mode:** Set to GPIO_MODE_OUTPUT to allow the pins to drive output signals.
 * - **Pull-Up Resistors:** Disabled to prevent unintended high states.
 * - **Pull-Down Resistors:** Disabled to prevent unintended low states.
 * - **Interrupt Type:** Disabled to ensure the pins operate without generating interrupts.
 * 
 * The pin configuration is created using a bitmask that combines the specified motor pins.
 * The `gpio_config` function is then called with this configuration to apply the settings.
 */
void init_motor_pins() {
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << MOTOR_PIN_1) | (1ULL << MOTOR_PIN_2) |
                        (1ULL << MOTOR_PIN_3) | (1ULL << MOTOR_PIN_4),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&io_conf);
}

/**
 * @brief Sets the motor GPIO pins based on the specified step.
 *
 * This function updates the state of four GPIO pins to control a motor's movement
 * by setting each pin to the appropriate level according to the `motor_sequence`.
 * It also provides a debug output indicating the current step and the levels
 * of each motor pin.
 *
 * @param step The current step in the motor sequence, determining the GPIO levels.
 *
 * @note 
 * - `MOTOR_PIN_1` to `MOTOR_PIN_4` must be properly initialized GPIO pins.
 * - The `motor_sequence` array should be defined and contain valid sequences for motor control.
 * - This function assumes that the `step` parameter is within the valid range of the `motor_sequence` array.
 *
 * @example
 * set_motor_pins(2);
 * // This will set MOTOR_PIN_1 to motor_sequence[2][0],
 * // MOTOR_PIN_2 to motor_sequence[2][1],
 * // MOTOR_PIN_3 to motor_sequence[2][2],
 * // MOTOR_PIN_4 to motor_sequence[2][3],
 * // and print the current step and pin states.
 * 
 */

void set_motor_pins(int step) {
    gpio_set_level(MOTOR_PIN_1, motor_sequence[step][0]);
    gpio_set_level(MOTOR_PIN_2, motor_sequence[step][1]);
    gpio_set_level(MOTOR_PIN_3, motor_sequence[step][2]);
    gpio_set_level(MOTOR_PIN_4, motor_sequence[step][3]);

    // Debug-Ausgabe für jeden Schritt
    printf("Step: %d -> Pins: [%d, %d, %d, %d]\n",
           step,
           motor_sequence[step][0],
           motor_sequence[step][1],
           motor_sequence[step][2],
           motor_sequence[step][3]);
}

/**
 * @brief Moves the stepper motor by a specified number of steps in a given direction.
 *
 * This function controls a stepper motor by iterating through the required number of steps.
 * For each step, it calculates the current step index based on the direction:
 * - Forward direction: steps through 0 to 7, repeating as necessary.
 * - Reverse direction: steps through 7 to 0, repeating as necessary.
 * The function sets the motor pins accordingly and implements a delay between steps
 * to control the speed of the motor movement.
 *
 * @param steps The number of steps to move the motor.
 * @param direction The direction to move the motor. Positive values indicate forward movement,
 *                  while negative values indicate reverse movement.
 */
void move_motor(int steps, int direction) {
    for (int i = 0; i < steps; i++) {
        // Calculates the current step (forward or backward)
        int step = (direction > 0) ? i % 8 : (7 - (i % 8));
        set_motor_pins(step);       
        // delay for the motor to move 
        vTaskDelay(STEP_DELAY_MS / portTICK_PERIOD_MS);
    }
}