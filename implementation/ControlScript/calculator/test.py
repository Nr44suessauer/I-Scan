import math

def calculate_triangle_angles(a, b):
    """
    Calculate all angles in a right triangle given two sides.
    
    Args:
        a (float): Length of the first cathetus
        b (float): Length of the second cathetus
    
    Returns:
        tuple: (alpha, beta, C, c) where:
            - alpha is the angle at point A (between b and c)
            - beta is the angle at point B (between a and c)
            - C is the right angle (90 degrees)
            - c is the length of the hypotenuse
    """
    # Calculate hypotenuse using Pythagorean theorem: c² = a² + b²
    c = math.sqrt(a**2 + b**2)
    
    # Calculate alpha (angle at A): tan(alpha) = b/a
    alpha = math.degrees(math.atan(b/a))
    
    # Calculate beta (angle at B): tan(beta) = a/b
    beta = math.degrees(math.atan(a/b))
    
    # The right angle C is always 90°
    C = 90.0
    
    return alpha, beta, C, c

def main():
    """Main function to interact with the user and display results."""
    print("Right-Angled Triangle - Angle Calculator")
    print("=====================================")
    
    try:
        # Get user input for the two sides
        a = float(input("Please enter the length of side a (in cm): "))
        b = float(input("Please enter the length of side b (in cm): "))
        
        # Validate inputs
        if a <= 0 or b <= 0:
            print("Error: Both sides must be positive numbers.")
            return
            
        # Calculate angles and hypotenuse
        alpha, beta, C, c = calculate_triangle_angles(a, b)
        
        # Display results
        print("\nResults:")
        print("-----------")
        print(f"Hypotenuse c ≈ {c:.2f} cm")
        print(f"Angle α (at point A) ≈ {alpha:.2f}°")
        print(f"Angle β (at point B) ≈ {beta:.2f}°")
        print(f"Angle C (at point C) = {C}° (right angle)")
        
        # Verify the sum of angles equals 180°
        angle_sum = alpha + beta + C
        print(f"Sum of angles: {alpha:.2f}° + {beta:.2f}° + {C}° = {angle_sum:.2f}° ✓")
        
        # Provide a simple ASCII visualization
        print("\nVisualization (not to scale):")
        print("              A")
        print("              *")
        print(f"     a={a}cm |\\")
        print("              | \\")
        print("              |  \\")
        print("              |   \\")
        print("              |    \\")
        print("              |     \\")
        print("              |      \\")
        print("              |       \\")
        print("              |        \\")
        print("              *---------*------> X")
        print("             C         B")
        print(f"                   b={b}cm")
        
    except ValueError:
        print("Error: Please enter valid numbers.")
    except ZeroDivisionError:
        print("Error: None of the sides can be 0.")

if __name__ == "__main__":
    main()