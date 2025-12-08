#include "pin_config.h"
#include "motor_28byj48.h"
#include "advanced_motor.h"
#include "servo_control.h"
#include "led_control.h"
#include "button_control.h"

// Globale Pin-Konfiguration
PinConfiguration currentPinConfig;

// Preferences-Objekt für EEPROM-Zugriff
Preferences preferences;

/**
 * Initialisiert die Pin-Konfiguration
 * Lädt gespeicherte Werte oder setzt Standardwerte
 */
void initPinConfig() {
    loadPinConfig();
    
    // Wenn keine gültige Konfiguration vorhanden ist, Standardwerte setzen
    if (!currentPinConfig.isValid) {
        resetPinConfigToDefaults();
        savePinConfig();
    }
    
    // Pin-Konfiguration auf die jeweiligen Module anwenden
    applyPinConfig();
}

/**
 * Lädt die Pin-Konfiguration aus dem EEPROM
 */
void loadPinConfig() {
    preferences.begin(EEPROM_NAMESPACE, false);
    
    // Prüfen ob gültige Konfiguration vorhanden ist
    currentPinConfig.isValid = preferences.getBool("valid", false);
    
    if (currentPinConfig.isValid) {
        // 28BYJ-48 Motor Pins
        currentPinConfig.motor_28byj48_pin1 = preferences.getInt("m28_p1", MOTOR_28BYJ48_DEFAULT_PIN_1);
        currentPinConfig.motor_28byj48_pin2 = preferences.getInt("m28_p2", MOTOR_28BYJ48_DEFAULT_PIN_2);
        currentPinConfig.motor_28byj48_pin3 = preferences.getInt("m28_p3", MOTOR_28BYJ48_DEFAULT_PIN_3);
        currentPinConfig.motor_28byj48_pin4 = preferences.getInt("m28_p4", MOTOR_28BYJ48_DEFAULT_PIN_4);
        
        // NEMA 23 Motor Pins
        currentPinConfig.nema23_step_pin = preferences.getInt("nema_step", STEP_PIN);
        currentPinConfig.nema23_dir_pin = preferences.getInt("nema_dir", DIR_PIN);
        currentPinConfig.nema23_enable_pin = preferences.getInt("nema_en", ENABLE_PIN);
        
        // Servo Pin
        currentPinConfig.servo_pin = preferences.getInt("servo_p", 48);
        
        // LED Pin
        currentPinConfig.led_pin = preferences.getInt("led_p", LED_PIN);
        
        // Button Pin
        currentPinConfig.button_pin = preferences.getInt("btn_p", BUTTON_PIN);
        
        // WiFi Configuration
        preferences.getString("wifi_ssid", currentPinConfig.wifi_ssid, sizeof(currentPinConfig.wifi_ssid));
        preferences.getString("wifi_pass", currentPinConfig.wifi_password, sizeof(currentPinConfig.wifi_password));
        preferences.getString("wifi_host", currentPinConfig.wifi_hostname, sizeof(currentPinConfig.wifi_hostname));
        
        // Falls WiFi-Daten leer sind, Standard-Werte verwenden
        if (strlen(currentPinConfig.wifi_ssid) == 0) {
            strcpy(currentPinConfig.wifi_ssid, "Teekanne");
        }
        if (strlen(currentPinConfig.wifi_password) == 0) {
            strcpy(currentPinConfig.wifi_password, "49127983361694305550");
        }
        if (strlen(currentPinConfig.wifi_hostname) == 0) {
            strcpy(currentPinConfig.wifi_hostname, "ESP32-IScan");
        }
        
        Serial.println("✅ Pin-Konfiguration aus EEPROM geladen");
    } else {
        Serial.println("⚠️ Keine gültige Pin-Konfiguration im EEPROM gefunden");
        resetPinConfigToDefaults();
    }
    
    preferences.end();
}

/**
 * Speichert die aktuelle Pin-Konfiguration im EEPROM
 */
void savePinConfig() {
    preferences.begin(EEPROM_NAMESPACE, false);
    
    // 28BYJ-48 Motor Pins
    preferences.putInt("m28_p1", currentPinConfig.motor_28byj48_pin1);
    preferences.putInt("m28_p2", currentPinConfig.motor_28byj48_pin2);
    preferences.putInt("m28_p3", currentPinConfig.motor_28byj48_pin3);
    preferences.putInt("m28_p4", currentPinConfig.motor_28byj48_pin4);
    
    // NEMA 23 Motor Pins
    preferences.putInt("nema_step", currentPinConfig.nema23_step_pin);
    preferences.putInt("nema_dir", currentPinConfig.nema23_dir_pin);
    preferences.putInt("nema_en", currentPinConfig.nema23_enable_pin);
    
    // Servo Pin
    preferences.putInt("servo_p", currentPinConfig.servo_pin);
    
    // LED Pin
    preferences.putInt("led_p", currentPinConfig.led_pin);
    
    // Button Pin
    preferences.putInt("btn_p", currentPinConfig.button_pin);
    
    // WiFi Configuration
    preferences.putString("wifi_ssid", currentPinConfig.wifi_ssid);
    preferences.putString("wifi_pass", currentPinConfig.wifi_password);
    preferences.putString("wifi_host", currentPinConfig.wifi_hostname);
    
    // Validierungs-Flag setzen
    preferences.putBool("valid", true);
    currentPinConfig.isValid = true;
    
    preferences.end();
    
    Serial.println("💾 Pin-Konfiguration im EEPROM gespeichert");
    printPinConfig();
}

/**
 * Setzt die Pin-Konfiguration auf Standardwerte zurück
 */
void resetPinConfigToDefaults() {
    // 28BYJ-48 Motor Pins
    currentPinConfig.motor_28byj48_pin1 = MOTOR_28BYJ48_DEFAULT_PIN_1;
    currentPinConfig.motor_28byj48_pin2 = MOTOR_28BYJ48_DEFAULT_PIN_2;
    currentPinConfig.motor_28byj48_pin3 = MOTOR_28BYJ48_DEFAULT_PIN_3;
    currentPinConfig.motor_28byj48_pin4 = MOTOR_28BYJ48_DEFAULT_PIN_4;
    
    // NEMA 23 Motor Pins
    currentPinConfig.nema23_step_pin = STEP_PIN;
    currentPinConfig.nema23_dir_pin = DIR_PIN;
    currentPinConfig.nema23_enable_pin = ENABLE_PIN;
    
    // Servo Pin
    currentPinConfig.servo_pin = 48;
    
    // LED Pin
    currentPinConfig.led_pin = LED_PIN;
    
    // Button Pin
    currentPinConfig.button_pin = BUTTON_PIN;
    
    // WiFi Configuration - Defaults
    strncpy(currentPinConfig.wifi_ssid, "Teekanne", sizeof(currentPinConfig.wifi_ssid));
    strncpy(currentPinConfig.wifi_password, "49127983361694305550", sizeof(currentPinConfig.wifi_password));
    strncpy(currentPinConfig.wifi_hostname, "ESP32-IScan", sizeof(currentPinConfig.wifi_hostname));
    
    currentPinConfig.isValid = true;
    
    Serial.println("🔄 Pin-Konfiguration auf Standardwerte zurückgesetzt");
}

/**
 * Wendet die aktuelle Pin-Konfiguration auf alle Module an
 */
void applyPinConfig() {
    // 28BYJ-48 Motor Pins setzen
    motor_28byj48_pin_1 = currentPinConfig.motor_28byj48_pin1;
    motor_28byj48_pin_2 = currentPinConfig.motor_28byj48_pin2;
    motor_28byj48_pin_3 = currentPinConfig.motor_28byj48_pin3;
    motor_28byj48_pin_4 = currentPinConfig.motor_28byj48_pin4;
    
    // Servo Pin setzen
    SERVO_GPIO_PIN = currentPinConfig.servo_pin;
    
    Serial.println("✅ Pin-Konfiguration auf Module angewendet");
}

/**
 * Setzt die komplette Pin-Konfiguration
 */
void setPinConfig(const PinConfiguration& config) {
    currentPinConfig = config;
    currentPinConfig.isValid = true;
    applyPinConfig();
}

/**
 * Gibt die aktuelle Pin-Konfiguration zurück
 */
PinConfiguration getPinConfig() {
    return currentPinConfig;
}

/**
 * Gibt die Pin-Konfiguration auf der seriellen Konsole aus
 */
void printPinConfig() {
    Serial.println("\n📌 Aktuelle Pin-Konfiguration:");
    Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    Serial.printf("28BYJ-48 Motor: IN1=%d, IN2=%d, IN3=%d, IN4=%d\n", 
                  currentPinConfig.motor_28byj48_pin1,
                  currentPinConfig.motor_28byj48_pin2,
                  currentPinConfig.motor_28byj48_pin3,
                  currentPinConfig.motor_28byj48_pin4);
    Serial.printf("NEMA 23 Motor: STEP=%d, DIR=%d, ENABLE=%d\n",
                  currentPinConfig.nema23_step_pin,
                  currentPinConfig.nema23_dir_pin,
                  currentPinConfig.nema23_enable_pin);
    Serial.printf("Servo: GPIO %d\n", currentPinConfig.servo_pin);
    Serial.printf("LED: GPIO %d\n", currentPinConfig.led_pin);
    Serial.printf("Button: GPIO %d\n", currentPinConfig.button_pin);
    Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
}

// Einzelne Pin-Setter
void set28BYJ48Pins(int pin1, int pin2, int pin3, int pin4) {
    // Config-Struktur aktualisieren
    currentPinConfig.motor_28byj48_pin1 = pin1;
    currentPinConfig.motor_28byj48_pin2 = pin2;
    currentPinConfig.motor_28byj48_pin3 = pin3;
    currentPinConfig.motor_28byj48_pin4 = pin4;
    
    // Globale Variablen aktualisieren
    motor_28byj48_pin_1 = pin1;
    motor_28byj48_pin_2 = pin2;
    motor_28byj48_pin_3 = pin3;
    motor_28byj48_pin_4 = pin4;
    
    // In EEPROM speichern
    savePinConfig();
    
    Serial.printf("✓ 28BYJ-48 Pins gespeichert: %d, %d, %d, %d\n", pin1, pin2, pin3, pin4);
}

void setNEMA23Pins(int stepPin, int dirPin, int enablePin) {
    currentPinConfig.nema23_step_pin = stepPin;
    currentPinConfig.nema23_dir_pin = dirPin;
    currentPinConfig.nema23_enable_pin = enablePin;
    savePinConfig();
}

void setServoPin(int pin) {
    currentPinConfig.servo_pin = pin;
    SERVO_GPIO_PIN = pin;
    savePinConfig();
}

void setLedPin(int pin) {
    currentPinConfig.led_pin = pin;
    savePinConfig();
}

void setButtonPin(int pin) {
    currentPinConfig.button_pin = pin;
    savePinConfig();
}

void setWiFiConfig(const char* ssid, const char* password, const char* hostname) {
    strncpy(currentPinConfig.wifi_ssid, ssid, sizeof(currentPinConfig.wifi_ssid) - 1);
    currentPinConfig.wifi_ssid[sizeof(currentPinConfig.wifi_ssid) - 1] = '\0';
    
    strncpy(currentPinConfig.wifi_password, password, sizeof(currentPinConfig.wifi_password) - 1);
    currentPinConfig.wifi_password[sizeof(currentPinConfig.wifi_password) - 1] = '\0';
    
    strncpy(currentPinConfig.wifi_hostname, hostname, sizeof(currentPinConfig.wifi_hostname) - 1);
    currentPinConfig.wifi_hostname[sizeof(currentPinConfig.wifi_hostname) - 1] = '\0';
    
    savePinConfig();
}

// Einzelne Pin-Getter
void get28BYJ48Pins(int* pin1, int* pin2, int* pin3, int* pin4) {
    *pin1 = currentPinConfig.motor_28byj48_pin1;
    *pin2 = currentPinConfig.motor_28byj48_pin2;
    *pin3 = currentPinConfig.motor_28byj48_pin3;
    *pin4 = currentPinConfig.motor_28byj48_pin4;
}

void getNEMA23Pins(int* stepPin, int* dirPin, int* enablePin) {
    *stepPin = currentPinConfig.nema23_step_pin;
    *dirPin = currentPinConfig.nema23_dir_pin;
    *enablePin = currentPinConfig.nema23_enable_pin;
}

int getServoPin() {
    return currentPinConfig.servo_pin;
}

int getLedPin() {
    return currentPinConfig.led_pin;
}

int getButtonPin() {
    return currentPinConfig.button_pin;
}

void getWiFiConfig(char* ssid, char* password, char* hostname) {
    if (ssid) strcpy(ssid, currentPinConfig.wifi_ssid);
    if (password) strcpy(password, currentPinConfig.wifi_password);
    if (hostname) strcpy(hostname, currentPinConfig.wifi_hostname);
}
