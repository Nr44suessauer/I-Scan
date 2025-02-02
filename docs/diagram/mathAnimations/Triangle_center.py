import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patches as patches
import os

# Flag to toggle the animation: 1 = Animation on, 0 = static image
animate_flag = 0  # Change this value to 0 to disable the animation

# Define points
P = (0, 0)
C = (150, 0)
M = (0, 150)

# Calculate the angle at Z max (M)
# Angle from M towards Center
ray_to_C_rad_M = math.atan2(0 - M[1], C[0])
ray_to_C_deg_M = math.degrees(ray_to_C_rad_M)
internal_angle_M = ray_to_C_deg_M - (-90)

# Setup for the plot
fig, ax = plt.subplots(figsize=(8, 8))

# Static element (blue triangle as the Visionfield)
x_values1 = [P[0], M[0], C[0], P[0]]
y_values1 = [P[1], M[1], C[1], P[1]]
ax.plot(x_values1, y_values1, marker='o', color='blue', label='Visionfield')

# Annotations for the static points
ax.annotate('Initial Position\n (0, 0)', xy=P, xytext=(-30, -50), textcoords='offset points', fontsize=12)
ax.annotate('Z max\n (0, 150)', xy=M, xytext=(-50, 20), textcoords='offset points', fontsize=12)
ax.annotate('Center\n (150, 0)', xy=C, xytext=(10, -20), textcoords='offset points', fontsize=12)

# New annotation for the angle at Z max (M) in blue
ax.annotate(f'Angle: {internal_angle_M:.1f}°', xy=M, xytext=(10, -10),
            textcoords='offset points', fontsize=12, color='blue')

# Arc at Z max (M) in blue
arc_M = patches.Arc(M, 40, 40, angle=0, theta1=-90, theta2=ray_to_C_deg_M, color='blue')
ax.add_patch(arc_M)

# Dynamic elements (purple ZModule point and the connecting line Visionline)
zmodule_point, = ax.plot([0], [0], 'o', markersize=10, color='purple', label='ZModule')
vision_line, = ax.plot([0, C[0]], [0, C[1]], linestyle='--', color='violet', label='Visionline')

# Text object to display the angle (positioned in data coordinates)
angle_text = ax.text(5, 0, '', fontsize=12, verticalalignment='top')

# Angle arc (starting at 0, will be updated in the function)
arc = patches.Arc((0, 0), 40, 40, angle=0, theta1=0, theta2=0, color='red')
ax.add_patch(arc)

# Axis settings
ax.set_xlim(-20, 170)
ax.set_ylim(-20, 175)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

def update(frame):
    # ZModule moves vertically from 0 to 150
    y_pos = 150 * abs(math.sin(frame * 0.1))
    zmodule_point.set_data([0], [y_pos])
    vision_line.set_data([0, C[0]], [y_pos, C[1]])
    
    # Calculate the angle from the ZModule point to the Center
    ray_to_C_rad = math.atan2(0 - y_pos, C[0])
    ray_to_C_deg = math.degrees(ray_to_C_rad)
    
    # The inner triangle angle at the ZModule point:
    internal_angle = ray_to_C_deg - (-90)
    
    # Update the text
    angle_text.set_text(f"Angle: {internal_angle:.1f}°")
    angle_text.set_position((5, y_pos - 20))
    
    # Update the angle arc
    arc.center = (0, y_pos)
    arc.theta1 = -90
    arc.theta2 = ray_to_C_deg

    return zmodule_point, vision_line, angle_text, arc

if animate_flag:
    # Create animation when animate_flag == 1
    ani = FuncAnimation(
        fig,
        update,
        frames=range(0, 63),  # roughly 10 seconds at 200ms per frame
        interval=200,
        blit=False
    )
    
    folder = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(folder, "Triangle_center.gif")
    writer = PillowWriter(fps=1)  # 1 frame per second for GIF export
    ani.save(output_path, writer=writer)
else:
    # Static image: ZModule at fixed height (0, 75)
    y_pos = 75
    zmodule_point.set_data([0], [y_pos])
    vision_line.set_data([0, C[0]], [y_pos, C[1]])
    
    # Calculate the angle from the ZModule point to the Center
    ray_to_C_rad = math.atan2(0 - y_pos, C[0])
    ray_to_C_deg = math.degrees(ray_to_C_rad)
    internal_angle = ray_to_C_deg - (-90)
    
    angle_text.set_text(f"Angle: {internal_angle:.1f}°")
    angle_text.set_position((5, y_pos - 20))
    
    arc.center = (0, y_pos)
    arc.theta1 = -90
    arc.theta2 = ray_to_C_deg

plt.xlabel('Distance to Center (cm)')
plt.ylabel('Z-Distance (cm)')
plt.legend(loc='upper right')
plt.show()
