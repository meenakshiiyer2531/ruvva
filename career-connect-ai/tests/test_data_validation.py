"""
Test data validation
"""

import pytest
from api.validators.profile_validators import ProfileValidator
from api.validators.assessment_validators import AssessmentValidator
from api.validators.chat_validators import ChatValidator

class TestProfileValidator:
    """Test profile validation"""
    
    def test_valid_student_profile(self):
        """Test valid student profile"""
        profile_data = {
            'name': 'John Doe',
            'age': 20,
            'grade': '12th',
            'interests': ['Technology', 'Science'],
            'skills': ['Python', 'Communication'],
            'learning_style': 'Visual',
            'career_goals': ['Software Engineer'],
            'location': 'New York',
            'contact_info': {
                'email': 'john@example.com',
                'phone': '+1234567890'
            }
        }
        validator = ProfileValidator()
        result = validator.validate_student_profile(profile_data)
        assert result['valid'] == True
        assert 'errors' not in result
    
    def test_invalid_student_profile_missing_name(self):
        """Test invalid student profile missing name"""
        profile_data = {
            'age': 20,
            'grade': '12th',
            'interests': ['Technology', 'Science'],
            'skills': ['Python', 'Communication'],
            'learning_style': 'Visual',
            'career_goals': ['Software Engineer'],
            'location': 'New York',
            'contact_info': {
                'email': 'john@example.com',
                'phone': '+1234567890'
            }
        }
        validator = ProfileValidator()
        result = validator.validate_student_profile(profile_data)
        assert result['valid'] == False
        assert 'name' in result['errors']
    
    def test_invalid_student_profile_invalid_age(self):
        """Test invalid student profile with invalid age"""
        profile_data = {
            'name': 'John Doe',
            'age': -5,
            'grade': '12th',
            'interests': ['Technology', 'Science'],
            'skills': ['Python', 'Communication'],
            'learning_style': 'Visual',
            'career_goals': ['Software Engineer'],
            'location': 'New York',
            'contact_info': {
                'email': 'john@example.com',
                'phone': '+1234567890'
            }
        }
        validator = ProfileValidator()
        result = validator.validate_student_profile(profile_data)
        assert result['valid'] == False
        assert 'age' in result['errors']
    
    def test_invalid_student_profile_invalid_email(self):
        """Test invalid student profile with invalid email"""
        profile_data = {
            'name': 'John Doe',
            'age': 20,
            'grade': '12th',
            'interests': ['Technology', 'Science'],
            'skills': ['Python', 'Communication'],
            'learning_style': 'Visual',
            'career_goals': ['Software Engineer'],
            'location': 'New York',
            'contact_info': {
                'email': 'invalid-email',
                'phone': '+1234567890'
            }
        }
        validator = ProfileValidator()
        result = validator.validate_student_profile(profile_data)
        assert result['valid'] == False
        assert 'contact_info.email' in result['errors']
    
    def test_invalid_student_profile_invalid_phone(self):
        """Test invalid student profile with invalid phone"""
        profile_data = {
            'name': 'John Doe',
            'age': 20,
            'grade': '12th',
            'interests': ['Technology', 'Science'],
            'skills': ['Python', 'Communication'],
            'learning_style': 'Visual',
            'career_goals': ['Software Engineer'],
            'location': 'New York',
            'contact_info': {
                'email': 'john@example.com',
                'phone': 'invalid-phone'
            }
        }
        validator = ProfileValidator()
        result = validator.validate_student_profile(profile_data)
        assert result['valid'] == False
        assert 'contact_info.phone' in result['errors']

class TestAssessmentValidator:
    """Test assessment validation"""
    
    def test_valid_riasec_assessment(self):
        """Test valid RIASEC assessment"""
        assessment_data = {
            'responses': {
                'question_1': 'A',
                'question_2': 'B',
                'question_3': 'C'
            },
            'assessment_type': 'riasec'
        }
        validator = AssessmentValidator()
        result = validator.validate_riasec_assessment(assessment_data)
        assert result['valid'] == True
        assert 'errors' not in result
    
    def test_invalid_riasec_assessment_missing_responses(self):
        """Test invalid RIASEC assessment missing responses"""
        assessment_data = {
            'assessment_type': 'riasec'
        }
        validator = AssessmentValidator()
        result = validator.validate_riasec_assessment(assessment_data)
        assert result['valid'] == False
        assert 'responses' in result['errors']
    
    def test_invalid_riasec_assessment_invalid_type(self):
        """Test invalid RIASEC assessment with invalid type"""
        assessment_data = {
            'responses': {
                'question_1': 'A',
                'question_2': 'B',
                'question_3': 'C'
            },
            'assessment_type': 'invalid_type'
        }
        validator = AssessmentValidator()
        result = validator.validate_riasec_assessment(assessment_data)
        assert result['valid'] == False
        assert 'assessment_type' in result['errors']
    
    def test_valid_skills_assessment(self):
        """Test valid skills assessment"""
        assessment_data = {
            'responses': {
                'Python': {'level': 'intermediate', 'confidence': 80},
                'JavaScript': {'level': 'beginner', 'confidence': 60},
                'Communication': {'level': 'advanced', 'confidence': 90}
            },
            'assessment_type': 'skills'
        }
        validator = AssessmentValidator()
        result = validator.validate_skills_assessment(assessment_data)
        assert result['valid'] == True
        assert 'errors' not in result
    
    def test_invalid_skills_assessment_missing_level(self):
        """Test invalid skills assessment missing level"""
        assessment_data = {
            'responses': {
                'Python': {'confidence': 80},
                'JavaScript': {'level': 'beginner', 'confidence': 60},
                'Communication': {'level': 'advanced', 'confidence': 90}
            },
            'assessment_type': 'skills'
        }
        validator = AssessmentValidator()
        result = validator.validate_skills_assessment(assessment_data)
        assert result['valid'] == False
        assert 'responses.Python.level' in result['errors']
    
    def test_invalid_skills_assessment_invalid_confidence(self):
        """Test invalid skills assessment with invalid confidence"""
        assessment_data = {
            'responses': {
                'Python': {'level': 'intermediate', 'confidence': 150},
                'JavaScript': {'level': 'beginner', 'confidence': 60},
                'Communication': {'level': 'advanced', 'confidence': 90}
            },
            'assessment_type': 'skills'
        }
        validator = AssessmentValidator()
        result = validator.validate_skills_assessment(assessment_data)
        assert result['valid'] == False
        assert 'responses.Python.confidence' in result['errors']

class TestChatValidator:
    """Test chat validation"""
    
    def test_valid_chat_message(self):
        """Test valid chat message"""
        message_data = {
            'message': 'What careers match my personality?',
            'session_id': 'test-session-123'
        }
        validator = ChatValidator()
        result = validator.validate_chat_message(message_data)
        assert result['valid'] == True
        assert 'errors' not in result
    
    def test_invalid_chat_message_missing_message(self):
        """Test invalid chat message missing message"""
        message_data = {
            'session_id': 'test-session-123'
        }
        validator = ChatValidator()
        result = validator.validate_chat_message(message_data)
        assert result['valid'] == False
        assert 'message' in result['errors']
    
    def test_invalid_chat_message_missing_session_id(self):
        """Test invalid chat message missing session ID"""
        message_data = {
            'message': 'What careers match my personality?'
        }
        validator = ChatValidator()
        result = validator.validate_chat_message(message_data)
        assert result['valid'] == False
        assert 'session_id' in result['errors']
    
    def test_invalid_chat_message_empty_message(self):
        """Test invalid chat message with empty message"""
        message_data = {
            'message': '',
            'session_id': 'test-session-123'
        }
        validator = ChatValidator()
        result = validator.validate_chat_message(message_data)
        assert result['valid'] == False
        assert 'message' in result['errors']
    
    def test_valid_chat_session(self):
        """Test valid chat session"""
        session_data = {
            'initial_context': {'topic': 'career_guidance'}
        }
        validator = ChatValidator()
        result = validator.validate_chat_session(session_data)
        assert result['valid'] == True
        assert 'errors' not in result
    
    def test_invalid_chat_session_missing_context(self):
        """Test invalid chat session missing context"""
        session_data = {}
        validator = ChatValidator()
        result = validator.validate_chat_session(session_data)
        assert result['valid'] == False
        assert 'initial_context' in result['errors']
