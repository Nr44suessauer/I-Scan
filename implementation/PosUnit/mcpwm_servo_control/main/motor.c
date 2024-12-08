#include "includes/motor.h"

// Halbschrittsequenz (8 Schritte pro Phase für mehr Präzision und Drehmoment)
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


// Initialisierung der GPIO-Pins
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

// Setzt die GPIO-Pins gemäß der Sequenz
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

// Bewegt den Schrittmotor um die angegebene Anzahl an Schritten
void move_motor(int steps, int direction) {
    for (int i = 0; i < steps; i++) {
        // Berechnet den aktuellen Schritt (vorwärts oder rückwärts)
        int step = (direction > 0) ? i % 8 : (7 - (i % 8));
        set_motor_pins(step);

        // Zeitverzögerung zwischen den Schritten
        
    }
}

// Task für den Schrittmotorbetrieb
void motor_task() {


    while (1) {
        printf("Motor: 1 Umdrehung im Uhrzeigersinn\n");
        move_motor(2000, 1); // 512 Schritte für 1 Umdrehung
        
        printf("Motor: 1 Umdrehung gegen den Uhrzeigersinn\n");
        move_motor(20000, -1); // 512 Schritte in die andere Richtung
    
    }
}
