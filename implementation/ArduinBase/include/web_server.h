#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <Arduino.h>
#include <WebServer.h>
#include "led_control.h"

extern const uint16_t HTTP_PORT;
extern WebServer server;

void setupWebServer();
void handleWebServerRequests();

// Handler für verschiedene Routen
void handleRoot();
void handleColorChange();
void handleHexColorChange();
void handleNotFound();

#endif // WEB_SERVER_H