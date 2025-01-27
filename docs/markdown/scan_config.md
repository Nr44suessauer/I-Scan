![Scan Configuration Diagram](https://raw.githubusercontent.com/Nr44suessauer/I-Scan/394e9c62a99091687f8dc8185e1e62f2290e5e6f/docs/diagram/FlowDiagrams_API_Webserver/Scan%20config.svg){ width=50% }


**Send JSON (Post/Put command)**
- Configuration of the "next" scan

```json
{
    "MeasurementUnitInUse": ["Top", "Mid", "Bot"],
    "MeasurementUnitSize" : ["15","15","15"],
    "DistanceToObject": "100cm",
    "HeightOfObject": "50cm",
    "NumberOfPictures": 30,
    "MaxDistanceZmove": "170cm"
}
```

**Maximum Delta Z**

If the endstop Z is at 0 cm and the maximum height of the device is 210 cm, the maximum Delta Z can be calculated.

To calculate the maximum height, we need to know the size of each module. In our example, these are standardized to 15 cm.

The modules are labeld (Bot = 0, Mid = 1, Top = 2) and is the variable Z Endstop Unit.

Substituting the values

```math
\Delta Z_{\text{max}} = (\text{Z}_{\text{Endstop Unit}} \times \text{Unit Height} + \text{Maximum Height I-Scan}) - (\text{Z}_{\text{Endstop Mid}} \times \text{Unit Height} + \text{Z}_{\text{Endstop Top}} \times \text{Unit Height})
```

So the maximum Delta Z for Unit Bot is 180 cm.

---

### Transition to Integral Representation

To represent the height changes of units using integrals, we start with the equation and replace the discrete measurements with continuous functions:

1. **Define Continuous Functions:**
   - \( f_{\text{unit}}(z) \)
   - \( f_{\text{mid}}(z) \)
   - \( f_{\text{top}}(z) \)

2. **Integrate Over the Range:**
   - \(\int_{a}^{b} f_{\text{unit}}(z) \, dz\)
   - \(\int_{a}^{b} f_{\text{mid}}(z) \, dz\)
   - \(\int_{a}^{b} f_{\text{top}}(z) \, dz\)

3. **Calculate the Difference:**
   \[
   \Delta Z_{\text{max}} = \left( \int_{a}^{b} f_{\text{unit}}(z) \, dz + \text{Maximum Height I-Scan} \right) - \left( \int_{a}^{b} f_{\text{mid}}(z) \, dz + \int_{a}^{b} f_{\text{top}}(z) \, dz \right)
   \]

This approach provides a continuous representation of the height changes.
> Note: This formula is only intended for the case of 3 modules.


---

**Calculate resolution | for 30 Pictures over a Distance of 170 cm**

If 30 pictures are taken over a distance of 170 cm, the distance between each picture can be calculated.
The distance \(\Delta Z_{\text{scan}}\) is the distance we previously sent.

```math
\text{Distance between MeasurementPoints} = \frac{\Delta Z_{\text{scan}}}{\text{Number of Pictures}}
```

Substituting the values:

```math
\text{Distance between MeasurementPoints} = \frac{170 \text{ cm}}{30} \approx 5.67 \text{ cm}
```

So, the distance between each picture is approximately 5.67 cm.



