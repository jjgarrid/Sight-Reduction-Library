"""
LaTeX Output Module for Celestial Navigation Problems

This module provides functions for generating LaTeX documents and PDFs
from celestial navigation problems and almanac data.
"""

import os
import subprocess
import tempfile
import shutil
from datetime import datetime
from string import Template
from typing import Dict, List
import astropy.units as u
import re

from .latex_templates import (
    SIGHT_REDUCTION_PROBLEM_TEMPLATE,
    ANSWER_KEY_TEMPLATE,
    ALMANAC_PAGE_TEMPLATE,
    MULTIPLE_SIGHT_REDUCTION_TEMPLATE,
    SIGHT_REDUCTION_BOOKLET_TEMPLATE,
    format_angle_for_latex,
    format_lon_for_latex,
    format_time_for_latex
)


def _replace_placeholders(template: str, data: Dict) -> str:
    """
    Replace placeholders in template with data values using old-style
    %(key)s formatting, while preserving LaTeX % comments.

    - Escapes any '%' not starting a '%(' placeholder or '%%' literal so
      Python's formatter doesn't treat LaTeX comments like format codes.
    - Safely substitutes, using empty strings for missing keys.
    """
    # Escape '%' that are not followed by '(' or another '%'
    # This keeps LaTeX comments intact after formatting (%% -> % in output)
    safe_template = re.sub(r'%(?!\(|%)', '%%', template)

    class SafeDict(dict):
        def __missing__(self, key):  # type: ignore
            return ""

    try:
        return safe_template % SafeDict(**data)
    except Exception:
        # As a last resort, return a best-effort substitution
        return safe_template % SafeDict()


def generate_sight_reduction_latex(problem: Dict, include_answer_key: bool = False) -> str:
    """
    Generate LaTeX code for a single sight reduction problem.
    
    Parameters:
    - problem: Dictionary containing sight reduction problem data
    - include_answer_key: Whether to include the answer key in the output
    
    Returns:
    - String containing LaTeX code for the problem worksheet
    """
    # Prepare data for template
    template_data = {
        'celestial_body_name': problem['celestial_body_name'].capitalize(),
        'limb_text': f" ({problem['limb']} limb)" if problem['celestial_body_name'] in ['sun', 'moon'] else "",
        'observation_time': format_time_for_latex(problem['observation_time'].datetime),
        'observed_altitude': f"{problem['observed_altitude']:.1f}\\textdegree",
        'temperature': f"{problem['temperature']:.1f}",
        'pressure': f"{problem['pressure']:.1f}",
        'observer_height': f"{problem['observer_height']:.1f}",
        'assumed_lat': format_angle_for_latex(problem['assumed_position'].lat.deg),
        'assumed_lon': format_lon_for_latex(problem['assumed_position'].lon.deg),
        'instrument_error': f"{problem['instrument_error']:.3f}\\textdegree",
        'index_error': f"{problem['index_error']:.3f}\\textdegree",
        'personal_error': f"{problem['personal_error']:.3f}\\textdegree"
    }
    
    # Add answer key if requested
    if include_answer_key:
        answer_data = {
            'actual_lat': format_angle_for_latex(problem['actual_position'].lat.deg),
            'actual_lon': format_lon_for_latex(problem['actual_position'].lon.deg),
            'computed_altitude': f"{problem.get('true_altitude', 0):.1f}\\textdegree",
            'azimuth': f"{problem.get('true_azimuth', 0):.1f}\\textdegree",
            'intercept': f"{abs(problem.get('intercept', 0)):.1f}",
            'intercept_direction': "Toward" if problem.get('intercept', 0) > 0 else "Away from"
        }
        
        answer_key = _replace_placeholders(ANSWER_KEY_TEMPLATE, answer_data)
        template_data['answer_key'] = answer_key
    else:
        template_data['answer_key'] = ""
    
    # Render template
    return _replace_placeholders(SIGHT_REDUCTION_PROBLEM_TEMPLATE, template_data)


def generate_almanac_latex(body_name: str, date: datetime, hourly_data: List[Dict]) -> str:
    """
    Generate LaTeX code for almanac pages.
    
    Parameters:
    - body_name: Name of the celestial body
    - date: Date for which to generate almanac data
    - hourly_data: List of dictionaries containing hourly almanac data
    
    Returns:
    - String containing LaTeX code for the almanac page
    """
    # Prepare hourly data rows
    hourly_rows = []
    for entry in hourly_data:
        time_str = entry['time'].strftime("%H:%M")
        gha_str = f"{entry['GHA']:.1f}"
        dec_str = f"{entry['declination']:.1f}"
        sd_str = f"{entry.get('SD', 0.0):.1f}"
        hp_str = f"{entry.get('HP', 0.0):.1f}"
        hourly_rows.append(f"{time_str} & {gha_str} & {dec_str} & {sd_str} & {hp_str} \\\\ \\hline")
    
    # Prepare data for template
    template_data = {
        'date': date.strftime("%Y-%m-%d"),
        'celestial_body_name': body_name.capitalize(),
        'hourly_data_rows': "\n".join(hourly_rows),
        'semi_diameter': f"{hourly_data[0].get('SD', 0.0):.1f}",
        'horizontal_parallax': f"{hourly_data[0].get('HP', 0.0):.1f}",
        'magnitude': "N/A"  # Would need to add magnitude data
    }
    
    # Render template
    return _replace_placeholders(ALMANAC_PAGE_TEMPLATE, template_data)


def generate_multiple_sight_reduction_latex(problems: List[Dict], 
                                          vessel_speed: float = 0.0,
                                          vessel_course: float = 0.0) -> str:
    """
    Generate LaTeX code for multiple sight reduction problems (fix).
    
    Parameters:
    - problems: List of dictionaries containing sight reduction problem data
    - vessel_speed: Speed of vessel in knots (for running fixes)
    - vessel_course: Course of vessel in degrees
    
    Returns:
    - String containing LaTeX code for the multiple problem worksheet
    """
    # Prepare observations table
    observation_rows = []
    for problem in problems:
        body = problem['celestial_body_name'].capitalize()
        time_str = problem['observation_time'].datetime.strftime("%H:%M")
        alt_str = f"{problem['observed_altitude']:.1f}"
        temp_str = f"{problem['temperature']:.1f}"
        press_str = f"{problem['pressure']:.1f}"
        height_str = f"{problem['observer_height']:.1f}"
        observation_rows.append(f"{body} & {time_str} & {alt_str} & {temp_str} & {press_str} & {height_str} \\\\ \\hline")
    
    # Prepare data for template
    template_data = {
        'date': problems[0]['observation_time'].datetime.strftime("%Y-%m-%d"),
        'time_window': f"{len(problems)} observations",
        'vessel_speed': f"{vessel_speed:.1f}",
        'vessel_course': f"{vessel_course:.1f}",
        'observations_table': "\n".join(observation_rows)
    }
    
    # Add answer key (would include the calculated fix position)
    answer_sections = []
    for i, problem in enumerate(problems):
        answer_data = {
            'body': problem['celestial_body_name'].capitalize(),
            'computed_altitude': f"{problem.get('true_altitude', 0):.1f}",
            'azimuth': f"{problem.get('true_azimuth', 0):.1f}",
            'intercept': f"{abs(problem.get('intercept', 0)):.1f}",
            'intercept_direction': "Toward" if problem.get('intercept', 0) > 0 else "Away from"
        }
        answer_sections.append(
            f"\\textbf{{{answer_data['body']}}}: $H_c$ = {answer_data['computed_altitude']}, " +
            f"$Z_n$ = {answer_data['azimuth']}, " +
            f"Intercept = {answer_data['intercept']} {answer_data['intercept_direction']}"
        )
    
    template_data['answer_key'] = "\n\n".join(answer_sections)
    
    # Render template
    return _replace_placeholders(MULTIPLE_SIGHT_REDUCTION_TEMPLATE, template_data)


def compile_latex_to_pdf(latex_code: str, output_filename: str, 
                        output_dir: str = ".") -> str:
    """
    Compile LaTeX code to PDF using pdflatex.
    
    Parameters:
    - latex_code: String containing LaTeX code
    - output_filename: Name of output PDF file (without .pdf extension)
    - output_dir: Directory where to save the PDF
    
    Returns:
    - Path to the generated PDF file
    
    Raises:
    - RuntimeError: If LaTeX compilation fails
    """
    # Create temporary directory for compilation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write LaTeX code to file
        tex_file = os.path.join(temp_dir, f"{output_filename}.tex")
        with open(tex_file, 'w') as f:
            f.write(latex_code)
        
        # Compile LaTeX to PDF
        try:
            # Run pdflatex twice to ensure proper cross-references
            for i in range(2):
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', temp_dir,
                    f"{output_filename}.tex"
                ], cwd=temp_dir, capture_output=True, text=True, timeout=30)
                
                # Check if PDF was generated - continue even if there are warnings
                # because LaTeX often generates output despite warnings
                pdf_source = os.path.join(temp_dir, f"{output_filename}.pdf")
                if os.path.exists(pdf_source):
                    continue  # Continue to next iteration or finish
            
            # Copy PDF to output directory
            pdf_source = os.path.join(temp_dir, f"{output_filename}.pdf")
            pdf_dest = os.path.join(output_dir, f"{output_filename}.pdf")
            
            if os.path.exists(pdf_source):
                shutil.copy2(pdf_source, pdf_dest)
                return pdf_dest
            else:
                raise RuntimeError("PDF file was not generated")
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("LaTeX compilation timed out")
        except FileNotFoundError:
            raise RuntimeError("pdflatex not found. Please install a LaTeX distribution.")


def generate_problem_pdf(problem: Dict, output_filename: str,
                        output_dir: str = ".", include_answer_key: bool = False) -> str:
    """
    Generate a PDF worksheet for a single sight reduction problem.
    
    Parameters:
    - problem: Dictionary containing sight reduction problem data
    - output_filename: Name of output PDF file (without .pdf extension)
    - output_dir: Directory where to save the PDF
    - include_answer_key: Whether to include the answer key in the PDF
    
    Returns:
    - Path to the generated PDF file
    """
    # Generate LaTeX code
    latex_code = generate_sight_reduction_latex(problem, include_answer_key)
    
    # Compile to PDF
    return compile_latex_to_pdf(latex_code, output_filename, output_dir)


def generate_almanac_pdf(body_name: str, date: datetime, hourly_data: List[Dict],
                        output_filename: str, output_dir: str = ".") -> str:
    """
    Generate a PDF with almanac data for a celestial body.
    
    Parameters:
    - body_name: Name of the celestial body
    - date: Date for which to generate almanac data
    - hourly_data: List of dictionaries containing hourly almanac data
    - output_filename: Name of output PDF file (without .pdf extension)
    - output_dir: Directory where to save the PDF
    
    Returns:
    - Path to the generated PDF file
    """
    # Generate LaTeX code
    latex_code = generate_almanac_latex(body_name, date, hourly_data)
    
    # Compile to PDF
    return compile_latex_to_pdf(latex_code, output_filename, output_dir)


def generate_fix_pdf(problems: List[Dict], output_filename: str,
                    output_dir: str = ".", vessel_speed: float = 0.0,
                    vessel_course: float = 0.0) -> str:
    """
    Generate a PDF worksheet for a position fix from multiple sights.
    
    Parameters:
    - problems: List of dictionaries containing sight reduction problem data
    - output_filename: Name of output PDF file (without .pdf extension)
    - output_dir: Directory where to save the PDF
    - vessel_speed: Speed of vessel in knots (for running fixes)
    - vessel_course: Course of vessel in degrees
    
    Returns:
    - Path to the generated PDF file
    """
    # Generate LaTeX code
    latex_code = generate_multiple_sight_reduction_latex(problems, vessel_speed, vessel_course)
    
    # Compile to PDF
    return compile_latex_to_pdf(latex_code, output_filename, output_dir)


def generate_sight_reduction_booklet_latex(problem: Dict, 
                                          plot_path: str = None,
                                          almanac_pages: List[str] = None,
                                          include_answer_key: bool = False) -> str:
    """
    Generate LaTeX code for a sight reduction booklet with exercise, plot, annexes, and solutions.
    
    Parameters:
    - problem: Dictionary containing sight reduction problem data
    - plot_path: Path to the sight reduction plot image file
    - almanac_pages: List of LaTeX strings for almanac pages to include as annexes
    - include_answer_key: Whether to include the answer key in the booklet
    
    Returns:
    - String containing LaTeX code for the entire booklet
    """
    # Prepare data for template
    template_data = {
        'celestial_body_name': problem['celestial_body_name'].capitalize(),
        'limb_text': f" ({problem['limb']} limb)" if problem['celestial_body_name'] in ['sun', 'moon'] else "",
        'observation_time': format_time_for_latex(problem['observation_time'].datetime),
        'observed_altitude': f"{problem['observed_altitude']:.1f}\\\\textdegree",
        'temperature': f"{problem['temperature']:.1f}",
        'pressure': f"{problem['pressure']:.1f}",
        'observer_height': f"{problem['observer_height']:.1f}",
        'assumed_lat': format_angle_for_latex(problem['assumed_position'].lat.deg),
        'assumed_lon': format_lon_for_latex(problem['assumed_position'].lon.deg),
        'instrument_error': f"{problem['instrument_error']:.3f}\\\\textdegree",
        'index_error': f"{problem['index_error']:.3f}\\\\textdegree",
        'personal_error': f"{problem['personal_error']:.3f}\\\\textdegree"
    }
    
    # Handle plot inclusion
    if plot_path:
        template_data['plot_include'] = f"\\\\includegraphics[width=\\\\textwidth]{{{plot_path}}}"
    else:
        template_data['plot_include'] = "\\\\textit{Plot will be generated here}"  # No special handling needed for placeholder
    
    # Handle almanac annexes
    if almanac_pages:
        template_data['almanac_annexes'] = "\\\\\\\\\\n".join(almanac_pages)
    else:
        template_data['almanac_annexes'] = "\\\\textit{Relevant almanac pages and tables will be included here}"
    
    # Add additional tables (empty for now, can be extended)
    template_data['additional_tables'] = ""
    
    # Handle solutions
    if include_answer_key and problem.get('actual_position') is not None:
        answer_data = {
            'actual_lat': format_angle_for_latex(problem['actual_position'].lat.deg),
            'actual_lon': format_lon_for_latex(problem['actual_position'].lon.deg),
            'computed_altitude': f"{problem.get('true_altitude', 0):.1f}\\\\textdegree",
            'azimuth': f"{problem.get('true_azimuth', 0):.1f}\\\\textdegree",
            'intercept': f"{abs(problem.get('intercept', 0)):.1f}",
            'intercept_direction': "Toward" if problem.get('intercept', 0) > 0 else "Away from"
        }
        
        solution_content = f"""
\\subsection*{{Solution for {problem['celestial_body_name'].capitalize()}}}

\\begin{{tabular}}{{>{{\\bfseries}}lp{{10cm}}}}
Actual Position: & {answer_data['actual_lat']}, {answer_data['actual_lon']} \\\\
Computed Altitude ($H_c$): & {answer_data['computed_altitude']} \\\\
Azimuth ($Z_n$): & {answer_data['azimuth']} \\\\
Intercept ($a$): & {answer_data['intercept']} {answer_data['intercept_direction']} \\\\
\\end{{tabular}}

\\vspace{{1cm}}

\\textbf{{Steps to Solution:}}
\\begin{{enumerate}}
    \\item Calculate LHA = GHA - Assumed Longitude
    \\item Enter sight reduction tables with LHA, Assumed Latitude, and Declination
    \\item Extract $H_c$ and $Z$
    \\item Convert $Z$ to $Z_n$ based on hemisphere and LHA
    \\item Calculate intercept: $a = H_o - H_c$
\\end{{enumerate}}
        """
        template_data['solutions'] = solution_content
    else:
        template_data['solutions'] = f"\\subsection*{{Solution for {problem['celestial_body_name'].capitalize()}}} \n\n\\textit{{Worked solution will be included here}}"

    # Render template
    from .latex_templates import SIGHT_REDUCTION_BOOKLET_TEMPLATE
    return _replace_placeholders(SIGHT_REDUCTION_BOOKLET_TEMPLATE, template_data)


def generate_booklet_pdf(problem: Dict, output_filename: str,
                        output_dir: str = ".", plot_path: str = None,
                        almanac_pages: List[str] = None, 
                        include_answer_key: bool = False) -> str:
    """
    Generate a PDF booklet for sight reduction with exercise, plot, annexes, and solutions.
    
    Parameters:
    - problem: Dictionary containing sight reduction problem data
    - output_filename: Name of output PDF file (without .pdf extension)
    - output_dir: Directory where to save the PDF
    - plot_path: Path to the sight reduction plot image file
    - almanac_pages: List of LaTeX strings for almanac pages to include as annexes
    - include_answer_key: Whether to include the answer key in the PDF
    
    Returns:
    - Path to the generated PDF file
    """
    # Generate LaTeX code
    latex_code = generate_sight_reduction_booklet_latex(
        problem, 
        plot_path=plot_path,
        almanac_pages=almanac_pages,
        include_answer_key=include_answer_key
    )
    
    # Compile to PDF
    return compile_latex_to_pdf(latex_code, output_filename, output_dir)


def generate_almanac_annexes(bodies: List[str], date: datetime, hours: int = 24) -> List[str]:
    """
    Generate a list of almanac pages for use as annexes in the booklet.
    
    Parameters:
    - bodies: List of celestial body names to generate almanac data for
    - date: Date for which to generate almanac data
    - hours: Number of hours of data to include (default: 24)
    
    Returns:
    - List of strings containing LaTeX code for almanac annexes
    """
    from .almanac_integration import get_hourly_almanac_data
    from .latex_templates import ALMANAC_PAGE_TEMPLATE
    annexes = []
    
    for body in bodies:
        # Get hourly almanac data
        try:
            hourly_data = get_hourly_almanac_data(body, date, hours)
            
            # Convert to list of dictionaries
            hourly_list = []
            for _, row in hourly_data.iterrows():
                hourly_list.append({
                    'time': row['time'],
                    'GHA': row['GHA'],
                    'declination': row['declination'],
                    'SD': row.get('SD', 0.0),
                    'HP': row.get('HP', 0.0)
                })
            
            # Instead of using the full almanac template, just generate the content
            # that we need for the annex without the full document structure
            hourly_rows = []
            for entry in hourly_list:
                time_str = entry['time'].strftime("%H:%M")
                gha_str = f"{entry['GHA']:.1f}"
                dec_str = f"{entry['declination']:.1f}"
                sd_str = f"{entry.get('SD', 0.0):.1f}"
                hp_str = f"{entry.get('HP', 0.0):.1f}"
                # Fixed the escaping for the tabular environment
                hourly_rows.append(f"{time_str} & {gha_str} & {dec_str} & {sd_str} & {hp_str} \\\\\hline")
            
            # Prepare data for content, but only with the content parts we need
            hourly_data_rows = "\n".join(hourly_rows)
            
            # Create a simplified version for use as annex without document structure
            # Fixed the escaping to prevent "no line here to end" errors
            almanac_content = f"""\\subsubsection*{{Hourly Data for {body.capitalize()}}}

\\begin{{center}}
\\begin{{tabular}}{{|c|c|c|c|c|}}
\\hline
\\textbf{{Time}} & \\textbf{{GHA}} & \\textbf{{Dec}} & \\textbf{{SD}} & \\textbf{{HP}} \\\\
\\hline
{hourly_data_rows}
\\end{{tabular}}
\\end{{center}}

\\vspace{{0.5cm}}

\\textbf{{Additional Information:}}
\\begin{{itemize}}
    \\item GHA = Greenwich Hour Angle
    \\item Dec = Declination 
    \\item SD = Semi-Diameter
    \\item HP = Horizontal Parallax
\\end{{itemize}}""".strip()
            
            # Add the section header and the content
            # Make sure there are no extra formatting issues
            annexes.append(f"\\subsection*{{Almanac Data: {body.capitalize()}}}\n{almanac_content}")
        except Exception as e:
            print(f"Error generating almanac for {body}: {str(e)}")
            # Fallback to empty section
            annexes.append(f"\\subsection*{{Almanac Data: {body.capitalize()}}} \\textit{{Almanac data for {body} would appear here}}")
    
    return annexes


def generate_and_save_plot(problem: Dict, output_dir: str = ".", filename: str = "sight_plot.png") -> str:
    """
    Generate a sight reduction plot and save it to a file.
    
    Parameters:
    - problem: Dictionary containing sight reduction problem data
    - output_dir: Directory where to save the plot
    - filename: Name of the output file
    
    Returns:
    - Path to the generated plot file
    """
    from .plotting import create_line_of_position_plot
    
    # Extract required data from the problem
    assumed_lat = problem['assumed_position'].lat.deg
    assumed_lon = problem['assumed_position'].lon.deg
    intercept = problem.get('intercept', 0)  # This will be 0 if not calculated yet
    azimuth = problem.get('true_azimuth', 0)  # This will be 0 if not calculated yet
    
    # Generate the plot
    plot_path = os.path.join(output_dir, filename)
    fig = create_line_of_position_plot(
        intercept=intercept,
        azimuth=azimuth,
        assumed_lat=assumed_lat,
        assumed_lon=assumed_lon,
        save_path=plot_path,
        show_plot=False
    )
    
    return plot_path
