# I-Scan API-Befehle für Postman

## Servo-Steuerung

| HTTP-Methode | URL | Beschreibung |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/setServo?angle=90` | Positioniert den Servo auf 90 Grad |
| GET | `http://192.168.178.77/setServo?angle=0` | Positioniert den Servo auf 0 Grad (Minimum) |
| GET | `http://192.168.178.77/setServo?angle=180` | Positioniert den Servo auf 180 Grad (Maximum) |

## Stepper-Motor-Steuerung

| HTTP-Methode | URL | Beschreibung |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/setMotor?position=250` | Bewegt den Motor zur absoluten Position 250 |
| GET | `http://192.168.178.77/setMotor?position=0` | Bewegt den Motor zurück zur Nullposition |
| GET | `http://192.168.178.77/setMotor?position=-500` | Bewegt den Motor zur absoluten Position -500 |
| GET | `http://192.168.178.77/setMotor?steps=100&direction=1` | Bewegt den Motor 100 Schritte vorwärts |
| GET | `http://192.168.178.77/setMotor?steps=100&direction=-1` | Bewegt den Motor 100 Schritte rückwärts |
| GET | `http://192.168.178.77/setMotor?steps=4096&direction=1` | Bewegt den Motor eine vollständige Umdrehung vorwärts |
| GET | `http://192.168.178.77/setMotor?steps=4096&direction=-1` | Bewegt den Motor eine vollständige Umdrehung rückwärts |
| GET | `http://192.168.178.77/setMotor?steps=100&direction=1&speed=50` | Bewegt den Motor 100 Schritte vorwärts mit 50% Geschwindigkeit |
| GET | `http://192.168.178.77/setMotor?steps=100&direction=-1&speed=75` | Bewegt den Motor 100 Schritte rückwärts mit 75% Geschwindigkeit |

## RGB-LED-Steuerung

| HTTP-Methode | URL | Beschreibung |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/color?index=0` | Setzt die LED auf Rot (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=1` | Setzt die LED auf Grün (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=2` | Setzt die LED auf Blau (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=3` | Setzt die LED auf Gelb (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=4` | Setzt die LED auf Lila (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=5` | Setzt die LED auf Orange (voreingestellte Farbe) |
| GET | `http://192.168.178.77/color?index=6` | Setzt die LED auf Weiß (voreingestellte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%23FF0000` | Setzt die LED auf Rot (benutzerdefinierte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%2300FF00` | Setzt die LED auf Grün (benutzerdefinierte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%230000FF` | Setzt die LED auf Blau (benutzerdefinierte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%23FFFF00` | Setzt die LED auf Gelb (benutzerdefinierte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%23FF00FF` | Setzt die LED auf Magenta (benutzerdefinierte Farbe) |
| GET | `http://192.168.178.77/hexcolor?hex=%2300FFFF` | Setzt die LED auf Cyan (benutzerdefinierte Farbe) |

## Button-Status

| HTTP-Methode | URL | Beschreibung |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/getButtonState` | Ruft den aktuellen Status des Buttons ab (gedrückt oder nicht) |

## Sonstiges

| HTTP-Methode | URL | Beschreibung |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/` | Ruft die Hauptseite der Weboberfläche ab |