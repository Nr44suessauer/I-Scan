#ifndef SERVO_H
#define SERVO_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"

// Definitionen für den Servo
#define SERVO_GPIO_PIN    20        // GPIO-Pin, an den der Servo angeschlossen ist
#define SERVO_MIN_PULSE   500     // Minimale Pulsbreite in Mikrosekunden (0°)
#define SERVO_MAX_PULSE   2500     // Maximale Pulsbreite in Mikrosekunden (180°)
#define SERVO_NEUTRAL     1500     // Neutralposition des Servos
#define SERVO_MAX_DEGREE  180      // Maximale Bewegung in Grad
#define PWM_FREQUENCY     50       // PWM-Frequenz in Hz

// LEDC-Timer- und Kanaldefinitionen
#define LEDC_TIMER        LEDC_TIMER_0
#define LEDC_MODE         LEDC_LOW_SPEED_MODE
#define LEDC_CHANNEL      LEDC_CHANNEL_0

// Methods
uint32_t calculate_duty_us(uint32_t pulse_width_us, uint32_t timer_resolution_bits);
void init_servo();
void set_servo_angle(int angle);


#endif // SERVO_H