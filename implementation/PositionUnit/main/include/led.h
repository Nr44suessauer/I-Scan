#ifndef LED_H
#define LED_H

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "led_strip.h"
#include "sdkconfig.h"

#define BUILD_IN_LED 0
#define BLINK_GPIO CONFIG_BLINK_GPIO

static led_strip_handle_t led_strip;
static uint8_t s_led_state = 0;

typedef struct {
    uint8_t red;
    uint8_t green;
    uint8_t blue;
} Color;

// Basic Colors
const Color COLOR_RED = {255, 0, 0};
const Color COLOR_GREEN = {0, 255, 0};
const Color COLOR_BLUE = {0, 0, 255};
const Color COLOR_WHITE = {255, 255, 255};
const Color COLOR_OFF = {0, 0, 0};
const Color COLOR_PURPLE = {128, 0, 128};


/**
 * Sets the color of the built-in LED on the LED strip.
 *
 * This function updates the built-in LED's color by setting its red, green,
 * and blue components based on the provided Color structure. After setting the
 * color, it refreshes the LED strip to apply the changes.
 *
 * @param color In led.h struct Color
 */
void led_strip_set_color(Color color) {
    led_strip_set_pixel(led_strip,BUILD_IN_LED, color.red, color.green, color.blue);
    led_strip_refresh(led_strip);
}

#ifdef CONFIG_BLINK_LED_STRIP

void led_strip_set_color(Color color);

static void blink_led()
{
    s_led_state = !s_led_state;
    /* If the addressable LED is enabled */
    if (s_led_state) {
        /* Set the LED pixel using RGB from 0 (0%) to 255 (100%) for each color */
        led_strip_set_pixel(led_strip, 0, 255, 16, 16);
        /* Refresh the strip to send data */
        led_strip_refresh(led_strip);
    } else {
        /* Set all LED off to clear all pixels */
        led_strip_clear(led_strip);
    }
}

static void configure_led()
{
    /* LED strip initialization with the GPIO and pixels number*/
    led_strip_config_t strip_config = {
        .strip_gpio_num = BLINK_GPIO,
        .max_leds = 1, // at least one LED on board
    };
#if CONFIG_BLINK_LED_STRIP_BACKEND_RMT
    led_strip_rmt_config_t rmt_config = {
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
#elif CONFIG_BLINK_LED_STRIP_BACKEND_SPI
    led_strip_spi_config_t spi_config = {
        .spi_bus = SPI2_HOST,
        .flags.with_dma = true,
    };
    ESP_ERROR_CHECK(led_strip_new_spi_device(&strip_config, &spi_config, &led_strip));
#else
#error "unsupported LED strip backend"
#endif
    /* Set all LED off to clear all pixels */
    led_strip_clear(led_strip);
}

#elif CONFIG_BLINK_LED_GPIO

static void blink_led(void)
{
    /* Set the GPIO level according to the state (LOW or HIGH)*/
    gpio_set_level(BLINK_GPIO, s_led_state);
}

static void configure_led(void)
{
    ESP_LOGI(TAG, "Example configured to blink GPIO LED!");
    gpio_reset_pin(BLINK_GPIO);
    /* Set the GPIO as a push/pull output */
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);
}

#else
#endif



#endif // LED_H