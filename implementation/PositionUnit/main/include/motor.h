
#ifndef MOTOR_H
#define MOTOR_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// Schrittverzögerung in Millisekunden (anpassen für Leistung und Geschwindigkeit)
#define STEP_DELAY_MS 2

// GPIO-Pins für den 28BYJ-48
#define MOTOR_PIN_1 GPIO_NUM_15
#define MOTOR_PIN_2 GPIO_NUM_23
#define MOTOR_PIN_3 GPIO_NUM_22
#define MOTOR_PIN_4 GPIO_NUM_21


// Methods
void init_motor_pins();
void set_motor_pins(int step);
void move_motor(int steps, int direction);



#endif // MOTOR_H