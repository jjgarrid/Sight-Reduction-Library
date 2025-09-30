"""
Advanced Position Fix Calculation Module for Celestial Navigation

This module provides functions for calculating advanced position fixes using
least squares methods and error analysis.
"""

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
from typing import List, Dict, Tuple, Optional
from scipy.optimize import least_squares
import math


def calculate_least_squares_fix(sights: List[Dict]) -> Dict:
    """
    Calculate position fix using least squares method from multiple sight observations.
    
    Parameters:
    - sights: List of sight observations, each with keys:
              'observed_altitude', 'celestial_body_name', 'observation_time',
              'intercept', 'azimuth', 'assumed_position', 'altitude_correction_error'
    
    Returns:
    - Dictionary containing the calculated position fix and associated data
    """
    if len(sights) < 2:
        raise ValueError("At least 2 sights are required for a position fix")
    
    # Extract azimuths and intercepts from sights
    azimuths = np.array([math.radians(sight['azimuth']) for sight in sights])
    intercepts = np.array([sight['intercept'] for sight in sights])
    
    # Calculate initial position estimate as average of assumed positions
    avg_lat = np.mean([sight['assumed_position'].lat.value for sight in sights])
    avg_lon = np.mean([sight['assumed_position'].lon.value for sight in sights])
    
    # Use least squares to find best position
    def residuals(position_params):
        """
        Calculate residuals between observed and calculated intercepts
        for the given position (lat, lon).
        """
        lat, lon = position_params
        residuals = []
        
        for i, sight in enumerate(sights):
            # Calculate the difference between current position and intercept position
            # along the azimuth line
            az_rad = azimuths[i]
            
            # Calculate the change in intercept based on position change
            # This is a simplified linear approximation for small position changes
            delta_lat = lat - sight['assumed_position'].lat.value
            delta_lon = lon - sight['assumed_position'].lon.value
            
            # Project the position difference onto the intercept vector
            # (perpendicular to azimuth line)
            azimuth_correction = delta_lat * math.cos(az_rad) + delta_lon * math.sin(az_rad) * math.cos(math.radians(lat))
            
            # The residual is the difference between expected and actual intercept
            residual = intercepts[i] - azimuth_correction
            residuals.append(residual)
        
        return np.array(residuals)
    
    # Initial guess for position (in degrees)
    initial_position = [avg_lat, avg_lon]
    
    # Perform least squares optimization
    result = least_squares(residuals, initial_position)
    
    # Extract the calculated position
    fix_lat, fix_lon = result.x
    
    # Calculate error statistics
    residuals_final = result.fun
    rmse = np.sqrt(np.mean(residuals_final**2))  # Root mean square error
    
    # Calculate geometric factor (how well the azimuths intersect)
    azimuths_deg = np.array([sight['azimuth'] for sight in sights])
    geometric_factor = calculate_geometric_factor(azimuths_deg)
    
    # Calculate error ellipse parameters
    error_ellipse = calculate_error_ellipse(sights, result.jac)
    
    # Determine fix quality based on geometric factor and rmse
    fix_quality = assess_fix_quality(geometric_factor, rmse)
    
    return {
        'fix_position': EarthLocation(lat=fix_lat*u.deg, lon=fix_lon*u.deg, height=0*u.m),
        'fix_accuracy_nm': rmse,  # Approximate accuracy in nautical miles
        'error_ellipse': error_ellipse,
        'fix_quality': fix_quality,
        'geometric_factor': geometric_factor,
        'residual_errors': residuals_final.tolist(),
        'number_of_sights': len(sights),
        'solution_converged': result.success
    }


def calculate_running_fix(sights: List[Dict], vessel_speed: float, vessel_course: float) -> Dict:
    """
    Calculate a running fix by accounting for vessel movement between observations.
    
    Parameters:
    - sights: List of sight observations with time information
    - vessel_speed: Speed of the vessel in knots
    - vessel_course: Course of the vessel in degrees True
    
    Returns:
    - Dictionary containing the calculated running fix
    """
    if len(sights) < 2:
        raise ValueError("At least 2 sights are required for a running fix")
    
    # Sort sights by time
    sorted_sights = sorted(sights, key=lambda x: x['observation_time'].jd)
    
    # Calculate the first sight as reference
    reference_time = sorted_sights[0]['observation_time']
    
    # Adjust each line of position for vessel movement since the reference time
    adjusted_sights = []
    for sight in sorted_sights:
        # Calculate time difference from reference
        time_diff_hours = (sight['observation_time'].jd - reference_time.jd) * 24
        
        # Calculate vessel movement in nautical miles
        distance_travelled = vessel_speed * time_diff_hours
        
        # Calculate position shift based on course
        dlat = distance_travelled * math.cos(math.radians(vessel_course)) / 60  # Convert to degrees
        dlon = distance_travelled * math.sin(math.radians(vessel_course)) / (60 * math.cos(math.radians(sight['assumed_position'].lat.value)))  # Convert to degrees
        
        # Adjust the assumed position for this sight
        adj_lat = sight['assumed_position'].lat.value - dlat
        adj_lon = sight['assumed_position'].lon.value - dlon
        
        # Create adjusted sight
        adjusted_sight = sight.copy()
        adjusted_sight['assumed_position'] = EarthLocation(lat=adj_lat*u.deg, lon=adj_lon*u.deg, height=0*u.m)
        
        # Adjust the intercept as well based on the position change
        # For the running fix, we need to calculate how the intercept changes
        # due to the position movement along the azimuth
        az_rad = math.radians(sight['azimuth'])
        az_lat_diff = distance_travelled * math.cos(az_rad) / 60
        az_lon_diff = distance_travelled * math.sin(az_rad) / (60 * math.cos(math.radians(adj_lat)))
        
        # For simplicity, the intercept adjustment is approximated
        adjusted_intercept = sight['intercept']  # In practice, this would be more complex
        
        adjusted_sight['intercept'] = adjusted_intercept
        adjusted_sights.append(adjusted_sight)
    
    # Now calculate the fix with the adjusted sights
    return calculate_least_squares_fix(adjusted_sights)


def calculate_error_ellipse(sights: List[Dict], jacobian: Optional[np.ndarray] = None) -> Dict:
    """
    Calculate error ellipse parameters from the observed sights.
    
    Parameters:
    - sights: List of sight observations
    - jacobian: Jacobian matrix from least squares optimization
    
    Returns:
    - Dictionary containing error ellipse parameters
    """
    # If Jacobian is not provided, we'll estimate using simple geometric approach
    if jacobian is not None:
        # Calculate covariance matrix from Jacobian
        # For a least squares problem: covariance = (J^T * J)^(-1) * sigma^2
        try:
            jtj_inv = np.linalg.inv(jacobian.T @ jacobian)
            # Variance estimate (simplified)
            variance = 1.0  # This would be estimated from residual errors in practice
            covariance_matrix = jtj_inv * variance
            
            # Calculate eigenvalues and eigenvectors for error ellipse
            eigenvals, eigenvecs = np.linalg.eigh(covariance_matrix)
            
            # Semi-major and semi-minor axes
            semi_major = math.sqrt(max(eigenvals))
            semi_minor = math.sqrt(min(eigenvals))
            
            # Orientation (angle of major axis from North)
            major_axis_idx = np.argmax(eigenvals)
            orientation_rad = math.atan2(eigenvecs[1, major_axis_idx], eigenvecs[0, major_axis_idx])
            orientation_deg = math.degrees(orientation_rad) % 360
            
        except np.linalg.LinAlgError:
            # Fallback calculation if matrix is singular
            semi_major = 1.0  # nautical miles
            semi_minor = 0.5
            orientation_deg = 0.0
    else:
        # Fallback geometric calculation
        azimuths = [math.radians(sight['azimuth']) for sight in sights]
        n = len(azimuths)
        
        # Use geometric method to estimate error ellipse
        # This is a simplified approach based on azimuth distribution
        if n < 2:
            semi_major = 2.0
            semi_minor = 1.0
            orientation_deg = 0.0
        else:
            # Calculate the sum of squared sines/cosines for geometric strength
            sum_cos2 = sum(math.cos(2*a) for a in azimuths)
            sum_sin2 = sum(math.sin(2*a) for a in azimuths)
            
            # Simplified error analysis - in practice, this would use measurement uncertainties
            # and geometric factors
            azimuths_deg = np.array([sight['azimuth'] for sight in sights])
            geometric_factor = calculate_geometric_factor(azimuths_deg)
            base_error = 1.0  # Base uncertainty in nautical miles
            
            # Error is inversely proportional to geometric strength
            semi_major = base_error / max(geometric_factor, 0.1)  # Prevent division by zero
            semi_minor = semi_major * 0.5  # Assume ellipse ratio of 2:1 as default
            orientation_deg = 0.0  # Simplified orientation
    
    return {
        'semi_major_axis_nm': semi_major,
        'semi_minor_axis_nm': semi_minor,
        'orientation_deg': orientation_deg,
        'confidence_level': 0.95  # 95% confidence level
    }


def calculate_geometric_factor(azimuths: np.ndarray) -> float:
    """
    Calculate geometric factor indicating the quality of sight combination.
    A higher factor indicates better geometric intersection of position lines.
    
    Parameters:
    - azimuths: Array of azimuths in degrees
    
    Returns:
    - Geometric factor (higher is better)
    """
    n = len(azimuths)
    if n < 2:
        return 0.0
    
    # Convert to radians
    az_rads = np.radians(azimuths)
    
    # Calculate the determinant of the geometry matrix
    # This is a simplified approach; the full calculation involves more complex matrices
    A = np.column_stack([np.cos(az_rads), np.sin(az_rads)])
    G = A.T @ A
    
    # The geometric factor is related to the determinant of G
    # det(G) = 0 means lines are parallel, larger values indicate better geometry
    try:
        det_G = np.linalg.det(G)
        trace_G = np.trace(G)  # Sum of diagonal elements
        
        # Normalize by the number of sights for comparison across different numbers of sights
        geometric_factor = det_G / (trace_G + 1e-10)  # Add small value to avoid division by zero
        
        # Take absolute value and scale appropriately
        geometric_factor = abs(geometric_factor) * 100
        
        # In some cases, we might want to use the condition number
        # condition = np.linalg.cond(G)
        # geometric_factor = 1 / (condition + 1e-10)
        
    except np.linalg.LinAlgError:
        geometric_factor = 0.0
    
    return geometric_factor


def assess_fix_quality(geometric_factor: float, rmse: float) -> str:
    """
    Assess the quality of the position fix.
    
    Parameters:
    - geometric_factor: Geometric strength of the sight combination
    - rmse: Root mean square error of the solution
    
    Returns:
    - Quality assessment as a string
    """
    # Define thresholds for different quality levels
    if geometric_factor > 10 and rmse < 0.5:
        return "Excellent"
    elif geometric_factor > 5 and rmse < 1.0:
        return "Good"
    elif geometric_factor > 2 and rmse < 2.0:
        return "Fair"
    else:
        return "Poor"


def calculate_single_line_of_position(azimuth: float, intercept: float, assumed_position: EarthLocation) -> Tuple[float, float]:
    """
    Calculate the end points of a line of position for plotting purposes.
    
    Parameters:
    - azimuth: Azimuth of the celestial body in degrees
    - intercept: Intercept in nautical miles
    - assumed_position: Assumed position
    
    Returns:
    - Tuple of (lat, lon) coordinates for plotting the LOP
    """
    # Calculate the position of the celestial body GP relative to the assumed position
    az_rad = math.radians(azimuth)
    
    # Move from assumed position along the azimuth by the intercept distance
    # This gives us a point on the line of position
    lat_assumed = assumed_position.lat.value
    lon_assumed = assumed_position.lon.value
    
    # Calculate the end points of the LOP segment
    # LOP is perpendicular to the azimuth line
    perp_az1 = (azimuth + 90) % 360
    perp_az2 = (azimuth - 90) % 360
    
    # Calculate positions 5 nautical miles in each perpendicular direction
    lop_lat1, lop_lon1 = calculate_position_on_lop(lat_assumed, lon_assumed, perp_az1, 5.0)
    lop_lat2, lop_lon2 = calculate_position_on_lop(lat_assumed, lon_assumed, perp_az2, 5.0)
    
    return (lop_lat1, lop_lon1, lop_lat2, lop_lon2)


def calculate_position_on_lop(lat: float, lon: float, azimuth: float, distance_nm: float) -> Tuple[float, float]:
    """
    Calculate a new position given an initial position, azimuth, and distance.
    
    Parameters:
    - lat: Initial latitude in degrees
    - lon: Initial longitude in degrees
    - azimuth: Direction in degrees
    - distance_nm: Distance in nautical miles
    
    Returns:
    - Tuple of (new_latitude, new_longitude)
    """
    # Convert to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    az_rad = math.radians(azimuth)
    
    # Convert distance to angular distance (1 nautical mile = 1 arc minute)
    angular_distance = distance_nm / 60.0  # in degrees
    ang_dist_rad = math.radians(angular_distance)
    
    # Calculate new latitude
    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(ang_dist_rad) + 
        math.cos(lat_rad) * math.sin(ang_dist_rad) * math.cos(az_rad)
    )
    
    # Calculate new longitude
    delta_lon = math.atan2(
        math.sin(az_rad) * math.sin(ang_dist_rad) * math.cos(lat_rad),
        math.cos(ang_dist_rad) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )
    
    new_lon_rad = lon_rad + delta_lon
    
    # Normalize longitude to [-180, 180]
    new_lon_rad = math.fmod(new_lon_rad + math.pi, 2 * math.pi)
    if new_lon_rad < 0:
        new_lon_rad += 2 * math.pi
    new_lon_rad -= math.pi
    
    return math.degrees(new_lat_rad), math.degrees(new_lon_rad)