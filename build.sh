#!/bin/bash
export WORKSPACE=`pwd`
# Create/Activate virtualenv
virtualenv venv
source venv/bin/activate
# Install Requirements
pip install -r requirements.txt
# Run tests
py.test
