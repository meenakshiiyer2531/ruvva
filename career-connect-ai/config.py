"""
Configuration management for CareerConnect AI Flask application.
Handles environment-based configuration for development and production.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with common settings."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')
    
    # JWT / Auth Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 60 * 60))  # seconds
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS',
        'http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080').split(',')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    CORS_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept', 'Origin', 'Cache-Control']
    
    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/careerconnect.log')
    
    # Database Configuration (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///careerconnect.db')
    
    # External APIs Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    LINKEDIN_API_KEY = os.environ.get('LINKEDIN_API_KEY')
    
    # Email Configuration (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # CareerConnect Specific Configuration
    MAX_PROFILE_SIZE = int(os.environ.get('MAX_PROFILE_SIZE', 10000))  # bytes
    MAX_ASSESSMENT_QUESTIONS = int(os.environ.get('MAX_ASSESSMENT_QUESTIONS', 100))
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))  # seconds

    # Backend Integration Configuration
    BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:8080/api')
    BACKEND_INTEGRATION_ENABLED = os.environ.get('BACKEND_INTEGRATION_ENABLED', 'True').lower() == 'true'

    # Firebase Integration (for direct access if needed)
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', 'ruvaa-cbcaa')
    FIREBASE_DATABASE_URL = os.environ.get('FIREBASE_DATABASE_URL', 'https://ruvaa-cbcaa-default-rtdb.asia-southeast1.firebasedatabase.app/')
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '../backend/backend/credentials/serviceAccountKey.json')
    
    # Indian Education System Configuration
    INDIAN_GRADES = ['10th', '11th', '12th', 'Graduate', 'Post Graduate']
    INDIAN_STATES = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Puducherry'
    ]
    
    # Career Categories for Indian Students
    CAREER_CATEGORIES = [
        'Engineering', 'Medicine', 'Commerce', 'Arts', 'Science',
        'Law', 'Education', 'Agriculture', 'Technology', 'Management',
        'Design', 'Media', 'Sports', 'Defense', 'Civil Services'
    ]

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'
    
    # More lenient rate limiting for development
    RATELIMIT_DEFAULT = "1000 per hour"
    
    # Development logging
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    
    # Stricter rate limiting for production
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Ensure secret key is set in production
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'testing'
    
    # Use in-memory database for testing
    DATABASE_URL = 'sqlite:///:memory:'
    
    # Disable rate limiting for testing
    RATELIMIT_ENABLED = False
    
    # Testing logging
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])