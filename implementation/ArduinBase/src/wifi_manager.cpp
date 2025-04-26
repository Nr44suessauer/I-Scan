#include "wifi_manager.h"

// Netzwerk-Konfiguration
const char* SSID = "Teekanne";
const char* PASSWORD = "49127983361694305550";

void setupWiFi() {
  Serial.print("Verbindung mit WLAN wird hergestellt: ");
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
    Serial.println("WLAN-Verbindung verloren. Versuche Wiederverbindung...");
    setColorByIndex(0);  // Rot für Verbindungsverlust
    
    WiFi.begin(SSID, PASSWORD);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    
    Serial.println();
    printNetworkStatus();
    
    setColorByIndex(1);  // Grün für erfolgreiche Wiederverbindung
  }
}

void printNetworkStatus() {
  Serial.print("Verbunden mit: ");
  Serial.println(WiFi.SSID());
  Serial.print("Lokale IP: ");
  Serial.println(WiFi.localIP());
}