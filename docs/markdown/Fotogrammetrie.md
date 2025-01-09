# Ein Leitfaden zur Photogrammetrie: Technik, Software und Anwendungsfälle

Photogrammetrie ist eine innovative Technik, mit der aus zweidimensionalen Fotografien präzise dreidimensionale Modelle erstellt werden. Dieser Beitrag erklärt, wie die Photogrammetrie funktioniert, welche Schritte nötig sind und welche Software sich am besten eignet.

## Was ist Photogrammetrie?

Photogrammetrie ist ein Verfahren, das mithilfe von Fotos räumliche Daten eines Objekts oder einer Szene erfasst. Die Methode findet Anwendung in Bereichen wie:

- Architektur
- Archäologie
- Gamedesign
- Qualitätskontrolle
- Medizin
- Forensik
- Kartografie

Die Technik bietet eine flexible Möglichkeit, Objekte und Umgebungen zu digitalisieren, unabhängig von ihrer Größe oder Zugänglichkeit.

---

## Die technischen Grundlagen der Photogrammetrie

Photogrammetrie basiert auf der Analyse von überlappenden Fotos, um räumliche Informationen zu extrahieren. Dabei kommen folgende Schritte zum Einsatz:

### 1. Bildaufnahme
Eine Serie von überlappenden Bildern wird erstellt. Diese Bilder müssen das Zielobjekt oder die Szene aus unterschiedlichen Perspektiven erfassen. Für beste Ergebnisse eignen sich Kameras mit hoher Auflösung und genaue die Positions dieser.

![Beispiel für die Bildaufnahme](https://formlabs.com/_next/image/?url=https%3A%2F%2Fformlabs-media.formlabs.com%2Ffiler_public_thumbnails%2Ffiler_public%2F6d%2F43%2F6d430a93-30a4-4091-bb20-a24a09e07954%2Fphotogrammetry.jpg__1354x0_q85_subsampling-2.jpg&w=3840&q=75)

### 2. Bildabgleich & Triangulation
Bilder werden anhand ihrer räumlichen Position und übereinstimmender Merkmale in den einzelnen Aufnahmen identifiziert und verknüpft. Mit Tools wie Unity lassen sich aus diesen Daten präzise 3D-Modelle erstellen oder Modelle generiert werden können, die sich nahtlos in interaktive Anwendungen oder Spielszenen integrieren lassen.
Um mehr über den Photogrammetrie-Workflow in Unity zu erfahren, importiere diese PDF in einer Mini-Ansicht:

<iframe src="I-Scan\docs\datasheet\Unity-Photogrammetry-Workflow_2017-07_v2.pdf" width="300" height="400"></iframe>

![Bildabgleich mit Software](./images/image-matching.png)

### 3. Merkmalsextraktion
In jedem Bild werden eindeutige Merkmale identifiziert, die über mehrere Fotos hinweg verfolgt werden können. Dies bildet die Grundlage für die räumliche Rekonstruktion.

![Merkmalsextraktion erklärt](./images/feature-extraction.png)

### 4. Triangulation
Die 3D-Koordinaten der erkannten Merkmale werden mithilfe der Geometrie berechnet. Hierbei spielt die Triangulation eine zentrale Rolle.

![Triangulationsprozess visualisiert](./images/triangulation.png)

### 5. Erstellung der Punktwolke
Die erfassten Daten werden in eine dichte Punktwolke umgewandelt, die die 3D-Struktur des Objekts repräsentiert.

![Dichte Punktwolke](./images/point-cloud.png)

### 6. Mesh-Generierung
Aus der Punktwolke wird ein durchgehendes 3D-Oberflächennetz (Mesh) erstellt, das die Geometrie des Objekts beschreibt.

![Mesh-Generierung aus der Punktwolke](./images/mesh-generation.png)

### 7. Texturierung
Zum Abschluss wird eine Textur auf das Mesh angewendet, um ein realitätsnahes Aussehen zu erzeugen.

![Texturiertes 3D-Modell](./images/textured-model.png)

---

## Vorteile der Photogrammetrie

- **Flexibilität:** Sowohl kleine als auch große Objekte und sogar schwer zugängliche Bereiche können dokumentiert werden.
- **Kosten:** Oft günstiger als alternative Verfahren wie Laserscanning.
- **Genauigkeit:** Moderne Software ermöglicht hochpräzise Ergebnisse.

---

## Auswahl der richtigen Software

Für die Photogrammetrie gibt es eine Vielzahl von Softwarelösungen. Die Wahl hängt von den spezifischen Anforderungen und dem Budget ab. Hier einige beliebte Programme:

- **Agisoft Metashape:** Ideal für fortgeschrittene Nutzer, bietet umfassende Funktionen.
- **RealityCapture:** Sehr schnelle Verarbeitung, jedoch mit einem Fokus auf leistungsstarke Hardware.
- **Meshroom:** Open-Source-Software für Einsteiger.
- **Pix4D:** Speziell für Drohnenaufnahmen optimiert.

---

## Fazit

Die Photogrammetrie ist ein leistungsfähiges Werkzeug zur Erstellung von 3D-Modellen und wird in vielen technischen und wissenschaftlichen Bereichen eingesetzt. Mit der richtigen Ausrüstung und Software können beeindruckende Ergebnisse erzielt werden.

Weitere Details und einen ausführlichen Softwarevergleich findest du hier: [Formlabs Blog](https://formlabs.com/de/blog/photogrammetrie-leitfaden-und-software-vergleich/).

---

## Weiterführende Links

- [Wikipedia: Photogrammetrie](https://de.wikipedia.org/wiki/Photogrammetrie)
- [Pix4D Offizielle Website](https://www.pix4d.com)
- [Meshroom GitHub](https://github.com/alicevision/meshroom)

**Hinweis:** Dieser Beitrag basiert auf dem Leitfaden von Formlabs und dient als Einstieg in die Welt der Photogrammetrie.
