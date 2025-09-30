# Sight Reduction for Celestial Navigation

This project provides tools for performing sight reductions in celestial navigation, allowing navigators to determine their position based on observations of celestial bodies such as the Sun, Moon, and stars.

## Overview

Celestial navigation is a method of determining one's position on Earth by observing celestial bodies (Sun, Moon, planets, and stars) and measuring their altitude above the horizon using a sextant. A sight reduction is the mathematical process used to convert these sextant observations into lines of position on a chart.

This project uses the [Astropy](https://www.astropy.org/) library to accurately calculate celestial positions and perform sight reductions. The implementation includes important atmospheric corrections:

- **Atmospheric Refraction**: Accounts for the bending of light as it passes through Earth's atmosphere, making celestial bodies appear higher than they actually are
- **Temperature and Pressure Corrections**: Adjusts refraction calculations based on local atmospheric conditions
- **Dip of Horizon**: Corrects for observers at elevated positions (like on ships) where the horizon appears lower
- **Limb Corrections**: Adjusts for observations of the upper or lower limb of the Sun or Moon rather than the center

These corrections are critical for achieving accurate navigation fixes, especially when observing celestial bodies near the horizon.

## Features

- Calculate intercept and azimuth for celestial observations
- Support for Sun, Moon, and stars
- Atmospheric refraction corrections with temperature and pressure adjustments
- Dip of horizon correction for elevated observers
- Limb correction for solar and lunar observations (upper, lower, or center)
- Position formatting in degrees, minutes, and seconds
- Accurate celestial body positioning using Astropy
- Comprehensive input validation and error handling
- Utility functions for calculating total observation corrections
- **Advanced Position Fix Calculation using least squares methods**
- **Running fixes accounting for vessel movement between observations**
- **Statistical error analysis with error ellipse calculation**
- **Integration with problem generation for educational purposes**
- **Almanac data integration for precise celestial body positions**
- **LaTeX output generation for professional worksheets and almanac pages**
- **PDF generation directly from LaTeX templates**
- **Comprehensive documentation with step-by-step tutorials**
- **SPICE ephemeris support for highest accuracy celestial positions**

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Run the main script to perform a sight reduction:

```bash
python src/main.py
```

### As a Module

You can import and use the sight reduction functions in your own code:

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body
from src.position_fix import calculate_least_squares_fix

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

# For advanced position fixing with multiple sights:
# sights = [...]  # List of multiple sight observations
# fix_result = calculate_least_squares_fix(sights)
# print(f"Position Fix: {fix_result['fix_position']}")
```

### Usage with Atmospheric Corrections

The main `calculate_intercept` function now includes comprehensive atmospheric corrections:

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

## Project Structure

```
Sight_Reduction/
├── src/                 # Source code
│   ├── __init__.py      # Package initialization
│   ├── sight_reduction.py # Main sight reduction functions
│   ├── position_fix.py  # Advanced position fixing algorithms
│   ├── latex_output.py  # LaTeX generation functionality
│   ├── latex_templates.py # LaTeX templates
│   └── main.py          # Example usage script
├── tests/              # Unit tests
├── docs/               # Documentation
├── de421.bsp           # SPICE binary planetary ephemeris for precise celestial positions
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
└── README.md          # This file
```

## SPICE Ephemeris Support

The project includes the `de421.bsp` file, which is a SPICE (Spacecraft Planet Instrument C-matrix Events) binary planetary ephemeris. This high-precision ephemeris file provides accurate positions of celestial bodies (Sun, Moon, planets) used in sight reduction calculations. The DE421 covers the time period from 1799 to 2201 CE and significantly improves the accuracy of celestial navigation calculations by providing reference positions with centimeter-level precision for the Moon and meter-level precision for planets.

## API Reference

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

### `calculate_refraction_correction(observed_altitude, temperature=10.0, pressure=1010.0)`

Calculate atmospheric refraction correction for celestial observations.

**Parameters:**
- `observed_altitude`: The observed altitude of the celestial body in degrees
- `temperature`: Atmospheric temperature in degrees Celsius
- `pressure`: Atmospheric pressure in hPa

**Returns:**
- Refraction correction in degrees to be subtracted from observed altitude

### `calculate_dip_correction(observer_height)`

Calculate the dip of the horizon correction for an elevated observer.

**Parameters:**
- `observer_height`: Height of observer above sea level in meters

**Returns:**
- Dip correction in degrees

### `calculate_limb_correction(celestial_body_name, limb='center')`

Calculate limb correction for observations of the Sun and Moon.

**Parameters:**
- `celestial_body_name`: Name of the celestial body ('sun' or 'moon')
- `limb`: Which part of the body to observe ('center', 'upper', or 'lower')

**Returns:**
- Limb correction in degrees

### `get_total_observation_correction(observed_altitude, temperature=10.0, pressure=1010.0, observer_height=0.0, celestial_body_name=None, limb='center')`

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

## Documentation

For comprehensive guides and detailed information about the project, see the documentation:

- [Complete Sight Reduction Tutorial](docs/complete_sight_reduction_tutorial.md) - Comprehensive guide covering how to take observations, use the software, and interpret results
- [Installation Guide](docs/installation_guide.md) - How to install and set up the project
- [Sight Reduction Documentation](docs/sight_reduction_documentation.md) - Technical details about the sight reduction functions
- [API Reference](docs/api_reference.md) - Complete API documentation
- [Atmospheric Corrections](docs/atmospheric_corrections.md) - Details about atmospheric corrections applied in calculations
- [Usage Examples](docs/usage_examples.md) - Practical examples of using the software
- [Advanced Position Fix Calculation](docs/position_fix_documentation.md) - Documentation for advanced position fixing algorithms
- [Extended Usage Examples](docs/usage_examples_extended.md) - Examples of new features including problem generation and almanac integration
- [LaTeX Documentation Tutorial](docs/latex_tutorial.md) - Step-by-step tutorial for using the LaTeX output features

## Accuracy

The calculations are based on high-precision astrometric data from the Astropy library, which implements the International Astronomical Union (IAU) standards for celestial mechanics. This provides accuracy suitable for navigation.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## References

- [The Nautical Almanac](https://www.nauticalalmanac.com/)
- [Astropy Documentation](https://docs.astropy.org/en/stable/)
- [Celestial Navigation Resources](https://en.wikipedia.org/wiki/Celestial_navigation)