#!/bin/bash

# Exit on any error
set -e

# Activate the virtual environment
source env/bin/activate

# Run the script
python3 -m src.client.client_script
