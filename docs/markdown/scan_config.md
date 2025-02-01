## Scan config

<div style="display: flex; align-items: center; margin-top: 50px;">
<p></p>
</div>

<div style="display: flex; align-items: center;">
   <div style="flex: 1;">
      <img src="https://raw.githubusercontent.com/Nr44suessauer/I-Scan/e3244204858e6e4e7f5cfc8a78d4bcee4665ab8d/docs/diagram/FlowDiagrams_API_Webserver/Scan%20config.svg" alt="Scan Config Diagramm" width="70%">
   </div>
   <div style="flex: 1; padding-left: 0px;">
   In this configuration step, parameters required for aligning the machine are processed. This assumes that <strong>all devices being used are also configured</strong>. Currently, both configuration processes (device config & scan config) are not dependent on each other.
   <div style="display: flex; align-items: center; margin-top: 50px;">
   <p></p>
   </div>
   <h3>Scan Configuration</h3>
   <p>The parameters for configuring the scan are defined, explained, and put into context here:</p>
   <ol>
      <li><a href="#send-json-postput-command">Send JSON (Post/Put command)</a></li>
      <li><a href="#maximum-delta-z">Maximum Delta Z</a>
         <ul>
            <li><a href="#integral-representation">Integral Representation and Height Calculation</a></li>
            <li><a href="#upper-max-lower-max">Upper Max / Lower Max Table</a></li>
         </ul>
      </li>
      <li><a href="#module-offset">Module Offset</a></li>
      <li><a href="#resolution-calculation">Resolution Calculation</a></li>
   </ol>
   </div> 
</div>

<div style="display: flex; align-items: center; margin-top: 50px;">
   <p></p>
</div>

---

### <a id="send-json-postput-command"></a>Send JSON (Post/Put command)
- Configuration of the "next" scan

```json
{
   "MeasurementUnitInUse": ["Top", "Mid", "Bot"],
   "MeasurementUnitSize" : ["15","15","15"],
   "ModuleHeadOffsets": ["5cm", "7.5cm", "5cm", "7.5cm", "5cm", "7.5cm", "5cm", "7.5cm"],
   "NumberOfPictures": "30",
   "MaxDistanceZmove": "150cm",
   "DistanceToCenter": "150cm",
   "HeightOfObject": "50cm"
}
```

### <a id="maximum-delta-z"></a>Maximum Delta Z

If the endstop Z is at 0 cm and the maximum height of the device is 210 cm, the maximum Delta Z can be calculated.

To calculate the maximum height, we need to know the size of each unit. In our example, these are standardized to 15 cm.

The units are labeled (Bot = 0, Mid = 1, Top = 2) and is the variable Z Endstop Unit.

Substituting the values:

\[ \Delta Z_{\text{maxUnit}} = (\text{Z}_{\text{Endstop Unit}} \times \text{Unit Height} + \text{Maximum Height I-Scan}) - (\text{Z}_{\text{Endstop Mid}} \times \text{Unit Height} + \text{Z}_{\text{Endstop Top}} \times \text{Unit Height}) \]

So the ΔZmax for Unit bot is 165 cm.
>note: This formula is only for three same size units.

---

### <a id="integral-representation"></a>Integral Representation and Height Calculation

<div style="display: flex; align-items: center; margin-top: 20px;">
   <p></p>
</div>

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

### <a id="upper-max-lower-max"></a>Upper Max / Lower Max Table

The table below shows the dependency of the maximum and minimum heights of each unit based on the positions of the other units. The reference is taken from the bottom of the unit.

| Unit  | Upper Border (Maximum) | Lower Border (Initial Position) | Condition Upper Border | Condition Lower Border |
|-------|------------------------|---------------------------------|------------------------|------------------------|
| **Bot** | \( \text{Max } Z_{\text{bot}} = \text{Maximum Height I-Scan} - \left( \int_{a}^{b} f_{\text{bot}}(z) \, dz + \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right) \) | \( \text{Min } Z_{\text{bot}} = \text{Initial Height I-Scan} \) | \( Z_{\text{mid}} \) & \( Z_{\text{top}} \) = \( Z_{\text{max}} \) | - |
| **Mid** | \( \text{Max } Z_{\text{mid}} = \text{Maximum Height I-Scan} - \left( \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right) \) | \( \text{Min } Z_{\text{mid}} = \text{Initial Height I-Scan} + \int_{a}^{b} f_{\text{bot}}(z) \, dz \) | \( Z_{\text{top}} \) = \( Z_{\text{max}} \) | \( Z_{\text{bot}} \) = \( Z_{\text{min}} \) |
| **Top** | \( \text{Max } Z_{\text{top}} = \text{Maximum Height I-Scan} - \int_{a}^{b} f_{\text{top}}(z) \, dz \) | \( \text{Min } Z_{\text{top}} = \text{Initial Height I-Scan} + \left( \int_{a}^{b} f_{\text{bot}}(z) \, dz + \int_{a}^{b} f_{\text{mid}}(z) \, dz \right) \) | - | \( Z_{\text{mid}} \) & \( Z_{\text{bot}} \) = \( Z_{\text{min}} \) |


<div style="display: flex; align-items: center; margin-top: 20px;">
   <p></p>
</div>

### Table Description:
- **Upper Border (Maximum):**  
  The maximum height of each unit is calculated by subtracting the heights of the units above it from the maximum height of the I-Scan device.

- **Lower Border (Initial Position):**  
  The minimum height of each unit is calculated by adding the heights of the units below it to the initial height of the I-Scan device.
  
- **Conditions:**
- **\( Z_{\text{mid}} \) & \( Z_{\text{top}} \) = \( Z_{\text{max}} \):** The middle and top units are at their maximum heights.
- **\( Z_{\text{bot}} \) = \( Z_{\text{min}} \):** The bottom unit is at its minimum height.
- **\( Z_{\text{top}} \) = \( Z_{\text{max}} \):** The top unit is at its maximum height.
- **\( Z_{\text{mid}} \) & \( Z_{\text{bot}} \) = \( Z_{\text{min}} \):** The middle and bottom units are at their minimum heights.
   
### General Movement condition
- **Z<sub>bot</sub> < Z<sub>mid</sub> < Z<sub>top</sub>** 

---

### <a id="module-offset"></a>Module Offset

The module offset indicates the 2-dimensional offset from the reference point \( (X_{\text{unit}}, Y_{\text{unit}}) \). This value, along with the unit position, is required to determine the exact position of the modul. The offset can vary from module to module. It is assumed that measuring tools are mounted centrally on the units. If this is not the case, an additional offset vector must be considered.

To determine the exact position \( P_{\text{unit}} \) of the measurement unit, the following formulas can be used:

**For the 2D Case (X, Y Plane):**
\[
P_{\text{unit}} = \left( X_{\text{unit}} + \text{Offset}_{X}, Y_{\text{unit}} + \text{Offset}_{Y} \right)
\]

**For the 3D Case (X, Y, Z Space):**
\[
P_{\text{unit}} = \left( X_{\text{unit}} + \text{Offset}_{X}, Y_{\text{unit}} + \text{Offset}_{Y}, Z_{\text{unit}} + \text{Offset}_{Z} \right)
\]

### **Definitions:**
- \( X_{\text{unit}}, Y_{\text{unit}}, Z_{\text{unit}} \) represent the original position of the measurement unit in 3D space.
- \( \text{Offset}_{X} \) is the offset along the X-axis.
- \( \text{Offset}_{Y} \) is the offset along the Y-axis.
- \( \text{Offset}_{Z} \) is the offset along the Z-axis (if needed).

**Note:** The \( \text{Offset}_{Z} \) is not required for the scanning process but is used later during the processing of measurements on the external system.

By applying these formulas, the module's position can be precisely calculated and adjusted for varying mounting configurations.

---



### Calculation of Measurement Angle

#### Right-Angled Triangles

In this chapter, we will show how to calculate the angle \( \alpha \) in a right-angled triangle when one side is variable. For our example:
- **Side A** is the \( Z_{\text{dist}} \).
- **Side B** is the `DistanceToCenter` \( 150 \) cm (this value is in the JSON configuration). Side B refers to the standardized center of the machine.

### Mathematical Derivation

In a right-angled triangle, the tangent of an angle can be defined.
Since \( \alpha \) is the angle opposite to Side A, and Side B is the adjacent side, it follows:

\[ 
\tan(\alpha) = \frac{Z_{\text{dist}}}{\text{DistanceToOCenter}} 
\]

To calculate \( \alpha \), the arctangent (\( \arctan \)) is used:
\[ 
\alpha = \arctan\left(\frac{Z_{\text{dist}}}{\text{DistanceToCenter}}\right) 
\]
   
- **Example with \( Z_{\text{dist}} = 150 \) cm and \( \text{DistanceToCenter} = 150 \) cm:**  
   \[ 
   \alpha = \arctan\left(\frac{150}{150}\right) = 45° 
   \]

Using this method, any value for \( Z_{\text{dist}} \) can be substituted to calculate the corresponding angle \( \alpha \) in a right-angled triangle.



### Define Measurement Center

The variable \( Z_{\text{dist}} \) can also be used to determine the measurement center. This ensures that larger objects remain centered during measurements. The calculation is as follows:

\[ Z_{\text{dist}} = Z_{\text{center}} - Z_{\text{module}} \]

Here, \( Z_{\text{module}} \) represents the height of the respective unit, \( Z_{\text{center}} \) is our defined center point.

This formula helps in maintaining the central alignment of objects during the scanning process.

#### Z<sub>module</sub> Calculation

The height \( Z_{\text{module}} \) is calculated by adding the height of the unit \( Z_{\text{unit}} \) and its offset \( \text{Offset}_{Y} \):

\[ Z_{\text{module}} = Z_{\text{unit}} + \text{Offset}_{Y} \]

This ensures that the module's height is accurately determined by considering both the unit's height and its offset.

### Summary

In summary, \( Z_{\text{dist}} \) is our relative distance to the center, and the angle \( \alpha \) is calculated based on this distance. This ensures accurate and centered measurements during the scanning process.











---













### <a id="resolution-calculation"></a>Resolution Calculation

For 30 pictures taken over a distance of 150 cm, the distance between measurement points is calculated as follows:

Here, &Delta; Z<sub>scan</sub> is the value `MaxDistanceZmove` from the JSON configuration provided earlier.

<div style="display: flex; align-items: center; margin-top: 20px;">
   <p></p>
</div>

\[ \text{Distance Between Measurement Points} = \frac{\Delta Z_{\text{scan}}}{\text{Number of Measurements}} = \frac{150 \text{ cm}}{30} = 5 \text{ cm} \]

The distance between each picture is approximately **5 cm**.

\[ \text{Resolution} = \text{Distance Between Measurement Points} \times \text{Number of Measurements} \]

<div style="display: flex; align-items: center; margin-top: 20px;">
   <p></p>
</div>

#### **Condition for &Delta; Z<sub>scan</sub>**

It is important to ensure that the value of &Delta; Z<sub>scan</sub> (the maximum distance the Z-axis can move during a scan) is less than or equal to &Delta; Z<sub>max</sub> (the maximum allowable height difference).

\[ 
\Delta Z_{\text{scan}} \leq \Delta Z_{\text{max}} 
\]



---