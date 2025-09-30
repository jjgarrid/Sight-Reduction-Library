#!/usr/bin/env python
"""
Test script to verify almanac integration and compatibility with existing code.
"""

from datetime import datetime
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

def test_almanac_integration():
    """Test the almanac integration module."""
    print("Testing almanac integration module...")
    
    try:
        from src.almanac_integration import AlmanacInterface, get_celestial_body_almanac_data, get_hourly_almanac_data
        
        # Create an almanac interface
        almanac = AlmanacInterface()
        
        # Test datetime
        test_time = datetime(2023, 6, 15, 12, 0, 0)
        
        # Test Sun data
        sun_data = almanac.get_sun_data(test_time)
        print(f"Sun data: GHA={sun_data['GHA']:.4f}°, Dec={sun_data['declination']:.4f}°")
        
        # Test Moon data
        moon_data = almanac.get_moon_data(test_time)
        print(f"Moon data: GHA={moon_data['GHA']:.4f}°, Dec={moon_data['declination']:.4f}°")
        
        # Test star data
        star_data = almanac.get_star_data('sirius', test_time)
        print(f"Sirius data: GHA={star_data['GHA']:.4f}°, Dec={star_data['declination']:.4f}°")
        
        # Test using the utility function
        venus_data = get_celestial_body_almanac_data('venus', test_time)
        print(f"Venus data: GHA={venus_data['GHA']:.4f}°, Dec={venus_data['declination']:.4f}°")
        
        # Test hourly data
        hourly_sun = get_hourly_almanac_data('sun', test_time)
        print(f"Hourly sun data shape: {hourly_sun.shape}")
        print(f"First few hours:")
        print(hourly_sun.head())
        
        print("✓ Almanac integration working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error testing almanac integration: {e}")
        return False


def test_compatibility_with_existing_code():
    """Test that almanac integration works with existing sight reduction code."""
    print("\nTesting compatibility with existing sight reduction code...")
    
    try:
        from src.sight_reduction import calculate_intercept, get_celestial_body
        from src.almanac_integration import get_celestial_body_almanac_data
        from datetime import datetime
        
        # Test date/time
        test_time = Time("2023-06-15T12:00:00")
        test_datetime = datetime(2023, 6, 15, 12, 0, 0)
        
        # Get celestial body using existing function
        celestial_body = get_celestial_body("sun", test_time)
        print(f"✓ Got celestial body using existing function")
        
        # Get almanac data using new function
        almanac_data = get_celestial_body_almanac_data("sun", test_datetime)
        print(f"✓ Got almanac data using new function")
        print(f"  GHA: {almanac_data['GHA']:.4f}°, Dec: {almanac_data['declination']:.4f}°")
        
        # Set up assumed position
        assumed_position = EarthLocation(lat=40.7128*u.deg, lon=-74.0060*u.deg, height=0*u.m)
        
        # Execute sight reduction using the existing function
        intercept, azimuth = calculate_intercept(
            45.23,  # observed altitude
            celestial_body,
            assumed_position,
            test_time
        )
        
        print(f"✓ Sight reduction executed successfully")
        print(f"  Intercept: {intercept:.2f} nm, Azimuth: {azimuth:.2f}°")
        
        print("✓ Compatibility with existing code verified")
        return True
        
    except Exception as e:
        print(f"✗ Error testing compatibility: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_problem_generation_with_almanac():
    """Test that problem generation works with almanac data."""
    print("\nTesting problem generation with almanac integration...")
    
    try:
        from src.problem_generator import (
            generate_sight_reduction_problem, 
            generate_morning_sight_problem, 
            generate_evening_sight_problem,
            generate_twilight_star_sight_problem,
            generate_moon_sight_problem,
            generate_multi_body_sight_reduction_problems
        )
        from src.almanac_integration import get_celestial_body_almanac_data
        
        # Test generating a basic problem
        problem = generate_sight_reduction_problem(celestial_body_name="sun")
        print(f"✓ Generated basic sight reduction problem")
        print(f"  Body: {problem['celestial_body_name']}")
        print(f"  Observed Altitude: {problem['observed_altitude']:.4f}°")
        print(f"  Time: {problem['observation_time']}")
        
        # Test generating a morning sight
        morning_problem = generate_morning_sight_problem()
        print(f"✓ Generated morning sight problem")
        
        # Test generating an evening sight
        evening_problem = generate_evening_sight_problem()
        print(f"✓ Generated evening sight problem")
        
        # Test generating a star sight
        star_problem = generate_twilight_star_sight_problem()
        print(f"✓ Generated star sight problem")
        
        # Test generating a moon sight
        moon_problem = generate_moon_sight_problem()
        print(f"✓ Generated moon sight problem")
        
        # Test generating multi-body problems
        multi_problems = generate_multi_body_sight_reduction_problems(num_bodies=3)
        print(f"✓ Generated {len(multi_problems)}-body sight problems")
        
        # Verify we can get almanac data for the generated problems
        for i, prob in enumerate(multi_problems):
            almanac_data = get_celestial_body_almanac_data(
                prob['celestial_body_name'], 
                prob['observation_time'].datetime
            )
            print(f"  Problem {i+1}: {prob['celestial_body_name']} - GHA: {almanac_data['GHA']:.4f}°")
        
        print("✓ Problem generation with almanac integration working")
        return True
        
    except Exception as e:
        print(f"✗ Error testing problem generation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Testing almanac integration and compatibility...\n")
    
    success = True
    success &= test_almanac_integration()
    success &= test_compatibility_with_existing_code()
    success &= test_problem_generation_with_almanac()
    
    if success:
        print("\n✓ All tests passed! Almanac integration is compatible with existing code.")
    else:
        print("\n✗ Some tests failed. Need to troubleshoot integration issues.")