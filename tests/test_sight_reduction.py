"""
Basic tests for the sight reduction module.
"""
import sys
import os
# Add the src directory to the path to import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pytest
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body, format_position


def test_calculate_intercept():
    """Test the calculate_intercept function with basic inputs."""
    observed_altitude = 45.0
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    intercept, azimuth = calculate_intercept(
        observed_altitude, 
        celestial_body, 
        assumed_position, 
        observation_time
    )
    
    # Verify that we get numeric results
    assert isinstance(intercept, float)
    assert isinstance(azimuth, float)
    assert 0 <= azimuth <= 360


def test_format_position():
    """Test the format_position function."""
    result = format_position(40.7128, -74.0060)
    assert "N" in result
    assert "W" in result
    assert "40°" in result
    assert "74°" in result


def test_get_celestial_body():
    """Test getting celestial bodies."""
    time = Time.now()
    
    sun = get_celestial_body("sun", time)
    assert sun is not None
    
    moon = get_celestial_body("moon", time)
    assert moon is not None
    
    star = get_celestial_body("star", time)  # This should return Polaris coordinates
    assert star is not None