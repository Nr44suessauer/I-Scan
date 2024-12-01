1. [Einführung](#Einführung)
    ### Zielsetzung

    Das Ziel dieser wissenschaftlichen Arbeit ist die Entwicklung eines kostengünstigen und wartungsfreundlichen 3D-Scanners, der unabhängig von der verwendeten Hardware funktioniert und für verschiedene Anwendungsfälle geeignet ist. Dabei sollen verschiedene Verfahren unterstützt werden, darunter:

    - **Stereo Vision**: Nutzung von zwei Kameras zur Berechnung von Tiefeninformationen.
    - **Structured Light Scanning**: Projektion von Mustern auf das Objekt zur Erfassung der Geometrie.
    - **Photogrammetrie**: Erstellung von 3D-Modellen aus 2D-Bildern.
    - **Triangulation**: Bestimmung von Punktpositionen durch Messung von Winkeln und Entfernungen.
    - **Spektralanalyse**: Verwendung von spektralanalytischen Techniken zur Erfassung und Analyse von Lichtwellenlängen, um detaillierte Materialinformationen und präzise Oberflächenstrukturen des Objekts zu bestimmen.

    Ein Schwerpunkt ist die Replizierbarkeit mit gängigen, leicht verfügbaren Komponenten. Zudem wird eine flexible und modulare Softwarearchitektur entwickelt, die nicht nur die Integration verschiedener Kameras und Sensoren ermöglicht, sondern auch eine einfache Wartung und Erweiterbarkeit des Systems sicherstellt.

    ### Struktur
    Die Arbeit ist in sieben Hauptkapitel unterteilt, die systematisch die Entwicklung des I_Scan Projekts darstellen. Nach der **Einführung** werden im **State of the Art** bestehende 3D-Scanner und relevante Konzepte analysiert. Das Kapitel **Konzept & Planung** beschreibt die System- und Softwarearchitektur sowie die Hardwarewahl. In der **Implementierung** werden der Hardwareaufbau und die Softwareentwicklung detailliert erläutert. Anschließend behandelt die **Benutzerfreundlichkeit** die Interaktion über die REST API und die Nutzung des Scanners. Abschließend fasst die **Zusammenfassung** die Ergebnisse zusammen und gibt einen Ausblick auf zukünftige Entwicklungen. Das **Quellenverzeichnis** rundet die Arbeit ab.