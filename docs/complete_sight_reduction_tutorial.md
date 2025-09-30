# Complete Sight Reduction Tutorial

## Table of Contents
1. [Introduction to Celestial Navigation](#introduction-to-celestial-navigation)
2. [Taking Sextant Observations](#taking-sextant-observations)
3. [Using the Sight Reduction Software](#using-the-sight-reduction-software)
4. [Understanding Parameters](#understanding-parameters)
5. [Interpreting Results](#interpreting-results)
6. [Practical Example](#practical-example)
7. [Troubleshooting and Tips](#troubleshooting-and-tips)

## Introduction to Celestial Navigation

Celestial navigation is a method of determining one's position on Earth by observing celestial bodies such as the Sun, Moon, planets, and stars. The process involves measuring the altitude of these celestial bodies above the horizon using a sextant and then using mathematical calculations to determine your position.

A sight reduction is the mathematical process used to convert these sextant observations into lines of position on a nautical chart. This software automates the complex calculations required for sight reduction, making celestial navigation more accessible and accurate.

### Key Concepts
- **Altitude**: The angular distance of a celestial body above the horizon
- **Azimuth**: The compass bearing from the observer to the celestial body
- **Intercept**: The distance between the observer's assumed position and the actual position based on the observation
- **Line of Position (LOP)**: A line on the chart along which the observer's position lies
- **Assumed Position**: An approximate position, usually a round number, used for calculations

## Taking Sextant Observations

Taking accurate sextant observations is crucial for successful celestial navigation. Here's a step-by-step guide:

### Before the Observation
1. **Set up the sextant**: Check that the sextant is properly calibrated and adjust the index error if necessary
2. **Determine your approximate position**: Use GPS, dead reckoning, or other methods to get an estimated position
3. **Check the time**: Use an accurate timepiece, preferably synchronized to UTC
4. **Choose the right celestial body**: Select a celestial body that is well-positioned (not too low on the horizon, not too high)

### Taking the Observation
1. **Align the horizon**: Look through the sextant's telescope and align the horizon with the index mirror
2. **Find the celestial body**: Use the appropriate filters for the Sun, or locate the star or planet in your field of view
3. **"Rock" the sextant**: Gently rock the sextant to ensure it's perfectly vertical
4. **Bring the celestial body to the horizon**: Use the micrometer to carefully bring the celestial body down to the horizon
5. **Note the exact time**: Record the precise UTC time when the celestial body "kisses" the horizon
6. **Read the altitude**: Record the altitude measurement from the sextant

### Recording the Observation
- **Body observed**: Sun (upper/lower limb), Moon, planet, or star
- **UTC time**: Date and time of the observation (in UTC)
- **Sextant altitude**: The altitude reading from the sextant
- **Temperature**: Air temperature in Celsius
- **Pressure**: Atmospheric pressure in hPa
- **Height of eye**: Your height above sea level in meters
- **Index error**: Any known calibration error in the sextant

### Best Practices
- Take multiple observations and average them for better accuracy
- Avoid observations when the celestial body is too close to the horizon (less than 15°) due to atmospheric distortion
- For Sun observations, use the lower limb when it's rising and the upper limb when it's setting
- Ensure your timepiece is accurate to at least the nearest second

## Using the Sight Reduction Software

The sight reduction software automates the complex mathematical calculations involved in celestial navigation. Here's how to use it:

### Prerequisites
- Python 3.7 or higher installed on your system
- Required dependencies: astropy, numpy, matplotlib, pandas (install with `pip install -r requirements.txt`)

### Basic Usage

The main function for sight reduction is `calculate_intercept`. Here's the basic approach:

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

# Input data
observed_altitude = 45.23  # Observed altitude (degrees)
celestial_body_name = "sun"
assumed_lat = 40.7128      # Assumed latitude (degrees)
assumed_lon = -74.0060     # Assumed longitude (degrees)
observation_time = Time("2023-06-15T12:00:00")  # UTC time

# Define the celestial body
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction
intercept, azimuth = calculate_intercept(
    observed_altitude,
    celestial_body,
    assumed_position,
    observation_time
)

print(f"Intercept: {abs(intercept):.2f} nm {'Toward' if intercept > 0 else 'Away from'} celestial body")
print(f"Azimuth: {azimuth:.2f}°")
```

### Advanced Usage with Atmospheric Corrections

For more accurate results, include atmospheric corrections:

```python
from src.sight_reduction import calculate_intercept, get_celestial_body
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

# Input data with atmospheric conditions
observed_altitude = 45.23  # Observed altitude (degrees)
celestial_body_name = "sun"
assumed_lat = 40.7128      # Assumed latitude (degrees)
assumed_lon = -74.0060     # Assumed longitude (degrees)
observation_time = Time("2023-06-15T12:00:00")  # UTC time

# Atmospheric conditions
temperature = 15.0      # Celsius
pressure = 1020.0       # hPa
observer_height = 10.0  # Meters above sea level

# Define the celestial body
celestial_body = get_celestial_body(celestial_body_name, observation_time)

# Assumed position of the observer
assumed_position = EarthLocation(lat=assumed_lat*u.deg, lon=assumed_lon*u.deg, height=0*u.m)

# Perform sight reduction with atmospheric corrections
intercept, azimuth = calculate_intercept(
    observed_altitude, 
    celestial_body, 
    assumed_position, 
    observation_time,
    apply_refraction=True,           # Apply atmospheric refraction correction
    temperature=temperature,         # Temperature for refraction calculation
    pressure=pressure,               # Pressure for refraction calculation
    observer_height=observer_height, # Height above sea level for dip correction
    celestial_body_name=celestial_body_name,  # For limb correction
    limb='lower'                     # 'upper', 'lower', or 'center' for limb selection
)

print(f"Intercept with atmospheric corrections: {abs(intercept):.2f} nm")
print(f"Azimuth: {azimuth:.2f}°")
```

### Command-Line Usage

The software also provides a command-line interface:

```bash
cd src
python main.py
```

This will use default parameters from the config.py file. You can customize these in the config.py file according to your needs.

## Understanding Parameters

The sight reduction software uses several important parameters, each with specific meanings and effects:

### Required Parameters

#### observed_altitude
- **Type**: Float
- **Unit**: Degrees
- **Description**: The measured altitude of the celestial body above the horizon from your sextant reading
- **Range**: -1° to 90°
- **Note**: This is the raw sextant altitude before any corrections

#### celestial_body
- **Type**: Astropy SkyCoord object
- **Description**: An object representing the position of the celestial body in space
- **Creation**: Use the `get_cestial_body()` function with the body's name and observation time

#### assumed_position
- **Type**: Astropy EarthLocation object
- **Description**: Represents your assumed position on Earth
- **Components**: Latitude, longitude, and height
- **Note**: This should be close to your actual position; the closer it is, the more accurate your sight reduction will be

#### observation_time
- **Type**: Astropy Time object
- **Description**: The exact UTC time of the observation
- **Format**: ISO format string (e.g., "2023-06-15T12:00:00")
- **Importance**: Critical for accurate position calculations of celestial bodies

### Optional Parameters with Corrections

#### apply_refraction
- **Type**: Boolean
- **Default**: True
- **Description**: Whether to apply atmospheric refraction correction
- **Effect**: When True, accounts for the bending of light as it passes through Earth's atmosphere

#### temperature
- **Type**: Float
- **Unit**: Celsius
- **Default**: 10.0
- **Range**: -100°C to 100°C
- **Description**: Atmospheric temperature for refraction calculations
- **Effect**: Higher temperatures reduce refraction

#### pressure
- **Type**: Float
- **Unit**: hPa (hectopascals)
- **Default**: 1010.0
- **Range**: 800 to 1200 hPa
- **Description**: Atmospheric pressure for refraction calculations
- **Effect**: Higher pressure increases refraction

#### observer_height
- **Type**: Float
- **Unit**: Meters above sea level
- **Default**: 0.0
- **Range**: 0 or higher
- **Description**: Height of the observer above sea level
- **Effect**: Used to calculate the dip of the horizon correction

#### celestial_body_name
- **Type**: String
- **Default**: None
- **Valid values**: 'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', and various stars
- **Description**: Name of the celestial body for limb correction calculations
- **Effect**: Enables limb corrections for bodies with appreciable angular size

#### limb
- **Type**: String
- **Default**: 'center'
- **Valid values**: 'center', 'upper', 'lower'
- **Description**: Which part of the celestial body was observed
- **Effect**: Applies correction based on the limb observed for bodies with appreciable size

### Available Celestial Bodies

The software supports the following celestial bodies:

- **Sun**: The Sun
- **Moon**: The Moon
- **Planets**: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune
- **Stars**: 
  - Sirus, Canopus, Arcturus, Rigel, Procyon, Vega, Capella, Rigil Kentaurus A, Altair, Acrux
  - Aldebaran, Spica, Antares, Pollux, Deneb, Betelgeuse, Bellatrix, Alpheratz, Fomalhaut, Polaris

## Interpreting Results

The sight reduction function returns two critical values that enable navigation: intercept and azimuth.

### Intercept

#### What is it?
The intercept represents the distance between your assumed position and the line of position derived from your celestial observation. It's measured in nautical miles.

#### How is it calculated?
The intercept is calculated as the difference between the observed altitude and the calculated altitude (the altitude the celestial body would have if you were at your assumed position), converted to nautical miles. Since 1 degree of arc equals 60 nautical miles, the formula is:

```
Intercept (nautical miles) = (Corrected Observed Altitude - Calculated Altitude) * 60
```

#### Positive vs. Negative Intercept
- **Positive intercept** (+): The actual position is toward the celestial body from the assumed position
- **Negative intercept** (-): The actual position is away from the celestial body from the assumed position
- **Zero intercept**: The actual position coincides with the assumed position on the line of position

#### Plotting the Intercept
1. Draw a line from the assumed position in the direction of the azimuth
2. Measure the intercept distance along this line (toward or away based on the sign)
3. At this point, draw a perpendicular line - this is your line of position (LOP)

### Azimuth

#### What is it?
The azimuth is the compass bearing from your assumed position to the celestial body at the time of observation. It's measured in degrees from true north (0° to 360°).

#### How is it used?
- The azimuth provides the direction to the celestial body
- You plot the line of position perpendicular to the azimuth line
- The azimuth helps identify which celestial body was observed

#### Directional Conventions
- 0° = North
- 90° = East
- 180° = South
- 270° = West
- Values between 0° and 360° represent all possible compass directions

### Practical Interpretation

#### Single Line of Position
A single sight reduction gives you one line of position. You know your position is somewhere along this line, but the exact location is unknown without additional information.

#### Multiple Lines of Position
By taking multiple sights of different celestial bodies (or the same body at different times), you can plot multiple lines of position. Where these lines intersect is your fix - your estimated position.

#### Accuracy Considerations
- Intercepts smaller than 20-30 nautical miles generally indicate good observations
- Larger intercepts may indicate errors in observation, time, or assumed position
- Always consider multiple LOPs to confirm your position

## Practical Example

Here's a complete practical example using the sight reduction software:

### Scenario
You're navigating in the Atlantic Ocean on June 15, 2023. You take a morning Sun sight using your sextant and record the following:
- Time: 08:25:30 UTC
- Sextant altitude of Sun's lower limb: 28° 45.2'
- Assumed position: Latitude 40° 42.8' N, Longitude 74° 0.4' W
- Temperature: 18°C
- Pressure: 1015 hPa
- Height of eye: 3 meters

### Step-by-Step Solution

1. **Convert your sextant observation to decimal degrees**:
   - Observed altitude = 28 + 45.2/60 = 28.7533°

2. **Prepare the input parameters**:
   ```python
   from astropy.time import Time
   from astropy.coordinates import EarthLocation
   import astropy.units as u
   from src.sight_reduction import calculate_intercept, get_celestial_body
   
   # Observation data
   observed_altitude = 28.7533  # 28° 45.2' converted to decimal degrees
   celestial_body_name = "sun"
   assumed_lat = 40.7133        # 40° 42.8' N converted to decimal degrees
   assumed_lon = -74.0067       # 74° 0.4' W converted to decimal degrees
   observation_time = Time("2023-06-15T08:25:30")  # UTC time
   
   # Atmospheric conditions
   temperature = 18.0      # Celsius
   pressure = 1015.0       # hPa
   observer_height = 3.0   # Meters
   ```

3. **Run the sight reduction**:
   ```python
   # Get the celestial body coordinates
   celestial_body = get_celestial_body(celestial_body_name, observation_time)
   
   # Set up assumed position
   assumed_position = EarthLocation(
       lat=assumed_lat*u.deg, 
       lon=assumed_lon*u.deg, 
       height=0*u.m
   )
   
   # Calculate intercept and azimuth
   intercept, azimuth = calculate_intercept(
       observed_altitude,
       celestial_body,
       assumed_position,
       observation_time,
       apply_refraction=True,
       temperature=temperature,
       pressure=pressure,
       observer_height=observer_height,
       celestial_body_name=celestial_body_name,
       limb='lower'  # Since we observed the lower limb of the Sun
   )
   
   print(f"Intercept: {abs(intercept):.2f} nm {'toward' if intercept > 0 else 'away from'} the Sun")
   print(f"Azimuth: {azimuth:.2f}°")
   ```

4. **Interpret the results**:
   Assuming the software returns:
   - Intercept: -2.8 nm (meaning away from the Sun)
   - Azimuth: 98.5° (meaning the Sun is toward the ESE direction)
   
   This means your actual position is 2.8 nautical miles away from your assumed position in the direction opposite to azimuth 98.5°, which would be toward 278.5° (West-Northwest).

5. **Plot on nautical chart**:
   - From your assumed position, draw a line at azimuth 98.5°
   - Measure 2.8 nautical miles away from the celestial body
   - Draw a perpendicular line at this point - this is your line of position

## Troubleshooting and Tips

### Common Issues and Solutions

#### Invalid Altitude Range
**Problem**: "Altitude X° is not in valid range [-1°, 90°]"
**Solution**: Check that your altitude is between -1° and 90°. Altitudes above 90° are impossible, and negative altitudes indicate the body is below the horizon.

#### Invalid Temperature or Pressure
**Problem**: "Temperature X°C is not in valid range [-100°C, 100°C]" or similar for pressure
**Solution**: Ensure temperature is within the range -100°C to +100°C and pressure is between 800 and 1200 hPa.

#### Invalid Celestial Body Name
**Problem**: "Celestial body X is not supported for limb correction"
**Solution**: Check that you're using a supported celestial body name. See the "Available Celestial Bodies" section above.

#### Large Intercepts
**Problem**: Very large intercept values (e.g., 50+ nautical miles)
**Solution**: 
- Double-check your time accuracy (critical for celestial positions)
- Verify your assumed position is close to your actual position
- Check for errors in your observation
- Ensure you're using the correct limb for the celestial body

### Best Practices

#### Time Accuracy
- Use a properly synchronized timepiece accurate to the second
- Convert all times to UTC before using the software
- Record the exact time of the observation as you take it

#### Accurate Assumed Position
- Use GPS, dead reckoning, or other navigation methods to get the most accurate assumed position possible
- Round your assumed position to the nearest minute for easier manual plotting

#### Multiple Observations
- Take multiple shots of the same celestial body and average the results
- Take sights of different celestial bodies to get multiple lines of position
- Take sights of the same celestial body at different times (running fix)

#### Environmental Corrections
- Measure temperature and pressure as accurately as possible
- Ensure your height of eye measurement is accurate
- Apply appropriate limb corrections based on your observation method

#### Software Tips
- Always validate your input parameters
- Use atmospheric corrections for more accurate results
- Remember that the intercept indicates whether you're toward or away from the celestial body
- The software performs validation, so incorrect parameters will generate helpful error messages

### Accuracy Considerations

#### Theoretical Accuracy
- The software uses Astropy for high-precision celestial calculations
- Atmospheric refraction corrections are based on standard formulas
- With accurate inputs, results should be accurate to within 0.1 nautical miles

#### Practical Accuracy
- Depends on the skill of the observer
- Sextant measurements can have errors of several tenths of minutes of arc
- Time accuracy is critical
- Environmental conditions (temperature, pressure) should be measured accurately

#### Validation
- Compare results with known positions when possible
- Cross-check with GPS if available
- Use multiple celestial bodies to confirm position
- Consider taking multiple sightings and averaging results

### Summary

Celestial navigation remains a valuable backup navigation skill. This sight reduction software simplifies the complex mathematics involved, but taking accurate observations remains critical for good results. Pay attention to detail in your observations, time, and environmental conditions, and you'll have reliable celestial navigation results.