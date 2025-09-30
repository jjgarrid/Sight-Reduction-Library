"""
Almanac Integration Module for Celestial Navigation

This module provides functions for retrieving nautical almanac data using skyalmanac
and integrating it with the existing sight reduction functionality.
"""

from skyfield.api import load, N, S, E, W
from skyfield.data import hipparcos
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import numpy as np


class AlmanacInterface:
    """
    Interface class to access nautical almanac data using skyfield (which skyalmanac is based on).
    """
    
    def __init__(self):
        """Initialize the almanac interface."""
        self.ts = load.timescale()
        # Download or load the standard ephemeris file
        try:
            self.eph = load('de421.bsp')  # Standard solar system ephemeris
        except:
            # If de421.bsp is not available, try another one
            self.eph = load('de405.bsp')
        
        # Load star catalog for stellar navigation (only if needed)
        try:
            self.star_catalog = hipparcos.load_dataframe(load('hip_main.dat'))
        except:
            # hip_main.dat might need to be downloaded - skip for now
            self.star_catalog = None
    
    def get_sun_data(self, date_time: datetime) -> Dict[str, float]:
        """
        Get Sun's GHA and declination for a specific date and time.
        
        Parameters:
        - date_time: The date and time for which to get Sun data
        
        Returns:
        - Dictionary with GHA, declination, and other relevant data
        """
        t = self.ts.utc(date_time.year, date_time.month, date_time.day, 
                        date_time.hour, date_time.minute, date_time.second)
        
        sun = self.eph['sun']
        earth = self.eph['earth']
        
        # Calculate apparent position of the Sun
        astrometric = earth.at(t).observe(sun)
        ra_apparent, dec_apparent, distance = astrometric.apparent().radec()
        
        # Calculate Greenwich Hour Angle (GHA)
        # GHA = Sidereal Time - Right Ascension
        gst = t.gast  # Greenwich Apparent Sidereal Time in hours
        ra_hours = ra_apparent._hours
        gha_hours = gst - ra_hours
        if gha_hours < 0:
            gha_hours += 24
        gha_degrees = gha_hours * 15  # Convert to degrees
        
        return {
            'GHA': gha_degrees,
            'declination': dec_apparent.degrees,
            'SD': 0.26667,  # Semi-diameter in degrees (approx. 16' for the Sun)
            'HP': 0.0  # Horizontal parallax (negligible for the Sun)
        }
    
    def get_moon_data(self, date_time: datetime) -> Dict[str, float]:
        """
        Get Moon's GHA, declination, semi-diameter, and horizontal parallax for a specific date and time.
        
        Parameters:
        - date_time: The date and time for which to get Moon data
        
        Returns:
        - Dictionary with GHA, declination, semi-diameter, and horizontal parallax
        """
        t = self.ts.utc(date_time.year, date_time.month, date_time.day, 
                        date_time.hour, date_time.minute, date_time.second)
        
        moon = self.eph['moon']
        earth = self.eph['earth']
        
        # Calculate apparent position of the Moon
        astrometric = earth.at(t).observe(moon)
        ra_apparent, dec_apparent, distance = astrometric.apparent().radec()
        
        # Calculate Greenwich Hour Angle (GHA)
        gst = t.gast  # Greenwich Apparent Sidereal Time in hours
        ra_hours = ra_apparent._hours
        gha_hours = gst - ra_hours
        if gha_hours < 0:
            gha_hours += 24
        gha_degrees = gha_hours * 15  # Convert to degrees
        
        # Calculate horizontal parallax (HP) from distance
        # HP = arcsin(earth_radius/distance) converted to degrees
        distance_au = distance.au
        earth_radius_au = 1 / 23455.0  # Earth's radius in AU
        hp_degrees = np.degrees(np.arcsin(earth_radius_au / distance_au))
        
        return {
            'GHA': gha_degrees,
            'declination': dec_apparent.degrees,
            'SD': 0.25278,  # Semi-diameter in degrees (around 15.17' on average)
            'HP': hp_degrees
        }
    
    def get_planet_data(self, planet_name: str, date_time: datetime) -> Dict[str, float]:
        """
        Get GHA, declination, and other data for a planet.
        
        Parameters:
        - planet_name: Name of the planet (mercury, venus, mars, jupiter, saturn)
        - date_time: The date and time for which to get planet data
        
        Returns:
        - Dictionary with GHA, declination, and other relevant data
        """
        planet_name = planet_name.lower()
        
        # Use Skyfield's get_body function, similar to what we use in main sight_reduction.py
        t = self.ts.utc(date_time.year, date_time.month, date_time.day, 
                        date_time.hour, date_time.minute, date_time.second)
        
        # Use get_body function for planets like in the main code
        try:
            from skyfield.api import get_body
            planet = get_body(planet_name, t)
            earth = self.eph['earth']
            
            # Calculate apparent position of the planet from Earth
            astrometric = earth.at(t).observe(planet)
            ra_apparent, dec_apparent, distance = astrometric.apparent().radec()
        except Exception:
            # If get_body fails, fall back to ephemeris approach
            planet_map = {
                'mercury': 199,  # Mercury barycenter
                'venus': 299,    # Venus barycenter
                'mars': 499,     # Mars barycenter
                'jupiter': 5,    # Jupiter barycenter
                'saturn': 6      # Saturn barycenter
            }
            
            if planet_name not in planet_map:
                raise ValueError(f"Planet {planet_name} not supported")
            
            planet = self.eph[planet_map[planet_name]]
            earth = self.eph['earth']
            
            # Calculate apparent position of the planet
            astrometric = earth.at(t).observe(planet)
            ra_apparent, dec_apparent, distance = astrometric.apparent().radec()
        
        # Calculate Greenwich Hour Angle (GHA)
        gst = t.gast  # Greenwich Apparent Sidereal Time in hours
        ra_hours = ra_apparent._hours
        gha_hours = gst - ra_hours
        if gha_hours < 0:
            gha_hours += 24
        gha_degrees = gha_hours * 15  # Convert to degrees
        
        # For planets, SD and HP vary significantly with position
        # Use approximate values or calculate them based on distance
        distance_au = distance.au
        earth_radius_au = 1 / 23455.0  # Earth's radius in AU
        hp_degrees = np.degrees(np.arcsin(earth_radius_au / distance_au))
        
        # Semi-diameter is usually negligible for planets but varies based on distance
        # Approximate values (in arcminutes) from the Nautical Almanac
        sd_map = {
            'mercury': 3.0 / 60,  # 3 arcminutes converted to degrees
            'venus': 16.0 / 60,   # 16 arcminutes
            'mars': 4.0 / 60,     # 4 arcminutes
            'jupiter': 10.0 / 60, # 10 arcminutes
            'saturn': 8.0 / 60    # 8 arcminutes (not including rings)
        }
        
        return {
            'GHA': gha_degrees,
            'declination': dec_apparent.degrees,
            'SD': sd_map.get(planet_name, 0.0),
            'HP': hp_degrees
        }
    
    def get_star_data(self, star_name: str, date_time: datetime) -> Dict[str, float]:
        """
        Get GHA and declination for a star.
        
        Parameters:
        - star_name: Name of the star
        - date_time: The date and time for which to get star data
        
        Returns:
        - Dictionary with GHA, declination, and other relevant data
        """
        # Find the star in the catalog
        # For simplicity, we use some common navigational stars
        # In a real implementation, you'd look up proper motion-corrected positions
        star_names = {
            'sirius': {'ra_deg': 101.287155, 'dec_deg': -16.716108},
            'canopus': {'ra_deg': 95.987600, 'dec_deg': -52.695667},
            'arcturus': {'ra_deg': 213.915300, 'dec_deg': 19.182507},
            'rigel': {'ra_deg': 78.634467, 'dec_deg': -8.201638},
            'procyon': {'ra_deg': 114.825958, 'dec_deg': 5.224950},
            'vega': {'ra_deg': 279.234733, 'dec_deg': 38.783689},
            'capella': {'ra_deg': 79.172327, 'dec_deg': 45.997958},
            'rigel_kentaurus_a': {'ra_deg': 219.902077, 'dec_deg': -60.833956},
            'altair': {'ra_deg': 297.695827, 'dec_deg': 8.868330},
            'acrux': {'ra_deg': 186.650667, 'dec_deg': -63.099028},
            'aldebaran': {'ra_deg': 68.980183, 'dec_deg': 16.509303},
            'spica': {'ra_deg': 201.298300, 'dec_deg': -11.161339},
            'antares': {'ra_deg': 247.352000, 'dec_deg': -26.431997},
            'pollux': {'ra_deg': 116.328942, 'dec_deg': 28.026183},
            'deneb': {'ra_deg': 310.357979, 'dec_deg': 45.280339}
        }
        
        if star_name.lower() not in star_names:
            raise ValueError(f"Star {star_name} not in the common navigational stars list")
        
        star_info = star_names[star_name.lower()]
        
        # Calculate GHA from Aries (sidereal time)
        t = self.ts.utc(date_time.year, date_time.month, date_time.day, 
                        date_time.hour, date_time.minute, date_time.second)
        
        # Calculate sidereal time (Right Ascension of Aries)
        gst = t.gast  # Greenwich Apparent Sidereal Time in hours
        gst_degrees = gst * 15  # Convert to degrees
        
        # Calculate GHA of the star: GHA Aries + SHA (or in this case, GHA = GAST - RA)
        ra_degrees = star_info['ra_deg']
        gha_degrees = gst_degrees - ra_degrees
        if gha_degrees < 0:
            gha_degrees += 360
        
        return {
            'GHA': gha_degrees,
            'declination': star_info['dec_deg'],
            'SHA': 360 - ra_degrees if ra_degrees > 0 else -ra_degrees,  # Sidereal Hour Angle
            'SD': 0.0,  # Stars are point sources, no semi-diameter
            'HP': 0.0   # Stars have negligible horizontal parallax
        }
    
    def get_all_body_data(self, date_time: datetime) -> Dict[str, Dict[str, float]]:
        """
        Get data for all celestial bodies at once.
        
        Parameters:
        - date_time: The date and time for which to get data
        
        Returns:
        - Dictionary with data for all supported celestial bodies
        """
        data = {}
        
        # Get data for Sun
        data['sun'] = self.get_sun_data(date_time)
        
        # Get data for Moon
        data['moon'] = self.get_moon_data(date_time)
        
        # Get data for planets
        for planet in ['venus', 'mars', 'jupiter', 'saturn']:
            try:
                data[planet] = self.get_planet_data(planet, date_time)
            except Exception:
                # Some planets might not be available in certain ephemeris files
                pass
        
        # Get data for some key stars
        for star in ['sirius', 'canopus', 'arcturus', 'vega', 'capella', 'rigel_kentaurus_a', 'altair', 'deneb']:
            try:
                data[star] = self.get_star_data(star, date_time)
            except Exception:
                # Skip stars that are not in the list
                pass
        
        return data


# Functions that integrate with the problem generation
def get_celestial_body_almanac_data(body_name: str, date_time: datetime, navigation_mode: str = 'marine') -> Dict[str, float]:
    """
    Get almanac data for a specific celestial body at a specific date/time.
    
    Parameters:
    - body_name: Name of the celestial body
    - date_time: The date and time for which to get data
    - navigation_mode: Navigation mode ('marine' or 'aviation') to determine data source
    
    Returns:
    - Dictionary with almanac data for the celestial body
    """
    if navigation_mode == 'aviation':
        # Use aviation-specific almanac
        from .aviation_almanac import get_aviation_celestial_body_data
        return get_aviation_celestial_body_data(body_name, date_time)
    else:
        # Use traditional marine almanac
        almanac = AlmanacInterface()
        
        body_name_lower = body_name.lower()
        
        if body_name_lower == 'sun':
            return almanac.get_sun_data(date_time)
        elif body_name_lower == 'moon':
            return almanac.get_moon_data(date_time)
        elif body_name_lower in ['mercury', 'venus', 'mars', 'jupiter', 'saturn']:
            return almanac.get_planet_data(body_name_lower, date_time)
        else:
            # Assume it's a star
            return almanac.get_star_data(body_name_lower, date_time)


def get_hourly_almanac_data(body_name: str, date: datetime, hours: int = 24) -> pd.DataFrame:
    """
    Get hourly almanac data for a celestial body for a full day.
    
    Parameters:
    - body_name: Name of the celestial body
    - date: The date for which to get hourly data
    - hours: Number of hours of data to generate (default 24)
    
    Returns:
    - Pandas DataFrame with hourly GHA and declination data
    """
    almanac = AlmanacInterface()
    
    hourly_data = []
    
    for hour in range(hours):
        hour_datetime = date.replace(hour=hour, minute=0, second=0)
        data = get_celestial_body_almanac_data(body_name, hour_datetime)
        
        hourly_data.append({
            'time': hour_datetime,
            'GHA': data['GHA'],
            'declination': data['declination'],
            'SD': data.get('SD', 0.0),
            'HP': data.get('HP', 0.0),
        })
    
    return pd.DataFrame(hourly_data)