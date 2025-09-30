"""
Examples for using the plotting functionality in the Sight Reduction project.

This file demonstrates how to use the various plotting functions for celestial navigation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body, visualize_sight_reduction, visualize_multiple_sights

def example_azimuth_compass_plot():
    """
    Example: Create an azimuth compass plot showing celestial body positions.
    """
    print("Creating azimuth compass plot...")
    
    from src.plotting import create_azimuth_compass_plot
    
    # Example: Plot azimuths of multiple celestial bodies
    azimuths = [45.2, 120.7, 275.3, 320.1]  # Example azimuths in degrees
    labels = ["Sun", "Venus", "Jupiter", "Sirius"]
    
    fig = create_azimuth_compass_plot(
        azimuths=azimuths,
        labels=labels,
        title="Celestial Body Azimuths at 12:00 UTC"
    )
    return fig


def example_altitude_time_plot():
    """
    Example: Create an altitude vs time plot for a celestial body.
    """
    print("Creating altitude vs time plot...")
    
    from src.plotting import create_altitude_time_plot
    
    # Define observation parameters
    start_time = Time("2023-06-15T06:00:00")
    end_time = Time("2023-06-15T18:00:00")  # 12 hours
    location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)  # New York area
    
    fig = create_altitude_time_plot(
        celestial_body='sun',
        start_time=start_time,
        end_time=end_time,
        location=location,
        title="Sun Altitude vs Time (New York Area)"
    )
    return fig


def example_line_of_position_plot():
    """
    Example: Create a line of position visualization.
    """
    print("Creating line of position plot...")
    
    from src.plotting import create_line_of_position_plot
    
    # Example: Sun sight with intercept of 5.2 nautical miles toward celestial body at azimuth 125°
    fig = create_line_of_position_plot(
        intercept=5.2,  # nautical miles (positive = toward celestial body)
        azimuth=125.0,  # degrees
        assumed_lat=40.7128,  # degrees
        assumed_lon=-74.0060,  # degrees
        scale_nm=50,  # Scale of 50 nautical miles
        title="Line of Position Example"
    )
    return fig


def example_star_chart_plot():
    """
    Example: Create a star chart visualization.
    """
    print("Creating star chart plot...")
    
    from src.plotting import create_star_chart_plot
    
    # Define observation parameters
    obs_time = Time("2023-06-15T23:00:00")  # Night observation
    location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)  # New York area
    
    fig = create_star_chart_plot(
        obs_time=obs_time,
        location=location,
        magnitude_limit=3.0,
        title="Evening Star Chart - New York Area"
    )
    return fig


def example_multiple_body_azimuth_plot():
    """
    Example: Create a compass plot showing multiple celestial bodies.
    """
    print("Creating multiple celestial bodies azimuth plot...")
    
    from src.plotting import create_multiple_body_azimuth_plot
    
    # Define observation parameters
    observation_time = Time("2023-06-15T12:00:00")
    location = EarthLocation(lat=40.7*u.deg, lon=-74.0*u.deg, height=0*u.m)  # New York area
    
    # List of celestial bodies to plot
    celestial_bodies = ['sun', 'moon', 'jupiter', 'sirius']
    
    fig = create_multiple_body_azimuth_plot(
        celestial_bodies=celestial_bodies,
        observation_time=observation_time,
        location=location,
        title="Multiple Celestial Bodies - Noon Observations"
    )
    return fig


def example_full_sight_visualization():
    """
    Example: Full sight reduction with visualization.
    """
    print("Creating full sight visualization...")
    
    # Define observation parameters
    observed_altitude = 45.23  # degrees
    celestial_body_name = "sun"
    assumed_lat = 40.7128  # degrees
    assumed_lon = -74.0060  # degrees
    observation_time = Time("2023-06-15T12:00:00")
    
    # Define the celestial body
    celestial_body = get_celestial_body(celestial_body_name, observation_time)
    
    # Assumed position of the observer
    assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)
    
    # Perform sight reduction
    intercept, azimuth = calculate_intercept(
        observed_altitude, 
        celestial_body, 
        assumed_position, 
        observation_time
    )
    
    print(f"Sight Reduction Results:")
    print(f"  Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} celestial body")
    print(f"  Azimuth: {azimuth:.2f}°")
    
    # Create visualization
    figs = visualize_sight_reduction(
        observed_altitude=observed_altitude,
        celestial_body_name=celestial_body_name,
        assumed_lat=assumed_lat,
        assumed_lon=assumed_lon,
        observation_time=observation_time,
        plot_type='both'
    )
    
    return figs


def example_multiple_sights_visualization():
    """
    Example: Visualization of multiple sights for position fix.
    """
    print("Creating multiple sights visualization...")
    
    # Simulated results from multiple celestial observations
    sight_results = [
        ("Sun", -3.2, 125.5),      # 3.2 nm away from sun, azimuth 125.5°
        ("Venus", 2.1, 245.0),     # 2.1 nm toward Venus, azimuth 245.0°
        ("Jupiter", 4.7, 60.3),    # 4.7 nm toward Jupiter, azimuth 60.3°
    ]
    
    fig = visualize_multiple_sights(
        sight_results=sight_results,
        title="Multiple Sights Summary - Position Fix"
    )
    
    return fig


def run_all_examples():
    """
    Run all plotting examples to demonstrate the functionality.
    """
    print("Running all plotting examples...\n")
    
    try:
        print("1. Azimuth Compass Plot")
        example_azimuth_compass_plot()
        print("   Azimuth compass plot created successfully!\n")
    except Exception as e:
        print(f"   Error creating azimuth compass plot: {e}\n")
    
    try:
        print("2. Altitude vs Time Plot")
        example_altitude_time_plot()
        print("   Altitude vs time plot created successfully!\n")
    except Exception as e:
        print(f"   Error creating altitude vs time plot: {e}\n")
    
    try:
        print("3. Line of Position Plot")
        example_line_of_position_plot()
        print("   Line of position plot created successfully!\n")
    except Exception as e:
        print(f"   Error creating line of position plot: {e}\n")
    
    try:
        print("4. Star Chart Plot")
        example_star_chart_plot()
        print("   Star chart plot created successfully!\n")
    except Exception as e:
        print(f"   Error creating star chart plot: {e}\n")
    
    try:
        print("5. Multiple Bodies Azimuth Plot")
        example_multiple_body_azimuth_plot()
        print("   Multiple bodies azimuth plot created successfully!\n")
    except Exception as e:
        print(f"   Error creating multiple bodies plot: {e}\n")
    
    try:
        print("6. Full Sight Visualization")
        example_full_sight_visualization()
        print("   Full sight visualization created successfully!\n")
    except Exception as e:
        print(f"   Error creating full sight visualization: {e}\n")
    
    try:
        print("7. Multiple Sights Visualization")
        example_multiple_sights_visualization()
        print("   Multiple sights visualization created successfully!\n")
    except Exception as e:
        print(f"   Error creating multiple sights visualization: {e}\n")
    
    print("All examples completed!")


if __name__ == "__main__":
    run_all_examples()