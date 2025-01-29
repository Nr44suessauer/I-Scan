## Scan config

![Scan Config Diagramm](https://raw.githubusercontent.com/Nr44suessauer/I-Scan/e3244204858e6e4e7f5cfc8a78d4bcee4665ab8d/docs/diagram/FlowDiagrams_API_Webserver/Scan%20config.svg){ width=70% }

In this configuration step, parameters required for aligning the machine are processed. This assumes that **all devices being used are also configured**. Currently, both configuration processes (device config & scan config) are not dependent on each other.

### Scan Configuration

The parameters for configuring the scan are defined, explained, and put into context here:

1. [Send JSON (Post/Put command)](#send-json-postput-command)
2. [Maximum Delta Z](#maximum-delta-z)
   - [Integral Representation and Height Calculation](#integral-representation)
   - [Upper Max / Lower Max Table](#upper-max-lower-max)
3. [Resolution Calculation](#resolution-calculation)

---

### Send JSON (Post/Put command)

- Configuration of the "next" scan

```json
{
   "MeasurementUnitInUse": ["Top", "Mid", "Bot"],
   "MeasurementUnitSize" : ["15","15","15"],
   "ModuleHeadOffsets": ["5cm", "7.5cm", "5cm", "7.5cm", "5cm", "7.5cm", "5cm", "7.5cm"],
   "NumberOfPictures": "30",
   "MaxDistanceZmove": "150cm",
   "DistanceToObject": "100cm",
   "HeightOfObject": "50cm"
}
```

### Maximum Delta Z

If the endstop Z is at 0 cm and the maximum height of the device is 210 cm, the maximum Delta Z can be calculated.

To calculate the maximum height, we need to know the size of each unit. In our example, these are standardized to 15 cm.

The units are labeled (Bot = 0, Mid = 1, Top = 2) and is the variable Z Endstop Unit.

Substituting the values:

\[ \Delta Z_{\text{max}} = (\text{Z}_{\text{Endstop Unit}} \times \text{Unit Height} + \text{Maximum Height I-Scan}) - (\text{Z}_{\text{Endstop Mid}} \times \text{Unit Height} + \text{Z}_{\text{Endstop Top}} \times \text{Unit Height}) \]

So the maximum Delta Z for Unit Bot is 165 cm.
>note: This formula is only for three same size units.

---

### Integral Representation and Height Calculation

#### 1. **Discrete vs. Continuous Representation**

The discrete representation is based on fixed unit sizes (e.g., 15 cm per unit), while the continuous representation uses integrals to model units of varying sizes.

#### 2. **Integral Representation**

The heights of the units are represented using continuous functions:

1. **Definition of Continuous Functions:**
   - \( f_{\text{bot}}(z) \): Height contribution of the bottom unit.
   - \( f_{\text{mid}}(z) \): Height contribution of the middle unit.
   - \( f_{\text{top}}(z) \): Height contribution of the top unit.

2. **Integration Over the Range:**
   - \(\int_{a}^{b} f_{\text{bot}}(z) \, dz\)
   - \(\int_{a}^{b} f_{\text{mid}}(z) \, dz\)
   - \(\int_{a}^{b} f_{\text{top}}(z) \, dz\)

3. **Calculation of Maximum Height Difference:**
   \[ \Delta Z_{\text{max}} = \left( \text{Maximum Height I-Scan} \right) - \left( \int_{a}^{b} f_{\text{bot}}(z) \, dz + \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right) \]

This approach provides a continuous representation of the height changes of each unit.

---

### Upper Max / Lower Max Table

The table below shows the dependency of the maximum and minimum heights of each unit based on the positions of the other units. The reference is taken from the bottom of the unit.

| Unit | Upper Border (Maximum)                                                                 | Lower Border (Initial Position)                                                   | Condition Upper Border       | Condition Lower Border       |
|------|----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|------------------------------|------------------------------|
| **Bot** | \( \text{Max } Z_{\text{bot}} = \text{Maximum Height I-Scan} - \left( \int_{a}^{b} f_{\text{bot}}(z) \, dz + \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right) \) | \( \text{Min } Z_{\text{bot}} = \text{Initial Height I-Scan} \)                     | mid & top = max              | -                            |
| **Mid** | \( \text{Max } Z_{\text{mid}} = \text{Maximum Height I-Scan} - \left( \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right) \) | \( \text{Min } Z_{\text{mid}} = \text{Initial Height I-Scan} + \int_{a}^{b} f_{\text{bot}}(z) \, dz \) | top = max                    | bot = min                    |
| **Top** | \( \text{Max } Z_{\text{top}} = \text{Maximum Height I-Scan} - \int_{a}^{b} f_{\text{top}}(z) \, dz \) | \( \text{Min } Z_{\text{top}} = \text{Initial Height I-Scan} + \left( \int_{a}^{b} f_{\text{bot}}(z) \, dz + \int_{a}^{b} f_{\text{mid}}(z) \, dz \right) \) | -                            | mid & bot = min              |

### **Table Description:**

- **Upper Border (Maximum):**  
  The maximum height of each unit is calculated by subtracting the heights of the units above it from the maximum height of the I-Scan device.
  
- **Lower Border (Initial Position):**  
  The minimum height of each unit is calculated by adding the heights of the units below it to the initial height of the I-Scan device.

- **Conditions:**  
  - **"mid & top = max":** The middle and top units are at their maximum heights.
  - **"bot = min":** The bottom unit is at its minimum height.
  - **"top = max":** The top unit is at its maximum height.
  - **"mid & bot = min":** The middle and bottom units are at their minimum heights.

---

### 4. **Resolution Calculation**

For 30 pictures taken over a distance of 150 cm, the distance between measurement points is calculated as follows:

Here, &Delta; Z<sub>scan</sub> is the value `MaxDistanceZmove` from the JSON configuration provided earlier.

\[ \text{Distance Between Measurement Points} = \frac{\Delta Z_{\text{scan}}}{\text{Number of Pictures}} = \frac{150 \text{ cm}}{30} = 5 \text{ cm} \]

The distance between each picture is approximately **5 cm**.

### **Condition for &Delta; Z<sub>scan</sub>**

It is important to ensure that the value of &Delta; Z<sub>scan</sub> (the maximum distance the Z-axis can move during a scan) is less than or equal to &Delta; Z<sub>max</sub> (the maximum allowable height difference).

\[ \Delta Z_{\text{scan}} \leq \Delta Z_{\text{max}} \]

---

