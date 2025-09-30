"""
Tests for LaTeX placeholder handling to ensure percent signs (%) in
LaTeX comments or text do not break Python old-style formatting.
"""

import os
import sys

# Ensure project modules are importable when running tests directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

from src.problem_generator import generate_sight_reduction_problem
from src.latex_output import generate_sight_reduction_latex


def test_percent_signs_do_not_break_formatting():
    """LaTeX templates contain '%' comments; formatting must not error."""
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m)

    problem = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun",
    )

    latex = generate_sight_reduction_latex(problem, include_answer_key=True)

    # Core sanity checks
    assert "\\documentclass" in latex
    assert "SIGHT REDUCTION WORKSHEET" in latex
    # Ensure LaTeX comments remain as a single '%' after formatting
    assert "\n% Page setup" in latex
    # Ensure no un-substituted mapping placeholders remain
    assert "%(" not in latex
    # Ensure instrument parameters were substituted (value present, not placeholder)
    assert "Instrument Error:" in latex
    assert "Index Error:" in latex
    assert "Personal Error:" in latex

