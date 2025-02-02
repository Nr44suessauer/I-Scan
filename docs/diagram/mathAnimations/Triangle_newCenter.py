import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Arc
import os

# Variable zur Steuerung der Animation: 1 = an, 0 = aus
animation_enabled = 1

# Punkte definieren
P = (0, 0)
M = (0, 150)
newCenter = (150, 75)
oldCenter = (150, 0)  # Neuer Punkt: oldCenter
baseline = (0, 75)    # Baseline (wird hier nicht mehr direkt genutzt)

# Setup für Animation/Plot
fig, ax = plt.subplots(figsize=(8, 8))

# Statische Elemente (Dreiecke, Linien, Beschriftungen)
x_values2 = [newCenter[0], baseline[0], M[0], newCenter[0]]
y_values2 = [newCenter[1], baseline[1], M[1], newCenter[1]]
line2, = ax.plot(x_values2, y_values2, marker='o', linestyle='--', color='green', label='Over newCenter')

x_values3 = [P[0], newCenter[0], baseline[0], P[0]]
y_values3 = [P[1], newCenter[1], baseline[1], P[1]]
line3, = ax.plot(x_values3, y_values3, marker='o', linestyle='-.', color='red', label='Under newCenter')

# Annotationen für bestehende Punkte
ax.annotate('Initial Position\n (0, 0)', xy=P, xytext=(-30, -30), textcoords='offset points', fontsize=12)
ax.annotate('Z max unit\n (0, 150)', xy=M, xytext=(-30, 10), textcoords='offset points', fontsize=12)
ax.annotate('New Center\n(150, 75)', xy=newCenter, xytext=(-30, 30), textcoords='offset points', fontsize=12)

# Hinzufügen von oldCenter und Verbindungslinie zu newCenter
oldcenter_point, = ax.plot(oldCenter[0], oldCenter[1], marker='o', markersize=8, color='blue')
line_old_new, = ax.plot([newCenter[0], oldCenter[0]], [newCenter[1], oldCenter[1]], linestyle='--', color='blue')
ax.annotate('Old Center\n(150, 0)', xy=oldCenter, xytext=(-20, -30), textcoords='offset points', fontsize=12)

# Dynamische Elemente (werden in der Animation aktualisiert)
benis_point, = ax.plot([0], [0], 'o', markersize=10, color='purple', label='Zmodule')
benis_line, = ax.plot([0, 150], [0, 75], 'k--')

# Text-Objekt zur Anzeige des Winkels am Zmodule
angle_annotation = ax.text(0, 0, "", fontsize=12, color='purple', verticalalignment='bottom')

# Arc-Patch zum Visualisieren des Winkelbereichs (Radius festgelegt auf 20)
angle_arc = Arc((0, 0), 40, 40, angle=0, theta1=0, theta2=0, color='purple', lw=2)
ax.add_patch(angle_arc)

# Achseneinstellungen
ax.set_xlim(-20, 170)
ax.set_ylim(-20, 175)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

def update(frame):
    # Benis bewegt sich vertikal von 0 bis 150
    y_pos = 150 * abs(math.sin(frame * 0.1))
    benis_point.set_data([0], [y_pos])
    benis_line.set_data([0, 150], [y_pos, 75])
    
    # Berechnung des absoluten Winkels der Linie (benis_point -> newCenter)
    # Im Standardkoordinatensystem: 0° ist horizontal. Der vertikale Bezug entspricht 90°.
    # Daher: alpha = Winkel der Verbindungslinie (relativ zur Horizontalen)
    alpha = math.degrees(math.atan2(newCenter[1] - y_pos, newCenter[0] - 0))
    # Der Winkel relativ zur Y-Achse beträgt somit:
    angle_v = abs(90 - alpha)
    
    # Aktualisierung der Winkelanzeige am Punkt Zmodule
    angle_annotation.set_position((0, y_pos))
    angle_annotation.set_text(f"Winkel: {angle_v:.1f}°")
    
    # Aktualisiere den Arc-Patch:
    # Arc zeigt den Winkel zwischen der vertikalen Linie (90°) und der Verbindungslinie.
    # Wir ordnen theta1 und theta2 so, dass der Arc immer den kleineren Bogen darstellt.
    start_angle = 90
    end_angle = alpha
    if end_angle < 90:
        start_angle, end_angle = end_angle, 90
    angle_arc.center = (0, y_pos)
    angle_arc.theta1 = start_angle
    angle_arc.theta2 = end_angle

    return benis_point, benis_line, angle_annotation, angle_arc

plt.xlabel('Distance to Center (cm)')
plt.ylabel('Z-Distance (cm)')
plt.legend(loc='upper right')

folder = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(folder, "Triangle_newCenter.gif")

if animation_enabled:
    ani = FuncAnimation(
        fig,
        update,
        frames=range(0, 63),  # ca. 10 Sekunden bei 60ms pro Frame
        interval=200,
        blit=True
    )
    writer = PillowWriter(fps=15)  # 15 Frames pro Sekunde
    ani.save(output_path, writer=writer)
else:
    # Bei deaktivierter Animation: Punkt "benis" auf (0,35)
    y_pos = 35
    benis_point.set_data([0], [y_pos])
    benis_line.set_data([0, 150], [y_pos, 75])
    
    alpha = math.degrees(math.atan2(newCenter[1] - y_pos, newCenter[0] - 0))
    angle_v = abs(90 - alpha)
    
    angle_annotation.set_position((0, y_pos))
    angle_annotation.set_text(f"Winkel: {angle_v:.1f}°")
    
    start_angle = 90
    end_angle = alpha
    if end_angle < 90:
        start_angle, end_angle = end_angle, 90
    angle_arc.center = (0, y_pos)
    angle_arc.theta1 = start_angle
    angle_arc.theta2 = end_angle

plt.show()
