#include "advanced_motor.h"
#include "button_control.h"  // Für Button-Status Abfrage

// Globale Debug-Variable
bool motorDebugEnabled = false;  // Standardmäßig ausgeschaltet

// Globale Instanz
AdvancedStepperMotor advancedMotor(STEP_PIN, DIR_PIN, ENABLE_PIN, ADVANCED_STEPS_PER_REVOLUTION);

// Konstruktor
AdvancedStepperMotor::AdvancedStepperMotor(int stepPin, int dirPin, int enablePin, int stepsPerRevolution)
    : stepPin(stepPin), dirPin(dirPin), enablePin(enablePin), stepsPerRevolution(stepsPerRevolution) {
    currentPosition = 0;
    targetPosition = 0;
    virtualHomePosition = 0; // Initialisiere virtuelle Home-Position
    isMoving = false;
    isEnabled = false;
    isHomed = false;
    currentSpeedRPM = DEFAULT_SPEED_RPM;
    stepDelayMicros = 0;
    lastStepTime = 0;
    targetPassCount = 0;
    currentPassCount = 0;
    isPassingButton = false;
    calculateStepDelay();
}

void AdvancedStepperMotor::begin() {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    if (enablePin >= 0) {
        pinMode(enablePin, OUTPUT);
        digitalWrite(enablePin, HIGH);
    }
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
    enable();
    MOTOR_DEBUG_PRINTLN("Erweiterter Motor initialisiert");
}

void AdvancedStepperMotor::enable() {
    if (enablePin >= 0) digitalWrite(enablePin, LOW);
    isEnabled = true;
}

void AdvancedStepperMotor::disable() {
    if (enablePin >= 0) digitalWrite(enablePin, HIGH);
    isEnabled = false;
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::setPinsIdle() {
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
}

void AdvancedStepperMotor::setSpeed(int rpm) {
    rpm = constrain(rpm, 1, MAX_SPEED_RPM);
    currentSpeedRPM = rpm;
    calculateStepDelay();
    MOTOR_DEBUG_PRINTF("Motor-Geschwindigkeit: %d RPM\n", rpm);
}

void AdvancedStepperMotor::calculateStepDelay() {
    stepDelayMicros = (60000000L) / (currentSpeedRPM * stepsPerRevolution * 2);
}

void AdvancedStepperMotor::setDirection(bool clockwise) {
    digitalWrite(dirPin, clockwise ? HIGH : LOW);
    delayMicroseconds(5);
}

void AdvancedStepperMotor::step() {
    if (!isEnabled) return;
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayMicros);
}

void AdvancedStepperMotor::moveSteps(int steps) {
    if (!isEnabled || steps == 0) return;
    isMoving = true;
    setDirection(steps > 0);
    int absSteps = abs(steps);
    for (int i = 0; i < absSteps; i++) {
        step();
    }
    currentPosition += steps;
    targetPosition = currentPosition;
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::moveTo(int position) {
    moveSteps(position - currentPosition);
}

void AdvancedStepperMotor::moveRelative(int steps) {
    moveSteps(steps);
}

void AdvancedStepperMotor::stop() {
    isMoving = false;
    setPinsIdle();
}

void AdvancedStepperMotor::setHome() {
    currentPosition = 0;
    targetPosition = 0;
    isHomed = true;
}

void AdvancedStepperMotor::homeToButton() {
    if (!isEnabled) {
        MOTOR_DEBUG_PRINTLN("Motor ist deaktiviert - Home-Fahrt abgebrochen");
        return;
    }
    
    MOTOR_DEBUG_PRINTLN("Starte Home-Fahrt zum Button mit aktueller Geschwindigkeit: " + String(currentSpeedRPM) + " RPM");
    MOTOR_DEBUG_PRINTLN("Aktueller Button-Status: " + String(getButtonState() == HIGH ? "HIGH (nicht gedrückt)" : "LOW (gedrückt)"));
    MOTOR_DEBUG_PRINTLN("Aktuelle Motor-Position: " + String(currentPosition));
    
    // Prüfe ob Button bereits gedrückt ist
    if (getButtonState() == LOW) {
        MOTOR_DEBUG_PRINTLN("Button ist bereits gedrückt - setze aktuelle Position als Home");
        currentPosition = 0;
        targetPosition = 0;
        isHomed = true;
        return;
    }
    
    // Übernehme aktuelle Parameter vom Slider (Geschwindigkeit ist bereits gesetzt)
    // Weitere Parameter können hier hinzugefügt werden, falls nötig
    
    // Fahre in Richtung Button (negative Richtung angenommen)
    // Der Button fungiert als Home-Endschalter
    isMoving = true;
    setDirection(false);  // Fahre in negative Richtung zum Button
    
    int stepCount = 0;
    int maxSteps = 10000;  // Sicherheits-Maximum, um Endlos-Fahrt zu vermeiden
    
    MOTOR_DEBUG_PRINTLN("Beginne Fahrt in negative Richtung...");
    
    // Fahre bis Button gedrückt wird oder Maximum erreicht ist
    while (getButtonState() == HIGH && stepCount < maxSteps && isMoving) {
        // Button nicht gedrückt (HIGH = nicht gedrückt bei INPUT_PULLUP)
        step();
        currentPosition++;  // Position wird dekrementiert bei negativer Fahrt
        stepCount++;
        
        // Kurze Pause für Button-Abfrage und Debug-Ausgabe
        if (stepCount % 30 == 0) {
            MOTOR_DEBUG_PRINTLN("Schritte: " + String(stepCount) + ", Button-Status: " + String(getButtonState() == HIGH ? "HIGH" : "LOW") + ", Position: " + String(currentPosition));
            delay(1);  // Etwas längere Pause für Button-Abfrage
        }
    }
    
    // Prüfe Ergebnis
    if (getButtonState() == LOW) {
        // Button wurde gedrückt (LOW = gedrückt bei INPUT_PULLUP)
        MOTOR_DEBUG_PRINTLN("Home-Position am Button erreicht nach " + String(stepCount) + " Schritten");
        currentPosition = 0;  // Setze aktuelle Position als Home (0)
        targetPosition = 0;
        isHomed = true;
        MOTOR_DEBUG_PRINTLN("Motor erfolgreich gehomed - neue Home-Position gesetzt");
    } else if (stepCount >= maxSteps) {
        MOTOR_DEBUG_PRINTLN("WARNUNG: Maximale Schrittanzahl erreicht - Button nicht gefunden!");
        MOTOR_DEBUG_PRINTLN("Möglicherweise ist der Button defekt oder die Fahrtrichtung falsch");
        MOTOR_DEBUG_PRINTLN("Aktueller Button-Status: " + String(getButtonState() == HIGH ? "HIGH (nicht gedrückt)" : "LOW (gedrückt)"));
    } else if (!isMoving) {
        MOTOR_DEBUG_PRINTLN("Home-Fahrt wurde gestoppt");
    }
    
    isMoving = false;
    setPinsIdle();
    MOTOR_DEBUG_PRINTLN("Home-Fahrt beendet. Aktuelle Position: " + String(currentPosition));
}

void AdvancedStepperMotor::passButtonTimes(int count) {
    if (!isEnabled) {
        MOTOR_DEBUG_PRINTLN("Motor ist deaktiviert - Button-Pass-Fahrt abgebrochen");
        return;
    }
    
    if (count <= 0) {
        MOTOR_DEBUG_PRINTLN("Ungültige Anzahl: " + String(count) + " - Button-Pass-Fahrt abgebrochen");
        return;
    }
    
    // Initialisiere Pass-Variablen
    targetPassCount = count;
    currentPassCount = 0;
    isPassingButton = true;
    
    MOTOR_DEBUG_PRINTLN("Starte Button-Pass-Fahrt: Button soll " + String(count) + " mal passiert werden");
    MOTOR_DEBUG_PRINTLN("Geschwindigkeit: " + String(currentSpeedRPM) + " RPM");
    MOTOR_DEBUG_PRINTLN("Aktueller Button-Status: " + String(getButtonState() == HIGH ? "HIGH (nicht gedrückt)" : "LOW (gedrückt)"));
    MOTOR_DEBUG_PRINTLN("Start-Position: " + String(currentPosition));
    
    isMoving = true;
    setDirection(false);  // Fahre in negative Richtung (gleiche Richtung wie homeToButton)
    
    int passedCount = 0;
    int stepCount = 0;
    // maxSteps entfernt - keine Schrittbegrenzung mehr
    bool lastButtonState = (getButtonState() == LOW);  // true wenn Button gedrückt
    bool currentButtonState;
    
    MOTOR_DEBUG_PRINTLN("Beginne Fahrt - Ziel: " + String(count) + " Button-Passagen (keine Schrittbegrenzung)");
    
    // Fahre bis die gewünschte Anzahl von Button-Passagen erreicht ist
    while (passedCount < count && isMoving) {
        // Einen Schritt machen
        step();
        currentPosition--;  // Position wird dekrementiert bei negativer Fahrt
        stepCount++;
        
        // Button-Status prüfen
        currentButtonState = (getButtonState() == LOW);
        
        // Prüfe auf Flanke: von nicht-gedrückt zu gedrückt (steigende Flanke der Passage)
        if (!lastButtonState && currentButtonState) {
            passedCount++;
            currentPassCount = passedCount; // Aktualisiere die Klassenvariable
            MOTOR_DEBUG_PRINTLN("Button-Passage " + String(passedCount) + " von " + String(count) + 
                              " bei Schritt " + String(stepCount) + ", Position: " + String(currentPosition));
            

        }
        
        lastButtonState = currentButtonState;
        
        // Debug-Ausgabe alle 50 Schritte für besseres Feedback
        if (stepCount % 50 == 0) {
            MOTOR_DEBUG_PRINTLN("Schritte: " + String(stepCount) + 
                              ", Passagen: " + String(passedCount) + "/" + String(count) + 
                              ", Button: " + String(getButtonState() == HIGH ? "HIGH" : "LOW") + 
                              ", Position: " + String(currentPosition));
            delay(5);  // Etwas längere Pause für UI-Update-Möglichkeit
        }
    }
    
    // Ergebnis auswerten
    if (passedCount >= count) {
        MOTOR_DEBUG_PRINTLN("ERFOLG: Button wurde " + String(passedCount) + " mal passiert");
        MOTOR_DEBUG_PRINTLN("Benötigte Schritte: " + String(stepCount));
        MOTOR_DEBUG_PRINTLN("End-Position: " + String(currentPosition));
    } else if (!isMoving) {
        MOTOR_DEBUG_PRINTLN("Fahrt wurde gestoppt");
        MOTOR_DEBUG_PRINTLN("Erreichte Passagen: " + String(passedCount) + " von " + String(count));
    }
    
    isMoving = false;
    isPassingButton = false;
    setPinsIdle();
    MOTOR_DEBUG_PRINTLN("Button-Pass-Fahrt beendet. End-Position: " + String(currentPosition));
}

void AdvancedStepperMotor::setVirtualHome() {
    virtualHomePosition = currentPosition;
    isHomed = true;
    MOTOR_DEBUG_PRINTLN("Virtuelle Home-Position gesetzt auf: " + String(virtualHomePosition));
    MOTOR_DEBUG_PRINTLN("Aktuelle Position: " + String(currentPosition));
}

void AdvancedStepperMotor::moveToVirtualHome() {
    if (!isEnabled) {
        MOTOR_DEBUG_PRINTLN("Motor ist deaktiviert - Fahrt zur virtuellen Home-Position abgebrochen");
        return;
    }
    
    MOTOR_DEBUG_PRINTLN("Fahre zur virtuellen Home-Position: " + String(virtualHomePosition));
    MOTOR_DEBUG_PRINTLN("Aktuelle Position: " + String(currentPosition));
    MOTOR_DEBUG_PRINTLN("Geschwindigkeit: " + String(currentSpeedRPM) + " RPM");
    
    int stepsToVirtualHome = virtualHomePosition - currentPosition;
    MOTOR_DEBUG_PRINTLN("Benötigte Schritte: " + String(stepsToVirtualHome));
    
    if (stepsToVirtualHome == 0) {
        MOTOR_DEBUG_PRINTLN("Bereits an virtueller Home-Position");
        return;
    }
    
    moveRelative(stepsToVirtualHome);
    MOTOR_DEBUG_PRINTLN("Fahrt zur virtuellen Home-Position abgeschlossen");
}

int AdvancedStepperMotor::getCurrentPosition() { return currentPosition; }
int AdvancedStepperMotor::getTargetPosition() { return targetPosition; }
int AdvancedStepperMotor::getVirtualHomePosition() { return virtualHomePosition; }
bool AdvancedStepperMotor::getIsMoving() { return isMoving; }
bool AdvancedStepperMotor::getIsEnabled() { return isEnabled; }
int AdvancedStepperMotor::getCurrentSpeed() { return currentSpeedRPM; }
bool AdvancedStepperMotor::getIsHomed() { return isHomed; }
int AdvancedStepperMotor::getTargetPassCount() { return targetPassCount; }
int AdvancedStepperMotor::getCurrentPassCount() { return currentPassCount; }
bool AdvancedStepperMotor::getIsPassingButton() { return isPassingButton; }

AdvancedMotorStatus AdvancedStepperMotor::getStatus() {
    AdvancedMotorStatus status;
    status.currentPosition = currentPosition;
    status.targetPosition = targetPosition;
    status.virtualHomePosition = virtualHomePosition;
    status.isMoving = isMoving;
    status.currentSpeed = currentSpeedRPM;
    status.isHomed = isHomed;
    status.isEnabled = isEnabled;
    status.targetPassCount = targetPassCount;
    status.currentPassCount = currentPassCount;
    status.isPassingButton = isPassingButton;
    return status;
}

void AdvancedStepperMotor::update() {
    if (!isMoving) return;
    
    unsigned long currentTime = micros();
    if (currentTime - lastStepTime >= stepDelayMicros) {
        if (currentPosition != targetPosition) {
            step();
            lastStepTime = currentTime;
        } else {
            isMoving = false;
        }
    }
}

// Globale Setup-Funktion
void setupAdvancedMotor() {
    advancedMotor.begin();
    advancedMotor.setSpeed(60);  // Default speed 60 RPM
    advancedMotor.enable();
}

// Globale Update-Funktion für main loop
void updateMotor() {
    advancedMotor.update();
}

// Globale Home-Funktion mit Button
void homeMotorToButton() {
    advancedMotor.homeToButton();
}

// Globale Funktion für Button-Passagen
void passButtonTimes(int count) {
    advancedMotor.passButtonTimes(count);
}

// Globale Kalibrierungs-Funktion für virtuelle Home-Position
void calibrateVirtualHome() {
    advancedMotor.setVirtualHome();
}

// Globale Funktion für Fahrt zur virtuellen Home-Position
void moveToVirtualHome() {
    advancedMotor.moveToVirtualHome();
}

// Debug-Funktionen
void setMotorDebug(bool enabled) {
    motorDebugEnabled = enabled;
    if (enabled) {
        MOTOR_DEBUG_PRINTLN("Motor-Debug aktiviert");
    }
}

bool getMotorDebugStatus() {
    return motorDebugEnabled;
}
