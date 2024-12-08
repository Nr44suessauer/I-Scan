#include "include/led.h"
/**
 * @brief Available Colors
 *  led_strip_set_color(COLOR);
 * 
 *  **COLOR_RED**
 *  **COLOR_GREEN**
 *  **COLOR_BLUE**
 *  **COLOR_WHITE**
 *  **COLOR_OFF**
 *  **COLOR_PURPLE**
 */

#include "include/motor.h"
#include "include/servo.h"

uint16_t counter;

void test_function()
{
    counter = 0;    // Servo-Counter

    for (size_t i = 0; i < 18; i++)
    {
        led_strip_set_color(COLOR_PURPLE);
        vTaskDelay(300 / portTICK_PERIOD_MS);
        led_strip_set_color(COLOR_GREEN);
        vTaskDelay(300 / portTICK_PERIOD_MS);
        led_strip_set_color(COLOR_BLUE);
        vTaskDelay(300 / portTICK_PERIOD_MS);

        move_motor(1000, 1);

        set_servo_angle(counter);
        counter += 10;
        if (counter > 180)  
        {
            counter = 0;
        }
    }
}


void app_main(void)
{

    init_motor_pins();  // config for motorpins^^
    init_servo();       // sets config for Servo & 90° position
    configure_led();    // Configure Buildin LED

    while (1) 
    {
        test_function(); 
        
    }
}


