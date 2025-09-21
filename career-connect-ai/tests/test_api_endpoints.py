"""
Test API endpoints
"""

import pytest
import json

class TestProfileRoutes:
    """Test profile management endpoints"""
    
    def test_create_profile(self, client, auth_headers, sample_student_profile):
        """Test profile creation"""
        response = client.post(
            '/api/profile/create',
            json=sample_student_profile,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'profile' in data
        assert 'analysis' in data
    
    def test_get_profile(self, client, auth_headers):
        """Test profile retrieval"""
        response = client.get(
            '/api/profile/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'profile' in data
    
    def test_update_profile(self, client, auth_headers):
        """Test profile update"""
        update_data = {
            'skills': ['Python', 'JavaScript', 'Communication', 'Leadership']
        }
        response = client.put(
            '/api/profile/1',
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'analysis' in data
    
    def test_get_profile_analysis(self, client, auth_headers):
        """Test profile analysis"""
        response = client.get(
            '/api/profile/1/analysis',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'profile_analysis' in data

class TestAssessmentRoutes:
    """Test assessment endpoints"""
    
    def test_submit_riasec_assessment(self, client, auth_headers, sample_assessment_responses):
        """Test RIASEC assessment submission"""
        data = {
            'responses': sample_assessment_responses,
            'assessment_type': 'riasec'
        }
        response = client.post(
            '/api/assessment/riasec',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'riasec_scores' in data
        assert 'personality_analysis' in data
    
    def test_submit_skills_assessment(self, client, auth_headers):
        """Test skills assessment submission"""
        data = {
            'responses': {
                'Python': {'level': 'intermediate', 'confidence': 80},
                'JavaScript': {'level': 'beginner', 'confidence': 60},
                'Communication': {'level': 'advanced', 'confidence': 90}
            },
            'assessment_type': 'skills'
        }
        response = client.post(
            '/api/assessment/skills',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'skills_scores' in data
        assert 'overall_scores' in data
    
    def test_get_assessment_results(self, client, auth_headers):
        """Test assessment results retrieval"""
        response = client.get(
            '/api/assessment/results/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'assessment_result' in data
    
    def test_get_available_assessments(self, client, auth_headers):
        """Test available assessments retrieval"""
        response = client.get(
            '/api/assessment/available',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'available_assessments' in data

class TestCareerRoutes:
    """Test career discovery endpoints"""
    
    def test_get_career_recommendations(self, client, auth_headers):
        """Test career recommendations"""
        response = client.get(
            '/api/career/recommendations/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'career_recommendations' in data
    
    def test_search_careers(self, client, auth_headers):
        """Test career search"""
        response = client.get(
            '/api/career/search?q=software',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'search_results' in data
    
    def test_get_career_details(self, client, auth_headers):
        """Test career details"""
        response = client.get(
            '/api/career/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'career_details' in data
    
    def test_get_career_trends(self, client, auth_headers):
        """Test career trends"""
        response = client.get(
            '/api/career/trends',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'career_trends' in data
    
    def test_compare_careers(self, client, auth_headers):
        """Test career comparison"""
        data = {
            'career_ids': [1, 2]
        }
        response = client.post(
            '/api/career/compare',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'career_comparison' in data

class TestChatRoutes:
    """Test chat endpoints"""
    
    def test_create_chat_session(self, client, auth_headers, sample_student_profile):
        """Test chat session creation"""
        data = {
            'initial_context': {'topic': 'career_guidance'}
        }
        response = client.post(
            '/api/chat/session',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'session_id' in data
        assert 'student_profile' in data
    
    def test_send_message(self, client, auth_headers):
        """Test sending chat message"""
        data = {
            'message': 'What careers match my personality?',
            'session_id': 'test-session-123'
        }
        response = client.post(
            '/api/chat/message',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'response_data' in data
    
    def test_get_chat_history(self, client, auth_headers):
        """Test chat history retrieval"""
        response = client.get(
            '/api/chat/history/test-session-123',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'chat_history' in data
    
    def test_get_chat_suggestions(self, client, auth_headers):
        """Test chat suggestions"""
        response = client.get(
            '/api/chat/suggestions',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'chat_suggestions' in data

class TestLearningRoutes:
    """Test learning path endpoints"""
    
    def test_get_learning_path(self, client, auth_headers):
        """Test learning path generation"""
        response = client.get(
            '/api/learning/path/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'learning_path' in data
    
    def test_get_learning_resources(self, client, auth_headers):
        """Test learning resources"""
        response = client.get(
            '/api/learning/resources/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'learning_resources' in data
    
    def test_create_skill_development_path(self, client, auth_headers):
        """Test skill development path creation"""
        data = {
            'skill': 'Python',
            'current_level': 'beginner',
            'target_level': 'intermediate',
            'learning_style': 'visual'
        }
        response = client.post(
            '/api/learning/skill-development',
            json=data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'skill_development_path' in data
    
    def test_get_learning_recommendations(self, client, auth_headers):
        """Test learning recommendations"""
        response = client.get(
            '/api/learning/recommendations',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'learning_recommendations' in data

class TestMentorRoutes:
    """Test mentor matching endpoints"""
    
    def test_get_mentor_recommendations(self, client, auth_headers):
        """Test mentor recommendations"""
        response = client.get(
            '/api/mentor/recommendations/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'mentor_recommendations' in data
    
    def test_get_mentor_profile(self, client, auth_headers):
        """Test mentor profile"""
        response = client.get(
            '/api/mentor/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'mentor_profile' in data
        assert 'profile_analysis' in data
    
    def test_search_mentors(self, client, auth_headers):
        """Test mentor search"""
        response = client.get(
            '/api/mentor/search?q=software',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'search_results' in data
    
    def test_check_mentor_availability(self, client, auth_headers):
        """Test mentor availability"""
        response = client.get(
            '/api/mentor/availability/1',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'mentor_availability' in data
