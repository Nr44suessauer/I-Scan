# 3D Scanner Geometric Angle Calculator 📐

Kompakte Mathematik-Engine für 3D-Scanner Servoansteuerung mit Visualisierungen.

## 🎯 System Konzept

```
                3D SCANNER SYSTEM
    ┌─────────────────────────────────────────┐
    │  Scanner(0,0) ───────────► Target(100,0)│
    │      │                                  │
    │      ▼ 100cm scan distance              │
    │  ┌───────┐                              │
    │  │Point 1│ ◄── Calculate angles         │
    │  │Point 2│                              │
    │  │  ...  │                              │
    │  │Point10│                              │
    │  └───────┘                              │
    └─────────────────────────────────────────┘
         ▼ PROCESSING FLOW ▼
    ┌─────────────────────────────────────────┐
    │ 1. Geometric Calculation                │
    │    atan2(dx,dy) → angle                 │
    │ 2. Servo Interpolation                  │
    │    angle + 45° + 180° → servo_angle     │
    │ 3. Visualization Generation             │
    │    PNG files in output/ + subfolder/    │
    └─────────────────────────────────────────┘
```

## 📂 Funktions-Mapping

### CORE MODULE: `config.py`
```
🔧 ensure_output_dir()         ← Verzeichnis-Management
📊 OUTPUT_DIR                  ← "output"
📁 POINT_CALCULATIONS_SUBDIR   ← "point_calculations"
⚙️  TARGET_CENTER_X/Y          ← Scanner-Koordinaten
📏 SCAN_DISTANCE               ← 100cm
🎛️  ENABLE_VISUALIZATIONS      ← Feature-Kontrolle
```

### MATH ENGINE: `calculations.py`
```
🧮 print_step_by_step_explanation()  ← Vollständige Ausgabe
🔢 calculate_geometric_angles()      ← Stille Berechnung
📐 Algorithmus:
   for point in range(10):
       y = point * step_size
       dx = target_x - scanner_x
       dy = target_y - y
       angle = atan2(dx, dy) * 180/π
```

### SERVO LOGIC: `servo_interpolation.py`
```
🎯 print_servo_interpolation_explanation()  ← Servo-Details
⚙️  calculate_servo_interpolation()         ← Servo-Winkel
🔄 print_detailed_reachability_table()     ← Erreichbarkeits-Analyse
📊 Servo-Mapping:
   geometric_angle + 45° + 180° = servo_coord_angle
   if -135° ≤ servo_coord_angle ≤ -45°: REACHABLE
```

### COORDINATOR: `main.py`
```
🚀 main()                 ← Vollmodus (Erklärung + Visualisierungen)
🔇 main_silent()          ← Nur Visualisierungen
📊 get_servo_angles()     ← Nur Daten zurückgeben
```

## 📊 Visualisierungs-Pipeline

```
VISUALIZATION MODULES (visualizations/)
├── geometric.py ────────────► 01_geometric_representation.png
├── angle_progression.py ────► 02_angle_progression.png
├── point_calculation.py ────► 04_point_X_calculation.png (subfolder)
├── calculation_table.py ───► 05_calculation_table.png
└── servo_interpolation.py ─► 06_servo_interpolation.png
                            └► 07_servo_cone_detail.png
```

### Subfolder-System:
```
output/
├── 01_geometric_representation.png
├── 02_angle_progression.png
├── 05_calculation_table.png
├── 06_servo_interpolation.png
├── 07_servo_cone_detail.png
└── point_calculations/          ← NEUE STRUKTUR
    ├── 04_point_1_calculation.png
    ├── 04_point_2_calculation.png
    ├── ...
    └── 04_point_10_calculation.png
```

## 🔄 Datenfluss-Diagramm

```
    ┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │   CONFIG    │───▶│   CALCULATIONS   │───▶│ SERVO_INTERP    │
    │             │    │                  │    │                 │
    │ - Scanner   │    │ 1. Step size     │    │ 1. Coord mapping│
    │ - Target    │    │ 2. For each pt:  │    │ 2. Reachability │
    │ - Distance  │    │   • dx, dy       │    │ 3. Physical ang │
    │             │    │   • atan2()      │    │                 │
    └─────────────┘    └──────────────────┘    └─────────────────┘
            │                    │                        │
            ▼                    ▼                        ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    MAIN COORDINATOR                         │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
    │  │    MATH     │  │    SERVO    │  │    VISUALIZATIONS   │  │
    │  │   ENGINE    │  │   ENGINE    │  │                     │  │
    │  │             │  │             │  │ ├─ geometric.py     │  │
    │  │ Geometric   │──┤ Interpolate │──┤ ├─ progression.py   │  │
    │  │ Angles      │  │ & Check     │  │ ├─ point_calc.py    │  │
    │  │             │  │ Limits      │  │ ├─ table.py         │  │
    │  │             │  │             │  │ └─ servo_vis.py     │  │
    │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  OUTPUT FILES   │
                    │                 │
                    │ 📁 output/      │
                    │ ├─ 01-07.png    │
                    │ └─ point_calc/  │
                    │    └─ 04_X.png  │
                    └─────────────────┘
```

## ⚙️ Kern-Algorithmus

```
INPUT: Scanner(0,0), Target(100,0), Distance=100cm, Points=10

STEP 1: Geometric Calculation
step = distance / (points - 1)  // 11.11cm
for i in range(points):
    y = i * step
    dx = target_x - scanner_x    // 100
    dy = target_y - y            // 0 to -100
    angle = atan2(dx, dy) * 180/π  // 90° to 135°

STEP 2: Servo Mapping
servo_coord = angle + 45 + 180  // -45° to 0°
if -135° ≤ servo_coord ≤ -45°:
    physical = servo_coord + 135  // 0° to 90°
    status = REACHABLE
else:
    status = UNREACHABLE

STEP 3: Visualization
save main files to output/
save point calcs to output/point_calculations/
```

## 🚀 Schnellstart

```python
# Vollständige Analyse
python main.py

# Nur Berechnungen
from main import get_servo_angles
angles = get_servo_angles()

# Spezifische Visualisierung
from visualizations.geometric import create_geometric_visualization
create_geometric_visualization(angles)
```

## 📋 Feature-Kontrolle (config.py)

```python
ENABLE_VISUALIZATIONS = {
    'geometric_representation': True,   # Scanner-Setup
    'angle_progression': True,         # Winkel-Verlauf  
    'point_calculations': True,        # Detail-Berechnungen
    'calculation_table': True,         # Ergebnis-Tabelle
    'servo_interpolation': True,       # Servo-Diagramm
    'servo_cone_detail': True,         # Servo-Kegel
}
```

**Aktueller Status: SCAN_DISTANCE=100cm, 10 Punkte, 100% erreichbar, Subfolder aktiv** ✅

## 🎓 ADD-ONS: `addons/`

```
🏫 target_coord_explanation/
└── target_coord_angle_explanation.py  ← Erweiterte Erklärungen
```

## 🔧 Integration & API

```python
# Direkte Integration
from main import get_servo_angles
from visualizations.geometric import create_geometric_visualization

angles = get_servo_angles()         # Nur Daten
create_geometric_visualization()    # Spezifische Visualisierung

# Daten-Struktur
angle_data = {
    'point': 1,
    'y_position': 0.0,
    'dx': 100, 'dy': 0.0,
    'angle': 90.0,
    'distance': 100.0
}
```

**Kompakte Mathematik-Engine für präzise 3D-Scanner Servoansteuerung** 🎯
