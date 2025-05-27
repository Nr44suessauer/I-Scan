import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Mathematische Hilfsfunktionen für Dreiecksberechnung ---
def berechne_dreieck(a=None, b=None, c=None, alpha=None, beta=None, gamma=None):
    '''
    Berechnet alle Seiten und Winkel eines allgemeinen Dreiecks.
    Mindestens 3 Werte, davon mindestens eine Seite, müssen gegeben sein.
    Winkel in Grad, Seiten in beliebiger Längeneinheit.
    Gibt ein dict mit a, b, c, alpha, beta, gamma zurück (Winkel in Grad).
    '''
    # Umwandlung aller Winkel in Radiant für Berechnung
    def d2r(x): return math.radians(x) if x is not None else None
    def r2d(x): return math.degrees(x) if x is not None else None
    # Zuweisung
    sides = {'a': a, 'b': b, 'c': c}
    angles = {'alpha': alpha, 'beta': beta, 'gamma': gamma}
    # Zähle gegebene Werte
    n_sides = sum(1 for v in sides.values() if v is not None)
    n_angles = sum(1 for v in angles.values() if v is not None)
    if n_sides + n_angles < 3 or n_sides < 1:
        raise ValueError('Mindestens 3 Werte, davon mindestens eine Seite, müssen gegeben sein.')
    # SSS: 3 Seiten gegeben
    if n_sides == 3:
        a, b, c = sides['a'], sides['b'], sides['c']
        # Kosinussatz für alle Winkel
        alpha = r2d(math.acos((b**2 + c**2 - a**2) / (2*b*c)))
        beta  = r2d(math.acos((a**2 + c**2 - b**2) / (2*a*c)))
        gamma = 180 - alpha - beta
        return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    # SWS: 2 Seiten + eingeschlossener Winkel
    if n_sides == 2 and n_angles == 1:
        # Finde die Konstellation
        if a is not None and b is not None and gamma is not None:
            # a, b, gamma gegeben
            c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(d2r(gamma)))
            alpha = r2d(math.asin(a * math.sin(d2r(gamma)) / c))
            beta = 180 - alpha - gamma
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if a is not None and c is not None and beta is not None:
            b = math.sqrt(a**2 + c**2 - 2*a*c*math.cos(d2r(beta)))
            alpha = r2d(math.asin(a * math.sin(d2r(beta)) / b))
            gamma = 180 - alpha - beta
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if b is not None and c is not None and alpha is not None:
            a = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(d2r(alpha)))
            beta = r2d(math.asin(b * math.sin(d2r(alpha)) / a))
            gamma = 180 - alpha - beta
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    # SSW: 2 Seiten + nicht eingeschlossener Winkel (Sinussatz)
    if n_sides == 2 and n_angles == 1:
        # z.B. a, b, alpha gegeben
        if a is not None and b is not None and alpha is not None:
            beta = r2d(math.asin(b * math.sin(d2r(alpha)) / a))
            gamma = 180 - alpha - beta
            c = a * math.sin(d2r(gamma)) / math.sin(d2r(alpha))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if a is not None and c is not None and alpha is not None:
            gamma = r2d(math.asin(c * math.sin(d2r(alpha)) / a))
            beta = 180 - alpha - gamma
            b = a * math.sin(d2r(beta)) / math.sin(d2r(alpha))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if b is not None and c is not None and beta is not None:
            gamma = r2d(math.asin(c * math.sin(d2r(beta)) / b))
            alpha = 180 - beta - gamma
            a = b * math.sin(d2r(alpha)) / math.sin(d2r(beta))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    # WSW: 1 Seite, 2 Winkel
    if n_sides == 1 and n_angles == 2:
        # z.B. a, beta, gamma gegeben
        if a is not None and beta is not None and gamma is not None:
            alpha = 180 - beta - gamma
            b = a * math.sin(d2r(beta)) / math.sin(d2r(alpha))
            c = a * math.sin(d2r(gamma)) / math.sin(d2r(alpha))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if b is not None and alpha is not None and gamma is not None:
            beta = 180 - alpha - gamma
            a = b * math.sin(d2r(alpha)) / math.sin(d2r(beta))
            c = b * math.sin(d2r(gamma)) / math.sin(d2r(beta))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
        if c is not None and alpha is not None and beta is not None:
            gamma = 180 - alpha - beta
            a = c * math.sin(d2r(alpha)) / math.sin(d2r(gamma))
            b = c * math.sin(d2r(beta)) / math.sin(d2r(gamma))
            return {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    raise ValueError('Ungültige oder nicht unterstützte Dreieckskonstellation.')

# --- UI ---
class MainApp:
    def __init__(self, root):
        self.root = root
        root.title('Scan- & Dreiecksrechner')
        self.canvas = None  # Canvas für Matplotlib
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.entries = {}
        # Felder für beide Rechnungen (a, b für Dreieck, weitere für Scan falls gewünscht)
        fields = [
            ('Höhe Z-Modul (a)', 'a'),
            ('Abstand zum Zentrum (b)', 'b'),
        ]
        row = 0
        for label, key in fields:
            ttk.Label(frm, text=label+':').grid(row=row, column=0, sticky='e')
            entry = ttk.Entry(frm, width=12)
            entry.grid(row=row, column=1, sticky='w')
            self.entries[key] = entry
            row += 1
        ttk.Button(frm, text='Berechnen & Anzeigen', command=self.berechnen).grid(row=row, column=0, columnspan=2, pady=10)
        self.result_text = tk.Text(self.root, height=10, width=50, font=('Consolas', 10))
        self.result_text.grid(row=0, column=2, padx=10, pady=10)
        # Platz für die Grafik rechts neben den Eingabefeldern
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.grid(row=0, column=3, padx=10, pady=10)

    def berechnen(self):
        # Eingaben sammeln
        kwargs = {}
        for key in self.entries:
            val = self.entries[key].get().strip()
            if val:
                try:
                    kwargs[key] = float(val.replace(',', '.'))
                except Exception:
                    messagebox.showerror('Fehler', f'Ungültige Eingabe für {key}')
                    return
        # Gamma immer 90°, c und Winkel werden nicht eingegeben
        kwargs['gamma'] = 90.0
        try:
            res = berechne_dreieck(**kwargs)
        except Exception as e:
            messagebox.showerror('Fehler', str(e))
            return
        # Werte in cm und Grad ausgeben, Punkte als Koordinaten
        a, b, c = res['a'], res['b'], res['c']
        alpha, beta, gamma = res['alpha'], res['beta'], res['gamma']
        A = (0, 0)
        B = (0, a)
        C = (b, 0)
        lines = [
            f"a = {a:.2f} cm", f"b = {b:.2f} cm", f"c = {c:.2f} cm",
            f"α = {alpha:.2f}°", f"β = {beta:.2f}°", f"γ = {gamma:.2f}°",
            f"A (0.00|0.00)",
            f"B (0.00|{a:.2f})",
            f"C ({b:.2f}|0.00)"
        ]
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, '\n'.join(lines))
        self.plot_triangle(res)

    def plot_triangle(self, res):
        a, b, c = res['a'], res['b'], res['c']
        alpha, beta, gamma = res['alpha'], res['beta'], res['gamma']
        A = (0, 0)
        B = (0, a)
        C = (b, 0)
        fig, ax = plt.subplots(figsize=(6,6))  # Größeres Koordinatensystem
        ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'o-', color='blue')
        ax.annotate('A', A, textcoords='offset points', xytext=(-10,-10), fontsize=12)
        ax.annotate('B', B, textcoords='offset points', xytext=(-10,10), fontsize=12)
        ax.annotate('C', C, textcoords='offset points', xytext=(10,-10), fontsize=12)
        # Seitenbeschriftung direkt an den Geraden (nur Buchstaben)
        ax.text((A[0]+B[0])/2 - 0.1*a, (A[1]+B[1])/2, 'a', color='red', fontsize=14, ha='right', va='center', fontweight='bold')
        ax.text((A[0]+C[0])/2, (A[1]+C[1])/2 - 0.1*a, 'b', color='green', fontsize=14, ha='center', va='top', fontweight='bold')
        ax.text((B[0]+C[0])/2 + 0.1*b, (B[1]+C[1])/2, 'c', color='orange', fontsize=14, ha='left', va='center', fontweight='bold')
        # Winkelbeschriftung direkt an die Ecken (alpha/gamma getauscht)
        ax.text(A[0]+0.2, A[1]+0.2, "γ", color='purple', fontsize=13, ha='left', va='bottom')
        ax.text(B[0]+0.2, B[1]-0.2, "β", color='purple', fontsize=13, ha='left', va='top')
        ax.text(C[0]-0.2, C[1]+0.2, "α", color='purple', fontsize=13, ha='right', va='bottom')
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.6)
        # Legende entfernt, stattdessen Achsenbereich großzügig setzen
        # Achsenbereich so setzen, dass y auch ins Minus gehen kann (2 Quadranten)
        margin = max(a, b, c) * 0.3
        ax.set_xlim(min(0, b) - margin, max(b, 0) + margin)
        ax.set_ylim(-max(a, b, c) - margin, max(a, b, c) + margin)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_title('Dreieck (a parallel Y, γ=90°)')
        # --- Matplotlib-Canvas in Tkinter einbetten ---
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        plt.close(fig)

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
