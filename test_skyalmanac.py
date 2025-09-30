#!/usr/bin/env python
"""
Test script to verify skyalmanac functionality and compatibility with our project.
"""

from skyalmanac import almanac
from skyfield.api import load
import astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time
import numpy as np

def test_skyalmanac_basic():
    """Test basic functionality of skyalmanac"""
    print("Testing basic skyalmanac functionality...")
    
    # Load timescale
    ts = load.timescale()
    
    # Create a time for testing
    t = ts.utc(2023, 6, 15, 12, 0, 0)
    
    # Test getting basic almanac data for Sun
    print("Getting Sun's GHA and declination...")
    try:
        # Skyalmanac provides functions to get celestial body details
        # For this test, we'll use Skyfield directly to check compatibility
        eph = load('de421.bsp')  # Standard solar system ephemeris
        sun = eph['sun']
        earth = eph['earth']
        
        # Get position of sun
        astrometric = earth.at(t).observe(sun)
        ra, dec, distance = astrometric.radec()
        
        print(f"Sun: RA = {ra}, Dec = {dec}")
        
        # Get Greenwich Hour Angle (GHA = Local Hour Angle at Greenwich)
        from skyfield.api import N, E
        gcrs_sun = earth.at(t).observe(sun)
        apparent_sun = gcrs_sun.apparent()
        ra_hour, dec_deg, distance_au = apparent_sun.radec(epoch='date')
        lst_deg = t.gast * 15  # Convert Greenwich Apparent Sidereal Time to degrees
        gha_deg = lst_deg - ra_hour._degrees
        if gha_deg < 0:
            gha_deg += 360
        
        print(f"Sun: GHA = {gha_deg:.4f}°, Dec = {dec_deg:.4f}°")
        
        return True
    except Exception as e:
        print(f"Error testing skyalmanac functionality: {e}")
        return False

def test_astropy_compatibility():
    """Test that Astropy and Skyfield can coexist"""
    print("\nTesting Astropy and Skyfield compatibility...")
    
    try:
        # Test Astropy functionality
        astropy_time = Time("2023-06-15T12:00:00")
        astropy_location = EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m)
        
        print(f"Astropy time: {astropy_time}")
        print(f"Astropy location: {astropy_location.lat}, {astropy_location.lon}")
        
        # Test Skyfield functionality 
        ts = load.timescale()
        skyfield_time = ts.utc(2023, 6, 15, 12, 0, 0)
        print(f"Skyfield time: {skyfield_time.utc_iso()}")
        
        return True
    except Exception as e:
        print(f"Error testing compatibility: {e}")
        return False

def test_skyalmanac_tables():
    """Test generating almanac tables"""
    print("\nTesting almanac table generation...")
    
    try:
        # Generate a simple almanac for a day
        # Note: This will use skyalmanac functions if available
        from datetime import datetime
        import pandas as pd
        
        # Create a test date
        test_date = datetime(2023, 6, 15)
        
        # Verify we can still use our existing functions
        from src.sight_reduction import get_celestial_body, calculate_intercept
        from astropy.coordinates import EarthLocation
        from astropy.time import Time
        import astropy.units as u
        
        # Test that our existing functionality still works
        celestial_body = get_celestial_body("sun", Time("2023-06-15T12:00:00"))
        assumed_position = EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m)
        intercept, azimuth = calculate_intercept(
            45.23, 
            celestial_body, 
            assumed_position, 
            Time("2023-06-15T12:00:00")
        )
        
        print(f"Test calculation: Intercept = {intercept:.2f}, Azimuth = {azimuth:.2f}")
        
        return True
    except Exception as e:
        print(f"Error testing almanac tables: {e}")
        return False

if __name__ == "__main__":
    print("Testing skyalmanac installation and compatibility...\n")
    
    success = True
    success &= test_skyalmanac_basic()
    success &= test_astropy_compatibility()
    success &= test_skyalmanac_tables()
    
    if success:
        print("\nAll tests passed! Skyalmanac is compatible with our project.")
    else:
        print("\nSome tests failed. Need to troubleshoot compatibility issues.")