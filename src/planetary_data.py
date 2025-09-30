"""
Planetary Data for Celestial Navigation

This module contains functions to get planetary positions for celestial navigation.
"""
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import get_body, EarthLocation, AltAz
from astropy.coordinates import SkyCoord

# Planetary data - approximate angular diameters and other characteristics
PLANETARY_DATA = {
    'mercury': {
        'angular_diameter': (3.0, 13.0),  # arcseconds range depending on distance
        'magnitude_range': (-2.4, 5.5),
        'angular_radius_avg': (3.0 + 13.0) / 2 / 3600,  # Convert to degrees
        'description': 'Closest planet to the Sun'
    },
    'venus': {
        'angular_diameter': (9.5, 68.0),  # arcseconds range
        'magnitude_range': (-4.9, -3.8),
        'angular_radius_avg': (9.5 + 68.0) / 2 / 3600,  # Convert to degrees
        'description': 'Second planet from the Sun, brightest planet'
    },
    'mars': {
        'angular_diameter': (3.5, 25.1),  # arcseconds range
        'magnitude_range': (-2.9, 1.8),
        'angular_radius_avg': (3.5 + 25.1) / 2 / 3600,  # Convert to degrees
        'description': 'Fourth planet from the Sun, the Red Planet'
    },
    'jupiter': {
        'angular_diameter': (29.8, 50.1),  # arcseconds range
        'magnitude_range': (-2.9, -1.6),
        'angular_radius_avg': (29.8 + 50.1) / 2 / 3600,  # Convert to degrees
        'description': 'Largest planet, fifth from the Sun'
    },
    'saturn': {
        'angular_diameter': (14.5, 20.1),  # arcseconds range
        'magnitude_range': (0.7, -0.2),
        'angular_radius_avg': (14.5 + 20.1) / 2 / 3600,  # Convert to degrees (including rings)
        'description': 'Sixth planet, famous for its rings'
    }
}

def get_planet_position(planet_name, observation_time):
    """
    Get the position of a planet at a specific time.
    
    Parameters:
    - planet_name: Name of the planet (case-insensitive)
    - observation_time: Astropy Time object for the observation time
    
    Returns:
    - SkyCoord object with the planet's coordinates
    """
    planet_name_lower = planet_name.lower()
    
    if planet_name_lower not in PLANETARY_DATA:
        raise ValueError(f"Planet '{planet_name}' is not supported for navigation")
    
    return get_body(planet_name_lower, observation_time)


def get_planet_angular_radius(planet_name):
    """
    Get the average angular radius of a planet in degrees.
    
    Parameters:
    - planet_name: Name of the planet (case-insensitive)
    
    Returns:
    - Average angular radius in degrees
    """
    planet_name_lower = planet_name.lower()
    
    if planet_name_lower in PLANETARY_DATA:
        return PLANETARY_DATA[planet_name_lower]['angular_radius_avg']
    
    return 0.0  # Return 0 for unsupported planets


def get_planet_info(planet_name):
    """
    Get detailed information about a planet.
    
    Parameters:
    - planet_name: Name of the planet (case-insensitive)
    
    Returns:
    - Dictionary with planet information, or None if not found
    """
    planet_name_lower = planet_name.lower()
    
    if planet_name_lower in PLANETARY_DATA:
        return PLANETARY_DATA[planet_name_lower]
    
    return None


def list_supported_planets():
    """
    Get a list of all supported planets.
    
    Returns:
    - List of planet names
    """
    return list(PLANETARY_DATA.keys())