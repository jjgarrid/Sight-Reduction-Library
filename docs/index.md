# Sight Reduction Documentation

## Overview
The Sight Reduction package provides tools for performing celestial navigation sight reductions. This allows navigators to determine their position based on observations of celestial bodies.

## Table of Contents
- [Complete Project Documentation](sight_reduction_documentation.md) - Comprehensive guide covering all aspects of the project
- [Aeronautical Navigation Guide](aviation_navigation_guide.md) - Complete guide to celestial navigation from aircraft
- [Installation Guide](installation_guide.md) - Step-by-step installation and setup instructions
- [API Reference](api_reference.md) - Detailed documentation of all functions and their parameters
- [Usage Examples](usage_examples.md) - Practical examples for different celestial bodies and scenarios
- [Extended Usage Examples](usage_examples_extended.md) - Examples of new features including problem generation and almanac integration
- [Advanced Position Fix Calculation](position_fix_documentation.md) - Documentation for position fixing algorithms
- [LaTeX Documentation Tutorial](latex_tutorial.md) - Step-by-step tutorial for using the LaTeX output features
- [Atmospheric Corrections](atmospheric_corrections.md) - In-depth explanation of refraction, dip, and limb corrections
- [Testing and Validation](testing_validation.md) - Information about testing strategy and quality assurance

## Core API Reference

### `calculate_intercept(observed_altitude, celestial_body, assumed_position, observation_time, apply_refraction=True, temperature=10.0, pressure=1010.0, observer_height=0.0, celestial_body_name=None, limb='center')`

Perform a sight reduction to calculate the intercept and azimuth with atmospheric corrections.

**Parameters:**
- `observed_altitude`: Observed altitude of the celestial body (degrees)
- `celestial_body`: Astropy SkyCoord object for the celestial body
- `assumed_position`: EarthLocation object for the assumed observer position
- `observation_time`: Astropy Time object for the observation time
- `apply_refraction`: Whether to apply atmospheric refraction correction (default True)
- `temperature`: Atmospheric temperature in degrees Celsius (default 10°C)
- `pressure`: Atmospheric pressure in hPa (default 1010 hPa)
- `observer_height`: Height of observer above sea level in meters (default 0)
- `celestial_body_name`: Name of celestial body ('sun', 'moon') for limb correction
- `limb`: Which part of the celestial body to observe ('center', 'upper', 'lower')

**Returns:**
- `intercept`: Distance between observed and calculated altitude (nautical miles)
- `azimuth`: Calculated azimuth of the celestial body (degrees)

### `get_celestial_body(name, observation_time)`

Get the appropriate celestial body based on name.

**Parameters:**
- `name`: Name of the celestial body ('sun', 'moon', or 'star' for Polaris)
- `observation_time`: Astropy Time object for the observation time

**Returns:**
- Astropy SkyCoord object for the celestial body

### `format_position(lat, lon)`

Format latitude and longitude in degrees, minutes, and seconds.

**Parameters:**
- `lat`: Latitude in decimal degrees
- `lon`: Longitude in decimal degrees

**Returns:**
- Formatted position string

## Usage Examples

### Basic Sight Reduction
```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Define observation parameters
observed_altitude = 45.23  # degrees
observation_time = Time("2023-06-15T12:00:00")
celestial_body = get_celestial_body("sun", observation_time)
assumed_position = EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m)

# Calculate intercept and azimuth
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time
)

print(f"Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
```

### Sight Reduction with Atmospheric Corrections
```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Define observation parameters with atmospheric conditions
observed_altitude = 45.23  # degrees
observation_time = Time("2023-06-15T12:00:00")
celestial_body_name = "sun"
celestial_body = get_celestial_body(celestial_body_name, observation_time)
assumed_position = EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m)

# Atmospheric conditions
temperature = 15.0  # Celsius
pressure = 1020.0   # hPa
observer_height = 10.0  # Meters above sea level

# Calculate intercept and azimuth with atmospheric corrections
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time,
    apply_refraction=True,
    temperature=temperature,
    pressure=pressure,
    observer_height=observer_height,
    celestial_body_name=celestial_body_name,
    limb='lower'
)

print(f"Intercept with corrections: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
```

## Celestial Navigation Basics

### The Concept
Celestial navigation uses the geometric relationship between the observer on Earth and the celestial sphere. When you observe a celestial body with a sextant, you're measuring the angle between the horizon and the body.

### Sight Reduction Process
1. Take a sextant sight of a celestial body
2. Record the exact time of the observation
3. Use an assumed position near your estimated location
4. Calculate where the celestial body should be in the sky based on the assumed position and time
5. Compare the calculated altitude to the observed altitude to determine the intercept
6. Use the calculated azimuth to determine the direction to the celestial body
7. Plot this information on a chart to create a line of position

### Accuracy Notes
The calculations in this package use high-precision astrometric data from the Astropy library, implementing the IAU standards for celestial mechanics. This provides accuracy suitable for navigation. Atmospheric corrections are included for improved accuracy, particularly important for observations near the horizon.

## Units and Conventions
- All angles are in degrees unless otherwise specified
- Times use UTC (Coordinated Universal Time)
- Positions are in latitude and longitude (WGS84)
- Distances in nautical miles
- Azimuths measured clockwise from true north (0° to 360°)
- Temperature in degrees Celsius
- Pressure in hPa (hectopascals)
- Heights in meters above sea level

## References
- [The Nautical Almanac](https://www.nauticalalmanac.com/)
- [Astropy Documentation](https://docs.astropy.org/en/stable/)
- [USNO Astronomical Applications](https://aa.usno.navy.mil/)