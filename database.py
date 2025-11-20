import streamlit as st

# ----------------------------------------------
#  🔥 DATABASE DISABLED VERSION (SAFE MODE)
#  No SQLAlchemy, No Neon, No connections.
#  All DB functions return dummy values safely.
# ----------------------------------------------

def init_db():
    # No DB initialization
    print("Database disabled — init_db() skipped.")
    return None

def save_prediction(startup_data, prediction_result):
    # Skip saving, return fake ID
    print("Database disabled — save_prediction() skipped.")
    return None  # or return 0

def get_all_predictions():
    # No database → return empty list
    return []

def get_predictions_count():
    return 0

def get_predictions_by_date_range(start_date=None, end_date=None):
    return []

def get_predictions_by_filters(industry=None, country=None, business_model=None):
    return []
