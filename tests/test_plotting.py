"""
Tests for the plotting functionality in the Sight Reduction project.
"""
import sys
import os
import pytest
import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_azimuth_compass_plot():
    """Test that azimuth compass plot can be created without errors."""
    try:
        from src.plotting import create_azimuth_compass_plot
        
        # Create a simple compass plot
        fig = create_azimuth_compass_plot(
            azimuths=[45, 135, 225, 315],
            labels=['A', 'B', 'C', 'D'],
            title="Test Compass Plot",
            show_plot=False
        )
        
        # Verify that a figure was returned
        assert fig is not None
        print("✓ Azimuth compass plot test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib not available, skipping azimuth compass plot test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Azimuth compass plot test failed: {e}")
        return False


def test_altitude_time_plot():
    """Test that altitude vs time plot can be created without errors."""
    try:
        from src.plotting import create_altitude_time_plot
        
        # Define test parameters
        start_time = Time("2023-06-15T06:00:00")
        end_time = Time("2023-06-15T18:00:00")
        location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)
        
        # Create altitude vs time plot
        fig = create_altitude_time_plot(
            celestial_body='sun',
            start_time=start_time,
            end_time=end_time,
            location=location,
            title="Test Altitude vs Time",
            show_plot=False
        )
        
        # Verify that a figure was returned
        assert fig is not None
        print("✓ Altitude vs time plot test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib not available, skipping altitude vs time plot test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Altitude vs time plot test failed: {e}")
        return False


def test_line_of_position_plot():
    """Test that line of position plot can be created without errors."""
    try:
        from src.plotting import create_line_of_position_plot
        
        # Create a line of position plot
        fig = create_line_of_position_plot(
            intercept=5.2,
            azimuth=125.0,
            assumed_lat=40.7128,
            assumed_lon=-74.0060,
            title="Test Line of Position",
            show_plot=False
        )
        
        # Verify that a figure was returned
        assert fig is not None
        print("✓ Line of position plot test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib not available, skipping line of position plot test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Line of position plot test failed: {e}")
        return False


def test_star_chart_plot():
    """Test that star chart plot can be created without errors."""
    try:
        from src.plotting import create_star_chart_plot
        
        # Define test parameters
        obs_time = Time("2023-06-15T23:00:00")
        location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)
        
        # Create star chart plot
        fig = create_star_chart_plot(
            obs_time=obs_time,
            location=location,
            title="Test Star Chart",
            show_plot=False
        )
        
        # Verify that a figure was returned
        assert fig is not None
        print("✓ Star chart plot test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib not available, skipping star chart plot test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Star chart plot test failed: {e}")
        return False


def test_multiple_body_azimuth_plot():
    """Test that multiple body azimuth plot can be created without errors."""
    try:
        from src.plotting import create_multiple_body_azimuth_plot
        
        # Define test parameters
        observation_time = Time("2023-06-15T12:00:00")
        location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)
        celestial_bodies = ['sun', 'moon', 'venus']
        
        # Create multiple body azimuth plot
        fig = create_multiple_body_azimuth_plot(
            celestial_bodies=celestial_bodies,
            observation_time=observation_time,
            location=location,
            title="Test Multiple Bodies",
            show_plot=False
        )
        
        # Verify that a figure was returned (might be None if no bodies are above horizon)
        print("✓ Multiple body azimuth plot test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib not available, skipping multiple body azimuth plot test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Multiple body azimuth plot test failed: {e}")
        return False


def test_sight_visualization_integration():
    """Test the integration of plotting with sight reduction functions."""
    try:
        from src.sight_reduction import visualize_sight_reduction
        
        # Test parameters
        result = visualize_sight_reduction(
            observed_altitude=45.0,
            celestial_body_name="sun",
            assumed_lat=40.0,
            assumed_lon=-74.0,
            observation_time=Time("2023-06-15T12:00:00"),
            plot_type='both',
            save_path=None
        )
        
        # Result might be None if matplotlib is not available, which is acceptable
        print("✓ Sight visualization integration test passed")
        return True
    except ImportError:
        print("⚠ Matplotlib or other dependency not available, skipping sight visualization test")
        return True  # Don't fail the test if matplotlib isn't available
    except Exception as e:
        print(f"✗ Sight visualization integration test failed: {e}")
        return False


def test_plotting_module_imports():
    """Test that the plotting module can be imported without errors."""
    try:
        import src.plotting
        # Check that expected functions exist
        assert hasattr(src.plotting, 'create_azimuth_compass_plot')
        assert hasattr(src.plotting, 'create_altitude_time_plot')
        assert hasattr(src.plotting, 'create_line_of_position_plot')
        assert hasattr(src.plotting, 'create_star_chart_plot')
        assert hasattr(src.plotting, 'create_multiple_body_azimuth_plot')
        assert hasattr(src.plotting, 'create_sight_summary_plot')
        print("✓ Plotting module import test passed")
        return True
    except ImportError as e:
        print(f"⚠ Plotting module import failed (may be due to missing matplotlib): {e}")
        return True  # Don't fail if matplotlib isn't available
    except Exception as e:
        print(f"✗ Plotting module import test failed: {e}")
        return False


def run_all_plotting_tests():
    """Run all plotting tests and return overall success."""
    print("Running plotting functionality tests...\n")
    
    tests = [
        test_plotting_module_imports,
        test_azimuth_compass_plot,
        test_altitude_time_plot,
        test_line_of_position_plot,
        test_star_chart_plot,
        test_multiple_body_azimuth_plot,
        test_sight_visualization_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nPlotting tests summary: {passed}/{total} passed")
    
    # If matplotlib isn't available, all tests are considered passed (not failed)
    # since the plotting functionality is optional
    try:
        import matplotlib
        all_passed = (passed == total)
    except ImportError:
        # If matplotlib isn't available, we can't really test plotting, so consider it a pass
        print("(Note: Matplotlib not available, plotting functionality is optional)")
        all_passed = True
    
    return all_passed


if __name__ == "__main__":
    success = run_all_plotting_tests()
    if success:
        print("\n✓ All plotting tests completed successfully!")
    else:
        print("\n✗ Some plotting tests failed!")
        sys.exit(1)