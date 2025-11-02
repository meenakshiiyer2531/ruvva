
import pytest
import json
from app import create_app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    """Generate a token for a test user."""
    response = client.post('/api/v1/auth/dev-token', 
                           data=json.dumps({'student_id': 1}),
                           content_type='application/json')
    return json.loads(response.data)['data']['access_token']

def test_generate_learning_path(client, auth_token):
    """
    Test the generation of a personalized learning path for a target career.
    This helps users understand the steps to achieve their career goals.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    path_data = {
        "career_id": 1,
        "methods": ["online_courses", "books"],
        "time_commitment": "part-time"
    }
    response = client.post('/api/v1/learning/path/generate', 
                             data=json.dumps(path_data),
                             headers=headers,
                             content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'learning_path' in data
    assert 'modules' in data['learning_path']
    assert len(data['learning_path']['modules']) > 0

def test_get_learning_resources(client, auth_token):
    """
    Test retrieving learning resources for a specific career.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    # Test with a sample career ID
    career_id = 1
    response = client.get(f'/api/v1/learning/resources/{career_id}', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'learning_resources' in data
    assert 'courses' in data['learning_resources']
    assert 'books' in data['learning_resources']

def test_get_learning_recommendations(client, auth_token):
    """
    Test the endpoint for personalized learning recommendations.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/learning/recommendations', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'learning_recommendations' in data
    assert 'immediate_actions' in data['learning_recommendations']
    assert 'skill_gaps' in data['learning_recommendations']

