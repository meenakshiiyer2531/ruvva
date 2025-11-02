
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
    """Generate a token and return the token string."""
    response = client.post('/api/v1/auth/dev-token', 
                           data=json.dumps({'student_id': 1}),
                           content_type='application/json')
    return json.loads(response.data)['data']['access_token']

def test_create_profile(client, auth_token):
    """
    Test creating a new student profile.
    This is the first step for a new user.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    profile_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 21,
        "education_level": "bachelor",
        "skills": ["Python", "Data Analysis"],
        "interests": ["AI", "Machine Learning"],
        "career_goals": ["Data Scientist"]
    }
    response = client.post('/api/v1/profile/create', 
                           data=json.dumps(profile_data),
                           headers=headers,
                           content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)['data']
    assert data['profile']['name'] == "Test User"
    assert 'analysis' in data

def test_get_profile(client, auth_token):
    """
    Test retrieving an existing student profile.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    # The student_id (1) is embedded in the auth_token
    response = client.get('/api/v1/profile/1', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert data['id'] == 1
    assert data['name'] == 'John Doe' # Mocked data from the route

def test_update_profile(client, auth_token):
    """
    Test updating a student's profile.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    update_data = {
        "skills": ["Python", "Data Analysis", "Machine Learning"],
        "career_goals": ["Senior Data Scientist"]
    }
    response = client.put('/api/v1/profile/update', 
                          data=json.dumps(update_data),
                          headers=headers,
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert "Machine Learning" in data['profile']['skills']
    assert data['updated_fields'] == ["skills", "career_goals"]

def test_analyze_profile(client, auth_token):
    """
    Test the profile analysis endpoint.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.post('/api/v1/profile/analyze', 
                           headers=headers,
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'analysis' in data
    assert 'profile_summary' in data
    assert data['analysis_type'] == 'comprehensive'

