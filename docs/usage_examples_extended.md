# Examples for Sight Reduction Problem Generation

This document shows examples of how to use the new problem generation functionality in the sight reduction library.

## Basic Example: Generate a Single Sight Reduction Problem

```python
from src.problem_generator import generate_sight_reduction_problem

# Generate a random sight reduction problem
problem = generate_sight_reduction_problem()
print(f"Celestial Body: {problem['celestial_body_name']}")
print(f"Observed Altitude: {problem['observed_altitude']:.2f}°")
print(f"Observation Time: {problem['observation_time']}")

# Format the problem for user display
from src.problem_generator import format_problem_for_user
formatted_problem = format_problem_for_user(problem)
print(formatted_problem)
```

## Example: Generate Specific Types of Sights

```python
from src.problem_generator import (
    generate_morning_sight_problem,
    generate_evening_sight_problem,
    generate_twilight_star_sight_problem,
    generate_moon_sight_problem
)

# Generate a morning Sun sight
morning_problem = generate_morning_sight_problem()
print(f"Morning sight: {morning_problem['celestial_body_name']} at {morning_problem['observation_time']}")

# Generate an evening Sun sight
evening_problem = generate_evening_sight_problem()
print(f"Evening sight: {evening_problem['celestial_body_name']} at {evening_problem['observation_time']}")

# Generate a star sight for a specific star
star_problem = generate_twilight_star_sight_problem(star_name="sirius")
print(f"Star sight: {star_problem['celestial_body_name']} at {star_problem['observation_time']}")

# Generate a Moon sight
moon_problem = generate_moon_sight_problem()
print(f"Moon sight: {moon_problem['celestial_body_name']} at {moon_problem['observation_time']}")
```

## Example: Generate Multiple Sights for Position Fix

```python
from src.problem_generator import generate_multi_body_sight_reduction_problems

# Generate 3 sight problems for a position fix
multi_problems = generate_multi_body_sight_reduction_problems(num_bodies=3, time_window_hours=2.0)

print(f"Generated {len(multi_problems)} sight problems:")
for i, problem in enumerate(multi_problems):
    print(f"  {i+1}. {problem['celestial_body_name']} at {problem['observation_time'].datetime.time()}")
    print(f"     Observed Altitude: {problem['observed_altitude']:.2f}°")
    print(f"     Assumed Position: {problem['assumed_position'].lat:.4f}, {problem['assumed_position'].lon:.4f}")
```

## Example: Using Almanac Integration

```python
from datetime import datetime
from src.almanac_integration import get_celestial_body_almanac_data, get_hourly_almanac_data

# Get almanac data for the Sun at a specific time
sun_data = get_celestial_body_almanac_data('sun', datetime(2023, 6, 15, 12, 0, 0))
print(f"Sun GHA: {sun_data['GHA']:.4f}°, Declination: {sun_data['declination']:.4f}°")

# Get hourly almanac data for the Moon for a full day
hourly_moon_data = get_hourly_almanac_data('moon', datetime(2023, 6, 15), hours=24)
print("First few hours of Moon data:")
print(hourly_moon_data.head())
```

## Example: Complete Workflow - Generate and Solve a Problem

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.problem_generator import generate_sight_reduction_problem, validate_problem_solution
from src.sight_reduction import calculate_intercept, get_celestial_body

# Generate a problem
problem = generate_sight_reduction_problem(celestial_body_name="sun")

# Extract problem parameters
observed_altitude = problem['observed_altitude']
celestial_body_name = problem['celestial_body_name']
assumed_position = problem['assumed_position']
observation_time = problem['observation_time']
temperature = problem['temperature']
pressure = problem['pressure']
observer_height = problem['observer_height']
limb = problem['limb']

# In a real scenario, the navigator would need to solve this
# Here, we'll use the sight reduction function to solve it
celestial_body = get_celestial_body(celestial_body_name, observation_time)
intercept, azimuth = calculate_intercept(
    observed_altitude,
    celestial_body,
    assumed_position,
    observation_time,
    temperature=temperature,
    pressure=pressure,
    observer_height=observer_height,
    celestial_body_name=celestial_body_name,
    limb=limb
)

print(f"Solved: Intercept: {intercept:.2f} nm, Azimuth: {azimuth:.2f}°")

# Validate the solution against the known actual position
validation = validate_problem_solution(
    observed_altitude=observed_altitude,
    celestial_body_name=celestial_body_name,
    assumed_position=assumed_position,
    observation_time=observation_time,
    intercept=intercept,
    azimuth=azimuth,
    temperature=temperature,
    pressure=pressure,
    observer_height=observer_height,
    limb=limb
)

print(f"Validation error - Intercept: {validation['user_intercept_error']:.2f} nm")
print(f"Validation error - Azimuth: {validation['user_azimuth_error']:.2f}°")
```

## Example: Using Enhanced Parameters

The new functionality includes additional parameters for more realistic navigation scenarios:

- `instrument_error`: Error specific to the sextant being used (degrees)
- `index_error`: Error in sextant's index mirror alignment (degrees)  
- `personal_error`: Individual observer's consistent error (degrees)
- `humidity`: Atmospheric humidity percentage
- `wave_height`: Height of waves affecting horizon observation (meters)
- `sextant_precision`: Precision of the specific sextant (degrees)
- `observation_quality`: Subjective rating of observation quality

These parameters are automatically included in generated problems and affect the realism of the observations.