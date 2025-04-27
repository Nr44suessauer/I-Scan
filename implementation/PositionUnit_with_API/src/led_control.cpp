#include "led_control.h"

// Create LED array
CRGB leds[NUM_LEDS];

// Define various colors
CRGB colorList[] = {
  CRGB::Red,
  CRGB::Green,
  CRGB::Blue,
  CRGB::Yellow,
  CRGB::Purple,
  CRGB::Orange,
  CRGB::White
};

int currentColorIndex = 0;
unsigned long previousMillis = 0;

// Existing functions remain unchanged
void setupLEDs() {
  // Initialize FastLED
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  
  // Set first color
  leds[0] = colorList[currentColorIndex];
  FastLED.show();
  
  Serial.println("RGB@IO38 started");
}

void updateLEDs() {
  unsigned long currentMillis = millis();
  
  // Check if it's time for a color change
  if (currentMillis - previousMillis >= DELAY_MS) {
    previousMillis = currentMillis;
    
    // Select next color
    currentColorIndex = (currentColorIndex + 1) % (sizeof(colorList) / sizeof(colorList[0]));
    
    // Set color
    leds[0] = colorList[currentColorIndex];
    FastLED.show();
    
    // Output current color
    Serial.print("Color changed to: ");
    switch (currentColorIndex) {
      case 0: Serial.println("Red"); break;
      case 1: Serial.println("Green"); break;
      case 2: Serial.println("Blue"); break;
      case 3: Serial.println("Yellow"); break;
      case 4: Serial.println("Purple"); break;
      case 5: Serial.println("Orange"); break;
      case 6: Serial.println("White"); break;
    }
  }
}

// New functions for color control

// Set color by index (0=Red, 1=Green, etc.)
void setColorByIndex(int index) {
  // Ensure index is valid
  int maxIndex = sizeof(colorList) / sizeof(colorList[0]) - 1;
  index = constrain(index, 0, maxIndex);
  
  // Set color
  currentColorIndex = index;
  leds[0] = colorList[currentColorIndex];
  FastLED.show();
  
  // Debug output
  Serial.print("Color manually set to: ");
  switch (currentColorIndex) {
    case 0: Serial.println("Red"); break;
    case 1: Serial.println("Green"); break;
    case 2: Serial.println("Blue"); break;
    case 3: Serial.println("Yellow"); break;
    case 4: Serial.println("Purple"); break;
    case 5: Serial.println("Orange"); break;
    case 6: Serial.println("White"); break;
    default: Serial.println("Unknown");
  }
}

// Set color with RGB values (0-255 for each component)
void setColorRGB(int r, int g, int b) {
  // Set RGB values
  leds[0] = CRGB(r, g, b);
  FastLED.show();
  
  // Debug output
  Serial.print("Color manually set to RGB: ");
  Serial.print(r); Serial.print(", ");
  Serial.print(g); Serial.print(", ");
  Serial.println(b);
}

// Set color with HSV values (hue 0-255, saturation 0-255, brightness 0-255)
void setColorHSV(int h, int s, int v) {
  // Set HSV values
  leds[0] = CHSV(h, s, v);
  FastLED.show();
  
  // Debug output
  Serial.print("Color manually set to HSV: ");
  Serial.print(h); Serial.print(", ");
  Serial.print(s); Serial.print(", ");
  Serial.println(v);
}

// New function for brightness control
void setBrightness(int brightness) {
  // Ensure brightness is valid (0-255)
  brightness = constrain(brightness, 0, 255);
  
  // Set brightness
  FastLED.setBrightness(brightness);
  FastLED.show();
  
  // Debug output
  Serial.print("Brightness set to: ");
  Serial.println(brightness);
}