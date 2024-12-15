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

uint16_t counter;               // testcounter for things


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
    poll_GIPO(); // polls GPIO Pins (Inputs)
    //i2c_scanner(); // Scans for I²C devices
       counter = 0;    // Servo-Counter

    // for (size_t i = 0; i < 18; i++)
    // {
    //     led_strip_set_color(COLOR_PURPLE);
    //     vTaskDelay(300 / portTICK_PERIOD_MS);
    //     led_strip_set_color(COLOR_GREEN);
    //     vTaskDelay(300 / portTICK_PERIOD_MS);
    //     led_strip_set_color(COLOR_BLUE);
    //     vTaskDelay(300 / portTICK_PERIOD_MS);

    //     move_motor(1000, 1);

    //     set_servo_angle(counter);

    //     counter += 10;

    //     if (counter > 180)  
    //     {
    //         counter = 0;
    //     }
    // }
}


void app_main(void)
{
    init_sys();

    while (1) 
    {
        i2c_master_check_slave(); // Check if I²C is connected
        //test_function(); 
        //i2c_scanner();

        vTaskDelay(1000 / portTICK_PERIOD_MS);

    //   read_register_and_output_uart(0x00, 1);
    
    }
}


