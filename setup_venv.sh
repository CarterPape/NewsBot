#!/bin/bash

# If needed, install then define a python3.12 to use

python3.12 -m venv venv

source ven/bin/activate

pipenv install --dev
