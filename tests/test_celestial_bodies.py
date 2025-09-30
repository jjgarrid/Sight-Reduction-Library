"""
Integration tests for celestial bodies support in sight reduction
"""
import sys
import os
import math

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import (
    calculate_intercept,
    get_celestial_body,
    calculate_limb_correction,
    validate_celestial_body_name
)


def test_get_celestial_body_planets():
    """Test that get_celestial_body works correctly with planets."""
    observation_time = Time("2023-06-15T12:00:00")
    
    # Test that planets can be retrieved
    planets = ["venus", "mars", "jupiter", "saturn"]
    for planet in planets:
        celestial_body = get_celestial_body(planet, observation_time)
        assert celestial_body is not None, f"Could not retrieve {planet}"
        
        # Verify it's a SkyCoord object
        from astropy.coordinates import SkyCoord
        assert isinstance(celestial_body, SkyCoord), f"{planet} should return a SkyCoord object"


def test_get_celestial_body_stars():
    """Test that get_celestial_body works correctly with stars."""
    observation_time = Time("2023-06-15T12:00:00")
    
    # Test that stars can be retrieved
    stars = ["sirius", "vega", "polaris", "aldebaran"]
    for star in stars:
        celestial_body = get_celestial_body(star, observation_time)
        assert celestial_body is not None, f"Could not retrieve {star}"
        
        # Verify it's a SkyCoord object
        from astropy.coordinates import SkyCoord
        assert isinstance(celestial_body, SkyCoord), f"{star} should return a SkyCoord object"


def test_calculate_intercept_planets():
    """Test calculate_intercept with planets."""
    observation_time = Time("2023-06-15T12:00:00")
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Test with Venus
    celestial_body = get_celestial_body("venus", observation_time)
    intercept, azimuth = calculate_intercept(
        observed_altitude=45.0,
        celestial_body=celestial_body,
        assumed_position=assumed_position,
        observation_time=observation_time,
        celestial_body_name="venus",
        limb="center"
    )
    
    assert isinstance(intercept, float), "Intercept should be float"
    assert isinstance(azimuth, float), "Azimuth should be float"
    assert 0 <= azimuth <= 360, "Azimuth should be between 0 and 360 degrees"


def test_calculate_intercept_stars():
    """Test calculate_intercept with stars."""
    observation_time = Time("2023-06-15T12:00:00")
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Test with Sirius
    celestial_body = get_celestial_body("sirius", observation_time)
    intercept, azimuth = calculate_intercept(
        observed_altitude=45.0,
        celestial_body=celestial_body,
        assumed_position=assumed_position,
        observation_time=observation_time,
        celestial_body_name="sirius",
        limb="center"
    )
    
    assert isinstance(intercept, float), "Intercept should be float"
    assert isinstance(azimuth, float), "Azimuth should be float"
    assert 0 <= azimuth <= 360, "Azimuth should be between 0 and 360 degrees"


def test_limb_correction_planets():
    """Test that planets have appropriate limb corrections."""
    # Venus should have a small but measurable limb correction
    venus_center = calculate_limb_correction("venus", "center")
    venus_lower = calculate_limb_correction("venus", "lower")
    venus_upper = calculate_limb_correction("venus", "upper")
    
    assert venus_center == 0.0, "Center limb correction should be 0"
    assert venus_lower > 0.0, "Lower limb correction for Venus should be positive"
    assert venus_upper < 0.0, "Upper limb correction for Venus should be negative"
    assert abs(venus_lower) == abs(venus_upper), "Upper and lower corrections should have same magnitude"
    
    # Jupiter should have a larger limb correction than Venus
    jupiter_lower = calculate_limb_correction("jupiter", "lower")
    assert abs(jupiter_lower) > abs(venus_lower), "Jupiter should have larger limb correction than Venus"
    
    # Stars should have no limb correction
    sirius_lower = calculate_limb_correction("sirius", "lower")
    sirius_upper = calculate_limb_correction("sirius", "upper")
    sirius_center = calculate_limb_correction("sirius", "center")
    
    assert sirius_lower == 0.0, "Stars should not have limb correction"
    assert sirius_upper == 0.0, "Stars should not have limb correction"
    assert sirius_center == 0.0, "Stars should not have limb correction"


def test_validate_celestial_body_name():
    """Test that validation works for new celestial bodies."""
    # These should not raise errors
    validate_celestial_body_name("venus")
    validate_celestial_body_name("mars")
    validate_celestial_body_name("jupiter")
    validate_celestial_body_name("saturn")
    validate_celestial_body_name("sirius")
    validate_celestial_body_name("vega")
    
    # This should raise an error
    with pytest.raises(ValueError):
        validate_celestial_body_name("pluto")  # Not in our supported list


def test_comprehensive_celestial_body_support():
    """Comprehensive test of new celestial body support."""
    observation_time = Time("2023-06-15T12:00:00")
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Test multiple celestial bodies
    test_cases = [
        ("sun", "Sun should work"),
        ("moon", "Moon should work"),
        ("venus", "Venus should work"),
        ("mars", "Mars should work"),
        ("jupiter", "Jupiter should work"),
        ("saturn", "Saturn should work"),
        ("sirius", "Sirius should work"),
        ("vega", "Vega should work"),
        ("polaris", "Polaris should work"),
    ]
    
    for body_name, description in test_cases:
        celestial_body = get_celestial_body(body_name, observation_time)
        assert celestial_body is not None, f"{description}: Could not retrieve celestial body"
        
        # Test with basic parameters
        intercept, azimuth = calculate_intercept(
            observed_altitude=45.0,
            celestial_body=celestial_body,
            assumed_position=assumed_position,
            observation_time=observation_time,
            celestial_body_name=body_name,
            limb="center"
        )
        
        assert isinstance(intercept, float), f"{description}: Intercept should be float"
        assert isinstance(azimuth, float), f"{description}: Azimuth should be float"
        assert 0 <= azimuth <= 360, f"{description}: Azimuth should be between 0 and 360 degrees"


if __name__ == "__main__":
    # Run the tests
    test_get_celestial_body_planets()
    test_get_celestial_body_stars()
    test_calculate_intercept_planets()
    test_calculate_intercept_stars()
    test_limb_correction_planets()
    test_validate_celestial_body_name()
    test_comprehensive_celestial_body_support()
    print("All integration tests passed!")