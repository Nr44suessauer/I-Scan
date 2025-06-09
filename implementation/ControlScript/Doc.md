# I-Scan 3D-Scanner – Schritt-für-Schritt-Anleitung

---

## 1. Wie und warum nutzt man `calculator_simplified.py`?

### Was macht das Programm?

Der **calculator_simplified.py** berechnet alle nötigen Positionen und Winkel, die der Scanner später abfahren soll. Das Ziel: Möglichst gleichmäßige und vollständige Fotos von allen Seiten deines Objekts.

**Warum ist das wichtig?**
- Nur mit den richtigen Winkeln und Höhen bekommst du genug Bilder für ein gutes 3D-Modell.
- Die Berechnung per Hand wäre sehr aufwändig – das Programm macht das automatisch und fehlerfrei.

### Wie benutzt man das Programm?

1. **Starte das Programm**  
   Öffne eine Eingabeaufforderung im Projektordner und gib ein:
   ```powershell
   py calculator/calculator_simplified.py
   ```
2. **Folge den Anweisungen**  
   Du gibst z.B. die Höhe des Scanbereichs und die Anzahl der Fotos an.

3. **Ergebnis: Eine CSV-Datei**  
   Nach dem Durchlauf findest du eine Datei wie  
   `winkeltabelle_50x0_30punkte_approximiert.csv`  
   im Projektordner. Diese Datei enthält alle Bewegungs- und Foto-Befehle für den Scan.

---

### Beispiel einer erzeugten CSV-Datei:

```csv
type,params,description
home,{},Home-Position anfahren
servo,"{""angle"": 90}",Servo: Winkel auf 90° setzen (Y=0.0cm)
photo,{},"Kamera: Foto aufnehmen bei Y=0.0cm, Winkel=90°"
stepper,"{""steps"": 1086, ""direction"": 1, ""speed"": 80}","Stepper: 1086 Schritte, 2.3cm, Richtung aufwärts, Geschwindigkeit: 80"
servo,"{""angle"": 87}",Servo: Winkel auf 87° setzen (Y=2.3cm)
photo,{},"Kamera: Foto aufnehmen bei Y=2.3cm, Winkel=87°"
```

Jede Zeile steht für eine Aktion:  
- **servo** = Kamera drehen  
- **stepper** = Modul nach oben bewegen  
- **photo** = Foto aufnehmen

---

### Visualisierung der Berechnung

![Scan-Visualisierung](scan_visualization_approximated.png)

*Das Bild zeigt:*
- **Blaue Linie**: Bewegungsweg des Moduls
- **Rote Punkte**: Foto-Positionen
- **Tabellen**: Genaue Winkel und Koordinaten

---

## 2. Wie bindet man die CSV-Datei in `main.py` ein?

### Warum ist das wichtig?

`main.py` ist das Hauptprogramm mit grafischer Oberfläche. Es liest die CSV-Datei ein und führt die darin gespeicherten Bewegungen und Foto-Befehle automatisch aus. So musst du nicht jeden Schritt einzeln machen!

### Schritt-für-Schritt:

1. **Starte das Hauptprogramm**
   ```powershell
   py main.py
   ```
2. **Importiere die CSV-Datei**
   - Klicke im Programm auf „Import CSV“
   - Wähle z.B. `winkeltabelle_50x0_30punkte_approximiert.csv` aus

3. **Starte den Scan**
   - Klicke auf „Execute Queue“ oder „Scan starten“
   - Der Scanner arbeitet jetzt alle Befehle aus der CSV-Datei automatisch ab

4. **Fotos werden gespeichert**
   - Nach dem Scan findest du alle Bilder im Ausgabeordner

---

## 3. Wie funktioniert `main.py`?

### Übersicht

`main.py` ist die Steuerzentrale für den Scanner. Es bietet eine einfache grafische Oberfläche (GUI), mit der du:

- Die Kamera live sehen kannst
- Den Scanner manuell oder automatisch steuern kannst
- CSV-Dateien laden und ausführen kannst
- Die Beleuchtung einstellen kannst

### Die wichtigsten Funktionen im Überblick

1. **Kamera starten**
   - Zeigt das Live-Bild der Kamera

2. **Manuelle Steuerung**
   - Servo-Winkel (Kamera drehen) und Stepper-Schritte (Modul bewegen) eingeben
   - „Add to Queue“: Fügt die Bewegung zur Warteschlange hinzu

3. **Automatischer Scan**
   - CSV-Datei importieren (siehe oben)
   - „Execute Queue“: Scanner arbeitet alle Schritte ab

4. **Beleuchtung einstellen**
   - Farbe und Helligkeit der LEDs anpassen

5. **Status und Fehleranzeige**
   - Zeigt an, was der Scanner gerade macht
   - Gibt Hinweise bei Fehlern

---

### Beispielhafter Ablauf in der GUI

```
┌─────────────────────────────────────────────┐
│   I-Scan Control (main.py)                 │
├─────────────────────────────────────────────┤
│ [Start Camera]  [Import CSV]  [Execute Queue]│
│                                             │
│ [Servo Angle: ___] [Stepper Steps: ___]     │
│ [Add to Queue]                              │
│                                             │
│ [LED Color: ___] [Brightness: ___]          │
│ [Set Lighting]                              │
│                                             │
│ [Status: ...]                               │
└─────────────────────────────────────────────┘
```

---

## Zusammengefasst:

- **calculator_simplified.py** berechnet und erstellt die Bewegungs- und Foto-Befehle als CSV.
- **main.py** liest diese CSV ein und führt den Scan automatisch aus.
- So bekommst du mit wenigen Klicks perfekte Fotos für dein 3D-Modell!

---

**Tipp:**  
Wenn du etwas ändern willst (z.B. mehr Fotos, anderer Scanbereich), starte einfach calculator_simplified.py nochmal und erstelle eine neue CSV!