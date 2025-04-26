#include "led_control.h"

// LED-Array erstellen
CRGB leds[NUM_LEDS];

// Verschiedene Farben definieren
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

// Bestehende Funktionen bleiben unverändert
void setupLEDs() {
  // FastLED initialisieren
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  
  // Erste Farbe setzen
  leds[0] = colorList[currentColorIndex];
  FastLED.show();
  
  Serial.println("RGB@IO38 gestartet");
}

void updateLEDs() {
  unsigned long currentMillis = millis();
  
  // Prüfen, ob es Zeit für einen Farbwechsel ist
  if (currentMillis - previousMillis >= DELAY_MS) {
    previousMillis = currentMillis;
    
    // Nächste Farbe auswählen
    currentColorIndex = (currentColorIndex + 1) % (sizeof(colorList) / sizeof(colorList[0]));
    
    // Farbe setzen
    leds[0] = colorList[currentColorIndex];
    FastLED.show();
    
    // Aktuelle Farbe ausgeben
    Serial.print("Farbe gewechselt zu: ");
    switch (currentColorIndex) {
      case 0: Serial.println("Rot"); break;
      case 1: Serial.println("Grün"); break;
      case 2: Serial.println("Blau"); break;
      case 3: Serial.println("Gelb"); break;
      case 4: Serial.println("Lila"); break;
      case 5: Serial.println("Orange"); break;
      case 6: Serial.println("Weiß"); break;
    }
  }
}

// Neue Funktionen zur Farbsteuerung

// Farbe nach Index setzen (0=Rot, 1=Grün, usw.)
void setColorByIndex(int index) {
  // Sicherstellen, dass der Index gültig ist
  int maxIndex = sizeof(colorList) / sizeof(colorList[0]) - 1;
  index = constrain(index, 0, maxIndex);
  
  // Farbe setzen
  currentColorIndex = index;
  leds[0] = colorList[currentColorIndex];
  FastLED.show();
  
  // Debugging-Ausgabe
  Serial.print("Farbe manuell gesetzt auf: ");
  switch (currentColorIndex) {
    case 0: Serial.println("Rot"); break;
    case 1: Serial.println("Grün"); break;
    case 2: Serial.println("Blau"); break;
    case 3: Serial.println("Gelb"); break;
    case 4: Serial.println("Lila"); break;
    case 5: Serial.println("Orange"); break;
    case 6: Serial.println("Weiß"); break;
    default: Serial.println("Unbekannt");
  }
}

// Farbe mit RGB-Werten setzen (0-255 für jede Komponente)
void setColorRGB(int r, int g, int b) {
  // RGB-Werte setzen
  leds[0] = CRGB(r, g, b);
  FastLED.show();
  
  // Debugging-Ausgabe
  Serial.print("Farbe manuell gesetzt auf RGB: ");
  Serial.print(r); Serial.print(", ");
  Serial.print(g); Serial.print(", ");
  Serial.println(b);
}

// Farbe mit HSV-Werten setzen (Farbton 0-255, Sättigung 0-255, Helligkeit 0-255)
void setColorHSV(int h, int s, int v) {
  // HSV-Werte setzen
  leds[0] = CHSV(h, s, v);
  FastLED.show();
  
  // Debugging-Ausgabe
  Serial.print("Farbe manuell gesetzt auf HSV: ");
  Serial.print(h); Serial.print(", ");
  Serial.print(s); Serial.print(", ");
  Serial.println(v);
}