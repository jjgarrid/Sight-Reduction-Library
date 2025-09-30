#!/usr/bin/env python3
"""
Test Automation Script for Sight Reduction Project

This script automates the execution of tests for the Sight Reduction project
and generates a detailed report of the test results.
"""

import sys
import os
import subprocess
import time
from datetime import datetime
import json

def run_command(cmd, description="Running command"):
    """Execute a shell command and return the result."""
    print(f"  {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    dependencies = [
        ("pytest", "pytest --version"),
        ("python", "python --version"),
        ("pip", "pip --version")
    ]
    
    missing_deps = []
    for dep_name, cmd in dependencies:
        returncode, stdout, stderr = run_command(cmd, f"Checking {dep_name}")
        if returncode != 0:
            missing_deps.append(dep_name)
        else:
            print(f"  ✓ {dep_name}: {stdout.strip() if stdout.strip() else 'Available'}")
    
    if missing_deps:
        print(f"  ✗ Missing dependencies: {', '.join(missing_deps)}")
        return False
    else:
        print("  ✓ All dependencies are available")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    returncode, stdout, stderr = run_command(
        "pip install -r requirements.txt", 
        "Installing from requirements.txt"
    )
    
    if returncode != 0:
        print(f"  ✗ Failed to install requirements: {stderr}")
        return False
    else:
        print("  ✓ Dependencies installed successfully")
        return True

def run_tests():
    """Run the test suite and return results."""
    print("Running tests...")
    
    # Run tests with detailed output
    returncode, stdout, stderr = run_command(
        "python -m pytest tests/ -v --tb=short --maxfail=5",
        "Executing test suite"
    )
    
    return returncode, stdout, stderr

def parse_test_results(test_output):
    """Parse pytest output to extract test statistics."""
    stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "warnings": 0,
        "duration": 0.0
    }
    
    lines = test_output.split('\n')
    for line in lines:
        if 'passed' in line and 'collecting' not in line:
            stats['passed'] += line.count('PASSED')
        elif 'failed' in line:
            stats['failed'] += line.count('FAILED')
        elif 'skipped' in line:
            stats['skipped'] += line.count('SKIPPED')
        elif 'error' in line:
            stats['errors'] += line.count('ERROR')
    
    # Try to find the summary line
    summary_line = None
    for line in reversed(lines):
        if 'passed' in line or 'failed' in line:
            summary_line = line
            break
    
    if summary_line:
        # Parse the summary line to get counts
        import re
        passed_match = re.search(r'(\d+)\s+passed', summary_line)
        failed_match = re.search(r'(\d+)\s+failed', summary_line)
        skipped_match = re.search(r'(\d+)\s+skipped', summary_line)
        error_match = re.search(r'(\d+)\s+error', summary_line)
        
        if passed_match:
            stats['passed'] = int(passed_match.group(1))
        if failed_match:
            stats['failed'] = int(failed_match.group(1))
        if skipped_match:
            stats['skipped'] = int(skipped_match.group(1))
        if error_match:
            stats['errors'] = int(error_match.group(1))
        
        stats['total'] = stats['passed'] + stats['failed'] + stats['skipped'] + stats['errors']
        
        # Extract duration if available
        duration_match = re.search(r'(\d+\.?\d*)\w?\s*s', summary_line)
        if duration_match:
            try:
                stats['duration'] = float(duration_match.group(1))
            except ValueError:
                pass
    
    return stats

def generate_report(returncode, stdout, stderr, start_time, end_time):
    """Generate a detailed test report."""
    duration = end_time - start_time
    stats = parse_test_results(stdout)
    
    print("\n" + "="*70)
    print("TEST EXECUTION REPORT")
    print("="*70)
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    print("TEST RESULTS SUMMARY:")
    print(f"  Total Tests Run: {stats['total']}")
    print(f"  Passed: {stats['passed']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Duration: {stats['duration']:.2f}s")
    print()
    
    if returncode == 0:
        print("  🎉 ALL TESTS PASSED!")
        status_color = "\033[92m"  # Green
    else:
        print("  ❌ SOME TESTS FAILED!")
        status_color = "\033[91m"  # Red
    print(f"{status_color}  Exit Code: {returncode}\033[0m")
    print()
    
    if stats['failed'] > 0 or stats['errors'] > 0:
        print("FAILED TESTS DETAILS:")
        print("-" * 50)
        # Extract failed test details from output
        in_failures = False
        for line in stdout.split('\n'):
            if 'FAILURES' in line:
                in_failures = True
                print(line)
            elif in_failures and line.strip() and not line.startswith('=' * 10):
                print(line)
                if line.strip() and not line.startswith('_'):
                    continue
                elif line.startswith('=') and 'short test' in line.lower():
                    break
        print()
    
    if 'warnings summary' in stdout:
        print("WARNINGS:")
        print("-" * 30)
        in_warnings = False
        for line in stdout.split('\n'):
            if 'warnings summary' in line.lower():
                in_warnings = True
                print(line)
            elif in_warnings and line.strip():
                print(line)
                if line.startswith('=' * 10):
                    break
        print()
    
    if stderr and returncode != 0:
        print("ERROR OUTPUT:")
        print("-" * 30)
        print(stderr)
        print()
    
    print("TEST OUTPUT:")
    print("-" * 30)
    # Show the pytest summary
    lines = stdout.split('\n')
    for line in lines:
        if 'collected' in line or 'passed' in line or 'failed' in line or 'skipped' in line or 'error' in line:
            print(line)
    print()
    
    print("="*70)
    return returncode == 0

def main():
    """Main function to run the test automation."""
    print("Sight Reduction Project - Test Automation Script")
    print("=" * 50)
    
    start_time = time.time()
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt") or not os.path.exists("tests"):
        print("Error: This script should be run from the project root directory.")
        print("Please navigate to the Sight Reduction project directory and run this script.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\nAttempting to install dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Exiting.")
            sys.exit(1)
        # Recheck dependencies after installation
        if not check_dependencies():
            print("Dependencies still missing after installation. Exiting.")
            sys.exit(1)
    
    # Run tests
    returncode, stdout, stderr = run_tests()
    
    end_time = time.time()
    
    # Generate report
    success = generate_report(returncode, stdout, stderr, start_time, end_time)
    
    # Exit with the same code as the test run
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()