import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Arc
import os

# Variable to control the animation: 1 = on, 0 = off
animation_enabled = 1

# Define points
P = (0, 0)
M = (0, 150)
newCenter = (150, 75)
oldCenter = (150, 0)  # New point: oldCenter
baseline = (0, 75)    # Baseline (no longer used directly here)

# Setup for animation/plot
fig, ax = plt.subplots(figsize=(8, 8))

# Static elements (triangles, lines, labels)
x_values2 = [newCenter[0], baseline[0], M[0], newCenter[0]]
y_values2 = [newCenter[1], baseline[1], M[1], newCenter[1]]
line2, = ax.plot(x_values2, y_values2, marker='o', linestyle='--', color='green', label='Over newCenter')

x_values3 = [P[0], newCenter[0], baseline[0], P[0]]
y_values3 = [P[1], newCenter[1], baseline[1], P[1]]
line3, = ax.plot(x_values3, y_values3, marker='o', linestyle='-.', color='red', label='Under newCenter')

# Annotations for existing points
ax.annotate('Initial Position\n(0, 0)', xy=P, xytext=(-30, -30), textcoords='offset points', fontsize=12)
ax.annotate('Max Z Value\n(0, 150)', xy=M, xytext=(-30, 10), textcoords='offset points', fontsize=12)
ax.annotate('New Center\n(150, 75)', xy=newCenter, xytext=(-30, 30), textcoords='offset points', fontsize=12)

# Add oldCenter and connecting line to newCenter
oldcenter_point, = ax.plot(oldCenter[0], oldCenter[1], marker='o', markersize=8, color='blue')
line_old_new, = ax.plot([newCenter[0], oldCenter[0]], [newCenter[1], oldCenter[1]], linestyle='--', color='blue')
ax.annotate('Old Center\n(150, 0)', xy=oldCenter, xytext=(-20, -30), textcoords='offset points', fontsize=12)

# Dynamic elements (updated in the animation)
zmodule_point, = ax.plot([0], [0], 'o', markersize=10, color='purple', label='Z module')
zmodule_line, = ax.plot([0, 150], [0, 75], 'k--')

# Text object to display the angle at the Z module
angle_annotation = ax.text(0, 0, "", fontsize=12, color='purple', verticalalignment='bottom')

# Arc patch to visualize the angle range (radius fixed at 20)
angle_arc = Arc((0, 0), 40, 40, angle=0, theta1=0, theta2=0, color='purple', lw=2)
ax.add_patch(angle_arc)

# Axis settings
ax.set_xlim(-20, 170)
ax.set_ylim(-20, 175)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

def update(frame):
    # zmodule moves vertically from 0 to 150
    y_pos = 150 * abs(math.sin(frame * 0.1))
    zmodule_point.set_data([0], [y_pos])
    zmodule_line.set_data([0, 150], [y_pos, 75])
    
    # Calculate the absolute angle of the line (from zmodule_point to newCenter)
    # In the standard coordinate system: 0° is horizontal. The vertical reference corresponds to 90°.
    # Therefore: alpha = angle of the connecting line (relative to the horizontal)
    alpha = math.degrees(math.atan2(newCenter[1] - y_pos, newCenter[0] - 0))
    # The angle relative to the Y-axis is:
    angle_v = abs(90 - alpha)
    
    # Update the angle display at the Z module
    angle_annotation.set_position((0, y_pos))
    angle_annotation.set_text(f"Angle: {angle_v:.1f}°")
    
    # Update the Arc patch:
    # The Arc shows the angle between the vertical line (90°) and the connecting line.
    # We set theta1 and theta2 so that the Arc always represents the smaller angle.
    start_angle = 90
    end_angle = alpha
    if end_angle < 90:
        start_angle, end_angle = end_angle, 90
    angle_arc.center = (0, y_pos)
    angle_arc.theta1 = start_angle
    angle_arc.theta2 = end_angle

    return zmodule_point, zmodule_line, angle_annotation, angle_arc

plt.xlabel('Distance to Center (cm)')
plt.ylabel('Z-Distance (cm)')
plt.legend(loc='upper right')

folder = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(folder, "Triangle_newCenter.gif")

if animation_enabled:
    ani = FuncAnimation(
        fig,
        update,
        frames=range(0, 63),  # ~10 seconds at 200ms per frame
        interval=200,
        blit=True
    )
    writer = PillowWriter(fps=3)  # 3 frames per second
    ani.save(output_path, writer=writer)
else:
    # When animation is disabled: set zmodule point at (0,35)
    y_pos = 35
    zmodule_point.set_data([0], [y_pos])
    zmodule_line.set_data([0, 150], [y_pos, 75])
    
    alpha = math.degrees(math.atan2(newCenter[1] - y_pos, newCenter[0] - 0))
    angle_v = abs(90 - alpha)
    
    angle_annotation.set_position((0, y_pos))
    angle_annotation.set_text(f"Angle: {angle_v:.1f}°")
    
    start_angle = 90
    end_angle = alpha
    if end_angle < 90:
        start_angle, end_angle = end_angle, 90
    angle_arc.center = (0, y_pos)
    angle_arc.theta1 = start_angle
    angle_arc.theta2 = end_angle

plt.show()
