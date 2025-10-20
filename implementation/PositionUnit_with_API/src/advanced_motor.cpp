#include "advanced_motor.h"
#include "button_control.h"  // Für Button-Zustand
#include "relay_control.h"   // Für Relay-Steuerung

// Globale Instanz des erweiterten Motors
AdvancedStepperMotor advancedMotor(STEP_PIN, DIR_PIN, ENABLE_PIN, STEPS_PER_REVOLUTION);

// Konstruktor
AdvancedStepperMotor::AdvancedStepperMotor(int stepPin, int dirPin, int enablePin, int stepsPerRevolution)
    : stepPin(stepPin), dirPin(dirPin), enablePin(enablePin), stepsPerRevolution(stepsPerRevolution) {
    
    currentPosition = 0;
    targetPosition = 0;
    isMoving = false;
    isEnabled = false;
    isHomed = false;
    usePhysicalHome = true;        // Standard: Physisches Home mit Button
    isButtonHomingActive = false;  // Button-Homing-Modus initial deaktiviert
    
    // Row Counter Initialisierung
    isRowCounterActive = false;
    currentRows = 0;
    targetRows = 0;
    lastButtonState = true;        // true = nicht gedrückt (INPUT_PULLUP)
    rowCounterState = ROW_COUNTER_IDLE;
    
    // Motor Relay Control Initialisierung
    motorRelayControlEnabled = false;
    relayInverted = false;
    
    currentSpeedRPM = DEFAULT_SPEED_RPM;
    stepDelayMicros = 0;
    lastStepTime = 0;
    
    calculateStepDelay();
}

// Initialisierung
void AdvancedStepperMotor::begin() {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    
    if (enablePin >= 0) {
        pinMode(enablePin, OUTPUT);
        digitalWrite(enablePin, HIGH); // Normalerweise HIGH = disabled
    }
    
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
    
    Serial.println("Erweiterter Schrittmotor initialisiert");
    Serial.printf("Step Pin: %d, Dir Pin: %d, Enable Pin: %d\n", stepPin, dirPin, enablePin);
    Serial.printf("Schritte pro Umdrehung: %d\n", stepsPerRevolution);
}

// Motor aktivieren
void AdvancedStepperMotor::enable() {
    isEnabled = true;
    if (enablePin >= 0) {
        digitalWrite(enablePin, LOW); // LOW = enabled
    }
    Serial.println("Motor aktiviert");
}

// Motor deaktivieren
void AdvancedStepperMotor::disable() {
    isEnabled = false;
    isMoving = false;
    if (enablePin >= 0) {
        digitalWrite(enablePin, HIGH); // HIGH = disabled
    }
    setPinsIdle(); // Pins in Ruhezustand setzen
    Serial.println("Motor deaktiviert");
}

// Pins in Ruhezustand setzen (kein Strom)
void AdvancedStepperMotor::setPinsIdle() {
    digitalWrite(stepPin, LOW);  // STEP Pin auf LOW
    digitalWrite(dirPin, LOW);   // DIR Pin auf LOW
    Serial.println("Motor-Pins in Ruhezustand (LOW)");
}

// Geschwindigkeit setzen (RPM)
void AdvancedStepperMotor::setSpeed(int rpm) {
    rpm = constrain(rpm, 1, MAX_SPEED_RPM);
    currentSpeedRPM = rpm;
    calculateStepDelay();
    Serial.printf("Motor-Geschwindigkeit: %d RPM\n", rpm);
}

// Verzögerung zwischen Schritten berechnen
void AdvancedStepperMotor::calculateStepDelay() {
    // Berechnung: 60 Sekunden / (RPM * Schritte pro Umdrehung) = Sekunden pro Schritt
    // Dann in Mikrosekunden umwandeln und durch 2 teilen (für HIGH und LOW Phase)
    stepDelayMicros = (60000000L) / (currentSpeedRPM * stepsPerRevolution * 2);
}

// Richtung setzen
void AdvancedStepperMotor::setDirection(bool clockwise) {
    digitalWrite(dirPin, clockwise ? HIGH : LOW);
    delayMicroseconds(5); // Kurze Pause für Treiber
}

// Einzelner Schritt
void AdvancedStepperMotor::step() {
    if (!isEnabled) return;
    
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicros);
}

// Einzelnen Schritt ausführen (für non-blocking Bewegung)
void AdvancedStepperMotor::performStep() {
    if (!isEnabled) return;
    
    unsigned long currentTime = micros();
    if (currentTime - lastStepTime >= stepDelayMicros * 2) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2);
        digitalWrite(stepPin, LOW);
        lastStepTime = currentTime;
    }
}

// Bestimmte Anzahl von Schritten bewegen
void AdvancedStepperMotor::moveSteps(int steps) {
    if (steps == 0) return;
    
    // Motor automatisch aktivieren wenn eine Bewegung angefordert wird
    if (!isEnabled) {
        enable();
    }
    
    isMoving = true;
    
    // Relay-Steuerung beim Bewegungsstart
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
        } else {
            setRelayState(true);   // Relay ON wenn Motor läuft (normal)
        }
    }
    
    setDirection(steps > 0);
    
    int absSteps = abs(steps);
    Serial.printf("Bewege %d Schritte...\n", absSteps);
    
    for (int i = 0; i < absSteps; i++) {
        step();
    }
    
    currentPosition += steps;
    targetPosition = currentPosition;
    isMoving = false;
    
    // Relay-Steuerung beim Bewegungsende
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(true);   // Relay ON wenn Motor steht (inverted)
        } else {
            setRelayState(false);  // Relay OFF wenn Motor steht (normal)
        }
    }
    
    setPinsIdle(); // Pins in Ruhezustand setzen nach Bewegung
    Serial.printf("Bewegung abgeschlossen. Neue Position: %d\n", currentPosition);
}

// Zu absoluter Position bewegen
void AdvancedStepperMotor::moveTo(int position) {
    int stepsToMove = position - currentPosition;
    targetPosition = position;
    moveSteps(stepsToMove);
}

// Relative Bewegung
void AdvancedStepperMotor::moveRelative(int steps) {
    targetPosition = currentPosition + steps;
    moveSteps(steps);
}

// Bewegung in Grad
void AdvancedStepperMotor::moveDegrees(float degrees) {
    int steps = (int)((degrees / 360.0) * stepsPerRevolution);
    Serial.printf("Bewege %.1f Grad (%d Schritte)\n", degrees, steps);
    moveSteps(steps);
}

// Bewegung in Umdrehungen
void AdvancedStepperMotor::moveRevolutions(float revolutions) {
    int steps = (int)(revolutions * stepsPerRevolution);
    Serial.printf("Bewege %.2f Umdrehungen (%d Schritte)\n", revolutions, steps);
    moveSteps(steps);
}

// Bewegung mit Beschleunigung
void AdvancedStepperMotor::moveWithAcceleration(int steps, int startRPM, int endRPM) {
    if (!isEnabled || steps == 0) return;
    
    isMoving = true;
    setDirection(steps > 0);
    
    int absSteps = abs(steps);
    startRPM = constrain(startRPM, 1, MAX_SPEED_RPM);
    endRPM = constrain(endRPM, 1, MAX_SPEED_RPM);
    
    Serial.printf("Bewege %d Schritte mit Beschleunigung %d->%d RPM\n", absSteps, startRPM, endRPM);
    
    for (int i = 0; i < absSteps; i++) {
        // Linear interpolierte Geschwindigkeit
        int currentRPM = startRPM + ((endRPM - startRPM) * i) / absSteps;
        unsigned long currentDelay = (60000000L) / (currentRPM * stepsPerRevolution * 2);
        
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(currentDelay);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(currentDelay);
    }
    
    currentPosition += steps;
    targetPosition = currentPosition;
    isMoving = false;
    
    Serial.printf("Beschleunigte Bewegung abgeschlossen. Position: %d\n", currentPosition);
}

// Sanfte Bewegung mit S-Kurve
void AdvancedStepperMotor::moveSmoothly(int steps, int targetRPM) {
    if (!isEnabled || steps == 0) return;
    
    isMoving = true;
    setDirection(steps > 0);
    
    int absSteps = abs(steps);
    int accelSteps = min(ACCELERATION_STEPS, absSteps / 3);
    targetRPM = constrain(targetRPM, 1, MAX_SPEED_RPM);
    
    Serial.printf("Sanfte Bewegung: %d Schritte, Ziel: %d RPM\n", absSteps, targetRPM);
    
    for (int i = 0; i < absSteps; i++) {
        int currentRPM;
        
        if (i < accelSteps) {
            // Beschleunigungsphase
            currentRPM = map(i, 0, accelSteps, 10, targetRPM);
        } else if (i >= absSteps - accelSteps) {
            // Verzögerungsphase
            currentRPM = map(i, absSteps - accelSteps, absSteps, targetRPM, 10);
        } else {
            // Konstante Geschwindigkeit
            currentRPM = targetRPM;
        }
        
        unsigned long currentDelay = (60000000L) / (currentRPM * stepsPerRevolution * 2);
        
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(currentDelay);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(currentDelay);
    }
    
    currentPosition += steps;
    targetPosition = currentPosition;
    isMoving = false;
    
    Serial.printf("Sanfte Bewegung abgeschlossen. Position: %d\n", currentPosition);
}

// Kontinuierliches Jogging
void AdvancedStepperMotor::jogContinuous(bool direction, int rpm) {
    if (!isEnabled) return;
    
    setSpeed(rpm);
    setDirection(direction);
    isMoving = true;
    
    // Relay-Steuerung beim Jogging-Start
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
        } else {
            setRelayState(true);   // Relay ON wenn Motor läuft (normal)
        }
    }
    
    Serial.printf("Kontinuierliches Jogging gestartet. Richtung: %s, Geschwindigkeit: %d RPM\n", 
                  direction ? "vorwärts" : "rückwärts", rpm);
}

// Motor stoppen
void AdvancedStepperMotor::stop() {
    isMoving = false;
    targetPosition = currentPosition;
    
    // Relay-Steuerung beim Stoppen
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(true);   // Relay ON wenn Motor steht (inverted)
        } else {
            setRelayState(false);  // Relay OFF wenn Motor steht (normal)
        }
    }
    
    setPinsIdle(); // Pins in Ruhezustand setzen
    Serial.println("Motor gestoppt - Pins auf LOW");
}

// Notfall-Stopp
void AdvancedStepperMotor::emergencyStop() {
    stop();
    disable();
    Serial.println("NOTFALL-STOPP ausgeführt!");
}

// Home-Position anfahren
void AdvancedStepperMotor::home() {
    if (usePhysicalHome) {
        Serial.println("Fahre zur physischen Home-Position (bis Button gedrückt)...");
        startButtonHomingMode();
    } else {
        Serial.println("Fahre zur virtuellen Home-Position (Position 0)...");
        Serial.println("Verwende aktuelle Geschwindigkeit: " + String(currentSpeedRPM) + " RPM");
        moveTo(0);
        isHomed = true;
        Serial.println("Virtuelle Home-Position erreicht");
    }
}

// Aktuelle Position als Home setzen
void AdvancedStepperMotor::setHome() {
    currentPosition = 0;
    targetPosition = 0;
    isHomed = true;
    Serial.println("Aktuelle Position als Home-Position gesetzt");
}

// Motor kalibrieren
void AdvancedStepperMotor::calibrate() {
    Serial.println("Motor-Kalibrierung gestartet...");
    
    // Hier könnte eine Kalibrierungsroutine implementiert werden
    // z.B. Endschalter anfahren
    
    setHome();
    Serial.println("Motor-Kalibrierung abgeschlossen");
}



// Status-Funktionen
int AdvancedStepperMotor::getCurrentPosition() { return currentPosition; }
int AdvancedStepperMotor::getTargetPosition() { return targetPosition; }
bool AdvancedStepperMotor::getIsMoving() { return isMoving; }
bool AdvancedStepperMotor::getIsEnabled() { return isEnabled; }
bool AdvancedStepperMotor::getIsHomed() { return isHomed; }

int AdvancedStepperMotor::getCurrentSpeed() { return currentSpeedRPM; }

// Status-Struktur zurückgeben
AdvancedMotorStatus AdvancedStepperMotor::getStatus() {
    AdvancedMotorStatus status;
    status.currentPosition = currentPosition;
    status.targetPosition = targetPosition;
    status.isMoving = isMoving;
    status.currentSpeed = currentSpeedRPM;
    status.isHomed = isHomed;
    status.isEnabled = isEnabled;
    status.usePhysicalHome = usePhysicalHome;             // Homing-Modus hinzugefügt
    status.isButtonHomingActive = isButtonHomingActive;  // Neuer Status hinzugefügt
    status.isRowCounterActive = isRowCounterActive;      // Row Counter Status
    status.currentRows = currentRows;                    // Aktuelle Rows
    status.targetRows = targetRows;                      // Ziel-Rows

    status.lastMoveTime = millis();
    
    return status;
}

// Konfiguration
void AdvancedStepperMotor::setStepsPerRevolution(int steps) {
    stepsPerRevolution = steps;
    calculateStepDelay();
    Serial.printf("Schritte pro Umdrehung auf %d gesetzt\n", steps);
}

void AdvancedStepperMotor::setMicrostepping(int factor) {
    stepsPerRevolution = 200 * factor; // 200 ist Standard für NEMA17
    calculateStepDelay();
    Serial.printf("Microstepping auf 1/%d gesetzt (%d Schritte/Umdrehung)\n", factor, stepsPerRevolution);
}

// Non-blocking Bewegungen
void AdvancedStepperMotor::update() {
    // Row Counter Verarbeitung
    if (isRowCounterActive) {
        bool currentButtonState = getButtonState(); // true = nicht gedrückt
        bool buttonPressed = !currentButtonState;   // true = gedrückt
        
        // Edge Detection für Button-Zustandsänderungen
        bool buttonJustPressed = lastButtonState && !currentButtonState;  // Flanke von HIGH zu LOW
        
        // Zeit-Variable für alle cases verfügbar machen
        unsigned long currentTime = micros();
        
        switch (rowCounterState) {
            case ROW_COUNTER_MOVING:
                // Kontinuierliche Schritte in Fahrtrichtung
                if (currentTime - lastStepTime >= stepDelayMicros) {
                    digitalWrite(stepPin, HIGH);
                    delayMicroseconds(1);
                    digitalWrite(stepPin, LOW);
                    currentPosition++;
                    lastStepTime = currentTime;
                }
                
                // Prüfe ob Home-Button gedrückt wurde
                if (buttonJustPressed) {
                    currentRows++;
                    Serial.printf("Row %d von %d abgeschlossen (Button gedrückt)\n", currentRows, targetRows);
                    
                    if (currentRows >= targetRows) {
                        Serial.println("Ziel-Rows erreicht!");
                        stopRowCounter();
                    } else {
                        // Weiter fahren für nächste Row
                        Serial.println("Fahre weiter für nächste Row...");
                    }
                }
                break;
        }
        
        lastButtonState = currentButtonState;
        return; // Wenn Row Counter aktiv ist, andere Funktionen überspringen
    }
    
    // Button-Homing-Modus überwachen
    if (isButtonHomingActive) {
        // Prüfe Button-Zustand (getButtonState() gibt false zurück wenn Button gedrückt)
        bool buttonPressed = !getButtonState(); // Invertieren, da getButtonState() true = nicht gedrückt
        
        if (buttonPressed) {
            // Button wurde gedrückt - sofort stoppen
            Serial.println("Button gedrückt! Home-Position erreicht");
            stopButtonHomingMode();
        } else {
            // Button nicht gedrückt - weiter fahren mit aktueller Geschwindigkeit
            unsigned long currentTime = micros();
            if (currentTime - lastStepTime >= stepDelayMicros * 2) {
                // STEP Pin HIGH
                digitalWrite(stepPin, HIGH);
                // Minimaler Delay nur für saubere Flanke
                delayMicroseconds(1);
                // STEP Pin LOW
                digitalWrite(stepPin, LOW);
                
                // Position aktualisieren (Home-Fahrt = negative Richtung)
                currentPosition--;
                
                lastStepTime = currentTime;
            }
        }
    }
    
    // Weitere non-blocking Bewegungen können hier implementiert werden
}

// Homing-Modus setzen
void AdvancedStepperMotor::setUsePhysicalHome(bool usePhysical) {
    usePhysicalHome = usePhysical;
    Serial.println("Homing-Modus gesetzt auf: " + String(usePhysical ? "Physisches Home (Button)" : "Virtuelles Home (Position 0)"));
}

bool AdvancedStepperMotor::getUsePhysicalHome() {
    return usePhysicalHome;
}

// Button-Homing-Modus starten (fährt bis Button gedrückt wird)
void AdvancedStepperMotor::startButtonHomingMode() {
    Serial.println("Button-Homing-Modus gestartet - Motor fährt bis Button gedrückt wird");
    Serial.println("Verwende aktuelle Geschwindigkeit: " + String(currentSpeedRPM) + " RPM");
    isButtonHomingActive = true;
    isMoving = true;
    
    // Relay-Steuerung beim Homing-Start
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
        } else {
            setRelayState(true);   // Relay ON wenn Motor läuft (normal)
        }
    }
    
    // Sicherstellen, dass Step-Delay aktuell ist
    calculateStepDelay();
    // Richtung explizit setzen (gegen Uhrzeigersinn zum Home)
    setDirection(false); // Richtung Home (gegen Uhrzeigersinn angenommen)
    Serial.println("Step Delay: " + String(stepDelayMicros) + " Mikrosekunden");
}

// Button-Homing-Modus stoppen
void AdvancedStepperMotor::stopButtonHomingMode() {
    if (isButtonHomingActive) {
        Serial.println("Button-Homing-Modus gestoppt");
        isButtonHomingActive = false;
        stop();
        
        // Position auf Home setzen
        currentPosition = 0;
        isHomed = true;
        Serial.println("Home-Position erreicht und gesetzt.");
    }
}

void AdvancedStepperMotor::startNonBlockingMoveTo(int position) {
    targetPosition = position;
    // Implementation für non-blocking Bewegung
}

void AdvancedStepperMotor::startNonBlockingMoveSteps(int steps) {
    targetPosition = currentPosition + steps;
    // Implementation für non-blocking Bewegung
}

// Homing-Modus setzen/abfragen

// Row Counter Funktionen
bool AdvancedStepperMotor::startRowCounter(int targetRowCount) {
    if (!isHomed) {
        Serial.println("Motor muss erst gehomed werden");
        return false;
    }
    
    if (isRowCounterActive) {
        Serial.println("Row Counter bereits aktiv");
        return false;
    }
    
    if (targetRowCount <= 0 || targetRowCount > 1000) {
        Serial.println("Ungültige Row-Anzahl (1-1000)");
        return false;
    }
    
    Serial.printf("Row Counter initialisiert - Ziel: %d Rows\n", targetRowCount);
    isRowCounterActive = false; // Noch nicht aktiv, nur initialisiert
    currentRows = 0;
    targetRows = targetRowCount;
    lastButtonState = getButtonState();
    rowCounterState = ROW_COUNTER_IDLE;
    return true;
}

bool AdvancedStepperMotor::goRowCounter() {
    if (targetRows <= 0) {
        Serial.println("Row Counter nicht initialisiert - bitte zuerst 'Start Row Counter' drücken");
        return false;
    }
    
    if (isRowCounterActive) {
        Serial.println("Row Counter bereits aktiv");
        return false;
    }
    
    if (!isHomed) {
        Serial.println("Motor muss erst gehomed werden");
        return false;
    }
    
    Serial.printf("Row Counter gestartet - Ziel: %d Rows\n", targetRows);
    isRowCounterActive = true;
    currentRows = 0;
    lastButtonState = getButtonState();
    rowCounterState = ROW_COUNTER_MOVING;
    isMoving = true;
    
    // Relay-Steuerung beim Row Counter Start
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
        } else {
            setRelayState(true);   // Relay ON wenn Motor läuft (normal)
        }
    }
    
    // Geschwindigkeit wird von Web-Handler gesetzt (basierend auf User-Eingabe)
    // Keine feste Geschwindigkeit hier setzen
    
    // Richtung für Bewegung setzen (hier vorwärts)
    setDirection(true); // Uhrzeigersinn
    return true;
}

void AdvancedStepperMotor::stopRowCounter() {
    if (!isRowCounterActive) return;
    
    Serial.printf("Row Counter gestoppt - %d von %d Rows erreicht\n", currentRows, targetRows);
    isRowCounterActive = false;
    rowCounterState = ROW_COUNTER_IDLE;
    stop();
}

bool AdvancedStepperMotor::isRowCounterRunning() {
    return isRowCounterActive;
}

int AdvancedStepperMotor::getCurrentRows() {
    return currentRows;
}

int AdvancedStepperMotor::getTargetRows() {
    return targetRows;
}

// Motor Relay Control Funktionen
void AdvancedStepperMotor::setMotorRelayControl(bool enabled) {
    motorRelayControlEnabled = enabled;
    Serial.printf("Motor Relay Control: %s\n", enabled ? "Enabled" : "Disabled");
    
    // Wenn deaktiviert, Relay-Status auf aktuellen Motor-Status setzen
    if (!enabled && !isMoving) {
        // Relay entsprechend der Invert-Logik setzen
        if (relayInverted) {
            setRelayState(true);   // Relay ON wenn Motor AUS (inverted)
        } else {
            setRelayState(false);  // Relay OFF wenn Motor AUS (normal)
        }
    }
}

void AdvancedStepperMotor::setRelayInvert(bool inverted) {
    relayInverted = inverted;
    Serial.printf("Relay Logic: %s\n", inverted ? "Inverted" : "Normal");
    
    // Wenn Motor Relay Control aktiv ist, sofort anwenden
    if (motorRelayControlEnabled) {
        if (isMoving) {
            setRelayState(!inverted);  // Motor läuft: normal=ON, inverted=OFF
        } else {
            setRelayState(inverted);   // Motor steht: normal=OFF, inverted=ON
        }
    }
}

bool AdvancedStepperMotor::getMotorRelayControl() {
    return motorRelayControlEnabled;
}

bool AdvancedStepperMotor::getRelayInvert() {
    return relayInverted;
}


// Setup-Funktion
void setupAdvancedMotor() {
    advancedMotor.begin();
    advancedMotor.enable();
    Serial.println("Erweiterter Motor setup abgeschlossen");
}

// Update-Funktion für main loop
void updateMotor() {
    advancedMotor.update();
}