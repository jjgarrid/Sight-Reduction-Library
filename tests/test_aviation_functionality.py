"""
Test Suite for Aviation Sight Reduction Functionality

This module contains comprehensive tests for the aviation-specific
celestial navigation functionality implemented in the sight reduction library.
"""

import unittest
import math
import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import (
    calculate_intercept,
    get_total_observation_correction,
    calculate_refraction_correction,
    calculate_dip_correction,
    calculate_bubble_sextant_correction,
    calculate_movement_correction,
    apply_time_interval_correction,
    get_celestial_body
)
from src.problem_generator import generate_sight_reduction_problem
from src.aviation_almanac import (
    AviationAlmanacInterface, 
    get_aviation_celestial_body_data, 
    get_aviation_table_lookup
)


class TestAviationSightReduction(unittest.TestCase):
    """Test aviation-specific sight reduction functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Common test parameters
        self.observed_altitude = 45.0  # degrees
        self.observation_time = Time('2023-06-15T12:00:00')
        self.celestial_body_name = 'sun'
        self.assumed_lat = 40.0  # degrees
        self.assumed_lon = -74.0  # degrees
        self.assumed_position = EarthLocation(
            lat=self.assumed_lat*u.deg, 
            lon=self.assumed_lon*u.deg, 
            height=0*u.m
        )
        self.temperature = 15.0  # Celsius
        self.pressure = 1013.25  # hPa
        self.celestial_body = get_celestial_body(self.celestial_body_name, self.observation_time)
    
    def test_aviation_mode_selection(self):
        """Test that aviation mode is properly selected in calculate_intercept."""
        # Test marine mode (default)
        marine_intercept, marine_azimuth = calculate_intercept(
            self.observed_altitude,
            self.celestial_body,
            self.assumed_position,
            self.observation_time,
            navigation_mode='marine'
        )
        
        # Test aviation mode
        aviation_intercept, aviation_azimuth = calculate_intercept(
            self.observed_altitude,
            self.celestial_body,
            self.assumed_position,
            self.observation_time,
            navigation_mode='aviation'
        )
        
        # The results should be different due to different correction methods
        # In aviation mode, there's no dip correction when observer_height > 0
        # but other corrections might be applied differently
        self.assertIsNotNone(marine_intercept)
        self.assertIsNotNone(marine_azimuth)
        self.assertIsNotNone(aviation_intercept)
        self.assertIsNotNone(aviation_azimuth)
    
    def test_no_dip_correction_in_aviation(self):
        """Test that dip correction is not applied in aviation mode."""
        observer_height = 3000.0  # meters (high altitude)
        
        # Calculate intercept in marine mode (should include dip correction)
        marine_intercept, _ = calculate_intercept(
            self.observed_altitude,
            self.celestial_body,
            self.assumed_position,
            self.observation_time,
            observer_height=observer_height,
            navigation_mode='marine'
        )
        
        # Calculate intercept in aviation mode (should not include dip correction)
        aviation_intercept, _ = calculate_intercept(
            self.observed_altitude,
            self.celestial_body,
            self.assumed_position,
            self.observation_time,
            observer_height=observer_height,
            navigation_mode='aviation'
        )
        
        # Results should be different due to dip correction application
        self.assertNotEqual(marine_intercept, aviation_intercept)
    
    def test_bubble_sextant_correction(self):
        """Test bubble sextant correction calculation."""
        # Basic test with default parameters
        correction = calculate_bubble_sextant_correction()
        self.assertEqual(correction, 0.0)  # Current implementation returns 0
        
        # Test with specific parameters
        correction = calculate_bubble_sextant_correction(
            aircraft_altitude=3000.0,
            temperature=-20.0,
            pressure=700.0
        )
        self.assertIsInstance(correction, float)
        self.assertEqual(correction, 0.0)  # Current implementation returns 0
    
    def test_movement_correction(self):
        """Test aircraft movement correction."""
        # Original position
        original_pos = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
        
        # Stationary aircraft (no movement)
        corrected_pos = calculate_movement_correction(
            original_pos,
            self.observation_time,
            aircraft_speed_knots=0.0,
            aircraft_course=0.0,
            time_interval_hours=1.0
        )
        
        # Position should be unchanged when aircraft is not moving
        self.assertAlmostEqual(original_pos.lat.value, corrected_pos.lat.value, places=10)
        self.assertAlmostEqual(original_pos.lon.value, corrected_pos.lon.value, places=10)
        
        # Moving aircraft
        corrected_pos = calculate_movement_correction(
            original_pos,
            self.observation_time,
            aircraft_speed_knots=200.0,  # 200 knots
            aircraft_course=90.0,       # Eastward
            time_interval_hours=1.0
        )
        
        # Position should be shifted eastward
        self.assertAlmostEqual(corrected_pos.lat.value, original_pos.lat.value, places=1)  # Same latitude (approximately)
        self.assertGreater(corrected_pos.lon.value, original_pos.lon.value)  # Eastward shift
    
    def test_time_interval_correction(self):
        """Test celestial body movement correction over time."""
        # Apply time interval correction
        corrected_altitude = apply_time_interval_correction(
            self.observed_altitude,
            time_interval_hours=1.0,  # 1 hour later
            celestial_body=self.celestial_body,
            assumed_position=self.assumed_position,
            observation_time=self.observation_time
        )
        
        # The altitude should have changed due to celestial motion
        self.assertNotEqual(corrected_altitude, self.observed_altitude)
        self.assertIsInstance(corrected_altitude, float)
    
    def test_aviation_problem_generation(self):
        """Test that aviation problems can be generated."""
        # Generate a problem in aviation mode
        problem = generate_sight_reduction_problem(
            navigation_mode='aviation',
            aircraft_altitude=3000.0  # meters
        )
        
        # Verify that the problem contains aviation-specific parameters
        self.assertIn('navigation_mode', problem)
        self.assertEqual(problem['navigation_mode'], 'aviation')
        self.assertIn('aircraft_altitude', problem)
        self.assertEqual(problem['aircraft_altitude'], 3000.0)
        
        # Verify that the problem can be used in a calculation
        celestial_body = get_celestial_body(
            problem['celestial_body_name'], 
            problem['observation_time']
        )
        
        intercept, azimuth = calculate_intercept(
            problem['observed_altitude'],
            celestial_body,
            problem['assumed_position'],
            problem['observation_time'],
            observer_height=problem['observer_height'],
            temperature=problem['temperature'],
            pressure=problem['pressure'],
            celestial_body_name=problem['celestial_body_name'],
            limb=problem['limb'],
            navigation_mode=problem['navigation_mode']
        )
        
        # Both intercept and azimuth should be valid numbers
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(azimuth, float)
    
    def test_altitude_based_refraction_correction(self):
        """Test that refraction correction accounts for altitude."""
        # At sea level
        sea_refraction = calculate_refraction_correction(
            self.observed_altitude,
            self.temperature,
            self.pressure,
            altitude_meters=0.0
        )
        
        # At high altitude
        high_alt_refraction = calculate_refraction_correction(
            self.observed_altitude,
            self.temperature,
            self.pressure,
            altitude_meters=3000.0  # 3000 meters
        )
        
        # Refraction should be less at higher altitudes due to lower air density
        self.assertNotEqual(sea_refraction, high_alt_refraction)


class TestAviationAlmanac(unittest.TestCase):
    """Test aviation almanac functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aviation_almanac = AviationAlmanacInterface()
        self.observation_time = Time('2025-06-15T12:00:00')
    
    def test_aviation_almanac_initialization(self):
        """Test that aviation almanac initializes properly."""
        self.assertIsNotNone(self.aviation_almanac.aviation_tables)
        self.assertIn('vol1_stars', self.aviation_almanac.aviation_tables)
    
    def test_get_aviation_star_data(self):
        """Test getting aviation star data."""
        # Test with a known star
        star_data = self.aviation_almanac.get_aviation_star_data(
            self.observation_time,
            'sirius'
        )
        
        self.assertIn('GHA', star_data)
        self.assertIn('declination', star_data)
        self.assertIn('SHA', star_data)
        self.assertIn('magnitude', star_data)
        self.assertIn('epoch_year', star_data)
    
    def test_aviation_table_lookup(self):
        """Test aviation table lookup functionality."""
        # Test looking up altitude and azimuth
        lookup_result = get_aviation_table_lookup(
            assumed_lat=40.0,
            lha=45.0,
            declination=20.0,
            table_volume=1
        )
        
        self.assertIn('computed_altitude', lookup_result)
        self.assertIn('azimuth', lookup_result)
        self.assertIn('delta_correction', lookup_result)
        self.assertIn('table_volume', lookup_result)
        self.assertIsInstance(lookup_result['computed_altitude'], float)
        self.assertIsInstance(lookup_result['azimuth'], float)

    def test_get_aviation_celestial_body_data(self):
        """Test getting aviation celestial body data."""
        # Test with a star
        star_data = get_aviation_celestial_body_data('sirius', self.observation_time)
        
        self.assertIn('GHA', star_data)
        self.assertIn('declination', star_data)
        self.assertIn('SHA', star_data)
        
        # Test with a planet - this should fall back to marine almanac
        planet_data = get_aviation_celestial_body_data('venus', self.observation_time)
        
        self.assertIn('GHA', planet_data)
        self.assertIn('declination', planet_data)


class TestAviationIntegration(unittest.TestCase):
    """Test integration of aviation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.observation_time = Time('2023-06-15T12:00:00')
        self.assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    def test_complete_aviation_sight_reduction(self):
        """Test a complete aviation sight reduction process."""
        # Generate an aviation problem
        problem = generate_sight_reduction_problem(
            celestial_body_name='sirius',
            observation_time=self.observation_time,
            navigation_mode='aviation',
            aircraft_altitude=3000.0
        )
        
        # Get the celestial body for calculation
        celestial_body = get_celestial_body(
            problem['celestial_body_name'],
            problem['observation_time']
        )
        
        # Perform the sight reduction with aviation parameters
        intercept, azimuth = calculate_intercept(
            problem['observed_altitude'],
            celestial_body,
            problem['assumed_position'],
            problem['observation_time'],
            apply_refraction=True,
            temperature=problem['temperature'],
            pressure=problem['pressure'],
            observer_height=problem['observer_height'],
            celestial_body_name=problem['celestial_body_name'],
            limb=problem['limb'],
            navigation_mode=problem['navigation_mode'],
            aircraft_speed_knots=200.0,  # Moving aircraft
            aircraft_course=90.0,        # Eastward
            time_interval_hours=0.5      # Midway through flight
        )
        
        # Verify results
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(azimuth, float)
        
        # Azimuth should be a valid bearing (0-360 degrees)
        self.assertGreaterEqual(azimuth, 0)
        self.assertLess(azimuth, 360)


if __name__ == '__main__':
    # Run the tests
    unittest.main()