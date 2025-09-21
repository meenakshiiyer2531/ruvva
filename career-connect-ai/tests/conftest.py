"""
Test configuration and fixtures
"""

import pytest
import os
import tempfile
from app import create_app
from config import TestingConfig

@pytest.fixture
def app():
    """Create test application"""
    app = create_app()
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers():
    """Mock authentication headers"""
    return {
        'Authorization': 'Bearer mock-jwt-token'
    }

@pytest.fixture
def sample_student_profile():
    """Sample student profile for testing"""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 25,
        'education_level': 'bachelor',
        'skills': ['Python', 'JavaScript', 'Communication'],
        'interests': ['Technology', 'Data Science'],
        'career_goals': ['Software Engineer', 'Data Scientist'],
        'riasec_scores': {
            'realistic': 60,
            'investigative': 80,
            'artistic': 40,
            'social': 50,
            'enterprising': 70,
            'conventional': 30
        }
    }

@pytest.fixture
def sample_career_data():
    """Sample career data for testing"""
    return {
        'id': 1,
        'title': 'Software Engineer',
        'description': 'Develop software applications and systems',
        'category': 'Technology',
        'industry': 'Software',
        'required_skills': ['Programming', 'Problem Solving', 'Communication'],
        'riasec_requirements': {
            'realistic': 40,
            'investigative': 80,
            'artistic': 30,
            'social': 40,
            'enterprising': 60,
            'conventional': 50
        },
        'salary': {'median': 90000, 'min': 60000, 'max': 120000},
        'growth_rate': 'high'
    }

@pytest.fixture
def sample_assessment_responses():
    """Sample assessment responses for testing"""
    return {
        'q1': 4,
        'q2': 5,
        'q3': 2,
        'q4': 3,
        'q5': 4,
        'q6': 3,
        'q7': 4,
        'q8': 5,
        'q9': 2,
        'q10': 3
    }
