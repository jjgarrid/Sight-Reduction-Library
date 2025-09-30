"""
Example script demonstrating the LaTeX booklet generation functionality.

This script shows how to generate a complete celestial navigation booklet with:
- Sight reduction exercises
- Plots of the sight reductions
- Almanac annexes with celestial body data
- Solutions for the exercises

Usage:
    python examples/booklet_generation_example.py

This will create a PDF file named 'sight_reduction_booklet_example.pdf' in the current directory.
"""

import os
import sys
import tempfile
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the necessary functions from our project
from src.problem_generator import generate_sight_reduction_problem
from src.latex_output import (
    generate_booklet_pdf,
    generate_almanac_annexes,
    generate_and_save_plot
)


def create_sample_booklet():
    """
    Create a sample booklet with sight reduction problems and supporting materials.
    
    Returns:
        str: Path to the generated PDF booklet
    """
    print("Creating sample celestial navigation booklet...")
    
    # Create a temporary directory for our files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in temporary directory: {temp_dir}")
        
        # Generate a sample sight reduction problem
        print("Generating sight reduction problem...")
        observation_time = Time("2023-06-15T12:00:00")
        actual_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
        
        problem = generate_sight_reduction_problem(
            actual_position=actual_position,
            observation_time=observation_time,
            celestial_body_name="sun"
        )
        
        # Generate a plot of the sight reduction
        print("Generating sight reduction plot...")
        plot_path = generate_and_save_plot(
            problem=problem,
            output_dir=temp_dir,
            filename="sample_plot.png"
        )
        print(f"Plot saved to: {plot_path}")
        
        # Generate almanac annexes for the booklet
        print("Generating almanac annexes...")
        date = datetime.now()
        almanac_pages = generate_almanac_annexes(
            bodies=["sun", "moon", "venus"], 
            date=date, 
            hours=12
        )
        print(f"Generated {len(almanac_pages)} almanac pages")
        
        # Generate the complete booklet
        print("Generating complete booklet PDF...")
        output_path = generate_booklet_pdf(
            problem=problem,
            output_filename="sight_reduction_booklet_example",
            output_dir=".",
            plot_path=plot_path,
            almanac_pages=almanac_pages,
            include_answer_key=True
        )
        
        print(f"Booklet generated successfully!")
        print(f"PDF saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    # Create the sample booklet
    try:
        pdf_path = create_sample_booklet()
        print(f"\n🎉 Successfully created booklet: {pdf_path}")
        
        # Show information about the generated booklet
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"📁 File size: {file_size / 1024:.1f} KB")
            
            # Count pages using pdftotext if available
            try:
                import subprocess
                result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Pages:' in line:
                        print(f"📄 {line.strip()}")
                        break
            except FileNotFoundError:
                print("📄 Page count unavailable (pdfinfo not found)")
                
        print("\n📖 The booklet contains:")
        print("   • Sight reduction exercise with observation details")
        print("   • Plot of the sight reduction")
        print("   • Almanac data for Sun, Moon, and Venus")
        print("   • Detailed solution with worked example")
        
    except Exception as e:
        print(f"❌ Error creating booklet: {e}")
        import traceback
        traceback.print_exc()