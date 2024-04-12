#!/bin/bash

# Exit on error
set -e

# Create a virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip3 install -r requirements.txt

#pip install -e .

echo "Installation succesful!"
echo "Call \"source env/bin/activate\" to activate the virtual environment"
