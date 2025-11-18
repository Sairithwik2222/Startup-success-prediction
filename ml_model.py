import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class StartupSuccessPredictor:
    def __init__(self):
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'SVM': SVC(random_state=42, probability=True, kernel='rbf')
        }
        self.scaler = StandardScaler()
        self.feature_names = []
        self.model_accuracies = {}
        
    def generate_synthetic_training_data(self, n_samples=1000):
        """Generate synthetic training data based on realistic patterns"""
        np.random.seed(42)
        
        data = {
            'funding_amount_normalized': np.random.exponential(scale=0.3, size=n_samples),
            'team_size': np.random.randint(1, 50, size=n_samples),
            'founding_year_age': np.random.randint(0, 10, size=n_samples),
            'population_density': np.random.uniform(0, 1, size=n_samples),
            'gdp_index': np.random.uniform(0, 1, size=n_samples),
            'internet_penetration': np.random.uniform(0, 1, size=n_samples),
            'industry_score': np.random.uniform(0, 1, size=n_samples),
            'location_score': np.random.uniform(0, 1, size=n_samples),
            'competition_factor': np.random.uniform(0, 1, size=n_samples),
            'business_model_score': np.random.uniform(0, 1, size=n_samples),
        }
        
        df = pd.DataFrame(data)
        
        success_probability = (
            0.15 * df['funding_amount_normalized'] +
            0.10 * (df['team_size'] / 50) +
            0.05 * (1 - df['founding_year_age'] / 10) +
            0.10 * df['population_density'] +
            0.15 * df['gdp_index'] +
            0.10 * df['internet_penetration'] +
            0.15 * df['industry_score'] +
            0.10 * df['location_score'] +
            0.05 * (1 - df['competition_factor']) +
            0.05 * df['business_model_score']
        )
        
        noise = np.random.normal(0, 0.15, size=n_samples)
        success_probability = np.clip(success_probability + noise, 0, 1)
        
        df['success'] = (success_probability > 0.55).astype(int)
        
        return df
    
    def train_models(self):
        """Train all models on synthetic data"""
        df = self.generate_synthetic_training_data(1000)
        
        X = df.drop('success', axis=1)
        y = df['success']
        
        self.feature_names = X.columns.tolist()
        
        X_scaled = self.scaler.fit_transform(X)
        
        for name, model in self.models.items():
            model.fit(X_scaled, y)
            
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
            self.model_accuracies[name] = {
                'mean': cv_scores.mean(),
                'std': cv_scores.std()
            }
    
    def prepare_features(self, startup_data):
        """Prepare features from startup data for prediction"""
        
        funding_normalized = min(startup_data.get('funding_amount', 0) / 10000000, 1.0)
        
        team_size = startup_data.get('team_size', 5)
        
        founding_year = startup_data.get('founding_year', 2024)
        founding_year_age = 2024 - founding_year
        
        population_density = self._calculate_population_density(
            startup_data.get('country'),
            startup_data.get('state'),
            startup_data.get('city')
        )
        
        gdp_index = self._calculate_gdp_index(startup_data.get('country'))
        
        internet_penetration = self._calculate_internet_penetration(startup_data.get('country'))
        
        industry_score = self._calculate_industry_score(
            startup_data.get('industry'),
            startup_data.get('industry_metrics', {})
        )
        
        location_score = self._calculate_location_score(
            startup_data.get('country'),
            startup_data.get('state'),
            startup_data.get('city')
        )
        
        competition_factor = self._calculate_competition_factor(
            startup_data.get('industry'),
            startup_data.get('industry_metrics', {})
        )
        
        business_model_score = self._calculate_business_model_score(
            startup_data.get('business_model')
        )
        
        features = {
            'funding_amount_normalized': funding_normalized,
            'team_size': team_size,
            'founding_year_age': founding_year_age,
            'population_density': population_density,
            'gdp_index': gdp_index,
            'internet_penetration': internet_penetration,
            'industry_score': industry_score,
            'location_score': location_score,
            'competition_factor': competition_factor,
            'business_model_score': business_model_score,
        }
        
        return features
    
    def predict(self, startup_data):
        """Make predictions using ensemble of models"""
        features = self.prepare_features(startup_data)
        feature_values = [features[name] for name in self.feature_names]
        feature_array = np.array(feature_values).reshape(1, -1)
        
        feature_array_scaled = self.scaler.transform(feature_array)
        
        predictions = {}
        probabilities = {}
        
        for name, model in self.models.items():
            pred = model.predict(feature_array_scaled)[0]
            prob = model.predict_proba(feature_array_scaled)[0]
            
            predictions[name] = pred
            probabilities[name] = prob[1] * 100
        
        ensemble_probability = np.mean(list(probabilities.values()))
        
        confidence_interval = np.std(list(probabilities.values()))
        
        feature_importance = self._calculate_feature_importance(features)
        
        return {
            'success_probability': ensemble_probability,
            'confidence_interval': confidence_interval,
            'model_predictions': probabilities,
            'feature_importance': feature_importance,
            'model_accuracies': self.model_accuracies
        }
    
    def _calculate_population_density(self, country, state, city):
        """Calculate population density score"""
        high_density_countries = ['India', 'China', 'Japan', 'Singapore', 'Bangladesh']
        high_density_cities = ['Mumbai', 'Delhi', 'New York City', 'Tokyo', 'London', 'Singapore']
        
        score = 0.5
        
        if country in high_density_countries:
            score += 0.2
        
        if city in high_density_cities:
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_gdp_index(self, country):
        """Calculate GDP index score"""
        high_gdp_countries = {
            'United States': 0.95,
            'China': 0.90,
            'Japan': 0.88,
            'Germany': 0.87,
            'United Kingdom': 0.85,
            'India': 0.75,
            'France': 0.84,
            'Canada': 0.83,
            'Australia': 0.82,
            'Singapore': 0.90,
            'Switzerland': 0.92,
            'Netherlands': 0.83,
            'Sweden': 0.82,
            'United Arab Emirates': 0.80
        }
        
        return high_gdp_countries.get(country, 0.60)
    
    def _calculate_internet_penetration(self, country):
        """Calculate internet penetration score"""
        high_internet_countries = {
            'United States': 0.92,
            'United Kingdom': 0.95,
            'South Korea': 0.96,
            'Japan': 0.93,
            'Germany': 0.91,
            'Singapore': 0.92,
            'Australia': 0.90,
            'Canada': 0.91,
            'Sweden': 0.94,
            'Netherlands': 0.93,
            'India': 0.55,
            'China': 0.70,
            'Brazil': 0.71
        }
        
        return high_internet_countries.get(country, 0.65)
    
    def _calculate_industry_score(self, industry, metrics):
        """Calculate industry-specific score"""
        base_scores = {
            'Software & IT': 0.80,
            'Fintech': 0.75,
            'Food & Restaurants': 0.60,
            'Healthcare': 0.70,
            'Education': 0.65,
            'Manufacturing': 0.65,
            'Agritech': 0.60,
            'Retail & E-commerce': 0.70
        }
        
        base_score = base_scores.get(industry, 0.60)
        
        if industry == 'Food & Restaurants':
            if metrics.get('food_quality_rating', 7) >= 8:
                base_score += 0.10
            if metrics.get('location_foot_traffic') in ['High', 'Very High']:
                base_score += 0.05
        
        elif industry == 'Software & IT':
            if metrics.get('has_mvp') in ['Completed', 'Beta testing', 'Launched']:
                base_score += 0.10
            if metrics.get('unique_value_proposition') == 'Strong':
                base_score += 0.05
        
        return min(base_score, 1.0)
    
    def _calculate_location_score(self, country, state, city):
        """Calculate location-based score"""
        tech_hubs = ['San Francisco', 'New York City', 'London', 'Bangalore', 'Singapore', 
                     'Berlin', 'Tel Aviv', 'Austin', 'Seattle', 'Boston', 'Toronto', 
                     'Hyderabad', 'Pune', 'Mumbai', 'Delhi', 'Sydney', 'Tokyo']
        
        startup_friendly_countries = {
            'United States': 0.90,
            'United Kingdom': 0.85,
            'Singapore': 0.88,
            'India': 0.75,
            'Canada': 0.80,
            'Germany': 0.82,
            'Israel': 0.87,
            'Australia': 0.78
        }
        
        score = startup_friendly_countries.get(country, 0.60)
        
        if city in tech_hubs:
            score += 0.10
        
        return min(score, 1.0)
    
    def _calculate_competition_factor(self, industry, metrics):
        """Calculate competition factor (lower competition = better)"""
        if industry == 'Food & Restaurants':
            nearby = metrics.get('nearby_restaurants', 5)
            if nearby < 3:
                return 0.2
            elif nearby < 10:
                return 0.5
            else:
                return 0.8
        
        elif industry == 'Software & IT':
            competitors = metrics.get('competitors_count', 5)
            if competitors < 3:
                return 0.2
            elif competitors < 10:
                return 0.5
            else:
                return 0.7
        
        return 0.5
    
    def _calculate_business_model_score(self, business_model):
        """Calculate business model score"""
        model_scores = {
            'SaaS (Software as a Service)': 0.85,
            'Marketplace': 0.80,
            'B2B (Business-to-Business)': 0.75,
            'Freemium': 0.70,
            'Subscription': 0.75,
            'E-commerce': 0.70,
            'B2C (Business-to-Consumer)': 0.65,
            'Franchise': 0.60,
            'Hybrid': 0.75
        }
        
        return model_scores.get(business_model, 0.65)
    
    def _calculate_feature_importance(self, features):
        """Calculate feature importance for explanation"""
        importance = {}
        
        for feature_name, value in features.items():
            if 'Random Forest' in self.models:
                rf_model = self.models['Random Forest']
                feature_idx = self.feature_names.index(feature_name)
                importance[feature_name] = {
                    'value': value,
                    'importance': rf_model.feature_importances_[feature_idx],
                    'normalized_value': value
                }
        
        sorted_importance = dict(sorted(importance.items(), 
                                       key=lambda x: x[1]['importance'], 
                                       reverse=True))
        
        return sorted_importance
