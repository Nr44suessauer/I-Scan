# I-Scan 3D-Scanner Dokumentation

## Was ist I-Scan?

I-Scan ist ein automatisches 3D-Scanner-System, das Objekte aus verschiedenen Winkeln fotografiert und daraus 3D-Modelle erstellt. Stellt euch vor, ihr möchtet eine Tasse von allen Seiten fotografieren - I-Scan macht das automatisch!

```
Einfaches Scan-Prinzip:

    📷 Kamera bewegt sich um das Objekt
         ↙     ↓     ↘
      Foto1  Foto2  Foto3
         ↓     ↓     ↓
      🖥️ Computer erstellt 3D-Modell
```

## Ablauf der Programme

### 1. Wie funktioniert das System?

Das I-Scan System besteht aus mehreren Teilen, die zusammenarbeiten:

```
System-Aufbau:

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Computer     │◄──►│   Position      │◄──►│    Kamera       │
│   (eure GUI)    │    │     Unit        │    │                 │
│                 │    │  (bewegt sich)  │    │ (macht Fotos)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Was passiert beim Scannen:**

1. **Start**: Computer startet das Programm
2. **Verbindung**: Computer spricht mit der Position Unit
3. **Home-Position**: Alles fährt zur Startposition
4. **Scan-Loop**: 
   - Position Unit bewegt sich zu einem Punkt
   - Kamera macht ein Foto
   - Wiederholen für alle Punkte
5. **Fertig**: Alle Fotos sind gespeichert

### 2. Programme und ihre Aufgaben

#### Hauptprogramm: `main.py`
```
main.py = Das Hauptprogramm mit der grafischen Oberfläche

Was es macht:
├── GUI anzeigen (Knöpfe und Eingabefelder)
├── Mit Hardware sprechen
├── Fotos speichern
└── Befehle in einer Warteschlange verwalten
```

#### Winkel-Rechner: `calculator_simplified.py`
```
calculator_simplified.py = Berechnet optimale Scan-Positionen

Eingabe: "Ich will 30 Fotos von einem 50cm hohen Objekt"
Ausgabe: CSV-Datei mit allen Positionen und Winkeln
```

#### API-Client: `api_client.py`
```
api_client.py = Übersetzt Befehle für die Hardware

Computer sagt: "Bewege dich zu Position X"
API-Client übersetzt: HTTP-Request an Position Unit
Position Unit antwortet: "OK, bin da!"
```

### 3. Schritt-für-Schritt Ablauf eines Scans

```
Detaillierter Scan-Ablauf:

1. [START] Programm starten
   └── main.py öffnet GUI

2. [VERBINDUNG] Hardware prüfen  
   └── Ist Position Unit erreichbar?
   └── Ist Kamera angeschlossen?

3. [VORBEREITUNG] CSV-Datei laden
   └── calculator_simplified.py hat Positionen berechnet
   └── Beispiel: 30 Punkte für 50cm Höhe

4. [INITIALISIERUNG] Home-Position
   └── Servo auf 90° (gerade)
   └── Stepper auf Position 0 (unten)

5. [SCAN-SCHLEIFE] Für jeden Punkt:
   ├── Stepper bewegt sich nach oben (z.B. 2.3cm)
   ├── Servo stellt Winkel ein (z.B. 87°)
   ├── Kurz warten (Hardware braucht Zeit)
   ├── Foto aufnehmen
   └── Foto speichern

6. [FERTIG] Alle Fotos gespeichert
   └── Zurück zur Home-Position
```

**Beispiel aus echter CSV-Datei:**

Die Datei `winkeltabelle_50x0_30punkte_approximiert.csv` enthält:

```csv
type,params,description
home,{},Home-Position anfahren
servo,"{""angle"": 90}",Servo: Winkel auf 90° setzen (Y=0.0cm)
photo,{},"Kamera: Foto aufnehmen bei Y=0.0cm, Winkel=90°"
stepper,"{""steps"": 1086, ""direction"": 1, ""speed"": 80}","Stepper: 1086 Schritte, 2.3cm, Richtung aufwärts"
servo,"{""angle"": 87}",Servo: Winkel auf 87° setzen (Y=2.3cm)
photo,{},"Kamera: Foto aufnehmen bei Y=2.3cm, Winkel=87°"
```

**Was bedeutet das:**
- **Zeile 1**: Fahre zur Startposition
- **Zeile 2**: Stelle Kamera auf 90° (gerade nach unten)
- **Zeile 3**: Mache ein Foto
- **Zeile 4**: Bewege dich 2.3cm nach oben (1086 Schritte)
- **Zeile 5**: Stelle Kamera auf 87° (etwas schräger)
- **Zeile 6**: Mache noch ein Foto

### 4. Mathematik dahinter (einfach erklärt)

```
Warum ändern sich die Winkel?

      📷 Kamera
       ╲
        ╲ 87°
         ╲
          🎯 Objekt (oben)
          
      📷 Kamera  
       │
       │ 90°
       │
       🎯 Objekt (mitte)
       
      📷 Kamera
      ╱
     ╱ 93°
    ╱
   🎯 Objekt (unten)

Die Kamera soll immer das Objekt "anschauen".
Wenn das Objekt höher ist, muss die Kamera steiler schauen.
```

## Verwendung der Programme

### 1. Programm starten

#### Einfacher Start:
```powershell
# Im I-Scan Ordner die start.bat doppelklicken
# ODER im PowerShell:
cd "C:\Users\Marc\Desktop\I-Scan\I-Scan\implementation\ControlScript"
python main.py
```

#### Was ihr seht:
```
GUI-Fenster öffnet sich:

┌─────────────────────────────────────────────────────────┐
│  I-Scan Control                                [X]      │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │   Servo     │ │  Stepper    │ │   Kamera    │        │
│ │   📐        │ │    ↕️        │ │    📷       │        │
│ │ [90°] [Set] │ │ [100] [Up]  │ │ [Foto]      │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │    Queue    │ │    CSV      │ │   Status    │        │
│ │   📋        │ │    📄       │ │    💡       │        │
│ │ [Start All] │ │ [Import]    │ │ [Verbinden] │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### 2. Erste Schritte - Verbindung testen

#### Schritt 1: Hardware-Verbindung prüfen
```python
# Klickt auf "Verbindung testen" Button
# Oder manuell im Code:
app.test_connection()
```

**Was passiert:**
- System sendet Test-Befehle an Position Unit
- Prüft ob Servo und Stepper antworten
- Zeigt Status in der GUI an

**Erfolgreiche Verbindung:**
```
✅ Position Unit: OK
✅ Servo Motor: OK  
✅ Stepper Motor: OK
✅ Kamera: OK
```

**Probleme beheben:**
```
❌ Position Unit: Fehler
Lösung: IP-Adresse in api_client.py prüfen

❌ Kamera: Fehler  
Lösung: USB-Kabel prüfen, anderen Port probieren
```

#### Schritt 2: Home-Position anfahren
```python
# Immer zuerst machen!
app.move_to_home()
```

Das bewegt alle Motoren zur sicheren Startposition.

### 3. Manueller Modus - Einzelne Befehle

#### Servo (Kamera-Winkel) steuern:
```
1. Winkel eingeben: 45
2. "Set Servo" klicken
3. Kamera bewegt sich zu 45°
```

#### Stepper (Höhe) steuern:
```
1. Schritte eingeben: 500
2. "Move Up" oder "Move Down" klicken  
3. Position Unit bewegt sich nach oben/unten
```

#### Foto aufnehmen:
```
1. "Take Photo" klicken
2. Foto wird in /fotos/ gespeichert
3. Dateiname: scan_2024_01_15_14_30_25.jpg
```

### 4. Automatischer Modus - CSV-Import

#### Schritt 1: CSV-Datei vorbereiten
```powershell
# Fertige CSV-Dateien verwenden:
winkeltabelle_50x0_30punkte_approximiert.csv  # 30 Punkte, 50cm Höhe
winkeltabelle_40x0_20punkte_approximiert.csv  # 20 Punkte, 40cm Höhe
```

#### Schritt 2: CSV importieren
```python
# In der GUI:
1. "CSV Import" klicken
2. Datei auswählen
3. Queue wird automatisch gefüllt
```

#### Schritt 3: Automatischen Scan starten
```python
# Queue ausführen:
1. "Start All" klicken
2. System arbeitet alle Befehle ab
3. Fotos werden automatisch gespeichert
```

**Was passiert automatisch:**
```
Automatischer Ablauf:

[Queue hat 90 Befehle geladen]
├── Befehl 1: home → ✅ Fertig
├── Befehl 2: servo(90°) → ✅ Fertig  
├── Befehl 3: photo → ✅ Foto gespeichert
├── Befehl 4: stepper(1086) → ✅ Fertig
├── Befehl 5: servo(87°) → ✅ Fertig
├── Befehl 6: photo → ✅ Foto gespeichert
├── ...
└── Befehl 90: Alle Fotos fertig!
```

### 5. Eigene Scan-Parameter erstellen

#### Mit calculator_simplified.py:
```python
# Neue Winkeltabelle berechnen:
python calculator_simplified.py

# Eingaben:
# - Objekthöhe: 60cm
# - Anzahl Punkte: 25  
# - Ausgabedatei: mein_scan.csv
```

#### Parameter verstehen:
```
Objekthöhe = Wie hoch ist das zu scannende Objekt?
├── Kleine Objekte (10-20cm): 15-20 Fotos reichen
├── Mittlere Objekte (30-40cm): 20-25 Fotos  
└── Große Objekte (50cm+): 30+ Fotos

Anzahl Punkte = Wie viele Fotos?
├── Weniger Fotos = Schneller, aber weniger Detail
└── Mehr Fotos = Langsamer, aber bessere Qualität
```

### 6. Ergebnisse verstehen

#### Wo finde ich die Fotos?
```
Datei-Struktur:
I-Scan/
├── implementation/
│   └── ControlScript/
│       ├── fotos/              ← Hier sind eure Fotos!
│       │   ├── scan_001.jpg
│       │   ├── scan_002.jpg
│       │   └── ...
│       └── main.py
```

#### Dateinamen verstehen:
```
scan_2024_01_15_14_30_25.jpg
│    │    │  │  │  │  │  └── Sekunden
│    │    │  │  │  └── Minuten  
│    │    │  │  └── Stunden
│    │    │  └── Tag
│    │    └── Monat
│    └── Jahr
└── Prefix
```

#### Scan-Visualisierung:

![Scan Visualization](scan_visualization_approximated.png)

**Was zeigt das Bild:**
- **Blaue Linie**: Mathematisch perfekte Winkel
- **Grüne Linie**: Angepasste/praktische Winkel  
- **Rote Punkte**: Wo tatsächlich Fotos gemacht werden
- **X-Achse**: Position seitlich (cm)
- **Y-Achse**: Position in der Höhe (cm)

### 7. Tipps für bessere Scans

#### Objekt-Vorbereitung:
```
✅ Objekt gut beleuchten
✅ Einfarbiger Hintergrund  
✅ Objekt mittig platzieren
✅ Keine glänzenden Oberflächen

❌ Zu dunkle Umgebung
❌ Unordentlicher Hintergrund
❌ Objekt zu groß für Scanner
❌ Spiegelnde Materialien
```

#### Scan-Qualität verbessern:
```
Mehr Fotos = Bessere Qualität
├── Minimum: 20 Fotos
├── Standard: 30 Fotos  
└── Hoch: 40+ Fotos

Langsamere Geschwindigkeit = Schärfere Fotos
├── Speed: 30-50 für beste Qualität
└── Speed: 80+ für schnelle Tests
```

## API-Dokumentation

### Was ist eine API?

Eine API ist wie ein Übersetzer zwischen eurem Computer und der I-Scan Hardware.

```
Einfache API-Erklärung:

Ihr sagt: "Bewege dich zu 90°"
    ↓
API übersetzt: "POST /api/servo" mit {"angle": 90}
    ↓  
Hardware antwortet: "OK, bin bei 90°"
    ↓
API übersetzt zurück: "Bewegung erfolgreich"
```

### Grundlagen für Windows (PowerShell)

#### API-Befehle senden:
```powershell
# Grundformat für alle API-Befehle:
Invoke-RestMethod -Uri "http://192.168.1.100/api/BEFEHL" -Method METHODE -Body $daten -ContentType "application/json"

# Beispiel - Servo bewegen:
$daten = @{
    "angle" = 90
    "speed" = 50
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://192.168.1.100/api/servo" -Method POST -Body $daten -ContentType "application/json"
```

### Wichtige API-Befehle

#### 1. System-Status prüfen
```powershell
# Ist das System bereit?
Invoke-RestMethod -Uri "http://192.168.1.100/api/status" -Method GET
```

**Antwort:**
```json
{
    "success": true,
    "data": {
        "status": "ready",
        "firmware": "1.2.3",
        "temperature": "23°C"
    }
}
```

#### 2. Servo (Kamera-Winkel) steuern
```powershell
# Kamera auf 45° stellen:
$servoBefehl = @{
    "angle" = 45
    "speed" = 60
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://192.168.1.100/api/servo" -Method POST -Body $servoBefehl -ContentType "application/json"
```

**Parameter:**
- `angle`: 0-180° (Winkel der Kamera)
- `speed`: 1-100 (wie schnell bewegen)

#### 3. Stepper (Höhen-Position) steuern
```powershell
# 2.3cm nach oben bewegen:
$stepperBefehl = @{
    "steps" = 1086      # 1086 Schritte = 2.3cm
    "direction" = 1     # 1 = hoch, 0 = runter
    "speed" = 80        # Geschwindigkeit
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://192.168.1.100/api/stepper/move" -Method POST -Body $stepperBefehl -ContentType "application/json"
```

#### 4. Foto aufnehmen
```powershell
# Foto machen:
$fotoBefehl = @{
    "camera_id" = 1
    "quality" = 95
    "filename" = "mein_foto_$(Get-Date -Format 'yyyyMMdd_HHmmss').jpg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://192.168.1.100/api/camera/capture" -Method POST -Body $fotoBefehl -ContentType "application/json"
```

#### 5. Home-Position anfahren
```powershell
# Zurück zur sicheren Startposition:
Invoke-RestMethod -Uri "http://192.168.1.100/api/home" -Method POST
```

### Automatischer Scan über API

#### Kompletter Scan-Vorgang:
```powershell
# 1. Home-Position
Write-Host "Fahre zur Startposition..."
Invoke-RestMethod -Uri "http://192.168.1.100/api/home" -Method POST

# 2. Erste Position
Write-Host "Stelle Winkel ein..."
$servo1 = @{ "angle" = 90 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://192.168.1.100/api/servo" -Method POST -Body $servo1 -ContentType "application/json"

# 3. Erstes Foto
Write-Host "Foto 1..."
$foto1 = @{ "filename" = "scan_001.jpg" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://192.168.1.100/api/camera/capture" -Method POST -Body $foto1 -ContentType "application/json"

# 4. Nächste Position
Write-Host "Bewege nach oben..."
$move1 = @{ "steps" = 1086; "direction" = 1; "speed" = 80 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://192.168.1.100/api/stepper/move" -Method POST -Body $move1 -ContentType "application/json"

# 5. Winkel anpassen
Write-Host "Neuer Winkel..."
$servo2 = @{ "angle" = 87 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://192.168.1.100/api/servo" -Method POST -Body $servo2 -ContentType "application/json"

# 6. Zweites Foto
Write-Host "Foto 2..."
$foto2 = @{ "filename" = "scan_002.jpg" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://192.168.1.100/api/camera/capture" -Method POST -Body $foto2 -ContentType "application/json"

Write-Host "Scan abgeschlossen!"
```

### Fehler verstehen und beheben

#### Typische Fehler:
```powershell
# Fehler: Verbindung nicht möglich
# Lösung: IP-Adresse prüfen
Test-NetConnection -ComputerName "192.168.1.100" -Port 80

# Fehler: "Hardware busy"  
# Lösung: Warten bis Bewegung fertig ist
Start-Sleep -Seconds 2

# Fehler: "Invalid angle"
# Lösung: Nur Winkel zwischen 0-180° verwenden
```

#### Fehlerbehandlung in PowerShell:
```powershell
try {
    # API-Befehl versuchen
    $result = Invoke-RestMethod -Uri "http://192.168.1.100/api/servo" -Method POST -Body $daten -ContentType "application/json"
    Write-Host "✅ Erfolg: Servo bewegt!"
}
catch {
    # Bei Fehler:
    Write-Host "❌ Fehler: $($_.Exception.Message)"
    Write-Host "Lösung: Verbindung und Parameter prüfen"
}
```

### API mit Python verwenden

#### Einfaches Python-Beispiel:
```python
import requests
import json
import time

# API-Adresse
api_url = "http://192.168.1.100/api"

def bewege_servo(winkel):
    """Servo zu bestimmtem Winkel bewegen"""
    daten = {"angle": winkel, "speed": 60}
    response = requests.post(f"{api_url}/servo", json=daten)
    
    if response.status_code == 200:
        print(f"✅ Servo auf {winkel}° bewegt")
        return True
    else:
        print(f"❌ Fehler: {response.status_code}")
        return False

def mache_foto(dateiname):
    """Foto aufnehmen"""
    daten = {"filename": dateiname, "quality": 95}
    response = requests.post(f"{api_url}/camera/capture", json=daten)
    
    if response.status_code == 200:
        print(f"✅ Foto gespeichert: {dateiname}")
        return True
    else:
        print(f"❌ Foto-Fehler: {response.status_code}")
        return False

# Beispiel-Verwendung:
if __name__ == "__main__":
    print("Starte einfachen Scan...")
    
    # Servo bewegen und Foto machen
    if bewege_servo(90):
        time.sleep(1)  # Kurz warten
        mache_foto("test_foto.jpg")
    
    print("Fertig!")
```

### Erweiterte API-Funktionen

#### Batch-Befehle (mehrere Aktionen gleichzeitig):
```powershell
# Mehrere Befehle in einem Aufruf:
$batch = @{
    "operations" = @(
        @{
            "type" = "servo"
            "params" = @{ "angle" = 90 }
        },
        @{
            "type" = "stepper"
            "params" = @{ "steps" = 1086; "direction" = 1 }
        },
        @{
            "type" = "camera"
            "params" = @{ "capture" = $true }
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://192.168.1.100/api/batch" -Method POST -Body $batch -ContentType "application/json"
```

#### System-Informationen abrufen:
```powershell
# Detaillierte System-Info:
$info = Invoke-RestMethod -Uri "http://192.168.1.100/api/system/info" -Method GET

Write-Host "Firmware Version: $($info.firmware)"
Write-Host "Aktuelle Position: Höhe $($info.position.height)cm, Winkel $($info.position.angle)°"
Write-Host "Anzahl Fotos heute: $($info.stats.photos_today)"
```

Diese API-Dokumentation zeigt euch, wie ihr das I-Scan System nicht nur über die GUI, sondern auch programmatisch steuern könnt. Das ist besonders nützlich für eigene Experimente und erweiterte Anwendungen!
