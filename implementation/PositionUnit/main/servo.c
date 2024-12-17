#include "include/servo.h"
/**
 * @brief Initializes the servo controller.
 *
 * This function configures the timer and channel for the servo controller using the LEDC (LED Control) peripheral.
 * It sets up the timer with a specified frequency and resolution, and configures the channel with the appropriate
 * GPIO pin, duty cycle, and other parameters.
 *
 * Timer Configuration:
 * - speed_mode: The speed mode of the LEDC timer.
 * - timer_num: The timer number to use.
 * - duty_resolution: The resolution of the duty cycle (15-bit in this case).
 * - freq_hz: The frequency of the PWM signal.
 * - clk_cfg: The clock configuration (automatic clock selection).
 *
 * Channel Configuration:
 * - gpio_num: The GPIO pin number connected to the servo.
 * - speed_mode: The speed mode of the LEDC channel.
 * - channel: The channel number to use.
 * - timer_sel: The timer to be used by the channel.
 * - duty: The duty cycle for the neutral position of the servo, calculated using the `calculate_duty_us` function.
 * - hpoint: The high point value (set to 0).
 * - intr_type: The interrupt type (interrupts disabled).
 *
 * This function should be called during the initialization phase to set up the servo controller before using it.
 */
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

    // channel-configuration
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

/**
 * @brief Calculates the duty cycle for a given pulse width in microseconds.
 *
 * This function converts a pulse width specified in microseconds to a duty cycle
 * value based on the resolution of the timer. The duty cycle is calculated as
 * a proportion of the timer's maximum count value, which is determined by the
 * timer's resolution in bits.
 *
 * @param pulse_width_us The pulse width in microseconds. This is the duration
 *                       of the high signal in the PWM cycle.
 * @param timer_resolution_bits The resolution of the timer in bits. This value
 *                              determines the maximum count value of the timer.
 *                              For example, if the timer has a resolution of 8 bits,
 *                              the maximum count value is 2^8 - 1 = 255.
 *
 * @return The calculated duty cycle as a 32-bit unsigned integer. This value
 *         represents the number of timer counts corresponding to the specified
 *         pulse width.
 */
uint32_t calculate_duty_us(uint32_t pulse_width_us, uint32_t timer_resolution_bits) {
    // Umwandlung von Mikrosekunden in Duty-Cycle-Bits
    uint32_t duty = ((uint64_t)(1 << timer_resolution_bits) * pulse_width_us) / 20000; // 20000 µs = 20 ms (50 Hz)
    return duty;
}

/**
 * @brief Sets the servo to a specified angle.
 *
 * This function adjusts the servo motor to the desired angle within the 
 * allowable range. If the provided angle is outside the valid range, 
 * it will be clamped to the nearest valid value.
 *
 * @param angle The desired angle to set the servo to. This value should 
 *              be between 0 and SERVO_MAX_DEGREE.
 *
 * The function performs the following steps:
 * 1. Clamps the input angle to ensure it is within the valid range.
 * 2. Calculates the pulse width corresponding to the desired angle.
 * 3. Computes the duty cycle based on the calculated pulse width.
 * 4. Sets the duty cycle for the servo control signal.
 * 5. Updates the duty cycle to apply the changes.
 *
 * The pulse width is calculated using the formula:
 * pulse_width = SERVO_MIN_PULSE + ((SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle) / SERVO_MAX_DEGREE;
 *
 * The duty cycle is then calculated using the `calculate_duty_us` function.
 *
 * The function uses the following constants and functions:
 * - SERVO_MAX_DEGREE: The maximum allowable angle for the servo.
 * - SERVO_MIN_PULSE: The minimum pulse width for the servo.
 * - SERVO_MAX_PULSE: The maximum pulse width for the servo.
 * - calculate_duty_us(pulse_width, 15): Function to calculate the duty cycle.
 * - ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty): Function to set the duty cycle.
 * - ledc_update_duty(LEDC_MODE, LEDC_CHANNEL): Function to update the duty cycle.
 */

void set_servo_angle(int angle) {
    if (angle < 0) angle = 0;
    if (angle > SERVO_MAX_DEGREE) angle = SERVO_MAX_DEGREE;

    // Calculate the pulse width
    uint32_t pulse_width = SERVO_MIN_PULSE +
                           ((SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle) / SERVO_MAX_DEGREE;

    // Calculate the duty cycle
    uint32_t duty = calculate_duty_us(pulse_width, 15);

    // Set the duty cycle
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
}
