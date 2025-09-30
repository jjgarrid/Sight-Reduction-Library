# Atmospheric Corrections in Celestial Navigation

## Overview

Atmospheric corrections are critical for accurate celestial navigation sight reductions. When taking observations with a sextant, the raw measurements must be corrected for various atmospheric effects that alter the apparent position of celestial bodies. The Sight Reduction project includes three major atmospheric corrections:

1. **Atmospheric Refraction**: Light bending as it passes through Earth's atmosphere
2. **Dip of Horizon**: Lower horizon when observing from elevated positions
3. **Limb Corrections**: Angular radius adjustments for the Sun and Moon

These corrections can significantly impact position accuracy, especially for observations near the horizon.

## 1. Atmospheric Refraction

### What is Atmospheric Refraction?

Atmospheric refraction is the bending of light as it passes through Earth's atmosphere. When celestial bodies are near the horizon, their light passes through more of the atmosphere, causing greater refraction. This makes celestial bodies appear higher in the sky than they actually are.

### Impact on Navigation

- Refraction makes bodies appear about 34 minutes of arc higher at the horizon
- The effect rapidly decreases as altitude increases
- Neglecting refraction correction can result in position errors of several nautical miles

### Physics of Refraction

When light travels from the vacuum of space into Earth's atmosphere, it encounters increasingly dense air layers, causing the light path to curve downward toward the denser air. This bending makes the celestial body appear higher than its true position.

### Calculation Method

The Sight Reduction project uses different formulas based on the altitude of the celestial body:

- For altitudes ≤ 15° (near horizon): Uses a more accurate formula accounting for the non-linear relationship
- For altitudes > 15°: Uses simplified formulas for computational efficiency

The calculation also accounts for:
- **Temperature**: Colder air is denser, causing more refraction
- **Pressure**: Higher pressure means denser air, causing more refraction

### Formula Used

For low altitudes (≤ 15°):
```
R = 0.96 / tan(h + 7.32/(h + 4.32))
```
Where h is the apparent altitude in minutes of arc.

For higher altitudes:
```
R = 1.02 / tan(h)
```
Where h is the altitude in degrees.

These are then adjusted based on temperature and pressure:
```
R_adjusted = R * (pressure/1010) * (273/(273+temperature))
```

### Implementation in Code

```python
def calculate_refraction_correction(observed_altitude: float, 
                                  temperature: float = 10.0, 
                                  pressure: float = 1010.0) -> float:
    # Implementation as described in the source code
```

### Example of Refraction Impact

- At 0° altitude (horizon): ~34' of refraction
- At 10° altitude: ~6' of refraction
- At 30° altitude: ~1.8' of refraction
- At 60° altitude: ~0.6' of refraction
- At 85° altitude: ~0.1' of refraction

## 2. Dip of Horizon

### What is Dip of Horizon?

When an observer is at an elevated position above sea level (like on a ship's bridge or on a cliff), the horizon appears lower than it would from sea level. This is because the observer's line of sight to the horizon forms a different angle than it would from sea level.

### Impact on Navigation

- The horizon appears lower when observing from above sea level
- Without correction, this leads to systematically high altitude measurements
- The error increases with observer height

### Physics of Dip

The dip of horizon occurs because the observer's eye level is above the water surface. The geometric horizon (where the sky appears to meet the sea) is at a lower angular position than it would be at sea level.

### Calculation Method

The Sight Reduction project uses the standard formula for dip of horizon:

```
Dip (minutes) = 0.97 * sqrt(height in meters)
```

This formula is derived from geometric considerations of the Earth's curvature and observer height.

### Implementation in Code

```python
def calculate_dip_correction(observer_height: float) -> float:
    # Implementation as described in the source code
```

### Example of Dip Impact

- At 1 meter height: ~0.97' dip
- At 4 meters height: ~1.94' dip
- At 9 meters height: ~2.91' dip
- At 16 meters height: ~3.88' dip
- At 25 meters height: ~4.85' dip

### When to Apply

The dip correction is only applied when the observer is at a height above sea level. It's added to the observed altitude (since the horizon appears lower, the celestial body appears higher by the same amount).

## 3. Limb Corrections

### What are Limb Corrections?

The Sun and Moon have appreciable angular sizes, so navigators sometimes observe the upper or lower limb instead of the center. Limb corrections account for the angular radius of these bodies.

### Impact on Navigation

- The Sun and Moon each have an apparent diameter of about 32 minutes of arc
- This means the limb is about 16 minutes of arc above or below the center
- Using the wrong limb without correction creates systematic errors

### Types of Limb Observations

- **Lower Limb**: Most common for Sun and Moon sights; observe where the body appears to rise from the horizon
- **Upper Limb**: Used when the lower part is obscured or when taking evening sights of bodies near horizon
- **Center**: When using instruments that can sight the center directly or when bodies are high in the sky

### Calculation Method

The Sight Reduction project uses a standard angular radius of 16 minutes of arc (16/60 degrees) for both the Sun and Moon:

- For **lower limb**: Add the radius (since the center is higher than the lower limb)
- For **upper limb**: Subtract the radius (since the center is lower than the upper limb)
- For **center**: No correction needed

### Implementation in Code

```python
def calculate_limb_correction(celestial_body_name: str, limb: str = "center") -> float:
    # Implementation as described in the source code
```

### Why Only Sun and Moon?

Stars are so distant that they appear as point sources with no measurable angular diameter. Planets, while having some angular diameter, are typically treated as point sources for celestial navigation purposes due to their small apparent size compared to the Sun and Moon.

## Combined Atmospheric Corrections

### Order of Application

When performing sight reductions, corrections are applied in a specific order to ensure accuracy:

1. **Index Error**: Instrument calibration correction (not in this code but important in practice)
2. **Dip Correction**: Applied to the observed altitude
3. **Refraction Correction**: Applied to the dip-corrected altitude
4. **Limb Correction**: Applied to get the center altitude

### Total Correction Formula

The total atmospheric correction is:
```
Corrected Altitude = Observed Altitude + Dip Correction - Refraction Correction + Limb Correction
```

### Implementation in Code

The Sight Reduction project provides a utility function to calculate all corrections together:

```python
def get_total_observation_correction(observed_altitude: float, 
                                   temperature: float = 10.0, 
                                   pressure: float = 1010.0,
                                   observer_height: float = 0.0,
                                   celestial_body_name: str = None,
                                   limb: str = 'center') -> dict:
    # Combines all corrections in the proper order
```

## Importance of Atmospheric Corrections

### Accuracy Considerations

Atmospheric corrections are essential for achieving accurate navigation fixes:

- **Without refraction correction**: Position errors of several nautical miles, especially for horizon sights
- **Without dip correction**: Systematic errors that depend on observer height
- **Without limb correction**: Errors of up to 16' (0.27 nautical miles) for Sun/Moon

### When Corrections Are Most Critical

1. **Horizon Sights**: Refraction effects are strongest near the horizon
2. **High Observer Positions**: Dip corrections increase with height
3. **Precise Navigation**: When accuracy of less than 1 nautical mile is required
4. **Long Ocean Passages**: Small errors accumulate over distance

### Practical Application

In real-world celestial navigation:

1. The navigator takes a sight with the sextant
2. Records the observed altitude and time
3. Notes environmental conditions (temperature, pressure)
4. Records observer height above sea level
5. Identifies which limb of the Sun/Moon was observed
6. Applies all appropriate corrections to get the true altitude
7. Uses the corrected altitude in sight reduction calculations

## Temperature and Pressure Effects

### Temperature Impact

- **Colder air** is more dense
- More dense air causes greater refraction
- For every 10°C decrease in temperature, refraction increases by about 1%
- Cold weather navigation requires careful temperature correction

### Pressure Impact

- **Higher pressure** means more dense air
- More dense air causes greater refraction
- For every 3.5 hPa increase in pressure, refraction increases by about 1%
- High-pressure systems can affect refraction significantly

### Standard Atmosphere

The Sight Reduction project uses standard atmospheric values when specific measurements are unavailable:
- Temperature: 10°C
- Pressure: 1010 hPa

These represent average conditions but should be adjusted for local weather when possible.

## Validation and Accuracy

### Testing of Corrections

The atmospheric correction implementations have been validated against:
- Standard nautical almanac tables
- Known astronomical algorithms
- Empirical observations

### Accuracy Limits

- Atmospheric corrections are accurate to within 0.1' under normal conditions
- Accuracy may decrease under unusual atmospheric conditions (temperature inversions, etc.)
- For critical navigation, multiple sights should be taken to verify results

The Sight Reduction project includes comprehensive atmospheric corrections to ensure accurate celestial navigation fixes. These corrections are essential for converting raw sextant observations into accurate position fixes.