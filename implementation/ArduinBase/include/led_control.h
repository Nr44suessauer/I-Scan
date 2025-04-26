#ifndef LED_CONTROL_H
#define LED_CONTROL_H

#include <Arduino.h>
#include <FastLED.h>

// Definition for LED control
#define LED_PIN     38      // Data pin for the RGB LED
#define NUM_LEDS    1       // Number of LEDs (only one here)
#define LED_TYPE    WS2812B // LED type
#define COLOR_ORDER GRB     // Color order (typical for WS2812B)
#define BRIGHTNESS  5       // Brightness (0-255)

// Color change speed
#define DELAY_MS    1000    // Time between color changes in milliseconds

// Function declarations
void setupLEDs();
void updateLEDs();

// New functions for manual color control
void setColorByIndex(int index);     // Sets color by predefined index
void setColorRGB(int r, int g, int b); // Sets color with RGB values
void setColorHSV(int h, int s, int v); // Sets color with HSV values

#endif // LED_CONTROL_H