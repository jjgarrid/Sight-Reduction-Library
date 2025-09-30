"""
Star Database for Celestial Navigation

This module contains Right Ascension (RA) and Declination (Dec) data for
common navigation stars used in celestial navigation.

Data is based on standard nautical almanac values and J2000.0 coordinates.
"""
import astropy.units as u
from astropy.coordinates import SkyCoord

# Navigation Star Database - Coordinates in J2000.0 epoch
NAVIGATION_STARS = {
    # First Magnitude Stars
    'sirius': {
        'ra': '6h45m8.9s',
        'dec': '-16d42m58s',
        'magnitude': -1.46,
        'description': 'Brightest star in the sky, in Canis Major'
    },
    'canopus': {
        'ra': '6h23m57.1s', 
        'dec': '-52d41m44s',
        'magnitude': -0.74,
        'description': 'Second brightest star, in Carina'
    },
    'arcturus': {
        'ra': '14h15m39.7s',
        'dec': '19d10m57s', 
        'magnitude': -0.05,
        'description': 'Bright star in Bootes'
    },
    'rigel': {
        'ra': '5h14m32.3s',
        'dec': '-8d12m6s',
        'magnitude': 0.13,
        'description': 'Bright star in Orion (left foot of Orion)'
    },
    'procyon': {
        'ra': '7h39m18.1s',
        'dec': '5d13m30s',
        'magnitude': 0.34,
        'description': 'Bright star in Canis Minor'
    },
    'vega': {
        'ra': '18h36m56.3s',
        'dec': '38d47m01s',
        'magnitude': 0.03,
        'description': 'Bright star in Lyra'
    },
    'capella': {
        'ra': '5h16m41.4s',
        'dec': '45d59m53s',
        'magnitude': 0.08,
        'description': 'Bright star in Auriga'
    },
    'rigel_kentaurus_a': {  # Alpha Centauri A
        'ra': '14h39m36.5s',
        'dec': '-60d50m02s',
        'magnitude': -0.01,
        'description': 'Bright star in Centaurus (closest star system to Sun)'
    },
    'altair': {
        'ra': '19h50m46.7s',
        'dec': '8d52m06s',
        'magnitude': 0.77,
        'description': 'Bright star in Aquila'
    },
    'acrux': {
        'ra': '12h26m35.9s',
        'dec': '-63d07m29s',
        'magnitude': 0.76,
        'description': 'Bright star in Crux (Southern Cross)'
    },
    'aldebaran': {
        'ra': '4h35m55.2s',
        'dec': '16d30m33s',
        'magnitude': 0.87,
        'description': 'Bright star in Taurus (eye of Taurus)'
    },
    'spica': {
        'ra': '13h25m11.6s',
        'dec': '-11d09m41s',
        'magnitude': 0.98,
        'description': 'Bright star in Virgo'
    },
    'antares': {
        'ra': '16h29m24.5s',
        'dec': '-26d25m55s',
        'magnitude': 1.09,
        'description': 'Bright red star in Scorpius'
    },
    'pollux': {
        'ra': '7h45m18.9s',
        'dec': '28d01m34s',
        'magnitude': 1.14,
        'description': 'Bright star in Gemini (one of the twins)'
    },
    
    # Additional useful navigation stars
    'deneb': {
        'ra': '20h41m25.9s',
        'dec': '45d16m49s',
        'magnitude': 1.25,
        'description': 'Bright star in Cygnus (tail of Cygnus)'
    },
    'betelgeuse': {
        'ra': '5h55m10.3s',
        'dec': '7d24m25s',
        'magnitude': 0.50,
        'description': 'Bright red star in Orion (shoulder of Orion)'
    },
    'bellatrix': {
        'ra': '5h25m07.9s',
        'dec': '6d20m59s',
        'magnitude': 1.64,
        'description': 'Bright star in Orion (left shoulder of Orion)'
    },
    'alpheratz': {
        'ra': '0h8m23.3s',
        'dec': '29d5m05s',
        'magnitude': 2.07,
        'description': 'Bright star in Andromeda'
    },
    'fomalhaut': {
        'ra': '22h57m39.0s',
        'dec': '-29d37m20s',
        'magnitude': 1.16,
        'description': 'Bright star in Piscis Austrinus'
    },
    'scheat': {
        'ra': '23h03m46.5s',
        'dec': '28d04m34s',
        'magnitude': 2.42,
        'description': 'Bright star in Pegasus'
    },
    'markab': {
        'ra': '23h04m45.7s',
        'dec': '15d12m19s',
        'magnitude': 2.49,
        'description': 'Bright star in Pegasus'
    },
    'algenib': {
        'ra': '0h13m14.2s',
        'dec': '15d11m00s',
        'magnitude': 2.83,
        'description': 'Bright star in Perseus'
    },
    'enif': {
        'ra': '21h44m11.8s',
        'dec': '9d52m06s',
        'magnitude': 2.38,
        'description': 'Bright star in Pegasus'
    },
    'sadalmelik': {
        'ra': '22h5m47.0s',
        'dec': '-0d19m11s',
        'magnitude': 2.96,
        'description': 'Bright star in Aquarius'
    },
    'kochab': {
        'ra': '14h50m42.3s',
        'dec': '74d09m12s',
        'magnitude': 2.08,
        'description': 'Bright star in Ursa Minor'
    },
    'gacrux': {
        'ra': '12h31m09.9s',
        'dec': '-57d07m07s',
        'magnitude': 1.60,
        'description': 'Bright star in Crux (Southern Cross)'
    },
    'aphard': {
        'ra': '14h3m14.3s',
        'dec': '-9d02m00s',
        'magnitude': 2.56,
        'description': 'Bright star in Hydra'
    },
    'alnilam': {
        'ra': '5h36m12.8s',
        'dec': '-1d12m07s',
        'magnitude': 1.69,
        'description': 'Bright star in Orion (center of Orion\'s Belt)'
    },
    'alnair': {
        'ra': '22h8m13.7s',
        'dec': '-46d57m39s',
        'magnitude': 1.73,
        'description': 'Bright star in Grus'
    },
    'adara': {
        'ra': '6h58m37.6s',
        'dec': '-28d58m32s',
        'magnitude': 1.50,
        'description': 'Bright star in Canis Major'
    },
    'mirphak': {
        'ra': '3h24m19.4s',
        'dec': '49d51m40s',
        'magnitude': 1.80,
        'description': 'Bright star in Perseus'
    },
    'wezen': {
        'ra': '7h07m56.0s',
        'dec': '-26d23m42s',
        'magnitude': 1.83,
        'description': 'Bright star in Canis Major'
    },
    'alphekka': {
        'ra': '16h25m56.2s',
        'dec': '26d25m56s',
        'magnitude': 2.35,
        'description': 'Bright star in Corona Borealis'
    },
    'sargas': {
        'ra': '17h37m34.2s',
        'dec': '-43d01m12s',
        'magnitude': 1.85,
        'description': 'Bright star in Scorpius'
    },
    'dubhe': {
        'ra': '11h2m47.5s',
        'dec': '61d45m03s',
        'magnitude': 1.79,
        'description': 'Bright star in Ursa Major (one of the pointers)'
    },
    'algenib': {
        'ra': '0h13m14.2s',
        'dec': '15d11m00s',
        'magnitude': 2.83,
        'description': 'Bright star in Perseus'
    },
    'alcyone': {
        'ra': '3h47m29.1s',
        'dec': '24d07m26s',
        'magnitude': 2.87,
        'description': 'Bright star in Taurus (in Pleiades cluster)'
    },
    'castor': {
        'ra': '7h34m35.9s',
        'dec': '31d53m18s',
        'magnitude': 1.58,
        'description': 'Bright star in Gemini (one of the twins)'
    },
    'polaris': {
        'ra': '2h31m47.1s',
        'dec': '89d15m51s',
        'magnitude': 1.98,
        'description': 'North Star in Ursa Minor'
    }
}

def get_star_coordinates(star_name):
    """
    Get the coordinates for a navigation star.
    
    Parameters:
    - star_name: Name of the star (case-insensitive)
    
    Returns:
    - SkyCoord object with the star's coordinates, or None if not found
    """
    star_name_lower = star_name.lower()
    
    # Handle special cases
    if star_name_lower in NAVIGATION_STARS:
        star_data = NAVIGATION_STARS[star_name_lower]
        return SkyCoord(
            ra=star_data['ra'],
            dec=star_data['dec'],
            frame='icrs'
        )
    
    # If not found, return None
    return None


def get_star_info(star_name):
    """
    Get detailed information about a navigation star.
    
    Parameters:
    - star_name: Name of the star (case-insensitive)
    
    Returns:
    - Dictionary with star information, or None if not found
    """
    star_name_lower = star_name.lower()
    
    if star_name_lower in NAVIGATION_STARS:
        return NAVIGATION_STARS[star_name_lower]
    
    return None


def list_navigation_stars():
    """
    Get a list of all navigation stars in the database.
    
    Returns:
    - List of star names
    """
    return list(NAVIGATION_STARS.keys())