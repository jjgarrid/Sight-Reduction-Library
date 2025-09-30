# API Reference for Sight Reduction Module

## Overview

The Sight Reduction module provides functions for performing celestial navigation sight reductions, including calculating intercepts and azimuths based on celestial observations with atmospheric corrections.

## Module Structure

```python
from src.sight_reduction import (
    calculate_intercept,
    calculate_refraction_correction,
    calculate_dip_correction,
    calculate_limb_correction,
    apply_refraction_correction,
    get_total_observation_correction,
    get_celestial_body,
    format_position,
    validate_altitude,
    validate_temperature,
    validate_pressure,
    validate_observer_height,
    validate_celestial_body_name,
    validate_limb
)
```

## Core Functions

### `calculate_intercept`

Perform a sight reduction to calculate the intercept (distance and direction) and azimuth with atmospheric corrections.

#### Function Signature
```python
def calculate_intercept(
    observed_altitude,
    celestial_body,
    assumed_position,
    observation_time,
    apply_refraction=True,
    temperature=10.0,
    pressure=1010.0,
    observer_height=0.0,
    celestial_body_name=None,
    limb='center'
):
```

#### Parameters
- **observed_altitude** (`float`): Observed altitude of the celestial body (degrees)
- **celestial_body** (`astropy.coordinates.SkyCoord`): Astropy SkyCoord object for the celestial body
- **assumed_position** (`astropy.coordinates.EarthLocation`): EarthLocation object for the assumed observer position
- **observation_time** (`astropy.time.Time`): Astropy Time object for the observation time
- **apply_refraction** (`bool`, optional): Whether to apply atmospheric refraction correction (default True)
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)
- **observer_height** (`float`, optional): Height of observer above sea level in meters (default 0)
- **celestial_body_name** (`str`, optional): Name of the celestial body ('sun', 'moon', etc.) for limb correction
- **limb** (`str`, optional): Which part of the celestial body to observe ('center', 'upper', 'lower') (default 'center')

#### Returns
- **intercept** (`float`): Distance between observed and calculated altitude (nautical miles)
- **azimuth** (`float`): Calculated azimuth of the celestial body (degrees)

#### Example
```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

observation_time = Time("2023-06-15T12:00:00")
celestial_body = get_celestial_body("sun", observation_time)
assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)

intercept, azimuth = calculate_intercept(
    observed_altitude=45.0,
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=observation_time
)
```

### `calculate_refraction_correction`

Calculate atmospheric refraction correction for celestial observations.

#### Function Signature
```python
def calculate_refraction_correction(
    observed_altitude: float,
    temperature: float = 10.0,
    pressure: float = 1010.0
) -> float:
```

#### Parameters
- **observed_altitude** (`float`): The observed altitude of the celestial body in degrees
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)

#### Returns
- **refraction_correction** (`float`): Refraction correction in degrees to be subtracted from observed altitude

#### Example
```python
correction = calculate_refraction_correction(
    observed_altitude=30.0,
    temperature=15.0,
    pressure=1020.0
)
```

### `apply_refraction_correction`

Apply atmospheric refraction correction to convert observed altitude to true altitude.

#### Function Signature
```python
def apply_refraction_correction(
    observed_altitude: float,
    temperature: float = 10.0,
    pressure: float = 1010.0
) -> float:
```

#### Parameters
- **observed_altitude** (`float`): The raw altitude measured with the sextant in degrees
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)

#### Returns
- **true_altitude** (`float`): True altitude in degrees (after refraction correction)

#### Example
```python
true_alt = apply_refraction_correction(
    observed_altitude=30.0,
    temperature=15.0,
    pressure=1020.0
)
```

### `calculate_dip_correction`

Calculate the dip of the horizon correction for an elevated observer.

#### Function Signature
```python
def calculate_dip_correction(observer_height: float) -> float:
```

#### Parameters
- **observer_height** (`float`): Height of observer above sea level in meters

#### Returns
- **dip_correction** (`float`): Dip correction in degrees (always positive, represents how much higher the horizon appears)

#### Example
```python
dip_corr = calculate_dip_correction(observer_height=10.0)  # 10 meters above sea level
```

### `calculate_limb_correction`

Calculate limb correction for observations of the Sun and Moon.

#### Function Signature
```python
def calculate_limb_correction(celestial_body_name: str, limb: str = "center") -> float:
```

#### Parameters
- **celestial_body_name** (`str`): Name of the celestial body ('sun' or 'moon')
- **limb** (`str`, optional): Which part of the body to observe ('center', 'upper', 'lower') (default 'center')

#### Returns
- **limb_correction** (`float`): Limb correction in degrees

#### Example
```python
# For lower limb of the sun
sun_lower_limb_corr = calculate_limb_correction('sun', 'lower')

# For upper limb of the moon
moon_upper_limb_corr = calculate_limb_correction('moon', 'upper')
```

### `get_total_observation_correction`

Calculate all corrections for a celestial observation.

#### Function Signature
```python
def get_total_observation_correction(
    observed_altitude: float,
    temperature: float = 10.0,
    pressure: float = 1010.0,
    observer_height: float = 0.0,
    celestial_body_name: str = None,
    limb: str = 'center'
) -> dict:
```

#### Parameters
- **observed_altitude** (`float`): Raw observed altitude in degrees
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)
- **observer_height** (`float`, optional): Height of observer above sea level in meters (default 0)
- **celestial_body_name** (`str`, optional): Name of celestial body for limb correction
- **limb** (`str`, optional): Which part of the body to observe ('center', 'upper', 'lower') (default 'center')

#### Returns
- **corrections** (`dict`): Dictionary with all corrections and final altitude
  - `observed_altitude`: Original observed altitude
  - `refraction_correction`: Amount to subtract for refraction
  - `dip_correction`: Amount to add for dip of horizon
  - `limb_correction`: Amount to add for limb correction
  - `total_correction`: Total correction applied
  - `corrected_altitude`: Final corrected altitude

#### Example
```python
corrections = get_total_observation_correction(
    observed_altitude=45.0,
    temperature=15.0,
    pressure=1020.0,
    observer_height=10.0,
    celestial_body_name='sun',
    limb='lower'
)
print(f"Corrected altitude: {corrections['corrected_altitude']:.2f}°")
```

### `get_celestial_body`

Get the appropriate celestial body based on name.

#### Function Signature
```python
def get_celestial_body(name: str, observation_time) -> astropy.coordinates.SkyCoord:
```

#### Parameters
- **name** (`str`): Name of the celestial body ('sun', 'moon', or 'star')
- **observation_time** (`astropy.time.Time`): Astropy Time object for the observation time

#### Returns
- **celestial_body** (`astropy.coordinates.SkyCoord`): Astropy SkyCoord object for the celestial body

#### Example
```python
from astropy.time import Time
time = Time("2023-06-15T12:00:00")
sun = get_celestial_body("sun", time)
```

### `format_position`

Format latitude and longitude in degrees, minutes, and seconds.

#### Function Signature
```python
def format_position(lat: float, lon: float) -> str:
```

#### Parameters
- **lat** (`float`): Latitude in degrees
- **lon** (`float`): Longitude in degrees

#### Returns
- **formatted_position** (`str`): Formatted position string

#### Example
```python
position = format_position(40.7128, -74.0060)
print(position)  # Output: "40°42'46.08"N, 74°00'21.60"W"
```

## Validation Functions

### `validate_altitude`
Validate that altitude is within reasonable range (-1° to 90°).

### `validate_temperature`
Validate temperature is within reasonable range (-100°C to +100°C).

### `validate_pressure`
Validate pressure is within reasonable range (800 to 1200 hPa).

### `validate_observer_height`
Validate observer height is non-negative.

### `validate_celestial_body_name`
Validate celestial body name is supported ('sun' or 'moon').

### `validate_limb`
Validate limb value is supported ('center', 'upper', or 'lower').

## Constants

The module uses the following constants for calculations:
- Angular radius of Sun/Moon: Approximately 16 minutes of arc (16/60 degrees)

## Errors and Exceptions

The module raises the following exceptions:

- `ValueError`: Raised when input parameters are outside valid ranges
  - Invalid altitude: less than -1° or greater than 90°
  - Invalid temperature: less than -100°C or greater than 100°C
  - Invalid pressure: less than 800 hPa or greater than 1200 hPa
  - Invalid observer height: negative values
  - Invalid celestial body name: not 'sun' or 'moon'
  - Invalid limb value: not 'center', 'upper', or 'lower'