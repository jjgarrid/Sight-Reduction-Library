# Usage Examples for Sight Reduction

## Overview

This document provides detailed usage examples for the Sight Reduction project, demonstrating how to use the library for different celestial bodies and scenarios in celestial navigation.

## Basic Examples

### 1. Basic Sun Sight Reduction

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data for a sun sight
observed_altitude = 45.23  # Observed altitude (degrees)
celestial_body_name = "sun"
assumed_lat = 40.7128  # Assumed latitude (degrees)
assumed_lon = -74.0060  # Assumed longitude (degrees)
observation_time = Time("2023-06-15T12:00:00")

# Define the celestial body
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time
)

print(f"Observed Altitude: {observed_altitude:.2f}°")
print(f"Assumed Position: {assumed_lat}°N, {abs(assumed_lon)}°W")
print(f"Intercept: {abs(intercept):.2f} nautical miles {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
```

### 2. Moon Sight Reduction

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data for a moon sight
observed_altitude = 38.45  # Observed altitude (degrees)
celestial_body_name = "moon"
assumed_lat = 35.6895  # Assumed latitude (degrees) - Tokyo
assumed_lon = 139.6917  # Assumed longitude (degrees) - Tokyo
observation_time = Time("2023-06-15T22:30:00")  # Evening observation

# Define the celestial body
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time
)

print(f"Moon Sight Results:")
print(f"  Observed Altitude: {observed_altitude:.2f}°")
print(f"  Intercept: {abs(intercept):.2f} nautical miles {'Toward' if intercept > 0 else 'Away from'} moon")
print(f"  Azimuth: {azimuth:.2f}°")
```

## Advanced Examples with Atmospheric Corrections

### 3. Sun Sight with Atmospheric Corrections

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data with atmospheric conditions
observed_altitude = 45.23  # Observed altitude (degrees)
celestial_body_name = "sun"
assumed_lat = 40.7128  # Assumed latitude (degrees)
assumed_lon = -74.0060  # Assumed longitude (degrees)
observation_time = Time("2023-06-15T12:00:00")

# Atmospheric conditions
temperature = 15.0  # Celsius
pressure = 1020.0   # hPa
observer_height = 10.0  # Meters above sea level

# Define the celestial body
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction with atmospheric corrections
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time,
    apply_refraction=True,        # Apply atmospheric refraction correction
    temperature=temperature,      # Temperature for refraction calculation
    pressure=pressure,            # Pressure for refraction calculation
    observer_height=observer_height,  # Height above sea level for dip correction
    celestial_body_name=celestial_body_name,  # For limb correction
    limb='lower'                  # 'upper', 'lower', or 'center' for limb selection
)

print(f"Sun Sight with Atmospheric Corrections:")
print(f"  Observed Altitude: {observed_altitude:.2f}°")
print(f"  Temperature: {temperature}°C")
print(f"  Pressure: {pressure} hPa")
print(f"  Observer Height: {observer_height}m")
print(f"  Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} sun")
print(f"  Azimuth: {azimuth:.2f}°")
print(f"  Observation Time: {observation_time.isot}")
```

### 4. Star Sight Reduction (Polaris)

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data for Polaris sight
observed_altitude = 41.0  # Observed altitude (degrees) - Approximates latitude
celestial_body_name = "star"  # Polaris
assumed_lat = 40.7128  # Assumed latitude (degrees)
assumed_lon = -74.0060  # Assumed longitude (degrees)
observation_time = Time("2023-06-15T01:00:00")  # Night observation

# Define the celestial body (using default star - Polaris)
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction for star
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time
)

print(f"Polaris Sight Results:")
print(f"  Observed Altitude: {observed_altitude:.2f}°")
print(f"  Intercept: {abs(intercept):.2f} nautical miles {'Toward' if intercept > 0 else 'Away from'} Polaris")
print(f"  Azimuth: {azimuth:.2f}°")
print(f"  Note: Polaris is near the celestial north pole, so azimuth should be close to 0°")
```

## Complete Example with All Corrections

### 5. Full Calculation with Correction Breakdown

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import (
    calculate_intercept, 
    get_celestial_body,
    get_total_observation_correction
)

# Full example with detailed corrections
observed_altitude = 32.75  # Raw sextant altitude
celestial_body_name = "sun"
assumed_lat = 25.7617  # Miami latitude
assumed_lon = -80.1918  # Miami longitude
observation_time = Time("2023-07-04T14:30:00")

# Atmospheric conditions
temperature = 28.0  # Celsius (hot day)
pressure = 1013.0   # hPa
observer_height = 5.0  # Meters above sea level (on a small boat)
limb_observed = 'lower'  # Observing lower limb of the sun

print("=== Full Sight Reduction Example ===")
print(f"Observed Altitude: {observed_altitude:.2f}°")
print(f"Celestial Body: {celestial_body_name}")
print(f"Assumed Position: {assumed_lat}°N, {abs(assumed_lon)}°W")
print(f"Observation Time: {observation_time.isot}")
print(f"Temperature: {temperature}°C, Pressure: {pressure} hPa")
print(f"Observer Height: {observer_height}m")
print(f"Limb Observed: {limb_observed}")
print()

# Break down all corrections
corrections = get_total_observation_correction(
    observed_altitude=observed_altitude,
    temperature=temperature,
    pressure=pressure,
    observer_height=observer_height,
    celestial_body_name=celestial_body_name,
    limb=limb_observed
)

print("=== Correction Breakdown ===")
print(f"Observed Altitude: {corrections['observed_altitude']:.4f}°")
print(f"Refraction Correction: -{corrections['refraction_correction']:.4f}°")
print(f"Dip Correction: +{corrections['dip_correction']:.4f}°")
print(f"Limb Correction: +{corrections['limb_correction']:.4f}°")
print(f"Corrected Altitude: {corrections['corrected_altitude']:.4f}°")
print(f"Total Correction: {corrections['total_correction']:.4f}°")
print()

# Now perform the complete sight reduction
celestial_body = get_celestial_body(celestial_body_name, observation_time)
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

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
    limb=limb_observed
)

print("=== Final Results ===")
print(f"Intercept: {abs(intercept):.2f} nautical miles {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
print(f"Line of Position: Plot from assumed position along azimuth, intercept distance {'toward' if intercept > 0 else 'away from'} celestial body")
```

## Multiple Sights Example

### 6. Morning Sun Line and Evening Sun Line

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

def perform_sight(observed_altitude, observation_time, celestial_body_name, assumed_position, **corrections):
    """Helper function to perform a sight reduction with common parameters"""
    celestial_body = get_celestial_body(celestial_body_name, observation_time)
    return calculate_intercept(
        observed_altitude=observed_altitude,
        celestial_body=celestial_body,
        assumed_position=assumed_position,
        observation_time=observation_time,
        **corrections
    )

# Assumed position (could be dead reckoning position)
assumed_lat = 30.0  # degrees
assumed_lon = -60.0  # degrees
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Morning sun sight
morning_altitude = 15.5
morning_time = Time("2023-06-15T08:30:00")

# Evening sun sight
evening_altitude = 20.8
evening_time = Time("2023-06-15T18:45:00")

# Atmospheric conditions
atmospheric_conditions = {
    'apply_refraction': True,
    'temperature': 20.0,
    'pressure': 1015.0,
    'observer_height': 3.0,
    'celestial_body_name': 'sun',
    'limb': 'lower'
}

print("=== Morning Sun Sight ===")
morning_intercept, morning_azimuth = perform_sight(
    morning_altitude, 
    morning_time, 
    'sun', 
    assumed_position,
    **atmospheric_conditions
)
print(f"  Time: {morning_time.isot}")
print(f"  Observed Altitude: {morning_altitude:.2f}°")
print(f"  Intercept: {abs(morning_intercept):.2f} nm {'Toward' if morning_intercept > 0 else 'Away'}")
print(f"  Azimuth: {morning_azimuth:.2f}°")

print("\n=== Evening Sun Sight ===")
evening_intercept, evening_azimuth = perform_sight(
    evening_altitude, 
    evening_time, 
    'sun', 
    assumed_position,
    **atmospheric_conditions
)
print(f"  Time: {evening_time.isot}")
print(f"  Observed Altitude: {evening_altitude:.2f}°")
print(f"  Intercept: {abs(evening_intercept):.2f} nm {'Toward' if evening_intercept > 0 else 'Away'}")
print(f"  Azimuth: {evening_azimuth:.2f}°")

print("\n=== Position Fix ===")
print("With two sun lines, you can determine a fix by finding the intersection")
print("of the two position lines. Plot the lines on a chart using the intercept")
print("and azimuth from each observation.")
```

## Jupyter Notebook Example

### 7. Using with Jupyter Notebooks

If you're using the provided Jupyter notebook (`sight.ipynb`), here's how to structure your analysis:

```python
# In a Jupyter notebook cell
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
import matplotlib.pyplot as plt
from src.sight_reduction import calculate_intercept, get_celestial_body

# Example: Plot intercepts for different assumed positions
assumed_lats = [40.5, 40.6, 40.7, 40.8, 40.9]
assumed_lon = -74.0060

observed_altitude = 45.23
celestial_body_name = "sun"
observation_time = Time("2023-06-15T12:00:00")

intercepts = []
azimuths = []

for lat in assumed_lats:
    celestial_body = get_celestial_body(celestial_body_name, observation_time)
    assumed_position = EarthLocation(lat=lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)
    
    intercept, azimuth = calculate_intercept(
        observed_altitude, 
        celestial_body, 
        assumed_position, 
        observation_time
    )
    
    intercepts.append(intercept)
    azimuths.append(azimuth)

# Plot the results
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(assumed_lats, intercepts, 'bo-')
plt.title('Intercept vs Latitude')
plt.xlabel('Assumed Latitude (°N)')
plt.ylabel('Intercept (nautical miles)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(assumed_lats, azimuths, 'ro-')
plt.title('Azimuth vs Latitude')
plt.xlabel('Assumed Latitude (°N)')
plt.ylabel('Azimuth (°)')
plt.grid(True)

plt.tight_layout()
plt.show()
```

## Error Handling Examples

### 8. Safe Usage with Error Handling

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

def safe_sight_reduction(observed_altitude, celestial_body_name, assumed_lat, assumed_lon, observation_time_str):
    """Wrapper function with error handling"""
    try:
        # Validate inputs
        if not -1 <= observed_altitude <= 90:
            raise ValueError(f"Invalid altitude: {observed_altitude}. Must be between -1° and 90°")
        
        # Parse time string
        observation_time = Time(observation_time_str)
        
        # Create celestial body and assumed position
        celestial_body = get_celestial_body(celestial_body_name, observation_time)
        assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)
        
        # Calculate intercept
        intercept, azimuth = calculate_intercept(
            observed_altitude, 
            celestial_body, 
            assumed_position, 
            observation_time
        )
        
        return {
            'success': True,
            'intercept': intercept,
            'azimuth': azimuth,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'intercept': None,
            'azimuth': None,
            'error': str(e)
        }

# Example usage with error handling
result = safe_sight_reduction(
    observed_altitude=45.0,
    celestial_body_name="sun",
    assumed_lat=40.7128,
    assumed_lon=-74.0060,
    observation_time_str="2023-06-15T12:00:00"
)

if result['success']:
    print(f"Successful calculation:")
    print(f"  Intercept: {abs(result['intercept']):.2f} nm {'Toward' if result['intercept'] > 0 else 'Away'}")
    print(f"  Azimuth: {result['azimuth']:.2f}°")
else:
    print(f"Error in calculation: {result['error']}")
```

## Real-world Scenario Examples

### 9.航海 Scenario: Offshore Navigation

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body, format_position

# Simulate a navigation scenario at sea
print("=== Offshore Navigation Scenario ===")
print("Ship position estimated at 25°N, 75°W in the Atlantic")
print("Taking morning sun sight at 0930 UTC\n")

# Dead reckoning position
dr_lat = 25.0  # degrees
dr_lon = -75.0  # degrees

# Sextant observation
observed_altitude = 42.18  # Measured with sextant
celestial_body_name = "sun"
observation_time = Time("2023-07-15T09:30:00")  # UTC time

# Environmental conditions
temperature = 25.0  # Celsius (warm day at sea)
pressure = 1012.0   # hPa
observer_height = 4.0  # Meters above sea level (bridge of ship)
limb = 'lower'  # Sun lower limb observation

print(f"Dead Reckoning Position: {format_position(dr_lat, dr_lon)}")
print(f"Observation Time (UTC): {observation_time.isot}")
print(f"Observed Altitude: {observed_altitude:.2f}°")
print(f"Environmental Conditions: {temperature}°C, {pressure} hPa")
print(f"Observer Height: {observer_height}m (Bridge height)")
print()

# Perform sight reduction
celestial_body = get_celestial_body(celestial_body_name, observation_time)
assumed_position = EarthLocation(lat=dr_lat*u.deg, lon=dr_lon*u.deg, height=0*u.m)

intercept, azimuth = calculate_intercept(
    observed_altitude=observed_altitude,
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=observation_time,
    apply_refraction=True,
    temperature=temperature,
    pressure=pressure,
    observer_height=observer_height,
    celestial_body_name=celestial_body_name,
    limb=limb
)

print("=== Sight Reduction Results ===")
print(f"Intercept: {abs(intercept):.2f} nautical miles {'Toward' if intercept > 0 else 'Away from'} sun")
print(f"Azimuth: {azimuth:.2f}°")
print(f"Line of Position: Plot from DR position along {azimuth:.2f}° azimuth")
print(f"  Distance: {abs(intercept):.2f} nm {'toward' if intercept > 0 else 'away from'} celestial body")
print()
print("This line of position, combined with other sights or dead reckoning,")
print("helps determine the ship's actual position.")
```

These examples demonstrate the various ways to use the Sight Reduction library for different celestial navigation scenarios, from basic sun sights to complex multi-body fixes with atmospheric corrections.

## New Features: Problem Generation and Almanac Integration

For examples of the new features including sight reduction problem generation and almanac integration, see [Extended Usage Examples](usage_examples_extended.md).