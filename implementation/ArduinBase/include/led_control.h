#ifndef LED_CONTROL_H
#define LED_CONTROL_H

#include <Arduino.h>
#include <FastLED.h>

// Definition für die LED-Ansteuerung
#define LED_PIN     38      // Datenpin für die RGB-LED
#define NUM_LEDS    1       // Anzahl der LEDs (hier nur eine)
#define LED_TYPE    WS2812B // Typ der LED
#define COLOR_ORDER GRB     // Farbfolge (typisch für WS2812B)
#define BRIGHTNESS  5      // Helligkeit (0-255)

// Farbwechselgeschwindigkeit
#define DELAY_MS    1000    // Zeit zwischen Farbwechseln in Millisekunden

// Funktionsdeklarationen
void setupLEDs();
void updateLEDs();

// Neue Funktionen zur manuellen Farbsteuerung
void setColorByIndex(int index);     // Setzt Farbe nach vordefiniertem Index
void setColorRGB(int r, int g, int b); // Setzt Farbe mit RGB-Werten
void setColorHSV(int h, int s, int v); // Setzt Farbe mit HSV-Werten

#endif // LED_CONTROL_H