# PositionUnit_with_API - Feature- und Architekturbericht

## 1. Ziel der Software

Die Firmware steuert eine ESP32-S3 Positionseinheit mit Web-UI und REST-API.
Sie verbindet mehrere Aktoren/Sensoren in einer gemeinsamen Steueroberflaeche:

- NEMA23 (Advanced Stepper), bis zu 3 Motorinstanzen
- 28BYJ-48 Stepper
- Servo, bis zu 3 Kanaele
- LED (NeoPixel), bis zu 3 Outputs mit jeweils konfigurierbarer LED-Anzahl
- Button-Eingang

Wichtige Eigenschaft: Pin- und Systemkonfiguration werden persistent gespeichert (Preferences/NVS), damit Einstellungen Neustarts ueberstehen.

---

## 2. Hauptfeatures

## 2.1 Multi-Instanz Steuerung

- `motorId` fuer NEMA23-Endpunkte (1..3)
- `servoId` fuer Servo-Endpunkte (1..3)
- `ledId` fuer LED-Endpunkte (1..3)

Dadurch koennen mehrere gleichartige Aktoren unabhaengig konfiguriert und angesprochen werden.

## 2.2 Persistente Konfiguration

Gespeichert werden unter anderem:

- NEMA23: `STEP/DIR/EN` je Motorinstanz
- Servo: Pin je Servokanal
- LED: Pin + Count je LED-Output
- 28BYJ-48: 4 Steuerpins
- Button-Pin
- WiFi (SSID, Passwort, Hostname)
- Device-Info (Name, Nummer, Konfiguration, Beschreibung)

Die Daten liegen im NVS und werden beim Boot geladen und auf die Module angewendet.

## 2.3 Web-UI mit Tabs

Die Bedienung erfolgt ueber eine eingebettete HTML/JS-Oberflaeche in `src/web_server.cpp`.

Tabs:

- Motor Control
- 28BYJ-48 Motor
- Servo Control
- LED Control
- Info (Button)
- Status & Info

## 2.4 API-First Design

Alle UI-Aktionen rufen REST-Endpunkte auf. Das erlaubt:

- Browser-Steuerung
- API-Tests via Notebook/Postman
- externe Integrationen

## 2.5 Pinout-UX

- Pin-Felder wurden auf Dropdown-Selektoren umgestellt
- nicht verfuegbare Pins sind visuell kenntlich gemacht
- einklappbare Pinout-Bilder in Pin-Zuweisungsbereichen
- Pinout-Bild ist zoombar (Modal mit Mausradzoom)

## 2.6 Stabilitaetsverbesserungen

- Schutz gegen ungueltige Pins bei kritischen Modulen
- Setup-Reihenfolge verbessert (Servo-Initialisierung spaet im Boot), damit gespeicherte Servopins nach Neustart aktiv bleiben
- serielle Ausgabe auf konsistent 115200

---

## 3. Softwareaufbau

## 3.1 Dateistruktur (Kernmodule)

- `src/main.cpp`: Bootstrapping und Hauptloop
- `src/web_server.cpp`: UI + HTTP-Routing + API-Handler
- `src/pin_config.cpp`: Persistenz und Konfigmodell (NVS)
- `src/servo_control.cpp`: Mehrkanal-Servo (LEDC)
- `src/advanced_motor.cpp`: NEMA23-Steuerung (multi-instance)
- `src/led_control.cpp`: NeoPixel-Outputs (runtime-konfigurierbar)
- `src/motor_28byj48.cpp`: 28BYJ-48 Logik
- `src/button_control.cpp`: Button-Handling
- `src/wifi_manager.cpp`: WiFi-Verbindung und Reconnect

## 3.2 Boot- und Laufzeitfluss

```text
Power On / Reset
   |
   v
main.cpp::setup()
   |
   +--> initPinConfig()
   |      +--> loadPinConfig() aus NVS
   |      +--> sanitize/apply auf globale Modulpins
   |
   +--> initDeviceInfo()
   +--> setupLEDs()
   +--> setupMotor() / setupAdvancedMotor() / setup28BYJ48Motor()
   +--> setupButton()
   +--> setupServo()   (spaet, damit finaler Servo-Pin gewinnt)
   +--> setupWiFi()
   +--> setupWebServer()
   |
   v
main.cpp::loop()
   +--> handleWebServerRequests()
   +--> updateMotor()
   +--> getButtonState()
   +--> checkWiFiConnection()
```

## 3.3 API-Verarbeitung

```text
Browser UI Action
   |
   v
fetch('/savePinConfig', ...)
   |
   v
web_server.cpp::handleSavePinConfig()
   |
   +--> setXxxPinById(...)
   |      +--> pin_config.cpp::savePinConfig()  --> NVS write
   |
   +--> reconfigure/setup module runtime
   |
   v
HTTP Response an UI
```

## 3.4 Persistenzmodell

```text
NVS namespace: pin_config

  m28_p1..m28_p4
  nema1_stp/dir/en, nema2_..., nema3_...
  servo1_p, servo2_p, servo3_p
  led1_p, led2_p, led3_p
  led1_c, led2_c, led3_c
  btn_p
  wifi_ssid, wifi_pass, wifi_host
  valid

NVS namespace: device_info

  deviceName
  deviceNumber
  configuration
  description
```

## 3.5 Modulbeziehungen

```text
                 +---------------------+
                 |     web_server      |
                 |  UI + REST API      |
                 +----------+----------+
                            |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
 +-------------+    +---------------+    +-------------+
 | pin_config  |    | servo_control |    | led_control |
 | NVS model   |    | LEDC channels |    | NeoPixel    |
 +------+------+    +-------+-------+    +------+------+ 
        |                   |                   |
        |                   |                   |
        v                   v                   v
 +-------------+    +---------------+    +-------------+
 | advanced_   |    | motor_28byj48 |    | button_     |
 | motor       |    | step sequence |    | control     |
 +------+------+    +---------------+    +-------------+
        |
        v
 +-------------+
 | wifi_manager|
 +-------------+
```

---

## 4. Wichtige Endpunkte (Auszug)

Steuerung:

- `GET /setServo?servoId=<1..3>&angle=<0..180>`
- `GET /advancedMotor?...&motorId=<1..3>`
- `GET /color?ledId=<1..3>&index=<...>`
- `GET /hexcolor?ledId=<1..3>&hex=<RRGGBB>`
- `GET /setBrightness?ledId=<1..3>&value=<0..255>`

Konfiguration:

- `GET /pinConfig`
- `POST /savePinConfig`
- `GET /resetPinConfig`
- `POST /saveWiFiConfig`

Infos:

- `GET /systemInfo`
- `GET /getDeviceInfo`
- `GET /setDeviceInfo?...`

---

## 5. Aktueller Stand der Implementierung

- Multi-Servo: umgesetzt
- Multi-LED mit Count je Output: umgesetzt
- Multi-NEMA23: umgesetzt
- Pinout-basierte UI-Hilfen: umgesetzt
- Zoombares Pinout-Bild: umgesetzt
- EEPROM/NVS Persistenz fuer Pin- und Geraetedaten: umgesetzt
- Bootstabilitaet und Initialisierungsreihenfolge verbessert: umgesetzt

---

## 6. Betrieb und Entwicklung

## 6.1 Build/Upload

Environment: `esp32-s3-devkitm-1`

Typische Befehle:

```text
platformio run --environment esp32-s3-devkitm-1
platformio run --target upload --environment esp32-s3-devkitm-1
platformio device monitor --port COM4 --baud 115200 --filter direct
```

## 6.2 Hinweise fuer den Einsatz

- Bei Pinwechseln immer auf reale Verdrahtung achten
- Save+Apply schreibt Konfiguration persistent
- Nach Reboot werden gespeicherte Werte automatisch geladen

---

## 7. Zusammenfassung

Die Software ist als modulare, API-getriebene Embedded-Steuerung aufgebaut.
Kernstaerken sind Multi-Instanz-Faehigkeit, persistente Konfiguration und eine umfangreiche Web-UI.
Durch die aktuelle Struktur lassen sich neue Komponenten, Endpunkte und Validierungsregeln gezielt erweitern, ohne die Gesamtsystemlogik grundlegend zu aendern.
