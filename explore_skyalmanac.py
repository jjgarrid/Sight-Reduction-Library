#!/usr/bin/env python
"""
Script to explore skyalmanac functionality and understand how to use it.
"""

def explore_skyalmanac():
    """Explore skyalmanac package structure"""
    import skyalmanac
    
    # Check the path where the package is located
    import skyalmanac
    print(f"Skyalmanac package path: {skyalmanac.__path__}")
    
    import os
    for root, dirs, files in os.walk(skyalmanac.__path__[0]):
        level = root.replace(skyalmanac.__path__[0], '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f"{subindent}{file}")

def explore_skyfield():
    """Explore Skyfield functionality for celestial navigation"""
    from skyfield.api import load
    ts = load.timescale()
    
    # Example of how to get celestial body positions using Skyfield
    t = ts.utc(2023, 6, 15, 12, 0, 0)
    eph = load('de421.bsp')  # Standard solar system ephemeris
    
    # Get the sun
    sun = eph['sun']
    earth = eph['earth']
    
    # Calculate apparent position
    astrometric = earth.at(t).observe(sun)
    ra, dec, distance = astrometric.radec()
    
    print(f"Skyfield - Sun position on 2023-06-15 at 12:00 UTC:")
    print(f"  Right Ascension: {ra}")
    print(f"  Declination: {dec}")
    print(f"  Distance: {distance}")
    
    # Calculate GHA (Greenwich Hour Angle)
    # GHA = GAST * 15 - RA in degrees
    gast = t.gast  # Greenwich Apparent Sidereal Time in hours
    gha_hours = gast - ra._hours
    if gha_hours < 0:
        gha_hours += 24
    gha_degrees = gha_hours * 15
    
    print(f"  GHA: {gha_degrees:.4f}°")

if __name__ == "__main__":
    print("Exploring Skyalmanac package structure...\n")
    explore_skyalmanac()
    
    print("\n\nTesting Skyfield functionality (which skyalmanac is based on)...")
    explore_skyfield()