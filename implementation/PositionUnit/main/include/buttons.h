#ifndef BUTTONS_H
#define BUTTONS_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define BUTTON_PIN 18


/**
 * @brief Initialize the GPIO pins for button input.
 *
 * This function configures the GPIO pins used for button input.
 */
void init_GPIO();

/**
 * @brief Header file for polling defined input pins for their current state.
 *
 * This file contains the declarations and definitions necessary for polling
 * the input pins to determine their current state.
 */
void poll_GIPO();

#endif