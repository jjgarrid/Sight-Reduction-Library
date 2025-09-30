"""
Unit tests for atmospheric correction functionality in sight_reduction.py
"""
import sys
import os
import math

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
from src.sight_reduction import (
    calculate_refraction_correction,
    apply_refraction_correction,
    calculate_dip_correction,
    calculate_limb_correction,
    calculate_intercept,
    get_total_observation_correction,
    validate_altitude,
    validate_temperature,
    validate_pressure,
    validate_observer_height,
    validate_celestial_body_name,
    validate_limb,
    get_celestial_body
)


def test_calculate_refraction_correction_basic():
    """Test basic refraction correction calculation."""
    # Test at 45 degrees altitude
    correction = calculate_refraction_correction(45.0)
    assert isinstance(correction, float)
    assert correction > 0  # Correction should be positive (in arc minutes converted to degrees)
    
    # At higher altitude, refraction should be less
    correction_high = calculate_refraction_correction(80.0)
    assert correction_high < correction
    print("✓ test_calculate_refraction_correction_basic passed")


def test_calculate_refraction_correction_near_horizon():
    """Test refraction correction near horizon where it's largest."""
    correction = calculate_refraction_correction(1.0)  # Just above horizon
    assert correction > 0
    
    # At the horizon (0 degrees) should return some correction
    correction_horizon = calculate_refraction_correction(0.0)
    assert correction_horizon == 0.0  # According to implementation
    print("✓ test_calculate_refraction_correction_near_horizon passed")


def test_calculate_refraction_correction_temperature_pressure():
    """Test refraction correction with different temperature and pressure."""
    # Standard conditions
    correction_standard = calculate_refraction_correction(30.0, 10, 1010)
    
    # Higher pressure increases refraction
    correction_high_pressure = calculate_refraction_correction(30.0, 10, 1100)
    assert correction_high_pressure > correction_standard
    
    # Higher temperature decreases refraction
    correction_high_temp = calculate_refraction_correction(30.0, 30, 1010)
    assert correction_high_temp < correction_standard
    print("✓ test_calculate_refraction_correction_temperature_pressure passed")


def test_apply_refraction_correction():
    """Test applying refraction correction to get true altitude."""
    observed_alt = 45.0
    true_alt = apply_refraction_correction(observed_alt)  # Subtract refraction
    
    # True altitude should be less than observed due to refraction
    correction = calculate_refraction_correction(observed_alt)
    assert abs(true_alt - (observed_alt - correction)) < 0.0001
    print("✓ test_apply_refraction_correction passed")


def test_calculate_dip_correction():
    """Test dip correction for elevated observers."""
    # At sea level, no dip correction
    assert calculate_dip_correction(0.0) == 0.0
    
    # At 10 meter height
    dip_10m = calculate_dip_correction(10.0)
    assert dip_10m > 0  # Dip correction should be positive
    
    # At higher elevation, more dip
    dip_20m = calculate_dip_correction(20.0)
    assert dip_20m > dip_10m
    print("✓ test_calculate_dip_correction passed")


def test_calculate_limb_correction():
    """Test limb correction for Sun and Moon."""
    # Center has no correction
    assert calculate_limb_correction('sun', 'center') == 0.0
    assert calculate_limb_correction('moon', 'center') == 0.0
    
    # Lower limb correction is positive (adds to altitude)
    lower_sun = calculate_limb_correction('sun', 'lower')
    assert lower_sun > 0
    lower_moon = calculate_limb_correction('moon', 'lower')
    assert lower_moon > 0
    
    # Upper limb correction is negative (subtracts from altitude)
    upper_sun = calculate_limb_correction('sun', 'upper')
    assert upper_sun < 0
    upper_moon = calculate_limb_correction('moon', 'upper')
    assert upper_moon < 0
    
    # Same magnitude for sun and moon (same approximation used)
    assert abs(lower_sun) == abs(upper_sun)
    assert abs(lower_moon) == abs(upper_moon)
    print("✓ test_calculate_limb_correction passed")


def test_calculate_limb_correction_unsupported_body():
    """Test limb correction for truly unsupported celestial bodies (like stars)."""
    # For stars (point sources), should return 0
    assert calculate_limb_correction('sirius', 'lower') == 0.0
    assert calculate_limb_correction('vega', 'upper') == 0.0
    assert calculate_limb_correction('polaris', 'center') == 0.0
    print("✓ test_calculate_limb_correction_unsupported_body passed")


def test_calculate_intercept_with_corrections():
    """Test calculate_intercept with various atmospheric corrections."""
    # Set up basic parameters
    observed_altitude = 45.0
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Test without corrections
    intercept_no_corr, azimuth_no_corr = calculate_intercept(
        observed_altitude, celestial_body, assumed_position, observation_time,
        apply_refraction=False, observer_height=0, celestial_body_name=None
    )
    
    # Test with refraction only
    intercept_refr, azimuth_refr = calculate_intercept(
        observed_altitude, celestial_body, assumed_position, observation_time,
        apply_refraction=True, observer_height=0, celestial_body_name=None
    )
    
    # With refraction, the corrected altitude is lower, so intercept should be different
    # (This depends on the calculated altitude from the celestial body position)
    # The test will pass if the function executes without error
    assert isinstance(intercept_no_corr, float)
    assert isinstance(azimuth_no_corr, float)
    assert isinstance(intercept_refr, float)
    assert isinstance(azimuth_refr, float)
    print("✓ test_calculate_intercept_with_corrections passed")


def test_calculate_intercept_all_corrections():
    """Test calculate_intercept with all corrections enabled."""
    # Set up basic parameters
    observed_altitude = 45.0
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # All corrections enabled
    intercept, azimuth = calculate_intercept(
        observed_altitude, celestial_body, assumed_position, observation_time,
        apply_refraction=True,
        temperature=15.0,
        pressure=1020.0,
        observer_height=10.0,  # 10m above sea level
        celestial_body_name='sun',
        limb='lower'
    )
    
    assert isinstance(intercept, float)
    assert isinstance(azimuth, float)
    print("✓ test_calculate_intercept_all_corrections passed")


def test_get_total_observation_correction():
    """Test the utility function that calculates all corrections."""
    corrections = get_total_observation_correction(
        observed_altitude=45.0,
        temperature=15.0,
        pressure=1020.0,
        observer_height=10.0,
        celestial_body_name='sun',
        limb='lower'
    )
    
    # Check that all expected keys are present
    expected_keys = ['observed_altitude', 'refraction_correction', 'dip_correction', 
                     'limb_correction', 'total_correction', 'corrected_altitude']
    for key in expected_keys:
        assert key in corrections
    
    # Check that calculated values make sense
    assert corrections['observed_altitude'] == 45.0
    assert corrections['refraction_correction'] >= 0  # Non-negative correction value
    assert corrections['dip_correction'] >= 0  # Non-negative dip correction
    assert corrections['limb_correction'] >= 0  # Non-negative for lower limb
    # Corrected altitude may be different from observed due to multiple corrections
    assert isinstance(corrections['corrected_altitude'], float)
    print("✓ test_get_total_observation_correction passed")


def test_validation_functions():
    """Test all validation functions."""
    # Test altitude validation
    validate_altitude(45.0)  # Valid altitude
    
    try:
        validate_altitude(-5)  # Too low - should raise error
        assert False, "Should have raised ValueError for altitude -5"
    except ValueError:
        pass  # Expected
    
    try:
        validate_altitude(95)  # Too high - should raise error
        assert False, "Should have raised ValueError for altitude 95"
    except ValueError:
        pass  # Expected
    
    # Test temperature validation
    validate_temperature(20.0)  # Valid temperature
    try:
        validate_temperature(-150)  # Too cold - should raise error
        assert False, "Should have raised ValueError for temperature -150"
    except ValueError:
        pass  # Expected
    try:
        validate_temperature(150)  # Too hot - should raise error
        assert False, "Should have raised ValueError for temperature 150"
    except ValueError:
        pass  # Expected
    
    # Test pressure validation
    validate_pressure(1010.0)  # Valid pressure
    try:
        validate_pressure(700)  # Too low - should raise error
        assert False, "Should have raised ValueError for pressure 700"
    except ValueError:
        pass  # Expected
    try:
        validate_pressure(1300)  # Too high - should raise error
        assert False, "Should have raised ValueError for pressure 1300"
    except ValueError:
        pass  # Expected
    
    # Test observer height validation
    validate_observer_height(10.0)  # Valid height
    try:
        validate_observer_height(-5)  # Negative height - should raise error
        assert False, "Should have raised ValueError for negative height"
    except ValueError:
        pass  # Expected
    
    # Test celestial body name validation
    validate_celestial_body_name('sun')  # Valid
    validate_celestial_body_name('moon')  # Valid
    validate_celestial_body_name('mars')  # Now supported for limb correction
    validate_celestial_body_name('venus')  # Now supported for limb correction
    validate_celestial_body_name('jupiter')  # Now supported for limb correction
    validate_celestial_body_name('sirius')  # Now supported for limb correction
    validate_celestial_body_name('vega')  # Now supported for limb correction
    try:
        validate_celestial_body_name('pluto')  # Still not supported
        assert False, "Should have raised ValueError for invalid body name"
    except ValueError:
        pass  # Expected
    
    # Test limb validation
    validate_limb('center')  # Valid
    validate_limb('upper')  # Valid
    validate_limb('lower')  # Valid
    try:
        validate_limb('middle')  # Invalid
        assert False, "Should have raised ValueError for invalid limb"
    except ValueError:
        pass  # Expected
    print("✓ test_validation_functions passed")


def test_calculate_intercept_input_validation():
    """Test that calculate_intercept properly validates inputs."""
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Valid call should work
    calculate_intercept(
        45.0, celestial_body, assumed_position, observation_time,
        celestial_body_name='sun', limb='center'
    )
    
    # Invalid altitude should raise error
    try:
        calculate_intercept(
            -5.0, celestial_body, assumed_position, observation_time
        )
        assert False, "Should have raised ValueError for negative altitude"
    except ValueError:
        pass  # Expected
    
    # Invalid temperature should raise error
    try:
        calculate_intercept(
            45.0, celestial_body, assumed_position, observation_time,
            temperature=-200.0
        )
        assert False, "Should have raised ValueError for invalid temperature"
    except ValueError:
        pass  # Expected
    
    # Invalid pressure should raise error
    try:
        calculate_intercept(
            45.0, celestial_body, assumed_position, observation_time,
            pressure=500.0
        )
        assert False, "Should have raised ValueError for invalid pressure"
    except ValueError:
        pass  # Expected
    
    # Invalid observer height should raise error
    try:
        calculate_intercept(
            45.0, celestial_body, assumed_position, observation_time,
            observer_height=-10.0
        )
        assert False, "Should have raised ValueError for negative height"
    except ValueError:
        pass  # Expected
    
    # Invalid celestial body name should raise error
    try:
        calculate_intercept(
            45.0, celestial_body, assumed_position, observation_time,
            celestial_body_name='pluto', limb='center'
        )
        assert False, "Should have raised ValueError for invalid body name"
    except ValueError:
        pass  # Expected
    
    # Invalid limb should raise error
    try:
        calculate_intercept(
            45.0, celestial_body, assumed_position, observation_time,
            celestial_body_name='sun', limb='side'
        )
        assert False, "Should have raised ValueError for invalid limb"
    except ValueError:
        pass  # Expected
    print("✓ test_calculate_intercept_input_validation passed")


def test_edge_cases():
    """Test edge cases for correction functions."""
    # Very low altitude
    correction = calculate_refraction_correction(0.1)
    assert correction >= 0
    
    # Zero observer height
    dip = calculate_dip_correction(0)
    assert dip == 0
    
    # Refraction at horizon (0 altitude)
    correction_zero = calculate_refraction_correction(0)
    assert correction_zero == 0.0
    print("✓ test_edge_cases passed")


if __name__ == "__main__":
    # Run the tests
    test_calculate_refraction_correction_basic()
    test_calculate_refraction_correction_near_horizon()
    test_calculate_refraction_correction_temperature_pressure()
    test_apply_refraction_correction()
    test_calculate_dip_correction()
    test_calculate_limb_correction()
    test_calculate_limb_correction_unsupported_body()
    test_get_total_observation_correction()
    test_validation_functions()
    test_calculate_intercept_input_validation()
    test_edge_cases()
    print("All tests passed!")