"""
Assessment data validation
"""

from typing import Dict, List, Any

def validate_assessment_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate assessment creation data"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'assessment_type']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # Assessment type validation
    assessment_type = data.get('assessment_type')
    valid_types = ['riasec', 'skills', 'personality', 'aptitude', 'career_interest']
    if assessment_type and assessment_type not in valid_types:
        errors.append(f"Assessment type must be one of: {', '.join(valid_types)}")
    
    # Questions validation
    questions = data.get('questions', [])
    if not isinstance(questions, list):
        errors.append("Questions must be a list")
    elif len(questions) == 0:
        errors.append("At least one question is required")
    else:
        for i, question in enumerate(questions):
            if not isinstance(question, dict):
                errors.append(f"Question {i+1} must be a dictionary")
            elif not question.get('text'):
                errors.append(f"Question {i+1} must have text")
            elif not question.get('options') and question.get('type') != 'text':
                errors.append(f"Question {i+1} must have options")
    
    # Question count validation
    question_count = data.get('question_count')
    if question_count is not None:
        if not isinstance(question_count, int) or question_count < 1:
            errors.append("Question count must be a positive integer")
        elif len(questions) != question_count:
            errors.append("Question count must match the number of questions provided")
    
    # Estimated duration validation
    estimated_duration = data.get('estimated_duration')
    if estimated_duration is not None:
        if not isinstance(estimated_duration, int) or estimated_duration < 1:
            errors.append("Estimated duration must be a positive integer")
    
    # Difficulty level validation
    difficulty_level = data.get('difficulty_level')
    valid_difficulties = ['beginner', 'intermediate', 'advanced']
    if difficulty_level and difficulty_level not in valid_difficulties:
        errors.append(f"Difficulty level must be one of: {', '.join(valid_difficulties)}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_assessment_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate assessment response data"""
    errors = []
    
    # Required fields
    if not data.get('responses'):
        errors.append("Responses are required")
    
    responses = data.get('responses', {})
    if not isinstance(responses, dict):
        errors.append("Responses must be a dictionary")
    elif len(responses) == 0:
        errors.append("At least one response is required")
    else:
        # Validate each response
        for question_id, response in responses.items():
            if not isinstance(question_id, str) or len(question_id.strip()) == 0:
                errors.append("Question ID must be a non-empty string")
            
            # Response can be various types depending on question type
            if response is None:
                errors.append(f"Response for question {question_id} cannot be null")
            elif isinstance(response, dict):
                # For complex responses (e.g., RIASEC weights)
                if 'score' in response:
                    score = response['score']
                    if not isinstance(score, (int, float)) or score < 0:
                        errors.append(f"Score for question {question_id} must be a non-negative number")
            elif isinstance(response, (int, float)):
                # For numeric responses
                if response < 0:
                    errors.append(f"Response for question {question_id} must be non-negative")
            elif isinstance(response, str):
                # For text responses
                if len(response.strip()) == 0:
                    errors.append(f"Text response for question {question_id} cannot be empty")
            else:
                errors.append(f"Invalid response type for question {question_id}")
    
    # Assessment type validation
    assessment_type = data.get('assessment_type')
    valid_types = ['riasec', 'skills', 'personality', 'aptitude', 'career_interest']
    if assessment_type and assessment_type not in valid_types:
        errors.append(f"Assessment type must be one of: {', '.join(valid_types)}")
    
    # Session ID validation
    session_id = data.get('session_id')
    if session_id and not isinstance(session_id, str):
        errors.append("Session ID must be a string")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_riasec_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate RIASEC assessment response"""
    errors = []
    
    responses = data.get('responses', {})
    if not responses:
        errors.append("Responses are required for RIASEC assessment")
        return {'valid': False, 'errors': errors}
    
    # Validate RIASEC-specific responses
    riasec_types = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
    
    for question_id, response in responses.items():
        if isinstance(response, dict) and 'riasec_weights' in response:
            # Validate RIASEC weights
            weights = response['riasec_weights']
            if not isinstance(weights, dict):
                errors.append(f"RIASEC weights for question {question_id} must be a dictionary")
            else:
                for riasec_type, weight in weights.items():
                    if riasec_type not in riasec_types:
                        errors.append(f"Invalid RIASEC type: {riasec_type}")
                    elif not isinstance(weight, (int, float)) or weight < 0:
                        errors.append(f"Weight for {riasec_type} must be a non-negative number")
        elif isinstance(response, int):
            # Simple numeric response
            if response < 1 or response > 5:
                errors.append(f"Response for question {question_id} must be between 1 and 5")
        else:
            errors.append(f"Invalid response format for question {question_id}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_skills_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate skills assessment response"""
    errors = []
    
    responses = data.get('responses', {})
    if not responses:
        errors.append("Responses are required for skills assessment")
        return {'valid': False, 'errors': errors}
    
    # Validate skills-specific responses
    for skill, response in responses.items():
        if not isinstance(skill, str) or len(skill.strip()) == 0:
            errors.append("Skill name must be a non-empty string")
        
        if isinstance(response, dict):
            # Complex skill response
            if 'level' in response:
                level = response['level']
                valid_levels = ['novice', 'beginner', 'intermediate', 'advanced', 'expert']
                if level not in valid_levels:
                    errors.append(f"Skill level for {skill} must be one of: {', '.join(valid_levels)}")
            
            if 'confidence' in response:
                confidence = response['confidence']
                if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 100:
                    errors.append(f"Confidence for {skill} must be between 0 and 100")
        elif isinstance(response, (int, float)):
            # Simple numeric response
            if response < 0 or response > 100:
                errors.append(f"Response for {skill} must be between 0 and 100")
        else:
            errors.append(f"Invalid response format for skill {skill}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
