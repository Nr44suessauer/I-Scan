#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include "led_control.h"

// Network Configuration
extern const char* SSID;
extern const char* PASSWORD;

void setupWiFi();
void checkWiFiConnection();
void printNetworkStatus();

#endif // WIFI_MANAGER_H