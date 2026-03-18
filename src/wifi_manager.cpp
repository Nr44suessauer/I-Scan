#include "wifi_manager.h"
#include "pin_config.h"

// Netzwerk-Konfiguration - wird aus EEPROM geladen
char current_ssid[64] = "Teekanne";
char current_password[64] = "49127983361694305550";
char current_hostname[32] = "ESP32-IScan";

void setupWiFi() {
  // Lade WiFi-Konfiguration aus EEPROM
  getWiFiConfig(current_ssid, current_password, current_hostname);
  
  // Setze Hostname
  WiFi.setHostname(current_hostname);
  
  Serial.print("Verbindung mit WLAN wird hergestellt: ");
  Serial.println(current_ssid);
  Serial.print("Hostname: ");
  Serial.println(current_hostname);
  
  WiFi.begin(current_ssid, current_password);
  
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
    
    WiFi.begin(current_ssid, current_password);
    
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