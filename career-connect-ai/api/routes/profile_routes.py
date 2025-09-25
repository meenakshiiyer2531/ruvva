"""
Profile management API routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.limiter import limiter
from api.validators.profile_validators import validate_profile_data, validate_profile_update
from services.profile_analyzer import StudentProfileAnalyzer
from models.student import Student
from utils.logger import get_logger
from utils.response_formatter import APIResponse, handle_exceptions
import json
import uuid

logger = get_logger(__name__)

# Create blueprint
profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/profile')

# Rate limiter is initialized in app.py

# Initialize services
profile_analyzer = StudentProfileAnalyzer()

@profile_bp.route('/create', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
@handle_exceptions
def create_profile():
    """Create a new student profile"""
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Validate input data
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    validation_result = validate_profile_data(data)
    
    if not validation_result['valid']:
        return APIResponse.validation_error(validation_result['errors'])
    
    # Create student profile
    student = Student.from_dict(data)
    student.id = user_id  # Use JWT user ID
    
    # Save to database (this would be implemented with actual database)
    # db.session.add(student)
    # db.session.commit()
    
    # Generate profile analysis
    analysis = profile_analyzer.analyze_complete_profile(data)
    
    response_data = {
        'profile': student.to_dict(),
        'analysis': analysis,
        'profile_id': user_id
    }
    
    logger.info(f"Profile created successfully for user {user_id}")
    return APIResponse.success(response_data, "Profile created successfully", 201)

@profile_bp.route('/update', methods=['PUT'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def update_profile():
    """Update existing student profile"""
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Validate input data
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    validation_result = validate_profile_update(data)
    
    if not validation_result['valid']:
        return APIResponse.validation_error(validation_result['errors'])
    
    # Update profile in database
    # student = Student.query.get(user_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Update fields
    # for key, value in data.items():
    #     if hasattr(student, key):
    #         setattr(student, key, value)
    
    # db.session.commit()
    
    # Generate updated analysis
    updated_data = data  # This would be the updated student data
    analysis = profile_analyzer.analyze_complete_profile(updated_data)
    
    response_data = {
        'profile': updated_data,
        'analysis': analysis,
        'updated_fields': list(data.keys())
    }
    
    logger.info(f"Profile updated successfully for user {user_id}")
    return APIResponse.success(response_data, "Profile updated successfully")

@profile_bp.route('/<int:student_id>', methods=['GET'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def get_profile(student_id):
    """Get student profile by ID"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only access your own profile")
    
    # Get profile from database
    # student = Student.query.get(student_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock data for now
    student_data = {
        'id': student_id,
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 25,
        'education_level': 'bachelor',
        'skills': ['Python', 'JavaScript', 'Communication'],
        'interests': ['Technology', 'Data Science'],
        'career_goals': ['Software Engineer', 'Data Scientist'],
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-15T10:30:00Z',
        'profile_completion': 85
    }
    
    logger.info(f"Profile retrieved for user {user_id}")
    return APIResponse.success(student_data, "Profile retrieved successfully")

@profile_bp.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def analyze_profile():
    """Analyze profile for insights and recommendations"""
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json() or {}
    analysis_type = data.get('analysis_type', 'comprehensive')  # 'comprehensive', 'skills', 'personality', 'career_fit'
    
    # Get profile data
    # student = Student.query.get(user_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock profile data
    profile_data = {
        'id': user_id,
        'name': 'John Doe',
        'skills': ['Python', 'JavaScript', 'Communication'],
        'interests': ['Technology', 'Data Science'],
        'career_goals': ['Software Engineer', 'Data Scientist'],
        'riasec_scores': {
            'realistic': 60,
            'investigative': 80,
            'artistic': 40,
            'social': 50,
            'enterprising': 70,
            'conventional': 30
        }
    }
    
    # Generate analysis based on type
    if analysis_type == 'comprehensive':
        analysis = profile_analyzer.analyze_complete_profile(profile_data)
    elif analysis_type == 'skills':
        analysis = profile_analyzer.analyze_skills_profile(profile_data.get('skills', []))
    elif analysis_type == 'personality':
        analysis = profile_analyzer.analyze_personality_profile(profile_data.get('riasec_scores', {}))
    else:
        analysis = profile_analyzer.analyze_complete_profile(profile_data)
    
    response_data = {
        'analysis': analysis,
        'analysis_type': analysis_type,
        'profile_summary': {
            'strengths': analysis.get('strengths', []),
            'areas_for_improvement': analysis.get('areas_for_improvement', []),
            'recommended_careers': analysis.get('recommended_careers', [])
        }
    }
    
    logger.info(f"Profile analysis completed for user {user_id}, type: {analysis_type}")
    return APIResponse.success(response_data, "Profile analysis completed successfully")

@profile_bp.route('/<int:student_id>/insights', methods=['GET'])
@limiter.limit("15 per minute")
@jwt_required()
@handle_exceptions
def get_profile_insights(student_id):
    """Get AI-powered profile insights"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only access your own profile insights")
    
    # Get profile data
    # student = Student.query.get(student_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock profile data
    profile_data = {
        'id': student_id,
        'name': 'John Doe',
        'skills': ['Python', 'JavaScript', 'Communication'],
        'interests': ['Technology', 'Data Science'],
        'career_goals': ['Software Engineer', 'Data Scientist'],
        'riasec_scores': {
            'realistic': 60,
            'investigative': 80,
            'artistic': 40,
            'social': 50,
            'enterprising': 70,
            'conventional': 30
        }
    }
    
    # Generate insights
    insights = profile_analyzer.generate_profile_insights(profile_data)
    
    response_data = {
        'insights': insights,
        'profile_id': student_id,
        'insight_categories': {
            'personality_insights': insights.get('personality_insights', []),
            'career_recommendations': insights.get('career_recommendations', []),
            'skill_development': insights.get('skill_development', []),
            'learning_suggestions': insights.get('learning_suggestions', [])
        },
        'confidence_score': insights.get('confidence_score', 0.85)
    }
    
    logger.info(f"Profile insights generated for user {user_id}")
    return APIResponse.success(response_data, "Profile insights generated successfully")

# Additional profile management endpoints

@profile_bp.route('/<int:student_id>/skills-gap', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def analyze_skills_gap(student_id):
    """Analyze skills gap for career transition"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only analyze your own profile")
    
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    target_career = data.get('target_career')
    career_requirements = data.get('career_requirements', {})
    
    if not target_career:
        return APIResponse.validation_error({"target_career": "Target career is required"})
    
    # Get current skills
    # student = Student.query.get(student_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock current skills
    current_skills = ['Python', 'JavaScript', 'Communication']
    
    # Analyze skills gap
    gap_analysis = profile_analyzer.analyze_skills_gap(
        current_skills, target_career, career_requirements
    )
    
    response_data = {
        'skills_gap_analysis': gap_analysis,
        'target_career': target_career,
        'current_skills': current_skills,
        'missing_skills': gap_analysis.get('missing_skills', []),
        'skill_match_percentage': gap_analysis.get('skill_match_percentage', 0)
    }
    
    logger.info(f"Skills gap analysis completed for user {user_id}, target: {target_career}")
    return APIResponse.success(response_data, "Skills gap analysis completed successfully")


@profile_bp.route('/<int:student_id>/personality-fit', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def assess_personality_fit(student_id):
    """Assess personality-career fit"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only assess your own profile")
    
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    career_riasec_requirements = data.get('career_riasec_requirements', {})
    
    if not career_riasec_requirements:
        return APIResponse.validation_error({"career_riasec_requirements": "Career RIASEC requirements are required"})
    
    # Get RIASEC scores
    # student = Student.query.get(student_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock RIASEC scores
    riasec_scores = {
        'realistic': 60,
        'investigative': 80,
        'artistic': 40,
        'social': 50,
        'enterprising': 70,
        'conventional': 30
    }
    
    # Assess personality fit
    fit_analysis = profile_analyzer.assess_personality_career_fit(
        riasec_scores, career_riasec_requirements
    )
    
    response_data = {
        'personality_fit_analysis': fit_analysis,
        'student_riasec_scores': riasec_scores,
        'career_requirements': career_riasec_requirements,
        'fit_percentage': fit_analysis.get('fit_percentage', 0),
        'compatibility_level': fit_analysis.get('compatibility_level', 'moderate')
    }
    
    logger.info(f"Personality fit analysis completed for user {user_id}")
    return APIResponse.success(response_data, "Personality fit analysis completed successfully")


@profile_bp.route('/validate', methods=['POST'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def validate_profile_data_endpoint():
    """Validate profile data without saving"""
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    validation_result = validate_profile_data(data)
    
    response_data = {
        'validation_result': validation_result,
        'is_valid': validation_result['valid'],
        'errors': validation_result.get('errors', {}),
        'warnings': validation_result.get('warnings', {}),
        'completion_score': validation_result.get('completion_score', 0)
    }
    
    message = "Profile data is valid" if validation_result['valid'] else "Profile data validation failed"
    status_code = 200 if validation_result['valid'] else 400
    
    return APIResponse.success(response_data, message) if validation_result['valid'] else APIResponse.validation_error(validation_result['errors'])


@profile_bp.route('/completion-status', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_profile_completion_status():
    """Get profile completion status and suggestions"""
    user_id = get_jwt_identity()
    
    # Get profile data
    # student = Student.query.get(user_id)
    # if not student:
    #     return APIResponse.not_found("Profile")
    
    # Mock profile completion analysis
    completion_analysis = {
        'overall_completion': 75,
        'sections': {
            'basic_info': {'completion': 100, 'required': True},
            'education': {'completion': 80, 'required': True},
            'skills': {'completion': 60, 'required': True},
            'interests': {'completion': 90, 'required': False},
            'career_goals': {'completion': 50, 'required': True},
            'riasec_assessment': {'completion': 0, 'required': False}
        },
        'missing_fields': ['work_experience', 'certifications'],
        'suggestions': [
            'Complete your RIASEC personality assessment',
            'Add more technical skills to your profile',
            'Define clearer career goals'
        ],
        'next_steps': [
            'Take the personality assessment',
            'Update your skills section',
            'Set specific career objectives'
        ]
    }
    
    response_data = {
        'completion_analysis': completion_analysis,
        'profile_strength': 'good' if completion_analysis['overall_completion'] > 70 else 'needs_improvement',
        'recommendations': completion_analysis['suggestions']
    }
    
    logger.info(f"Profile completion status retrieved for user {user_id}")
    return APIResponse.success(response_data, "Profile completion status retrieved successfully")
