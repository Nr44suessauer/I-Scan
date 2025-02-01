import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Arc
import os

# Punkte definieren
P = (0, 0)
C = (150, 0)
M = (0, 150)
newCenter = (150, 75)
baseline = (0, 75)

# Setup für Animation
fig, ax = plt.subplots(figsize=(8, 8))

# Statische Elemente (Dreiecke, Winkel, Beschriftungen)
x_values1 = [P[0], M[0], C[0], P[0]]
y_values1 = [P[1], M[1], C[1], P[1]]
line1, = ax.plot(x_values1, y_values1, marker='o', color='blue', label='Regular Vision')

x_values2 = [newCenter[0], baseline[0], M[0], newCenter[0]]
y_values2 = [newCenter[1], baseline[1], M[1], newCenter[1]]
line2, = ax.plot(x_values2, y_values2, marker='o', linestyle='--', color='green', label='Over Baseline')

x_values3 = [P[0], newCenter[0], baseline[0], P[0]]
y_values3 = [P[1], newCenter[1], baseline[1], P[1]]
line3, = ax.plot(x_values3, y_values3, marker='o', linestyle='-.', color='red', label='Under Baseline')

# Annotationen
ax.annotate('Initial Position\n (0, 0)', xy=P, xytext=(-30, -10), textcoords='offset points', fontsize=12)
ax.annotate('Z max unit\n (0, 150)', xy=M, xytext=(-70, 10), textcoords='offset points', fontsize=12)
ax.annotate('Center\n (150, 0)', xy=C, xytext=(10, -20), textcoords='offset points', fontsize=12)
ax.annotate('New Center\n(150, 75)', xy=newCenter, xytext=(10, 10), textcoords='offset points', fontsize=12)
ax.annotate('Our defined\nBaseLine\n(0, 75)', xy=baseline, xytext=(-60, 10), textcoords='offset points', fontsize=12)

# Dynamische Elemente (Benis-Punkt und Verbindungslinie)
benis_point, = ax.plot([0], [0], 'o', markersize=10, color='purple', label='VisionLine to Center')
benis_line, = ax.plot([0, 150], [0, 75], 'k--')

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
    return benis_point, benis_line

# Animation erstellen
ani = FuncAnimation(
    fig,
    update,
    frames=range(0, 63),  # etwa 10 Sekunden bei 60ms pro Frame
    interval=60,
    blit=True
)

plt.xlabel('Distance to Center (cm)')
plt.ylabel('Z-Distance (cm)')
plt.legend(loc='upper right')

folder = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(folder, "animation.gif")
writer = PillowWriter(fps=15)  # fps kann je nach gewünschter Geschwindigkeit angepasst werden
ani.save(output_path, writer=writer)
plt.show()
