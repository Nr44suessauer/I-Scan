import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc, Polygon
import numpy as np

class TriangleCalculator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.animation_running = False
        self.current_animation = None  # Speichert die aktuelle Animation
        
    def calculate_triangle_angles(self, a, b):
        """
        Berechnet alle Winkel in einem rechtwinkligen Dreieck bei gegebenen zwei Katheten.
        Akzeptiert auch negative Werte für a (Kathete in Y-Richtung).
        
        Args:
            a (float): Länge der ersten Kathete (kann negativ sein für 2. Quadrant)
            b (float): Länge der zweiten Kathete (muss positiv sein)
        
        Returns:
            dict: Wörterbuch mit allen Dreieckswerten
        """
        if b <= 0:
            raise ValueError("Kathete b muss positiv sein!")
        
        # Absolute Werte für Berechnungen verwenden
        a_abs = abs(a)
        b_abs = abs(b)
        
        # Hypotenuse berechnen: c² = a² + b²
        c = math.sqrt(a_abs**2 + b_abs**2)
        
        # Winkel Alpha (bei Punkt A): tan(alpha) = Gegenkathete/Ankathete = a/b
        alpha = math.degrees(math.atan(a_abs/b_abs))
        
        # Winkel Beta (bei Punkt B): tan(beta) = Gegenkathete/Ankathete = b/a
        beta = math.degrees(math.atan(b_abs/a_abs))
        
        # Rechter Winkel Gamma ist immer 90°
        gamma = 90.0
        
        # Fläche berechnen: A = (a * b) / 2
        area = (a_abs * b) / 2
        
        # Umfang berechnen: U = a + b + c
        perimeter = a_abs + b + c
        
        # Quadrant bestimmen
        quadrant = 1 if a >= 0 else 2
        
        return {
            'sides': {'a': a, 'a_abs': a_abs, 'b': b, 'c': c},
            'angles': {'alpha': alpha, 'beta': beta, 'gamma': gamma},
            'area': area, 
            'perimeter': perimeter,
            'quadrant': quadrant
        }
    
    def print_results(self, results):
        """Zeigt die Berechnungsergebnisse an."""
        print("\n" + "="*50)
        print("RECHTWINKLIGES DREIECK - BERECHNUNGSERGEBNISSE")
        print("="*50)
        
        sides = results['sides']
        angles = results['angles']
        quadrant = results['quadrant']
        
        print(f"\nQUADRANT: {quadrant}. Quadrant")
        if quadrant == 2:
            print("  (Kathete a ist negativ - Dreieck im 2. Quadranten)")
        
        print(f"\nSEITENLÄNGEN:")
        print(f"  Kathete a = {sides['a']:.2f} cm (|a| = {sides['a_abs']:.2f} cm)")
        print(f"  Kathete b = {sides['b']:.2f} cm")
        print(f"  Hypotenuse c = {sides['c']:.2f} cm")
        
        print(f"\nWINKEL:")
        print(f"  Winkel α (Alpha) = {angles['alpha']:.2f}°")
        print(f"  Winkel β (Beta) = {angles['beta']:.2f}°")
        print(f"  Winkel γ (Gamma) = {angles['gamma']:.2f}° (rechter Winkel)")
        
        # Verifikation
        angle_sum = angles['alpha'] + angles['beta'] + angles['gamma']
        print(f"\nVERIFIKATION:")
        print(f"  Winkelsumme: {angles['alpha']:.2f}° + {angles['beta']:.2f}° + {angles['gamma']:.2f}° = {angle_sum:.2f}° ✓")
        
        # Pythagoras-Verifikation
        pythagoras_check = math.sqrt(sides['a_abs']**2 + sides['b']**2)
        print(f"  Pythagoras: √({sides['a_abs']:.2f}² + {sides['b']:.2f}²) = {pythagoras_check:.2f} ≈ {sides['c']:.2f} ✓")
        
        # Wir entfernen die Ausgabe von Umfang und Flächeninhalt
        
        print("="*50)
    
    def visualize_static(self, results, show_construction=True):
        """Erstellt eine statische Visualisierung des Dreiecks."""
        self.ax.clear()
        
        sides = results['sides']
        angles = results['angles']
        quadrant = results['quadrant']
        
        # Dreieckspunkte definieren (C ist der rechte Winkel)
        C = (0, 0)  # Rechter Winkel am Ursprung
        A = (sides['b'], 0)  # Punkt A auf der x-Achse
        
        # B-Punkt je nach Quadrant positionieren
        if quadrant == 1:
            B = (0, sides['a_abs'])  # 1. Quadrant: positive Y-Koordinate
        else:  # quadrant == 2
            B = (0, -sides['a_abs'])  # 2. Quadrant: negative Y-Koordinate
        
        # Dreieck zeichnen
        triangle_points = [C, A, B, C]
        triangle_x = [point[0] for point in triangle_points]
        triangle_y = [point[1] for point in triangle_points]
        
        # Dreieck als gefüllte Fläche
        triangle_patch = Polygon([C, A, B], alpha=0.3, facecolor='lightblue', edgecolor='blue', linewidth=2)
        self.ax.add_patch(triangle_patch)
        
        # Dreieckskanten mit Labels
        self.ax.plot(triangle_x, triangle_y, 'b-', linewidth=2, marker='o', markersize=8)
        
        # Koordinatenachsen zeichnen
        max_side = max(sides['a_abs'], sides['b'])
        margin = max_side * 0.15
        
        # X-Achse
        self.ax.axhline(y=0, color='gray', linewidth=1, alpha=0.7)
        # Y-Achse  
        self.ax.axvline(x=0, color='gray', linewidth=1, alpha=0.7)
        
        # X-Achse als Mittellinie hervorheben (bei negativem a)
        if quadrant == 2:
            self.ax.axhline(y=0, color='black', linewidth=2, linestyle='-', alpha=0.9)
            self.ax.text(sides['b']/2, 0.5, 'X-Achse (Mittellinie)', ha='center', 
                        fontsize=10, color='black', fontweight='bold')
        
        # Punkte beschriften
        self.ax.annotate('C (90°)', xy=C, xytext=(-20, 10 if quadrant == 2 else -20), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        self.ax.annotate('A', xy=A, xytext=(10, -20), textcoords='offset points', 
                        fontsize=12, fontweight='bold')
        
        if quadrant == 1:
            self.ax.annotate('B', xy=B, xytext=(-20, 10), textcoords='offset points', 
                            fontsize=12, fontweight='bold')
        else:
            self.ax.annotate('B', xy=B, xytext=(-20, -20), textcoords='offset points', 
                            fontsize=12, fontweight='bold')
        
        # Seitenlängen beschriften
        mid_a = ((C[0] + B[0])/2, (C[1] + B[1])/2)
        mid_b = ((C[0] + A[0])/2, (C[1] + A[1])/2)
        mid_c = ((A[0] + B[0])/2, (A[1] + B[1])/2)
        
        # Kathete a Label
        a_offset_x = -30 if quadrant == 1 else -40
        a_offset_y = 0 if quadrant == 1 else 0
        self.ax.annotate(f'a = {sides["a"]:.1f} cm', xy=mid_a, xytext=(a_offset_x, a_offset_y), 
                        textcoords='offset points', fontsize=10, color='green', fontweight='bold')
        
        # Kathete b Label
        b_offset_y = -15 if quadrant == 1 else 15
        self.ax.annotate(f'b = {sides["b"]:.1f} cm', xy=mid_b, xytext=(0, b_offset_y), 
                        textcoords='offset points', fontsize=10, color='green', fontweight='bold')
        
        # Hypotenuse c Label
        c_offset_x = 10 if quadrant == 1 else 10
        c_offset_y = 10 if quadrant == 1 else -10
        self.ax.annotate(f'c = {sides["c"]:.1f} cm', xy=mid_c, xytext=(c_offset_x, c_offset_y), 
                        textcoords='offset points', fontsize=10, color='red', fontweight='bold')
        
        # Winkel visualisieren
        if show_construction:
            arc_radius = min(2, min(sides['a_abs'], sides['b']) * 0.15)
            
            # Rechter Winkel bei C
            square_size = min(1.5, min(sides['a_abs'], sides['b']) * 0.1)
            if quadrant == 1:
                square = plt.Rectangle((C[0], C[1]), square_size, square_size, 
                                     fill=False, edgecolor='red', linewidth=2)
            else:  # quadrant == 2
                square = plt.Rectangle((C[0], C[1]-square_size), square_size, square_size, 
                                     fill=False, edgecolor='red', linewidth=2)
            self.ax.add_patch(square)
            
            # Winkel Alpha bei A
            if quadrant == 1:
                alpha_arc = Arc(A, arc_radius*2, arc_radius*2, angle=0, 
                               theta1=90, theta2=90+angles['alpha'], 
                               color='orange', linewidth=2)
                alpha_text_pos = (A[0]-1.5, A[1]+0.5)
            else:  # quadrant == 2
                alpha_arc = Arc(A, arc_radius*2, arc_radius*2, angle=0, 
                               theta1=180+angles['alpha'], theta2=270, 
                               color='orange', linewidth=2)
                alpha_text_pos = (A[0]-1.5, A[1]-0.5)
            
            self.ax.add_patch(alpha_arc)
            self.ax.annotate(f'α = {angles["alpha"]:.1f}°', 
                           xy=alpha_text_pos, fontsize=10, color='orange', fontweight='bold')
            
            # Winkel Beta bei B
            if quadrant == 1:
                beta_arc = Arc(B, arc_radius*2, arc_radius*2, angle=0, 
                              theta1=270, theta2=270+angles['beta'], 
                              color='purple', linewidth=2)
                beta_text_pos = (B[0]+0.5, B[1]-1.5)
            else:  # quadrant == 2
                beta_arc = Arc(B, arc_radius*2, arc_radius*2, angle=0, 
                              theta1=90-angles['beta'], theta2=90, 
                              color='purple', linewidth=2)
                beta_text_pos = (B[0]+0.5, B[1]+1.5)
            
            self.ax.add_patch(beta_arc)
            self.ax.annotate(f'β = {angles["beta"]:.1f}°', 
                           xy=beta_text_pos, fontsize=10, color='purple', fontweight='bold')
        
        # Achsen und Grid
        max_side = max(sides['a_abs'], sides['b'])
        margin = max_side * 0.15
        
        self.ax.set_xlim(-margin, sides['b'] + margin)
        
        if quadrant == 1:
            self.ax.set_ylim(-margin, sides['a_abs'] + margin)
        else:  # quadrant == 2
            self.ax.set_ylim(-sides['a_abs'] - margin, margin)
        
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Breite (cm)', fontsize=12)
        self.ax.set_ylabel('Höhe (cm)', fontsize=12)
        
        # Quadrant-spezifischer Titel
        quadrant_text = f" - {quadrant}. Quadrant" if quadrant == 2 else ""
        title = f'Rechtwinkliges Dreieck{quadrant_text}: a={sides["a"]:.1f}cm, b={sides["b"]:.1f}cm, c={sides["c"]:.1f}cm'
        subtitle = f'Winkel: α={angles["alpha"]:.1f}°, β={angles["beta"]:.1f}°, γ=90°'
        self.ax.set_title(f'{title}\n{subtitle}', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def create_animated_construction(self, results):
        """Erstellt eine animierte Konstruktion des Dreiecks."""
        # Erzeuge eine neue Figure und Axes für jede Animation
        plt.close(self.fig)  # Schließe vorherige Figur
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        sides = results['sides']
        angles = results['angles']
        quadrant = results['quadrant']
        
        # Animation Setup
        frames = 150
        self.construction_data = {
            'frames': frames,
            'current_frame': 0,
            'sides': sides,
            'angles': angles,
            'quadrant': quadrant
        }
        
        def animate(frame):
            self.ax.clear()
            progress = frame / frames
            
            # Legende mit allen Werten
            legend_text = [
                "BERECHNETE WERTE:",
                "─" * 20,
                f"Quadrant: {quadrant}",
                f"Kathete a = {sides['a']:.2f} cm",
                f"Kathete b = {sides['b']:.2f} cm", 
                f"Hypotenuse c = {sides['c']:.2f} cm",
                "",
                f"Winkel α = {angles['alpha']:.2f}°",
                f"Winkel β = {angles['beta']:.2f}°", 
                f"Winkel γ = {angles['gamma']:.2f}°"
            ]
            
            legend_str = "\n".join(legend_text)
            textbox_props = dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.9, edgecolor="black")
            
            max_side = max(sides['a_abs'], sides['b'])
            margin = max_side * 0.15
            legend_x = sides['b'] + margin * 0.3
            
            if quadrant == 1:
                legend_y = sides['a_abs'] + margin * 0.5
            else:
                legend_y = margin * 0.5
            
            self.ax.text(legend_x, legend_y, legend_str, fontsize=9, fontfamily='monospace',
                        verticalalignment='top', horizontalalignment='left',
                        bbox=textbox_props, transform=self.ax.transData)
            
            # Schrittweise Konstruktion
            C = (0, 0)
            
            # X-Achse als Mittellinie bei negativem a
            if quadrant == 2:
                self.ax.axhline(y=0, color='black', linewidth=1, linestyle='-', alpha=0.5)
            
            if progress < 0.25:  # Erste Kathete (b)
                length = sides['b'] * (progress / 0.25)
                A = (length, 0)
                self.ax.plot([C[0], A[0]], [C[1], A[1]], 'b-', linewidth=3)
                self.ax.text(length/2, -0.8, f'b = {length:.1f} cm', ha='center', fontsize=10, color='blue', fontweight='bold')
                
            elif progress < 0.5:  # Zweite Kathete (a)
                A = (sides['b'], 0)
                length = sides['a_abs'] * ((progress - 0.25) / 0.25)
                
                if quadrant == 1:
                    B = (0, length)
                    text_y = length/2
                    text_rotation = 90
                else:  # quadrant == 2
                    B = (0, -length)
                    text_y = -length/2
                    text_rotation = 90
                
                self.ax.plot([C[0], A[0]], [C[1], A[1]], 'b-', linewidth=3)
                self.ax.plot([C[0], B[0]], [C[1], B[1]], 'g-', linewidth=3)
                
                self.ax.text(sides['b']/2, -0.8, f'b = {sides["b"]:.1f} cm', ha='center', fontsize=10, color='blue', fontweight='bold')
                self.ax.text(-1.5, text_y, f'a = {sides["a"]:.1f} cm', ha='center', fontsize=10, rotation=text_rotation, color='green', fontweight='bold')
                
            elif progress < 0.75:  # Hypotenuse
                A = (sides['b'], 0)
                B = (0, sides['a_abs'] if quadrant == 1 else -sides['a_abs'])
                
                self.ax.plot([C[0], A[0]], [C[1], A[1]], 'b-', linewidth=3)
                self.ax.plot([C[0], B[0]], [C[1], B[1]], 'g-', linewidth=3)
                self.ax.plot([A[0], B[0]], [A[1], B[1]], 'r-', linewidth=3)
                
                # Alle Seitenlabels
                self.ax.text(sides['b']/2, -0.8, f'b = {sides["b"]:.1f} cm', ha='center', fontsize=10, color='blue', fontweight='bold')
                
                if quadrant == 1:
                    self.ax.text(-1.5, sides['a_abs']/2, f'a = {sides["a"]:.1f} cm', ha='center', fontsize=10, rotation=90, color='green', fontweight='bold')
                    self.ax.text(sides['b']/2, sides['a_abs']/2 + 0.5, f'c = {sides["c"]:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')
                else:
                    self.ax.text(-1.5, -sides['a_abs']/2, f'a = {sides["a"]:.1f} cm', ha='center', fontsize=10, rotation=90, color='green', fontweight='bold')
                    self.ax.text(sides['b']/2, -sides['a_abs']/2 - 0.5, f'c = {sides["c"]:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')
                
            else:  # Winkel hinzufügen
                A = (sides['b'], 0)
                B = (0, sides['a_abs'] if quadrant == 1 else -sides['a_abs'])
                
                self.ax.plot([C[0], A[0]], [C[1], A[1]], 'b-', linewidth=3)
                self.ax.plot([C[0], B[0]], [C[1], B[1]], 'g-', linewidth=3)
                self.ax.plot([A[0], B[0]], [A[1], B[1]], 'r-', linewidth=3)
                
                # Alle Seitenlabels
                self.ax.text(sides['b']/2, -0.8, f'b = {sides["b"]:.1f} cm', ha='center', fontsize=10, color='blue', fontweight='bold')
                
                if quadrant == 1:
                    self.ax.text(-1.5, sides['a_abs']/2, f'a = {sides["a"]:.1f} cm', ha='center', fontsize=10, rotation=90, color='green', fontweight='bold')
                    self.ax.text(sides['b']/2, sides['a_abs']/2 + 0.5, f'c = {sides["c"]:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')
                else:
                    self.ax.text(-1.5, -sides['a_abs']/2, f'a = {sides["a"]:.1f} cm', ha='center', fontsize=10, rotation=90, color='green', fontweight='bold')
                    self.ax.text(sides['b']/2, -sides['a_abs']/2 - 0.5, f'c = {sides["c"]:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')
                
                # Winkel und Punkte hinzufügen
                arc_radius = min(2, min(sides['a_abs'], sides['b']) * 0.15)
                
                # Rechter Winkel bei C
                square_size = min(1.5, min(sides['a_abs'], sides['b']) * 0.1)
                if quadrant == 1:
                    square = plt.Rectangle((C[0], C[1]), square_size, square_size, 
                                         fill=False, edgecolor='red', linewidth=2)
                    self.ax.text(C[0] + 0.3, C[1] + 0.3, 'γ = 90°', fontsize=10, color='red', fontweight='bold')
                else:
                    square = plt.Rectangle((C[0], C[1]-square_size), square_size, square_size, 
                                         fill=False, edgecolor='red', linewidth=2)
                    self.ax.text(C[0] + 0.3, C[1] - 0.3, 'γ = 90°', fontsize=10, color='red', fontweight='bold')
                self.ax.add_patch(square)
                
                # Winkel Alpha und Beta (quadrant-abhängig)
                if quadrant == 1:
                    alpha_arc = Arc(A, arc_radius*2, arc_radius*2, angle=0, 
                                   theta1=90, theta2=90+angles['alpha'], 
                                   color='orange', linewidth=2)
                    self.ax.text(A[0]-2, A[1]+1, f'α = {angles["alpha"]:.1f}°', fontsize=10, color='orange', fontweight='bold')
                    
                    beta_arc = Arc(B, arc_radius*2, arc_radius*2, angle=0, 
                                  theta1=270, theta2=270+angles['beta'], 
                                  color='purple', linewidth=2)
                    self.ax.text(B[0]+1, B[1]-2, f'β = {angles["beta"]:.1f}°', fontsize=10, color='purple', fontweight='bold')
                else:
                    alpha_arc = Arc(A, arc_radius*2, arc_radius*2, angle=0, 
                                   theta1=180+angles['alpha'], theta2=270, 
                                   color='orange', linewidth=2)
                    self.ax.text(A[0]-2, A[1]-1, f'α = {angles["alpha"]:.1f}°', fontsize=10, color='orange', fontweight='bold')
                    
                    beta_arc = Arc(B, arc_radius*2, arc_radius*2, angle=0, 
                                  theta1=90-angles['beta'], theta2=90, 
                                  color='purple', linewidth=2)
                    self.ax.text(B[0]+1, B[1]+2, f'β = {angles["beta"]:.1f}°', fontsize=10, color='purple', fontweight='bold')
                
                self.ax.add_patch(alpha_arc)
                self.ax.add_patch(beta_arc)
                
                # Punkte markieren
                self.ax.plot(C[0], C[1], 'ko', markersize=8)
                self.ax.plot(A[0], A[1], 'ko', markersize=8)
                self.ax.plot(B[0], B[1], 'ko', markersize=8)
                
                # Punktbeschriftungen
                self.ax.text(C[0]-0.5, C[1] + (0.5 if quadrant == 2 else -0.5), 'C', fontsize=12, fontweight='bold')
                self.ax.text(A[0]+0.3, A[1]-0.5, 'A', fontsize=12, fontweight='bold')
                self.ax.text(B[0]-0.5, B[1] + (0.3 if quadrant == 1 else -0.5), 'B', fontsize=12, fontweight='bold')
            
            # Achsen Setup
            max_side = max(sides['a_abs'], sides['b'])
            margin = max_side * 0.15
            
            self.ax.set_xlim(-margin, sides['b'] + margin * 2.5)
            
            if quadrant == 1:
                self.ax.set_ylim(-margin, sides['a_abs'] + margin)
            else:
                self.ax.set_ylim(-sides['a_abs'] - margin, margin)
            
            self.ax.set_aspect('equal')
            self.ax.grid(True, alpha=0.3)
            
            # Dynamischer Titel
            quadrant_text = f" ({quadrant}. Quadrant)" if quadrant == 2 else ""
            if progress < 0.25:
                title = f'Schritt 1: Kathete b konstruieren{quadrant_text}'
            elif progress < 0.5:
                title = f'Schritt 2: Kathete a konstruieren{quadrant_text}'
            elif progress < 0.75:
                title = f'Schritt 3: Hypotenuse c konstruieren{quadrant_text}'
            else:
                title = f'Schritt 4: Winkel berechnen{quadrant_text}'
            
            self.ax.set_title(title, fontsize=12, fontweight='bold')
        
        # Animation erstellen und zurückgeben
        ani = FuncAnimation(self.fig, animate, frames=frames, 
                          interval=80, repeat=False, blit=False, cache_frame_data=False)
        plt.tight_layout()
        # Speichern der Animation in der Instanz, um sie vor dem Garbage Collector zu schützen
        self.current_animation = ani
        return ani

def main():
    """Hauptfunktion für Benutzerinteraktion."""
    print("RECHTWINKLIGES DREIECK - RECHNER UND VISUALISIERUNG")
    print("="*55)
    print("HINWEIS: Kathete a kann positiv (1. Quadrant) oder negativ (2. Quadrant) sein")
    print("         Kathete b muss immer positiv sein")
    
    calculator = TriangleCalculator()
    
    while True:
        try:
            print(f"\nGeben Sie die Längen der beiden Katheten ein:")
            a = float(input("Kathete a (in cm, kann negativ sein): "))
            b = float(input("Kathete b (in cm, muss positiv sein): "))
            
            if a == 0:
                print("Fehler: Kathete a darf nicht null sein.")
                continue
            if b <= 0:
                print("Fehler: Kathete b muss eine positive Zahl sein.")
                continue
            
            # Berechnungen durchführen
            results = calculator.calculate_triangle_angles(a, b)
            
            # Ergebnisse anzeigen
            calculator.print_results(results)
            
            # Visualisierung wählen
            print(f"\nVisualisierungsoptionen:")
            print("1 - Statische Darstellung")
            print("2 - Animierte Konstruktion")
            print("3 - Keine Visualisierung")
            
            choice = input("Ihre Wahl (1-3): ").strip()
            
            if choice == '1':
                calculator.visualize_static(results, show_construction=True)
            elif choice == '2':
                animation = calculator.create_animated_construction(results)
                # Wichtig: Hier plt.show() aufrufen, um die Animation anzuzeigen
                # Wir verwenden block=True, damit das Programm wartet, bis das Fenster geschlossen wird
                plt.show(block=True)
            elif choice == '3':
                pass
            else:
                print("Ungültige Eingabe, verwende statische Darstellung.")
                calculator.visualize_static(results, show_construction=True)
            
            # Weiter oder beenden
            continue_choice = input(f"\nMöchten Sie ein weiteres Dreieck berechnen? (j/n): ").lower().strip()
            if continue_choice not in ['j', 'ja', 'y', 'yes']:
                break
                
        except ValueError as e:
            if "Kathete b muss positiv sein" in str(e):
                print(f"Fehler: {e}")
            else:
                print("Fehler: Bitte geben Sie gültige Zahlen ein.")
        except KeyboardInterrupt:
            print(f"\nProgramm beendet.")
            break
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    
    print("Vielen Dank für die Nutzung des Dreieck-Rechners!")

if __name__ == "__main__":
    main()
