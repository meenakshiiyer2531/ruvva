
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

def test_get_mentor_recommendations(client, auth_token):
    """
    Test getting mentor recommendations for a student.
    This helps connect students with experienced professionals.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    # The profile_id (1) is part of the URL
    response = client.get('/mentor/recommendations/1', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'mentor_recommendations' in data
    assert len(data['mentor_recommendations']) > 0

def test_get_mentor_profile(client, auth_token):
    """
    Test retrieving the detailed profile of a specific mentor.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    # Test with a sample mentor ID
    mentor_id = 1
    response = client.get(f'/mentor/{mentor_id}', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'mentor_profile' in data
    assert 'profile_analysis' in data
    assert data['mentor_profile']['id'] == mentor_id

def test_book_mentor_session(client, auth_token):
    """
    Test the functionality to book a session with a mentor.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    booking_data = {
        "mentor_id": 1,
        "session_type": "career_advice"
    }
    response = client.post('/mentor/booking', 
                             data=json.dumps(booking_data),
                             headers=headers,
                             content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert 'session' in data
    assert data['session']['mentor_id'] == 1

def test_search_mentors(client, auth_token):
    """
    Test the mentor search functionality.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/mentor/search?industry=Technology', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'search_results' in data
    assert len(data['search_results']) > 0
    assert all('Technology' in mentor['industry'] for mentor in data['search_results'])

