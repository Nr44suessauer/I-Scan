# 📋 Calculator_Angle_Maschine - Befehle und Parameter

## 🚀 Haupt-Befehle (Modi)

### **Standardausführung**
```bash
python main.py
```
- **Beschreibung:** Vollständige Analyse mit allen Visualisierungen
- **Ausgabe:** 6+ PNG-Dateien, mathematische Erklärung
- **Verwendung:** Für Entwicklung und detaillierte Analyse

### **--csv / -c** (CSV Export Modus)
```bash
python main.py --csv
python main.py -c
```
- **Beschreibung:** Vollständige Analyse + CSV-Export für Software_IScan
- **Ausgabe:** Visualisierungen + CSV-Datei
- **Verwendung:** Für Produktionsscans mit Dokumentation

### **--silent / -s** (Silent Modus)
```bash
python main.py --silent
python main.py -s
```
- **Beschreibung:** Minimale Ausgabe, nur Mathematik + CSV
- **Ausgabe:** CSV-Datei, reduzierte Konsolen-Ausgabe
- **Verwendung:** Für Automatisierung und Batch-Processing

### **--math / -m** (Mathematik Modus)
```bash
python main.py --math
python main.py -m
```
- **Beschreibung:** Mathematische Analyse + CSV ohne Visualisierungen
- **Ausgabe:** CSV-Datei, detaillierte mathematische Erklärung
- **Verwendung:** Schnelle Berechnungen ohne Grafiken

### **--visualize / -v** (Visualisierung Modus)
```bash
python main.py --visualize
python main.py -v
```
- **Beschreibung:** Alle Visualisierungen mit angepasster Konfiguration
- **Ausgabe:** PNG-Dateien, keine CSV
- **Verwendung:** Für grafische Analyse ohne CSV-Export

### **--servo-graph / -g** (Servo Graph Modus)
```bash
python main.py --servo-graph
python main.py -g
```
- **Beschreibung:** Nur Servo-Geometrie-Graph erstellen
- **Ausgabe:** Ein PNG-File mit Servo-Diagramm
- **Verwendung:** Schnelle Servo-Visualisierung

### **--help / -h** (Hilfe)
```bash
python main.py --help
python main.py -h
```
- **Beschreibung:** Zeigt alle verfügbaren Befehle und Parameter
- **Ausgabe:** Hilfetext in der Konsole

---

## ⚙️ Konfigurations-Parameter

### **CSV-Benennung**
```bash
--csv-name DATEINAME
```
- **Typ:** String (ohne .csv Endung)
- **Standard:** Zeitstempel-basiert (z.B. `iscan_commands_2025-06-12_14-30-15.csv`)
- **Beispiel:** `--csv-name mein_scan_projekt`
- **Resultat:** `mein_scan_projekt.csv`

### **Ziel-Position (Target)**
```bash
--target-x WERT     # X-Koordinate des Ziels in cm
--target-y WERT     # Y-Koordinate des Ziels in cm
```
- **Typ:** Float (Dezimalzahlen)
- **Standard:** X=50, Y=50
- **Bereich:** Beliebige positive/negative Werte
- **Beispiel:** `--target-x 33 --target-y 50`

### **Scanner-Position**
```bash
--scanner-x WERT    # X-Koordinate des Scanners in cm
--scanner-y WERT    # Y-Koordinate des Scanners in cm
```
- **Typ:** Float
- **Standard:** X=0, Y=0
- **Beispiel:** `--scanner-x 0 --scanner-y 0`

### **Scan-Einstellungen**
```bash
--scan-distance WERT      # Maximale Scan-Distanz in cm
--measurements WERT       # Anzahl der Messpunkte
```
- **scan-distance:**
  - **Typ:** Float
  - **Standard:** 100.0 cm
  - **Beispiel:** `--scan-distance 80`
- **measurements:**
  - **Typ:** Integer
  - **Standard:** 10
  - **Beispiel:** `--measurements 7`

### **Servo-Parameter**
```bash
--servo-min WERT         # Minimum Servo-Winkel in Grad
--servo-max WERT         # Maximum Servo-Winkel in Grad
--servo-neutral WERT     # Neutral-Position in Grad
--servo-offset WERT      # Rotations-Offset in Grad
```
- **Typ:** Float
- **Standard:** min=0.0°, max=90.0°, neutral=45.0°, offset=45.0°
- **Beispiel:** `--servo-min 10 --servo-max 80 --servo-neutral 45`

---

## 🎯 Praktische Beispiele

### **Original I-Scan Setup nachstellen**
```bash
python main.py --csv --csv-name original_iscan --target-x 33 --target-y 50 --scan-distance 80 --measurements 7
```
- **Erstellt:** Vollständige Analyse + CSV für das ursprüngliche I-Scan Setup

### **Schneller Silent-Scan für Automation**
```bash
python main.py --silent --csv-name produktions_scan --target-x 40 --target-y 60 --measurements 5
```
- **Erstellt:** Nur CSV-Datei mit minimaler Ausgabe

### **Hochauflösender Scan**
```bash
python main.py --csv --csv-name high_res_scan --target-x 50 --target-y 50 --scan-distance 100 --measurements 15
```
- **Erstellt:** 15 Messpunkte über 100cm Distanz

### **Angepasste Servo-Konfiguration**
```bash
python main.py --math --csv-name custom_servo --servo-min 10 --servo-max 80 --servo-neutral 45
```
- **Erstellt:** Mathematik + CSV mit angepassten Servo-Grenzen

### **Nur Visualisierungen mit custom Setup**
```bash
python main.py --visualize --target-x 90 --target-y 50 --scan-distance 80 --measurements 20
```
- **Erstellt:** Nur PNG-Dateien, keine CSV

### **Test-Setup für Entwicklung**
```bash
python main.py --silent --csv-name test_run --target-x 33 --target-y 50 --scan-distance 40 --measurements 5
```
- **Erstellt:** Schneller Test mit 5 Punkten über 40cm

---

## 📁 Ausgabe-Dateien

### **CSV-Dateien** (im `output/` Ordner)
- **Format:** `type,params,description`
- **Inhalt:** Software_IScan kompatible Befehle
- **Befehle:** `home`, `servo`, `photo`, `stepper`
- **Beispiel:** `mein_scan.csv`

### **Visualisierungs-Dateien** (im `output/` Ordner)
- `01_geometric_representation.png` - Geometrische Darstellung
- `02_angle_progression.png` - Winkel-Verlauf
- `05_calculation_table.png` - Berechnungstabelle
- `06_servo_interpolation.png` - Servo-Interpolation
- `06_servo_geometry_graph_only.png` - Servo-Geometrie
- `07_servo_cone_detail.png` - Servo-Kegel Details
- `point_calculations/` - Ordner mit detaillierten Punkt-Berechnungen

---

## 🔄 Kombinationen

### **Mehrere Parameter kombinieren**
```bash
python main.py --csv --csv-name vollstaendiger_scan --target-x 33 --target-y 50 --scan-distance 80 --measurements 7 --servo-min 5 --servo-max 85
```

### **Batch-Processing Beispiel**
```bash
# Scan 1: Original Setup
python main.py --silent --csv-name scan_01_original --target-x 33 --target-y 50 --scan-distance 80 --measurements 7

# Scan 2: Hohe Auflösung
python main.py --silent --csv-name scan_02_highres --target-x 33 --target-y 50 --scan-distance 80 --measurements 15

# Scan 3: Kurze Distanz
python main.py --silent --csv-name scan_03_short --target-x 33 --target-y 50 --scan-distance 40 --measurements 5
```

---

## ⚠️ Wichtige Hinweise

1. **CSV-Namen:** Keine Leerzeichen verwenden, Unterstriche sind OK
2. **Werte-Bereiche:** Servo-Winkel sollten zwischen 0-180° liegen
3. **Measurements:** Mindestens 2 Messpunkte erforderlich
4. **Scan-Distance:** Muss größer als 0 sein
5. **Dateien:** Werden im `output/` Ordner gespeichert
6. **Überschreibung:** Alte Dateien werden automatisch überschrieben

---

## 🚀 Software_IScan Integration

Alle generierten CSV-Dateien sind direkt in Software_IScan importierbar:

1. **CSV Silent Mode Button** → Verwendet diese Parameter
2. **Vollanalyse + CSV Button** → Verwendet diese Parameter  
3. **CSV importieren Button** → Lädt generierte Dateien

**Beispiel für Integration:**
```bash
python main.py --silent --csv-name integration_test --target-x 33 --target-y 50 --scan-distance 80 --measurements 7
```
→ Erstellt `integration_test.csv` → Import in Software_IScan → Ausführung der Warteschlange
