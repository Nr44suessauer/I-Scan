# I-Scan Hardware-Steuerung API

Diese Dokumentation beschreibt die API zur Steuerung der I-Scan Hardware über HTTP-Anfragen. Die Hardware umfasst einen Servomotor, einen 28BYJ-48 Schrittmotor und eine RGB-LED.

## Basis-URL

Die I-Scan Hardware ist unter folgender Adresse erreichbar:

```
http://192.168.178.77
```

## Verfügbare API-Befehle

### Servo-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/setServo` | `angle` (0-180) | Positioniert den Servo auf den angegebenen Winkel | `http://192.168.178.77/setServo?angle=90` |

### Stepper-Motor-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/setMotor` | `position` (-4096 bis 4096) | Bewegt den Motor zur angegebenen absoluten Position | `http://192.168.178.77/setMotor?position=250` |
| `/setMotor` | `steps` (0-4096), `direction` (1 oder -1) | Bewegt den Motor um die angegebene Anzahl von Schritten in die angegebene Richtung | `http://192.168.178.77/setMotor?steps=100&direction=1` |
| `/setMotor` | `steps` (0-4096), `direction` (1 oder -1), `speed` (0-100) | Bewegt den Motor mit angegebener Geschwindigkeit | `http://192.168.178.77/setMotor?steps=100&direction=1&speed=75` |

### RGB-LED-Steuerung

| Befehl | Parameter | Beschreibung | Beispiel |
|--------|-----------|-------------|----------|
| `/color` | `index` (0-6) | Setzt die LED auf eine vordefinierte Farbe:<br>0: Rot<br>1: Grün<br>2: Blau<br>3: Gelb<br>4: Lila<br>5: Orange<br>6: Weiß | `http://192.168.178.77/color?index=2` |
| `/hexcolor` | `hex` (Format: #RRGGBB, URL-encoded) | Setzt die LED auf eine benutzerdefinierte Farbe im Hex-Format | `http://192.168.178.77/hexcolor?hex=%23FF00FF` |

## API-Nutzung

### Verwendung mit cURL

#### Servo bewegen:
```bash
# Servo auf 45 Grad positionieren
curl "http://192.168.178.77/setServo?angle=45"

# Servo in Mittelstellung (90°) bewegen
curl "http://192.168.178.77/setServo?angle=90"

# Servo in maximale Position (180°) bewegen
curl "http://192.168.178.77/setServo?angle=180"
```

#### Motor steuern:
```bash
# Motor 200 Schritte vorwärts bewegen
curl "http://192.168.178.77/setMotor?steps=200&direction=1"

# Motor 200 Schritte rückwärts bewegen
curl "http://192.168.178.77/setMotor?steps=200&direction=-1"

# Motor mit hoher Geschwindigkeit (85%) 500 Schritte vorwärts bewegen
curl "http://192.168.178.77/setMotor?steps=500&direction=1&speed=85"

# Eine vollständige Umdrehung vorwärts mit mittlerer Geschwindigkeit (50%)
curl "http://192.168.178.77/setMotor?steps=4096&direction=1&speed=50"

# Motor zur absoluten Position 500 bewegen
curl "http://192.168.178.77/setMotor?position=500"

# Motor zur absoluten Position 0 zurücksetzen
curl "http://192.168.178.77/setMotor?position=0"
```

#### LED steuern:
```bash
# LED auf Rot setzen (voreingestellte Farbe 0)
curl "http://192.168.178.77/color?index=0"

# LED auf Grün setzen (voreingestellte Farbe 1)
curl "http://192.168.178.77/color?index=1"

# LED auf Blau setzen (voreingestellte Farbe 2)
curl "http://192.168.178.77/color?index=2"

# LED auf benutzerdefinierte Farbe setzen (Magenta)
curl "http://192.168.178.77/hexcolor?hex=%23FF00FF"

# LED auf benutzerdefinierte Farbe setzen (Gelb)
curl "http://192.168.178.77/hexcolor?hex=%23FFFF00"
```

### Verwendung mit Python

```python
import requests

# Basis-URL
base_url = "http://192.168.178.77"

# Servo auf 45 Grad positionieren
response = requests.get(f"{base_url}/setServo", params={"angle": 45})
print(response.text)

# Motor 200 Schritte vorwärts bewegen mit 70% Geschwindigkeit
response = requests.get(
    f"{base_url}/setMotor", 
    params={"steps": 200, "direction": 1, "speed": 70}
)
print(response.text)

# LED auf Blau setzen
response = requests.get(f"{base_url}/color", params={"index": 2})
print(response.text)

# LED auf benutzerdefinierte Farbe setzen
response = requests.get(f"{base_url}/hexcolor", params={"hex": "#FF00FF"})
print(response.text)
```

### Verwendung mit JavaScript

```javascript
// Servo auf 45 Grad positionieren
fetch('http://192.168.178.77/setServo?angle=45')
  .then(response => response.text())
  .then(data => console.log(data));

// Motor 200 Schritte vorwärts bewegen
fetch('http://192.168.178.77/setMotor?steps=200&direction=1&speed=70')
  .then(response => response.text())
  .then(data => console.log(data));

// LED auf Blau setzen
fetch('http://192.168.178.77/color?index=2')
  .then(response => response.text())
  .then(data => console.log(data));

// LED auf benutzerdefinierte Farbe setzen
fetch('http://192.168.178.77/hexcolor?hex=' + encodeURIComponent('#FF00FF'))
  .then(response => response.text())
  .then(data => console.log(data));
```

### Verwendung mit Postman

1. Erstellen Sie eine neue Anfrage in Postman
2. Wählen Sie die HTTP-Methode `GET`
3. Geben Sie die URL und Parameter ein, z.B. `http://192.168.178.77/setServo?angle=90`
4. Klicken Sie auf "Send" und sehen Sie die Antwort im Bereich darunter

### Beispiel-Sequenzen für Tests

#### Servo-Test
```
http://192.168.178.77/setServo?angle=0
http://192.168.178.77/setServo?angle=90
http://192.168.178.77/setServo?angle=180
```

#### Motor-Test
```
http://192.168.178.77/setMotor?steps=200&direction=1
http://192.168.178.77/setMotor?steps=200&direction=-1
http://192.168.178.77/setMotor?position=500
http://192.168.178.77/setMotor?position=0
```

#### LED-Test
```
http://192.168.178.77/color?index=0
http://192.168.178.77/color?index=1
http://192.168.178.77/color?index=2
http://192.168.178.77/hexcolor?hex=%23FF00FF
```

## Hinweise

- Alle API-Befehle verwenden die HTTP-GET-Methode für einfache Zugänglichkeit und Testbarkeit
- Die Antworten werden im Plaintext-Format zurückgegeben
- Bei ungültigen Parametern wird ein HTTP-Statuscode 400 zurückgegeben
- Die maximale Motorgeschwindigkeit ist intern auf 90% begrenzt, um zuverlässigen Betrieb zu gewährleisten
- Ein kompletter Umlauf des 28BYJ-48 Motors entspricht 4096 Schritten

