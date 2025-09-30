#!/bin/bash
# Test Execution Script for Sight Reduction Project
# This script runs all tests and generates a report

echo "Sight Reduction Project - Test Execution Script"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ] || [ ! -d "tests" ]; then
    echo "Error: This script should be run from the project root directory."
    echo "Please navigate to the Sight Reduction project directory and run this script."
    exit 1
fi

echo "Checking dependencies..."
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing..."
    pip install pytest
fi

echo "Running tests..."
echo "=================="
python -m pytest tests/ -v --tb=short --maxfail=5

TEST_RESULT=$?

echo ""
echo "=================================================="
echo "Test execution completed with exit code: $TEST_RESULT"
if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED!"
else
    echo "❌ SOME TESTS FAILED!"
fi
echo "=================================================="

exit $TEST_RESULT