import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    startup_name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    state = Column(String(100))
    city = Column(String(100))
    locality = Column(String(255))
    
    team_size = Column(Integer)
    founding_year = Column(Integer)
    business_model = Column(String(100))
    
    funding_amount = Column(Float)
    currency_code = Column(String(10))
    currency_symbol = Column(String(10))
    
    success_probability = Column(Float, nullable=False)
    confidence_interval = Column(Float)
    
    industry_metrics = Column(JSON)
    model_predictions = Column(JSON)
    model_accuracies = Column(JSON)
    feature_importance = Column(JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'startup_name': self.startup_name,
            'industry': self.industry,
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'locality': self.locality,
            'team_size': self.team_size,
            'founding_year': self.founding_year,
            'business_model': self.business_model,
            'funding_amount': self.funding_amount,
            'currency_code': self.currency_code,
            'currency_symbol': self.currency_symbol,
            'success_probability': self.success_probability,
            'confidence_interval': self.confidence_interval,
            'industry_metrics': self.industry_metrics,
            'model_predictions': self.model_predictions,
            'model_accuracies': self.model_accuracies,
            'feature_importance': self.feature_importance
        }

@st.cache_resource
def get_engine():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    engine = create_engine(database_url, pool_pre_ping=True)
    return engine

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def save_prediction(startup_data, prediction_result):
    session = get_session()
    try:
        prediction = Prediction(
            startup_name=startup_data.get('startup_name'),
            industry=startup_data.get('industry'),
            country=startup_data.get('country'),
            state=startup_data.get('state'),
            city=startup_data.get('city'),
            locality=startup_data.get('locality'),
            team_size=startup_data.get('team_size'),
            founding_year=startup_data.get('founding_year'),
            business_model=startup_data.get('business_model'),
            funding_amount=startup_data.get('funding_amount'),
            currency_code=startup_data.get('currency', {}).get('code'),
            currency_symbol=startup_data.get('currency', {}).get('symbol'),
            success_probability=prediction_result.get('success_probability'),
            confidence_interval=prediction_result.get('confidence_interval'),
            industry_metrics=startup_data.get('industry_metrics', {}),
            model_predictions=prediction_result.get('model_predictions', {}),
            model_accuracies=prediction_result.get('model_accuracies', {}),
            feature_importance=prediction_result.get('feature_importance', {})
        )
        
        session.add(prediction)
        session.commit()
        return prediction.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_predictions():
    session = get_session()
    try:
        predictions = session.query(Prediction).order_by(Prediction.created_at.desc()).all()
        return [p.to_dict() for p in predictions]
    finally:
        session.close()

def get_predictions_count():
    session = get_session()
    try:
        return session.query(Prediction).count()
    finally:
        session.close()

def get_predictions_by_date_range(start_date=None, end_date=None):
    session = get_session()
    try:
        query = session.query(Prediction)
        
        if start_date:
            query = query.filter(Prediction.created_at >= start_date)
        if end_date:
            query = query.filter(Prediction.created_at <= end_date)
        
        predictions = query.order_by(Prediction.created_at.desc()).all()
        return [p.to_dict() for p in predictions]
    finally:
        session.close()

def get_predictions_by_filters(industry=None, country=None, business_model=None):
    session = get_session()
    try:
        query = session.query(Prediction)
        
        if industry:
            query = query.filter(Prediction.industry == industry)
        if country:
            query = query.filter(Prediction.country == country)
        if business_model:
            query = query.filter(Prediction.business_model == business_model)
        
        predictions = query.order_by(Prediction.created_at.desc()).all()
        return [p.to_dict() for p in predictions]
    finally:
        session.close()
