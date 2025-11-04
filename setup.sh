#!/usr/bin/env bash
set -e
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. Activate venv with: source venv/bin/activate"
