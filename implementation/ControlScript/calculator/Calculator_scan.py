# Calculator_scan.py
# Kombiniert Werte aus der Web-Variante mit der Dreiecksberechnung
from dreiecksrechner_2quadranten import berechne_dreieck
import math
import matplotlib.pyplot as plt

# Beispielwerte wie in old_from_website.md (können angepasst werden)
pY = 0.0           # Y von Punkt P
zX = 0.0           # X von Z-Modul
nX = 150.0         # X von neuem Zentrum
nY = 30.0          # Y von neuem Zentrum
deltaScan = 150.0   # z.B. 30 cm Scanbereich
numberOfMeasurements = 10

# Berechnung der Schrittweite (wie in JS: result = deltaScan / numberOfMeasurements)
if numberOfMeasurements > 0:
    result = deltaScan / numberOfMeasurements
else:
    result = 0

print(f"Schrittweite: {result:.2f} cm pro Messung")

# Tabelle wie auf der Webseite: für jede Messung den Winkel und die Koordinate berechnen
table = []
for i in range(numberOfMeasurements):
    currentY = pY + result * i
    dx = nX - zX
    dy = nY - currentY
    angle = math.atan2(dy, dx) * 180 / math.pi
    angle_corr = abs(90 - angle)
    # Dreiecksberechnung: a = Abstand Z-Modul (currentY), b = Abstand zum Zentrum (dx), gamma=90°
    a = abs(dy)
    b = abs(dx)
    gamma = 90.0
    try:
        dreieck = berechne_dreieck(a=a, b=b, gamma=gamma)
        alpha = dreieck['alpha']
        beta = dreieck['beta']
        c = dreieck['c']
    except Exception as e:
        alpha = beta = c = None
    table.append({
        'Messung': i+1,
        'Angle (°)': round(angle_corr, 2),
        'Zmodule (X,Y)': (zX, round(currentY, 2)),
        'a': a,
        'b': b,
        'c': c,
        'alpha': alpha,
        'beta': beta
    })

# Ausgabe als Tabelle
print(f"{'#':<3} {'Angle':<8} {'Zmodule (X,Y)':<18} {'a':<8} {'b':<8} {'c':<8} {'alpha':<8} {'beta':<8}")
for row in table:
    print(f"{row['Messung']:<3} {row['Angle (°)']:<8} {str(row['Zmodule (X,Y)']):<18} {row['a']:<8.2f} {row['b']:<8.2f} {row['c'] if row['c'] is not None else '-':<8} {row['alpha'] if row['alpha'] is not None else '-':<8} {row['beta'] if row['beta'] is not None else '-':<8}")

# --- Visuelle Ausgabe als Diagramm ---
angles = [row['Angle (°)'] for row in table]
ys = [row['Zmodule (X,Y)'][1] for row in table]
alphas = [row['alpha'] for row in table]
betas = [row['beta'] for row in table]
cs = [row['c'] for row in table]

plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.plot(range(1, numberOfMeasurements+1), angles, marker='o', label='Angle (°)')
plt.xlabel('Messung')
plt.ylabel('Angle (°)')
plt.title('Winkel pro Messung')
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(range(1, numberOfMeasurements+1), ys, marker='o', color='green', label='Zmodule Y')
plt.xlabel('Messung')
plt.ylabel('Y-Koordinate')
plt.title('Y-Koordinate des Z-Moduls')
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(range(1, numberOfMeasurements+1), alphas, marker='o', color='purple', label='Alpha (°)')
plt.plot(range(1, numberOfMeasurements+1), betas, marker='o', color='orange', label='Beta (°)')
plt.xlabel('Messung')
plt.ylabel('Winkel (°)')
plt.title('Alpha/Beta pro Messung')
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(range(1, numberOfMeasurements+1), cs, marker='o', color='red', label='c (Seite)')
plt.xlabel('Messung')
plt.ylabel('c (cm)')
plt.title('Seite c pro Messung')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# --- Visualisierung: Ein Dreieck, alle Messpunkte als Linie von C zu Zmodule ---
fig, ax = plt.subplots(figsize=(8, 8))

# Wir nehmen das letzte berechnete Dreieck als Referenz (z.B. das für die letzte Messung)
last_row = table[-1]
a = last_row['a']
b = last_row['b']
c = last_row['c']
if None not in (a, b, c):
    # Eckpunkte: A=(0,0), B=(0,a), C=(b,0)
    A = (0, 0)
    B = (0, a)
    C = (b, 0)
    # Dreieck zeichnen
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'o-', color='blue', label='Dreieck')
    ax.annotate('A', A, textcoords='offset points', xytext=(-10,-10), fontsize=12)
    ax.annotate('B', B, textcoords='offset points', xytext=(-10,10), fontsize=12)
    ax.annotate('C', C, textcoords='offset points', xytext=(10,-10), fontsize=12)

    # Alle Messpunkte (Zmodule Y) und Linien von C zu diesen Punkten
    for row in table:
        zm_x, zm_y = row['Zmodule (X,Y)']
        # Zmodule-Punkt einzeichnen
        ax.plot(zm_x, zm_y, 'ko', markersize=5)
        # Linie von C zu Zmodule
        ax.plot([C[0], zm_x], [C[1], zm_y], 'r--', alpha=0.6)
        # Optional: Messpunkt-Nummer
        ax.annotate(f"{row['Messung']}", (zm_x, zm_y), textcoords='offset points', xytext=(5,5), fontsize=8, color='darkred')

    ax.set_aspect('equal')
    margin = max(a, b, c) * 0.3
    ax.set_xlim(min(0, b) - margin, max(b, 0) + margin)
    ax.set_ylim(-margin, max(a, b, c) + margin)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Dreieck mit allen Messpunkten (Zmodule Y) und Linien zu C')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()

# --- Tabellarische Ausgabe der Winkel und Seiten ---
from tabulate import tabulate

winkel_tabelle = []
for row in table:
    winkel_tabelle.append([
        row['Messung'],
        row['Angle (°)'],
        row['a'],
        row['b'],
        row['c'],
        row['alpha'],
        row['beta']
    ])

headers = ["#", "Angle (°)", "a", "b", "c", "alpha (°)", "beta (°)"]
print("\nWinkel- und Seiten-Tabelle:")
try:
    print(tabulate(winkel_tabelle, headers=headers, floatfmt=".2f"))
except Exception:
    # Fallback falls tabulate nicht installiert ist
    print(f"{headers[0]:<3} {headers[1]:<10} {headers[2]:<8} {headers[3]:<8} {headers[4]:<8} {headers[5]:<12} {headers[6]:<12}")
    for row in winkel_tabelle:
        print(f"{row[0]:<3} {row[1]:<10.2f} {row[2]:<8.2f} {row[3]:<8.2f} {row[4] if row[4] is not None else '-':<8} {row[5] if row[5] is not None else '-':<12} {row[6] if row[6] is not None else '-':<12}")
