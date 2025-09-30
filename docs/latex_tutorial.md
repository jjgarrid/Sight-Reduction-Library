# LaTeX Documentation Tutorial

This tutorial explains how to use the LaTeX output features of the Sight Reduction library. The library provides functions to generate professional-looking celestial navigation worksheets and almanac pages in LaTeX format.

## Table of Contents
1. [Overview](#overview)
2. [Installation Requirements](#installation-requirements)
3. [Basic Usage](#basic-usage)
4. [Generating Sight Reduction Worksheets](#generating-sight-reduction-worksheets)
5. [Generating Almanac Pages](#generating-almanac-pages)
6. [Generating Multiple Sight Reduction Worksheets](#generating-multiple-sight-reduction-worksheets)
7. [Converting LaTeX to PDF](#converting-latex-to-pdf)
8. [Customizing Templates](#customizing-templates)
9. [Advanced Usage](#advanced-usage)

## Overview

The Sight Reduction library includes LaTeX generation capabilities that allow you to create:
- Single sight reduction worksheets
- Nautical almanac pages
- Multiple sight reduction worksheets for position fixes
- All with professional formatting and proper celestial navigation notation

## Installation Requirements

To use the LaTeX features, you need to have a LaTeX distribution installed on your system:
- For PDF generation, install `pdflatex` (part of most LaTeX distributions)
- On Ubuntu/Debian: `sudo apt-get install texlive-latex-recommended texlive-latex-extra`
- On Windows: Install MiKTeX or TeX Live
- On macOS: Install MacTeX or BasicTeX

## Basic Usage

Here's a simple example that generates a sight reduction worksheet:

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.problem_generator import generate_sight_reduction_problem
from src.latex_output import generate_sight_reduction_latex

# Create a sample problem
observation_time = Time("2023-06-15T12:00:00")
actual_position = EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m)

problem = generate_sight_reduction_problem(
    actual_position=actual_position,
    observation_time=observation_time,
    celestial_body_name="sun"
)

# Generate LaTeX code for the worksheet
latex_code = generate_sight_reduction_latex(problem, include_answer_key=False)
print(latex_code)
```

## Generating Sight Reduction Worksheets

### Step 1: Prepare the Problem Data
Create a problem dictionary with all necessary information:

```python
problem = {
    'celestial_body_name': 'sun',
    'observation_time': Time("2023-06-15T12:00:00"),
    'observed_altitude': 45.0,  # degrees
    'temperature': 20.0,  # Celsius
    'pressure': 1013.0,  # hPa
    'observer_height': 3.0,  # meters
    'assumed_position': EarthLocation(lat=39.0 * u.deg, lon=-74.5 * u.deg, height=0 * u.m),
    'actual_position': EarthLocation(lat=40.0 * u.deg, lon=-74.0 * u.deg, height=0 * u.m),
    'instrument_error': 0.1,  # degrees
    'index_error': 0.2,  # degrees
    'personal_error': 0.3,  # degrees
    # Additional computed values (for answer key):
    'true_altitude': 44.8,  # degrees
    'true_azimuth': 120.5,  # degrees
    'intercept': -0.2  # nautical miles
}
```

### Step 2: Generate LaTeX Code

Generate the LaTeX code for the worksheet:

```python
from src.latex_output import generate_sight_reduction_latex

# Generate LaTeX without answer key
latex_code = generate_sight_reduction_latex(problem, include_answer_key=False)

# Or generate with answer key
latex_code_with_answers = generate_sight_reduction_latex(problem, include_answer_key=True)
```

The function creates a complete LaTeX document with:
- Observation details (celestial body, time, altitude)
- Environmental conditions
- Assumed position
- Instrument parameters
- Task description
- Plotting area
- Optional answer key with solution

## Generating Almanac Pages

### Step 1: Prepare Hourly Data

Create hourly data for the celestial body:

```python
from datetime import datetime

hourly_data = [
    {
        'time': datetime(2023, 6, 15, 0),  # 00:00 UTC
        'GHA': 120.5,  # degrees
        'declination': 23.5,  # degrees
        'SD': 0.25,  # Semi-diameter in minutes
        'HP': 0.1  # Horizontal parallax in minutes
    },
    {
        'time': datetime(2023, 6, 15, 1),  # 01:00 UTC
        'GHA': 135.0,  # degrees
        'declination': 23.4,  # degrees
        'SD': 0.25,  # Semi-diameter in minutes
        'HP': 0.1  # Horizontal parallax in minutes
    }
    # ... more hourly entries
]
```

### Step 2: Generate Almanac LaTeX

Generate the LaTeX code for the almanac page:

```python
from src.latex_output import generate_almanac_latex

latex_code = generate_almanac_latex('sun', datetime(2023, 6, 15), hourly_data)
```

This generates a complete LaTeX document with:
- Title and header information
- Hourly data table
- Additional information section
- Notes about abbreviations

## Generating Multiple Sight Reduction Worksheets

### Step 1: Prepare Multiple Problems

Create a list of problems for the fix:

```python
problems = [problem1, problem2, problem3]  # List of problem dictionaries
```

### Step 2: Generate LaTeX for Multiple Sights

```python
from src.latex_output import generate_multiple_sight_reduction_latex

latex_code = generate_multiple_sight_reduction_latex(
    problems, 
    vessel_speed=5.0,  # knots (for running fixes)
    vessel_course=90.0  # degrees
)
```

## Converting LaTeX to PDF

You can directly generate PDFs from the LaTeX code:

```python
from src.latex_output import generate_problem_pdf, generate_almanac_pdf, generate_fix_pdf

# Generate a PDF for a single problem
pdf_path = generate_problem_pdf(
    problem, 
    "sight_reduction_worksheet", 
    output_dir=".", 
    include_answer_key=True
)

# Generate a PDF for almanac data
pdf_path = generate_almanac_pdf(
    'sun',
    datetime(2023, 6, 15),
    hourly_data,
    "sun_almanac_2023_06_15",
    output_dir="."
)

# Generate a PDF for multiple sights
pdf_path = generate_fix_pdf(
    problems,
    "multiple_sight_reduction_fix",
    output_dir=".",
    vessel_speed=5.0,
    vessel_course=90.0
)
```

The `generate_*_pdf` functions automatically:
1. Generate the LaTeX code
2. Compile it to PDF using pdflatex
3. Save the PDF to the specified location

## Customizing Templates

The library uses templates stored in `src/latex_templates.py`. You can customize these templates to change the appearance of generated documents:

### Available Templates
- `SIGHT_REDUCTION_PROBLEM_TEMPLATE` - Template for single sight reduction problems
- `ANSWER_KEY_TEMPLATE` - Template for answer sections
- `ALMANAC_PAGE_TEMPLATE` - Template for almanac pages
- `MULTIPLE_SIGHT_REDUCTION_TEMPLATE` - Template for multiple sight reductions

### Template Customization
The templates use `%(key)s` format for placeholders, which gets replaced with actual data. When customizing, make sure to preserve the placeholder format and avoid breaking LaTeX comments that begin with `%`.

## Advanced Usage

### Error Handling

When generating PDFs, make sure to handle potential errors:

```python
try:
    pdf_path = generate_problem_pdf(problem, "my_worksheet")
    print(f"PDF saved to: {pdf_path}")
except RuntimeError as e:
    print(f"Error generating PDF: {e}")
```

### Working with Different Celestial Bodies

The system supports various celestial bodies:
- Sun, moon
- Planets (mars, venus, jupiter, saturn)
- Stars (using proper names)

Example:
```python
# Generate a problem for Mars
problem_mars = generate_sight_reduction_problem(
    actual_position=actual_position,
    observation_time=observation_time,
    celestial_body_name="mars"
)
```

This covers the basic and advanced usage of the LaTeX generation features in the Sight Reduction library.