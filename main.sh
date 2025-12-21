#!/usr/bin/env bash

# Exit immediately on error
set -e

# Absolute paths ONLY
PROJECT_DIR="/home/imtiaz/Downloads/Scrapping Codes"
VENV_PYTHON="/home/imtiaz/Downloads/Scrapping Codes/.venv/bin/python"

# Go to project directory
cd "$PROJECT_DIR" || exit 1

# Run script using venv python
"$VENV_PYTHON" main.py

