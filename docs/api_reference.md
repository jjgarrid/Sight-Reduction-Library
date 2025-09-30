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
    validate_limb,
    calculate_bubble_sextant_correction,
    calculate_movement_correction,
    apply_time_interval_correction
)

from src.aviation_almanac import (
    AviationAlmanacInterface,
    get_aviation_celestial_body_data,
    get_aviation_table_lookup
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
    limb='center',
    navigation_mode='marine',
    aircraft_speed_knots=0.0,
    aircraft_course=0.0,
    time_interval_hours=0.0
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
- **navigation_mode** (`str`, optional): Navigation mode ('marine' or 'aviation') to determine correction methods (default 'marine')
- **aircraft_speed_knots** (`float`, optional): Aircraft speed in knots (for aviation mode) (default 0.0)
- **aircraft_course** (`float`, optional): Aircraft heading in degrees (for aviation mode) (default 0.0)
- **time_interval_hours** (`float`, optional): Time interval from reference observation in hours (for aviation mode) (default 0.0)

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
    pressure: float = 1010.0,
    altitude_meters: float = 0.0
) -> float:
```

#### Parameters
- **observed_altitude** (`float`): The observed altitude of the celestial body in degrees
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)
- **altitude_meters** (`float`, optional): Observer altitude above sea level in meters, for aviation corrections (default 0.0)

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

### `calculate_bubble_sextant_correction`

Calculate corrections specific to bubble sextant observations in aviation.

#### Function Signature
```python
def calculate_bubble_sextant_correction(
    aircraft_altitude: float = 0.0, 
    temperature: float = 10.0, 
    pressure: float = 1013.25
) -> float:
```

#### Parameters
- **aircraft_altitude** (`float`, optional): Aircraft altitude above sea level in meters (default 0.0)
- **temperature** (`float`, optional): Atmospheric temperature at aircraft altitude in degrees Celsius (default 10.0)
- **pressure** (`float`, optional): Atmospheric pressure at aircraft altitude in hPa (default 1013.25)

#### Returns
- **correction** (`float`): Correction in degrees for bubble sextant observations

#### Example
```python
correction = calculate_bubble_sextant_correction(
    aircraft_altitude=3000.0,
    temperature=-20.0,
    pressure=700.0
)
```

### `calculate_movement_correction`

Calculate position correction for observer movement during flight.

#### Function Signature
```python
def calculate_movement_correction(
    assumed_position,
    observation_time,
    aircraft_speed_knots: float = 0.0,
    aircraft_course: float = 0.0,
    time_interval_hours: float = 0.0
) -> astropy.coordinates.EarthLocation:
```

#### Parameters
- **assumed_position** (`astropy.coordinates.EarthLocation`): Original assumed position
- **observation_time** (`astropy.time.Time`): Time of the original observation
- **aircraft_speed_knots** (`float`, optional): Aircraft speed in knots (nautical miles per hour) (default 0.0)
- **aircraft_course** (`float`, optional): Aircraft course in degrees (0° = North, 90° = East, etc.) (default 0.0)
- **time_interval_hours** (`float`, optional): Time interval from original observation in hours (default 0.0)

#### Returns
- **corrected_position** (`astropy.coordinates.EarthLocation`): Corrected EarthLocation accounting for movement

#### Example
```python
from astropy.coordinates import EarthLocation
import astropy.units as u
from astropy.time import Time

original_pos = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
obs_time = Time("2023-06-15T12:00:00")

corrected_pos = calculate_movement_correction(
    assumed_position=original_pos,
    observation_time=obs_time,
    aircraft_speed_knots=250.0,
    aircraft_course=90.0,
    time_interval_hours=1.0
)
```

### `apply_time_interval_correction`

Apply time interval correction for changes in celestial body position.

#### Function Signature
```python
def apply_time_interval_correction(
    observed_altitude: float,
    time_interval_hours: float,
    celestial_body,
    assumed_position,
    observation_time
) -> float:
```

#### Parameters
- **observed_altitude** (`float`): Original observed altitude
- **time_interval_hours** (`float`): Time interval from original observation in hours
- **celestial_body** (`astropy.coordinates.SkyCoord`): Astropy SkyCoord of the celestial body
- **assumed_position** (`astropy.coordinates.EarthLocation`): Assumed position for observation
- **observation_time** (`astropy.time.Time`): Original observation time

#### Returns
- **corrected_altitude** (`float`): Corrected altitude accounting for body movement during time interval

#### Example
```python
corrected_alt = apply_time_interval_correction(
    observed_altitude=45.0,
    time_interval_hours=0.5,
    celestial_body=celestial_body,
    assumed_position=assumed_position,
    observation_time=obs_time
)
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
    limb: str = 'center',
    navigation_mode: str = 'marine'
) -> dict:
```

#### Parameters
- **observed_altitude** (`float`): Raw observed altitude in degrees
- **temperature** (`float`, optional): Atmospheric temperature in degrees Celsius (default 10°C)
- **pressure** (`float`, optional): Atmospheric pressure in hPa (default 1010 hPa)
- **observer_height** (`float`, optional): Height of observer above sea level in meters (default 0)
- **celestial_body_name** (`str`, optional): Name of celestial body for limb correction
- **limb** (`str`, optional): Which part of the body to observe ('center', 'upper', 'lower') (default 'center')
- **navigation_mode** (`str`, optional): Navigation mode ('marine' or 'aviation') to determine correction methods (default 'marine')

#### Returns
- **corrections** (`dict`): Dictionary with all corrections and final altitude
  - `observed_altitude`: Original observed altitude
  - `refraction_correction`: Amount to subtract for refraction
  - `dip_correction`: Amount to add for dip of horizon
  - `limb_correction`: Amount to add for limb correction
  - `total_correction`: Total correction applied
  - `corrected_altitude`: Final corrected altitude
  - `navigation_mode`: The navigation mode used

#### Example
```python
corrections = get_total_observation_correction(
    observed_altitude=45.0,
    temperature=15.0,
    pressure=1020.0,
    observer_height=10.0,
    celestial_body_name='sun',
    limb='lower',
    navigation_mode='aviation'
)
print(f"Corrected altitude: {corrections['corrected_altitude']:.2f}°")
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

## Aviation Almanac Functions

### `AviationAlmanacInterface`

Interface class to access aviation-specific almanac data and tables.

#### Example
```python
from src.aviation_almanac import AviationAlmanacInterface
aviation_almanac = AviationAlmanacInterface()

# Get aviation-specific star data
star_data = aviation_almanac.get_aviation_star_data(
    date_time=observation_time,
    star_name='sirius'
)
```

### `get_aviation_celestial_body_data`

Get aviation almanac data for a specific celestial body at a specific date/time.

#### Function Signature
```python
def get_aviation_celestial_body_data(body_name: str, date_time) -> dict:
```

#### Parameters
- **body_name** (`str`): Name of the celestial body
- **date_time**: The date and time for which to get data

#### Returns
- **data** (`dict`): Dictionary with aviation almanac data for the celestial body

#### Example
```python
from astropy.time import Time

obs_time = Time("2023-06-15T12:00:00")
star_data = get_aviation_celestial_body_data('sirius', obs_time)
print(f"GHA: {star_data['GHA']}")
print(f"Declination: {star_data['declination']}")
```

### `get_aviation_table_lookup`

Look up altitude and azimuth from aviation tables (simulated Pub. No. 249 functionality).

#### Function Signature
```python
def get_aviation_table_lookup(
    assumed_lat: float,
    lha: float, 
    declination: float,
    table_volume: int = 1
) -> dict:
```

#### Parameters
- **assumed_lat** (`float`): Assumed latitude (0° to 90°, positive for North)
- **lha** (`float`): Local Hour Angle (0° to 359°)
- **declination** (`float`): Declination of the celestial body (-90° to +90°)
- **table_volume** (`int`): Which volume of Pub. No. 249 (1, 2, or 3) (default 1)

#### Returns
- **lookup_result** (`dict`): Dictionary with computed altitude, azimuth and corrections
  - `computed_altitude`: Calculated altitude
  - `azimuth`: Calculated azimuth
  - `delta_correction`: Delta correction value
  - `table_volume`: The volume used
  - `intercept_correction`: Correction for plotting the line of position

#### Example
```python
lookup_result = get_aviation_table_lookup(
    assumed_lat=40.0,
    lha=45.0,
    declination=20.0,
    table_volume=1
)
altitude = lookup_result['computed_altitude']
azimuth = lookup_result['azimuth']
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