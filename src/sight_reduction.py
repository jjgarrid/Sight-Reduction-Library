"""
Sight Reduction Module for Celestial Navigation

This module provides functions for performing celestial navigation sight reductions,
including calculating intercepts and azimuths based on celestial observations.
"""
import math
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon, get_body, SkyCoord
import astropy.units as u
import numpy as np


def validate_altitude(altitude: float) -> None:
    """Validate that altitude is within reasonable range."""
    if altitude < -1 or altitude > 90:
        raise ValueError(f"Altitude {altitude}° is not in valid range [-1°, 90°]")


def validate_temperature(temperature: float) -> None:
    """Validate temperature is within reasonable range (-100°C to +100°C)."""
    if temperature < -100 or temperature > 100:
        raise ValueError(f"Temperature {temperature}°C is not in valid range [-100°C, 100°C]")


def validate_pressure(pressure: float) -> None:
    """Validate pressure is within reasonable range (800 to 1200 hPa)."""
    if pressure < 800 or pressure > 1200:
        raise ValueError(f"Pressure {pressure} hPa is not in valid range [800 hPa, 1200 hPa]")


def validate_observer_height(height: float) -> None:
    """Validate observer height is non-negative."""
    if height < 0:
        raise ValueError(f"Observer height {height} m cannot be negative")


def validate_celestial_body_name(name: str) -> None:
    """Validate celestial body name is supported."""
    supported_bodies = [
        'sun', 'moon',  # Original bodies
        # Planets
        'mercury', 'venus', 'mars', 'jupiter', 'saturn',
        # Some commonly used stars
        'sirius', 'canopus', 'arcturus', 'rigel', 'procyon', 
        'vega', 'capella', 'rigel_kentaurus_a', 'altair', 'acrux',
        'aldebaran', 'spica', 'antares', 'pollux', 'deneb', 
        'betelgeuse', 'bellatrix', 'alpheratz', 'fomalhaut', 'polaris'
    ]
    if name and name.lower() not in supported_bodies:
        raise ValueError(f"Celestial body '{name}' is not supported for limb correction")


def validate_limb(limb: str) -> None:
    """Validate limb value is supported."""
    if limb.lower() not in ['center', 'upper', 'lower']:
        raise ValueError(f"Limb '{limb}' is not supported. Use 'center', 'upper', or 'lower'")


def calculate_refraction_correction(observed_altitude: float, 
                                  temperature: float = 10.0, 
                                  pressure: float = 1010.0) -> float:
    """
    Calculate atmospheric refraction correction for celestial observations.
    
    Parameters:
    - observed_altitude: The observed altitude of the celestial body in degrees
    - temperature: Atmospheric temperature in degrees Celsius (default: 10°C)
    - pressure: Atmospheric pressure in hPa (default: 1010 hPa)
    
    Returns:
    - Refraction correction in degrees to be subtracted from observed altitude
    """
    # Validate inputs
    validate_altitude(observed_altitude)
    validate_temperature(temperature)
    validate_pressure(pressure)
    
    # Convert observed altitude to radians for calculation
    alt_deg = observed_altitude
    alt_rad = math.radians(alt_deg)
    
    # Check if altitude is at or below horizon 
    if alt_deg <= 0:
        return 0.0  # No correction below horizon
    
    # For altitudes near the horizon (up to 15 degrees), use more accurate formula
    if alt_deg <= 15:
        # Calculate apparent altitude in minutes of arc
        alt_min = alt_deg * 60.0
        
        # Calculate refraction using standard formula for low altitudes
        # R = 0.96 / tan(h + 7.32/(h + 4.32))
        # where h is in minutes of arc
        h = alt_min + 7.32 / (alt_min + 4.32)
        refraction_min = 0.96 / math.tan(math.radians(h / 60.0))
        
        # Apply temperature and pressure corrections
        refraction_min *= (pressure / 1010.0) * (273.0 / (273.0 + temperature))
        
        # Convert from minutes of arc to degrees
        refraction_deg = refraction_min / 60.0
    else:
        # For higher altitudes, use simplified formula
        # R = 1.02 / tan(h) where h is in degrees
        if math.sin(alt_rad) == 0:  # Altitude is 0 (horizon)
            refraction_deg = 34.0 / 60.0  # Standard refraction at horizon in degrees
        else:
            refraction_min = 1.02 / math.tan(alt_rad)  # In minutes of arc
            refraction_deg = (refraction_min / 60.0) * (pressure / 1010.0) * (273.0 / (273.0 + temperature))
    
    # Refraction makes objects appear higher than they actually are
    # The correction value is positive (as refraction always makes things appear higher)
    # To get true altitude from observed altitude, subtract this correction
    return abs(refraction_deg)  # Return positive value representing the correction amount


def apply_refraction_correction(observed_altitude: float, 
                              temperature: float = 10.0, 
                              pressure: float = 1010.0) -> float:
    """
    Apply atmospheric refraction correction to convert observed altitude to true altitude.
    
    Parameters:
    - observed_altitude: The raw altitude measured with the sextant in degrees
    - temperature: Atmospheric temperature in degrees Celsius
    - pressure: Atmospheric pressure in hPa
    
    Returns:
    - True altitude in degrees (after refraction correction)
    """
    correction = calculate_refraction_correction(observed_altitude, temperature, pressure)
    # Since refraction makes objects appear higher, subtract the correction to get true altitude
    return observed_altitude - correction


def calculate_dip_correction(observer_height: float) -> float:
    """
    Calculate the dip of the horizon correction for an elevated observer.
    
    When observing from an elevated position (like on a ship), the horizon
    appears lower than it would from sea level. This correction accounts for
    that effect.
    
    Parameters:
    - observer_height: Height of observer above sea level in meters
    
    Returns:
    - Dip correction in degrees (always negative, since horizon appears lower)
    """
    validate_observer_height(observer_height)
    if observer_height <= 0:
        return 0.0
    
    # Standard formula for dip of horizon: 
    # Dip (minutes) = 0.97 * sqrt(height in meters)
    dip_minutes = 0.97 * math.sqrt(observer_height)
    
    # Convert to degrees
    dip_degrees = dip_minutes / 60.0
    
    # Dip is negative because the horizon appears lower
    return dip_degrees  # Return positive value; in the main function, we add it to the altitude


def calculate_limb_correction(celestial_body_name: str, limb: str = "center") -> float:
    """
    Calculate limb correction for observations of celestial bodies with appreciable angular size.
    
    When observing bodies with appreciable angular size (Sun, Moon, planets), 
    navigators sometimes use the upper or lower limb instead of the center. 
    This correction accounts for the angular radius of these bodies.
    
    Parameters:
    - celestial_body_name: Name of the celestial body ('sun', 'moon', or planets)
    - limb: Which part of the body to observe ('center', 'upper', or 'lower')
    
    Returns:
    - Limb correction in degrees
    """
    # If the body name is not provided, return 0
    if celestial_body_name is None:
        return 0.0
    
    validate_celestial_body_name(celestial_body_name)
    validate_limb(limb)
    
    body_name_lower = celestial_body_name.lower()
    limb_lower = limb.lower()
    
    # Determine the angular radius based on the celestial body
    if body_name_lower in ['sun', 'moon']:
        # Angular radius of Sun and Moon is approximately 16 minutes of arc (15.8' on average)
        # For simplicity, we'll use 16 minutes = 16/60 degrees
        angular_radius_deg = 16.0 / 60.0  # degrees
    elif body_name_lower in ['mercury']:
        # Mercury has a small angular size
        angular_radius_deg = (3.0 + 13.0) / 2 / 3600  # Convert from arcseconds to degrees
    elif body_name_lower in ['venus']:
        # Venus has varying angular size depending on distance
        angular_radius_deg = (9.5 + 68.0) / 2 / 3600  # Convert from arcseconds to degrees
    elif body_name_lower in ['mars']:
        # Mars has varying angular size depending on distance
        angular_radius_deg = (3.5 + 25.1) / 2 / 3600  # Convert from arcseconds to degrees
    elif body_name_lower in ['jupiter']:
        # Jupiter has a substantial angular size
        angular_radius_deg = (29.8 + 50.1) / 2 / 3600  # Convert from arcseconds to degrees
    elif body_name_lower in ['saturn']:
        # Saturn has substantial angular size including rings
        angular_radius_deg = (14.5 + 20.1) / 2 / 3600  # Convert from arcseconds to degrees
    else:
        # Stars appear as point sources, no limb correction needed
        return 0.0
    
    if limb_lower == 'upper':
        # When observing upper limb, the center is lower, so subtract the radius
        return -angular_radius_deg
    elif limb_lower == 'lower':
        # When observing lower limb, the center is higher, so add the radius
        return angular_radius_deg
    elif limb_lower == 'center':
        # No correction needed for center
        return 0.0
    else:
        # Default to center if invalid limb specified
        return 0.0


def calculate_intercept(observed_altitude, celestial_body, assumed_position, observation_time,
                       apply_refraction=True, temperature=10.0, pressure=1010.0, 
                       observer_height=0.0, celestial_body_name=None, limb='center'):
    """
    Perform a sight reduction to calculate the intercept (distance and direction) and azimuth
    with atmospheric corrections.

    Parameters:
    - observed_altitude: Observed altitude of the celestial body (degrees).
    - celestial_body: Astropy SkyCoord object for the celestial body.
    - assumed_position: EarthLocation object for the assumed observer position.
    - observation_time: Astropy Time object for the observation time.
    - apply_refraction: Whether to apply atmospheric refraction correction (default True).
    - temperature: Atmospheric temperature in degrees Celsius (default 10°C).
    - pressure: Atmospheric pressure in hPa (default 1010 hPa).
    - observer_height: Height of observer above sea level in meters (default 0).
    - celestial_body_name: Name of the celestial body ('sun', 'moon', etc.) for limb correction.
    - limb: Which part of the celestial body to observe ('center', 'upper', 'lower').

    Returns:
    - intercept: Distance between observed and calculated altitude (nautical miles).
    - azimuth: Calculated azimuth of the celestial body (degrees).
    """
    # Validate inputs
    validate_altitude(observed_altitude)
    validate_temperature(temperature)
    validate_pressure(pressure)
    validate_observer_height(observer_height)
    if celestial_body_name is not None:
        validate_celestial_body_name(celestial_body_name)
        validate_limb(limb)
    
    # Apply atmospheric corrections to the observed altitude
    corrected_altitude = observed_altitude
    
    # Apply refraction correction
    if apply_refraction:
        refraction_corr = calculate_refraction_correction(observed_altitude, temperature, pressure)
        corrected_altitude -= refraction_corr  # Subtract because refraction makes objects appear higher
    
    # Apply dip of horizon correction if observer is elevated
    if observer_height > 0:
        dip_corr = calculate_dip_correction(observer_height)
        corrected_altitude += dip_corr  # Add dip correction (dip makes horizon appear lower)
    
    # Apply limb correction if needed
    if celestial_body_name is not None:
        limb_corr = calculate_limb_correction(celestial_body_name, limb)
        corrected_altitude += limb_corr
    
    # Create an AltAz frame for the assumed position
    altaz_frame = AltAz(location=assumed_position, obstime=observation_time)

    # Transform the celestial body's coordinates to AltAz
    body_altaz = celestial_body.transform_to(altaz_frame)

    # Extract calculated altitude and azimuth
    calculated_altitude = body_altaz.alt.deg
    azimuth = body_altaz.az.deg

    # Calculate the intercept (difference in altitude)
    intercept = (corrected_altitude - calculated_altitude) * 60  # Convert degrees to nautical miles

    return intercept, azimuth


def get_total_observation_correction(observed_altitude: float, 
                                   temperature: float = 10.0, 
                                   pressure: float = 1010.0,
                                   observer_height: float = 0.0,
                                   celestial_body_name: str = None,
                                   limb: str = 'center') -> dict:
    """
    Calculate all corrections for a celestial observation.
    
    Parameters:
    - observed_altitude: Raw observed altitude in degrees
    - temperature: Atmospheric temperature in degrees Celsius
    - pressure: Atmospheric pressure in hPa
    - observer_height: Height of observer above sea level in meters
    - celestial_body_name: Name of celestial body for limb correction
    - limb: Which part of the body to observe ('center', 'upper', 'lower')
    
    Returns:
    - Dictionary with all corrections and final altitude
    """
    # Validate inputs first
    validate_altitude(observed_altitude)
    validate_temperature(temperature)
    validate_pressure(pressure)
    validate_observer_height(observer_height)
    if celestial_body_name is not None:
        validate_celestial_body_name(celestial_body_name)
        validate_limb(limb)
    
    corrections = {
        'observed_altitude': observed_altitude,
        'refraction_correction': 0.0,
        'dip_correction': 0.0,
        'limb_correction': 0.0,
        'total_correction': 0.0,
        'corrected_altitude': observed_altitude
    }
    
    # Calculate refraction correction
    refraction_corr = calculate_refraction_correction(observed_altitude, temperature, pressure)
    corrections['refraction_correction'] = refraction_corr
    
    # Calculate dip correction if observer is elevated
    if observer_height > 0:
        dip_corr = calculate_dip_correction(observer_height)
        corrections['dip_correction'] = dip_corr
    
    # Calculate limb correction if needed
    if celestial_body_name is not None:
        limb_corr = calculate_limb_correction(celestial_body_name, limb)
        corrections['limb_correction'] = limb_corr
    
    # Apply all corrections
    corrected_alt = observed_altitude
    corrected_alt -= refraction_corr  # Refraction makes objects appear higher, so subtract
    corrected_alt += corrections['dip_correction']  # Dip affects the horizon, so add
    corrected_alt += corrections['limb_correction']  # Add limb correction
    
    corrections['corrected_altitude'] = corrected_alt
    corrections['total_correction'] = corrected_alt - observed_altitude
    
    return corrections


def calculate_limb_altitudes(center_altitude, celestial_body, observation_time, observer_location):
    """
    Calculate lower and upper limb altitudes.
    """
    # Calculate the angular radius of the celestial body
    if celestial_body == "sun":
        body = get_sun(observation_time)
    elif celestial_body == "moon":
        body = get_moon(observation_time)
    else:
        raise ValueError("Only 'sun' or 'moon' supported for now.")
    
    # AltAz frame for the observer
    altaz_frame = AltAz(location=observer_location, obstime=observation_time)
    body_altaz = body.transform_to(altaz_frame)

    # Angular diameter
    angular_diameter = body.size.to(u.deg)  # Angular diameter in degrees
    angular_radius = angular_diameter / 2

    # Calculate limb altitudes
    lower_limb = center_altitude - angular_radius.value
    upper_limb = center_altitude + angular_radius.value

    return lower_limb, upper_limb


def get_celestial_body(name, observation_time):
    """
    Get the appropriate celestial body based on name
    
    Parameters:
    - name: Name of the celestial body ('sun', 'moon', planets, or stars)
    - observation_time: Astropy Time object for the observation time
    
    Returns:
    - Astropy SkyCoord object for the celestial body
    """
    name_lower = name.lower()
    
    # Handle Sun and Moon
    if name_lower == "sun":
        return get_sun(observation_time)
    elif name_lower == "moon":
        return get_moon(observation_time)
    
    # Handle planets
    elif name_lower in ["mercury", "venus", "mars", "jupiter", "saturn", 
                        "uranus", "neptune"]:
        try:
            return get_body(name_lower, observation_time)
        except Exception:
            # If planet is not available for this time, raise a more descriptive error
            raise ValueError(f"Could not compute position for {name_lower} at the specified time")
    
    # Handle stars and other celestial bodies
    else:
        # Try to get the star from our star database
        try:
            from . import star_database
            star_coord = star_database.get_star_coordinates(name)
            if star_coord is not None:
                return star_coord
        except ImportError:
            # star_database module not available, continue to default
            pass
        
        # For unknown bodies, default to Polaris as fallback
        # This preserves backward compatibility
        return SkyCoord(ra=2.530301028*u.hourangle, dec=89.264109444*u.deg)


def format_position(lat, lon):
    """
    Format latitude and longitude in degrees, minutes, and seconds
    """
    def to_dms(decimal_degrees):
        degrees = int(decimal_degrees)
        minutes_float = abs(decimal_degrees - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60
        return f"{degrees}°{minutes:02d}'{seconds:05.2f}\""
    
    lat_cardinal = "N" if lat >= 0 else "S"
    lon_cardinal = "E" if lon >= 0 else "W"
    
    return f"{to_dms(abs(lat))}{lat_cardinal}, {to_dms(abs(lon))}{lon_cardinal}"


def visualize_sight_reduction(observed_altitude, celestial_body_name, assumed_lat, assumed_lon, 
                              observation_time, apply_refraction=True, temperature=10.0, 
                              pressure=1010.0, observer_height=0.0, limb='center', 
                              plot_type='both', save_path=None):
    """
    Visualize the sight reduction results with plots.
    
    Parameters:
    - observed_altitude: Observed altitude of the celestial body (degrees)
    - celestial_body_name: Name of the celestial body
    - assumed_lat: Assumed latitude (degrees)
    - assumed_lon: Assumed longitude (degrees)
    - observation_time: Astropy Time object for the observation time
    - apply_refraction: Whether to apply atmospheric refraction correction
    - temperature: Atmospheric temperature in degrees Celsius
    - pressure: Atmospheric pressure in hPa
    - observer_height: Height of observer above sea level in meters
    - limb: Which part of the celestial body to observe ('center', 'upper', 'lower')
    - plot_type: Type of plot to create ('azimuth', 'line_of_position', 'both')
    - save_path: Path to save the plot (optional)
    
    Returns:
    - Tuple of matplotlib figure objects
    """
    try:
        # Import here to avoid circular imports
        from .plotting import create_azimuth_compass_plot, create_line_of_position_plot
        
        # Get the celestial body
        celestial_body = get_celestial_body(celestial_body_name, observation_time)
        
        # Set up the assumed position
        assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)
        
        # Perform the sight reduction
        intercept, azimuth = calculate_intercept(
            observed_altitude, 
            celestial_body, 
            assumed_position, 
            observation_time,
            apply_refraction=apply_refraction,
            temperature=temperature,
            pressure=pressure,
            observer_height=observer_height,
            celestial_body_name=celestial_body_name,
            limb=limb
        )
        
        figs = []
        
        if plot_type in ['azimuth', 'both']:
            fig_az = create_azimuth_compass_plot(
                [azimuth], 
                labels=[f"{celestial_body_name.capitalize()}\nAz: {azimuth:.1f}°\nInt: {abs(intercept):.1f}{'T' if intercept > 0 else 'A'}"],
                title=f"Celestial Body Azimuth - {celestial_body_name.capitalize()}",
                show_labels=True,
                save_path=save_path + "_azimuth.png" if save_path else None,
                show_plot=False
            )
            figs.append(fig_az)
        
        if plot_type in ['line_of_position', 'both']:
            fig_lop = create_line_of_position_plot(
                intercept, 
                azimuth, 
                assumed_lat, 
                assumed_lon,
                title=f"Line of Position - {celestial_body_name.capitalize()}",
                save_path=save_path + "_lop.png" if save_path else None,
                show_plot=False
            )
            figs.append(fig_lop)
        
        return tuple(figs) if figs else None
        
    except ImportError:
        print("Plotting module not available. Install matplotlib to use visualization functions.")
        return None


def visualize_multiple_sights(sight_results, title="Multiple Sights Summary", save_path=None):
    """
    Visualize multiple sight reduction results together.
    
    Parameters:
    - sight_results: List of tuples (name, intercept, azimuth)
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    
    Returns:
    - Matplotlib figure object
    """
    try:
        from .plotting import create_sight_summary_plot
        return create_sight_summary_plot(
            sight_results,
            title=title,
            save_path=save_path,
            show_plot=False
        )
    except ImportError:
        print("Plotting module not available. Install matplotlib to use visualization functions.")
        return None