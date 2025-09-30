"""
Test for LaTeX Output Module

This module tests the LaTeX output functionality.
"""

import os
import sys
import tempfile
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.problem_generator import generate_sight_reduction_problem
from src.latex_output import generate_problem_pdf, generate_sight_reduction_latex
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u


def test_latex_generation():
    """Test LaTeX code generation."""
    print("Testing LaTeX code generation...")
    
    # Generate a sample problem with specific parameters to ensure success
    from astropy.time import Time
    from astropy.coordinates import EarthLocation
    import astropy.units as u
    
    # Use specific parameters that should work
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    problem = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun"
    )
    
    # Generate LaTeX code
    latex_code = generate_sight_reduction_latex(problem, include_answer_key=True)
    
    # Check that LaTeX code contains expected elements
    assert "\\documentclass" in latex_code
    assert "SIGHT REDUCTION WORKSHEET" in latex_code
    assert "Celestial Body:" in latex_code
    assert "Answer Key" in latex_code
    
    print("✓ LaTeX code generation test passed")
    return latex_code


def test_pdf_generation():
    """Test PDF generation."""
    print("Testing PDF generation...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a sample problem with specific parameters to ensure success
        from astropy.time import Time
        from astropy.coordinates import EarthLocation
        import astropy.units as u
        
        # Use specific parameters that should work
        observation_time = Time("2023-06-15T12:00:00")
        actual_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
        
        problem = generate_sight_reduction_problem(
            actual_position=actual_position,
            observation_time=observation_time,
            celestial_body_name="sun"
        )
        
        # Generate PDF
        output_path = generate_problem_pdf(
            problem=problem,
            output_filename="test_sight_reduction",
            output_dir=temp_dir,
            include_answer_key=True
        )
        
        # Check that PDF was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        
        print(f"✓ PDF generation test passed")
        print(f"  PDF saved to: {output_path}")
        return output_path


def test_specific_problem():
    """Test with a specific problem to ensure consistency."""
    print("Testing with specific problem...")
    
    # Create a specific problem with known parameters
    from astropy.time import Time
    from astropy.coordinates import EarthLocation
    import astropy.units as u
    
    observation_time = Time("2023-06-15T12:00:00")
    actual_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    problem = generate_sight_reduction_problem(
        actual_position=actual_position,
        observation_time=observation_time,
        celestial_body_name="sun"
    )
    
    # Generate LaTeX
    latex_code = generate_sight_reduction_latex(problem)
    
    # Check content
    assert "Sun" in latex_code
    assert "2023-06-15" in latex_code
    
    print("✓ Specific problem test passed")
    return latex_code


if __name__ == "__main__":
    print("Running LaTeX Output Tests...\n")
    
    try:
        test_latex_generation()
        test_specific_problem()
        test_pdf_generation()
        
        print("\n🎉 All tests passed! LaTeX output module is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)