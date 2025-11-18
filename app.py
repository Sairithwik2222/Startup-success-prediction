import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

from location_data import get_all_countries, get_states_for_country, get_cities_for_state, get_localities_for_city
from currency_data import get_currency_for_country, format_currency
from industry_metrics import get_industry_specific_fields, get_all_industries, get_business_models
from ml_model import StartupSuccessPredictor
from dashboard import render_dashboard
from database import init_db, save_prediction
from utils import (validate_startup_name, validate_team_size, validate_founding_year, 
                   validate_locality, show_success_message, show_error_message, 
                   show_warning_message, show_info_message)

st.set_page_config(page_title="Startup Success Predictor",
                   page_icon="🚀",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    .main {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main:hover {
        box-shadow: 0 12px 48px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        height: 3.5em;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1em;
        border: none;
        box-shadow: 0 4px 20px 0 rgba(0, 212, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px 0 rgba(123, 47, 247, 0.6);
        background: linear-gradient(135deg, #7b2ff7 0%, #00d4ff 100%);
    }
    
    h1 {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f72585 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0;
        font-weight: 700;
        font-size: 3em;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #00d4ff;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 100%) 1;
        padding-bottom: 0.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #e0e0e0;
        font-weight: 600;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(72, 187, 120, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(72, 187, 120, 0.5);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(72, 187, 120, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .success-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(72, 187, 120, 0.35);
        border: 2px solid rgba(72, 187, 120, 0.7);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(66, 153, 225, 0.1) 0%, rgba(66, 153, 225, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(66, 153, 225, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(66, 153, 225, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .info-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(66, 153, 225, 0.35);
        border: 2px solid rgba(66, 153, 225, 0.7);
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(237, 137, 54, 0.1) 0%, rgba(237, 137, 54, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(237, 137, 54, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(237, 137, 54, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .warning-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(237, 137, 54, 0.35);
        border: 2px solid rgba(237, 137, 54, 0.7);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 212, 255, 0.3);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.3);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 100%);
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        background-color: transparent;
        font-weight: 500;
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .step-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(123, 47, 247, 0.15) 100%);
        backdrop-filter: blur(10px);
        font-weight: 600;
        color: #e0e0e0;
        margin: 0.25rem;
        border: 1px solid rgba(0, 212, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .step-indicator:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    }
    
    .step-complete {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.5);
    }
    
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stAlert {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00d4ff !important;
    }
    
    .stSpinner > div {
        border-color: rgba(0, 212, 255, 0.3) !important;
        border-top-color: #00d4ff !important;
    }
    
    .stExpander {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stExpander:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        transform: translateX(5px);
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 1.5rem;
            margin: 0.5rem;
        }
        
        h1 {
            font-size: 2em !important;
        }
        
        h2 {
            font-size: 1.5em !important;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
        
        .step-indicator {
            font-size: 0.85em;
            padding: 0.4rem 0.8rem;
        }
        
        [data-testid="stSidebar"] {
            box-shadow: none;
        }
    }
    
    @media (max-width: 480px) {
        .main {
            padding: 1rem;
            margin: 0.25rem;
            border-radius: 16px;
        }
        
        h1 {
            font-size: 1.75em !important;
        }
        
        .stButton>button {
            height: 3em;
            font-size: 1em;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    
    html {
        scroll-behavior: smooth;
    }
    
    *:focus-visible {
        outline: 2px solid #00d4ff;
        outline-offset: 2px;
    }
    
    .stProgress > div > div {
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stDataFrame"] {
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get('theme', 'dark') == 'light':
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #e0e7ff 100%) !important;
        }
        
        .main {
            background: rgba(255, 255, 255, 0.7) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 50%, #e0e7ff 100%) !important;
            border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.6) 0%, rgba(255, 255, 255, 0.3) 100%) !important;
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        h2 {
            color: #667eea !important;
            border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1 !important;
        }
        
        h3, p, label, .stMarkdown {
            color: #2d3748 !important;
        }
        
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid rgba(102, 126, 234, 0.2) !important;
            color: #2d3748 !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            box-shadow: 0 4px 20px 0 rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            box-shadow: 0 8px 30px 0 rgba(118, 75, 162, 0.6) !important;
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        }
        
        .metric-card:hover {
            box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.25) !important;
            border: 1px solid rgba(102, 126, 234, 0.4) !important;
        }
        
        .success-box {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(72, 187, 120, 0.08) 100%) !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
        }
        
        .info-box {
            background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(66, 153, 225, 0.08) 100%) !important;
            border: 2px solid rgba(66, 153, 225, 0.6) !important;
        }
        
        .warning-box {
            background: linear-gradient(135deg, rgba(237, 137, 54, 0.15) 0%, rgba(237, 137, 54, 0.08) 100%) !important;
            border: 2px solid rgba(237, 137, 54, 0.6) !important;
        }
        
        .step-indicator {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
            border: 1px solid rgba(102, 126, 234, 0.4) !important;
            color: #2d3748 !important;
        }
        
        .step-complete {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        .stExpander {
            background: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
        }
        
        .stAlert {
            background: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown p {
            color: #2d3748 !important;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #667eea !important;
        }
        </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'startup_data' not in st.session_state:
    st.session_state.startup_data = {}
if 'predictor' not in st.session_state:
    with st.spinner('🤖 Initializing AI prediction models...'):
        st.session_state.predictor = StartupSuccessPredictor()
        st.session_state.predictor.train_models()
if 'page' not in st.session_state:
    st.session_state.page = 'Prediction Tool'
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'


def reset_form():
    st.session_state.step = 1
    st.session_state.startup_data = {}
    st.rerun()


def render_prediction_tool():
    st.title("🚀 Startup Success Prediction Platform")
    st.markdown(
        "<p style='text-align: center; font-size: 1.2em; color: #b0b0b0; margin-bottom: 2rem;'>Predict your startup's success probability using AI-powered analysis across all industries and global regions</p>",
        unsafe_allow_html=True
    )

    progress_value = (st.session_state.step - 1) / 4
    st.progress(progress_value)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = "step-complete" if st.session_state.step > 1 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 1 else '1️⃣'} Basic Info</div>",
            unsafe_allow_html=True)
    with col2:
        status = "step-complete" if st.session_state.step > 2 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 2 else '2️⃣'} Location</div>",
            unsafe_allow_html=True)
    with col3:
        status = "step-complete" if st.session_state.step > 3 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 3 else '3️⃣'} Industry Details</div>",
            unsafe_allow_html=True)
    with col4:
        status = "step-complete" if st.session_state.step > 4 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 4 else '4️⃣'} Prediction</div>",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.step == 1:
        st.header("Step 1: Basic Startup Information")

        col1, col2 = st.columns(2)

        with col1:
            startup_name = st.text_input("Startup Name *",
                                         value=st.session_state.startup_data.get(
                                             'startup_name', ''),
                                         placeholder="Enter your startup name")

            industry = st.selectbox("Industry *",
                                    options=get_all_industries(),
                                    index=get_all_industries().index(
                                        st.session_state.startup_data.get(
                                            'industry', 'Software & IT')))

            team_size = st.number_input(
                "Team Size *",
                min_value=1,
                max_value=1000,
                value=st.session_state.startup_data.get('team_size', 5),
                help="Total number of team members including founders")

        with col2:
            current_year = datetime.now().year
            founding_year = st.number_input(
                "Founding Year *",
                min_value=2000,
                max_value=current_year,
                value=st.session_state.startup_data.get('founding_year',
                                                        current_year),
                help="Year the startup was founded")

            business_models = get_business_models()
            business_model_options = list(business_models.keys())
            selected_model = st.selectbox("Business Model *",
                                          options=business_model_options,
                                          index=business_model_options.index(
                                              st.session_state.startup_data.get(
                                                  'business_model',
                                                  'B2C (Business-to-Consumer)')))

            with st.expander("ℹ️ What is this business model?"):
                st.write(f"**{selected_model}**")
                st.write(business_models[selected_model]['description'])
                st.write(
                    f"*Examples:* {business_models[selected_model]['examples']}")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Next: Location Details →", type="primary"):
            # Validate all inputs
            name_valid, name_error = validate_startup_name(startup_name)
            team_valid, team_error = validate_team_size(team_size)
            year_valid, year_error = validate_founding_year(founding_year)
            
            if not name_valid:
                show_error_message(name_error)
            elif not team_valid:
                show_error_message(team_error)
            elif not year_valid:
                show_error_message(year_error)
            else:
                st.session_state.startup_data.update({
                    'startup_name':
                    startup_name.strip(),
                    'industry':
                    industry,
                    'team_size':
                    team_size,
                    'founding_year':
                    founding_year,
                    'business_model':
                    selected_model
                })
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.header("Step 2: Location & Funding")

        col1, col2 = st.columns(2)

        with col1:
            countries = get_all_countries()
            default_country = st.session_state.startup_data.get('country', 'India')
            country_index = countries.index(
                default_country) if default_country in countries else 0

            country = st.selectbox("Country *",
                                   options=countries,
                                   index=country_index,
                                   key="country_selector")

            states_dict = get_states_for_country(country)
            states = list(
                states_dict.keys()) if states_dict else ["Default Region"]

            if not states:
                states = ["Default Region"]

            saved_state = st.session_state.startup_data.get('state', '')
            saved_country = st.session_state.startup_data.get('country', '')

            if country != saved_country or saved_state not in states:
                state_index = 0
            else:
                state_index = states.index(saved_state)

            state = st.selectbox("State/Region *",
                                 options=states,
                                 index=state_index,
                                 key="state_selector")

            cities = get_cities_for_state(country, state)
            if not cities:
                cities = ["Default City"]

            saved_city = st.session_state.startup_data.get('city', '')
            city_index = cities.index(saved_city) if saved_city in cities else 0

            city = st.selectbox("City *",
                                options=cities,
                                index=city_index,
                                key="city_selector")

            saved_locality = st.session_state.startup_data.get('locality', '')

            locality = st.text_input(
                "Locality/Area/Neighborhood *",
                value=saved_locality,
                placeholder=
                "e.g., Koramangala, Downtown, Central Business District, Tech Park Area",
                help=
                "Enter the specific locality, area, or neighborhood where your startup is located",
                key="locality_input")

        with col2:
            currency_info = get_currency_for_country(country)
            st.info(
                f"💱 Currency: **{currency_info['name']} ({currency_info['code']})**"
            )

            funding_amount = st.number_input(
                f"Funding Amount ({currency_info['symbol']}) *",
                min_value=0.0,
                max_value=1000000000.0,
                value=float(st.session_state.startup_data.get('funding_amount',
                                                              0)),
                step=10000.0,
                help=f"Total funding raised in {currency_info['code']}")

            st.markdown("#### Selected Location")
            st.markdown(f"""
            <div class="info-box">
            <strong>📍 Full Address:</strong><br>
            {locality}<br>
            {city}, {state}<br>
            {country}
            </div>
            """,
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", type="secondary"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next: Industry Details →", type="primary"):
                # Validate locality
                locality_valid, locality_error = validate_locality(locality)
                
                if not locality_valid:
                    show_error_message(locality_error)
                else:
                    st.session_state.startup_data.update({
                        'country':
                        country,
                        'state':
                        state,
                        'city':
                        city,
                        'locality':
                        locality.strip(),
                        'funding_amount':
                        funding_amount,
                        'currency':
                        currency_info
                    })
                    st.session_state.step = 3
                    st.rerun()

    elif st.session_state.step == 3:
        st.header(
            f"Step 3: {st.session_state.startup_data['industry']} Specific Details"
        )

        industry = st.session_state.startup_data['industry']
        industry_data = get_industry_specific_fields(industry)

        st.info(
            f"Please provide specific details about your {industry.lower()} startup to improve prediction accuracy."
        )

        industry_metrics = {}

        fields = industry_data.get('fields', [])

        if len(fields) > 0:
            num_cols = 2
            rows = (len(fields) + num_cols - 1) // num_cols

            for row in range(rows):
                cols = st.columns(num_cols)

                for col_idx in range(num_cols):
                    field_idx = row * num_cols + col_idx

                    if field_idx < len(fields):
                        field = fields[field_idx]

                        with cols[col_idx]:
                            if field['type'] == 'number':
                                value = st.number_input(
                                    field['label'],
                                    min_value=field.get('min', 0),
                                    max_value=field.get('max', 100000),
                                    value=st.session_state.startup_data.get(
                                        'industry_metrics',
                                        {}).get(field['name'],
                                                field.get('default', 0)),
                                    key=field['name'])
                                industry_metrics[field['name']] = value

                            elif field['type'] == 'select':
                                options = field.get('options', [])
                                default_val = st.session_state.startup_data.get(
                                    'industry_metrics',
                                    {}).get(field['name'], options[0])
                                index = options.index(
                                    default_val) if default_val in options else 0

                                value = st.selectbox(field['label'],
                                                     options=options,
                                                     index=index,
                                                     key=field['name'])
                                industry_metrics[field['name']] = value

                            elif field['type'] == 'slider':
                                value = st.slider(
                                    field['label'],
                                    min_value=field.get('min', 0),
                                    max_value=field.get('max', 10),
                                    value=st.session_state.startup_data.get(
                                        'industry_metrics',
                                        {}).get(field['name'],
                                                field.get('default', 5)),
                                    key=field['name'])
                                industry_metrics[field['name']] = value

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", type="secondary"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Generate Prediction 🎯", type="primary"):
                st.session_state.startup_data[
                    'industry_metrics'] = industry_metrics
                st.session_state.step = 4
                st.rerun()

            elif st.session_state.step == 4:
                st.header("🎯 Success Prediction Results")

    # Enhanced loading state with progress messages
    progress_placeholder = st.empty()
    
    with st.spinner('🤖 Analyzing your startup with AI models...'):
        progress_placeholder.info("⏳ Loading ML models...")
        prediction_result = st.session_state.predictor.predict(
            st.session_state.startup_data)
        
        progress_placeholder.info("💾 Saving prediction to database...")
        try:
            prediction_id = save_prediction(st.session_state.startup_data, prediction_result)
            progress_placeholder.empty()
            show_success_message(f"Prediction saved successfully! (ID: {prediction_id})")
        except Exception as e:
            progress_placeholder.empty()
            show_warning_message(f"Prediction generated but not saved to database: {str(e)}")

    success_prob = prediction_result['success_probability']
    confidence = prediction_result['confidence_interval']

    st.markdown(f"""
    <div class="success-box" style="text-align: center;">
        <h2 style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 1.8em;">Success Probability</h2>
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; font-size: 5em; font-weight: 800;">{success_prob:.1f}%</h1>
        <p style="font-size: 1.3em; margin: 0; color: #b0b0b0; font-weight: 500;">Confidence Interval: ±{confidence:.1f}%</p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if success_prob >= 70:
            verdict = "High Success Potential"
            color = "#48bb78"
            icon = "🟢"
        elif success_prob >= 50:
            verdict = "Moderate Success Potential"
            color = "#ed8936"
            icon = "🟡"
        else:
            verdict = "Needs Improvement"
            color = "#f56565"
            icon = "🔴"

        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">{icon} Verdict</h3>
            <h2 style="color: {color}; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{verdict}</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        avg_accuracy = np.mean([
            acc['mean']
            for acc in prediction_result['model_accuracies'].values()
        ])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">🎯 Model Accuracy</h3>
            <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{avg_accuracy*100:.1f}%</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        risk_level = "Low" if success_prob >= 70 else "Medium" if success_prob >= 50 else "High"
        risk_color = "#48bb78" if risk_level == "Low" else "#ed8936" if risk_level == "Medium" else "#f56565"
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">⚠️ Risk Level</h3>
            <h2 style="color: {risk_color}; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{risk_level}</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=success_prob,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Success Probability", 'font': {'size': 24, 'color': '#e0e0e0'}},
        number={'font': {'size': 60, 'color': '#00d4ff'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#e0e0e0', 'tickfont': {'color': '#e0e0e0'}},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(245, 101, 101, 0.3)'},
                {'range': [50, 70], 'color': 'rgba(237, 137, 54, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(72, 187, 120, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': success_prob
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0'},
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Model Predictions Breakdown")
    
    model_predictions = prediction_result.get('model_predictions', {})
    if not model_predictions:
        st.error("No model predictions to display. Please check your input data or model output.")
    else:
        model_names = list(model_predictions.keys())
        model_probs = list(model_predictions.values())

        fig2 = go.Figure(data=[
            go.Bar(
                x=model_names,
                y=model_probs,
                marker=dict(
                    color=model_probs,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Probability %", titlefont=dict(color='#e0e0e0'), tickfont=dict(color='#e0e0e0'))
                ),
                text=[f"{p:.1f}%" for p in model_probs],
                textposition='outside',
                textfont=dict(color='#e0e0e0')
            )
        ])

       import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

from location_data import get_all_countries, get_states_for_country, get_cities_for_state, get_localities_for_city
from currency_data import get_currency_for_country, format_currency
from industry_metrics import get_industry_specific_fields, get_all_industries, get_business_models
from ml_model import StartupSuccessPredictor
from dashboard import render_dashboard
from database import init_db, save_prediction
from utils import (validate_startup_name, validate_team_size, validate_founding_year, 
                   validate_locality, show_success_message, show_error_message, 
                   show_warning_message, show_info_message)

st.set_page_config(page_title="Startup Success Predictor",
                   page_icon="🚀",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    .main {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main:hover {
        box-shadow: 0 12px 48px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        height: 3.5em;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1em;
        border: none;
        box-shadow: 0 4px 20px 0 rgba(0, 212, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px 0 rgba(123, 47, 247, 0.6);
        background: linear-gradient(135deg, #7b2ff7 0%, #00d4ff 100%);
    }
    
    h1 {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f72585 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0;
        font-weight: 700;
        font-size: 3em;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #00d4ff;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 100%) 1;
        padding-bottom: 0.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #e0e0e0;
        font-weight: 600;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(72, 187, 120, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(72, 187, 120, 0.5);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(72, 187, 120, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .success-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(72, 187, 120, 0.35);
        border: 2px solid rgba(72, 187, 120, 0.7);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(66, 153, 225, 0.1) 0%, rgba(66, 153, 225, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(66, 153, 225, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(66, 153, 225, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .info-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(66, 153, 225, 0.35);
        border: 2px solid rgba(66, 153, 225, 0.7);
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(237, 137, 54, 0.1) 0%, rgba(237, 137, 54, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(237, 137, 54, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(237, 137, 54, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .warning-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(237, 137, 54, 0.35);
        border: 2px solid rgba(237, 137, 54, 0.7);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 212, 255, 0.3);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.3);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 100%);
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        background-color: transparent;
        font-weight: 500;
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .step-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(123, 47, 247, 0.15) 100%);
        backdrop-filter: blur(10px);
        font-weight: 600;
        color: #e0e0e0;
        margin: 0.25rem;
        border: 1px solid rgba(0, 212, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .step-indicator:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    }
    
    .step-complete {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.5);
    }
    
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stAlert {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00d4ff !important;
    }
    
    .stSpinner > div {
        border-color: rgba(0, 212, 255, 0.3) !important;
        border-top-color: #00d4ff !important;
    }
    
    .stExpander {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stExpander:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        transform: translateX(5px);
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 1.5rem;
            margin: 0.5rem;
        }
        
        h1 {
            font-size: 2em !important;
        }
        
        h2 {
            font-size: 1.5em !important;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
        
        .step-indicator {
            font-size: 0.85em;
            padding: 0.4rem 0.8rem;
        }
        
        [data-testid="stSidebar"] {
            box-shadow: none;
        }
    }
    
    @media (max-width: 480px) {
        .main {
            padding: 1rem;
            margin: 0.25rem;
            border-radius: 16px;
        }
        
        h1 {
            font-size: 1.75em !important;
        }
        
        .stButton>button {
            height: 3em;
            font-size: 1em;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    
    html {
        scroll-behavior: smooth;
    }
    
    *:focus-visible {
        outline: 2px solid #00d4ff;
        outline-offset: 2px;
    }
    
    .stProgress > div > div {
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stDataFrame"] {
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get('theme', 'dark') == 'light':
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #e0e7ff 100%) !important;
        }
        
        .main {
            background: rgba(255, 255, 255, 0.7) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 50%, #e0e7ff 100%) !important;
            border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.6) 0%, rgba(255, 255, 255, 0.3) 100%) !important;
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        h2 {
            color: #667eea !important;
            border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1 !important;
        }
        
        h3, p, label, .stMarkdown {
            color: #2d3748 !important;
        }
        
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid rgba(102, 126, 234, 0.2) !important;
            color: #2d3748 !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            box-shadow: 0 4px 20px 0 rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            box-shadow: 0 8px 30px 0 rgba(118, 75, 162, 0.6) !important;
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        }
        
        .metric-card:hover {
            box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.25) !important;
            border: 1px solid rgba(102, 126, 234, 0.4) !important;
        }
        
        .success-box {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(72, 187, 120, 0.08) 100%) !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
        }
        
        .info-box {
            background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(66, 153, 225, 0.08) 100%) !important;
            border: 2px solid rgba(66, 153, 225, 0.6) !important;
        }
        
        .warning-box {
            background: linear-gradient(135deg, rgba(237, 137, 54, 0.15) 0%, rgba(237, 137, 54, 0.08) 100%) !important;
            border: 2px solid rgba(237, 137, 54, 0.6) !important;
        }
        
        .step-indicator {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
            border: 1px solid rgba(102, 126, 234, 0.4) !important;
            color: #2d3748 !important;
        }
        
        .step-complete {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        .stExpander {
            background: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
        }
        
        .stAlert {
            background: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown p {
            color: #2d3748 !important;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #667eea !important;
        }
        </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'startup_data' not in st.session_state:
    st.session_state.startup_data = {}
if 'predictor' not in st.session_state:
    with st.spinner('🤖 Initializing AI prediction models...'):
        st.session_state.predictor = StartupSuccessPredictor()
        st.session_state.predictor.train_models()
if 'page' not in st.session_state:
    st.session_state.page = 'Prediction Tool'
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'


def reset_form():
    st.session_state.step = 1
    st.session_state.startup_data = {}
    st.rerun()


def render_prediction_tool():
    st.title("🚀 Startup Success Prediction Platform")
    st.markdown(
        "<p style='text-align: center; font-size: 1.2em; color: #b0b0b0; margin-bottom: 2rem;'>Predict your startup's success probability using AI-powered analysis across all industries and global regions</p>",
        unsafe_allow_html=True
    )

    progress_value = (st.session_state.step - 1) / 4
    st.progress(progress_value)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = "step-complete" if st.session_state.step > 1 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 1 else '1️⃣'} Basic Info</div>",
            unsafe_allow_html=True)
    with col2:
        status = "step-complete" if st.session_state.step > 2 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 2 else '2️⃣'} Location</div>",
            unsafe_allow_html=True)
    with col3:
        status = "step-complete" if st.session_state.step > 3 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 3 else '3️⃣'} Industry Details</div>",
            unsafe_allow_html=True)
    with col4:
        status = "step-complete" if st.session_state.step > 4 else ""
        st.markdown(
            f"<div class='step-indicator {status}'>{'✅' if st.session_state.step > 4 else '4️⃣'} Prediction</div>",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.step == 1:
        st.header("Step 1: Basic Startup Information")

        col1, col2 = st.columns(2)

        with col1:
            startup_name = st.text_input("Startup Name *",
                                         value=st.session_state.startup_data.get(
                                             'startup_name', ''),
                                         placeholder="Enter your startup name")

            industry = st.selectbox("Industry *",
                                    options=get_all_industries(),
                                    index=get_all_industries().index(
                                        st.session_state.startup_data.get(
                                            'industry', 'Software & IT')))

            team_size = st.number_input(
                "Team Size *",
                min_value=1,
                max_value=1000,
                value=st.session_state.startup_data.get('team_size', 5),
                help="Total number of team members including founders")

        with col2:
            current_year = datetime.now().year
            founding_year = st.number_input(
                "Founding Year *",
                min_value=2000,
                max_value=current_year,
                value=st.session_state.startup_data.get('founding_year',
                                                        current_year),
                help="Year the startup was founded")

            business_models = get_business_models()
            business_model_options = list(business_models.keys())
            selected_model = st.selectbox("Business Model *",
                                          options=business_model_options,
                                          index=business_model_options.index(
                                              st.session_state.startup_data.get(
                                                  'business_model',
                                                  'B2C (Business-to-Consumer)')))

            with st.expander("ℹ️ What is this business model?"):
                st.write(f"**{selected_model}**")
                st.write(business_models[selected_model]['description'])
                st.write(
                    f"*Examples:* {business_models[selected_model]['examples']}")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Next: Location Details →", type="primary"):
            # Validate all inputs
            name_valid, name_error = validate_startup_name(startup_name)
            team_valid, team_error = validate_team_size(team_size)
            year_valid, year_error = validate_founding_year(founding_year)
            
            if not name_valid:
                show_error_message(name_error)
            elif not team_valid:
                show_error_message(team_error)
            elif not year_valid:
                show_error_message(year_error)
            else:
                st.session_state.startup_data.update({
                    'startup_name':
                    startup_name.strip(),
                    'industry':
                    industry,
                    'team_size':
                    team_size,
                    'founding_year':
                    founding_year,
                    'business_model':
                    selected_model
                })
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.header("Step 2: Location & Funding")

        col1, col2 = st.columns(2)

        with col1:
            countries = get_all_countries()
            default_country = st.session_state.startup_data.get('country', 'India')
            country_index = countries.index(
                default_country) if default_country in countries else 0

            country = st.selectbox("Country *",
                                   options=countries,
                                   index=country_index,
                                   key="country_selector")

            states_dict = get_states_for_country(country)
            states = list(
                states_dict.keys()) if states_dict else ["Default Region"]

            if not states:
                states = ["Default Region"]

            saved_state = st.session_state.startup_data.get('state', '')
            saved_country = st.session_state.startup_data.get('country', '')

            if country != saved_country or saved_state not in states:
                state_index = 0
            else:
                state_index = states.index(saved_state)

            state = st.selectbox("State/Region *",
                                 options=states,
                                 index=state_index,
                                 key="state_selector")

            cities = get_cities_for_state(country, state)
            if not cities:
                cities = ["Default City"]

            saved_city = st.session_state.startup_data.get('city', '')
            city_index = cities.index(saved_city) if saved_city in cities else 0

            city = st.selectbox("City *",
                                options=cities,
                                index=city_index,
                                key="city_selector")

            saved_locality = st.session_state.startup_data.get('locality', '')

            locality = st.text_input(
                "Locality/Area/Neighborhood *",
                value=saved_locality,
                placeholder=
                "e.g., Koramangala, Downtown, Central Business District, Tech Park Area",
                help=
                "Enter the specific locality, area, or neighborhood where your startup is located",
                key="locality_input")

        with col2:
            currency_info = get_currency_for_country(country)
            st.info(
                f"💱 Currency: **{currency_info['name']} ({currency_info['code']})**"
            )

            funding_amount = st.number_input(
                f"Funding Amount ({currency_info['symbol']}) *",
                min_value=0.0,
                max_value=1000000000.0,
                value=float(st.session_state.startup_data.get('funding_amount',
                                                              0)),
                step=10000.0,
                help=f"Total funding raised in {currency_info['code']}")

            st.markdown("#### Selected Location")
            st.markdown(f"""
            <div class="info-box">
            <strong>📍 Full Address:</strong><br>
            {locality}<br>
            {city}, {state}<br>
            {country}
            </div>
            """,
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", type="secondary"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next: Industry Details →", type="primary"):
                # Validate locality
                locality_valid, locality_error = validate_locality(locality)
                
                if not locality_valid:
                    show_error_message(locality_error)
                else:
                    st.session_state.startup_data.update({
                        'country':
                        country,
                        'state':
                        state,
                        'city':
                        city,
                        'locality':
                        locality.strip(),
                        'funding_amount':
                        funding_amount,
                        'currency':
                        currency_info
                    })
                    st.session_state.step = 3
                    st.rerun()

    elif st.session_state.step == 3:
        st.header(
            f"Step 3: {st.session_state.startup_data['industry']} Specific Details"
        )

        industry = st.session_state.startup_data['industry']
        industry_data = get_industry_specific_fields(industry)

        st.info(
            f"Please provide specific details about your {industry.lower()} startup to improve prediction accuracy."
        )

        industry_metrics = {}

        fields = industry_data.get('fields', [])

        if len(fields) > 0:
            num_cols = 2
            rows = (len(fields) + num_cols - 1) // num_cols

            for row in range(rows):
                cols = st.columns(num_cols)

                for col_idx in range(num_cols):
                    field_idx = row * num_cols + col_idx

                    if field_idx < len(fields):
                        field = fields[field_idx]

                        with cols[col_idx]:
                            if field['type'] == 'number':
                                value = st.number_input(
                                    field['label'],
                                    min_value=field.get('min', 0),
                                    max_value=field.get('max', 100000),
                                    value=st.session_state.startup_data.get(
                                        'industry_metrics',
                                        {}).get(field['name'],
                                                field.get('default', 0)),
                                    key=field['name'])
                                industry_metrics[field['name']] = value

                            elif field['type'] == 'select':
                                options = field.get('options', [])
                                default_val = st.session_state.startup_data.get(
                                    'industry_metrics',
                                    {}).get(field['name'], options[0])
                                index = options.index(
                                    default_val) if default_val in options else 0

                                value = st.selectbox(field['label'],
                                                     options=options,
                                                     index=index,
                                                     key=field['name'])
                                industry_metrics[field['name']] = value

                            elif field['type'] == 'slider':
                                value = st.slider(
                                    field['label'],
                                    min_value=field.get('min', 0),
                                    max_value=field.get('max', 10),
                                    value=st.session_state.startup_data.get(
                                        'industry_metrics',
                                        {}).get(field['name'],
                                                field.get('default', 5)),
                                    key=field['name'])
                                industry_metrics[field['name']] = value

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", type="secondary"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Generate Prediction 🎯", type="primary"):
                st.session_state.startup_data[
                    'industry_metrics'] = industry_metrics
                st.session_state.step = 4
                st.rerun()

            elif st.session_state.step == 4:
                st.header("🎯 Success Prediction Results")

    # Enhanced loading state with progress messages
    progress_placeholder = st.empty()
    
    with st.spinner('🤖 Analyzing your startup with AI models...'):
        progress_placeholder.info("⏳ Loading ML models...")
        prediction_result = st.session_state.predictor.predict(
            st.session_state.startup_data)
        
        progress_placeholder.info("💾 Saving prediction to database...")
        try:
            prediction_id = save_prediction(st.session_state.startup_data, prediction_result)
            progress_placeholder.empty()
            show_success_message(f"Prediction saved successfully! (ID: {prediction_id})")
        except Exception as e:
            progress_placeholder.empty()
            show_warning_message(f"Prediction generated but not saved to database: {str(e)}")

    success_prob = prediction_result['success_probability']
    confidence = prediction_result['confidence_interval']

    st.markdown(f"""
    <div class="success-box" style="text-align: center;">
        <h2 style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 1.8em;">Success Probability</h2>
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; font-size: 5em; font-weight: 800;">{success_prob:.1f}%</h1>
        <p style="font-size: 1.3em; margin: 0; color: #b0b0b0; font-weight: 500;">Confidence Interval: ±{confidence:.1f}%</p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if success_prob >= 70:
            verdict = "High Success Potential"
            color = "#48bb78"
            icon = "🟢"
        elif success_prob >= 50:
            verdict = "Moderate Success Potential"
            color = "#ed8936"
            icon = "🟡"
        else:
            verdict = "Needs Improvement"
            color = "#f56565"
            icon = "🔴"

        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">{icon} Verdict</h3>
            <h2 style="color: {color}; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{verdict}</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        avg_accuracy = np.mean([
            acc['mean']
            for acc in prediction_result['model_accuracies'].values()
        ])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">🎯 Model Accuracy</h3>
            <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{avg_accuracy*100:.1f}%</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        risk_level = "Low" if success_prob >= 70 else "Medium" if success_prob >= 50 else "High"
        risk_color = "#48bb78" if risk_level == "Low" else "#ed8936" if risk_level == "Medium" else "#f56565"
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1em; color: #b0b0b0; margin: 0;">⚠️ Risk Level</h3>
            <h2 style="color: {risk_color}; margin: 10px 0; font-size: 1.5em; font-weight: 700;">{risk_level}</h2>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=success_prob,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Success Probability", 'font': {'size': 24, 'color': '#e0e0e0'}},
        number={'font': {'size': 60, 'color': '#00d4ff'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#e0e0e0', 'tickfont': {'color': '#e0e0e0'}},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(245, 101, 101, 0.3)'},
                {'range': [50, 70], 'color': 'rgba(237, 137, 54, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(72, 187, 120, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': success_prob
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0'},
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Model Predictions Breakdown")
    
    model_predictions = prediction_result.get('model_predictions', {})
    if not model_predictions:
        st.error("No model predictions to display. Please check your input data or model output.")
    else:
        model_names = list(model_predictions.keys())
        model_probs = list(model_predictions.values())

        fig2 = go.Figure(data=[
            go.Bar(
                x=model_names,
                y=model_probs,
                marker=dict(
                    color=model_probs,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Probability %", titlefont=dict(color='#e0e0e0'), tickfont=dict(color='#e0e0e0'))
                ),
                text=[f"{p:.1f}%" for p in model_probs],
                textposition='outside',
                textfont=dict(color='#e0e0e0')
            )
        ])

        fig2.update_layout(
            title="Individual Model Predictions",
            xaxis_title="ML Model",
            yaxis_title="Success Probability (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            xaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0')),
            yaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0'), gridcolor='rgba(255,255,255,0.1)'),
            height=400
        )
        try:
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying the model predictions graph: {e}")

    st.subheader("🔍 Feature Importance Analysis")

    featureimportance = prediction_result.get('featureimportance', {})
    if not featureimportance:
        st.error("No feature importance data available from the models.")
    else:
        topfeatures = dict(list(featureimportance.items())[:5])
        featurenames = list(topfeatures.keys())
        importancescores = [v for v in topfeatures.values()]

        fig3 = go.Figure(data=[
            go.Bar(
                y=featurenames,
                x=importancescores,
                orientation='h',
                marker=dict(color="#00d4ff"),
                text=[f"{s:.3f}" for s in importancescores],
                textposition='outside',
                textfont=dict(color='#e0e0e0')
            )
        ])

        fig3.update_layout(
            title="Top 5 Most Important Factors",
            xaxis_title="Importance Score",
            yaxis_title="Feature",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            xaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0'), gridcolor='rgba(255,255,255,0.1)'),
            height=400
        )
        try:
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying feature importance graph: {e}")

    # Add additional per-model analysis or graphs if available similarly
    # Example placeholder:
    # regression_output = prediction_result.get('regression_output')
    # if regression_output:
    #     ... plot regression related graphs with safety checks



        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Prediction", type="primary"):
                reset_form()
        
        with col2:
            if st.button("← Back to Edit Details", type="secondary"):
                st.session_state.step = 3
                st.rerun()


with st.sidebar:
    st.markdown("## 🚀 Navigation")
    
    page_options = ["Prediction Tool", "Analytics Dashboard"]
    selected_page = st.radio("Go to:", page_options, index=page_options.index(st.session_state.page))
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🎨 Theme")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    with col2:
        if st.button("☀️ Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    This AI-powered platform helps predict startup success using:
    
    - **Machine Learning Models**: 4 ensemble algorithms
    - **Global Coverage**: 200+ countries
    - **Industry Support**: 8+ sectors
    - **Real-time Analysis**: Instant predictions
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    1. Enter basic startup info
    2. Provide location details
    3. Add industry-specific metrics
    4. Get AI-powered prediction
    """)

if st.session_state.page == "Prediction Tool":
    render_prediction_tool()
elif st.session_state.page == "Analytics Dashboard":
    render_dashboard()


        fig3 = go.Figure(data=[
            go.Bar(
                y=featurenames,
                x=importancescores,
                orientation='h',
                marker=dict(color="#00d4ff"),
                text=[f"{s:.3f}" for s in importancescores],
                textposition='outside',
                textfont=dict(color='#e0e0e0')
            )
        ])

        fig3.update_layout(
            title="Top 5 Most Important Factors",
            xaxis_title="Importance Score",
            yaxis_title="Feature",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            xaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(tickfont=dict(color='#e0e0e0'), titlefont=dict(color='#e0e0e0'), gridcolor='rgba(255,255,255,0.1)'),
            height=400
        )
        try:
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying feature importance graph: {e}")

    # Add additional per-model analysis or graphs if available similarly
    # Example placeholder:
    # regression_output = prediction_result.get('regression_output')
    # if regression_output:
    #     ... plot regression related graphs with safety checks



        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Prediction", type="primary"):
                reset_form()
        
        with col2:
            if st.button("← Back to Edit Details", type="secondary"):
                st.session_state.step = 3
                st.rerun()


with st.sidebar:
    st.markdown("## 🚀 Navigation")
    
    page_options = ["Prediction Tool", "Analytics Dashboard"]
    selected_page = st.radio("Go to:", page_options, index=page_options.index(st.session_state.page))
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🎨 Theme")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    with col2:
        if st.button("☀️ Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    This AI-powered platform helps predict startup success using:
    
    - **Machine Learning Models**: 4 ensemble algorithms
    - **Global Coverage**: 200+ countries
    - **Industry Support**: 8+ sectors
    - **Real-time Analysis**: Instant predictions
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    1. Enter basic startup info
    2. Provide location details
    3. Add industry-specific metrics
    4. Get AI-powered prediction
    """)

if st.session_state.page == "Prediction Tool":
    render_prediction_tool()
elif st.session_state.page == "Analytics Dashboard":
    render_dashboard()
