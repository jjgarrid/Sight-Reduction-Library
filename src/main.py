#!/usr/bin/env python3
"""
Main script for sight reduction calculations in celestial navigation.

This script demonstrates how to perform sight reductions using the sight_reduction module.
"""
import sys
import os
# Add the parent directory to the path to import the sight_reduction module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body, format_position

# Import configuration
try:
    from config import (
        DEFAULT_OBSERVED_ALTITUDE,
        DEFAULT_CELESTIAL_BODY,
        DEFAULT_ASSUMED_LAT,
        DEFAULT_ASSUMED_LON
    )
except ImportError:
    # Use defaults if config is not available
    DEFAULT_OBSERVED_ALTITUDE = 45.23
    DEFAULT_CELESTIAL_BODY = "sun"
    DEFAULT_ASSUMED_LAT = 40.7128
    DEFAULT_ASSUMED_LON = -74.0060


def main():
    # Input data - using defaults from config if available
    observed_altitude = DEFAULT_OBSERVED_ALTITUDE  # Observed altitude of the celestial body (degrees)
    celestial_body_name = DEFAULT_CELESTIAL_BODY  # Specify 'sun' or 'moon' or use RA/Dec for stars
    assumed_lat = DEFAULT_ASSUMED_LAT  # Assumed latitude (degrees)
    assumed_lon = DEFAULT_ASSUMED_LON  # Assumed longitude (degrees)
    observation_time = Time.now()  # Observation time in UTC

    # Define the celestial body
    celestial_body = get_celestial_body(celestial_body_name, observation_time)

    # Assumed position of the observer
    assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

    # Perform sight reduction
    intercept, azimuth = calculate_intercept(observed_altitude, celestial_body, assumed_position, observation_time)

    # Format and display the results
    print(f"Observed Altitude: {observed_altitude:.2f}°")
    print(f"Assumed Position: {format_position(assumed_lat, assumed_lon)}")
    print(f"Intercept (difference in altitude): {abs(intercept):.2f} nautical miles")
    print(f"Direction of intercept: {'Toward' if intercept > 0 else 'Away from'} celestial body")
    print(f"Azimuth of Celestial Body: {azimuth:.2f}°")
    print(f"Observation Time: {observation_time.isot}")


if __name__ == "__main__":
    main()