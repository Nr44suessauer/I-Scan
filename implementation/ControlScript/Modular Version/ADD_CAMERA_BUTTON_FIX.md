# "Kamera hinzufügen" Button korrigiert ✅

## Problem vorher:
Der "Kamera hinzufügen" Button im JSON-Editor hatte mehrere Probleme:
- **Fester Index**: Immer "2" statt dynamischer Berechnung
- **Falsche Position**: Regex-Pattern funktionierte nicht korrekt
- **Schlechte Formatierung**: Template wurde als String eingefügt
- **Keine Validierung**: Keine Prüfung der bestehenden JSON-Struktur

## Lösung:
Vollständige Neuentwicklung der `add_camera_template()` Methode:

### ✅ Dynamischer Index:
```python
existing_indices = [cam.get('index', 0) for cam in config_data.get('cameras', [])]
next_index = max(existing_indices) + 1 if existing_indices else 0
```

### ✅ Intelligente Template-Erstellung:
```python
new_camera = {
    "index": next_index,
    "verbindung": f"USB:{next_index}",
    "beschreibung": f"Neue Kamera Beschreibung {next_index}",
    "name": f"Kamera {next_index + 1}",
    "enabled": True,
    "resolution": [640, 480],
    "fps": 30
}
```

### ✅ JSON-basierte Verarbeitung:
- Parst bestehende JSON-Struktur
- Fügt neue Kamera zur Liste hinzu
- Formatiert komplett neu mit korrekter Einrückung
- Validiert JSON-Syntax

### ✅ Benutzerfreundlichkeit:
- Erfolgs-Meldung mit Index-Anzeige
- Automatisches Scrollen zur neuen Kamera
- Fehlerbehandlung für ungültiges JSON

## Ergebnis:
Jetzt funktioniert der "Kamera hinzufügen" Button korrekt:
1. **Berechnet automatisch den nächsten freien Index**
2. **Erstellt korrekte USB-Verbindung** (USB:0, USB:1, USB:2, ...)
3. **Fügt die Kamera an der richtigen Stelle ein**
4. **Formatiert das JSON korrekt**
5. **Zeigt Erfolgs-Bestätigung an**

✅ **Problem behoben - Button funktioniert jetzt perfekt!**
