/**
 * @file servo.h
 * @brief Header file for controlling a servo motor using ESP32 and FreeRTOS.
 *
 * This file contains the definitions and function prototypes for initializing
 * and controlling a servo motor connected to an ESP32 microcontroller.
 */

#ifndef SERVO_H
#define SERVO_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"

// Definitions for the servo motor
#define SERVO_GPIO_PIN    20        ///< GPIO pin to which the servo is connected
#define SERVO_MIN_PULSE   500       ///< Minimum pulse width in microseconds (0°)
#define SERVO_MAX_PULSE   2500      ///< Maximum pulse width in microseconds (180°)
#define SERVO_NEUTRAL     1500      ///< Neutral position pulse width in microseconds
#define SERVO_MAX_DEGREE  180       ///< Maximum movement in degrees
#define PWM_FREQUENCY     50        ///< PWM frequency in Hz

// LEDC timer and channel definitions
#define LEDC_TIMER        LEDC_TIMER_0       ///< LEDC timer used for PWM
#define LEDC_MODE         LEDC_LOW_SPEED_MODE///< LEDC mode used for PWM
#define LEDC_CHANNEL      LEDC_CHANNEL_0     ///< LEDC channel used for PWM

/**
 * @brief Calculate the duty cycle in microseconds for a given pulse width.
 *
 * This function calculates the duty cycle required to generate a specific pulse width
 * based on the timer resolution.
 *
 * @param pulse_width_us The desired pulse width in microseconds.
 * @param timer_resolution_bits The resolution of the timer in bits.
 * @return The calculated duty cycle in microseconds.
 */
uint32_t calculate_duty_us(uint32_t pulse_width_us, uint32_t timer_resolution_bits);

/**
 * @brief Initialize the servo motor.
 *
 * This function initializes the servo motor by configuring the LEDC timer and channel
 * for PWM generation.
 */
void init_servo();

/**
 * @brief Set the servo motor to a specific angle.
 *
 * This function sets the servo motor to a specified angle by calculating the appropriate
 * pulse width and updating the PWM duty cycle.
 *
 * @param angle The desired angle to set the servo motor to (0° to 180°).
 */
void set_servo_angle(int angle);

#endif // SERVO_H