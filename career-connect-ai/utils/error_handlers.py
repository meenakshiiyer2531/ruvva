"""
Error handling utilities
"""

from flask import jsonify
from utils.logger import get_logger
import traceback

logger = get_logger(__name__)

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {str(error)}")
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request was invalid or cannot be served',
            'status_code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"Unauthorized access: {str(error)}")
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication is required',
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"Forbidden access: {str(error)}")
        return jsonify({
            'error': 'Forbidden',
            'message': 'Access to this resource is denied',
            'status_code': 403
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Resource not found: {str(error)}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        logger.warning(f"Unprocessable entity: {str(error)}")
        return jsonify({
            'error': 'Unprocessable Entity',
            'message': 'The request was well-formed but contains semantic errors',
            'status_code': 422
        }), 422
    
    @app.errorhandler(429)
    def too_many_requests(error):
        logger.warning(f"Rate limit exceeded: {str(error)}")
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded. Please try again later',
            'status_code': 429
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal server error: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

class APIError(Exception):
    """Custom API error class"""
    
    def __init__(self, message: str, status_code: int = 400, payload: dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self):
        return {
            'error': self.message,
            'status_code': self.status_code,
            'payload': self.payload
        }

class ValidationError(APIError):
    """Validation error"""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message, 400)
        self.field = field
    
    def to_dict(self):
        result = super().to_dict()
        if self.field:
            result['field'] = self.field
        return result

class AuthenticationError(APIError):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)

class AuthorizationError(APIError):
    """Authorization error"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)

class NotFoundError(APIError):
    """Resource not found error"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class RateLimitError(APIError):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429)
