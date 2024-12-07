#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"

// Definitionen für den Servo
#define SERVO_GPIO_PIN    0        // GPIO-Pin, an den der Servo angeschlossen ist
#define SERVO_MIN_PULSE   1000      // Minimale Pulsbreite in Mikrosekunden (0°)
#define SERVO_MAX_PULSE   2000      // Maximale Pulsbreite in Mikrosekunden (180°)
#define SERVO_NEUTRAL     1500      // Neutralposition des Servos
#define SERVO_MAX_DEGREE  180       // Maximale Bewegung in Grad
#define PWM_FREQUENCY     50        // PWM-Frequenz in Hz

// LEDC-Timer- und Kanaldefinitionen
#define LEDC_TIMER        LEDC_TIMER_0
#define LEDC_MODE         LEDC_LOW_SPEED_MODE
#define LEDC_CHANNEL      LEDC_CHANNEL_0

// Berechnung der Duty-Cycle für eine gegebene Pulsbreite
uint32_t calculate_duty_us(uint32_t pulse_width_us, uint32_t timer_resolution_bits) {
    // Umwandlung von Mikrosekunden in Duty-Cycle-Bits
    uint32_t duty = (1 << timer_resolution_bits) * pulse_width_us / 20000; // 20000 µs = 20 ms (50 Hz)
    return duty;
}

// Initialisierung des Servo-Controllers
void init_servo() {
    // Timer-Konfiguration
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .timer_num        = LEDC_TIMER,
        .duty_resolution  = LEDC_TIMER_15_BIT, // 15-Bit-Auflösung
        .freq_hz          = PWM_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);

    // Kanal-Konfiguration
    ledc_channel_config_t ledc_channel = {
        .gpio_num       = SERVO_GPIO_PIN,
        .speed_mode     = LEDC_MODE,
        .channel        = LEDC_CHANNEL,
        .timer_sel      = LEDC_TIMER,
        .duty           = calculate_duty_us(SERVO_NEUTRAL, 15), // Neutralposition
        .hpoint         = 0,
        .intr_type      = LEDC_INTR_DISABLE
    };
    ledc_channel_config(&ledc_channel);
}

// Setzt den Servo auf einen Winkel
void set_servo_angle(int angle) {
    if (angle < 0) angle = 0;
    if (angle > SERVO_MAX_DEGREE) angle = SERVO_MAX_DEGREE;

    // Berechnung der Pulsbreite
    uint32_t pulse_width = SERVO_MIN_PULSE +
                           (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle / SERVO_MAX_DEGREE;

    // Berechnung des Duty-Cycles
    uint32_t duty = calculate_duty_us(pulse_width, 15);

    // Setzen des Duty-Cycles
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
}

void app_main() {
    // Initialisiere den Servo
    init_servo();

    while (1) {
        // Servo langsam von 0° auf 180° bewegen
        for (int angle = 0; angle <= 180; angle += 10) {
            set_servo_angle(angle);
            vTaskDelay(pdMS_TO_TICKS(500)); // 500 ms warten
        }

        // Servo langsam von 180° auf 0° zurück bewegen
        for (int angle = 180; angle >= 0; angle -= 10) {
            set_servo_angle(angle);
            vTaskDelay(pdMS_TO_TICKS(500)); // 500 ms warten
        }
    }
}
