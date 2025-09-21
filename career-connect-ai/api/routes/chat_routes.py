"""
Chat interface API routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.limiter import limiter
from api.validators.chat_validators import validate_chat_message
from services.chat_service import ChatService
from models.conversation import Conversation, Message
from utils.logger import get_logger
from utils.response_formatter import APIResponse, handle_exceptions
import json
import uuid

logger = get_logger(__name__)

# Create blueprint
chat_bp = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

# Rate limiter is initialized in app.py

# Initialize services
chat_service = ChatService()

@chat_bp.route('/session', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def create_chat_session():
    """Create a new chat session"""
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
        
        # Get initial context from request
        data = request.get_json() or {}
        initial_context = data.get('initial_context', {})
        
        # Create chat session
        session_id = chat_service.create_chat_session(student_profile, initial_context)
        
        return APIResponse.success({
            'session_id': session_id,
            'student_profile': student_profile
        }, "Chat session created successfully", 201)
        
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        return APIResponse.error("Failed to create chat session", {"details": str(e)}, 500)

@chat_bp.route('/message', methods=['POST'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def send_message():
    """Send a message to the AI counselor"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Validate input data
        data = request.get_json()
        validation_result = validate_chat_message(data)
        
        if not validation_result['valid']:
            return APIResponse.validation_error(validation_result['errors'])
        
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        if not session_id:
            return APIResponse.validation_error({'session_id': 'Session ID is required'})
        
        # Process chat message
        response_data = chat_service.process_chat_message(message, session_id)
        
        return APIResponse.success({'response_data': response_data}, "Message processed successfully")
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return APIResponse.error("Failed to send message", {"details": str(e)}, 500)

@chat_bp.route('/history/<int:student_id>', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_chat_history_by_student(student_id):
    """Get chat history for a session"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Authorization check
        if student_id != user_id:
            return APIResponse.forbidden("You can only access your own chat history")

        # Get query parameters
        limit = request.args.get('limit', None, type=int)
        
        # Service method may differ; for now, aggregate from sessions
        history = chat_service.get_user_chat_history(student_id, limit) if hasattr(chat_service, 'get_user_chat_history') else []
        
        return APIResponse.success({'chat_history': history}, "Chat history retrieved successfully")
        
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return APIResponse.error("Failed to get chat history", {"details": str(e)}, 500)

@chat_bp.route('/session/<session_id>/end', methods=['POST'])
@limiter.limit("20 per minute")
@jwt_required()
@handle_exceptions
def end_chat_session(session_id):
    """End a chat session with feedback"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get feedback from request
        data = request.get_json() or {}
        feedback = data.get('feedback', {})
        
        # End chat session
        session_summary = chat_service.end_chat_session(session_id, feedback)
        
        return APIResponse.success({'session_summary': session_summary}, "Chat session ended successfully")
        
    except Exception as e:
        logger.error(f"Error ending chat session: {str(e)}")
        return APIResponse.error("Failed to end chat session", {"details": str(e)}, 500)

@chat_bp.route('/session/<session_id>/sentiment', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def analyze_conversation_sentiment(session_id):
    """Analyze conversation sentiment and engagement"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Analyze conversation sentiment
        sentiment_analysis = chat_service.analyze_conversation_sentiment(session_id)
        
        return APIResponse.success({'sentiment_analysis': sentiment_analysis}, "Conversation sentiment analyzed successfully")
        
    except Exception as e:
        logger.error(f"Error analyzing conversation sentiment: {str(e)}")
        return APIResponse.error("Failed to analyze conversation sentiment", {"details": str(e)}, 500)

@chat_bp.route('/session/<session_id>/summary', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_conversation_summary(session_id):
    """Get comprehensive conversation summary"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Generate conversation summary
        summary = chat_service.generate_conversation_summary(session_id)
        
        return APIResponse.success({'conversation_summary': summary}, "Conversation summary generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating conversation summary: {str(e)}")
        return APIResponse.error("Failed to generate conversation summary", {"details": str(e)}, 500)

@chat_bp.route('/sessions', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def get_user_chat_sessions():
    """Get all chat sessions for a user"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', 'all')
        
        # Get user's chat sessions
        # sessions = Conversation.query.filter_by(student_id=user_id).order_by(Conversation.last_activity.desc()).limit(limit).all()
        
        # Mock chat sessions
        chat_sessions = [
            {
                'id': 1,
                'session_id': 'session_1',
                'conversation_type': 'chat',
                'title': 'Career Guidance Session',
                'status': 'completed',
                'message_count': 15,
                'started_at': '2024-01-01T10:00:00Z',
                'ended_at': '2024-01-01T10:30:00Z',
                'topics_discussed': ['career_planning', 'skill_development']
            },
            {
                'id': 2,
                'session_id': 'session_2',
                'conversation_type': 'chat',
                'title': 'Assessment Discussion',
                'status': 'active',
                'message_count': 8,
                'started_at': '2024-01-02T14:00:00Z',
                'ended_at': None,
                'topics_discussed': ['assessment', 'personality']
            }
        ]
        
        # Filter by status if specified
        if status != 'all':
            chat_sessions = [session for session in chat_sessions if session['status'] == status]
        
        return APIResponse.success({'chat_sessions': chat_sessions}, "Chat sessions retrieved successfully")
        
    except Exception as e:
        logger.error(f"Error getting user chat sessions: {str(e)}")
        return APIResponse.error("Failed to get chat sessions", {"details": str(e)}, 500)

@chat_bp.route('/quick-replies', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required()
@handle_exceptions
def get_quick_replies():
    """Get suggested conversation starters"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Get user's profile to personalize suggestions
        # student = Student.query.get(user_id)
        
        # Mock suggestions based on common career guidance topics
        suggestions = [
            {
                'category': 'Career Exploration',
                'suggestions': [
                    "What careers match my personality?",
                    "How do I choose the right career path?",
                    "What skills do I need to develop?"
                ]
            },
            {
                'category': 'Assessment',
                'suggestions': [
                    "Help me understand my RIASEC results",
                    "What do my personality scores mean?",
                    "How can I improve my skills?"
                ]
            },
            {
                'category': 'Learning',
                'suggestions': [
                    "Create a learning plan for me",
                    "What resources should I use?",
                    "How do I track my progress?"
                ]
            },
            {
                'category': 'Mentorship',
                'suggestions': [
                    "Find me a mentor",
                    "What should I look for in a mentor?",
                    "How do I approach potential mentors?"
                ]
            }
        ]
        
        return APIResponse.success({'quick_replies': suggestions}, "Quick replies retrieved successfully")
        
    except Exception as e:
        logger.error(f"Error getting chat suggestions: {str(e)}")
        return APIResponse.error("Failed to get chat suggestions", {"details": str(e)}, 500)

@chat_bp.route('/feedback', methods=['POST'])
@limiter.limit("30 per minute")
@jwt_required()
@handle_exceptions
def submit_chat_feedback():
    """Submit feedback for a chat message or session"""
    try:
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Validate input data
        data = request.get_json()
        
        message_id = data.get('message_id')
        session_id = data.get('session_id')
        feedback_type = data.get('feedback_type', 'general')  # 'helpful', 'not_helpful', 'general'
        rating = data.get('rating')  # 1-5 scale
        comments = data.get('comments', '')
        
        if not (message_id or session_id):
            return APIResponse.validation_error({'message_id|session_id': 'Either message_id or session_id is required'})
        
        # Create feedback record
        feedback_data = {
            'student_id': user_id,
            'message_id': message_id,
            'session_id': session_id,
            'feedback_type': feedback_type,
            'rating': rating,
            'comments': comments,
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        # Save feedback to database
        # feedback = ChatFeedback.from_dict(feedback_data)
        # db.session.add(feedback)
        # db.session.commit()
        
        return APIResponse.success({'feedback_id': 1}, "Feedback submitted successfully", 201)


@chat_bp.route('/context/reset', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required()
@handle_exceptions
def reset_chat_context():
    """Reset conversation context for the current user"""
    user_id = get_jwt_identity()
    # Reset via service if available
    result = chat_service.reset_context(user_id) if hasattr(chat_service, 'reset_context') else {'status': 'reset'}
    return APIResponse.success({'result': result}, "Chat context reset successfully")
