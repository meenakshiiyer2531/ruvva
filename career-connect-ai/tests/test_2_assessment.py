"""
Test Assessment API endpoints - Tests complete flow: Route → RIASECAnalyzer → Career Matching → Response
According to AI Service Flow: Responses → RIASECAnalyzer → Scores → Career Mapping (top 2) → Results
"""

import pytest
import json
from app import create_app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['GEMINI_API_KEY'] = 'test-api-key'
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
def sample_riasec_responses():
    """Sample RIASEC assessment responses (36 questions)."""
    return {
        'R1': 4, 'R2': 3, 'R3': 5, 'R4': 4, 'R5': 4, 'R6': 2,
        'I1': 5, 'I2': 4, 'I3': 4, 'I4': 3, 'I5': 5, 'I6': 3,
        'A1': 2, 'A2': 3, 'A3': 2, 'A4': 3, 'A5': 2, 'A6': 3,
        'S1': 3, 'S2': 4, 'S3': 3, 'S4': 3, 'S5': 3, 'S6': 3,
        'E1': 4, 'E2': 3, 'E3': 3, 'E4': 3, 'E5': 4, 'E6': 3,
        'C1': 4, 'C2': 5, 'C3': 4, 'C4': 4, 'C5': 5, 'C6': 4
    }

def test_get_riasec_questions(client, auth_token):
    """
    Test fetching the RIASEC assessment questions.
    Flow: GET /api/v1/assessment/riasec/questions → Returns assessment questions
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/assessment/riasec/questions', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'questions' in data
    assert 'pagination' in data
    assert 'assessment_info' in data
    assert len(data['questions']) > 0
    
    # Check question structure
    question = data['questions'][0]
    assert 'id' in question
    assert 'question' in question
    assert 'category' in question
    assert 'type' in question

def test_submit_riasec_assessment(client, auth_token, sample_riasec_responses):
    """
    Test submitting RIASEC assessment.
    Flow: POST /api/v1/assessment/riasec/submit → RIASECAnalyzer → Returns top 2 careers (after tuning)
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    assessment_data = {
        "responses": sample_riasec_responses
    }
    response = client.post('/api/v1/assessment/riasec/submit', 
                             data=json.dumps(assessment_data),
                             headers=headers,
                             content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)['data']
    assert 'assessment_result' in data
    assert 'riasec_scores' in data
    assert 'personality_analysis' in data
    assert 'primary_personality_type' in data
    
    # Check RIASEC scores
    riasec_scores = data['riasec_scores']
    assert isinstance(riasec_scores, dict)
    assert 'Realistic' in riasec_scores or 'realistic' in riasec_scores
    
    # Check personality analysis
    personality_analysis = data['personality_analysis']
    assert 'primary_type' in personality_analysis
    
    # After tuning, career suggestions should be limited
    if 'career_suggestions' in personality_analysis:
        # RIASEC analyzer returns max 2 careers
        assert len(personality_analysis['career_suggestions']) <= 2

def test_submit_riasec_assessment_validation_error(client, auth_token):
    """
    Test RIASEC assessment validation - missing responses.
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    assessment_data = {}  # Missing responses
    
    response = client.post('/api/v1/assessment/riasec/submit', 
                             data=json.dumps(assessment_data),
                             headers=headers,
                             content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False

def test_get_riasec_results(client, auth_token):
    """
    Test retrieving RIASEC assessment results.
    Flow: GET /api/v1/assessment/riasec/results/{student_id}
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/assessment/riasec/results/1', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'assessment_result' in data
    assert 'interpretation' in data

def test_get_assessment_history(client, auth_token):
    """
    Test retrieving assessment history.
    Flow: GET /api/v1/assessment/history/{student_id}
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/assessment/history/1', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'assessment_history' in data
    assert 'summary_statistics' in data
    assert isinstance(data['assessment_history'], list)

def test_get_available_assessments(client, auth_token):
    """
    Test getting available assessments.
    Flow: GET /api/v1/assessment/available
    """
    if not auth_token:
        pytest.skip("Auth token generation failed")
    
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = client.get('/api/v1/assessment/available', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'available_assessments' in data
    assert isinstance(data['available_assessments'], list)
    assert len(data['available_assessments']) > 0

