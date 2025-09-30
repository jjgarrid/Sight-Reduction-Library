"""
Tests for almanac LaTeX generation functionality
"""
import os
import sys
from datetime import datetime

# Ensure project modules are importable when running tests directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.latex_output import generate_almanac_latex


def test_generate_almanac_latex():
    """Test that almanac LaTeX generation works without errors."""
    # Create sample hourly data
    hourly_data = [
        {
            'time': datetime(2023, 6, 15, 0),
            'GHA': 120.5,
            'declination': 23.5,
            'SD': 0.25,
            'HP': 0.1
        },
        {
            'time': datetime(2023, 6, 15, 1),
            'GHA': 135.0,
            'declination': 23.4,
            'SD': 0.25,
            'HP': 0.1
        }
    ]
    
    # Generate LaTeX for the almanac
    latex = generate_almanac_latex('sun', datetime(2023, 6, 15), hourly_data)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'NAUTICAL ALMANAC' in latex
    assert 'Sun - 2023-06-15' in latex  # Date format check
    assert '00:00 & 120.5 & 23.5 & 0.2 & 0.1' in latex  # Hourly data check (with formatting applied)
    assert '01:00 & 135.0 & 23.4 & 0.2 & 0.1' in latex  # Second row check
    assert 'GHA = Greenwich Hour Angle' in latex
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact
    assert '%(date)s' not in latex  # Ensure placeholders are substituted
    assert '%(celestial_body_name)s' not in latex  # Ensure placeholders are substituted
    assert '%(hourly_data_rows)s' not in latex  # Ensure placeholders are substituted


def test_generate_almanac_latex_moon():
    """Test that almanac LaTeX generation works for moon data."""
    # Create sample hourly data for moon
    hourly_data = [
        {
            'time': datetime(2023, 6, 15, 6),
            'GHA': 45.2,
            'declination': -18.3,
            'SD': 0.27,
            'HP': 0.9
        }
    ]
    
    # Generate LaTeX for the moon almanac
    latex = generate_almanac_latex('moon', datetime(2023, 6, 15), hourly_data)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'Moon - 2023-06-15' in latex  # Date format check
    assert '06:00 & 45.2 & -18.3 & 0.3 & 0.9' in latex  # Hourly data check (with formatting applied)
    assert 'Horizontal Parallax: & 0.9' in latex
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact


def test_generate_almanac_latex_planet():
    """Test that almanac LaTeX generation works for planet data."""
    # Create sample hourly data for a planet
    hourly_data = [
        {
            'time': datetime(2023, 6, 15, 12),
            'GHA': 210.7,
            'declination': -5.8,
            'SD': 0.0,
            'HP': 0.0
        }
    ]
    
    # Generate LaTeX for the planet almanac
    latex = generate_almanac_latex('mars', datetime(2023, 6, 15), hourly_data)
    
    # Check that essential elements are present
    assert '\\documentclass' in latex
    assert 'Mars - 2023-06-15' in latex  # Date format check
    assert '210.7 & -5.8 & 0.0 & 0.0' in latex  # Hourly data check
    assert 'Page setup' in latex  # Make sure LaTeX comments remain intact