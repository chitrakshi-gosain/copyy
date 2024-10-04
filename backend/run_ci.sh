#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define your Python version and the module name
PYTHON_VERSION="3.10"
MODULE_NAME="app"  # Change this to your actual module name

# Step 1: Set up Python 3.10
echo "Setting up Python $PYTHON_VERSION..."
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python $PYTHON_VERSION."
    exit 1
fi

# Step 2: Upgrade pip and install dependencies
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
pip install flake8 pytest pytest-cov black safety mypy fastapi httpx uvicorn

# Install additional requirements if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Step 3: Lint with flake8
echo "Linting with flake8..."
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 tests/ --count --exit-zero --max-complexity=10 --max-line-length=130 --statistics
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 tests/ --count --exit-zero --max-complexity=10 --max-line-length=130 --statistics

# Step 4: Format check with black
# echo "Checking code formatting with Black..."
# black --check .

# Step 5: Security check with safety
echo "Running security checks with Safety..."
safety check --ignore 70612

# Step 6: Type check with mypy
echo "Running type checks with mypy..."
mypy "$MODULE_NAME/"

# Step 7: Test with pytest
echo "Running tests with pytest..."
pytest --cov="$MODULE_NAME" --cov-report=term-missing --cov-report=html tests/

echo "All checks completed successfully!"
