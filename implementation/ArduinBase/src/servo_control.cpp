#include "servo_control.h"

// Variable für den Servo-Pin (Standardwert: 20)
int SERVO_GPIO_PIN = 14;

// Variable to track the current servo position
static int currentServoAngle = 90; // Start at neutral position

uint32_t calculate_duty_us(uint32_t pulse_width_us, uint32_t timer_resolution_bits) {
    uint32_t max_duty = (1 << timer_resolution_bits) - 1;
    return (pulse_width_us * max_duty) / (1000000 / PWM_FREQUENCY);
}

void setupServo() {
    // Configure the LEDC timer
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,
        .duty_resolution = LEDC_TIMER_13_BIT, // 13-bit resolution for high precision
        .timer_num = LEDC_TIMER,
        .freq_hz = PWM_FREQUENCY,
        .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);
    
    // Configure the LEDC channel
    ledc_channel_config_t ledc_channel = {
        .gpio_num = SERVO_GPIO_PIN,
        .speed_mode = LEDC_MODE,
        .channel = LEDC_CHANNEL,
        .timer_sel = LEDC_TIMER,
        .duty = calculate_duty_us(SERVO_NEUTRAL, LEDC_TIMER_13_BIT),
        .hpoint = 0
    };
    ledc_channel_config(&ledc_channel);
    
    // Set the servo to neutral position
    setServoAngle(90);
    
    Serial.println("Servo @IO20 initialisiert");
}

void setServoAngle(int angle) {
    // Constrain the angle to valid range
    angle = constrain(angle, 0, SERVO_MAX_DEGREE);
    
    // Map the angle to pulse width
    uint32_t pulse_width = map(angle, 0, SERVO_MAX_DEGREE, SERVO_MIN_PULSE, SERVO_MAX_PULSE);
    
    // Calculate duty cycle
    uint32_t duty = calculate_duty_us(pulse_width, LEDC_TIMER_13_BIT);
    
    // Set duty cycle
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
    
    // Update current position
    currentServoAngle = angle;
    
    Serial.print("Servo Winkel gesetzt auf: ");
    Serial.println(angle);
}

void sweepServo(int targetAngle, int speed) {
    // Constrain target angle
    targetAngle = constrain(targetAngle, 0, SERVO_MAX_DEGREE);
    
    // Get the current position
    int startAngle = currentServoAngle;
    
    // Determine direction and step size
    int step = (targetAngle > startAngle) ? 1 : -1;
    
    // Move the servo step by step
    for (int angle = startAngle; angle != targetAngle + step; angle += step) {
        setServoAngle(angle);
        delay(speed); // delay between steps for smooth movement
    }
}

int getCurrentServoAngle() {
    return currentServoAngle;
}