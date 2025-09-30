# Sight Reduction for Celestial Navigation - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [API Reference](#api-reference)
4. [Usage Examples](#usage-examples)
5. [Atmospheric Corrections](#atmospheric-corrections)
6. [Testing](#testing)
7. [References](#references)

## Project Overview

This project provides tools for performing sight reductions in celestial navigation, allowing navigators to determine their position based on observations of celestial bodies such as the Sun, Moon, and stars.

Celestial navigation is a method of determining one's position on Earth by observing celestial bodies (Sun, Moon, planets, and stars) and measuring their altitude above the horizon using a sextant. A sight reduction is the mathematical process used to convert these sextant observations into lines of position on a nautical chart.

The project uses the [Astropy](https://www.astropy.org/) library to accurately calculate celestial positions and perform sight reductions. The implementation includes important atmospheric corrections that are critical for achieving accurate navigation fixes, especially when observing celestial bodies near the horizon.

### Key Features
- Calculate intercept and azimuth for celestial observations
- Support for Sun, Moon, and stars
- Atmospheric refraction corrections with temperature and pressure adjustments
- Dip of horizon correction for elevated observers
- Limb correction for solar and lunar observations (upper, lower, or center)
- Position formatting in degrees, minutes, and seconds
- Accurate celestial body positioning using Astropy
- Comprehensive input validation and error handling
- Utility functions for calculating total observation corrections

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies
The project requires the following Python packages:
- astropy>=5.0
- numpy>=1.21.0
- matplotlib>=3.3.0
- pandas>=1.3.0

## API Reference

### Main Functions

#### `calculate_intercept(observed_altitude, celestial_body, assumed_position, observation_time, apply_refraction=True, temperature=10.0, pressure=1010.0, observer_height=0.0, celestial_body_name=None, limb='center')`

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

#### `calculate_refraction_correction(observed_altitude, temperature=10.0, pressure=1010.0)`

Calculate atmospheric refraction correction for celestial observations.

**Parameters:**
- `observed_altitude`: The observed altitude of the celestial body in degrees
- `temperature`: Atmospheric temperature in degrees Celsius
- `pressure`: Atmospheric pressure in hPa

**Returns:**
- Refraction correction in degrees to be subtracted from observed altitude

#### `calculate_dip_correction(observer_height)`

Calculate the dip of the horizon correction for an elevated observer.

**Parameters:**
- `observer_height`: Height of observer above sea level in meters

**Returns:**
- Dip correction in degrees

#### `calculate_limb_correction(celestial_body_name, limb='center')`

Calculate limb correction for observations of the Sun and Moon.

**Parameters:**
- `celestial_body_name`: Name of the celestial body ('sun' or 'moon')
- `limb`: Which part of the body to observe ('center', 'upper', or 'lower')

**Returns:**
- Limb correction in degrees

#### `get_total_observation_correction(observed_altitude, temperature=10.0, pressure=1010.0, observer_height=0.0, celestial_body_name=None, limb='center')`

Calculate all corrections for a celestial observation.

**Parameters:**
- `observed_altitude`: Raw observed altitude in degrees
- `temperature`: Atmospheric temperature in degrees Celsius
- `pressure`: Atmospheric pressure in hPa
- `observer_height`: Height of observer above sea level in meters
- `celestial_body_name`: Name of celestial body for limb correction
- `limb`: Which part of the body to observe ('center', 'upper', 'lower')

**Returns:**
- Dictionary with all corrections and final altitude

#### `get_celestial_body(name, observation_time)`

Get the appropriate celestial body based on name.

**Parameters:**
- `name`: Name of the celestial body ('sun', 'moon', or 'star')
- `observation_time`: Astropy Time object for the observation time

**Returns:**
- Astropy SkyCoord object for the celestial body

#### `format_position(lat, lon)`

Format latitude and longitude in degrees, minutes, and seconds.

**Parameters:**
- `lat`: Latitude in degrees
- `lon`: Longitude in degrees

**Returns:**
- Formatted position string

## New Features: Sight Reduction Problem Generation

The sight reduction library now includes functionality for generating realistic sight reduction problems. This is particularly useful for educational purposes, practice, and testing navigation skills.

### Problem Generator Module

#### `generate_sight_reduction_problem(actual_position=None, observation_time=None, celestial_body_name=None, add_random_error=True, error_range=0.1, max_retries=10)`

Generate a realistic sight reduction problem with all necessary parameters.

**Parameters:**
- `actual_position`: The actual vessel position (will be generated if None)
- `observation_time`: Time of observation (will be generated if None)
- `celestial_body_name`: Name of the celestial body (will be selected if None)
- `add_random_error`: Whether to add random error to make the problem more realistic
- `error_range`: Range of random error to add (in degrees)
- `max_retries`: Maximum number of retries when celestial body is not visible

**Returns:**
- Dictionary containing all parameters needed for a sight reduction problem

#### `generate_morning_sight_problem()`

Generate a morning sight problem (typically Sun lower limb sight).

**Returns:**
- Dictionary containing parameters for a morning sight problem

#### `generate_evening_sight_problem()`

Generate an evening sight problem (typically Sun upper limb sight).

**Returns:**
- Dictionary containing parameters for an evening sight problem

#### `generate_twilight_star_sight_problem(star_name=None)`

Generate a twilight star sight problem.

**Parameters:**
- `star_name`: Name of the star to observe (will be selected randomly if None)

**Returns:**
- Dictionary containing parameters for a star sight problem

#### `generate_moon_sight_problem()`

Generate a Moon sight problem.

**Returns:**
- Dictionary containing parameters for a Moon sight problem

#### `generate_multi_body_sight_reduction_problems(num_bodies=3, time_window_hours=2.0)`

Generate multiple sight reduction problems for a position fix.

**Parameters:**
- `num_bodies`: Number of celestial bodies to observe (default 3)
- `time_window_hours`: Time window in which all observations are made (default 2 hours)

**Returns:**
- List of dictionaries, each containing parameters for a sight reduction problem

#### `format_problem_for_user(problem_params)`

Format the sight reduction problem in a user-friendly way.

**Parameters:**
- `problem_params`: Dictionary containing the problem parameters

**Returns:**
- Formatted string describing the sight reduction problem

#### `validate_problem_solution(observed_altitude, celestial_body_name, assumed_position, observation_time, intercept, azimuth, temperature=10.0, pressure=1010.0, observer_height=0.0, limb='center')`

Validate a solution to a sight reduction problem by comparing with the known actual position.

**Parameters:**
- `observed_altitude`: The altitude measured with the sextant
- `celestial_body_name`: Name of the celestial body observed
- `assumed_position`: The assumed position used for calculation
- `observation_time`: Time of the observation
- `intercept`: Calculated intercept from user's solution
- `azimuth`: Calculated azimuth from user's solution
- `temperature`: Atmospheric temperature (default 10°C)
- `pressure`: Atmospheric pressure (default 1010 hPa)
- `observer_height`: Height above sea level (default 0m)
- `limb`: Which limb was observed ('upper', 'lower', 'center') - for Sun and Moon

**Returns:**
- Dictionary with validation results

## Enhanced Parameters

The sight reduction functionality now includes additional parameters for more realistic navigation scenarios:

- `instrument_error`: Error specific to the sextant being used (degrees)
- `index_error`: Error in sextant's index mirror alignment (degrees)
- `personal_error`: Individual observer's consistent error (degrees)
- `humidity`: Atmospheric humidity percentage
- `wave_height`: Height of waves affecting horizon observation (meters)
- `sextant_precision`: Precision of the specific sextant (degrees)
- `observation_quality`: Subjective rating of observation quality

## Almanac Integration

The library now includes integration with nautical almanac data:

#### `get_celestial_body_almanac_data(body_name, date_time)`

Get almanac data for a specific celestial body at a specific date/time.

**Parameters:**
- `body_name`: Name of the celestial body
- `date_time`: The date and time for which to get data

**Returns:**
- Dictionary with almanac data for the celestial body

#### `get_hourly_almanac_data(body_name, date, hours=24)`

Get hourly almanac data for a celestial body for a full day.

**Parameters:**
- `body_name`: Name of the celestial body
- `date`: The date for which to get hourly data
- `hours`: Number of hours of data to generate (default 24)

**Returns:**
- Pandas DataFrame with hourly GHA and declination data

## Advanced Position Fix Calculation

The library now includes advanced position fixing algorithms:

### Position Fix Module

#### `calculate_least_squares_fix(sights)`

Calculate position fix using least squares method from multiple sight observations.

**Parameters:**
- `sights`: List of sight observations, each with keys:
  - `observed_altitude`: Measured altitude of celestial body
  - `celestial_body_name`: Name of observed celestial body
  - `observation_time`: Time of observation (UTC)
  - `intercept`: Calculated intercept in nautical miles
  - `azimuth`: Calculated azimuth in degrees
  - `assumed_position`: Assumed position for calculation
  - `altitude_correction_error`: Estimated error in altitude measurement

**Returns:**
- Dictionary containing the calculated position fix and associated data

#### `calculate_running_fix(sights, vessel_speed, vessel_course)`

Calculate a running fix by accounting for vessel movement between observations.

**Parameters:**
- `sights`: List of sight observations
- `vessel_speed`: Speed of the vessel in knots
- `vessel_course`: Course of the vessel in degrees True

**Returns:**
- Dictionary containing the calculated running fix

#### `calculate_error_ellipse(sights)`

Calculate error ellipse parameters from the observed sights.

**Parameters:**
- `sights`: List of sight observations

**Returns:**
- Dictionary containing error ellipse parameters

#### `calculate_geometric_factor(azimuths)`

Calculate geometric factor indicating the quality of sight combination.

**Parameters:**
- `azimuths`: Array of azimuths in degrees

**Returns:**
- Geometric factor (higher is better)## Usage Examples

### Basic Sight Reduction

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data
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
intercept, azimuth = calculate_intercept(observed_altitude, celestial_body, assumed_position, observation_time)

print(f"Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
```

### Usage with Atmospheric Corrections

The main `calculate_intercept` function includes comprehensive atmospheric corrections:

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

print(f"Intercept with atmospheric corrections: {abs(intercept):.2f} nm")
print(f"Azimuth: {azimuth:.2f}°")
```

### Calculate Total Observation Corrections

You can also calculate all corrections separately using the utility function:

```python
from src.sight_reduction import get_total_observation_correction

# Calculate all corrections for an observation
corrections = get_total_observation_correction(
    observed_altitude=45.0,
    temperature=15.0,
    pressure=1020.0,
    observer_height=10.0,  # 10 meters above sea level
    celestial_body_name='sun',
    limb='lower'
)

print(f"Observed altitude: {corrections['observed_altitude']:.2f}°")
print(f"Refraction correction: {corrections['refraction_correction']:.4f}°")
print(f"Dip correction: {corrections['dip_correction']:.4f}°")
print(f"Limb correction: {corrections['limb_correction']:.4f}°")
print(f"Corrected altitude: {corrections['corrected_altitude']:.2f}°")
```

## Atmospheric Corrections

### Atmospheric Refraction
When light from celestial bodies passes through Earth's atmosphere, it bends due to the different densities of the air layers. This makes celestial bodies appear higher above the horizon than they actually are. The refraction correction accounts for this effect, which is most significant near the horizon and decreases as the altitude increases.

The correction depends on:
- Observed altitude of the celestial body
- Atmospheric temperature
- Atmospheric pressure

### Dip of Horizon
When an observer is at an elevated position (like on a ship or on a hill), the horizon appears lower than it would from sea level. This correction accounts for the apparent lowering of the horizon based on the observer's height above sea level.

### Limb Corrections
The Sun and Moon have appreciable angular size, so navigators sometimes observe the upper or lower limb instead of the center. For the Sun and Moon, the limb correction accounts for the angular radius of the body. The correction is approximately 16 minutes of arc (16/60 degrees).

- For upper limb observations: subtract the radius
- For lower limb observations: add the radius
- For center observations: no correction needed

## Testing

The project includes tests for the core functionality in the `tests/` directory:

- `test_sight_reduction.py`: Tests for the main sight reduction functions
- `test_atmospheric_corrections.py`: Tests for atmospheric correction functions

To run the tests:
```bash
pytest tests/
```

## How Sight Reduction Works

1. An observer takes a sextant sight of a celestial body (e.g., the Sun) and records:
   - The observed altitude above the horizon
   - The time of the observation
   - An assumed position (close to the actual position)

2. Using the assumed position and observation time, the program calculates:
   - Where the celestial body should be in the sky (calculated altitude and azimuth)
   - The difference between observed and calculated altitudes (intercept)
   - The azimuth (bearing) to the celestial body

3. The intercept and azimuth are used to plot a line of position on a nautical chart

## Accuracy

The calculations are based on high-precision astrometric data from the Astropy library, which implements the International Astronomical Union (IAU) standards for celestial mechanics. This provides accuracy suitable for navigation.

## Command-Line Usage

Run the main script to perform a sight reduction with default parameters:

```bash
python src/main.py
```

This will use default values from the config.py file unless those are not available, in which case it will use built-in defaults.

## Configuration

The config.py file allows you to set default values for calculations:

```python
# Configuration for Sight Reduction project

# Default observation parameters
DEFAULT_OBSERVED_ALTITUDE = 45.0  # degrees
DEFAULT_CELESTIAL_BODY = "sun"
DEFAULT_ASSUMED_LAT = 40.7128     # degrees
DEFAULT_ASSUMED_LON = -74.0060    # degrees

# Calculation settings
NAUTICAL_MILES_PER_DEGREE = 60.0

# Output formatting
FORMAT_PRECISION = 2
```

## References

- [The Nautical Almanac](https://www.nauticalalmanac.com/)
- [Astropy Documentation](https://docs.astropy.org/en/stable/)
- [Celestial Navigation Resources](https://en.wikipedia.org/wiki/Celestial_navigation)
- [USNO Astronomical Applications](https://aa.usno.navy.mil/)