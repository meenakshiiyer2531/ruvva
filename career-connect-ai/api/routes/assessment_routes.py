"""
Assessment processing API routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.limiter import limiter
from api.validators.assessment_validators import validate_assessment_data, validate_assessment_response
from core.riasec_analyzer import RIASECAnalyzer
from models.assessment import Assessment, AssessmentResult, RIASECResult
from utils.logger import get_logger
from utils.response_formatter import APIResponse, handle_exceptions, paginate_response
import json
import uuid

logger = get_logger(__name__)

# Create blueprint
assessment_bp = Blueprint('assessment', __name__, url_prefix='/api/v1/assessment')

# Rate limiter is initialized in app.py

# Initialize services
riasec_analyzer = RIASECAnalyzer()

@assessment_bp.route('/riasec/questions', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_riasec_questions():
    """Get RIASEC assessment questions"""
    # Mock RIASEC questions - in real implementation, these would come from database
    riasec_questions = [
        {
            'id': 1,
            'question': 'I like to work on cars',
            'category': 'realistic',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        },
        {
            'id': 2,
            'question': 'I like to do puzzles',
            'category': 'investigative',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        },
        {
            'id': 3,
            'question': 'I am good at keeping records of my work',
            'category': 'conventional',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        },
        {
            'id': 4,
            'question': 'I like to lead people',
            'category': 'enterprising',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        },
        {
            'id': 5,
            'question': 'I like to draw',
            'category': 'artistic',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        },
        {
            'id': 6,
            'question': 'I like to help people solve their problems',
            'category': 'social',
            'type': 'likert',
            'scale': {'min': 1, 'max': 5, 'labels': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']}
        }
        # In real implementation, there would be 60+ questions
    ]
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', None)  # Filter by RIASEC category
    
    # Filter by category if specified
    if category:
        filtered_questions = [q for q in riasec_questions if q['category'].lower() == category.lower()]
    else:
        filtered_questions = riasec_questions
    
    # Paginate results
    paginated_data = paginate_response(filtered_questions, page, per_page)
    
    response_data = {
        'questions': paginated_data['items'],
        'pagination': paginated_data['pagination'],
        'assessment_info': {
            'total_questions': len(riasec_questions),
            'categories': ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional'],
            'estimated_duration': '15-20 minutes',
            'instructions': 'Rate each statement based on how much you agree with it'
        }
    }
    
    logger.info(f"RIASEC questions retrieved, page {page}, category: {category or 'all'}")
    return APIResponse.success(response_data, "RIASEC questions retrieved successfully")


@assessment_bp.route('/riasec/submit', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
@handle_exceptions
def submit_riasec_assessment():
    """Submit RIASEC personality assessment"""
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Validate input data
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    validation_result = validate_assessment_response(data)
    
    if not validation_result['valid']:
        return APIResponse.validation_error(validation_result['errors'])
    
    responses = data.get('responses', {})
    
    if not responses:
        return APIResponse.validation_error({"responses": "Assessment responses are required"})
    
    # Calculate RIASEC scores
    riasec_scores = riasec_analyzer.calculate_riasec_scores(responses)
    
    # Analyze personality profile
    personality_analysis = riasec_analyzer.analyze_personality_profile(riasec_scores)
    
    # Create assessment result
    assessment_result = {
        'student_id': user_id,
        'assessment_id': 1,  # RIASEC assessment ID
        'responses': responses,
        'raw_scores': riasec_scores,
        'primary_result': personality_analysis.get('primary_type'),
        'detailed_analysis': personality_analysis,
        'status': 'completed',
        'completed_at': '2024-01-01T00:00:00Z'
    }
    
    # Save to database
    # result = AssessmentResult.from_dict(assessment_result)
    # db.session.add(result)
    # db.session.commit()
    
    response_data = {
        'assessment_result': assessment_result,
        'riasec_scores': riasec_scores,
        'personality_analysis': personality_analysis,
        'assessment_result_id': 1,  # result.id
        'primary_personality_type': personality_analysis.get('primary_type'),
        'career_suggestions': personality_analysis.get('career_suggestions', [])
    }
    
    logger.info(f"RIASEC assessment completed for user {user_id}")
    return APIResponse.success(response_data, "RIASEC assessment completed successfully", 201)


@assessment_bp.route('/riasec/results/<int:student_id>', methods=['GET'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def get_riasec_results(student_id):
    """Get RIASEC assessment results for a student"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only access your own assessment results")
    
    # Get assessment result from database
    # result = AssessmentResult.query.filter_by(student_id=student_id, assessment_id=1).first()
    # if not result:
    #     return APIResponse.not_found("RIASEC assessment result")
    
    # Mock assessment result
    assessment_result = {
        'id': 1,
        'student_id': student_id,
        'assessment_id': 1,
        'responses': {'q1': 4, 'q2': 3, 'q3': 5, 'q4': 2, 'q5': 4, 'q6': 5},
        'raw_scores': {
            'realistic': 60,
            'investigative': 80,
            'artistic': 40,
            'social': 50,
            'enterprising': 70,
            'conventional': 30
        },
        'primary_result': 'investigative',
        'detailed_analysis': {
            'primary_type': 'investigative',
            'secondary_type': 'enterprising',
            'personality_description': 'You have an investigative personality type with strong analytical and problem-solving skills.',
            'strengths': ['Analytical thinking', 'Problem solving', 'Research skills'],
            'career_suggestions': ['Data Scientist', 'Research Analyst', 'Software Engineer']
        },
        'status': 'completed',
        'created_at': '2024-01-01T00:00:00Z',
        'completed_at': '2024-01-01T00:15:00Z'
    }
    
    response_data = {
        'assessment_result': assessment_result,
        'interpretation': {
            'primary_type_description': 'Investigative types are analytical, intellectual, and introspective.',
            'career_fit_areas': ['Science', 'Technology', 'Research', 'Analysis'],
            'development_suggestions': [
                'Develop leadership skills to complement analytical abilities',
                'Consider roles that combine investigation with practical application'
            ]
        }
    }
    
    logger.info(f"RIASEC results retrieved for user {user_id}")
    return APIResponse.success(response_data, "RIASEC assessment results retrieved successfully")


@assessment_bp.route('/skills/evaluate', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def evaluate_technical_skills():
    """Evaluate technical skills through assessment"""
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Validate input data
    data = request.get_json()
    if not data:
        return APIResponse.validation_error({"request_body": "Request body is required"})
    
    skills_data = data.get('skills', {})
    assessment_type = data.get('assessment_type', 'self_evaluation')  # 'self_evaluation', 'quiz', 'practical'
    
    if not skills_data:
        return APIResponse.validation_error({"skills": "Skills data is required"})
    
    # Process skills evaluation
    skills_evaluation = {
        'technical_skills': {},
        'soft_skills': {},
        'overall_scores': {}
    }
    
    for skill, level in skills_data.items():
        if skill in ['Python', 'JavaScript', 'Java', 'SQL', 'Git', 'Docker']:
            skills_evaluation['technical_skills'][skill] = {
                'self_reported_level': level,
                'validated_level': min(level, 5),  # Cap at 5
                'proficiency': 'beginner' if level <= 2 else 'intermediate' if level <= 4 else 'advanced'
            }
        else:
            skills_evaluation['soft_skills'][skill] = {
                'self_reported_level': level,
                'validated_level': min(level, 5),
                'proficiency': 'beginner' if level <= 2 else 'intermediate' if level <= 4 else 'advanced'
            }
    
    # Calculate overall scores
    tech_scores = [s['validated_level'] for s in skills_evaluation['technical_skills'].values()]
    soft_scores = [s['validated_level'] for s in skills_evaluation['soft_skills'].values()]
    
    skills_evaluation['overall_scores'] = {
        'technical_average': sum(tech_scores) / len(tech_scores) if tech_scores else 0,
        'soft_skills_average': sum(soft_scores) / len(soft_scores) if soft_scores else 0,
        'overall_average': (sum(tech_scores + soft_scores)) / (len(tech_scores) + len(soft_scores)) if (tech_scores or soft_scores) else 0
    }
    
    response_data = {
        'skills_evaluation': skills_evaluation,
        'assessment_type': assessment_type,
        'recommendations': {
            'strengths': [skill for skill, data in skills_evaluation['technical_skills'].items() if data['validated_level'] >= 4],
            'areas_for_improvement': [skill for skill, data in skills_evaluation['technical_skills'].items() if data['validated_level'] <= 2],
            'suggested_learning_paths': ['Advanced Python Programming', 'System Design', 'Leadership Skills']
        },
        'evaluation_id': str(uuid.uuid4())
    }
    
    logger.info(f"Skills evaluation completed for user {user_id}, type: {assessment_type}")
    return APIResponse.success(response_data, "Skills evaluation completed successfully", 201)

@assessment_bp.route('/history/<int:student_id>', methods=['GET'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def get_assessment_history(student_id):
    """Get assessment history for a student"""
    # Verify user owns this profile
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only access your own assessment history")
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    assessment_type = request.args.get('type', None)  # Filter by assessment type
    
    # Get all assessment results for student
    # results = AssessmentResult.query.filter_by(student_id=student_id).all()
    
    # Mock assessment results
    all_assessments = [
        {
            'id': 1,
            'assessment_id': 1,
            'assessment_type': 'riasec',
            'assessment_name': 'RIASEC Personality Assessment',
            'primary_result': 'investigative',
            'status': 'completed',
            'score': 85,
            'duration_minutes': 15,
            'created_at': '2024-01-01T00:00:00Z',
            'completed_at': '2024-01-01T00:15:00Z'
        },
        {
            'id': 2,
            'assessment_id': 2,
            'assessment_type': 'skills',
            'assessment_name': 'Technical Skills Assessment',
            'primary_result': 'intermediate',
            'status': 'completed',
            'score': 78,
            'duration_minutes': 25,
            'created_at': '2024-01-02T00:00:00Z',
            'completed_at': '2024-01-02T00:25:00Z'
        },
        {
            'id': 3,
            'assessment_id': 3,
            'assessment_type': 'career_interest',
            'assessment_name': 'Career Interest Assessment',
            'primary_result': 'technology_focused',
            'status': 'in_progress',
            'score': None,
            'duration_minutes': None,
            'created_at': '2024-01-03T00:00:00Z',
            'completed_at': None
        }
    ]
    
    # Filter by assessment type if specified
    if assessment_type:
        filtered_assessments = [a for a in all_assessments if a['assessment_type'] == assessment_type]
    else:
        filtered_assessments = all_assessments
    
    # Paginate results
    paginated_data = paginate_response(filtered_assessments, page, per_page)
    
    # Calculate summary statistics
    completed_assessments = [a for a in filtered_assessments if a['status'] == 'completed']
    summary_stats = {
        'total_assessments': len(filtered_assessments),
        'completed_assessments': len(completed_assessments),
        'in_progress_assessments': len([a for a in filtered_assessments if a['status'] == 'in_progress']),
        'average_score': sum(a['score'] for a in completed_assessments if a['score']) / len(completed_assessments) if completed_assessments else 0,
        'total_time_spent': sum(a['duration_minutes'] for a in completed_assessments if a['duration_minutes']) or 0
    }
    
    response_data = {
        'assessment_history': paginated_data['items'],
        'pagination': paginated_data['pagination'],
        'summary_statistics': summary_stats,
        'available_types': ['riasec', 'skills', 'career_interest', 'personality']
    }
    
    logger.info(f"Assessment history retrieved for user {user_id}, type: {assessment_type or 'all'}")
    return APIResponse.success(response_data, "Assessment history retrieved successfully")

@assessment_bp.route('/available', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_available_assessments():
    """Get available assessments"""
    # Get available assessments from database
    # assessments = Assessment.query.filter_by(is_active=True).all()
    
    available_assessments = [
        {
            'id': 1,
            'name': 'RIASEC Personality Assessment',
            'description': 'Discover your personality type and career preferences',
            'assessment_type': 'riasec',
            'question_count': 60,
            'estimated_duration': 15,
            'difficulty_level': 'beginner',
            'categories': ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional'],
            'is_active': True
        },
        {
            'id': 2,
            'name': 'Technical Skills Assessment',
            'description': 'Evaluate your technical and programming skills',
            'assessment_type': 'skills',
            'question_count': 40,
            'estimated_duration': 20,
            'difficulty_level': 'intermediate',
            'categories': ['programming', 'databases', 'web_development', 'devops'],
            'is_active': True
        },
        {
            'id': 3,
            'name': 'Career Interest Assessment',
            'description': 'Explore your career interests and preferences',
            'assessment_type': 'career_interest',
            'question_count': 30,
            'estimated_duration': 10,
            'difficulty_level': 'beginner',
            'categories': ['interests', 'values', 'work_environment'],
            'is_active': True
        },
        {
            'id': 4,
            'name': 'Soft Skills Assessment',
            'description': 'Assess your communication, leadership, and interpersonal skills',
            'assessment_type': 'soft_skills',
            'question_count': 35,
            'estimated_duration': 12,
            'difficulty_level': 'beginner',
            'categories': ['communication', 'leadership', 'teamwork', 'problem_solving'],
            'is_active': True
        }
    ]
    
    # Filter by type if specified
    assessment_type = request.args.get('type', None)
    if assessment_type:
        available_assessments = [a for a in available_assessments if a['assessment_type'] == assessment_type]
    
    response_data = {
        'available_assessments': available_assessments,
        'total_count': len(available_assessments),
        'assessment_types': ['riasec', 'skills', 'career_interest', 'soft_skills']
    }
    
    logger.info(f"Available assessments retrieved, type filter: {assessment_type or 'all'}")
    return APIResponse.success(response_data, "Available assessments retrieved successfully")
