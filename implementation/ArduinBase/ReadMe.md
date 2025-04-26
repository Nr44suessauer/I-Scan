## Verfügbare API-Befehle

### Servo-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/setServo` | `angle` (0-180) | Positioniert den Servo auf den angegebenen Winkel | `http://192.168.178.77/setServo?angle=90` |

### Stepper-Motor-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/setMotor` | `position` (-1000 bis 1000) | Bewegt den Motor zur angegebenen absoluten Position | `http://192.168.178.77/setMotor?position=250` |
| `/setMotor` | `steps` (0-1000), `direction` (1 oder -1) | Bewegt den Motor um die angegebene Anzahl von Schritten in die angegebene Richtung | `http://192.168.178.77/setMotor?steps=100&direction=1` |

### RGB-LED-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/color` | `index` (0-6) | Setzt die LED auf eine vordefinierte Farbe:<br>0: Rot<br>1: Grün<br>2: Blau<br>3: Gelb<br>4: Lila<br>5: Orange<br>6: Weiß | `http://192.168.178.77/color?index=2` |
| `/hexcolor` | `hex` (Format: #RRGGBB, URL-encoded) | Setzt die LED auf eine benutzerdefinierte Farbe im Hex-Format | `http://192.168.178.77/hexcolor?hex=%23FF00FF` |

## Beispiel-Sequenzen

### Servo-Test
http://192.168.178.77/setServo?angle=0 http://192.168.178.77/setServo?angle=90 http://192.168.178.77/setServo?angle=180
### Motor-Test
http://192.168.178.77/setMotor?steps=200&direction=1 http://192.168.178.77/setMotor?steps=200&direction=-1 http://192.168.178.77/setMotor?position=500 http://192.168.178.77/setMotor?position=0
### LED-Test
http://192.168.178.77/color?index=0 http://192.168.178.77/color?index=1 http://192.168.178.77/color?index=2 http://192.168.178.77/hexcolor?hex=%23FF00FF

