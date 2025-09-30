"""
Aviation Almanac Module for Celestial Navigation

This module provides functions for retrieving aviation-specific almanac data 
and using Sight Reduction Tables for Air Navigation (e.g., Pub. No. 249).
"""

from datetime import datetime
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


class AviationAlmanacInterface:
    """
    Interface class to access aviation-specific almanac data and tables.
    Supports both Air Almanac and Sight Reduction Tables for Air Navigation.
    """
    
    def __init__(self):
        """Initialize the aviation almanac interface."""
        # For now, we'll use the same ephemeris as the marine almanac
        # In a full implementation, we'd have aviation-specific tables
        
        # Aviation almanac data will be structured differently
        # We'll simulate aviation tables like Pub. No. 249
        self.aviation_tables = self._generate_aviation_tables()
    
    def _generate_aviation_tables(self) -> Dict:
        """
        Generate simulated aviation tables data.
        In a real implementation, this would load actual aviation almanac data.
        """
        # Create simplified aviation tables based on Pub. No. 249 structure
        # These would normally include precomputed altitude and azimuth values
        # based on LHA, declination, and assumed latitude
        
        tables = {}
        
        # Simulate Volume 1 of Pub. No. 249 (selected stars for 2025)
        # These are placeholder values that would be replaced with actual data
        tables['vol1_stars'] = {
            'sirius': {
                'SHA': 258.96,  # Sidereal Hour Angle
                'declination': -16.72,  # Declination
                'epoch_year': 2025,
                'magnitude': -1.46
            },
            'canopus': {
                'SHA': 263.89,
                'declination': -52.70,
                'epoch_year': 2025,
                'magnitude': -0.74
            },
            'arcturus': {
                'SHA': 145.86,
                'declination': 19.18,
                'epoch_year': 2025,
                'magnitude': -0.05
            },
            'vega': {
                'SHA': 80.76,
                'declination': 38.78,
                'epoch_year': 2025,
                'magnitude': 0.03
            },
            'capella': {
                'SHA': 280.50,
                'declination': 45.99,
                'epoch_year': 2025,
                'magnitude': 0.08
            }
        }
        
        # Simulate selected stars for other volumes
        tables['vol2_3_stars'] = []
        for star_name in ['rigel', 'procyon', 'rigel_kentaurus_a', 'altair', 'acrux']:
            tables['vol2_3_stars'].append({
                'name': star_name,
                'SHA': np.random.uniform(0, 360),  # Placeholder
                'declination': np.random.uniform(-90, 90),  # Placeholder
                'epoch_year': 2025
            })
        
        return tables
    
    def get_star_data_for_aviation(self, star_name: str) -> Dict:
        """
        Get star data formatted for aviation use.
        
        Parameters:
        - star_name: Name of the star
        
        Returns:
        - Dictionary with aviation-formatted star data
        """
        star_lower = star_name.lower()
        
        # Check Vol 1 first (most important stars)
        if star_lower in self.aviation_tables['vol1_stars']:
            return self.aviation_tables['vol1_stars'][star_lower]
        
        # Check other volumes
        for star_data in self.aviation_tables['vol2_3_stars']:
            if star_data['name'].lower() == star_lower:
                return star_data
        
        raise ValueError(f"Star {star_name} not found in aviation almanac")
    
    def lookup_altitude_azimuth(self, assumed_lat: float, lha: float, declination: float, 
                               table_volume: int = 1) -> Dict[str, float]:
        """
        Look up altitude and azimuth from aviation tables.
        
        Parameters:
        - assumed_lat: Assumed latitude (0° to 90°, positive for North)
        - lha: Local Hour Angle (0° to 359°)
        - declination: Declination of the celestial body (-90° to +90°)
        - table_volume: Which volume of Pub. No. 249 (1, 2, or 3)
        
        Returns:
        - Dictionary with computed altitude, azimuth and corrections
        """
        # This is a simplified implementation of aviation table lookup
        # In a real implementation, this would use the actual Pub. No. 249 tables
        
        # Normalize inputs
        assumed_lat = max(-89.9, min(89.9, assumed_lat))  # Keep away from poles
        lha = lha % 360  # Normalize LHA to 0-360
        declination = max(-89.9, min(89.9, declination))
        
        # Perform sight reduction calculation (similar to marine but optimized for aviation)
        # The formula is: sin(Hc) = sin(dec)·sin(lat) + cos(dec)·cos(lat)·cos(LHA)
        # and tan(Z) = sin(LHA) / (cos(LHA)·sin(lat) - tan(dec)·cos(lat))
        
        dec_rad = np.radians(declination)
        lat_rad = np.radians(assumed_lat)
        lha_rad = np.radians(lha)
        
        # Calculate computed altitude (Hc)
        sin_hc = (np.sin(dec_rad) * np.sin(lat_rad) + 
                  np.cos(dec_rad) * np.cos(lat_rad) * np.cos(lha_rad))
        hc_rad = np.arcsin(max(-1, min(1, sin_hc)))  # Clamp to valid range
        hc_degrees = np.degrees(hc_rad)
        
        # Calculate azimuth (Z)
        numerator = np.sin(lha_rad)
        denominator = np.cos(lha_rad) * np.sin(lat_rad) - np.tan(dec_rad) * np.cos(lat_rad)
        
        if abs(denominator) < 1e-10:  # Avoid division by zero
            if declination > assumed_lat:
                z_degrees = 0.0  # North
            else:
                z_degrees = 180.0  # South
        else:
            z_rad = np.arctan2(numerator, denominator)
            z_degrees = np.degrees(z_rad)
        
        # Convert azimuth to 0-360 range
        if z_degrees < 0:
            z_degrees += 360
        
        # Calculate table corrections (similar to actual aviation tables)
        # These would normally come from precomputed tables
        delta_correction = 0.0  # Simplified for this implementation
        if table_volume == 1:
            # Volume 1 is for first choice stars, has more precise tables
            delta_correction = np.sin(np.radians(declination - assumed_lat)) * 10  # Simplified
        else:
            # Other volumes have slightly different corrections
            delta_correction = np.sin(np.radians(declination - assumed_lat)) * 5  # Simplified
        
        return {
            'computed_altitude': hc_degrees,
            'azimuth': z_degrees,
            'delta_correction': delta_correction,
            'table_volume': table_volume,
            'intercept_correction': delta_correction  # For plotting the line of position
        }
    
    def get_aviation_star_data(self, date_time: datetime, star_name: str) -> Dict[str, float]:
        """
        Get aviation-specific star data for a specific date and time.
        
        Parameters:
        - date_time: The date and time for which to get star data
        - star_name: Name of the star
        
        Returns:
        - Dictionary with aviation-specific star data
        """
        # Get base star data from aviation tables
        star_data = self.get_star_data_for_aviation(star_name)
        
        # Calculate GHA from Aries (sidereal time)
        # This is similar to the marine calculation but may be optimized for aviation
        gst_degrees = self._calculate_gst(date_time)
        
        # Calculate GHA of the star: GHA Aries + SHA
        sha_degrees = star_data['SHA']
        gha_degrees = gst_degrees - sha_degrees
        if gha_degrees < 0:
            gha_degrees += 360
        
        # Add proper motion corrections for aviation precision
        # Convert astropy Time object to get the year
        if hasattr(date_time, 'datetime'):
            year = date_time.datetime.year
        else:
            from astropy.time import Time
            converted_time = Time(date_time)
            year = converted_time.datetime.year
        
        years_since_epoch = year - star_data['epoch_year']
        # Simplified proper motion correction
        proper_motion_corr = years_since_epoch * 0.0001  # degrees per year
        
        return {
            'GHA': gha_degrees + proper_motion_corr,
            'declination': star_data['declination'] + proper_motion_corr,
            'SHA': sha_degrees,
            'magnitude': star_data.get('magnitude', 2.0),
            'epoch_year': star_data['epoch_year']
        }
    
    def _calculate_gst(self, date_time: datetime) -> float:
        """
        Calculate Greenwich Sidereal Time for a given date and time.
        This is a simplified calculation for demonstration purposes.
        """
        # Convert datetime to Astropy Time if needed
        if not hasattr(date_time, 'ut1'):
            from astropy.time import Time
            astropy_time = Time(date_time)
        else:
            astropy_time = date_time
        
        # Use astropy's built-in GST calculation
        gst_hours = astropy_time.sidereal_time('mean', 'greenwich').hour
        gst_degrees = gst_hours * 15.0  # Convert hours to degrees
        return gst_degrees
        
        # Calculate GST in degrees
        # 280.46061837 + 360.98564736629 * days_since_j2000 (degrees)
        gst_degrees = (280.46061837 + 360.98564736629 * days_since_j2000) % 360
        
        # Adjust for the current time of day
        gst_degrees += (date_time.hour + date_time.minute / 60.0 + date_time.second / 3600.0) * 15.04106899  # Sidereal rate
        
        return gst_degrees % 360


def get_aviation_celestial_body_data(body_name: str, date_time: datetime) -> Dict[str, float]:
    """
    Get aviation almanac data for a specific celestial body at a specific date/time.
    This function provides an interface similar to the marine almanac function
    but optimized for aviation use.
    
    Parameters:
    - body_name: Name of the celestial body
    - date_time: The date and time for which to get data
    
    Returns:
    - Dictionary with aviation almanac data for the celestial body
    """
    aviation_almanac = AviationAlmanacInterface()
    
    # Note: For now, we only support stars in aviation mode
    # Sun and planets would be added in a full implementation
    body_name_lower = body_name.lower()
    
    if body_name_lower in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']:
        # For now, fall back to marine almanac for solar system bodies
        # In a full implementation, aviation almanac would have all bodies
        from .almanac_integration import get_celestial_body_almanac_data
        
        # Convert astropy Time object to datetime if necessary for the marine almanac
        from astropy.time import Time
        if isinstance(date_time, Time):
            # It's an astropy Time object, convert to datetime
            date_time_converted = date_time.datetime
        else:
            # It's already a datetime object
            date_time_converted = date_time
            
        return get_celestial_body_almanac_data(body_name, date_time_converted)
    else:
        # Assume it's a star
        return aviation_almanac.get_aviation_star_data(date_time, body_name_lower)


def get_aviation_table_lookup(assumed_lat: float, lha: float, declination: float, 
                             table_volume: int = 1) -> Dict[str, float]:
    """
    Get altitude and azimuth lookup using aviation tables.
    
    Parameters:
    - assumed_lat: Assumed latitude (0° to 90°, positive for North)
    - lha: Local Hour Angle (0° to 359°)
    - declination: Declination of the celestial body (-90° to +90°)
    - table_volume: Which volume of Pub. No. 249 (1, 2, or 3)
    
    Returns:
    - Dictionary with computed altitude, azimuth and corrections
    """
    aviation_almanac = AviationAlmanacInterface()
    return aviation_almanac.lookup_altitude_azimuth(assumed_lat, lha, declination, table_volume)