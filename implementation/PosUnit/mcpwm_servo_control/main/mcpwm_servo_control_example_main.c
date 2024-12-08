#include "includes/motor.h"
#include "includes/servo.h"

uint16_t counter;

// Einstiegspunkt des Programms
void app_main() {
    
    counter = 0;    // Servo-Counter

    init_motor_pins();  // config for motorpins^^
    init_servo();       // sets config for Servo & 90° position

    while (1)
    {
        move_motor(512, 1);
        // vTaskDelay(1000 / portTICK_PERIOD_MS);
        set_servo_angle(counter);
        counter += 10;
        if (counter > 180)  
        {
            counter = 0;
        }
    }
    
    // xTaskCreate(motor_task, "motor_task", 2048, NULL, 5, NULL);
}
