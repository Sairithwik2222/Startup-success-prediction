# Clean C2 with minimal comment
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

from database import init_db, save_prediction
from location_data import get_all_countries, get_states_for_country, get_cities_for_state
from currency_data import get_currency_for_country
from industry_metrics import get_industry_specific_fields, get_all_industries, get_business_models
from ml_model import StartupSuccessPredictor

try:
    init_db()
except Exception:
    pass

st.set_page_config(page_title="Startup Success Predictor", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.metric-card {background:#f8f9fa;border-radius:10px;padding:15px;box-shadow:0 2px 4px rgba(0,0,0,0.06);}
.success-box {background:#d4edda;border:2px solid #28a745;border-radius:10px;padding:20px;}
.info-box {background:#d1ecf1;border:2px solid #17a2b8;border-radius:10px;padding:15px;}
</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state.step=1
if "startup_data" not in st.session_state: st.session_state.startup_data={}
if "page" not in st.session_state: st.session_state.page="Prediction Tool"

if "predictor" not in st.session_state:
    with st.spinner("Loading models..."):
        st.session_state.predictor=StartupSuccessPredictor()
        try: st.session_state.predictor.train_models()
        except: pass

def reset_form():
    st.session_state.step=1
    st.session_state.startup_data={}
    st.experimental_rerun()

def format_currency(a,c): 
    return f"{c.get('symbol','')}{float(a):,.2f}"

# ---- Main Tool ----
def render_prediction_tool():
    st.title("🚀 Startup Success Prediction Platform")
    st.progress((st.session_state.step-1)/4)
    st.markdown("---")

    # STEP 1
    if st.session_state.step==1:
        st.header("Basic Info")
        c1,c2=st.columns(2)
        with c1:
            name=st.text_input("Startup Name *", st.session_state.startup_data.get("startup_name",""))
            industry=st.selectbox("Industry *", get_all_industries())
            team=st.number_input("Team Size *",1,1000,st.session_state.startup_data.get("team_size",5))
        with c2:
            year=datetime.now().year
            founded=st.number_input("Founding Year *",1900,year,st.session_state.startup_data.get("founding_year",year))
            bmodels=get_business_models()
            bm=st.selectbox("Business Model *", list(bmodels.keys()))
        if st.button("Next →"):
            if not name.strip(): st.error("Enter name")
            else:
                st.session_state.startup_data.update({"startup_name":name,"industry":industry,"team_size":team,"founding_year":founded,"business_model":bm})
                st.session_state.step=2; st.experimental_rerun()

    # STEP 2
    elif st.session_state.step==2:
        st.header("Location & Funding")
        c1,c2=st.columns(2)
        with c1:
            countries=get_all_countries()
            country=st.selectbox("Country *", countries)
            states=list((get_states_for_country(country) or {"Default":None}).keys())
            state=st.selectbox("State/Region *", states)
            cities=get_cities_for_state(country,state) or ["Default City"]
            city=st.selectbox("City *", cities)
            loc=st.text_input("Locality *", st.session_state.startup_data.get("locality",""))
        with c2:
            currency=get_currency_for_country(country)
            st.info(f"Currency: {currency['name']} ({currency['code']})")
            amt=st.number_input(f"Funding ({currency['symbol']})",0.0,1e9,float(st.session_state.startup_data.get("funding_amount",0)))
        if st.button("Next →"):
            if not loc.strip(): st.error("Enter locality")
            else:
                st.session_state.startup_data.update({"country":country,"state":state,"city":city,"locality":loc,"funding_amount":amt,"currency":currency})
                st.session_state.step=3; st.experimental_rerun()
        if st.button("← Back"):
            st.session_state.step=1; st.experimental_rerun()

    # STEP 3
    elif st.session_state.step==3:
        st.header("Industry Details")
        inds=st.session_state.startup_data["industry"]
        fields=get_industry_specific_fields(inds).get("fields",[])
        metrics={}
        for f in fields:
            if f["type"]=="number": metrics[f["name"]]=st.number_input(f["label"],value=f.get("default",0))
            elif f["type"]=="select": metrics[f["name"]]=st.selectbox(f["label"],f["options"])
            else: metrics[f["name"]]=st.slider(f["label"],f["min"],f["max"],f["default"])
        if st.button("Predict 🎯"):
            st.session_state.startup_data["industry_metrics"]=metrics
            st.session_state.step=4; st.experimental_rerun()
        if st.button("← Back"):
            st.session_state.step=2; st.experimental_rerun()

    # STEP 4
    elif st.session_state.step==4:
        st.header("Prediction Results")
        with st.spinner("Analyzing..."):
            data=st.session_state.startup_data
            try: res=st.session_state.predictor.predict(data)
            except: res={"success_probability":50,"confidence_interval":10,"model_predictions":{},"model_accuracies":{},"feature_importance":{}}
            try: save_prediction(data,res)
            except: pass

        sp=res["success_probability"]; ci=res["confidence_interval"]
        st.markdown(f"<div class='success-box' style='text-align:center;'><h2>Success Probability</h2><h1 style='font-size:3em;'>{sp:.1f}%</h1><p>±{ci:.1f}%</p></div>",unsafe_allow_html=True)

        if st.button("New Prediction"): reset_form()

# Sidebar + Navigation
def render_dashboard():
    st.title("📊 Dashboard Coming Soon")

st.sidebar.title("Navigation")
page=st.sidebar.radio("Select:",["Prediction Tool","Analytics Dashboard"])
if page=="Prediction Tool": render_prediction_tool()
else: render_dashboard()
