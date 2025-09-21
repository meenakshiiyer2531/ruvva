"""
Basic tests for CareerConnect AI Flask application.
"""

import pytest
import json
from app import create_app

@pytest.fixture
def app():
    """Create test Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['FLASK_ENV'] = 'testing'
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_index_endpoint(client):
    """Test the index endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'CareerConnect AI' in data['message']

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code in [200, 503]  # 503 if Redis is not available
    
    data = json.loads(response.data)
    assert 'status' in data
    assert 'timestamp' in data

def test_status_endpoint(client):
    """Test the status endpoint."""
    response = client.get('/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'application' in data
    assert 'version' in data
    assert 'environment' in data

def test_api_docs_endpoint(client):
    """Test the API documentation endpoint."""
    response = client.get('/api/docs')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'title' in data
    assert 'endpoints' in data

def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.get('/')
    assert 'Access-Control-Allow-Origin' in response.headers

if __name__ == '__main__':
    pytest.main([__file__])
