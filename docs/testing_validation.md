# Testing and Validation for Sight Reduction Project

## Overview

This document describes the testing strategy, validation methods, and quality assurance procedures for the Sight Reduction project. Proper testing ensures the accuracy and reliability of celestial navigation calculations.

## Test Structure

The project includes tests in the `tests/` directory with the following organization:

- `test_sight_reduction.py`: Tests for the core sight reduction functions
- `test_atmospheric_corrections.py`: Tests specifically for atmospheric correction functions

## Running Tests

### Prerequisites

First, install the testing dependencies:

```bash
pip install pytest pytest-cov
```

### Running All Tests

```bash
pytest tests/
```

### Running Specific Test Files

```bash
# Run sight reduction tests only
pytest tests/test_sight_reduction.py

# Run atmospheric correction tests only
pytest tests/test_atmospheric_corrections.py
```

### Running with Coverage Report

```bash
pytest tests/ --cov=src/ --cov-report=html
```

This generates an HTML coverage report in the `htmlcov/` directory.

## Test Categories

### 1. Core Function Tests

#### `test_calculate_intercept`
- Verifies that the main sight reduction function returns expected numeric results
- Tests that azimuth values are within valid range (0-360°)
- Confirms intercept and azimuth are returned as floats

```python
def test_calculate_intercept():
    """Test the calculate_intercept function with basic inputs."""
    observed_altitude = 45.0
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    intercept, azimuth = calculate_intercept(
        observed_altitude, 
        celestial_body, 
        assumed_position, 
        observation_time
    )
    
    # Verify that we get numeric results
    assert isinstance(intercept, float)
    assert isinstance(azimuth, float)
    assert 0 <= azimuth <= 360
```

#### `test_get_celestial_body`
- Tests that celestial bodies (Sun, Moon, Star) are returned correctly
- Confirms that returned objects are not None

### 2. Utility Function Tests

#### `test_format_position`
- Verifies that position formatting returns expected string format
- Tests that cardinal directions (N, S, E, W) are correctly included
- Ensures degree formatting is properly applied

```python
def test_format_position():
    """Test the format_position function."""
    result = format_position(40.7128, -74.0060)
    assert "N" in result
    assert "W" in result
    assert "40°" in result
    assert "74°" in result
```

### 3. Atmospheric Correction Tests

The project should include tests for atmospheric corrections (though not shown in the initial code, these would be important to add):

#### Refraction Correction Tests
- Verify refraction values are positive
- Test extreme altitude values (0°, 90°)
- Validate temperature and pressure effects on refraction

#### Dip Correction Tests
- Test with various observer heights
- Verify dip is zero when height is zero
- Confirm dip values are positive for positive heights

#### Limb Correction Tests
- Test all limb types ('center', 'upper', 'lower')
- Verify only Sun and Moon have limb corrections
- Confirm star limb correction is zero

## Validation Methods

### 1. Unit Validation

The project includes comprehensive input validation:

```python
def validate_altitude(altitude: float) -> None:
    """Validate that altitude is within reasonable range."""
    if altitude < -1 or altitude > 90:
        raise ValueError(f"Altitude {altitude}° is not in valid range [-1°, 90°]")

def validate_temperature(temperature: float) -> None:
    """Validate temperature is within reasonable range (-100°C to +100°C)."""
    if temperature < -100 or temperature > 100:
        raise ValueError(f"Temperature {temperature}°C is not in valid range [-100°C, 100°C]")
```

### 2. Cross-Validation with External Tools

For validation, results can be compared with:
- Nautical almanac values
- Other celestial navigation software
- Known astronomical calculations

### 3. Boundary Condition Testing

The project handles various boundary conditions:

- Altitude of 0° (horizon observations)
- Altitude of 90° (zenith observations)
- Observer height of 0 (sea level)
- Extreme temperatures and pressures
- Different celestial bodies

## Test Coverage

### Current Test Coverage

The existing tests cover:
- Basic functionality of main sight reduction
- Input validation
- Position formatting
- Celestial body selection

### Recommended Additional Tests

For comprehensive validation, additional tests should cover:

#### Atmospheric Correction Validation
- Refraction correction accuracy across altitude range
- Temperature effect on refraction
- Pressure effect on refraction
- Dip correction accuracy
- Limb correction accuracy

#### Error Handling Tests
- Invalid altitude values
- Invalid temperature values
- Invalid pressure values
- Invalid observer height values
- Invalid celestial body names
- Invalid limb selections

#### Integration Tests
- Combined corrections functionality
- Edge case scenarios
- Real-world usage patterns

## Quality Assurance Standards

### Accuracy Requirements

- Intercept calculations should be accurate to within 0.1 nautical miles
- Azimuth calculations should be accurate to within 0.1°
- Atmospheric corrections should match standard nautical tables

### Performance Requirements

- Single sight reduction should execute in under 100ms
- Multiple calculations should maintain consistent performance
- Memory usage should be minimal and bounded

### Code Quality Standards

- All functions should have proper docstrings
- Input validation should be comprehensive
- Error messages should be clear and informative
- Code should follow Python best practices

## Testing Best Practices

### Writing New Tests

When adding functionality to the project, follow these testing practices:

```python
import pytest
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from src.sight_reduction import calculate_intercept, get_celestial_body

def test_example_function():
    """Test description: What the test is verifying."""
    # Arrange: Set up test conditions
    observed_altitude = 45.0
    observation_time = Time("2023-06-15T12:00:00")
    celestial_body = get_celestial_body("sun", observation_time)
    assumed_position = EarthLocation(lat=40.0*u.deg, lon=-74.0*u.deg, height=0*u.m)
    
    # Act: Execute the function
    result = calculate_intercept(
        observed_altitude,
        celestial_body,
        assumed_position,
        observation_time
    )
    
    # Assert: Verify expected outcomes
    intercept, azimuth = result
    assert isinstance(intercept, float)
    assert isinstance(azimuth, float)
    # Add more specific assertions based on expected values
```

### Test Naming Conventions

- Use descriptive names: `test_function_name_scenario`
- Follow the pattern: `test_[function_name]_[scenario]`
- Include expected behavior in name where appropriate

### Test Data

- Use realistic values from actual celestial navigation scenarios
- Include boundary conditions and edge cases
- Consider real-world atmospheric conditions

## Continuous Integration

The project should implement continuous integration to ensure:
- All tests pass before merging code
- Code quality standards are maintained
- Documentation remains up to date

Example GitHub Actions workflow:

```yaml
name: Test Sight Reduction

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    - name: Run tests
      run: pytest tests/ -v
    - name: Generate coverage report
      run: pytest tests/ --cov=src/ --cov-report=xml
```

## Validation Against Standards

### Nautical Almanac Verification

Results from the sight reduction functions should be validated against:
- Nautical almanac values
- Standard astronomical calculations
- Established celestial navigation procedures

### Accuracy Benchmarks

The project should maintain accuracy benchmarks:
- Compare results with established navigation software
- Validate against known test cases
- Maintain accuracy documentation for reference

## Maintenance and Updates

### Test Maintenance

- Regularly review and update tests as functionality changes
- Add new tests for any new features
- Remove outdated tests when functionality is deprecated
- Ensure backward compatibility where appropriate

### Validation Updates

As astrometric standards evolve:
- Update to new IAU standards when necessary
- Recalibrate calculations to maintain accuracy
- Document any changes in precision or methodology

## Test Automation Scripts

The project includes automated test execution scripts to make running tests easier:

### Python Test Runner Script

The `run_tests.py` script provides detailed test execution with comprehensive reporting:

```bash
# Run from the project root directory
python run_tests.py
```

Features of the Python script:
- Checks for required dependencies automatically
- Installs missing dependencies if needed
- Runs all tests with detailed output
- Generates a comprehensive report with statistics
- Shows failed test details and warnings
- Provides execution time and performance metrics

### Shell Test Runner Script

The `run_tests.sh` script provides a simple shell-based test execution:

```bash
# Run from the project root directory
./run_tests.sh
```

### Running Tests Directly

You can also run tests directly with pytest:

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=src/ --cov-report=html

# Run specific test file
python -m pytest tests/test_sight_reduction.py

# Run specific test
python -m pytest tests/test_sight_reduction.py::test_calculate_intercept
```

This comprehensive testing and validation approach ensures that the Sight Reduction project provides accurate and reliable results for celestial navigation applications.