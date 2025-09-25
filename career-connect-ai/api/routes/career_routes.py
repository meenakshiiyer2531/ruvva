"""
Career discovery API routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.limiter import limiter
from services.career_discovery import CareerDiscoveryService
from models.career import Career, CareerRecommendation
from utils.logger import get_logger
from utils.response_formatter import APIResponse, handle_exceptions
import json

logger = get_logger(__name__)

# Create blueprint
career_bp = Blueprint('career', __name__, url_prefix='/api/v1/careers')

# Rate limiter is initialized in app.py

# Initialize services
career_discovery = CareerDiscoveryService()

@career_bp.route('/discover', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def discover_careers():
    """Discover careers based on profile and preferences"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    filters = data.get('filters', {})
    limit = data.get('limit', 10)

    # Mock student profile
    student_profile = {
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

    # Mock career database
    career_database = [
            {
                'id': 1,
                'title': 'Software Engineer',
                'description': 'Develop software applications and systems',
                'category': 'Technology',
                'industry': 'Software',
                'required_skills': ['Programming', 'Problem Solving', 'Communication'],
                'riasec_requirements': {
                    'realistic': 40,
                    'investigative': 80,
                    'artistic': 30,
                    'social': 40,
                    'enterprising': 60,
                    'conventional': 50
                },
                'salary': {'median': 90000, 'min': 60000, 'max': 120000},
                'growth_rate': 'high'
            },
            {
                'id': 2,
                'title': 'Data Scientist',
                'description': 'Analyze data to extract insights and build models',
                'category': 'Technology',
                'industry': 'Data Science',
                'required_skills': ['Statistics', 'Machine Learning', 'Python'],
                'riasec_requirements': {
                    'realistic': 30,
                    'investigative': 90,
                    'artistic': 20,
                    'social': 30,
                    'enterprising': 50,
                    'conventional': 60
                },
                'salary': {'median': 95000, 'min': 70000, 'max': 130000},
                'growth_rate': 'high'
            }
    ]

    recommendations = career_discovery.discover_careers_by_profile(student_profile)

    return APIResponse.success({
        'career_recommendations': recommendations[:limit]
    }, "Career discovery completed successfully")

@career_bp.route('/search', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def search_careers():
    """Search careers based on query and filters"""
    try:
        # Get query parameters
        query = request.args.get('q', '')
        filters = request.args.get('filters', {})
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return APIResponse.validation_error({'q': 'Search query is required'})
        
        # Get career database
        # careers = Career.query.filter_by(is_active=True).all()
        
        # Mock career database
        career_database = [
            {
                'id': 1,
                'title': 'Software Engineer',
                'description': 'Develop software applications and systems',
                'category': 'Technology',
                'industry': 'Software',
                'required_skills': ['Programming', 'Problem Solving', 'Communication']
            },
            {
                'id': 2,
                'title': 'Data Scientist',
                'description': 'Analyze data to extract insights and build models',
                'category': 'Technology',
                'industry': 'Data Science',
                'required_skills': ['Statistics', 'Machine Learning', 'Python']
            },
            {
                'id': 3,
                'title': 'Product Manager',
                'description': 'Manage product development and strategy',
                'category': 'Business',
                'industry': 'Technology',
                'required_skills': ['Leadership', 'Strategy', 'Communication']
            }
        ]
        
        # Search careers
        # Use mock search results since method doesn't exist
        search_results = career_database[:3]  # Return first 3 careers as mock results

        return APIResponse.success({'search_results': search_results[:limit]}, "Career search successful")

    except Exception as e:
        logger.error(f"Error searching careers: {str(e)}")
        return APIResponse.error("Failed to search careers", {"details": str(e)}, 500)

@career_bp.route('/<int:career_id>/details', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_career_details(career_id):
    """Get detailed information about a specific career"""
    try:
        # Get career from database
        # career = Career.query.get(career_id)
        # if not career:
        #     return jsonify({'error': 'Career not found'}), 404
        
        # Mock career data
        career_data = {
            'id': career_id,
            'title': 'Software Engineer',
            'description': 'Develop software applications and systems',
            'category': 'Technology',
            'industry': 'Software',
            'job_level': 'mid',
            'education_requirements': 'Bachelor\'s degree',
            'experience_required': '2-5 years',
            'required_skills': ['Programming', 'Problem Solving', 'Communication'],
            'preferred_skills': ['Python', 'JavaScript', 'Git'],
            'certifications': ['AWS Certified Developer'],
            'salary': {'min': 60000, 'max': 120000, 'median': 90000},
            'benefits': ['Health Insurance', '401k', 'Flexible Hours'],
            'workplace_type': 'hybrid',
            'work_schedule': 'full-time',
            'travel_required': False,
            'remote_possible': True,
            'demand_level': 'high',
            'growth_rate': 'high',
            'competition_level': 'medium',
            'job_security': 'high',
            'riasec_requirements': {
                'realistic': 40,
                'investigative': 80,
                'artistic': 30,
                'social': 40,
                'enterprising': 60,
                'conventional': 50
            },
            'technology_impact': 'high',
            'automation_risk': 'low',
            'future_outlook': 'positive'
        }
        
        # Get student profile for personalized analysis
        user_id = get_jwt_identity()
        student_profile = {
            'id': user_id,
            'skills': ['Python', 'JavaScript', 'Communication'],
            'interests': ['Technology', 'Data Science'],
            'riasec_scores': {
                'realistic': 60,
                'investigative': 80,
                'artistic': 40,
                'social': 50,
                'enterprising': 70,
                'conventional': 30
            }
        }
        
        # Explore career details
        # Use mock career details
        career_details = {
            'id': career_id,
            'title': career_data['title'],
            'description': career_data['description'],
            'skills': career_data.get('required_skills', []),
            'salary': career_data.get('salary', {}),
            'growth_outlook': career_data.get('growth_rate', 'stable')
        }

        return APIResponse.success({'career_details': career_details}, "Career details retrieved successfully")

    except Exception as e:
        logger.error(f"Error getting career details: {str(e)}")
        return APIResponse.error("Failed to get career details", {"details": str(e)}, 500)

@career_bp.route('/trending', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_career_trends():
    """Get current career trends and market insights"""
    try:
        # Get query parameters
        categories = request.args.get('categories', '').split(',') if request.args.get('categories') else None
        
        # Get career trends
        trends = career_discovery.get_trending_careers('1year')

        return APIResponse.success({'career_trends': trends}, "Trending careers retrieved successfully")

    except Exception as e:
        logger.error(f"Error getting career trends: {str(e)}")
        return APIResponse.error("Failed to get career trends", {"details": str(e)}, 500)

@career_bp.route('/compare', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def compare_careers():
    """Compare multiple careers side by side"""
    try:
        data = request.get_json()
        career_ids = data.get('career_ids', [])
        
        if len(career_ids) < 2:
            return APIResponse.validation_error({'career_ids': 'At least 2 careers required for comparison'})
        
        if len(career_ids) > 5:
            return APIResponse.validation_error({'career_ids': 'Maximum 5 careers allowed for comparison'})
        
        # Get career database
        # careers = Career.query.filter(Career.id.in_(career_ids)).all()
        
        # Mock career database
        career_database = [
            {
                'id': 1,
                'title': 'Software Engineer',
                'description': 'Develop software applications and systems',
                'category': 'Technology',
                'industry': 'Software',
                'required_skills': ['Programming', 'Problem Solving', 'Communication'],
                'salary': {'median': 90000},
                'growth_rate': 'high',
                'work_life_balance': 'good',
                'job_security': 'high'
            },
            {
                'id': 2,
                'title': 'Data Scientist',
                'description': 'Analyze data to extract insights and build models',
                'category': 'Technology',
                'industry': 'Data Science',
                'required_skills': ['Statistics', 'Machine Learning', 'Python'],
                'salary': {'median': 95000},
                'growth_rate': 'high',
                'work_life_balance': 'good',
                'job_security': 'high'
            }
        ]
        
        # Compare careers
        # Mock career comparison
        comparison = {
            'careers': career_database[:len(career_ids)],
            'comparison_factors': ['salary', 'growth_rate', 'job_security'],
            'recommendations': 'Based on comparison, consider your interests and skills.'
        }

        return APIResponse.success({'career_comparison': comparison}, "Career comparison successful")

    except Exception as e:
        logger.error(f"Error comparing careers: {str(e)}")
        return APIResponse.error("Failed to compare careers", {"details": str(e)}, 500)

@career_bp.route('/<int:career_id>/similar', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_similar_careers(career_id: int):
    """Find similar careers to a given career"""
    # Mock list; in real implementation search similar by skills/category
    similar = [
        {
            'id': 10,
            'title': 'Backend Engineer',
            'similarity_score': 0.86
        },
        {
            'id': 11,
            'title': 'ML Engineer',
            'similarity_score': 0.82
        }
    ]
    return APIResponse.success({'similar_careers': similar, 'career_id': career_id}, "Similar careers retrieved successfully")

@career_bp.route('/fit/<int:career_id>', methods=['POST'])
@jwt_required()
def analyze_career_fit(career_id):
    """Analyze fit for a specific career"""
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
            'riasec_scores': {
                'realistic': 60,
                'investigative': 80,
                'artistic': 40,
                'social': 50,
                'enterprising': 70,
                'conventional': 30
            }
        }
        
        # Get career database
        # careers = Career.query.filter_by(is_active=True).all()
        
        # Mock career database
        career_database = [
            {
                'id': career_id,
                'title': 'Software Engineer',
                'description': 'Develop software applications and systems',
                'required_skills': ['Programming', 'Problem Solving', 'Communication'],
                'riasec_requirements': {
                    'realistic': 40,
                    'investigative': 80,
                    'artistic': 30,
                    'social': 40,
                    'enterprising': 60,
                    'conventional': 50
                }
            }
        ]
        
        # Mock career fit analysis
        fit_analysis = {
            'overall_fit': 85,
            'skill_match': 90,
            'interest_match': 80,
            'personality_match': 85,
            'recommendations': ['Develop leadership skills', 'Gain more experience in data analysis']
        }
        
        return jsonify({
            'career_fit_analysis': fit_analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing career fit: {str(e)}")
        return jsonify({'error': 'Failed to analyze career fit'}), 500

@career_bp.route('/transitions', methods=['POST'])
@jwt_required()
def suggest_career_transitions():
    """Suggest career transitions from current career"""
    try:
        data = request.get_json()
        current_career = data.get('current_career')
        
        if not current_career:
            return jsonify({'error': 'Current career is required'}), 400
        
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
            'riasec_scores': {
                'realistic': 60,
                'investigative': 80,
                'artistic': 40,
                'social': 50,
                'enterprising': 70,
                'conventional': 30
            }
        }
        
        # Get career database
        # careers = Career.query.filter_by(is_active=True).all()
        
        # Mock career database
        career_database = [
            {
                'id': 1,
                'title': 'Software Engineer',
                'description': 'Develop software applications and systems',
                'required_skills': ['Programming', 'Problem Solving', 'Communication']
            },
            {
                'id': 2,
                'title': 'Data Scientist',
                'description': 'Analyze data to extract insights and build models',
                'required_skills': ['Statistics', 'Machine Learning', 'Python']
            },
            {
                'id': 3,
                'title': 'Product Manager',
                'description': 'Manage product development and strategy',
                'required_skills': ['Leadership', 'Strategy', 'Communication']
            }
        ]
        
        # Mock career transitions
        transitions = {
            'recommended_transitions': [
                {'career': 'Senior Data Scientist', 'timeline': '2-3 years', 'requirements': ['Advanced ML skills']},
                {'career': 'Product Manager', 'timeline': '1-2 years', 'requirements': ['Business acumen', 'Communication skills']}
            ],
            'transition_plan': 'Focus on developing leadership and strategic thinking skills'
        }
        
        return jsonify({
            'career_transitions': transitions
        }), 200
        
    except Exception as e:
        logger.error(f"Error suggesting career transitions: {str(e)}")
        return jsonify({'error': 'Failed to suggest career transitions'}), 500
