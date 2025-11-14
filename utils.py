import pandas as pd
import json
from datetime import datetime
import streamlit as st

def validate_startup_name(name):
    """Validate startup name input"""
    if not name or not name.strip():
        return False, "Startup name is required"
    if len(name.strip()) < 2:
        return False, "Startup name must be at least 2 characters"
    if len(name.strip()) > 100:
        return False, "Startup name must be less than 100 characters"
    return True, ""

def validate_team_size(size):
    """Validate team size"""
    if size < 1:
        return False, "Team must have at least 1 member"
    if size > 10000:
        return False, "Team size seems unrealistic (max 10,000)"
    return True, ""

def validate_founding_year(year):
    """Validate founding year"""
    current_year = datetime.now().year
    if year < 2000:
        return False, "Founding year must be 2000 or later"
    if year > current_year:
        return False, f"Founding year cannot be in the future (max {current_year})"
    return True, ""

def validate_locality(locality):
    """Validate locality input"""
    if not locality or not locality.strip():
        return False, "Locality/area is required"
    if len(locality.strip()) < 2:
        return False, "Locality must be at least 2 characters"
    return True, ""

def export_predictions_to_csv(predictions):
    """Export predictions to CSV format"""
    if not predictions:
        return None
    
    data = []
    for pred in predictions:
        data.append({
            'Date': pred.get('created_at', '').strftime('%Y-%m-%d %H:%M:%S') if isinstance(pred.get('created_at'), datetime) else str(pred.get('created_at', '')),
            'Startup Name': pred.get('startup_name', ''),
            'Industry': pred.get('industry', ''),
            'Country': pred.get('country', ''),
            'City': pred.get('city', ''),
            'Business Model': pred.get('business_model', ''),
            'Team Size': pred.get('team_size', ''),
            'Founding Year': pred.get('founding_year', ''),
            'Funding Amount': pred.get('funding_amount', 0),
            'Currency': pred.get('currency_code', ''),
            'Success Probability (%)': round(pred.get('success_probability', 0), 2),
            'Confidence Interval (%)': round(pred.get('confidence_interval', 0), 2)
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')

def export_predictions_to_json(predictions):
    """Export predictions to JSON format"""
    if not predictions:
        return None
    
    data = []
    for pred in predictions:
        export_data = {
            'date': pred.get('created_at', '').strftime('%Y-%m-%d %H:%M:%S') if isinstance(pred.get('created_at'), datetime) else str(pred.get('created_at', '')),
            'startup_name': pred.get('startup_name', ''),
            'industry': pred.get('industry', ''),
            'country': pred.get('country', ''),
            'state': pred.get('state', ''),
            'city': pred.get('city', ''),
            'locality': pred.get('locality', ''),
            'business_model': pred.get('business_model', ''),
            'team_size': pred.get('team_size', ''),
            'founding_year': pred.get('founding_year', ''),
            'funding_amount': pred.get('funding_amount', 0),
            'currency_code': pred.get('currency_code', ''),
            'currency_symbol': pred.get('currency_symbol', ''),
            'success_probability': round(pred.get('success_probability', 0), 2),
            'confidence_interval': round(pred.get('confidence_interval', 0), 2),
            'model_predictions': pred.get('model_predictions', {}),
            'feature_importance': pred.get('feature_importance', {})
        }
        data.append(export_data)
    
    return json.dumps(data, indent=2).encode('utf-8')

def show_success_message(message, duration=3):
    """Show a success message with auto-dismiss"""
    st.success(f"✅ {message}")

def show_error_message(message):
    """Show an error message"""
    st.error(f"❌ {message}")

def show_warning_message(message):
    """Show a warning message"""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Show an info message"""
    st.info(f"ℹ️ {message}")
