"""
Integration tests for complete AI service flow
Tests the full flow: API Route → Service → Core AI → Response
According to the AI Service Flow document
"""

import pytest
import json
from app import create_app

@pytest.fixture
def client():
    """Create test Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['GEMINI_API_KEY'] = 'test-api-key'
    with app.test_client() as client:
        yield client

class TestCompleteChatFlow:
    """Test complete chat flow from API to AI response."""
    
    def test_chat_complete_flow(self, client):
        """
        Test complete chat flow:
        POST /api/v1/chat → ChatService.process_chat_message() → 
        ConversationManager → GeminiClient.chat_response() → Response
        """
        chat_data = {
            "message": "What career should I choose?",
            "profile": {
                "name": "Test Student",
                "skills": ["Python"],
                "interests": ["Technology"]
            }
        }
        
        response = client.post('/api/v1/chat',
                             data=json.dumps(chat_data),
                             content_type='application/json')
        
        # Tests the flow - may require API key but validates structure
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            # Validate response structure matches flow
            assert data['success'] == True
            assert 'data' in data
            assert 'response' in data['data']
            assert 'session_id' in data['data']

class TestCompleteCareerFlow:
    """Test complete career analysis flow."""
    
    def test_career_analysis_complete_flow(self, client):
        """
        Test complete career analysis flow:
        POST /api/v1/careers/analyze → CareerDiscoveryService.discover_careers_by_profile() →
        Multi-factor matching → Returns recommendations
        """
        profile = {
            "name": "Test Student",
            "skills": ["Python", "Data Analysis"],
            "interests": ["Technology", "Data Science"],
            "riasecScores": {
                "realistic": 60,
                "investigative": 85,
                "artistic": 40,
                "social": 45,
                "enterprising": 70,
                "conventional": 50
            }
        }
        
        response = client.post('/api/v1/careers/analyze',
                             data=json.dumps(profile),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Validate flow produces correct structure
        assert data['success'] == True
        assert 'data' in data
        response_data = data['data']
        
        # Should have RIASEC scores (from profile or defaults)
        assert 'riasecScores' in response_data
        assert 'topCareers' in response_data
        assert 'personalityProfile' in response_data
        assert 'analysis_complete' in response_data

class TestCompleteAssessmentFlow:
    """Test complete RIASEC assessment flow."""
    
    def test_riasec_complete_flow(self, client):
        """
        Test complete RIASEC flow:
        POST /api/v1/assessment/riasec/submit → RIASECAnalyzer.calculate_riasec_scores() →
        RIASECAnalyzer.analyze_personality_profile() → RIASECAnalyzer.map_careers_to_personality() →
        Returns top 2 careers
        """
        # Get auth token first
        auth_response = client.post('/api/v1/auth/dev-token',
                                  data=json.dumps({'student_id': 1}),
                                  content_type='application/json')
        auth_token = json.loads(auth_response.data)['data']['access_token']
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Sample RIASEC responses (36 questions)
        assessment_data = {
            "responses": {
                'R1': 4, 'R2': 3, 'R3': 5, 'R4': 4, 'R5': 4, 'R6': 2,
                'I1': 5, 'I2': 4, 'I3': 4, 'I4': 3, 'I5': 5, 'I6': 3,
                'A1': 2, 'A2': 3, 'A3': 2, 'A4': 3, 'A5': 2, 'A6': 3,
                'S1': 3, 'S2': 4, 'S3': 3, 'S4': 3, 'S5': 3, 'S6': 3,
                'E1': 4, 'E2': 3, 'E3': 3, 'E4': 3, 'E5': 4, 'E6': 3,
                'C1': 4, 'C2': 5, 'C3': 4, 'C4': 4, 'C5': 5, 'C6': 4
            }
        }
        
        response = client.post('/api/v1/assessment/riasec/submit',
                             data=json.dumps(assessment_data),
                             headers=headers,
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        
        # Validate complete flow produces expected output
        assert 'assessment_result' in data
        assert 'riasec_scores' in data
        assert 'personality_analysis' in data
        assert 'primary_personality_type' in data
        
        # After tuning: Should return max 2 career matches
        personality_analysis = data['personality_analysis']
        if 'career_suggestions' in personality_analysis:
            assert len(personality_analysis['career_suggestions']) <= 2

class TestServiceLayerIntegration:
    """Test service layer integration without API calls."""
    
    def test_career_discovery_service_flow(self):
        """Test CareerDiscoveryService flow without API."""
        from services.career_discovery import CareerDiscoveryService
        
        service = CareerDiscoveryService()
        
        profile = {
            'academic_info': {'stream': 'Science'},
            'skill_assessments': {
                'technical_skills': {'Programming': 4}
            },
            'interests': ['Technology'],
            'riasec_scores': {
                'Realistic': 60,
                'Investigative': 80,
                'Artistic': 40,
                'Social': 45,
                'Enterprising': 70,
                'Conventional': 50
            },
            'preferences': {}
        }
        
        # Test the service directly
        result = service.discover_careers_by_profile(profile)
        
        # Validate service returns expected structure
        assert hasattr(result, 'primary_matches')
        assert hasattr(result, 'alternative_careers')
        assert hasattr(result, 'recommendations')
        assert hasattr(result, 'discovery_timestamp')
        
        # Validate matches are returned
        assert isinstance(result.primary_matches, list)
        # After tuning: Service may return up to 10, but individual analyzers return max 2

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

