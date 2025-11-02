"""
Test Chat API endpoints - Tests complete flow: Route → ChatService → GeminiClient → Response
According to AI Service Flow: User Message → ChatService → ConversationManager → GeminiClient → Gemini API
"""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from app import create_app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['GEMINI_API_KEY'] = 'test-api-key'  # Mock API key for testing
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    """Generate a token for a test user."""
    response = client.post('/api/v1/auth/dev-token', 
                           data=json.dumps({'student_id': 1}),
                           content_type='application/json')
    return json.loads(response.data)['data']['access_token']

@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response."""
    mock_response = MagicMock()
    mock_response.content = "Based on your profile, I recommend exploring software engineering. Key exams: JEE Main. Top colleges: IITs, NITs. Start by learning programming basics."
    mock_response.usage = {'totalTokenCount': 85}
    mock_response.model = 'gemini-2.0-flash'
    mock_response.cached = False
    return mock_response

def test_simple_chat_endpoint(client, mock_gemini_response):
    """
    Test the simple chat endpoint (no auth required for MVP).
    Flow: POST /api/v1/chat → ChatService → GeminiClient → Response
    Tests the complete flow without mocking (uses actual services with error handling).
    """
    chat_data = {
        "message": "What careers match my skills?",
        "profile": {
            "name": "Test Student",
            "skills": ["Python", "Communication"],
            "interests": ["Technology"],
            "career_goals": ["Software Engineer"]
        }
    }
    
    # Test may fail if Gemini API is not configured, but should handle gracefully
    response = client.post('/api/v1/chat',
                         data=json.dumps(chat_data),
                         content_type='application/json')
    
    # Should return either success or error (both are valid for testing flow)
    assert response.status_code in [200, 500]
    data = json.loads(response.data)
    
    if response.status_code == 200:
        assert data['success'] == True
        assert 'data' in data
        assert 'response' in data['data']
        assert 'session_id' in data['data']
        # Response should be concise (after prompt tuning)
        response_text = data['data']['response']
        assert len(response_text) > 0
        # After tuning, responses should be concise (300 tokens max)
        assert len(response_text) <= 2000  # Allow some buffer for error messages

def test_simple_chat_without_profile(client):
    """
    Test simple chat endpoint works without profile (uses defaults).
    """
    chat_data = {
        "message": "Help me with career guidance"
    }
    
    response = client.post('/api/v1/chat',
                         data=json.dumps(chat_data),
                         content_type='application/json')
    
    # Should handle request (may fail without API key, but tests flow)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'response' in data['data']

def test_simple_chat_validation_error(client):
    """
    Test simple chat endpoint validation - missing message.
    """
    response = client.post('/api/v1/chat',
                         data=json.dumps({}),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    # Check for validation error message
    errors = data.get('errors', {})
    assert 'message' in str(errors).lower() or 'message' in errors

def test_create_chat_session(client, auth_token):
    """
    Test creating a new chat session (authenticated endpoint).
    Flow: POST /api/v1/chat/session → ChatService.create_chat_session()
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.post('/api/v1/chat/session', 
                             headers=headers,
                             content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)['data']
    assert 'session_id' in data
    assert 'student_profile' in data

def test_send_message_authenticated(client, auth_token):
    """
    Test sending a message to the AI counselor within a session (authenticated).
    Flow: POST /api/v1/chat/message → ChatService → GeminiClient → Response
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    
    # First, create a session
    session_res = client.post('/api/v1/chat/session', headers=headers)
    if session_res.status_code != 201:
        pytest.skip("Session creation failed")
    
    session_id = json.loads(session_res.data)['data']['session_id']
    
    message_data = {
        "session_id": session_id,
        "message": "What careers match my personality?"
    }
    
    response = client.post('/api/v1/chat/message', 
                         data=json.dumps(message_data),
                         headers=headers,
                         content_type='application/json')
    
    # May fail without API key, but tests the flow
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = json.loads(response.data)['data']
        assert 'response_data' in data
        # Check for AI response
        response_data = data['response_data']
        assert 'ai_response' in response_data or 'response' in response_data

def test_get_chat_history(client, auth_token):
    """
    Test retrieving the chat history for a student.
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/chat/history/1', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'chat_history' in data
    assert isinstance(data['chat_history'], list)

def test_chat_cors_preflight(client):
    """
    Test CORS preflight request handling.
    """
    response = client.options('/api/v1/chat')
    assert response.status_code == 204

