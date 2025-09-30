# Advanced Position Fix Calculation Example

This example demonstrates how to use the Advanced Position Fix Calculation module to determine a position fix from multiple celestial observations.

## Basic Least Squares Fix

```python
from src.position_fix import calculate_least_squares_fix
from src.sight_reduction import calculate_intercept, get_celestial_body
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u

# Create example sight observations
# In practice, these would come from actual sextant observations

# Sight 1: Sun observation
sight1 = {
    'observed_altitude': 45.23,
    'celestial_body_name': 'sun',
    'observation_time': Time('2023-06-15T12:00:00'),
    'assumed_position': EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m),
    'altitude_correction_error': 0.1
}

# Calculate intercept and azimuth for this sight
celestial_body1 = get_celestial_body(sight1['celestial_body_name'], sight1['observation_time'])
intercept1, azimuth1 = calculate_intercept(
    sight1['observed_altitude'],
    celestial_body1,
    sight1['assumed_position'],
    sight1['observation_time']
)
sight1['intercept'] = intercept1
sight1['azimuth'] = azimuth1

# Sight 2: Moon observation (different time)
sight2 = {
    'observed_altitude': 32.56,
    'celestial_body_name': 'moon',
    'observation_time': Time('2023-06-15T12:15:00'),
    'assumed_position': EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m),
    'altitude_correction_error': 0.1
}

# Calculate intercept and azimuth for this sight
celestial_body2 = get_celestial_body(sight2['celestial_body_name'], sight2['observation_time'])
intercept2, azimuth2 = calculate_intercept(
    sight2['observed_altitude'],
    celestial_body2,
    sight2['assumed_position'],
    sight2['observation_time']
)
sight2['intercept'] = intercept2
sight2['azimuth'] = azimuth2

# Sight 3: Planet observation (e.g., Venus)
sight3 = {
    'observed_altitude': 52.11,
    'celestial_body_name': 'venus',
    'observation_time': Time('2023-06-15T12:30:00'),
    'assumed_position': EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m),
    'altitude_correction_error': 0.1
}

# Calculate intercept and azimuth for this sight
celestial_body3 = get_celestial_body(sight3['celestial_body_name'], sight3['observation_time'])
intercept3, azimuth3 = calculate_intercept(
    sight3['observed_altitude'],
    celestial_body3,
    sight3['assumed_position'],
    sight3['observation_time']
)
sight3['intercept'] = intercept3
sight3['azimuth'] = azimuth3

# Combine all sights for position fix calculation
sights = [sight1, sight2, sight3]

# Calculate the least squares position fix
result = calculate_least_squares_fix(sights)

print(f"Calculated Position Fix:")
print(f"  Latitude: {result['fix_position'].lat:.6f}")
print(f"  Longitude: {result['fix_position'].lon:.6f}")
print(f"  Accuracy: {result['fix_accuracy_nm']:.2f} nautical miles")
print(f"  Fix Quality: {result['fix_quality']}")
print(f"  Geometric Factor: {result['geometric_factor']:.2f}")
print(f"  Number of Sights Used: {result['number_of_sights']}")
```

## Running Fix Example

```python
from src.position_fix import calculate_running_fix

# Example of calculating a running fix when the vessel is moving
# Vessel moving at 8 knots on course 090 (due East)

running_fix_result = calculate_running_fix(
    sights=sights,
    vessel_speed=8.0,      # knots
    vessel_course=90.0     # degrees True (due East)
)

print(f"\\nRunning Fix Result:")
print(f"  Latitude: {running_fix_result['fix_position'].lat:.6f}")
print(f"  Longitude: {running_fix_result['fix_position'].lon:.6f}")
print(f"  Accuracy: {running_fix_result['fix_accuracy_nm']:.2f} nautical miles")
print(f"  Fix Quality: {running_fix_result['fix_quality']}")
```

## Error Analysis Example

```python
from src.position_fix import calculate_error_ellipse

# Calculate the error ellipse for the position fix
error_ellipse = calculate_error_ellipse(sights)

print(f"\\nError Ellipse Analysis:")
print(f"  Semi-major axis: {error_ellipse['semi_major_axis_nm']:.2f} nm")
print(f"  Semi-minor axis: {error_ellipse['semi_minor_axis_nm']:.2f} nm")
print(f"  Orientation: {error_ellipse['orientation_deg']:.1f}°")
print(f"  Confidence level: {error_ellipse['confidence_level']*100}%")
```

## Using with the Problem Generator

```python
from src.problem_generator import generate_multi_body_sight_reduction_problems

# Generate a set of realistic sight problems
multi_sights = generate_multi_body_sight_reduction_problems(num_bodies=3, time_window_hours=2.0)

# Format them for the position fix calculation
formatted_sights = []
for problem in multi_sights:
    # Calculate intercept and azimuth for this generated problem
    celestial_body = get_celestial_body(
        problem['celestial_body_name'], 
        problem['observation_time']
    )
    intercept, azimuth = calculate_intercept(
        problem['observed_altitude'],
        celestial_body,
        problem['assumed_position'],
        problem['observation_time'],
        temperature=problem['temperature'],
        pressure=problem['pressure'],
        observer_height=problem['observer_height'],
        celestial_body_name=problem['celestial_body_name'],
        limb=problem.get('limb', 'center')
    )
    
    formatted_sight = {
        'observed_altitude': problem['observed_altitude'],
        'celestial_body_name': problem['celestial_body_name'],
        'observation_time': problem['observation_time'],
        'intercept': intercept,
        'azimuth': azimuth,
        'assumed_position': problem['assumed_position'],
        'altitude_correction_error': 0.1
    }
    
    formatted_sights.append(formatted_sight)

# Calculate the position fix from the generated problems
generated_fix_result = calculate_least_squares_fix(formatted_sights)

print(f"\\nPosition Fix from Generated Problems:")
print(f"  Calculated Position: {generated_fix_result['fix_position'].lat:.6f}, {generated_fix_result['fix_position'].lon:.6f}")
print(f"  Actual Position (from generation): {multi_sights[0]['actual_position'].lat:.6f}, {multi_sights[0]['actual_position'].lon:.6f}")
print(f"  Accuracy: {generated_fix_result['fix_accuracy_nm']:.2f} nautical miles")
print(f"  Fix Quality: {generated_fix_result['fix_quality']}")
```

This example demonstrates the complete functionality of the Advanced Position Fix Calculation module, showing how to:
1. Calculate basic least squares fixes from multiple observations
2. Account for vessel movement with running fixes
3. Perform statistical error analysis
4. Integrate with the problem generation module for educational purposes