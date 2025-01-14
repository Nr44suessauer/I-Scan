
## Konzept eines beweglichen Kamera-Setups in der Z-Achse


Dieses Konzept beschreibt ein bewegliches Kamera-Setup in der Z-Achse, bestehend aus drei beweglichen Modulen, die jeweils mit einer Kamera ausgestattet sind. Der Winkel jeder Kamera ist individuell einstellbar, um eine flexible und präzise Aufnahme zu ermöglichen.

### Komponenten
1. **Bewegliche Module**: Drei Module, die entlang der Z-Achse bewegt werden können.
2. **Kameras**: Jede Einheit ist mit einer beliebigen Kamera ausgestattet.
3. **Winkelverstellung**: Mechanismus zur Änderung des Kamerawinkels.

### Funktionsweise
- **Bewegung entlang der Z-Achse**: Die Module können unabhängig voneinander entlang der Z-Achse bewegt werden, um verschiedene Höhen und Positionen abzudecken.
- **Einstellbarer Kamerawinkel**: Der Winkel jeder Kamera kann manuell oder automatisch angepasst werden, um den optimalen Blickwinkel für die Aufnahme zu gewährleisten.

### Vorteile
- **Flexibilität**: Durch die beweglichen Module und einstellbaren Kamerawinkel kann das Setup an verschiedene Szenarien und Anforderungen angepasst werden.

### Ziele
- **3D-Aufnahmen von größeren Objekten**: Das Setup soll präzise 3D-Aufnahmen von großen Objekten ermöglichten und soll kompatibel mit verschiedenen Szenarien, unabhängig von Größe oder Messkonzept sein.
- **Erweiterbarkeit**: Es können entweder vier dieser Aufbauten genutzt werden  oder ein der Größe des Usecases angepasster **"Drehteller"**.

<div style="display: flex; align-items: center; margin-top: 20px;">
    <p></p>
</div>

### Orientierung der Module

Diese Module werden ihre "Tasks" wireless erhalten. Die Erstellung dieser Tasks und das senden zum relevantem modul, wird ein externes System übernehmen.

<div style="display: flex; align-items: center; margin-top: 20px;">
    <p></p>
</div>

<div style="display: flex;">
    <div style="flex: 1; padding-left: 10px;">
        <img src="https://github.com/Nr44suessauer/nr44suessauer.github.io/blob/main/assets/img/I-Scan/AufbauUndTeile.jpg?raw=true" alt="Aufbau und Teile" style="width: 250px;">
    </div>
    <div style="flex: 1; padding-left: 10px;">
        Zum Ausrichten der Module werden 3 Größen benötigt: 
        <div style="display: flex; align-items: center; margin-top: 0px;">
    <p></p>
</div>
        <ul>
            <li>Die Absolute Höhe eines Moduls</li>
            <li>Die Relative Höhe der Module zueinander (Fehlervermeidung)</li>
            <li>Winkel der Kamera</li>
        </ul>
        Diese Größen erhalten wir durch:
        <div style="display: flex; align-items: center; margin-top: 0px;">
    <p></p>
</div>
        <ul>
            <li>Lidarsensoren montiert jedem Modul oder am mittlerem allein.</li>
            <li>Endstop Schalter an der Unterseite jedes Moduls, in kombination mit Steppermotoren.</li>
        </ul>
        <div style="display: flex; align-items: center; margin-top: 0px;">
    <p></p>
</div>
        Dies setzt eine Initialisierung vorraus, in der alle Module auf 0 (Endstop = true) fahren.  
    </div>
</div>


### Verbindung und Steuerung

Die Kameras werden über USB-Verbindungen am Hauptsystem angebracht, welches die zentrale Steuerungseinheit darstellt. Von diesem Hauptsystem aus erfolgt auch die Steuerung der Module. Dies ermöglicht eine koordinierte und effiziente Verwaltung des gesamten Kamera-Setups.

