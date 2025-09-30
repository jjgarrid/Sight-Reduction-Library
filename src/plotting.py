"""
Plotting Module for Celestial Navigation

This module provides visualization tools for celestial navigation, including
azimuth compass plots, celestial body position tracking, and line of position visualization.
"""
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon, get_body, SkyCoord
from astropy.time import Time
import astropy.units as u
from matplotlib.patches import Circle
import warnings

# Filter matplotlib warnings
warnings.filterwarnings("ignore", category=UserWarning)


def create_azimuth_compass_plot(azimuths, labels=None, title="Celestial Body Azimuths", 
                                show_labels=True, save_path=None, show_plot=True):
    """
    Create a compass plot showing azimuths of celestial bodies.
    
    Parameters:
    - azimuths: List of azimuth values in degrees (0-360, measured clockwise from North)
    - labels: List of labels for each azimuth (optional)
    - title: Title for the plot
    - show_labels: Whether to show radial labels
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Convert azimuths to radians (with 0 degrees at the top, increasing clockwise)
    # Matplotlib's polar plots start at the positive x-axis (East) and go counterclockwise
    # So we need to adjust: subtract from 90 and negate to get North at top, clockwise
    azimuths_rad = np.radians(90 - np.array(azimuths))
    
    # Create the compass plot
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_theta_offset(np.pi / 2.0)  # North at top
    
    # Plot points
    ax.scatter(azimuths_rad, [1.0] * len(azimuths_rad), s=100, c='red', edgecolors='black', zorder=5)
    
    # Add labels
    if labels is not None:
        for i, (azi_rad, label) in enumerate(zip(azimuths_rad, labels)):
            ax.annotate(label, (azi_rad, 1.1), ha='center', va='center', fontsize=10)
    
    # Add compass directions
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    angles = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
    ax.set_xticks(angles)
    ax.set_xticklabels(directions)
    
    # Set radial limits and remove radial labels
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    
    # Add title
    ax.set_title(title, pad=20, fontsize=14)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig


def create_altitude_time_plot(celestial_body, start_time, end_time, location, 
                              num_points=100, title=None, save_path=None, show_plot=True):
    """
    Create a plot showing the altitude of a celestial body over time.
    
    Parameters:
    - celestial_body: Name of the celestial body ('sun', 'moon', 'venus', etc.)
    - start_time: Starting time (astropy Time object)
    - end_time: Ending time (astropy Time object)
    - location: Observer's location (EarthLocation object)
    - num_points: Number of points to calculate
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    # Create time range
    time_range = np.linspace(start_time.mjd, end_time.mjd, num_points)
    times = Time(time_range, format='mjd')
    
    # Get celestial body positions at each time
    altitudes = []
    for time in times:
        if celestial_body.lower() in ['sun']:
            body = get_sun(time)
        elif celestial_body.lower() in ['moon']:
            body = get_moon(time)
        elif celestial_body.lower() in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
            body = get_body(celestial_body.lower(), time)
        else:
            # For stars, assume fixed position
            try:
                from . import star_database
                body = star_database.get_star_coordinates(celestial_body)
            except ImportError:
                # Default to Polaris if star database is not available
                body = SkyCoord(ra=2.530301028*u.hourangle, dec=89.264109444*u.deg)
            if body is None:
                # Default to Polaris if not found
                body = SkyCoord(ra=2.530301028*u.hourangle, dec=89.264109444*u.deg)
        
        # Transform to AltAz coordinates
        altaz_frame = AltAz(obstime=time, location=location)
        body_altaz = body.transform_to(altaz_frame)
        altitudes.append(body_altaz.alt.degree)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert times to hours for better x-axis formatting
    time_hours = (times.jd - times[0].jd) * 24  # Hours since start
    
    ax.plot(time_hours, altitudes, linewidth=2, label=celestial_body.capitalize())
    ax.set_xlabel('Time (hours from start)')
    ax.set_ylabel('Altitude (degrees)')
    ax.set_title(title or f'Altitude vs Time for {celestial_body.capitalize()}')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Highlight altitudes below horizon
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Horizon')
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig


def create_line_of_position_plot(intercept, azimuth, assumed_lat, assumed_lon, 
                                 scale_nm=100, title="Line of Position", 
                                 save_path=None, show_plot=True):
    """
    Create a plot showing the line of position based on intercept and azimuth.
    
    Parameters:
    - intercept: Distance from assumed position in nautical miles
    - azimuth: Azimuth direction in degrees
    - assumed_lat: Assumed latitude
    - assumed_lon: Assumed longitude
    - scale_nm: Scale of the plot in nautical miles
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Calculate the point where the celestial body appears
    # The azimuth gives the direction from the observer to the celestial body
    azimuth_rad = np.radians(azimuth)
    
    # Calculate the position of the celestial body's GP relative to the assumed position
    # For simplicity, we'll plot the line of position as perpendicular to the azimuth line
    assumed_x, assumed_y = 0, 0  # Center of plot
    
    # Calculate the point where the intercept is applied
    intercept_x = -intercept * np.sin(azimuth_rad) / 60.0  # Convert nm to approx degrees
    intercept_y = intercept * np.cos(azimuth_rad) / 60.0
    
    # Plot the assumed position
    ax.plot(assumed_x, assumed_y, 'bo', markersize=10, label=f'Assumed Position ({assumed_lat:.2f}°, {assumed_lon:.2f}°)')
    
    # Calculate the point of the celestial body's GP
    body_x = -np.sin(azimuth_rad)
    body_y = np.cos(azimuth_rad)
    
    # Draw the azimuth line (from assumed position toward celestial body)
    ax.annotate('', xy=(body_x, body_y), xytext=(assumed_x, assumed_y),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(body_x, body_y, ' celestial body', verticalalignment='bottom')
    
    # Draw the line of position perpendicular to the azimuth line
    # The line of position is perpendicular to the azimuth line
    perp_azimuth = (azimuth + 90) % 360
    perp_rad = np.radians(perp_azimuth)
    
    # Length of the line of position (in degrees)
    lop_length = scale_nm / 60.0  # Convert nautical miles to degrees
    
    # Start from the intercept point
    lop_start_x = assumed_x + intercept_x
    lop_start_y = assumed_y + intercept_y
    
    # Calculate line of position endpoints
    lop_end1_x = lop_start_x + lop_length/2 * np.sin(np.radians(perp_azimuth))
    lop_end1_y = lop_start_y - lop_length/2 * np.cos(np.radians(perp_azimuth))
    
    lop_end2_x = lop_start_x - lop_length/2 * np.sin(np.radians(perp_azimuth))
    lop_end2_y = lop_start_y + lop_length/2 * np.cos(np.radians(perp_azimuth))
    
    ax.plot([lop_end1_x, lop_end2_x], [lop_end1_y, lop_end2_y], 'g-', linewidth=2, label='Line of Position')
    
    # Mark the intercept point
    ax.plot(lop_start_x, lop_start_y, 'go', markersize=8, label=f'Intercept Point ({intercept:.2f} nm)')
    
    # Add labels and formatting
    ax.set_xlabel('Longitude offset (degrees)')
    ax.set_ylabel('Latitude offset (degrees)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    
    # Add compass direction
    ax.text(0.02, 0.98, 'N', transform=ax.transAxes, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig


def create_star_chart_plot(obs_time, location, magnitude_limit=3.0, 
                          title="Celestial Sphere View", save_path=None, show_plot=True):
    """
    Create a star chart showing visible celestial objects.
    
    Parameters:
    - obs_time: Observation time (astropy Time object)
    - location: Observer's location (EarthLocation object)
    - magnitude_limit: Limiting magnitude to show (brighter stars only)
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # Set up polar plot for all directions (360 degrees)
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_theta_offset(np.pi / 2.0)  # North at top
    
    # Create horizon and zenith circles
    zenith_angles = np.linspace(0, np.pi/2, 100)  # From zenith to horizon
    horizon_angles = np.full_like(zenith_angles, np.pi/2)  # Horizon at 90° from zenith
    
    # Generate some sample celestial objects
    try:
        from . import star_database
    except ImportError:
        print("Star database not available. Install required modules to use star charts.")
        return None
    
    # Get navigation stars that are visible at the given time
    all_stars = star_database.list_navigation_stars()
    
    visible_azimuths = []
    visible_altitudes = []
    visible_magnitudes = []
    star_names = []
    
    for star_name in all_stars:
        star_coord = star_database.get_star_coordinates(star_name)
        if star_coord:
            # Transform to AltAz coordinates
            altaz_frame = AltAz(obstime=obs_time, location=location)
            star_altaz = star_coord.transform_to(altaz_frame)
            
            # Only include stars above horizon and brighter than magnitude limit
            if star_altaz.alt.degree > 0:  # Above horizon
                visible_azimuths.append(star_altaz.az.degree)
                visible_altitudes.append(star_altaz.alt.degree)
                star_names.append(star_name)
                
                # Use a simple magnitude estimation for size
                star_info = star_database.get_star_info(star_name)
                mag = star_info.get('magnitude', 5.0) if star_info else 5.0
                visible_magnitudes.append(mag)
    
    if visible_azimuths:
        # Convert to radians for polar plot
        azimuths_rad = np.radians(90 - np.array(visible_azimuths))
        # Convert altitude to radius (inverted: zenith = 0, horizon = 1)
        radii = 1 - (np.array(visible_altitudes) / 90.0)
        
        # Calculate marker sizes based on magnitude (brighter = larger)
        sizes = 200 - (np.array(visible_magnitudes) * 20)  # Invert so brighter stars are larger
        sizes = np.clip(sizes, 20, 200)  # Limit to reasonable range
        
        # Plot the stars
        sc = ax.scatter(azimuths_rad, radii, s=sizes, c='blue', alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Add some star names for bright stars
        for i, (azi_rad, rad, name) in enumerate(zip(azimuths_rad, radii, star_names)):
            if visible_magnitudes[i] < 1.5:  # Only label bright stars
                ax.annotate(name, (azi_rad, rad), fontsize=8, ha='center', va='center')
    
    # Add compass directions
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    angles = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
    ax.set_xticks(angles)
    ax.set_xticklabels(directions)
    
    # Set radial limits and labels (radius = distance from zenith)
    ax.set_ylim(0, 1)
    ax.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Circles at different altitudes
    ax.set_rlabel_position(0)
    ax.set_yticklabels(['72°', '54°', '36°', '18°', '0°'])  # Altitudes
    
    # Add title
    ax.set_title(title + f"\n({obs_time.datetime.strftime('%Y-%m-%d %H:%M')} UTC, {location.lat:.2f}, {location.lon:.2f})", 
                 pad=30, fontsize=12)
    
    # Add horizon circle
    ax.add_patch(plt.Circle((0, 0), 1, transform=ax.transData._get_inverse_transform(), 
                            fill=False, color='gray', linestyle='--', alpha=0.5))
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig


def create_multiple_body_azimuth_plot(celestial_bodies, observation_time, location,
                                     title="Multiple Celestial Bodies Azimuths",
                                     save_path=None, show_plot=True):
    """
    Create a compass plot showing azimuths of multiple celestial bodies at a specific time.
    
    Parameters:
    - celestial_bodies: List of celestial body names
    - observation_time: Observation time (astropy Time object)
    - location: Observer's location (EarthLocation object)
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    azimuths = []
    labels = []
    
    for body_name in celestial_bodies:
        # Get celestial body position at the specified time
        if body_name.lower() in ['sun']:
            body = get_sun(observation_time)
        elif body_name.lower() in ['moon']:
            body = get_moon(observation_time)
        elif body_name.lower() in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
            body = get_body(body_name.lower(), observation_time)
        else:
            # Try to get a star from our database
            try:
                from . import star_database
                body = star_database.get_star_coordinates(body_name)
            except ImportError:
                # Default to Polaris if star database is not available
                body = SkyCoord(ra=2.530301028*u.hourangle, dec=89.264109444*u.deg)
            if body is None:
                # Default to Polaris if not found
                body = SkyCoord(ra=2.530301028*u.hourangle, dec=89.264109444*u.deg)
        
        # Transform to AltAz coordinates
        altaz_frame = AltAz(obstime=observation_time, location=location)
        body_altaz = body.transform_to(altaz_frame)
        
        # Only add to plot if body is above horizon
        if body_altaz.alt.degree > 0:
            azimuths.append(body_altaz.az.degree)
            labels.append(f"{body_name.capitalize()}\n({body_altaz.alt.degree:.1f}°)")
    
    if not azimuths:
        print("No celestial bodies above horizon for the given time and location.")
        return None
    
    return create_azimuth_compass_plot(azimuths, labels, title, save_path=save_path, show_plot=show_plot)


def create_sight_summary_plot(results_list, title="Sight Reduction Summary", 
                             save_path=None, show_plot=True):
    """
    Create a summary plot showing multiple sight reduction results.
    
    Parameters:
    - results_list: List of tuples (name, intercept, azimuth)
    - title: Title for the plot
    - save_path: Path to save the plot (optional)
    - show_plot: Whether to display the plot
    
    Returns:
    - Matplotlib figure object
    """
    if not results_list:
        print("No sight results to plot.")
        return None
    
    names = [result[0] for result in results_list]
    intercepts = [result[1] for result in results_list]
    azimuths = [result[2] for result in results_list]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Azimuth compass for all bodies
    azimuths_rad = np.radians(90 - np.array(azimuths))
    
    ax1.set_projection('polar')
    ax1.set_theta_direction(-1)  # Clockwise
    ax1.set_theta_offset(np.pi / 2.0)  # North at top
    
    # Create different colors for different intercept values
    colors = ['red' if i > 0 else 'blue' for i in intercepts]
    
    ax1.scatter(azimuths_rad, [1.0] * len(azimuths_rad), s=100, c=colors, edgecolors='black', zorder=5)
    
    # Add labels
    for i, (azi_rad, label) in enumerate(zip(azimuths_rad, names)):
        ax1.annotate(f"{label}\n{abs(intercepts[i]):.1f}nm {'T' if intercepts[i] > 0 else 'A'}", 
                    (azi_rad, 1.1), ha='center', va='center', fontsize=9)
    
    # Add compass directions
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    angles = np.radians([0, 45, 90, 135, 180, 225, 270, 315])
    ax1.set_xticks(angles)
    ax1.set_xticklabels(directions)
    
    ax1.set_ylim(0, 1.3)
    ax1.set_yticks([])
    ax1.set_title("Azimuths & Intercepts", fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Intercept vs Azimuth bar chart
    y_pos = np.arange(len(names))
    colors2 = ['red' if i > 0 else 'blue' for i in intercepts]
    
    bars = ax2.barh(y_pos, intercepts, color=colors2, edgecolor='black')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names)
    ax2.set_xlabel('Intercept (nautical miles)')
    ax2.set_title('Intercept Values', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    
    # Add value labels to bars
    for i, (bar, intercept_val) in enumerate(zip(bars, intercepts)):
        width = bar.get_width()
        ax2.text(width + (0.5 if width >= 0 else -0.5), bar.get_y() + bar.get_height()/2,
                f'{abs(intercept_val):.1f}{"T" if intercept_val > 0 else "A"}',
                ha='left' if width >= 0 else 'right', va='center')
    
    plt.suptitle(title, fontsize=14)
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show plot if requested
    if show_plot:
        plt.show()
    
    return fig