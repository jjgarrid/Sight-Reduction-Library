"""
Command Line Interface for Sight Reduction with LaTeX Output

This module provides a command-line interface for generating
celestial navigation problems with LaTeX/PDF output.
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astropy.time import Time
from src.problem_generator import (
    generate_sight_reduction_problem,
    generate_morning_sight_problem,
    generate_evening_sight_problem,
    generate_twilight_star_sight_problem,
    generate_moon_sight_problem,
    generate_multi_body_sight_reduction_problems
)
from src.latex_output import (
    generate_problem_pdf,
    generate_almanac_pdf,
    generate_fix_pdf
)
from src.almanac_integration import get_hourly_almanac_data


def create_parser():
    """Create argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='sight-reduction-latex',
        description='Generate celestial navigation problems with LaTeX/PDF output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a morning sight problem PDF
  sight-reduction-latex generate morning --output morning_sight.pdf
  
  # Generate a fix from 3 sights with PDF output
  sight-reduction-latex generate fix --bodies 3 --output fix.pdf
  
  # Generate almanac page for the Sun
  sight-reduction-latex almanac sun --date 2023-06-15 --output sun_almanac.pdf
  
  # Generate a custom sight problem with specific parameters
  sight-reduction-latex generate custom --body sun --time "2023-06-15T12:00:00" --output custom_sight.pdf
        """
    )
    
    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate navigation problems')
    generate_subparsers = generate_parser.add_subparsers(dest='type', help='Type of problem to generate')
    
    # Morning sight generation
    morning_parser = generate_subparsers.add_parser('morning', help='Generate morning sight problem')
    morning_parser.add_argument('--output', '-o', default='morning_sight.pdf', 
                               help='Output PDF filename (default: morning_sight.pdf)')
    morning_parser.add_argument('--with-answers', action='store_true',
                               help='Include answer key in PDF')
    morning_parser.add_argument('--output-dir', default='.', 
                               help='Output directory (default: current directory)')
    
    # Evening sight generation
    evening_parser = generate_subparsers.add_parser('evening', help='Generate evening sight problem')
    evening_parser.add_argument('--output', '-o', default='evening_sight.pdf', 
                               help='Output PDF filename (default: evening_sight.pdf)')
    evening_parser.add_argument('--with-answers', action='store_true',
                               help='Include answer key in PDF')
    evening_parser.add_argument('--output-dir', default='.', 
                               help='Output directory (default: current directory)')
    
    # Star sight generation
    star_parser = generate_subparsers.add_parser('star', help='Generate star sight problem')
    star_parser.add_argument('--star-name', default=None,
                            help='Specific star name (default: random selection)')
    star_parser.add_argument('--output', '-o', default='star_sight.pdf', 
                             help='Output PDF filename (default: star_sight.pdf)')
    star_parser.add_argument('--with-answers', action='store_true',
                             help='Include answer key in PDF')
    star_parser.add_argument('--output-dir', default='.', 
                             help='Output directory (default: current directory)')
    
    # Moon sight generation
    moon_parser = generate_subparsers.add_parser('moon', help='Generate moon sight problem')
    moon_parser.add_argument('--output', '-o', default='moon_sight.pdf', 
                            help='Output PDF filename (default: moon_sight.pdf)')
    moon_parser.add_argument('--with-answers', action='store_true',
                            help='Include answer key in PDF')
    moon_parser.add_argument('--output-dir', default='.', 
                            help='Output directory (default: current directory)')
    
    # Fix (multiple sights) generation
    fix_parser = generate_subparsers.add_parser('fix', help='Generate position fix from multiple sights')
    fix_parser.add_argument('--bodies', '-b', type=int, default=3,
                           help='Number of celestial bodies (default: 3)')
    fix_parser.add_argument('--time-window', type=float, default=2.0,
                            help='Time window in hours (default: 2.0)')
    fix_parser.add_argument('--vessel-speed', type=float, default=0.0,
                            help='Vessel speed in knots for running fix (default: 0.0)')
    fix_parser.add_argument('--vessel-course', type=float, default=0.0,
                            help='Vessel course in degrees for running fix (default: 0.0)')
    fix_parser.add_argument('--navigation-mode', default='marine',
                           choices=['marine', 'aviation'],
                           help='Navigation mode: marine or aviation (default: marine)')
    fix_parser.add_argument('--aircraft-altitude', type=float, default=0.0,
                           help='Aircraft altitude in meters (for aviation mode)')
    fix_parser.add_argument('--aircraft-speed', type=float, default=0.0,
                           help='Aircraft speed in knots (for aviation mode)')
    fix_parser.add_argument('--aircraft-course', type=float, default=0.0,
                           help='Aircraft course in degrees (for aviation mode)')
    fix_parser.add_argument('--output', '-o', default='position_fix.pdf', 
                            help='Output PDF filename (default: position_fix.pdf)')
    fix_parser.add_argument('--with-answers', action='store_true',
                            help='Include answer key in PDF')
    fix_parser.add_argument('--output-dir', default='.', 
                            help='Output directory (default: current directory)')
    
    # Custom sight generation
    custom_parser = generate_subparsers.add_parser('custom', help='Generate custom sight problem')
    custom_parser.add_argument('--body', required=True,
                              help='Celestial body name (sun, moon, venus, etc.)')
    custom_parser.add_argument('--time', required=True,
                              help='Observation time (YYYY-MM-DDTHH:MM:SS)')
    custom_parser.add_argument('--navigation-mode', default='marine',
                              choices=['marine', 'aviation'],
                              help='Navigation mode: marine or aviation (default: marine)')
    custom_parser.add_argument('--aircraft-altitude', type=float, default=0.0,
                              help='Aircraft altitude in meters (for aviation mode)')
    custom_parser.add_argument('--aircraft-speed', type=float, default=0.0,
                              help='Aircraft speed in knots (for aviation mode)')
    custom_parser.add_argument('--aircraft-course', type=float, default=0.0,
                              help='Aircraft course in degrees (for aviation mode)')
    custom_parser.add_argument('--time-interval', type=float, default=0.0,
                              help='Time interval from reference in hours (for aviation mode)')
    custom_parser.add_argument('--output', '-o', default='custom_sight.pdf', 
                               help='Output PDF filename (default: custom_sight.pdf)')
    custom_parser.add_argument('--with-answers', action='store_true',
                               help='Include answer key in PDF')
    custom_parser.add_argument('--output-dir', default='.', 
                               help='Output directory (default: current directory)')
    
    # Almanac command
    almanac_parser = subparsers.add_parser('almanac', help='Generate almanac pages')
    almanac_parser.add_argument('body', help='Celestial body name (sun, moon, venus, etc.)')
    almanac_parser.add_argument('--date', default=None,
                               help='Date for almanac data (YYYY-MM-DD, default: today)')
    almanac_parser.add_argument('--hours', type=int, default=24,
                               help='Number of hours of data (default: 24)')
    almanac_parser.add_argument('--output', '-o', default=None, 
                               help='Output PDF filename (default: {body}_almanac_{date}.pdf)')
    almanac_parser.add_argument('--output-dir', default='.', 
                               help='Output directory (default: current directory)')
    
    return parser


def handle_generate_morning(args):
    """Handle generation of morning sight problem."""
    print(f"Generating morning sight problem...")
    
    # Generate the problem
    problem = generate_morning_sight_problem()
    
    # Generate PDF
    output_path = generate_problem_pdf(
        problem=problem,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        include_answer_key=args.with_answers
    )
    
    print(f"Morning sight problem generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_evening(args):
    """Handle generation of evening sight problem."""
    print(f"Generating evening sight problem...")
    
    # Generate the problem
    problem = generate_evening_sight_problem()
    
    # Generate PDF
    output_path = generate_problem_pdf(
        problem=problem,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        include_answer_key=args.with_answers
    )
    
    print(f"Evening sight problem generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_star(args):
    """Handle generation of star sight problem."""
    print(f"Generating star sight problem...")
    
    # Generate the problem
    problem = generate_twilight_star_sight_problem(star_name=args.star_name)
    
    # Generate PDF
    output_path = generate_problem_pdf(
        problem=problem,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        include_answer_key=args.with_answers
    )
    
    print(f"Star sight problem generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_moon(args):
    """Handle generation of moon sight problem."""
    print(f"Generating moon sight problem...")
    
    # Generate the problem
    problem = generate_moon_sight_problem()
    
    # Generate PDF
    output_path = generate_problem_pdf(
        problem=problem,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        include_answer_key=args.with_answers
    )
    
    print(f"Moon sight problem generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_fix(args):
    """Handle generation of position fix from multiple sights."""
    print(f"Generating position fix from {args.bodies} sights...")
    
    # Generate the problems with navigation mode and aviation parameters
    problems = generate_multi_body_sight_reduction_problems(
        num_bodies=args.bodies,
        time_window_hours=args.time_window,
        navigation_mode=args.navigation_mode,
        aircraft_altitude=args.aircraft_altitude
    )
    
    # Generate PDF
    output_path = generate_fix_pdf(
        problems=problems,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        vessel_speed=args.vessel_speed,
        vessel_course=args.vessel_course
    )
    
    print(f"Position fix generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_custom(args):
    """Handle generation of custom sight problem."""
    print(f"Generating custom sight problem for {args.body}...")
    
    # Parse the time
    try:
        observation_time = Time(args.time)
    except Exception as e:
        print(f"Error parsing time: {e}")
        return None
    
    # Generate the problem with navigation mode and aviation parameters
    problem = generate_sight_reduction_problem(
        celestial_body_name=args.body,
        observation_time=observation_time,
        navigation_mode=args.navigation_mode,
        aircraft_altitude=args.aircraft_altitude
    )
    
    # Generate PDF
    output_path = generate_problem_pdf(
        problem=problem,
        output_filename=args.output.replace('.pdf', ''),
        output_dir=args.output_dir,
        include_answer_key=args.with_answers
    )
    
    print(f"Custom sight problem generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def handle_generate_almanac(args):
    """Handle generation of almanac pages."""
    print(f"Generating almanac page for {args.body}...")
    
    # Parse the date
    if args.date:
        try:
            date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format. Use YYYY-MM-DD.")
            return None
    else:
        date = datetime.now()
    
    # Get hourly almanac data
    hourly_data = get_hourly_almanac_data(args.body, date, args.hours)
    
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
    
    # Generate output filename if not provided
    if not args.output:
        output_filename = f"{args.body}_almanac_{date.strftime('%Y%m%d')}.pdf"
    else:
        output_filename = args.output
    
    # Generate PDF
    output_path = generate_almanac_pdf(
        body_name=args.body,
        date=date,
        hourly_data=hourly_list,
        output_filename=output_filename.replace('.pdf', ''),
        output_dir=args.output_dir
    )
    
    print(f"Almanac page generated successfully!")
    print(f"PDF saved to: {output_path}")
    return output_path


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Check if a command was provided
    if not hasattr(args, 'command') or args.command is None:
        parser.print_help()
        return
    
    try:
        if args.command == 'generate':
            if args.type == 'morning':
                handle_generate_morning(args)
            elif args.type == 'evening':
                handle_generate_evening(args)
            elif args.type == 'star':
                handle_generate_star(args)
            elif args.type == 'moon':
                handle_generate_moon(args)
            elif args.type == 'fix':
                handle_generate_fix(args)
            elif args.type == 'custom':
                handle_generate_custom(args)
            else:
                parser.print_help()
        
        elif args.command == 'almanac':
            handle_generate_almanac(args)
        
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()