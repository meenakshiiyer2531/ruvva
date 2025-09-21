"""
Chat input validation
"""

from typing import Dict, List, Any

def validate_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate chat message data"""
    errors = []
    
    # Required fields
    if not data.get('message'):
        errors.append("Message is required")
    
    message = data.get('message', '')
    if not isinstance(message, str):
        errors.append("Message must be a string")
    elif len(message.strip()) == 0:
        errors.append("Message cannot be empty")
    elif len(message) > 2000:
        errors.append("Message cannot exceed 2000 characters")
    
    # Session ID validation
    session_id = data.get('session_id')
    if not session_id:
        errors.append("Session ID is required")
    elif not isinstance(session_id, str):
        errors.append("Session ID must be a string")
    elif len(session_id.strip()) == 0:
        errors.append("Session ID cannot be empty")
    
    # Message type validation
    message_type = data.get('message_type', 'text')
    valid_types = ['text', 'image', 'file', 'assessment']
    if message_type not in valid_types:
        errors.append(f"Message type must be one of: {', '.join(valid_types)}")
    
    # Context validation
    context = data.get('context')
    if context is not None and not isinstance(context, dict):
        errors.append("Context must be a dictionary")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_chat_session_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate chat session creation data"""
    errors = []
    
    # Initial context validation
    initial_context = data.get('initial_context', {})
    if not isinstance(initial_context, dict):
        errors.append("Initial context must be a dictionary")
    
    # Session type validation
    session_type = data.get('session_type', 'chat')
    valid_types = ['chat', 'assessment', 'mentor', 'learning']
    if session_type not in valid_types:
        errors.append(f"Session type must be one of: {', '.join(valid_types)}")
    
    # Preferences validation
    preferences = data.get('preferences', {})
    if not isinstance(preferences, dict):
        errors.append("Preferences must be a dictionary")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_chat_feedback(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate chat feedback data"""
    errors = []
    
    # At least one identifier required
    message_id = data.get('message_id')
    session_id = data.get('session_id')
    
    if not message_id and not session_id:
        errors.append("Either message_id or session_id is required")
    
    # Message ID validation
    if message_id and not isinstance(message_id, str):
        errors.append("Message ID must be a string")
    
    # Session ID validation
    if session_id and not isinstance(session_id, str):
        errors.append("Session ID must be a string")
    
    # Feedback type validation
    feedback_type = data.get('feedback_type', 'general')
    valid_types = ['helpful', 'not_helpful', 'general', 'accuracy', 'relevance']
    if feedback_type not in valid_types:
        errors.append(f"Feedback type must be one of: {', '.join(valid_types)}")
    
    # Rating validation
    rating = data.get('rating')
    if rating is not None:
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            errors.append("Rating must be an integer between 1 and 5")
    
    # Comments validation
    comments = data.get('comments', '')
    if comments and not isinstance(comments, str):
        errors.append("Comments must be a string")
    elif comments and len(comments) > 1000:
        errors.append("Comments cannot exceed 1000 characters")
    
    # Anonymous flag validation
    is_anonymous = data.get('is_anonymous', False)
    if not isinstance(is_anonymous, bool):
        errors.append("is_anonymous must be a boolean")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_conversation_query(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate conversation query parameters"""
    errors = []
    
    # Limit validation
    limit = data.get('limit')
    if limit is not None:
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            errors.append("Limit must be an integer between 1 and 100")
    
    # Status validation
    status = data.get('status')
    valid_statuses = ['active', 'completed', 'archived', 'all']
    if status and status not in valid_statuses:
        errors.append(f"Status must be one of: {', '.join(valid_statuses)}")
    
    # Date range validation
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if start_date and end_date:
        # This would need proper date parsing and comparison
        pass
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
