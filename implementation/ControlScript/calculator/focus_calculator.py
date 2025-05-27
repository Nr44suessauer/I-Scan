import math
import tkinter as tk
from tkinter import ttk, messagebox

def generate_results_table(number_of_measurements, pY, zX, nX, nY, delta_scan, show_plot=True):
    if number_of_measurements <= 0:
        print("number_of_measurements muss > 0 sein.")
        return
    result = delta_scan / number_of_measurements
    print(f"{'Index':>5} | {'Angle (°)':>10} | {'Zmodule (Coordinates)':>22}")
    print("-" * 45)
    angles = []
    y_coords = []
    indices = []
    for i in range(number_of_measurements):
        currentY = pY + result * i
        dx = nX - zX
        dy = nY - currentY
        angle = math.atan2(dy, dx) * 180 / math.pi
        angle = abs(90 - angle)
        print(f"{i:5d} | {angle:10.1f} | ({zX:.1f}, {currentY:.1f})")
        angles.append(angle)
        y_coords.append(currentY)
        indices.append(i)
    if show_plot:
        fig, ax1 = plt.subplots()
        color = 'tab:purple'
        ax1.set_xlabel('Messpunkt Index')
        ax1.set_ylabel('Winkel (°)', color=color)
        ax1.plot(indices, angles, 'o-', color=color, label='Winkel')
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()
        color2 = 'tab:blue'
        ax2.set_ylabel('Zmodule Y-Koordinate', color=color2)
        ax2.plot(indices, y_coords, 's--', color=color2, label='Zmodule Y')
        ax2.tick_params(axis='y', labelcolor=color2)
        fig.suptitle('Scan-Ergebnisse: Winkel und Zmodule-Koordinaten')
        fig.tight_layout()
        plt.show()

class ScanCalculatorUI:
    def __init__(self, root):
        self.root = root
        root.title('Scan Calculator')
        self.create_widgets()

    def create_widgets(self):
        # Eingabefelder
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.entries = {}
        # Neue, sprechende Namen für die Felder
        fields = [
            ('Startpunkt X (pX)', 'pX', 0),
            ('Startpunkt Y (pY)', 'pY', 0),
            ('Z max X (mX)', 'mX', 0),
            ('Z max Y (mY)', 'mY', 150),
            ('Center X (nX)', 'nX', 150),
            ('Center Y (nY)', 'nY', 75),
            ('Altes Center X (oX)', 'oX', 150),
            ('Altes Center Y (oY)', 'oY', 0),
            ('ZModule X (zX)', 'zX', 0),
            ('ZModule Y (zY)', 'zY', 0),
            ('DeltaScan', 'deltaScan', 0),
            ('Anzahl Messungen', 'numberOfMeasurements', 0)
        ]
        row = 0
        for label, key, default in fields:
            ttk.Label(frm, text=label+':').grid(row=row, column=0, sticky='e')
            entry = ttk.Entry(frm, width=12)
            entry.insert(0, str(default))
            entry.grid(row=row, column=1, sticky='w')
            self.entries[key] = entry
            row += 1
        # Button
        ttk.Button(frm, text='Berechnen & Plotten', command=self.calculate).grid(row=row, column=0, columnspan=2, pady=10)
        # Ergebnis-Tabelle
        self.result_text = tk.Text(self.root, height=15, width=45, font=('Consolas', 10))
        self.result_text.grid(row=0, column=1, padx=10, pady=10)

    def calculate(self):
        try:
            vals = {k: float(self.entries[k].get()) for k in self.entries}
            vals['numberOfMeasurements'] = int(vals['numberOfMeasurements'])
        except Exception as e:
            messagebox.showerror('Fehler', f'Ungültige Eingabe: {e}')
            return
        # Tabelle berechnen (neue Logik analog Visualisierung)
        result = vals['deltaScan'] / vals['numberOfMeasurements'] if vals['numberOfMeasurements'] > 0 else 0
        lines = [f"{'Idx':>3} | {'Angle (°)':>10} | {'Zmodule (X,Y)':>18}", '-'*38]
        angles, y_coords, indices = [], [], []
        for i in range(vals['numberOfMeasurements']):
            y_pos = vals['pY'] + result * i
            # Geometrie wie im Visualisierungsbeispiel:
            ray_to_C_rad = math.atan2(0 - y_pos, vals['nX'])
            ray_to_C_deg = math.degrees(ray_to_C_rad)
            internal_angle = ray_to_C_deg - (-90)
            lines.append(f"{i:3d} | {internal_angle:10.1f} | ({vals['zX']:.1f}, {y_pos:.1f})")
            angles.append(internal_angle)
            y_coords.append(y_pos)
            indices.append(i)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, '\n'.join(lines))
        # Plot
        try:
            import matplotlib.pyplot as plt
            fig, ax1 = plt.subplots()
            color = 'tab:purple'
            ax1.set_xlabel('Messpunkt Index')
            ax1.set_ylabel('Winkel (°)', color=color)
            ax1.plot(indices, angles, 'o-', color=color, label='Winkel')
            ax1.tick_params(axis='y', labelcolor=color)
            ax2 = ax1.twinx()
            color2 = 'tab:blue'
            ax2.set_ylabel('Zmodule Y-Koordinate', color=color2)
            ax2.plot(indices, y_coords, 's--', color=color2, label='Zmodule Y')
            ax2.tick_params(axis='y', labelcolor=color2)
            fig.suptitle('Scan-Ergebnisse: Winkel und Zmodule-Koordinaten')
            fig.tight_layout()
            plt.show()
        except ImportError:
            messagebox.showwarning('Warnung', 'matplotlib nicht installiert, kein Plot möglich.')

if __name__ == '__main__':
    root = tk.Tk()
    app = ScanCalculatorUI(root)
    root.mainloop()