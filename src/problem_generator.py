"""
Problem Generator Module for Celestial Navigation

This module provides functions for generating realistic sight reduction problems
with enhanced parameters for educational and training purposes.
"""

import math
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon, get_body, SkyCoord
import astropy.units as u
import numpy as np
from .sight_reduction import (
    calculate_intercept, 
    get_celestial_body, 
    calculate_refraction_correction, 
    calculate_dip_correction, 
    calculate_limb_correction,
    validate_altitude,
    validate_temperature,
    validate_pressure,
    validate_observer_height,
    validate_celestial_body_name,
    validate_limb
)


def validate_instrument_error(error: float) -> None:
    """Validate that instrument error is within reasonable range (-1.0 to 1.0 degrees)."""
    if error < -1.0 or error > 1.0:
        raise ValueError(f"Instrument error {error}° is not in valid range [-1.0°, 1.0°]")


def validate_index_error(error: float) -> None:
    """Validate that index error is within reasonable range (-1.0 to 1.0 degrees)."""
    if error < -1.0 or error > 1.0:
        raise ValueError(f"Index error {error}° is not in valid range [-1.0°, 1.0°]")


def validate_personal_error(error: float) -> None:
    """Validate that personal error is within reasonable range (-1.0 to 1.0 degrees)."""
    if error < -1.0 or error > 1.0:
        raise ValueError(f"Personal error {error}° is not in valid range [-1.0°, 1.0°]")


def validate_sextant_precision(precision: float) -> None:
    """Validate that sextant precision is within reasonable range (0.01 to 1.0 degrees)."""
    if precision < 0.01 or precision > 1.0:
        raise ValueError(f"Sextant precision {precision}° is not in valid range [0.01°, 1.0°]")


def validate_humidity(humidity: float) -> None:
    """Validate that humidity is within reasonable range (0% to 100%)."""
    if humidity < 0 or humidity > 100:
        raise ValueError(f"Humidity {humidity}% is not in valid range [0%, 100%]")


def validate_wave_height(height: float) -> None:
    """Validate that wave height is non-negative."""
    if height < 0:
        raise ValueError(f"Wave height {height} m cannot be negative")


def validate_observation_quality(quality: str) -> None:
    """Validate observation quality is one of the allowed values."""
    valid_qualities = ['excellent', 'good', 'fair', 'poor']
    if quality.lower() not in valid_qualities:
        raise ValueError(f"Observation quality '{quality}' is not valid. Use one of: {valid_qualities}")


def calculate_total_observation_error(
    instrument_error: float = 0.0,
    index_error: float = 0.0,
    personal_error: float = 0.0,
    random_error: float = 0.0
) -> float:
    """
    Calculate the total systematic observation error.
    
    Parameters:
    - instrument_error: Error specific to the sextant being used (degrees)
    - index_error: Error in sextant's index mirror alignment (degrees)
    - personal_error: Individual observer's consistent error (degrees)
    - random_error: Random error component (degrees)
    
    Returns:
    - Total error in degrees
    """
    # Validate inputs
    validate_instrument_error(instrument_error)
    validate_index_error(index_error)
    validate_personal_error(personal_error)
    
    total_error = instrument_error + index_error + personal_error + random_error
    return total_error


def generate_realistic_position() -> Tuple[float, float]:
    """
    Generate a realistic position for navigation (in navigable waters).
    
    Returns:
    - Tuple of (latitude, longitude) in decimal degrees
    """
    # Generate a position in the Atlantic or Pacific (between 40°N and 40°S)
    lat = np.random.uniform(-40.0, 40.0)
    # Focus on Atlantic and Pacific, avoiding landmasses
    lon = np.random.uniform(-150.0, 10.0)  # More Atlantic/Pacific focus
    
    return lat, lon


def generate_realistic_time(start_date: datetime = datetime(2023, 1, 1), 
                           end_date: datetime = datetime(2025, 12, 31)) -> Time:
    """
    Generate a realistic time for celestial observations.
    
    Parameters:
    - start_date: Start date for observation
    - end_date: End date for observation
    
    Returns:
    - Astropy Time object for observation
    """
    from datetime import timedelta
    
    # Calculate random time between dates
    time_range = end_date - start_date
    random_days = np.random.uniform(0, time_range.days)
    random_time = start_date + timedelta(days=random_days)
    
    # Add random time of day (between 00:00 and 23:59)
    random_hour = np.random.uniform(0, 23.999)
    random_time = random_time.replace(
        hour=int(random_hour),
        minute=int((random_hour % 1) * 60),
        second=int(((random_hour % 1) * 60) % 1 * 60)
    )
    
    return Time(random_time.isoformat())


def get_realistic_atmospheric_conditions() -> Dict[str, float]:
    """
    Generate realistic atmospheric conditions.
    
    Returns:
    - Dictionary with temperature, pressure, humidity
    """
    # Generate realistic atmospheric conditions
    temperature = np.random.uniform(-10, 40)  # Celsius
    pressure = np.random.uniform(980, 1040)   # hPa
    humidity = np.random.uniform(30, 90)      # Percent
    
    return {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity
    }


def get_realistic_observer_parameters() -> Dict[str, float]:
    """
    Generate realistic observer parameters.
    
    Returns:
    - Dictionary with observer parameters
    """
    # Generate realistic observer parameters
    observer_height = np.random.uniform(2, 30)  # meters above sea level
    wave_height = np.random.uniform(0, 8)       # meters
    
    return {
        'observer_height': observer_height,
        'wave_height': wave_height
    }


def get_realistic_instrument_parameters() -> Dict[str, float]:
    """
    Generate realistic instrument parameters.
    
    Returns:
    - Dictionary with instrument parameters
    """
    # Generate realistic instrument parameters
    instrument_error = np.random.uniform(-0.2, 0.2)  # degrees
    index_error = np.random.uniform(-0.1, 0.1)       # degrees
    personal_error = np.random.uniform(-0.1, 0.1)    # degrees
    sextant_precision = np.random.uniform(0.05, 0.2) # degrees
    
    return {
        'instrument_error': instrument_error,
        'index_error': index_error,
        'personal_error': personal_error,
        'sextant_precision': sextant_precision
    }


def generate_sight_reduction_problem(
    actual_position: Optional[EarthLocation] = None,
    observation_time: Optional[Time] = None,
    celestial_body_name: Optional[str] = None,
    add_random_error: bool = True,
    error_range: float = 0.1,
    max_retries: int = 10,
    navigation_mode: str = 'marine',
    aircraft_altitude: float = 0.0
) -> Dict:
    """
    Generate a realistic sight reduction problem with all necessary parameters.
    
    Parameters:
    - actual_position: The actual vessel position (will be generated if None)
    - observation_time: Time of observation (will be generated if None)
    - celestial_body_name: Name of the celestial body (will be selected if None)
    - add_random_error: Whether to add random error to make the problem more realistic
    - error_range: Range of random error to add (in degrees)
    - max_retries: Maximum number of retries when celestial body is not visible
    - navigation_mode: Navigation mode ('marine' or 'aviation') to determine correction methods
    - aircraft_altitude: Aircraft altitude above sea level in meters (for aviation mode)
    
    Returns:
    - Dictionary containing all parameters needed for a sight reduction problem
    """
    # Validate navigation mode
    if navigation_mode not in ['marine', 'aviation']:
        raise ValueError(f"Navigation mode '{navigation_mode}' is not supported. Use 'marine' or 'aviation'")
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            # If no position is provided, generate a realistic one
            if actual_position is None:
                if navigation_mode == 'aviation':
                    # For aviation, we can be anywhere, not just in navigable waters
                    lat = np.random.uniform(-90.0, 90.0)  # Any latitude possible in aviation
                    lon = np.random.uniform(-180.0, 180.0)  # Any longitude
                else:
                    # For marine navigation, generate position in navigable waters
                    lat, lon = generate_realistic_position()
                
                actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
            
            # If no observation time is provided, generate a realistic one
            if observation_time is None:
                observation_time = generate_realistic_time()
            
            # If no celestial body is specified, randomly select one that's visible
            if celestial_body_name is None:
                celestial_bodies = ['sun', 'moon', 'venus', 'mars', 'jupiter', 'saturn']
                # For now, just randomly select one; in the future, we could check visibility
                celestial_body_name = np.random.choice(celestial_bodies)
            
            # Generate realistic parameters
            atmospheric = get_realistic_atmospheric_conditions()
            
            # Generate observer parameters based on navigation mode
            if navigation_mode == 'aviation':
                # For aviation, set appropriate parameters
                observer_height = 0.0  # No dip correction needed with bubble sextant
                wave_height = 0.0      # No waves in flight
                # Adjust atmospheric conditions for flight altitude
                # For now, we'll keep standard values, but could add altitude-based adjustments
            else:
                # For marine navigation
                observer_params = get_realistic_observer_parameters()
                observer_height = observer_params['observer_height']
                wave_height = observer_params['wave_height']
            
            # Generate instrument parameters
            instrument_params = get_realistic_instrument_parameters()
            
            # Randomly choose limb for Sun and Moon
            limb = 'center'  # default
            if celestial_body_name in ['sun', 'moon']:
                limb = np.random.choice(['upper', 'lower', 'center'])
            
            # Get celestial body position (true position)
            celestial_body = get_celestial_body(celestial_body_name, observation_time)
            
            # Create alt/az frame for actual position
            altaz_frame = AltAz(location=actual_position, obstime=observation_time)
            body_altaz = celestial_body.transform_to(altaz_frame)
            
            # Calculate true altitude and azimuth
            true_altitude = body_altaz.alt.deg
            true_azimuth = body_altaz.az.deg
            
            # Skip if celestial body is not visible (below horizon)
            if true_altitude < 0:
                retry_count += 1
                # Try with new parameters, but preserve the originally requested ones
                # Only reset the actual position since that affects visibility
                actual_position = None
                # Don't reset observation_time or celestial_body_name if they were provided
                continue
            
            # Apply corrections that the navigator would need to account for
            # But in reverse: start with the true altitude and add errors to get observed altitude
            
            # Add random error to make it more realistic
            random_error = 0.0
            if add_random_error:
                random_error = np.random.uniform(-error_range, error_range)
            
            # Calculate total systematic error from instrument factors
            total_systematic_error = calculate_total_observation_error(
                instrument_params['instrument_error'],
                instrument_params['index_error'],
                instrument_params['personal_error'],
                random_error
            )
            
            # Calculate refraction correction (what would be applied to observed altitude)
            refraction_correction = calculate_refraction_correction(
                true_altitude,
                atmospheric['temperature'],
                atmospheric['pressure'],
                observer_height
            )
            
            # Calculate dip correction based on navigation mode
            if navigation_mode == 'aviation':
                # In aviation mode, we use a bubble sextant which provides an artificial horizon
                # So we don't need dip correction, but we may need bubble sextant corrections
                dip_correction = 0.0
            else:
                # Calculate dip correction (what would be applied to observed altitude)
                dip_correction = calculate_dip_correction(observer_height)
            
            # Calculate limb correction (what would be applied to observed altitude)
            limb_correction = calculate_limb_correction(celestial_body_name, limb)
            
            # The observed altitude is what the navigator would measure with their sextant
            # Add all corrections and errors to the true altitude to get the observed altitude
            observed_altitude = true_altitude
            observed_altitude += refraction_correction  # Refraction makes body appear higher
            observed_altitude -= dip_correction         # Dip makes horizon appear lower (or 0 for aviation)
            observed_altitude -= limb_correction        # Limb correction adjustment
            observed_altitude -= total_systematic_error  # Errors in measurement
            
            # Ensure observed altitude is in valid range (Celestial body must be above horizon to observe it)
            if observed_altitude < 0.1 or observed_altitude > 90:  # Use 0.1 to allow for tiny altitudes at horizon
                retry_count += 1
                # Try with new parameters, but preserve the originally requested ones
                # Only reset the actual position since that affects visibility
                actual_position = None
                # Don't reset observation_time or celestial_body_name if they were provided
                continue
            
            # Create an assumed position (close to actual) for the problem
            assumed_lat = actual_position.lat.deg + np.random.uniform(-0.5, 0.5)
            assumed_lon = actual_position.lon.deg + np.random.uniform(-0.5, 0.5)
            assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)
            
            # Return all parameters for the sight reduction problem
            problem_params = {
                'actual_position': actual_position,
                'assumed_position': assumed_position,
                'observed_altitude': observed_altitude,
                'celestial_body_name': celestial_body_name,
                'observation_time': observation_time,
                'temperature': atmospheric['temperature'],
                'pressure': atmospheric['pressure'],
                'humidity': atmospheric['humidity'],
                'observer_height': observer_height,  # Use the value based on navigation mode
                'wave_height': wave_height,         # Use the value based on navigation mode
                'instrument_error': instrument_params['instrument_error'],
                'index_error': instrument_params['index_error'],
                'personal_error': instrument_params['personal_error'],
                'sextant_precision': instrument_params['sextant_precision'],
                'limb': limb,
                'true_altitude': true_altitude,
                'true_azimuth': true_azimuth,
                'refraction_correction': refraction_correction,
                'dip_correction': dip_correction,
                'limb_correction': limb_correction,
                'total_systematic_error': total_systematic_error,
                'navigation_mode': navigation_mode,
                'aircraft_altitude': aircraft_altitude if navigation_mode == 'aviation' else 0.0
            }
            
            return problem_params
            
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                # If we've exhausted retries, raise an exception
                raise RuntimeError(f"Failed to generate sight reduction problem after {max_retries} retries: {e}")
            # Otherwise, continue to the next iteration with new parameters
    
    # This should not be reached if max_retries is handled properly above
    raise RuntimeError(f"Failed to generate sight reduction problem after {max_retries} retries")


def format_problem_for_user(problem_params: Dict) -> str:
    """
    Format the sight reduction problem in a user-friendly way.
    
    Parameters:
    - problem_params: Dictionary containing the problem parameters
    
    Returns:
    - Formatted string describing the sight reduction problem
    """
    obs_time = problem_params['observation_time'].iso
    body_name = problem_params['celestial_body_name'].capitalize()
    navigation_mode = problem_params.get('navigation_mode', 'marine')
    limb_text = f" ({problem_params['limb']} limb)" if problem_params['celestial_body_name'] in ['sun', 'moon'] else ""
    
    # Customize the problem text based on navigation mode
    if navigation_mode == 'aviation':
        problem_text = f"""
AERONAUTICAL SIGHT REDUCTION PROBLEM

Celestial Body: {body_name}{limb_text}
Observation Time (UTC): {obs_time}

Observed Sextant Altitude: {problem_params['observed_altitude']:.1f}°
(Using bubble sextant with artificial horizon)

Environmental Conditions:
- Temperature: {problem_params['temperature']:.1f}°C
- Atmospheric Pressure: {problem_params['pressure']:.1f} hPa
- Aircraft Altitude: {problem_params['aircraft_altitude']:.1f} meters

Assumed Position:
- Latitude: {problem_params['assumed_position'].lat.deg:+.4f}°
- Longitude: {problem_params['assumed_position'].lon.deg:+.4f}°

Instrument Parameters:
- Instrument Error: {problem_params['instrument_error']:.3f}°
- Index Error: {problem_params['index_error']:.3f}°
- Personal Error: {problem_params['personal_error']:.3f}°

Task: 
Calculate the intercept and azimuth for this aviation observation using sight reduction methods.
The actual aircraft position is at: 
- Latitude: {problem_params['actual_position'].lat.deg:+.4f}°
- Longitude: {problem_params['actual_position'].lon.deg:+.4f}°
"""
    else:  # marine navigation
        problem_text = f"""
SIGHT REDUCTION PROBLEM

Celestial Body: {body_name}{limb_text}
Observation Time (UTC): {obs_time}

Observed Sextant Altitude: {problem_params['observed_altitude']:.1f}°

Environmental Conditions:
- Temperature: {problem_params['temperature']:.1f}°C
- Atmospheric Pressure: {problem_params['pressure']:.1f} hPa
- Observer Height: {problem_params['observer_height']:.1f} meters

Assumed Position:
- Latitude: {problem_params['assumed_position'].lat.deg:+.4f}°
- Longitude: {problem_params['assumed_position'].lon.deg:+.4f}°

Instrument Parameters:
- Instrument Error: {problem_params['instrument_error']:.3f}°
- Index Error: {problem_params['index_error']:.3f}°
- Personal Error: {problem_params['personal_error']:.3f}°

Task: 
Calculate the intercept and azimuth for this observation using sight reduction methods.
The actual vessel position is at: 
- Latitude: {problem_params['actual_position'].lat.deg:+.4f}°
- Longitude: {problem_params['actual_position'].lon.deg:+.4f}°
"""
    return problem_text


def validate_problem_solution(observed_altitude: float, celestial_body_name: str, assumed_position: EarthLocation, 
                             observation_time: Time, intercept: float, azimuth: float, temperature: float = 10.0, 
                             pressure: float = 1010.0, observer_height: float = 0.0, limb: str = 'center',
                             navigation_mode: str = 'marine') -> Dict[str, float]:
    """
    Validate a solution to a sight reduction problem by comparing with the known actual position.
    
    Parameters:
    - observed_altitude: The altitude measured with the sextant
    - celestial_body_name: Name of the celestial body observed
    - assumed_position: The assumed position used for calculation
    - observation_time: Time of the observation
    - intercept: Calculated intercept from user's solution
    - azimuth: Calculated azimuth from user's solution
    - temperature: Atmospheric temperature (default 10°C)
    - pressure: Atmospheric pressure (default 1010 hPa)
    - observer_height: Height above sea level (default 0m)
    - limb: Which limb was observed ('upper', 'lower', 'center') - for Sun and Moon
    - navigation_mode: Navigation mode ('marine' or 'aviation') to determine correction methods
    
    Returns:
    - Dictionary with validation results
    """
    # Get the celestial body
    celestial_body = get_celestial_body(celestial_body_name, observation_time)
    
    # Calculate our own intercept and azimuth
    computed_intercept, computed_azimuth = calculate_intercept(
        observed_altitude, 
        celestial_body, 
        assumed_position, 
        observation_time,
        apply_refraction=True,
        temperature=temperature,
        pressure=pressure,
        observer_height=observer_height,
        celestial_body_name=celestial_body_name,
        limb=limb,
        navigation_mode=navigation_mode,
        aircraft_speed_knots=0.0,  # Default: no movement
        aircraft_course=0.0,      # Default: no course
        time_interval_hours=0.0   # Default: no time interval
    )
    
    # Return validation metrics
    return {
        'computed_intercept': computed_intercept,
        'computed_azimuth': computed_azimuth,
        'user_intercept_error': abs(computed_intercept - intercept),
        'user_azimuth_error': abs(computed_azimuth - azimuth) % 360,  # Normalize to 0-360°
        'acceptable_intercept_error': 0.5,  # nautical miles
        'acceptable_azimuth_error': 1.0    # degrees
    }


# Template-based generation for common scenarios
def generate_morning_sight_problem() -> Dict:
    """
    Generate a morning sight problem (typically Sun lower limb sight).
    
    Returns:
    - Dictionary containing parameters for a morning sight problem
    """
    from datetime import datetime
    
    # Generate a few attempts to get a good morning sight
    max_attempts = 10
    for attempt in range(max_attempts):
        # Morning sights are typically done after sunrise but before the sun gets too high
        # So we'll simulate an observation time around 08:00 - 10:00 UTC
        base_date = datetime(2023, 6, 15)  # Summer in the northern hemisphere
        # Add a random time between 08:00 and 10:00
        random_hour = np.random.uniform(8, 10)
        obs_datetime = base_date.replace(
            hour=int(random_hour),
            minute=int((random_hour % 1) * 60)
        )
        observation_time = Time(obs_datetime.isoformat())
        
        # Generate a position where the sun is likely to be visible in the morning
        lat, lon = generate_realistic_position()
        actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
        
        # Use the Sun for morning sight
        celestial_body_name = 'sun'
        
        try:
            # Generate the problem
            problem = generate_sight_reduction_problem(
                actual_position=actual_position,
                observation_time=observation_time,
                celestial_body_name=celestial_body_name,
                add_random_error=True,
                error_range=0.15,  # Slightly more error for realistic morning shots
                max_retries=3  # Limit retries to avoid changing the time
            )
            
            # Double-check that our celestial body name is preserved
            if problem['celestial_body_name'] == 'sun':
                return problem
        except Exception:
            # If generation fails, continue to next attempt
            continue
    
    # Fallback: if we can't generate a morning-specific sight, 
    # at least return a valid sun sight
    base_date = datetime(2023, 6, 15)
    random_hour = np.random.uniform(6, 12)  # Broader morning/early afternoon window
    obs_datetime = base_date.replace(
        hour=int(random_hour),
        minute=int((random_hour % 1) * 60)
    )
    observation_time = Time(obs_datetime.isoformat())
    
    lat, lon = generate_realistic_position()
    actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
    
    return generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name='sun',
        add_random_error=True,
        error_range=0.15,
        max_retries=5
    )


def generate_evening_sight_problem() -> Dict:
    """
    Generate an evening sight problem (typically Sun upper limb sight).
    
    Returns:
    - Dictionary containing parameters for an evening sight problem
    """
    from datetime import datetime
    
    # Generate a few attempts to get a good evening sight
    max_attempts = 10
    for attempt in range(max_attempts):
        # Evening sights are typically done before sunset when the sun is still visible
        # So we'll simulate an observation time around 16:00 - 18:00 UTC
        base_date = datetime(2023, 6, 15)  # Summer in the northern hemisphere
        # Add a random time between 16:00 and 18:00
        random_hour = np.random.uniform(16, 18)
        obs_datetime = base_date.replace(
            hour=int(random_hour),
            minute=int((random_hour % 1) * 60)
        )
        observation_time = Time(obs_datetime.isoformat())
        
        # Generate a realistic position
        lat, lon = generate_realistic_position()
        actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
        
        # Use the Sun for evening sight
        celestial_body_name = 'sun'
        
        try:
            # Generate the problem
            problem = generate_sight_reduction_problem(
                actual_position=actual_position,
                observation_time=observation_time,
                celestial_body_name=celestial_body_name,
                add_random_error=True,
                error_range=0.15,  # Slightly more error for realistic evening shots
                max_retries=3  # Limit retries to avoid changing the time
            )
            
            # Double-check that our celestial body name is preserved
            if problem['celestial_body_name'] == 'sun':
                return problem
        except Exception:
            # If generation fails, continue to next attempt
            continue
    
    # Fallback: if we can't generate an evening-specific sight, 
    # at least return a valid sun sight
    base_date = datetime(2023, 6, 15)
    random_hour = np.random.uniform(14, 19)  # Broader afternoon/evening window
    obs_datetime = base_date.replace(
        hour=int(random_hour),
        minute=int((random_hour % 1) * 60)
    )
    observation_time = Time(obs_datetime.isoformat())
    
    lat, lon = generate_realistic_position()
    actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
    
    return generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name='sun',
        add_random_error=True,
        error_range=0.15,
        max_retries=5
    )


def generate_twilight_star_sight_problem(star_name: Optional[str] = None) -> Dict:
    """
    Generate a twilight star sight problem.
    
    Parameters:
    - star_name: Name of the star to observe (will be selected randomly if None)
    
    Returns:
    - Dictionary containing parameters for a star sight problem
    """
    from datetime import datetime
    
    # Generate a few attempts to get a good star sight
    max_attempts = 10
    for attempt in range(max_attempts):
        # Star sights are typically done during twilight when stars are visible but the horizon is still clear
        # So we'll simulate an observation time around civil twilight (05:30-06:30 or 18:30-19:30 UTC)
        
        # Randomly choose morning or evening twilight
        if np.random.choice([True, False]):  # Morning twilight
            base_date = datetime(2023, 6, 15, 5, 30)  # Morning twilight
            random_minutes = np.random.uniform(0, 60)  # 05:30 to 06:30
            obs_datetime = base_date.replace(minute=int(random_minutes))
        else:  # Evening twilight
            base_date = datetime(2023, 6, 15, 18, 30)  # Evening twilight
            random_minutes = np.random.uniform(0, 60)  # 18:30 to 19:30
            obs_datetime = base_date.replace(minute=int(random_minutes))
        
        observation_time = Time(obs_datetime.isoformat())
        
        # Generate a realistic position
        lat, lon = generate_realistic_position()
        actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
        
        # Use a star - either the one provided or a random one from supported stars
        if star_name is None:
            supported_stars = ['sirius', 'canopus', 'arcturus', 'rigel', 'procyon', 
                              'vega', 'capella', 'rigel_kentaurus_a', 'altair', 'acrux',
                              'aldebaran', 'spica', 'antares', 'pollux', 'deneb']
            selected_star = np.random.choice(supported_stars)
        else:
            selected_star = star_name
        
        try:
            # Generate the problem
            problem = generate_sight_reduction_problem(
                actual_position=actual_position,
                observation_time=observation_time,
                celestial_body_name=selected_star,
                add_random_error=True,
                error_range=0.1  # Less error for star sights (stars don't have limb issues)
            )
            
            # Double-check that our celestial body name is preserved
            if problem['celestial_body_name'] == selected_star:
                return problem
        except Exception:
            # If generation fails, continue to next attempt
            continue
    
    # Fallback: if we can't generate a twilight-specific sight, 
    # at least return a valid star sight
    if star_name is None:
        supported_stars = ['sirius', 'canopus', 'arcturus', 'rigel', 'procyon', 
                          'vega', 'capella', 'rigel_kentaurus_a', 'altair', 'acrux',
                          'aldebaran', 'spica', 'antares', 'pollux', 'deneb']
        selected_star = np.random.choice(supported_stars)
    else:
        selected_star = star_name
    
    base_date = datetime(2023, 6, 15)
    random_hour = np.random.uniform(0, 23.99)
    obs_datetime = base_date.replace(
        hour=int(random_hour),
        minute=int((random_hour % 1) * 60)
    )
    observation_time = Time(obs_datetime.isoformat())
    
    lat, lon = generate_realistic_position()
    actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
    
    return generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name=selected_star,
        add_random_error=True,
        error_range=0.1,
        max_retries=5
    )


def generate_moon_sight_problem() -> Dict:
    """
    Generate a Moon sight problem.
    
    Returns:
    - Dictionary containing parameters for a Moon sight problem
    """
    # Moon sights can be done during day or night depending on moon phase and position
    from datetime import datetime
    
    # Generate a realistic date/time
    base_date = datetime(2023, 6, 15)
    # Add a random time of day
    random_hour = np.random.uniform(0, 23.99)
    obs_datetime = base_date.replace(
        hour=int(random_hour),
        minute=int((random_hour % 1) * 60)
    )
    observation_time = Time(obs_datetime.isoformat())
    
    # Generate a realistic position
    lat, lon = generate_realistic_position()
    actual_position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
    
    # Use the Moon - explicitly set the celestial body name
    celestial_body_name = 'moon'
    
    # Generate the problem with the specific celestial body name
    return generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name=celestial_body_name,
        add_random_error=True,
        error_range=0.2  # More error for moon sights due to its rapid movement
    )


def generate_multi_body_sight_reduction_problems(num_bodies: int = 3, 
                                                 time_window_hours: float = 2.0,
                                                 navigation_mode: str = 'marine',
                                                 aircraft_altitude: float = 0.0) -> list:
    """
    Generate multiple sight reduction problems for a position fix.
    
    Parameters:
    - num_bodies: Number of celestial bodies to observe (default 3)
    - time_window_hours: Time window in which all observations are made (default 2 hours)
    - navigation_mode: Navigation mode ('marine' or 'aviation') to determine correction methods
    - aircraft_altitude: Aircraft altitude in meters (for aviation mode)
    
    Returns:
    - List of dictionaries, each containing parameters for a sight reduction problem
    """
    if num_bodies < 2 or num_bodies > 5:
        raise ValueError("Number of bodies should be between 2 and 5 for a good position fix")
    
    # Generate a base time that will be shared across all observations
    base_time = generate_realistic_time()
    
    # Define possible celestial bodies for multiple sightings
    possible_bodies = ['sun', 'moon', 'venus', 'mars', 'jupiter', 'saturn']
    
    problems = []
    for i in range(num_bodies):
        # Attempt to generate a problem with constraints
        problem_generated = False
        attempt = 0
        max_attempts = 20  # Prevent infinite loops
        
        while not problem_generated and attempt < max_attempts:
            # Each observation happens within the time window of the first
            time_offset = np.random.uniform(0, time_window_hours)
            obs_time = Time((base_time.datetime + timedelta(hours=time_offset)).isoformat())
            
            # Get a celestial body for this observation
            celestial_body = np.random.choice(possible_bodies)
            
            try:
                # Generate the problem with the specific time and celestial body
                problem = generate_sight_reduction_problem(
                    actual_position=None,  # Allow generating new position for each body
                    observation_time=obs_time,
                    celestial_body_name=celestial_body,
                    add_random_error=True,
                    error_range=0.15,  # Standard error for realistic problems
                    max_retries=8,     # High retry count but not too high
                    navigation_mode=navigation_mode,
                    aircraft_altitude=aircraft_altitude
                )
                
                problems.append(problem)
                problem_generated = True
                
            except RuntimeError:
                # If generation fails, try again with different parameters
                attempt += 1
                if attempt >= max_attempts:
                    # If we still can't generate after many attempts, use a guaranteed visible body
                    # like the Sun or Moon with more flexibility
                    fallback_bodies = ['sun', 'moon']
                    fallback_body = np.random.choice(fallback_bodies)
                    
                    problem = generate_sight_reduction_problem(
                        actual_position=None,
                        observation_time=obs_time,
                        celestial_body_name=fallback_body,
                        add_random_error=True,
                        error_range=0.15,
                        max_retries=10,
                        navigation_mode=navigation_mode,
                        aircraft_altitude=aircraft_altitude
                    )
                    
                    problems.append(problem)
                    problem_generated = True
    
    return problems