# Advanced Position Fix Calculation

## Overview
The Advanced Position Fix Calculation module provides sophisticated methods for determining position fixes from multiple celestial observations. The module implements least squares methods, running fixes, and statistical error analysis to provide accurate and reliable position fixes.

## Key Features

### 1. Least Squares Position Fix
- Uses mathematical optimization to find the most probable position from multiple observations
- Minimizes the sum of squared errors between observed and calculated altitudes
- Provides error analysis and quality assessment

### 2. Running Fixes
- Accounts for vessel movement between observations
- Adjusts Lines of Position (LOPs) based on course and speed
- Provides accurate fixes even with time-separated observations

### 3. Error Analysis
- Calculates error ellipses showing statistical uncertainty
- Provides geometric strength analysis of sight combinations
- Assesses fix quality based on measurement accuracy and geometry

## Functions

### `calculate_least_squares_fix(sights)`
Calculates the most probable position from multiple sight observations using least squares optimization.

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
- Dictionary with:
  - `fix_position`: Calculated EarthLocation for the position fix
  - `fix_accuracy_nm`: Approximate accuracy in nautical miles
  - `error_ellipse`: Error ellipse parameters
  - `fix_quality`: Quality assessment ("Excellent", "Good", "Fair", "Poor")
  - `geometric_factor`: Geometric strength of sight combination
  - `residual_errors`: Errors for each sight after fix calculation
  - `number_of_sights`: Count of sights used
  - `solution_converged`: Boolean indicating if least squares converged

### `calculate_running_fix(sights, vessel_speed, vessel_course)`
Calculates a position fix accounting for vessel movement between observations.

**Parameters:**
- `sights`: List of sight observations (same format as least squares)
- `vessel_speed`: Speed of vessel in knots
- `vessel_course`: Course of vessel in degrees True

**Returns:**
- Same format as `calculate_least_squares_fix`

### `calculate_error_ellipse(sights)`
Calculates the error ellipse showing uncertainty in position fix.

**Parameters:**
- `sights`: List of sight observations

**Returns:**
- Dictionary with:
  - `semi_major_axis_nm`: Semi-major axis in nautical miles
  - `semi_minor_axis_nm`: Semi-minor axis in nautical miles
  - `orientation_deg`: Orientation of major axis in degrees
  - `confidence_level`: Confidence level of ellipse (0.95 = 95%)

### `calculate_geometric_factor(azimuths)`
Calculates the geometric strength of sight combination based on azimuth distribution.

**Parameters:**
- `azimuths`: Array of azimuths in degrees

**Returns:**
- Geometric factor (higher values indicate better geometry)

## Example Usage

```python
from src.position_fix import calculate_least_squares_fix
from src.sight_reduction import calculate_intercept, get_celestial_body
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u

# Example sight observations (usually from actual measurements)
sight1 = {
    'observed_altitude': 45.0,
    'celestial_body_name': 'sun',
    'observation_time': Time('2023-06-15T12:00:00'),
    'intercept': 10.0,  # nm towards celestial body
    'azimuth': 90.0,    # East
    'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
    'altitude_correction_error': 0.1
}

sight2 = {
    'observed_altitude': 40.0,
    'celestial_body_name': 'sun',
    'observation_time': Time('2023-06-15T12:05:00'),
    'intercept': -5.0,  # nm away from celestial body
    'azimuth': 0.0,     # North
    'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
    'altitude_correction_error': 0.1
}

sights = [sight1, sight2]

# Calculate the least squares position fix
result = calculate_least_squares_fix(sights)

print(f"Position fix: {result['fix_position']}")
print(f"Accuracy: {result['fix_accuracy_nm']:.2f} nautical miles")
print(f"Quality: {result['fix_quality']}")
print(f"Geometric Factor: {result['geometric_factor']:.2f}")
```

## Mathematical Approach

The least squares method finds the position (lat, lon) that minimizes the sum of squared residuals:

`Σ (observed_intercept_i - calculated_intercept_i)²`

Where the calculated intercept for each sight depends on the difference between the current position and the assumed position along the azimuth direction.

The error ellipse is calculated using the covariance matrix derived from the Jacobian of the least squares solution, providing statistical uncertainty bounds for the fix.

## Integration with Other Modules

The position fix module works seamlessly with other parts of the navigation system:

- **Problem Generator**: Compatible with generated sight problems
- **Sight Reduction**: Uses intercepts and azimuths from sight reduction calculations
- **Almanac Integration**: Can incorporate precise celestial body positions