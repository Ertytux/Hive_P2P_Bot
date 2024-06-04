#!/bin/bash

#Activate local python env
source ./venv/bin/activate
# Load data
source ./env_example

# Install dependencies
pip install -r requeriment.txt

# Run Bot service
python ./src/hcp2pb.py

