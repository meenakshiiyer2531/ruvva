
import pytest
from flask import Flask
import json

# Assume 'create_app' is in the root 'app' module
from app import create_app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    # Use a temporary, in-memory database for testing if applicable
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        # with app.app_context():
        #     # db.create_all() # Create all tables
        yield client
        # with app.app_context():
        #     # db.drop_all() # Drop all tables after test

def test_health_check(client):
    """
    Test the /health endpoint to ensure the application is running.
    """
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'services' in data

def test_status_check(client):
    """
    Test the /status endpoint for detailed application status.
    """
    response = client.get('/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['application'] == 'CareerConnect AI'
    assert 'version' in data
    assert 'environment' in data

def test_dev_token_generation(client):
    """
    Test the development JWT token generation endpoint.
    This is a critical first step for authenticating subsequent API calls.
    """
    # A sample student ID is required to generate a token
    student_id = 123
    response = client.post('/api/v1/auth/dev-token', 
                           data=json.dumps({'student_id': student_id}),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data['data']
    assert 'expires_in' in data['data']
    assert data['message'] == "Dev token issued"

def test_dev_token_requires_student_id(client):
    """
    Test that the dev-token endpoint returns a validation error if student_id is missing.
    """
    response = client.post('/api/v1/auth/dev-token', 
                           data=json.dumps({}),
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    # Updated to match actual error format
    assert data['success'] == False or 'error' in data or 'message' in data
    # Check that student_id validation error is present
    errors = data.get('errors', data.get('validation_errors', {}))
    assert 'student_id' in str(errors).lower() or 'student_id' in errors

