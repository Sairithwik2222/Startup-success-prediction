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

st.set_page_config(page_title="Startup Success Predictor",
                   page_icon="🚀",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
    }
    h2 {
        color: #2E86AB;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #333;
    }
    .success-box {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""",
            unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'startup_data' not in st.session_state:
    st.session_state.startup_data = {}
if 'predictor' not in st.session_state:
    with st.spinner('Initializing AI prediction models...'):
        st.session_state.predictor = StartupSuccessPredictor()
        st.session_state.predictor.train_models()


def reset_form():
    st.session_state.step = 1
    st.session_state.startup_data = {}
    st.rerun()


st.title("🚀 Startup Success Prediction Platform")
st.markdown(
    "### Predict your startup's success probability using AI-powered analysis across all industries and global regions"
)

progress_value = (st.session_state.step - 1) / 4
st.progress(progress_value)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"**{'✅' if st.session_state.step > 1 else '1️⃣'} Basic Info**")
with col2:
    st.markdown(f"**{'✅' if st.session_state.step > 2 else '2️⃣'} Location**")
with col3:
    st.markdown(
        f"**{'✅' if st.session_state.step > 3 else '3️⃣'} Industry Details**")
with col4:
    st.markdown(
        f"**{'✅' if st.session_state.step > 4 else '4️⃣'} Prediction**")

st.markdown("---")

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

    st.markdown("---")

    if st.button("Next: Location Details →", type="primary"):
        if startup_name.strip():
            st.session_state.startup_data.update({
                'startup_name':
                startup_name,
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
        else:
            st.error("Please enter a startup name")

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

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", type="secondary"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next: Industry Details →", type="primary"):
            if locality and locality.strip():
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
            else:
                st.error("Please enter your locality/area/neighborhood")

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

    st.markdown("---")

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

    with st.spinner('Analyzing your startup with AI models...'):
        prediction_result = st.session_state.predictor.predict(
            st.session_state.startup_data)

    success_prob = prediction_result['success_probability']
    confidence = prediction_result['confidence_interval']

    st.markdown(f"""
    <div class="success-box" style="text-align: center;">
        <h2 style="color: #28a745; margin: 0;">Success Probability</h2>
        <h1 style="color: #155724; margin: 10px 0; font-size: 4em;">{success_prob:.1f}%</h1>
        <p style="font-size: 1.2em; margin: 0;">Confidence Interval: ±{confidence:.1f}%</p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if success_prob >= 70:
            verdict = "High Success Potential"
            color = "#28a745"
            icon = "🟢"
        elif success_prob >= 50:
            verdict = "Moderate Success Potential"
            color = "#ffc107"
            icon = "🟡"
        else:
            verdict = "Needs Improvement"
            color = "#dc3545"
            icon = "🔴"

        st.markdown(f"""
        <div class="metric-card">
            <h3>{icon} Verdict</h3>
            <h4 style="color: {color};">{verdict}</h4>
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
            <h3>🎯 Model Accuracy</h3>
            <h4 style="color: #2E86AB;">{avg_accuracy*100:.1f}%</h4>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        risk_level = "Low" if success_prob >= 70 else "Medium" if success_prob >= 50 else "High"
        risk_color = "#28a745" if risk_level == "Low" else "#ffc107" if risk_level == "Medium" else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚠️ Risk Level</h3>
            <h4 style="color: {risk_color};">{risk_level}</h4>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📊 Model Analysis")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Model Predictions", "Success Factors", "Regional Insights",
        "Recommendations"
    ])

    with tab1:
        st.markdown("#### Individual Model Predictions")

        model_df = pd.DataFrame([{
            'Model':
            name,
            'Success Probability (%)':
            prob,
            'Model Accuracy (%)':
            prediction_result['model_accuracies'][name]['mean'] * 100
        } for name, prob in prediction_result['model_predictions'].items()])

        fig = go.Figure()

        fig.add_trace(
            go.Bar(x=model_df['Model'],
                   y=model_df['Success Probability (%)'],
                   name='Predicted Success %',
                   marker_color='#4CAF50',
                   text=model_df['Success Probability (%)'].round(1),
                   textposition='outside'))

        fig.add_trace(
            go.Scatter(x=model_df['Model'],
                       y=model_df['Model Accuracy (%)'],
                       name='Model Accuracy %',
                       mode='lines+markers',
                       marker=dict(size=10, color='#2E86AB'),
                       line=dict(width=3, color='#2E86AB'),
                       yaxis='y2'))

        fig.update_layout(title='AI Model Predictions Comparison',
                          xaxis_title='Machine Learning Model',
                          yaxis_title='Success Probability (%)',
                          yaxis2=dict(title='Model Accuracy (%)',
                                      overlaying='y',
                                      side='right'),
                          hovermode='x unified',
                          height=400)

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(model_df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### Key Success Factors")

        feature_importance = prediction_result['feature_importance']

        top_features = list(feature_importance.items())[:8]

        feature_names_map = {
            'funding_amount_normalized': 'Funding Amount',
            'team_size': 'Team Size',
            'founding_year_age': 'Company Age',
            'population_density': 'Population Density',
            'gdp_index': 'Regional GDP',
            'internet_penetration': 'Internet Access',
            'industry_score': 'Industry Strength',
            'location_score': 'Location Quality',
            'competition_factor': 'Competition Level',
            'business_model_score': 'Business Model'
        }

        feature_df = pd.DataFrame([{
            'Factor':
            feature_names_map.get(name, name),
            'Importance':
            details['importance'] * 100,
            'Your Score':
            details['normalized_value'] * 100
        } for name, details in top_features])

        fig = go.Figure()

        fig.add_trace(
            go.Bar(y=feature_df['Factor'],
                   x=feature_df['Importance'],
                   name='Factor Importance',
                   orientation='h',
                   marker_color='#2E86AB',
                   text=feature_df['Importance'].round(1),
                   textposition='outside'))

        fig.update_layout(title='What Drives Your Success Prediction',
                          xaxis_title='Importance Score',
                          yaxis_title='Success Factor',
                          height=400,
                          showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Your Startup's Factor Scores")

        for _, row in feature_df.iterrows():
            score = row['Your Score']
            if score >= 70:
                color = "green"
                emoji = "✅"
            elif score >= 40:
                color = "orange"
                emoji = "⚠️"
            else:
                color = "red"
                emoji = "❌"

            st.markdown(
                f"{emoji} **{row['Factor']}**: :{color}[{score:.1f}/100]")

    with tab3:
        st.markdown("#### Regional & Market Analysis")

        startup_data = st.session_state.startup_data

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📍 Your Location")
            st.markdown(f"""
            - **Country:** {startup_data['country']}
            - **State:** {startup_data['state']}
            - **City:** {startup_data['city']}
            - **Locality:** {startup_data['locality']}
            """)

            st.markdown("##### 💰 Financial Details")
            currency_info = startup_data['currency']
            st.markdown(f"""
            - **Funding:** {format_currency(startup_data['funding_amount'], currency_info)}
            - **Currency:** {currency_info['name']}
            """)

        with col2:
            st.markdown("##### 🏢 Business Details")
            st.markdown(f"""
            - **Industry:** {startup_data['industry']}
            - **Business Model:** {startup_data['business_model']}
            - **Team Size:** {startup_data['team_size']} members
            - **Founded:** {startup_data['founding_year']}
            """)

        st.markdown("---")

        regions_data = {
            'Region':
            [startup_data['city'], 'National Average', 'Top Tech Hubs'],
            'Startup Success Rate': [success_prob, 55, 75],
            'Type': ['Your Location', 'Benchmark', 'Benchmark']
        }

        fig = go.Figure()

        colors = ['#4CAF50', '#FFA726', '#2E86AB']

        for i, region in enumerate(regions_data['Region']):
            fig.add_trace(
                go.Bar(
                    x=[region],
                    y=[regions_data['Startup Success Rate'][i]],
                    name=region,
                    marker_color=colors[i],
                    text=[f"{regions_data['Startup Success Rate'][i]:.1f}%"],
                    textposition='outside'))

        fig.update_layout(title='Regional Success Comparison',
                          yaxis_title='Success Rate (%)',
                          showlegend=False,
                          height=350)

        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("#### 💡 Strategic Recommendations")

        if success_prob >= 70:
            st.success(
                "🎉 **Excellent Position!** Your startup shows strong potential for success."
            )
            st.markdown("""
            **Next Steps:**
            - Focus on execution and achieving key milestones
            - Build strategic partnerships in your industry
            - Scale your team strategically as you grow
            - Maintain strong customer feedback loops
            """)
        elif success_prob >= 50:
            st.warning(
                "⚡ **Good Foundation!** With some improvements, you can increase success probability."
            )
            st.markdown("""
            **Recommended Actions:**
            - Consider increasing funding to accelerate growth
            - Strengthen your unique value proposition
            - Expand your team with key expertise
            - Focus on customer acquisition and retention
            - Research your competition and differentiate clearly
            """)
        else:
            st.error(
                "🔧 **Needs Attention!** Several factors need improvement for better success chances."
            )
            st.markdown("""
            **Critical Improvements:**
            - Re-evaluate your business model and market fit
            - Seek mentorship from successful entrepreneurs
            - Consider pivoting to a stronger market position
            - Build a minimum viable product (MVP) quickly
            - Validate your idea with real customers
            - Look for co-founders with complementary skills
            """)

        st.markdown("---")
        st.markdown("#### 📈 Industry-Specific Insights")

        industry = startup_data['industry']

        if industry == "Food & Restaurants":
            st.info("""
            **Restaurant Success Tips:**
            - Location is critical - high foot traffic areas perform 3x better
            - Quality and consistency are more important than variety
            - Online presence and delivery integration are essential
            - Keep costs under control, especially in the first year
            """)
        elif industry == "Software & IT":
            st.info("""
            **Software Startup Tips:**
            - Launch MVP quickly and iterate based on feedback
            - Strong technical team is your biggest asset
            - Focus on solving a real, painful problem
            - Consider SaaS model for recurring revenue
            """)
        elif industry == "Education":
            st.info("""
            **Education Sector Tips:**
            - Accreditation and placement rates drive enrollment
            - Digital infrastructure is increasingly important
            - Partner with industry for practical training
            - Focus on student outcomes and success stories
            """)
        elif industry == "Healthcare":
            st.info("""
            **Healthcare Startup Tips:**
            - Regulatory compliance is non-negotiable
            - Quality of care builds reputation
            - Insurance partnerships increase accessibility
            - Technology can improve efficiency and reach
            """)
        else:
            st.info("""
            **General Startup Tips:**
            - Validate your business idea with real customers
            - Focus on solving a significant problem
            - Build a strong, diverse team
            - Manage cash flow carefully
            - Stay adaptable and ready to pivot
            """)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 View Summary Report",
                     type="secondary",
                     use_container_width=True):
            st.info("Summary report feature - showing key metrics overview")

    with col2:
        if st.button("🔄 Modify Inputs",
                     type="secondary",
                     use_container_width=True):
            st.session_state.step = 1
            st.rerun()

    with col3:
        if st.button("🆕 New Prediction",
                     type="primary",
                     use_container_width=True):
            reset_form()

st.sidebar.header("📋 About This Platform")
st.sidebar.markdown("""
This AI-powered platform predicts startup success probability using:

**🤖 Machine Learning Models:**
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)

**🌍 Global Coverage:**
- All countries worldwide
- Complete state/region data
- Major cities and localities
- Multi-currency support

**🏭 Industries Covered:**
- Food & Restaurants
- Software & IT
- Education
- Healthcare
- Manufacturing
- Fintech
- Agritech
- Retail & E-commerce

**📊 Analysis Factors:**
- Funding & financials
- Team composition
- Location metrics
- Industry dynamics
- Competition analysis
- Business model strength
- Regional indicators

---

**💡 How It Works:**

1. Enter your startup details
2. Provide location information
3. Add industry-specific data
4. Get AI-powered predictions
5. Review recommendations

---

*Predictions are based on statistical models and should be used as guidance, not guarantees.*
""")

if st.session_state.step < 4:
    st.sidebar.info(f"**Current Step:** {st.session_state.step}/4")

    if st.session_state.startup_data:
        st.sidebar.markdown("**Entered Data:**")
        if 'startup_name' in st.session_state.startup_data:
            st.sidebar.text(
                f"Startup: {st.session_state.startup_data['startup_name']}")
        if 'industry' in st.session_state.startup_data:
            st.sidebar.text(
                f"Industry: {st.session_state.startup_data['industry']}")
        if 'country' in st.session_state.startup_data:
            st.sidebar.text(
                f"Location: {st.session_state.startup_data.get('city', 'N/A')}, {st.session_state.startup_data['country']}"
            )
