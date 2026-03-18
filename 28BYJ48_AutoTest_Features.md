# 28BYJ-48 Auto-Test mit Permutations-Tabelle

## Neue Features

### 1. Permanente Permutations-Tabelle
- **Alle Kombinationen sichtbar**: Vor dem Test werden alle möglichen Pin-Permutationen in einer Tabelle angezeigt
- **24 Kombinationen** bei 4 eindeutigen Pins (z.B. 4,5,6,7)
- Zeigt alle Spalten: #, IN1, IN2, IN3, IN4, Status, ✓

### 2. Interaktive Test-Durchführung
- **Generieren**: Button "🔍 Permutationen generieren" erstellt die komplette Liste
- **Starten**: Button "▶️ Auto-Test starten" wird nach Generierung aktiv
- **Live-Status**: Aktuelle Kombination wird gelb hervorgehoben während des Tests
- **Ergebnis-Markierung**: 
  - ✓ Grün bei erfolgreicher Kombination
  - ✗ Rot bei fehlgeschlagener Kombination
  - Automatische Checkbox-Aktivierung bei Erfolg

### 3. Tastatur-Shortcuts
- **Y** oder **J**: Kombination bestätigen (funktioniert)
- **N**: Kombination ablehnen (funktioniert nicht)
- Schnelle Eingabe während des Tests ohne Maus

### 4. Intelligente Auswahl-Funktionen

#### ✅ Beste Kombination übernehmen
- Analysiert alle markierten Kombinationen
- Berechnet häufigste Pin-Belegung pro Position
- Übernimmt automatisch die beste ermittelte Kombination

#### 🔄 Invertierte auswählen
- Findet automatisch invertierte Pin-Reihenfolgen
- Beispiel: Wenn `4,5,6,7` funktioniert, wird auch `7,6,5,4` markiert
- Berücksichtigt HIGH/LOW Inversionen

#### ✖ Auswahl löschen
- Löscht alle Checkboxen und Status-Markierungen
- Setzt Tabelle zurück für neuen Test

### 5. Konfigurierbare Test-Parameter
- **Test Steps**: 20-200 Schritte pro Test (Standard: 50)
- **Delay**: 1-20ms zwischen Schritten (Standard: 5ms)
- **Timeout**: 3-30 Sekunden Wartezeit (Standard: 10s)
- **Zwischen-Delay**: 500-5000ms zwischen Tests (Standard: 1000ms)

### 6. Multi-Selection Support
- Mehrere Kombinationen können als funktionierend markiert werden
- Wichtig bei unterschiedlichen Motor-Verkabelungen
- Frequenz-Analyse ermittelt beste Pin-Zuordnung

## Workflow

1. **Pin-Liste eingeben**: z.B. `4,5,6,7` oder `4,5,6,7,12,13`
2. **Permutationen generieren**: Klick auf "🔍 Permutationen generieren"
3. **Tabelle prüfen**: Alle 24 Kombinationen werden angezeigt
4. **Test starten**: Klick auf "▶️ Auto-Test starten"
5. **Bewerten**: Mit Y/J/N Tasten oder Buttons jede Kombination bewerten
6. **Ergebnis anwenden**: 
   - Einzelne Kombination: Direkt aus Tabelle übernehmen
   - Mehrere Kombinationen: "✅ Beste Kombination übernehmen" klicken
   - Invertierte finden: "🔄 Invertierte auswählen" klicken

## Technische Details

### Permutations-Algorithmus
```javascript
function generatePermutationsRecursive(pins, current, needed) {
  if (current.length === needed) {
    allPermutations.push([...current]);
    return;
  }
  
  for (let i = 0; i < pins.length; i++) {
    if (!current.includes(pins[i])) {
      current.push(pins[i]);
      generatePermutationsRecursive(pins, current, needed);
      current.pop();
    }
  }
}
```

### Häufigkeits-Analyse (Beste Kombination)
```javascript
// Zählt für jede Pin-Position die häufigste Verwendung
const pinFreq = [{}, {}, {}, {}];
checkedPerms.forEach(perm => {
  for (let i = 0; i < 4; i++) {
    pinFreq[i][perm[i]] = (pinFreq[i][perm[i]] || 0) + 1;
  }
});
```

### Inversions-Erkennung
```javascript
const inverted = [perm[3], perm[2], perm[1], perm[0]];
// Sucht umgekehrte Reihenfolge in allen Permutationen
```

## Vorteile

✅ **Transparenz**: Alle Möglichkeiten sind sichtbar vor dem Test
✅ **Kontrolle**: Manuelle Auswahl welche Kombinationen getestet werden
✅ **Effizienz**: Tastatur-Shortcuts für schnelle Bewertung
✅ **Intelligenz**: Automatische Analyse findet beste Pin-Zuordnung
✅ **Flexibilität**: Mehrere funktionierende Kombinationen möglich
✅ **Visuell**: Farbcodierung zeigt Status auf einen Blick

## Beispiel-Szenario

**Situation**: 28BYJ-48 Motor mit unbekannter Verkabelung

1. Pins `4,5,6,7` eingeben
2. "Generieren" → 24 Permutationen werden angezeigt
3. "Test starten"
4. Bei Kombination #5 (`4,6,5,7`): Motor dreht → **Y** drücken → ✓ Grün
5. Bei Kombination #12 (`7,6,5,4`): Motor dreht rückwärts → **Y** drücken → ✓ Grün
6. Bei Kombination #18 (`6,4,7,5`): Motor dreht → **Y** drücken → ✓ Grün
7. Test durchläuft alle 24 Kombinationen
8. "Beste Kombination übernehmen" analysiert die 3 erfolgreichen und wählt häufigste Pin-Positionen
9. Resultat: `4,6,5,7` wird als beste Kombination erkannt und übernommen

## Zugriff

Web-Interface: `http://192.168.178.86`
Tab: **⚙️ 28BYJ-48 Motor**
Bereich: **📋 Erweiterte Auto-Test Funktionen**
