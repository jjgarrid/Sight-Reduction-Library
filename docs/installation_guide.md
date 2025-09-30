# Installation Guide for Sight Reduction Project

## Prerequisites

Before installing the Sight Reduction project, you'll need:
- Python 3.8 or higher
- pip (Python package installer)

## Quick Installation

For a quick setup, you can install all dependencies directly:

```bash
pip install -r requirements.txt
```

## Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>  # If using git
# OR download and extract the zip file
```

### 2. Navigate to the Project Directory

```bash
cd Sight_Reduction
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv sight_reduction_env
source sight_reduction_env/bin/activate  # On Linux/Mac
# OR
sight_reduction_env\Scripts\activate     # On Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Detailed Dependencies Information

The project requires the following packages:

- **astropy>=5.0**: Provides high-precision astronomical calculations and coordinate transformations
- **numpy>=1.21.0**: Used for mathematical computations
- **matplotlib>=3.3.0**: For plotting and visualization (if needed)
- **pandas>=1.3.0**: For data manipulation (if needed)

### Installing Individual Dependencies

If you prefer to install dependencies individually:

```bash
pip install astropy>=5.0
pip install numpy>=1.21.0
pip install matplotlib>=3.3.0
pip install pandas>=1.3.0
```

## Setup Script

The project includes a setup script that can automate the installation process:

```bash
bash setup.sh  # On Linux/Mac
# OR
chmod +x setup.sh && ./setup.sh
```

This script typically:
- Creates a virtual environment
- Activates the virtual environment
- Installs all required packages
- Sets up any necessary configuration

## Configuration

After installation, you can customize the default values by modifying the `config.py` file:

```python
# Configuration for Sight Reduction project

# Default observation parameters
DEFAULT_OBSERVED_ALTITUDE = 45.0  # degrees
DEFAULT_CELESTIAL_BODY = "sun"
DEFAULT_ASSUMED_LAT = 40.7128     # degrees
DEFAULT_ASSUMED_LON = -74.0060    # degrees

# Calculation settings
NAUTICAL_MILES_PER_DEGREE = 60.0

# Output formatting
FORMAT_PRECISION = 2
```

## Verification

After installation, you can verify that everything is working by running:

```bash
python src/main.py
```

This will execute the main sight reduction script using default parameters.

## Troubleshooting

### Common Installation Issues

1. **Permission Errors**
   - Solution: Use a virtual environment or install with the `--user` flag:
   ```bash
   pip install --user -r requirements.txt
   ```

2. **Missing Dependencies**
   - Solution: Install build tools:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install build-essential
   
   # On macOS
   xcode-select --install
   
   # On Windows
   Install Microsoft C++ Build Tools
   ```

3. **Python Version Incompatibility**
   - Check your Python version: `python --version`
   - Ensure you're using Python 3.8 or higher

### Virtual Environment Issues

If you encounter problems with the virtual environment:

1. Deactivate the current environment: `deactivate`
2. Remove the old environment folder: `rm -rf sight_reduction_env`
3. Recreate the environment: `python -m venv sight_reduction_env`
4. Activate it again: `source sight_reduction_env/bin/activate`

## Development Setup

If you're planning to contribute to the project:

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/yourusername/sight_reduction.git
```
3. Create a virtual environment as described above
4. Install in development mode:
```bash
pip install -e .
```
5. Install development dependencies:
```bash
pip install pytest pytest-cov
```

## Updating the Package

To update to the latest version:

```bash
git pull  # If using git
pip install -r requirements.txt --upgrade  # Update dependencies
```

## Uninstallation

To uninstall:

1. Deactivate the virtual environment: `deactivate`
2. Remove the virtual environment folder: `rm -rf sight_reduction_env`
3. Or simply remove the project directory if not using a virtual environment