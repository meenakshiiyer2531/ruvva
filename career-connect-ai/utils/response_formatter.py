"""
Response formatting utilities for consistent API responses
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union
from flask import jsonify, request


class APIResponse:
    """Utility class for formatting consistent API responses"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200) -> tuple:
        """Format successful API response"""
        response = {
            "success": True,
            "data": data,
            "message": message,
            "error": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": str(uuid.uuid4())
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str = "An error occurred", 
              error_details: Optional[Dict] = None, 
              status_code: int = 500) -> tuple:
        """Format error API response"""
        response = {
            "success": False,
            "data": None,
            "message": message,
            "error": error_details or {"code": status_code, "message": message},
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": str(uuid.uuid4())
        }
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error(errors: Dict, message: str = "Validation failed") -> tuple:
        """Format validation error response"""
        error_details = {
            "code": 400,
            "message": message,
            "validation_errors": errors
        }
        return APIResponse.error(message, error_details, 400)
    
    @staticmethod
    def not_found(resource: str = "Resource") -> tuple:
        """Format not found error response"""
        message = f"{resource} not found"
        error_details = {
            "code": 404,
            "message": message,
            "resource": resource
        }
        return APIResponse.error(message, error_details, 404)
    
    @staticmethod
    def unauthorized(message: str = "Authentication required") -> tuple:
        """Format unauthorized error response"""
        error_details = {
            "code": 401,
            "message": message,
            "auth_required": True
        }
        return APIResponse.error(message, error_details, 401)
    
    @staticmethod
    def forbidden(message: str = "Access denied") -> tuple:
        """Format forbidden error response"""
        error_details = {
            "code": 403,
            "message": message,
            "access_denied": True
        }
        return APIResponse.error(message, error_details, 403)
    
    @staticmethod
    def rate_limited(message: str = "Rate limit exceeded") -> tuple:
        """Format rate limit error response"""
        error_details = {
            "code": 429,
            "message": message,
            "retry_after": "60 seconds"
        }
        return APIResponse.error(message, error_details, 429)
    
    @staticmethod
    def service_unavailable(message: str = "Service temporarily unavailable") -> tuple:
        """Format service unavailable error response"""
        error_details = {
            "code": 503,
            "message": message,
            "service_status": "unavailable"
        }
        return APIResponse.error(message, error_details, 503)


def handle_exceptions(func):
    """Decorator to handle exceptions in route functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return APIResponse.validation_error({"value_error": str(e)})
        except KeyError as e:
            return APIResponse.validation_error({"missing_field": str(e)})
        except Exception as e:
            # Log the error here
            return APIResponse.error(
                "Internal server error", 
                {"code": 500, "message": str(e)}, 
                500
            )
    wrapper.__name__ = func.__name__
    return wrapper


def paginate_response(data: list, page: int = 1, per_page: int = 10, total: int = None) -> Dict:
    """Add pagination metadata to response data"""
    if total is None:
        total = len(data)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]
    
    return {
        "items": paginated_data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "has_next": end < total,
            "has_prev": page > 1
        }
    }
