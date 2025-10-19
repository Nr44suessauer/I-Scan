#include "wifi_manager.h"

// Network configuration
const char* SSID = "Teekanne";
const char* PASSWORD = "49127983361694305550";

void setupWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(SSID);
  
  WiFi.begin(SSID, PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println();
  printNetworkStatus();
}

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connection lost. Attempting reconnection...");
    setColorByIndex(0);  // Red for connection loss
    
    WiFi.begin(SSID, PASSWORD);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    
    Serial.println();
    printNetworkStatus();
    
    setColorByIndex(1);  // Green for successful reconnection
  }
}

void printNetworkStatus() {
  Serial.print("Connected to: ");
  Serial.println(WiFi.SSID());
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
}