#include "include/buttons.h"

    /**
     * @brief Configures the GPIO pin for the button.
     *
     * This code sets the direction of the GPIO pin connected to the button as input
     * and configures the pull mode to use the internal pull-up resistor.
     *
     * @param BUTTON_PIN The GPIO pin number connected to the button.
     */

void init_GPIO()
{
    gpio_set_direction(BUTTON_PIN, GPIO_MODE_INPUT);
    gpio_set_pull_mode(BUTTON_PIN, GPIO_PULLUP_ONLY);
    
}

/**
 * @brief Polls the state of the button and prints its status.
 *
 * This function reads the current state of the GPIO pin connected to the button.
 * If the button is pressed (logic level 0), it prints "Button pressed!".
 * Otherwise, it prints "Button NOT pressed!".
 *
 * @param BUTTON_PIN The GPIO pin number connected to the button.
 */

void poll_GIPO()
{
    int button_state = gpio_get_level(BUTTON_PIN);
    if (button_state == 0) // Button pressed
    {
        printf("Button pressed!\n");
    }
    else
    {
        printf("Button NOT pressed!\n");
    }
}
