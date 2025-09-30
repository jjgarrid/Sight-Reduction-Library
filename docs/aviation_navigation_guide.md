# Aeronautical Navigation Guide

This document provides comprehensive guidance on using the aeronautical navigation features of the Sight Reduction library for celestial navigation from aircraft.

## Table of Contents
1. [Introduction](#introduction)
2. [Key Differences from Marine Navigation](#key-differences-from-marine-navigation)
3. [Aircraft Navigation Setup](#aircraft-navigation-setup)
4. [Bubble Sextant Operations](#bubble-sextant-operations)
5. [Aircraft Movement Corrections](#aircraft-movement-corrections)
6. [Aviation Tables Integration](#aviation-tables-integration)
7. [Practical Examples](#practical-examples)
8. [Best Practices](#best-practices)

## Introduction

Aeronautical celestial navigation differs from marine navigation in several important ways due to the unique challenges of navigation from a moving aircraft at altitude. This library provides specialized tools to address these challenges while maintaining compatibility with traditional marine navigation methods.

Key features for aviation navigation include:
- Bubble sextant artificial horizon corrections
- Aircraft movement compensation
- Flight altitude atmospheric corrections
- Aviation table integration

## Key Differences from Marine Navigation

### Horizon Reference
- **Marine Navigation**: Uses the visible horizon as a natural reference
- **Aircraft Navigation**: Uses a bubble sextant with an artificial horizon, eliminating the need for a visible horizon

### Movement Compensation
- **Marine Navigation**: Vessel speeds are typically 5-25 knots with slower position changes
- **Aircraft Navigation**: Aircraft speeds are typically 150-500+ knots with rapid position changes requiring constant updates

### Atmospheric Corrections
- **Marine Navigation**: Standard sea-level atmospheric pressure and temperature
- **Aircraft Navigation**: Atmospheric conditions vary significantly with altitude, affecting refraction calculations

### Observation Conditions
- **Marine Navigation**: More stable platform with longer observation periods
- **Aircraft Navigation**: Platform experiences turbulence and motion, requiring rapid, averaged observations

## Aircraft Navigation Setup

To use aviation navigation features, specify the navigation mode parameter:

```python
from src.sight_reduction import calculate_intercept

# Aviation mode with default parameters
intercept, azimuth = calculate_intercept(
    observed_altitude=45.0,
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=observation_time,
    navigation_mode='aviation'  # Set navigation mode to aviation
)
```

## Bubble Sextant Operations

Bubble sextants provide an artificial horizon using a bubble mechanism, eliminating the need for a visible horizon. This is essential for high-altitude observations where a natural horizon is not visible.

### Bubble Sextant Corrections

The library includes functions to handle bubble sextant specific corrections:

```python
from src.sight_reduction import calculate_bubble_sextant_correction

# Calculate bubble sextant specific corrections
correction = calculate_bubble_sextant_correction(
    aircraft_altitude=3000.0,  # meters above sea level
    temperature=-20.0,         # temperature at flight altitude (°C)
    pressure=700.0             # pressure at flight altitude (hPa)
)
```

### Dip Correction Handling

In aviation mode, the library automatically handles dip correction differently:
- Marine mode: Applies dip correction based on observer height
- Aviation mode: No dip correction applied since bubble sextant provides artificial horizon

## Aircraft Movement Corrections

Aircraft move rapidly, and positions change significantly during observation periods. The library provides functions to account for this movement:

```python
from src.sight_reduction import calculate_movement_correction

# Calculate position correction for aircraft movement
corrected_position = calculate_movement_correction(
    assumed_position=original_position,
    observation_time=observation_time,
    aircraft_speed_knots=250.0,  # aircraft speed in knots
    aircraft_course=90.0,       # aircraft heading in degrees (0° = North)
    time_interval_hours=0.5     # time from reference observation in hours
)
```

### Time Interval Corrections

For celestial bodies that have moved during the observation interval:

```python
from src.sight_reduction import apply_time_interval_correction

# Apply time interval correction for celestial body movement
corrected_altitude = apply_time_interval_correction(
    observed_altitude=45.0,
    time_interval_hours=0.25,  # 15 minutes from reference
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=observation_time
)
```

## Aviation Tables Integration

The library provides support for aviation-specific navigation tables like Pub. No. 249 (Sight Reduction Tables for Air Navigation):

```python
from src.aviation_almanac import get_aviation_table_lookup

# Look up altitude and azimuth from aviation tables
lookup_result = get_aviation_table_lookup(
    assumed_lat=40.0,        # assumed latitude in degrees
    lha=45.0,               # local hour angle in degrees
    declination=20.0,       # declination in degrees
    table_volume=1          # which volume of Pub. No. 249 (1, 2, or 3)
)

computed_altitude = lookup_result['computed_altitude']
azimuth = lookup_result['azimuth']
correction = lookup_result['delta_correction']
```

## Practical Examples

### Complete Aviation Sight Reduction

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body
from src.aviation_almanac import get_aviation_celestial_body_data

# Setup for aviation navigation
observed_altitude = 42.5      # Observed altitude from bubble sextant (degrees)
celestial_body_name = 'sun'
observation_time = Time('2023-06-15T14:30:00')
aircraft_altitude = 2500.0    # meters above sea level
aircraft_speed = 200.0        # knots
aircraft_course = 45.0        # degrees (Northeast heading)

# Define the celestial body using aviation almanac data
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Set assumed position
assumed_position = EarthLocation(
    lat=40.5*u.deg, 
    lon=-73.8*u.deg, 
    height=0*u.m
)

# Perform aviation sight reduction with all corrections
intercept, azimuth = calculate_intercept(
    observed_altitude=observed_altitude,
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=observation_time,
    navigation_mode='aviation',
    observer_height=aircraft_altitude,  # Affects refraction calculation
    aircraft_speed_knots=aircraft_speed,
    aircraft_course=aircraft_course,
    time_interval_hours=0.0  # Time from reference observation
)

print(f"Aviation Sight Reduction Results:")
print(f"  Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away'}")
print(f"  Azimuth: {azimuth:.1f}°")
```

### Multiple Aircraft Position Fix

For improved accuracy, use multiple celestial observations:

```python
from src.position_fix import calculate_least_squares_fix
from src.sight_reduction import calculate_intercept, get_celestial_body

# Multiple observations from aircraft
sights = []

# First observation (Sun)
sun_body = get_celestial_body('sun', observation_time)
sun_intercept, sun_azimuth = calculate_intercept(
    observed_altitude=42.5,
    celestial_body=sun_body,
    assumed_position=assumed_position,
    observation_time=observation_time,
    navigation_mode='aviation',
    observer_height=aircraft_altitude
)

sights.append({
    'observed_altitude': 42.5,
    'celestial_body_name': 'sun',
    'observation_time': observation_time,
    'intercept': sun_intercept,
    'azimuth': sun_azimuth,
    'assumed_position': assumed_position,
    'altitude_correction_error': 0.1
})

# Second observation (Vega) - after accounting for aircraft movement
vega_body = get_celestial_body('vega', observation_time)
vega_intercept, vega_azimuth = calculate_intercept(
    observed_altitude=38.2,
    celestial_body=vega_body,
    assumed_position=assumed_position,  # Position corrected for aircraft movement
    observation_time=observation_time,
    navigation_mode='aviation',
    observer_height=aircraft_altitude
)

sights.append({
    'observed_altitude': 38.2,
    'celestial_body_name': 'vega',
    'observation_time': observation_time,
    'intercept': vega_intercept,
    'azimuth': vega_azimuth,
    'assumed_position': assumed_position,
    'altitude_correction_error': 0.1
})

# Calculate position fix using least squares method
fix_result = calculate_least_squares_fix(sights)
print(f"Aircraft Position Fix: {fix_result['fix_position']}")
print(f"Standard Deviation: {fix_result['standard_deviation']:.2f} nautical miles")
```

## Best Practices

### For Accurate Aircraft Navigation

1. **Use Appropriate Altitude Corrections**: Always specify aircraft altitude for accurate refraction calculations.

2. **Account for Movement**: Regularly update your position based on aircraft speed and course when taking multiple observations.

3. **Time Synchronization**: Use precise timekeeping as celestial positions change rapidly with aircraft movement.

4. **Multiple Observations**: Take multiple celestial observations to improve position accuracy.

5. **Weather Considerations**: Account for atmospheric conditions at flight altitude which affect refraction.

### Accuracy Considerations

- Aircraft position changes rapidly - account for this in your calculations
- Higher altitudes mean different atmospheric conditions affecting refraction
- Bubble sextant observations may require additional calibration
- Turbulence can affect observation precision

### Safety Notes

- Aeronautical celestial navigation is primarily a backup method
- Always cross-check with other navigation systems
- Be aware of limitations in instrument precision and observation conditions
- Consider the effect of aircraft attitude on bubble sextant stability

## Troubleshooting

### Common Issues

1. **Unexpected Intercept Values**: Check that navigation_mode is set to 'aviation' for aircraft operations.

2. **Azimuth Errors**: Verify aircraft course input and time interval calculations.

3. **Atmospheric Corrections**: Ensure aircraft altitude is properly specified for refraction calculations.

### Debugging Tips

- Use the `get_total_observation_correction` function to verify individual corrections
- Compare results with marine mode to understand aviation-specific differences
- Validate celestial body positions using almanac data

## References

- Air Almanac (published annually)
- Pub. No. 249 (Sight Reduction Tables for Air Navigation)
- Pub. No. 229 (Sight Reduction Tables for Marine Navigation)
- Aviation Navigation Standards