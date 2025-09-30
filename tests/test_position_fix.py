"""
Test suite for the Advanced Position Fix Calculation Module
"""

import unittest
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
from src.position_fix import (
    calculate_least_squares_fix,
    calculate_running_fix,
    calculate_error_ellipse,
    calculate_geometric_factor,
    assess_fix_quality,
    calculate_single_line_of_position,
    calculate_position_on_lop
)


class TestLeastSquaresFix(unittest.TestCase):
    """Test the least squares position fix calculation."""
    
    def test_least_squares_fix_basic(self):
        """Test basic least squares fix calculation."""
        # Create some test sights
        sight1 = {
            'observed_altitude': 45.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:00:00'),
            'intercept': 10.0,  # nm towards celestial body
            'azimuth': 90.0,    # East
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        sight2 = {
            'observed_altitude': 40.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:05:00'),
            'intercept': -5.0,  # nm away from celestial body
            'azimuth': 0.0,     # North
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        sights = [sight1, sight2]
        
        result = calculate_least_squares_fix(sights)
        
        # Check that we get a result
        self.assertIsNotNone(result)
        self.assertIn('fix_position', result)
        self.assertIn('fix_accuracy_nm', result)
        self.assertIn('error_ellipse', result)
        self.assertIn('fix_quality', result)
        self.assertIn('geometric_factor', result)
        
        # Check that the fix position is an EarthLocation object
        self.assertIsInstance(result['fix_position'], EarthLocation)
        
        # Check that fix accuracy is a reasonable value
        self.assertIsInstance(result['fix_accuracy_nm'], (int, float))
        self.assertGreaterEqual(result['fix_accuracy_nm'], 0)
    
    def test_least_squares_fix_insufficient_sights(self):
        """Test that we get an error with insufficient sights."""
        sight = {
            'observed_altitude': 45.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:00:00'),
            'intercept': 10.0,
            'azimuth': 90.0,
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        # Try with only one sight
        with self.assertRaises(ValueError):
            calculate_least_squares_fix([sight])
    
    def test_least_squares_fix_with_three_sights(self):
        """Test least squares fix with three sights."""
        sights = []
        for i in range(3):
            minute = 0 if i == 0 else i*10  # 0, 10, 20 minutes
            sight = {
                'observed_altitude': 45.0 + i,
                'celestial_body_name': 'sun',
                'observation_time': Time(f'2023-06-15T12:{minute:02d}:00'),
                'intercept': 10.0 - i*3,
                'azimuth': 90.0 + i*120,  # Spread azimuths around compass
                'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
                'altitude_correction_error': 0.1
            }
            sights.append(sight)
        
        result = calculate_least_squares_fix(sights)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['number_of_sights'], 3)
        self.assertTrue(result['solution_converged'])


class TestRunningFix(unittest.TestCase):
    """Test the running fix calculation."""
    
    def test_running_fix_basic(self):
        """Test basic running fix calculation."""
        # Create some test sights at different times
        sight1 = {
            'observed_altitude': 45.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:00:00'),
            'intercept': 10.0,
            'azimuth': 90.0,
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        sight2 = {
            'observed_altitude': 40.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:30:00'),  # 30 minutes later
            'intercept': -5.0,
            'azimuth': 0.0,
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        # Vessel moving at 10 knots on course 045
        result = calculate_running_fix([sight1, sight2], vessel_speed=10.0, vessel_course=45.0)
        
        self.assertIsNotNone(result)
        self.assertIn('fix_position', result)
        self.assertIsInstance(result['fix_position'], EarthLocation)


class TestErrorEllipse(unittest.TestCase):
    """Test the error ellipse calculation."""
    
    def test_error_ellipse_basic(self):
        """Test basic error ellipse calculation."""
        # Create some test sights
        sight1 = {
            'observed_altitude': 45.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:00:00'),
            'intercept': 10.0,
            'azimuth': 90.0,
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        sight2 = {
            'observed_altitude': 40.0,
            'celestial_body_name': 'sun',
            'observation_time': Time('2023-06-15T12:05:00'),
            'intercept': -5.0,
            'azimuth': 0.0,
            'assumed_position': EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m),
            'altitude_correction_error': 0.1
        }
        
        sights = [sight1, sight2]
        
        result = calculate_error_ellipse(sights)
        
        self.assertIsNotNone(result)
        self.assertIn('semi_major_axis_nm', result)
        self.assertIn('semi_minor_axis_nm', result)
        self.assertIn('orientation_deg', result)
        self.assertIn('confidence_level', result)
        
        # Check that values are positive
        self.assertGreaterEqual(result['semi_major_axis_nm'], 0)
        self.assertGreaterEqual(result['semi_minor_axis_nm'], 0)
        self.assertGreaterEqual(result['orientation_deg'], 0)
        self.assertLess(result['orientation_deg'], 360)


class TestGeometricFactor(unittest.TestCase):
    """Test the geometric factor calculation."""
    
    def test_geometric_factor_perpendicular_azimuths(self):
        """Test geometric factor with perpendicular azimuths (best case)."""
        azimuths = np.array([0.0, 90.0])  # North and East - perpendicular
        factor = calculate_geometric_factor(azimuths)
        
        # Perpendicular azimuths should give a good geometric factor
        self.assertGreater(factor, 0)
    
    def test_geometric_factor_parallel_azimuths(self):
        """Test geometric factor with parallel azimuths (worst case)."""
        azimuths = np.array([0.0, 180.0])  # North and South - parallel
        factor = calculate_geometric_factor(azimuths)
        
        # Parallel azimuths should give a lower geometric factor
        self.assertGreaterEqual(factor, 0)  # Should not be negative
    
    def test_geometric_factor_multiple_azimuths(self):
        """Test geometric factor with multiple azimuths."""
        # Three azimuths spread around the compass
        azimuths = np.array([0.0, 120.0, 240.0])
        factor = calculate_geometric_factor(azimuths)
        
        self.assertGreaterEqual(factor, 0)


class TestFixQuality(unittest.TestCase):
    """Test the fix quality assessment."""
    
    def test_fix_quality_excellent(self):
        """Test fix quality assessment for excellent fix."""
        quality = assess_fix_quality(geometric_factor=15.0, rmse=0.2)
        self.assertEqual(quality, "Excellent")
    
    def test_fix_quality_good(self):
        """Test fix quality assessment for good fix."""
        quality = assess_fix_quality(geometric_factor=8.0, rmse=0.8)
        self.assertEqual(quality, "Good")
    
    def test_fix_quality_fair(self):
        """Test fix quality assessment for fair fix."""
        quality = assess_fix_quality(geometric_factor=3.0, rmse=1.5)
        self.assertEqual(quality, "Fair")
    
    def test_fix_quality_poor(self):
        """Test fix quality assessment for poor fix."""
        quality = assess_fix_quality(geometric_factor=1.0, rmse=3.0)
        self.assertEqual(quality, "Poor")


class TestPositionCalculations(unittest.TestCase):
    """Test the position calculation utilities."""
    
    def test_calculate_position_on_lop(self):
        """Test calculation of position on line of position."""
        lat, lon = calculate_position_on_lop(40.0, -74.0, 90.0, 10.0)  # 10 nm east
        
        # Should be east (positive longitude) of starting position
        self.assertAlmostEqual(lat, 40.0, places=1)  # Latitude should stay the same for east movement
        self.assertGreater(lon, -74.0)  # Longitude should increase (eastward)
    
    def test_calculate_single_line_of_position(self):
        """Test calculation of single line of position for plotting."""
        assumed_pos = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
        lop_coords = calculate_single_line_of_position(90.0, 5.0, assumed_pos)  # Azimuth 90, intercept 5nm
        
        # Should return 4 coordinates (lat1, lon1, lat2, lon2)
        self.assertEqual(len(lop_coords), 4)
        
        # Check they are all numbers
        for coord in lop_coords:
            self.assertIsInstance(coord, (int, float))


if __name__ == '__main__':
    unittest.main()