#include "advanced_motor.h"
#include "button_control.h"  // For button state
#include "relay_control.h"   // For relay control

// Global instance of the advanced motor
AdvancedStepperMotor advancedMotor(STEP_PIN, DIR_PIN, ENABLE_PIN, STEPS_PER_REVOLUTION);

// Konstruktor
AdvancedStepperMotor::AdvancedStepperMotor(int stepPin, int dirPin, int enablePin, int stepsPerRevolution)
    : stepPin(stepPin), dirPin(dirPin), enablePin(enablePin), stepsPerRevolution(stepsPerRevolution) {
    
    currentPosition = 0;
    targetPosition = 0;
    isMoving = false;
    isEnabled = false;
    isHomed = false;
    usePhysicalHome = true;        // Default: Physical home with button
    isButtonHomingActive = false;  // Button homing mode initially disabled
    
    // Row Counter Initialization
    isRowCounterActive = false;
    currentRows = 0;
    targetRows = 0;
    lastButtonState = true;        // true = not pressed (INPUT_PULLUP)
    rowCounterState = ROW_COUNTER_IDLE;
    
    // Motor Relay Control Initialization
    motorRelayControlEnabled = false;
    relayInverted = false;
    
    // Chunked Movement Initialisierung
    isChunkedMovementActive = false;
    remainingSteps = 0;
    movementDirection = true;
    chunkSize = 50;              // Standard: 50 Schritte pro Chunk
    lastChunkTime = 0;
    chunkDelayMs = 10;           // Standard: 10ms Pause zwischen Chunks
    
    // Echtzeit-Update System Initialisierung
    lastRealtimeUpdateTime = 0;
    realtimeUpdateInterval = 5;  // Standard: 5ms Echtzeit-Updates
    
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
    Serial.println("Motor enabled");
}

// Disable motor
void AdvancedStepperMotor::disable() {
    isEnabled = false;
    isMoving = false;
    if (enablePin >= 0) {
        digitalWrite(enablePin, HIGH); // HIGH = disabled
    }
    setPinsIdle(); // Set pins to idle state
    Serial.println("Motor disabled");
}

// Set pins to idle state (no current)
void AdvancedStepperMotor::setPinsIdle() {
    digitalWrite(stepPin, LOW);  // STEP pin to LOW
    digitalWrite(dirPin, LOW);   // DIR Pin auf LOW
    Serial.println("Motor-Pins in Ruhezustand (LOW)");
}

// Geschwindigkeit setzen (RPM)
void AdvancedStepperMotor::setSpeed(int rpm) {
    rpm = constrain(rpm, 1, MAX_SPEED_RPM);
    currentSpeedRPM = rpm;
    calculateStepDelay();
    Serial.printf("Motor speed: %d RPM\n", rpm);
}

// Calculate delay between steps
void AdvancedStepperMotor::calculateStepDelay() {
    // Calculation: 60 seconds / (RPM * steps per revolution) = seconds per step
    // Then convert to microseconds and divide by 2 (for HIGH and LOW phase)
    stepDelayMicros = (60000000L) / (currentSpeedRPM * stepsPerRevolution * 2);
}

// Set direction
void AdvancedStepperMotor::setDirection(bool clockwise) {
    digitalWrite(dirPin, clockwise ? HIGH : LOW);
    delayMicroseconds(5); // Short pause for driver
}

// Single step
void AdvancedStepperMotor::step() {
    if (!isEnabled) return;
    
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicros);
}

// Execute single step (for non-blocking movement)
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
    
    // Relay control at movement start
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF when motor runs (inverted)
        } else {
            setRelayState(true);   // Relay ON when motor runs (normal)
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

// CHUNKED MOVEMENT FUNCTIONS (Interruptible large movements)
void AdvancedStepperMotor::moveStepsChunked(int steps, int chunkSize, int delayMs) {
    if (steps == 0) return;
    
    // Automatically enable motor when movement is requested
    if (!isEnabled) {
        enable();
    }
    
    // Stoppe vorherige chunked Bewegung falls aktiv
    if (isChunkedMovementActive) {
        stopChunkedMovement();
    }
    
    isChunkedMovementActive = true;
    remainingSteps = abs(steps);
    movementDirection = (steps > 0);
    this->chunkSize = chunkSize;
    this->chunkDelayMs = delayMs;
    lastChunkTime = 0;
    targetPosition = currentPosition + steps;
    
    // Relay-Steuerung beim Bewegungsstart
    if (motorRelayControlEnabled) {
        if (relayInverted) {
            setRelayState(false);  // Relay OFF when motor runs (inverted)
        } else {
            setRelayState(true);   // Relay ON when motor runs (normal)
        }
    }
    
    Serial.printf("Starting chunked movement: %d steps, chunk size: %d, delay: %dms\n", 
                  remainingSteps, chunkSize, delayMs);
}

void AdvancedStepperMotor::moveToChunked(int position, int chunkSize, int delayMs) {
    int stepsToMove = position - currentPosition;
    moveStepsChunked(stepsToMove, chunkSize, delayMs);
}

void AdvancedStepperMotor::moveRelativeChunked(int steps, int chunkSize, int delayMs) {
    moveStepsChunked(steps, chunkSize, delayMs);
}

bool AdvancedStepperMotor::isChunkedMovementRunning() {
    return isChunkedMovementActive;
}

void AdvancedStepperMotor::stopChunkedMovement() {
    if (isChunkedMovementActive) {
        isChunkedMovementActive = false;
        remainingSteps = 0;
        targetPosition = currentPosition;
        
        // Relay-Steuerung beim Stoppen
        if (motorRelayControlEnabled) {
            if (relayInverted) {
                setRelayState(true);   // Relay ON wenn Motor steht (inverted)
            } else {
                setRelayState(false);  // Relay OFF wenn Motor steht (normal)
            }
        }
        
        Serial.printf("Chunked movement stopped at position: %d\n", currentPosition);
    }
}

void AdvancedStepperMotor::setChunkParameters(int chunkSize, int delayMs) {
    this->chunkSize = chunkSize;
    this->chunkDelayMs = delayMs;
    Serial.printf("Chunk parameters set: size=%d, delay=%dms\n", chunkSize, delayMs);
}

// Movement with acceleration
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
    
    // Chunked Movement stoppen falls aktiv
    if (isChunkedMovementActive) {
        isChunkedMovementActive = false;
        remainingSteps = 0;
    }
    
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

// Move to home position
void AdvancedStepperMotor::home() {
    if (usePhysicalHome) {
        Serial.println("Moving to physical home position (until button pressed)...");
        startButtonHomingMode();
    } else {
        Serial.println("Moving to virtual home position (position 0)...");
        Serial.println("Using current speed: " + String(currentSpeedRPM) + " RPM");
        moveTo(0);
        isHomed = true;
        Serial.println("Virtual home position reached");
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
    unsigned long currentTime = millis();
    
    // Chunked Movement Verarbeitung
    if (isChunkedMovementActive && remainingSteps > 0) {
        // Prüfe ob genug Zeit seit dem letzten Chunk vergangen ist
        if (currentTime - lastChunkTime >= chunkDelayMs) {
            // Berechne die Schritte für diesen Chunk
            int stepsThisChunk = min(remainingSteps, chunkSize);
            
            // IMPORTANT: Check relay control BEFORE each chunk
            // Falls Motor Control with Relay während der Bewegung geändert wurde
            if (motorRelayControlEnabled) {
                if (relayInverted) {
                    setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
                } else {
                    setRelayState(true);   // Relay ON wenn Motor läuft (normal)
                }
            }
            
            // Führe den Chunk aus (blockierend, aber nur für wenige Schritte)
            isMoving = true;
            setDirection(movementDirection);
            
            for (int i = 0; i < stepsThisChunk; i++) {
                step();
                if (movementDirection) {
                    currentPosition++;
                } else {
                    currentPosition--;
                }
            }
            
            remainingSteps -= stepsThisChunk;
            lastChunkTime = currentTime;
            
            Serial.printf("Chunk ausgeführt: %d Schritte, verbleibend: %d, Position: %d\n", 
                         stepsThisChunk, remainingSteps, currentPosition);
            
            // Prüfen ob Bewegung abgeschlossen
            if (remainingSteps <= 0) {
                isChunkedMovementActive = false;
                isMoving = false;
                targetPosition = currentPosition;
                
                // Relay-Steuerung beim Bewegungsende
                if (motorRelayControlEnabled) {
                    if (relayInverted) {
                        setRelayState(true);   // Relay ON wenn Motor steht (inverted)
                    } else {
                        setRelayState(false);  // Relay OFF wenn Motor steht (normal)
                    }
                }
                
                setPinsIdle();
                Serial.printf("Chunked Bewegung abgeschlossen. Endposition: %d\n", currentPosition);
            } else {
                // IMPORTANT: Check relay control AFTER each chunk 
                // Falls Motor Control with Relay während der Bewegung ausgeschaltet wurde
                if (!motorRelayControlEnabled) {
                    // Benutzer hat Motor Relay Control ausgeschaltet, Relay-Zustand nicht automatisch ändern
                    Serial.println("Motor Relay Control disabled - Relay remains in manual mode");
                }
            }
        }
    }
    
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
                
                // Check if home button was pressed
                if (buttonJustPressed) {
                    currentRows++;
                    Serial.printf("Row %d of %d completed (button pressed)\n", currentRows, targetRows);
                    
                    if (currentRows >= targetRows) {
                        Serial.println("Target rows reached!");
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
    
    // Monitor button homing mode
    if (isButtonHomingActive) {
        // Check button state (getButtonState() returns false when button pressed)
        bool buttonPressed = !getButtonState(); // Invert, since getButtonState() true = not pressed
        
        if (buttonPressed) {
            // Button was pressed - stop immediately
            Serial.println("Button pressed! Home position reached");
            stopButtonHomingMode();
        } else {
            // Button not pressed - continue moving at current speed
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

// Start button homing mode (moves until button pressed)
void AdvancedStepperMotor::startButtonHomingMode() {
    Serial.println("Button homing mode started - motor moves until button pressed");
    Serial.println("Using current speed: " + String(currentSpeedRPM) + " RPM");
    isButtonHomingActive = true;
    isMoving = true;
    
    // Relay control at homing start
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

// Stop button homing mode
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

// Echtzeit-Update System Funktionen
void AdvancedStepperMotor::setRealtimeUpdateInterval(unsigned long intervalMs) {
    realtimeUpdateInterval = intervalMs;
    Serial.printf("Motor Echtzeit-Update Intervall auf %lums gesetzt\n", intervalMs);
}

void AdvancedStepperMotor::forceRealtimeUpdate() {
    Serial.println("Erzwinge Motor Echtzeit-Update...");
    updateRealtimeComponents();
}

void AdvancedStepperMotor::updateRealtimeComponents() {
    unsigned long currentTime = millis();
    
    // Prüfe ob Update-Intervall erreicht wurde
    if (currentTime - lastRealtimeUpdateTime >= realtimeUpdateInterval) {
        // Motor-Relay-Control Echtzeit-Prüfung
        if (isMoving || isChunkedMovementActive) {
            // Motor läuft - prüfe Relay-Einstellungen
            if (motorRelayControlEnabled) {
                if (relayInverted) {
                    setRelayState(false);  // Relay OFF wenn Motor läuft (inverted)
                } else {
                    setRelayState(true);   // Relay ON wenn Motor läuft (normal)
                }
            }
        } else {
            // Motor steht - prüfe Relay-Einstellungen  
            if (motorRelayControlEnabled) {
                if (relayInverted) {
                    setRelayState(true);   // Relay ON wenn Motor steht (inverted)
                } else {
                    setRelayState(false);  // Relay OFF wenn Motor steht (normal)
                }
            }
        }
        
        lastRealtimeUpdateTime = currentTime;
    }
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