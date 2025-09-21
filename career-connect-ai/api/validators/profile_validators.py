"""
Profile data validation
"""

from typing import Dict, List, Any
import re

def validate_profile_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate profile creation data"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # Email validation
    email = data.get('email')
    if email and not _is_valid_email(email):
        errors.append("Invalid email format")
    
    # Age validation
    age = data.get('age')
    if age is not None:
        if not isinstance(age, int) or age < 13 or age > 100:
            errors.append("Age must be between 13 and 100")
    
    # Skills validation
    skills = data.get('skills', [])
    if skills and not isinstance(skills, list):
        errors.append("Skills must be a list")
    elif skills:
        for skill in skills:
            if not isinstance(skill, str) or len(skill.strip()) == 0:
                errors.append("Each skill must be a non-empty string")
    
    # Interests validation
    interests = data.get('interests', [])
    if interests and not isinstance(interests, list):
        errors.append("Interests must be a list")
    elif interests:
        for interest in interests:
            if not isinstance(interest, str) or len(interest.strip()) == 0:
                errors.append("Each interest must be a non-empty string")
    
    # Career goals validation
    career_goals = data.get('career_goals', [])
    if career_goals and not isinstance(career_goals, list):
        errors.append("Career goals must be a list")
    elif career_goals:
        for goal in career_goals:
            if not isinstance(goal, str) or len(goal.strip()) == 0:
                errors.append("Each career goal must be a non-empty string")
    
    # Education level validation
    education_level = data.get('education_level')
    valid_education_levels = ['high_school', 'associate', 'bachelor', 'master', 'phd']
    if education_level and education_level not in valid_education_levels:
        errors.append(f"Education level must be one of: {', '.join(valid_education_levels)}")
    
    # Experience level validation
    experience_level = data.get('experience_level')
    valid_experience_levels = ['no_experience', 'entry_level', 'intermediate', 'experienced']
    if experience_level and experience_level not in valid_experience_levels:
        errors.append(f"Experience level must be one of: {', '.join(valid_experience_levels)}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_profile_update(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate profile update data"""
    errors = []
    
    # Email validation if provided
    email = data.get('email')
    if email and not _is_valid_email(email):
        errors.append("Invalid email format")
    
    # Age validation if provided
    age = data.get('age')
    if age is not None:
        if not isinstance(age, int) or age < 13 or age > 100:
            errors.append("Age must be between 13 and 100")
    
    # Skills validation if provided
    skills = data.get('skills')
    if skills is not None:
        if not isinstance(skills, list):
            errors.append("Skills must be a list")
        else:
            for skill in skills:
                if not isinstance(skill, str) or len(skill.strip()) == 0:
                    errors.append("Each skill must be a non-empty string")
    
    # Interests validation if provided
    interests = data.get('interests')
    if interests is not None:
        if not isinstance(interests, list):
            errors.append("Interests must be a list")
        else:
            for interest in interests:
                if not isinstance(interest, str) or len(interest.strip()) == 0:
                    errors.append("Each interest must be a non-empty string")
    
    # Career goals validation if provided
    career_goals = data.get('career_goals')
    if career_goals is not None:
        if not isinstance(career_goals, list):
            errors.append("Career goals must be a list")
        else:
            for goal in career_goals:
                if not isinstance(goal, str) or len(goal.strip()) == 0:
                    errors.append("Each career goal must be a non-empty string")
    
    # Education level validation if provided
    education_level = data.get('education_level')
    valid_education_levels = ['high_school', 'associate', 'bachelor', 'master', 'phd']
    if education_level and education_level not in valid_education_levels:
        errors.append(f"Education level must be one of: {', '.join(valid_education_levels)}")
    
    # Experience level validation if provided
    experience_level = data.get('experience_level')
    valid_experience_levels = ['no_experience', 'entry_level', 'intermediate', 'experienced']
    if experience_level and experience_level not in valid_experience_levels:
        errors.append(f"Experience level must be one of: {', '.join(valid_experience_levels)}")
    
    # Learning style validation if provided
    learning_style = data.get('learning_style')
    valid_learning_styles = ['visual', 'auditory', 'kinesthetic', 'reading']
    if learning_style and learning_style not in valid_learning_styles:
        errors.append(f"Learning style must be one of: {', '.join(valid_learning_styles)}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def _is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
