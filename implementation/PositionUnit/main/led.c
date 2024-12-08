#include "include/led.h"

/**
 * @file led.c
 * @brief LED control functions.
 *
 * This header file declares the following functions:
 *
 * @brief Sets the color of a single LED in the strip.
 *
 * @param led_strip The LED strip to control.
 * @param index The index of the pixel to change (here the first LED).
 * @param red The red component of the color (value from 0 to 255).
 * @param green The green component of the color (value from 0 to 255).
 * @param blue The blue component of the color (value from 0 to 255).
 *
 * @code
 * led_strip_set_pixel(led_strip, 0, 255, 16, 16);
 * @endcode
 *
 * Additionally:
 * - led_strip_refresh(led_strip);
 * - led_strip_clear(led_strip);
 *
 * BUILD_IN_LED is set to 0 and connected to BLINK_GPIO8.
 */
