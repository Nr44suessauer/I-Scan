import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# Define points (all coordinates in cm)
P = (0, 0)           # Initial position
C = (150, 0)         # Center
M = (0, 150)         # Measurement Unit position
newCenter = (150, 75)  # New Center
baseline = (0, 75)     # Baseline

# Coordinates for Triangle 1 (P, M, C)
x_values1 = [P[0], M[0], C[0], P[0]]
y_values1 = [P[1], M[1], C[1], P[1]]

# Coordinates for Triangle 2 (newCenter, baseline, M)
x_values2 = [newCenter[0], baseline[0], M[0], newCenter[0]]
y_values2 = [newCenter[1], baseline[1], M[1], newCenter[1]]

# Coordinates for Triangle 3 (P, newCenter, baseline)
x_values3 = [P[0], newCenter[0], baseline[0], P[0]]
y_values3 = [P[1], newCenter[1], baseline[1], P[1]]

# Calculate angles in degrees for each triangle using the atan2 function
# Triangle 1: angle at M between segments M->C and M->P
angle1 = math.degrees(math.atan2(C[1] - M[1], C[0] - M[0]) - math.atan2(P[1] - M[1], P[0] - M[0]))
if angle1 < 0:
    angle1 += 360

# Triangle 2: angle at M between segments M->newCenter and M->baseline
angle2 = math.degrees(math.atan2(newCenter[1] - M[1], newCenter[0] - M[0]) - math.atan2(baseline[1] - M[1], baseline[0] - M[0]))
if angle2 < 0:
    angle2 += 360

# Triangle 3: now calculate the angle at P (Initial Position) with inverted order
angle3 = math.degrees(math.atan2(baseline[1] - P[1], baseline[0] - P[0]) - math.atan2(newCenter[1] - P[1], newCenter[0] - P[0]))
if angle3 < 0:
    angle3 += 360

# Create the plot
plt.figure(figsize=(8, 8))

# Plot triangles with labels
line1, = plt.plot(x_values1, y_values1, marker='o', label='Regular Vision', linestyle='-', color='blue')
line2, = plt.plot(x_values2, y_values2, marker='o', label='Over Baseline', linestyle='--', color='green')
line3, = plt.plot(x_values3, y_values3, marker='o', label='Under Baseline', linestyle='-.', color='red')

# Annotate the key points with improved formatting and offsets for clarity
plt.annotate('Initial Position\n (0, 0)', xy=P, xytext=(-30, -10),
             textcoords='offset points', fontsize=12, color='black', arrowprops=dict(arrowstyle='->', color='gray'))

plt.annotate('Z max unit\n (0, 150)', xy=M, xytext=(-70, 10),
             textcoords='offset points', fontsize=12, color='black', arrowprops=dict(arrowstyle='->', color='gray'))

plt.annotate('Center\n (150, 0)', xy=C, xytext=(10, -20),
             textcoords='offset points', fontsize=12, color='black', arrowprops=dict(arrowstyle='->', color='gray'))

plt.annotate('New Center\n(150, 75)', xy=newCenter, xytext=(10, 10),
             textcoords='offset points', fontsize=12, color='black', arrowprops=dict(arrowstyle='->', color='gray'))

plt.annotate('Our defined\nBaseLine\n(0, 75)', xy=baseline, xytext=(-60, 10),
             textcoords='offset points', fontsize=12, color='black', arrowprops=dict(arrowstyle='->', color='gray'))

# Draw arcs for each angle with a fixed radius
arc_radius = 15

# --- Winkel in Triangle 1 (bei M) ---
start_angle1 = math.degrees(math.atan2(P[1] - M[1], P[0] - M[0]))
end_angle1 = math.degrees(math.atan2(C[1] - M[1], C[0] - M[0]))
if end_angle1 < start_angle1:
    end_angle1 += 360
arc1 = Arc(M, 2*arc_radius, 2*arc_radius, angle=0, theta1=start_angle1, theta2=end_angle1, color='blue', lw=2)
plt.gca().add_patch(arc1)
mid_angle1 = math.radians((start_angle1 + end_angle1) / 2)
x_text1 = M[0] + (arc_radius + 5) * math.cos(mid_angle1)
y_text1 = M[1] + (arc_radius + 5) * math.sin(mid_angle1)
plt.text(x_text1, y_text1, f'{angle1:.1f}°', color='blue', fontsize=12)

# --- Winkel in Triangle 2 (bei M) ---
start_angle2 = math.degrees(math.atan2(baseline[1] - M[1], baseline[0] - M[0]))
end_angle2 = math.degrees(math.atan2(newCenter[1] - M[1], newCenter[0] - M[0]))
if end_angle2 < start_angle2:
    end_angle2 += 360
arc2 = Arc(M, 2*arc_radius, 2*arc_radius, angle=0, theta1=start_angle2, theta2=end_angle2, color='green', lw=2)
plt.gca().add_patch(arc2)
mid_angle2 = math.radians((start_angle2 + end_angle2) / 2)
x_text2 = M[0] + (arc_radius + 5) * math.cos(mid_angle2)
y_text2 = M[1] + (arc_radius + 5) * math.sin(mid_angle2)
plt.text(x_text2, y_text2, f'{angle2:.1f}°', color='green', fontsize=12)


# --- Winkel in Triangle 3 (bei P, Initial Position) ---  
# Anzeige invertieren: Es wird von newCenter zu baseline gemessen  
start_angle3 = math.degrees(math.atan2(newCenter[1] - P[1], newCenter[0] - P[0]))
end_angle3 = math.degrees(math.atan2(baseline[1] - P[1], baseline[0] - P[0]))
if end_angle3 < start_angle3:
    end_angle3 += 360
arc3 = Arc(P, 2*arc_radius, 2*arc_radius, angle=0, theta1=start_angle3, theta2=end_angle3, color='red', lw=2)
plt.gca().add_patch(arc3)
mid_angle3 = math.radians((start_angle3 + end_angle3) / 2)
x_text3 = P[0] + (arc_radius + 5) * math.cos(mid_angle3)
y_text3 = P[1] + (arc_radius + 5) * math.sin(mid_angle3)
plt.text(x_text3, y_text3, f'{angle3:.1f}°', color='red', fontsize=12)

# Create legend for the triangles and position it at the top right
plt.legend(handles=[line1, line2, line3], loc='upper right', fontsize=12)

# Prepare angle information
angle_info = (f'AngleBlue : {angle1:.2f}°\n'
              f'AngleRed  : {angle2:.2f}°\n'
              f'AngleGreen: {angle3:.2f}°')

# Display the angle information below the diagram
plt.gcf().text(0.5, 0.01, angle_info, fontsize=12, ha='center', va='bottom',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# Set axis labels and title
plt.xlabel('Distance to Center (cm)', fontsize=14)
plt.ylabel('Z-Distance (cm)', fontsize=14)
plt.title('', fontsize=16)

# Ensure the aspect ratio is equal to avoid distortion
plt.gca().set_aspect('equal', adjustable='box')

# Set axis limits to include all points with some margin
all_x = [P[0], C[0], M[0], newCenter[0], baseline[0]]
all_y = [P[1], C[1], M[1], newCenter[1], baseline[1]]
plt.xlim(min(all_x) - 20, max(all_x) + 20)
plt.ylim(min(all_y) - 20, max(all_y) + 20)

# Optional: add grid for better readability
plt.grid(True, linestyle='--', alpha=0.6)

# Show the plot
plt.show()
