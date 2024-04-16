#!/bin/bash

# Exit on any error
set -e

# Create a virtual environment if it does not exist
if [ ! -d "env" ]; then
    python3 -m venv env
fi

# Activate the virtual environment
source env/bin/activate

# Ensure pip is up-to-date
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m src.test.test_api
