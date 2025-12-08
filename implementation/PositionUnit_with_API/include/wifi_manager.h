#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include "led_control.h"

// Network Configuration - werden aus EEPROM geladen
extern char current_ssid[64];
extern char current_password[64];
extern char current_hostname[32];

void setupWiFi();
void checkWiFiConnection();
void printNetworkStatus();

#endif // WIFI_MANAGER_H