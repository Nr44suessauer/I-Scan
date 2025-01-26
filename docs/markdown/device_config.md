<img src="https://raw.githubusercontent.com/Nr44suessauer/I-Scan/eac7a51ff977a7fc9e4928790c771728cb8c71d2/docs/diagram/FlowDiagrams_API_Webserver/device%20Config.svg" alt="Device Configuration Flow Diagram" style="width: 90%;">


## Schritte im Diagramm


1. **Send Json (Post/Put command)**
    - Das Gerät wird eingeschaltet und führt einen Selbsttest durch.

2. **Save input data**
    - Das Gerät verbindet sich mit dem lokalen Netzwerk.

3. **Check Ip-adress PositionUnits**
    - Das Gerät erhält eine IP-Adresse vom DHCP-Server.

4. **Check Ip-adress LightingUnits**
    - Das Gerät stellt eine Verbindung zum konfigurierten Webserver her.

5. **Authentifizierung**
    - Das Gerät authentifiziert sich beim Webserver mit den gespeicherten Zugangsdaten.

6. **Konfigurationsdaten abrufen**
    - Das Gerät lädt die aktuellen Konfigurationsdaten vom Webserver herunter.

7. **Konfiguration anwenden**
    - Die heruntergeladenen Konfigurationsdaten werden auf das Gerät angewendet.

8. **Statusmeldung senden**
    - Das Gerät sendet eine Statusmeldung an den Webserver, dass die Konfiguration erfolgreich angewendet wurde.
