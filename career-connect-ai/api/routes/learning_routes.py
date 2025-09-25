"""
Learning path API routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.limiter import limiter
from services.learning_path_generator import LearningPathGenerator
from services.skill_gap_analyzer import SkillGapAnalyzer
from models.student import Student
from utils.logger import get_logger
from utils.response_formatter import APIResponse, handle_exceptions
import json

logger = get_logger(__name__)

# Create blueprint
learning_bp = Blueprint('learning', __name__, url_prefix='/api/v1/learning')

# Rate limiter is initialized in app.py

# Initialize services
learning_generator = LearningPathGenerator()
skill_analyzer = SkillGapAnalyzer()

@learning_bp.route('/path/generate', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def generate_learning_path():
    """Generate personalized learning path for a target career"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        career_id = data.get('career_id')
        if not career_id:
            return APIResponse.validation_error({'career_id': 'career_id is required'})

        # Get student profile
        # student = Student.query.get(user_id)
        # if not student:
        #     return jsonify({'error': 'Profile not found'}), 404
        
        # Mock student profile
        student_profile = {
            'id': user_id,
            'name': 'John Doe',
            'skills': ['Python', 'JavaScript', 'Communication'],
            'interests': ['Technology', 'Data Science'],
            'career_goals': ['Software Engineer', 'Data Scientist'],
            'learning_style': 'visual',
            'riasec_scores': {
                'realistic': 60,
                'investigative': 80,
                'artistic': 40,
                'social': 50,
                'enterprising': 70,
                'conventional': 30
            }
        }
        
        # Get career information
        # career = Career.query.get(career_id)
        # if not career:
        #     return jsonify({'error': 'Career not found'}), 404
        
        # Mock career data
        target_career = {
            'id': career_id,
            'title': 'Software Engineer',
            'description': 'Develop software applications and systems',
            'required_skills': ['Programming', 'Problem Solving', 'Communication', 'Git', 'Testing'],
            'education_requirements': 'Bachelor\'s degree',
            'experience_required': '2-5 years'
        }
        
        # Get learning preferences from request body
        learning_preferences = {
            'preferred_methods': data.get('methods', ['online_courses']),
            'time_commitment': data.get('time_commitment', '10_hours_week'),
            'budget': data.get('budget', 'free_to_low_cost'),
            'certification_preferred': bool(data.get('certification', False))
        }
        
        # Generate learning path
        learning_path = learning_generator.generate_learning_path(
            student_profile, target_career, learning_preferences
        )
        
        return APIResponse.success({'learning_path': learning_path}, "Learning path generated successfully")
        
    except Exception as e:
        logger.error(f"Error getting learning path: {str(e)}")
        return APIResponse.error("Failed to get learning path", {"details": str(e)}, 500)

@learning_bp.route('/progress/update', methods=['POST'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def update_learning_progress():
    """Update learning progress"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return APIResponse.validation_error({'request_body': 'Request body is required'})
        learning_path_id = data.get('learning_path_id')
        progress_data = data.get('progress_data', {})
        if not learning_path_id:
            return APIResponse.validation_error({'learning_path_id': 'Learning path ID is required'})
        
        # Update learning progress
        # progress = LearningProgress.query.filter_by(
        #     student_id=user_id, learning_path_id=learning_path_id
        # ).first()
        
        # if not progress:
        #     return jsonify({'error': 'Learning path not found'}), 404
        
        # Update progress data
        # progress.progress_data = progress_data
        # progress.last_updated = datetime.now()
        # db.session.commit()
        
        return APIResponse.success({'progress_data': progress_data}, "Learning progress updated successfully")
        
    except Exception as e:
        logger.error(f"Error updating learning progress: {str(e)}")
        return APIResponse.error("Failed to update learning progress", {"details": str(e)}, 500)

@learning_bp.route('/resources/<int:career_id>', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_learning_resources(career_id):
    """Get learning resources for a specific career"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get query parameters
        resource_type = request.args.get('type', 'all')  # 'courses', 'books', 'videos', 'all'
        difficulty = request.args.get('difficulty', 'all')  # 'beginner', 'intermediate', 'advanced', 'all'
        free_only = request.args.get('free_only', 'false').lower() == 'true'
        
        # Get career information
        # career = Career.query.get(career_id)
        # if not career:
        #     return jsonify({'error': 'Career not found'}), 404
        
        # Mock career data
        career_data = {
            'id': career_id,
            'title': 'Software Engineer',
            'required_skills': ['Programming', 'Problem Solving', 'Communication', 'Git', 'Testing']
        }
        
        # Generate learning resources
        learning_resources = {
            'courses': [
                {
                    'id': 1,
                    'title': 'Complete Python Programming Course',
                    'provider': 'Coursera',
                    'duration': '4 weeks',
                    'difficulty': 'beginner',
                    'cost': 'free',
                    'url': 'https://example.com/python-course',
                    'skills_covered': ['Python', 'Programming']
                },
                {
                    'id': 2,
                    'title': 'Software Engineering Fundamentals',
                    'provider': 'edX',
                    'duration': '8 weeks',
                    'difficulty': 'intermediate',
                    'cost': '$99',
                    'url': 'https://example.com/se-course',
                    'skills_covered': ['Software Engineering', 'Problem Solving']
                }
            ],
            'books': [
                {
                    'id': 1,
                    'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                    'author': 'Robert C. Martin',
                    'pages': 464,
                    'difficulty': 'intermediate',
                    'cost': '$35',
                    'url': 'https://example.com/clean-code-book',
                    'skills_covered': ['Code Quality', 'Best Practices']
                }
            ],
            'videos': [
                {
                    'id': 1,
                    'title': 'Introduction to Software Engineering',
                    'provider': 'YouTube',
                    'duration': '45 minutes',
                    'difficulty': 'beginner',
                    'cost': 'free',
                    'url': 'https://example.com/se-video',
                    'skills_covered': ['Software Engineering', 'Overview']
                }
            ],
            'tools': [
                {
                    'id': 1,
                    'title': 'Git Version Control',
                    'type': 'Development Tool',
                    'cost': 'free',
                    'url': 'https://git-scm.com/',
                    'skills_covered': ['Version Control', 'Git']
                }
            ]
        }
        
        # Filter resources based on parameters
        if resource_type != 'all':
            learning_resources = {resource_type: learning_resources.get(resource_type, [])}
        
        if free_only:
            for resource_category in learning_resources:
                learning_resources[resource_category] = [
                    resource for resource in learning_resources[resource_category]
                    if resource.get('cost', '').lower() in ['free', '0', '$0']
                ]
        
        return APIResponse.success({'learning_resources': learning_resources}, "Learning resources retrieved successfully")
        
    except Exception as e:
        logger.error(f"Error getting learning resources: {str(e)}")
        return APIResponse.error("Failed to get learning resources", {"details": str(e)}, 500)

@learning_bp.route('/skill-development', methods=['POST'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def create_skill_development_path():
    """Create focused skill development path"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Validate input data
        data = request.get_json()
        
        skill = data.get('skill')
        current_level = data.get('current_level', 'beginner')
        target_level = data.get('target_level', 'intermediate')
        learning_style = data.get('learning_style', 'visual')
        
        if not skill:
            return APIResponse.validation_error({'skill': 'Skill is required'})
        
        # Create skill development path
        skill_path = learning_generator.create_skill_development_path(
            skill, current_level, target_level, learning_style
        )
        
        return APIResponse.success({'skill_development_path': skill_path}, "Skill development path created successfully", 201)
        
    except Exception as e:
        logger.error(f"Error creating skill development path: {str(e)}")
        return APIResponse.error("Failed to create skill development path", {"details": str(e)}, 500)

@learning_bp.route('/skill-progress', methods=['POST'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def track_skill_progress():
    """Track progress in skill development"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Validate input data
        data = request.get_json()
        
        skill = data.get('skill')
        progress_data = data.get('progress_data', {})
        
        if not skill:
            return jsonify({'error': 'Skill is required'}), 400
        
        # Track skill progress
        progress_tracking = skill_analyzer.track_skill_progress(skill, progress_data)
        
        return APIResponse.success({'skill_progress_tracking': progress_tracking}, "Skill progress tracked successfully")
        
    except Exception as e:
        logger.error(f"Error tracking skill progress: {str(e)}")
        return APIResponse.error("Failed to track skill progress", {"details": str(e)}, 500)

@learning_bp.route('/milestones', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_learning_milestones():
    """Get learning milestones for a student"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get query parameters
        status = request.args.get('status', 'all')  # 'completed', 'pending', 'all'
        category = request.args.get('category', 'all')  # 'skill', 'course', 'project', 'all'
        
        # Get student's learning milestones
        # milestones = LearningMilestone.query.filter_by(student_id=user_id).all()
        
        # Mock learning milestones
        milestones = [
            {
                'id': 1,
                'title': 'Complete Python Basics Course',
                'category': 'course',
                'status': 'completed',
                'target_date': '2024-01-15',
                'completed_date': '2024-01-10',
                'description': 'Learn fundamental Python programming concepts',
                'skills_gained': ['Python', 'Programming']
            },
            {
                'id': 2,
                'title': 'Build First Web Application',
                'category': 'project',
                'status': 'pending',
                'target_date': '2024-02-01',
                'completed_date': None,
                'description': 'Create a simple web application using Python and Flask',
                'skills_gained': ['Web Development', 'Flask', 'HTML', 'CSS']
            },
            {
                'id': 3,
                'title': 'Master Git Version Control',
                'category': 'skill',
                'status': 'in_progress',
                'target_date': '2024-01-20',
                'completed_date': None,
                'description': 'Become proficient in Git commands and workflows',
                'skills_gained': ['Git', 'Version Control']
            }
        ]
        
        # Filter milestones based on parameters
        if status != 'all':
            milestones = [milestone for milestone in milestones if milestone['status'] == status]
        
        if category != 'all':
            milestones = [milestone for milestone in milestones if milestone['category'] == category]
        
        return APIResponse.success({'learning_milestones': milestones}, "Learning milestones retrieved successfully")
        
    except Exception as e:
        logger.error(f"Error getting learning milestones: {str(e)}")
        return APIResponse.error("Failed to get learning milestones", {"details": str(e)}, 500)

@learning_bp.route('/recommendations', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_learning_recommendations():
    """Get personalized learning recommendations"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get student profile
        # student = Student.query.get(user_id)
        # if not student:
        #     return jsonify({'error': 'Profile not found'}), 404
        
        # Mock student profile
        student_profile = {
            'id': user_id,
            'skills': ['Python', 'JavaScript', 'Communication'],
            'interests': ['Technology', 'Data Science'],
            'career_goals': ['Software Engineer', 'Data Scientist'],
            'learning_style': 'visual'
        }
        
        # Get query parameters
        focus_area = request.args.get('focus_area', 'all')  # 'technical', 'soft', 'career', 'all'
        time_available = request.args.get('time_available', '10_hours_week')
        
        # Generate learning recommendations
        recommendations = {
            'immediate_actions': [
                'Complete Python intermediate course',
                'Practice coding problems daily',
                'Join programming community'
            ],
            'short_term_goals': [
                'Build portfolio project',
                'Learn version control with Git',
                'Complete data structures course'
            ],
            'long_term_goals': [
                'Master software engineering principles',
                'Gain industry experience',
                'Build professional network'
            ],
            'recommended_courses': [
                {
                    'title': 'Advanced Python Programming',
                    'provider': 'Coursera',
                    'duration': '6 weeks',
                    'difficulty': 'intermediate',
                    'relevance_score': 0.9
                }
            ],
            'skill_gaps': [
                'Database management',
                'System design',
                'Testing methodologies'
            ]
        }
        
        return APIResponse.success({'learning_recommendations': recommendations}, "Learning recommendations retrieved successfully")

    except Exception as e:
        logger.error(f"Error getting learning recommendations: {str(e)}")
        return APIResponse.error("Failed to get learning recommendations", {"details": str(e)}, 500)

@learning_bp.route('/progress/<int:student_id>', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_learning_progress(student_id: int):
    """Get learning progress for a student"""
    user_id = get_jwt_identity()
    if student_id != user_id:
        return APIResponse.forbidden("You can only access your own learning progress")
    # Mock progress data
    progress = {
        'learning_path_id': 1001,
        'completed_modules': 5,
        'total_modules': 12,
        'percentage_complete': 41.7,
        'last_updated': '2024-01-15T10:30:00Z'
    }
    return APIResponse.success({'progress': progress}, "Learning progress retrieved successfully")
