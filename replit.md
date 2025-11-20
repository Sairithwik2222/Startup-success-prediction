# Startup Success Prediction Platform

## Overview
A comprehensive AI-powered web application built with Python and Streamlit that predicts the success probability of startup companies across all industries and global regions.

**Status**: Production-ready MVP
**Last Updated**: November 9, 2025
**Tech Stack**: Python, Streamlit, Scikit-learn, Plotly, Pandas

## Features

### Core Capabilities
- **Global Coverage**: Support for 200+ countries with detailed state/city data for major regions
- **Multi-Currency Support**: Automatic currency switching based on selected country (50+ currencies)
- **8 Industries**: Food & Restaurants, Software & IT, Education, Healthcare, Manufacturing, Fintech, Agritech, Retail & E-commerce
- **AI Prediction**: Ensemble machine learning using 4 models (Logistic Regression, Decision Tree, Random Forest, SVM)
- **Interactive Visualizations**: Charts, graphs, and dashboards using Plotly

### User Flow
1. **Step 1 - Basic Info**: Enter startup name, select industry, team size, founding year, business model
2. **Step 2 - Location & Funding**: Select country → state → city → locality, enter funding amount in local currency
3. **Step 3 - Industry Details**: Provide industry-specific metrics (varies by selected industry)
4. **Step 4 - Prediction Results**: View success probability, model analysis, success factors, regional insights, recommendations

## Project Architecture

### File Structure
```
├── app.py                  # Main Streamlit application with multi-step form
├── location_data.py        # Country/state/city/locality data with global coverage
├── currency_data.py        # Currency mapping for 50+ countries
├── industry_metrics.py     # Industry-specific fields and business models
├── ml_model.py            # Machine learning prediction engine
└── replit.md              # Project documentation
```

### Key Components

#### 1. Location Data (`location_data.py`)
- **Predefined Countries**: Full state/city data for India (36 states/UTs), USA (50 states), UK, Canada, Australia, China, and 40+ other major countries
- **Fallback System**: Generic regional data (North, South, East, West, Central) for countries without predefined data
- **Locality Generation**: Dynamic locality/area names for all cities

#### 2. Currency Data (`currency_data.py`)
- Automatic currency selection based on country
- Includes currency code, symbol, and full name
- Covers INR, USD, EUR, GBP, JPY, CNY, and 45+ others

#### 3. Industry Metrics (`industry_metrics.py`)
- **Business Models**: B2B, B2C, SaaS, Marketplace, Freemium, E-commerce, Franchise, Subscription, Hybrid
- **Industry-Specific Fields**:
  - Restaurants: nearby competition, cuisine type, cost, seating, quality rating, foot traffic, parking, delivery
  - Software: tech stack, team experience, market size, MVP status, users, revenue model, competitors
  - Education: type, capacity, accreditation, faculty experience, placement rate, fees, competition
  - Healthcare: type, beds, doctors, specializations, insurance, emergency services, equipment
  - Manufacturing: type, production capacity, automation, certifications, raw materials, labor
  - Fintech: type, compliance, security, user base, transactions, partnerships, fraud prevention
  - Agritech: type, farmer network, adoption, crops, coverage, government support, supply chain
  - Retail: type, category, inventory, order value, logistics, returns, customer acquisition

#### 4. ML Model (`ml_model.py`)
- **Training**: Uses synthetic data based on realistic startup success patterns
- **Features**: Funding, team size, age, population density, GDP, internet penetration, industry strength, location quality, competition, business model
- **Models**: 4 algorithms with cross-validation
- **Output**: Success probability (%), confidence interval, model accuracy, feature importance

#### 5. Main App (`app.py`)
- **Multi-step Form**: Progressive data collection with session state management
- **Dynamic Fields**: Industry-specific inputs that change based on selections
- **Visualizations**: Interactive Plotly charts for predictions, factors, regional analysis
- **Recommendations**: Industry-specific tips and strategic guidance

## Recent Changes

### Bug Fixes (November 9, 2025)
- **Critical Fix**: Location selector now handles all countries gracefully
  - Added defensive checks for empty state/city/locality lists
  - Improved index handling when country selection changes
  - Enhanced fallback data with 5 regions per country instead of 1
  - Prevents Streamlit selectbox crashes for countries without predefined data

## Machine Learning Details

### Prediction Factors
1. **Funding Amount** (15%): Normalized investment level
2. **GDP Index** (15%): Regional economic strength
3. **Industry Score** (15%): Industry-specific metrics and market conditions
4. **Population Density** (10%): Market accessibility
5. **Internet Penetration** (10%): Digital infrastructure
6. **Location Score** (10%): Startup ecosystem quality
7. **Team Size** (10%): Organizational capacity
8. **Business Model** (5%): Revenue model strength
9. **Competition Factor** (5%): Market saturation (inverse)
10. **Company Age** (5%): Maturity level

### Model Accuracy
- Average ensemble accuracy: ~82-85% on synthetic validation data
- Individual model accuracies displayed on results dashboard
- Confidence intervals shown to indicate prediction uncertainty

## How to Use

### Running the Application
```bash
streamlit run app.py --server.port 5000
```
The app is configured to run on port 5000 with webview output.

### For Users
1. Access the web application through the Replit webview
2. Fill out the 3-step form with your startup details
3. Review the AI-generated prediction and recommendations
4. Modify inputs and re-run predictions as needed

## Technical Notes

### Dependencies
- streamlit: Web framework
- scikit-learn: Machine learning models
- plotly: Interactive visualizations
- pandas, numpy: Data manipulation
- pycountry: Country data

### Session State
- All form data stored in `st.session_state.startup_data`
- Current step tracked in `st.session_state.step`
- ML predictor cached in `st.session_state.predictor`

### Performance
- ML models trained once on app load (~1000 samples)
- Predictions execute in <1 second
- Responsive multi-column layouts for better UX

## Future Enhancements (Next Phase)

1. **Real Data Integration**: Connect to actual startup databases for training
2. **Time Series**: Add forecasting for optimal launch timing
3. **User Accounts**: Save predictions and track multiple startups
4. **Comparative Analysis**: Benchmark against similar successful/failed startups
5. **Live Data**: Integrate real-time regional metrics (GDP, population, internet stats)
6. **Extended Coverage**: Add more granular city/locality data for all countries
7. **API Access**: Provide programmatic access to predictions

## Known Limitations

- Predictions based on synthetic training data (not real historical startup outcomes)
- Some countries use generic fallback regional data instead of actual states
- Model weights are estimates based on startup success literature
- No user authentication or data persistence
- Single-user session (no multi-user support)

## Support

For issues or questions:
- Check logs in `/tmp/logs/streamlit_app_*.log`
- Review browser console for frontend errors
- Verify workflow is running on port 5000

---

*This project demonstrates a comprehensive data science application combining location intelligence, multi-currency support, industry-specific analysis, and machine learning predictions in an intuitive web interface.*
