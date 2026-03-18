#ifndef PIN_CONFIG_H
#define PIN_CONFIG_H

#include <Arduino.h>
#include <Preferences.h>

// EEPROM Namespace
#define EEPROM_NAMESPACE "pin_config"
#define DEVICE_INFO_NAMESPACE "device_info"

// Pin-Konfigurationsstruktur
struct PinConfiguration {
    // 28BYJ-48 Motor Pins
    int motor_28byj48_pin1;
    int motor_28byj48_pin2;
    int motor_28byj48_pin3;
    int motor_28byj48_pin4;
    
    // NEMA 23 Motor Pins (Advanced Motor)
    int nema23_step_pin;
    int nema23_dir_pin;
    int nema23_enable_pin;
    
    // Servo Pin
    int servo_pin;
    
    // LED Pin
    int led_pin;
    
    // Button Pin
    int button_pin;
    
    // WiFi Configuration
    char wifi_ssid[64];
    char wifi_password[64];
    char wifi_hostname[32];
    
    // Validierungs-Flag
    bool isValid;
};

// Globale Pin-Konfiguration
extern PinConfiguration currentPinConfig;

// Funktionsprototypen
void initPinConfig();
void loadPinConfig();
void savePinConfig();
void resetPinConfigToDefaults();
void applyPinConfig();
void setPinConfig(const PinConfiguration& config);
PinConfiguration getPinConfig();
void printPinConfig();

// Einzelne Pin-Setter
void set28BYJ48Pins(int pin1, int pin2, int pin3, int pin4);
void setNEMA23Pins(int stepPin, int dirPin, int enablePin);
void setServoPin(int pin);
void setLedPin(int pin);
void setButtonPin(int pin);
void setWiFiConfig(const char* ssid, const char* password, const char* hostname);

// Einzelne Pin-Getter
void get28BYJ48Pins(int* pin1, int* pin2, int* pin3, int* pin4);
void getNEMA23Pins(int* stepPin, int* dirPin, int* enablePin);
int getServoPin();
int getLedPin();
int getButtonPin();
void getWiFiConfig(char* ssid, char* password, char* hostname);

// Device Information Struktur
struct DeviceInfo {
    String deviceName;
    String deviceNumber;
    String configuration;
    String description;
};

// Device Information Funktionen
void initDeviceInfo();
void loadDeviceInfo();
void saveDeviceInfo();
DeviceInfo getDeviceInfo();
void setDeviceName(const char* name);
void setDeviceNumber(const char* number);
void setConfiguration(const char* config);
void setDescription(const char* desc);

#endif // PIN_CONFIG_H
