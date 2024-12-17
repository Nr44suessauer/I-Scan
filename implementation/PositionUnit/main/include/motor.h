/**
 * @file motor.h

 * @brief Header file for motor control in the I-Scan project.
 *
 * Defines GPIO pins for the 28BYJ-48 motor, step delay configuration,
 * and declares functions to initialize motor pins, set motor steps, 
 * and control motor movement.
 * 
 * @brief Motor control interface for the 28BYJ-48 motor.
 *
 * This header defines GPIO pins, delay constants, and function prototypes for
 * initializing and controlling the motor's movement.
 */

#ifndef MOTOR_H
#define MOTOR_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// Step delay in milliseconds (adjust for performance and speed)
#define STEP_DELAY_MS 2

// GPIO pins for the 28BYJ-48
#define MOTOR_PIN_1 GPIO_NUM_15
#define MOTOR_PIN_2 GPIO_NUM_23
#define MOTOR_PIN_3 GPIO_NUM_22
#define MOTOR_PIN_4 GPIO_NUM_21

/**
 * @brief Initializes the motor control pins.
 *
 * Configures the necessary GPIO pins for motor operation.
 */
void init_motor_pins();

/**
 * @brief Sets the motor pins based on the specified step value.
 *
 * @param step The step value to configure the motor pins.
 */
void set_motor_pins(int step);

/**
 * @brief Moves the motor a specified number of steps in the given direction.
 *
 * @param steps The number of steps to move the motor.
 * @param direction The direction to move the motor (e.g., 1 for forward, -1 for reverse).
 */

void move_motor(int steps, int direction);



#endif // MOTOR_H