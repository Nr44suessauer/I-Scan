<img src="https://raw.githubusercontent.com/Nr44suessauer/I-Scan/eac7a51ff977a7fc9e4928790c771728cb8c71d2/docs/diagram/FlowDiagrams_API_Webserver/device%20Config.svg" alt="Device Configuration Flow Diagram" style="width: 90%;">


## Steps in the Diagram

1. **Send JSON (Post/Put command)**
    - Configuration for device connection

    ```json
    {
        "IpPositionUnitTop": "192.168.1.10",
        "IpPositionUnitMid": "192.168.1.11",
        "IpPositionUnitBot": "192.168.1.12",
        "IpLightingUnitA": "192.168.1.20",
        "IpLightingUnitB": "192.168.1.21",
        "ComPortMeasurementUnitTop": "/dev/ttyUSB0",
        "ComPortMeasurementUnitMid": "/dev/ttyUSB1",
        "ComPortMeasurementUnitBot": "/dev/ttyUSB2"
    }
    ```

**Save input data**
- The web server receives the JSON and triggers further actions

**Check IP address of Position Units**
- Establish connection via IP address with Position Unit X

**Check IP address of Lighting Units**
- Establish connection via IP address with Lighting Unit X

**Check COM ports**
- The camera stream is checked, in future versions, this may not necessarily be a camera.

**Results**
- The results of the configuration will be available at /config/status after the routine is completed

```json
{
    "IpPositionUnitTop": "192.168.1.10",
    "IpPositionUnitMid": "192.168.1.11",
    "IpPositionUnitBot": "192.168.1.12",
    "IpLightingUnitA": "192.168.1.20",
    "IpLightingUnitB": "192.168.1.21",
    "ComPortMeasurementUnitTop": "/dev/ttyUSB0",
    "ComPortMeasurementUnitMid": "/dev/ttyUSB1",
    "ComPortMeasurementUnitBot": "/dev/ttyUSB2",

    "IpPositionUnitTopStatus": "connected",
    "IpPositionUnitMidStatus": "connected",
    "IpPositionUnitBotStatus": "connected",
    "IpLightingUnitAStatus": "connected",
    "IpLightingUnitBStatus": "connected",
    "ComPortMeasurementUnitTopStatus": "active",
    "ComPortMeasurementUnitMidStatus": "active",
    "ComPortMeasurementUnitBotStatus": "active",

    "IpPositionUnitTopMapping": "ComPortMeasurementUnitTop",
    "IpPositionUnitMidMapping": "ComPortMeasurementUnitMid",
    "IpPositionUnitBotMapping": "ComPortMeasurementUnitBot"
}
```
