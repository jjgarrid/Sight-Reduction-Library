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