# Startup Success Predictor

## Overview

A machine learning-powered web application that predicts startup success probability based on multiple factors including location, industry, funding, team size, and business model. The application uses ensemble machine learning models to generate predictions and stores results in a relational database. Users can input startup details through an interactive form and view historical predictions through an analytics dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Web Framework**: Streamlit-based single-page application
- Main prediction form with multi-step data collection workflow
- Dashboard view for analytics and historical prediction visualization
- Sidebar navigation for switching between prediction and dashboard views

**UI Components**:
- Custom CSS with gradient backgrounds and glassmorphism effects
- Interactive Plotly visualizations (charts, gauges, graphs)
- Wide layout mode for maximum screen utilization
- Real-time form validation with user-friendly error messages

**Rationale**: Streamlit selected for rapid prototyping of data-centric applications with pure Python. Eliminates need for separate frontend framework while providing built-in state management, component rendering, and automatic UI updates.

### Backend Architecture

**Application Structure**: Modular Python architecture
- `app.py`: Main application entry point and UI orchestration
- `ml_model.py`: Machine learning prediction engine
- `database.py`: Data persistence layer
- `dashboard.py`: Analytics and visualization logic
- `utils.py`: Shared validation and utility functions
- `location_data.py`: Geographic data provider
- `currency_data.py`: Currency mapping and formatting
- `industry_metrics.py`: Industry-specific configuration

**Machine Learning System**: Ensemble prediction approach
- Four scikit-learn classifiers: Logistic Regression, Decision Tree, Random Forest, SVM
- Synthetic training data generation (1000+ samples) with realistic correlation patterns
- Weighted averaging of model predictions for final success probability
- Feature engineering pipeline with StandardScaler normalization
- Cross-validation for model accuracy assessment
- Feature importance extraction for prediction explainability

**Features Engineered**:
- Normalized funding amounts (0-1 scale)
- Geographic indicators (population density, GDP index, internet penetration)
- Business metrics (team size ratio, company age, industry scores, business model ratings)
- Competition factors (market saturation, competitive indices)

**Rationale**: Ensemble approach mitigates individual model weaknesses and provides confidence intervals. Synthetic data generation necessary due to lack of publicly available startup outcome datasets. Modular architecture enables independent development and testing of components.

### Data Architecture

**Database**: SQLAlchemy ORM with relational database
- Single `Prediction` table storing all prediction records
- Columns for startup metadata (name, industry, location hierarchy)
- Columns for prediction results (success probability, confidence interval)
- JSON columns for complex data (industry metrics, model predictions, feature importance)
- Automatic timestamp tracking via `created_at` field

**Data Model Design**:
- Primary key: Auto-incrementing integer ID
- Location hierarchy: country → state → city → locality
- Financial data: funding amount, currency code, currency symbol
- Metadata: team size, founding year, business model
- Results: success probability, confidence interval, model accuracies

**Rationale**: SQLAlchemy provides database abstraction allowing easy migration between SQLite (development) and PostgreSQL (production). JSON columns offer flexibility for storing variable industry-specific metrics without schema changes.

### Location Data System

**Hierarchical Geographic Data**: Country → State → City → Locality
- Comprehensive country list via `pycountry` library
- Hardcoded state/city mappings for major countries (India, US, etc.)
- Dynamic locality input (user-provided)

**Rationale**: Hierarchical location system enables granular geographic analysis while pycountry integration ensures standardized country names. Hardcoded mappings for major markets provide better UX than API calls.

### Currency System

**Multi-Currency Support**: 
- Currency mapping for 40+ countries
- Includes currency code, symbol, and display name
- Dynamic currency selection based on country choice

**Rationale**: Supporting multiple currencies enables global usability. Country-based automatic selection reduces user input burden.

### Industry Configuration System

**Industry-Specific Fields**: Dynamic form fields based on selected industry
- Configurable field types (number, select, text)
- Industry-specific metrics (e.g., cuisine type for restaurants, tech stack for SaaS)
- Business model explanations with examples

**Rationale**: Different industries have unique success factors. Dynamic field generation allows capturing relevant metrics without cluttering the base form.

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for rapid UI development
- **scikit-learn**: Machine learning models (RandomForest, LogisticRegression, DecisionTree, SVM) and preprocessing
- **Plotly**: Interactive data visualization (graphs, charts, gauges)
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing and array operations

### Database & ORM
- **SQLAlchemy**: SQL toolkit and ORM for database abstraction
- Database backend: SQLite (default) or PostgreSQL (production-ready)

### Data Providers
- **pycountry**: ISO country database for standardized country information

### Utilities
- **datetime**: Timestamp handling and date operations
- **json**: JSON serialization for complex data structures
- **warnings**: Suppression of ML library warnings

### Visualization & UI
- **Plotly Express**: High-level plotting interface
- **Plotly Graph Objects**: Low-level chart customization
- Custom CSS via Google Fonts (Inter font family)

### Machine Learning Pipeline
- **StandardScaler**: Feature normalization preprocessing
- **cross_val_score**: Model validation and accuracy assessment
- Synthetic data generation using numpy random distributions

**Note**: Application currently supports SQLite by default but is designed to work with PostgreSQL through SQLAlchemy abstraction layer. PostgreSQL may be added for production deployments requiring concurrent access and better performance.