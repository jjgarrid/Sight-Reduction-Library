"""
Tests for multiple sight reduction LaTeX generation functionality
"""
import os
import sys
from datetime import datetime

# Ensure project modules are importable when running tests directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.problem_generator import generate_sight_reduction_problem
from src.latex_output import generate_multiple_sight_reduction_latex


def test_generate_multiple_sight_reduction_latex():
    """Test that multiple sight reduction LaTeX generation works without errors."""
    # Generate sample problems
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m)

    # Create multiple problems
    problem1 = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun",
    )
    problem1['observed_altitude'] = 45.0
    problem1['temperature'] = 20.0
    problem1['pressure'] = 1013.0
    problem1['observer_height'] = 3.0
    problem1['instrument_error'] = 0.1
    problem1['index_error'] = 0.2
    problem1['personal_error'] = 0.3
    
    # Create a second problem with slightly different time
    observation_time2 = Time("2023-06-15T15:00:00")
    problem2 = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time2,
        celestial_body_name="mars",
    )
    problem2['observed_altitude'] = 30.0
    problem2['temperature'] = 18.0
    problem2['pressure'] = 1012.0
    problem2['observer_height'] = 3.0
    problem2['instrument_error'] = 0.1
    problem2['index_error'] = 0.2
    problem2['personal_error'] = 0.3
    
    problems = [problem1, problem2]
    
    # Generate LaTeX for multiple sight reduction
    latex = generate_multiple_sight_reduction_latex(problems, vessel_speed=5.0, vessel_course=90.0)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'CELESTIAL NAVIGATION FIX' in latex
    assert '2023-06-15' in latex  # Date check
    assert '2 observations' in latex  # Time window check
    assert '5.0 knots' in latex  # Vessel speed check
    assert '90.0\\textdegree' in latex  # Vessel course check
    assert 'Sun' in latex and 'Mars' in latex  # Celestial bodies check
    assert '12:00' in latex and '15:00' in latex  # Time check
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact
    assert '%(date)s' not in latex  # Ensure placeholders are substituted
    assert '%(observations_table)s' not in latex  # Ensure placeholders are substituted


def test_generate_multiple_sight_reduction_latex_single_problem():
    """Test that multiple sight reduction LaTeX generation works with a single problem."""
    # Generate a single problem
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m)

    problem = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun",
    )
    problem['observed_altitude'] = 45.0
    problem['temperature'] = 20.0
    problem['pressure'] = 1013.0
    problem['observer_height'] = 3.0
    problem['instrument_error'] = 0.1
    problem['index_error'] = 0.2
    problem['personal_error'] = 0.3
    
    problems = [problem]
    
    # Generate LaTeX for single problem (still using multiple sight function)
    latex = generate_multiple_sight_reduction_latex(problems)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'CELESTIAL NAVIGATION FIX' in latex
    assert '2023-06-15' in latex  # Date check
    assert '1 observations' in latex  # Time window check (single problem)
    assert 'Sun' in latex  # Celestial body check
    assert '12:00' in latex  # Time check
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact


def test_generate_multiple_sight_reduction_latex_with_answer_key():
    """Test that multiple sight reduction LaTeX generation works with answer key."""
    # Generate sample problems with some answer data
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m)

    problem1 = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun",
    )
    problem1['observed_altitude'] = 45.0
    problem1['temperature'] = 20.0
    problem1['pressure'] = 1013.0
    problem1['observer_height'] = 3.0
    problem1['instrument_error'] = 0.1
    problem1['index_error'] = 0.2
    problem1['personal_error'] = 0.3
    # Add some computed values for the answer key
    problem1['true_altitude'] = 44.8
    problem1['true_azimuth'] = 120.5
    problem1['intercept'] = -0.2
    
    problems = [problem1]
    
    # Generate LaTeX for multiple sight reduction
    latex = generate_multiple_sight_reduction_latex(problems)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'CELESTIAL NAVIGATION FIX' in latex
    assert 'Sun' in latex
    # Check that answer key elements are present
    assert 'H_c' in latex and 'Z_n' in latex  # Answer key includes these elements
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact