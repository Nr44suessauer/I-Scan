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
#include "include/buttons.h"
#include "include/i2c.h"



void init_sys()         // @brief Initializes separate functions for the software, including: I²C,Uart etc.
{
    init_GPIO();        // config of I/O Pins
    init_motor_pins();  // config for motorpins^^
    init_servo();       // sets config for Servo & 90° position
    configure_led();    // Configure Buildin LED
    
    i2c_master_init();  // Initialize I²C
    i2c_master_check_slave(); // Check if I²C is connected

}

void test_function()
{
    // Poll GPIO Pins (Inputs)
    poll_GIPO();

    // Test LED strip colors
    for (int i = 0; i < 3; i++) 
    {
        led_strip_set_color(COLOR_PURPLE);
        vTaskDelay(300 / portTICK_PERIOD_MS);
        led_strip_set_color(COLOR_GREEN);
        vTaskDelay(300 / portTICK_PERIOD_MS);
        led_strip_set_color(COLOR_BLUE);
        vTaskDelay(300 / portTICK_PERIOD_MS);
    }

    // Test motor movement
    for (int i = 0; i < 5; i++) 
    {
        move_motor(100, 1);
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }

    // Test servo angles
    for (int i = 0; i < 180; i++) 
    {
        set_servo_angle(i);
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }

    i2c_scanner();
    printf("Value: %d\n",  distance_read());

}


void app_main(void)
{
    init_sys();

    while (1) 
    {
        test_function(); 
    }
}


