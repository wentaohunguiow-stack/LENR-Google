#!/bin/bash

# Ensure we're using the venv Python and Streamlit

# Activate virtual environment
source venv/bin/activate

# Run Streamlit from venv
python -m streamlit run web_ui/app.py
