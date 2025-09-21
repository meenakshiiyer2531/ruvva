"""
Auth routes to support development/testing JWT generation
"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from utils.response_formatter import APIResponse
from datetime import timedelta
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/dev-token', methods=['POST'])
def get_dev_token():
    """Issue a short-lived JWT for development/testing only.
    Body: { "student_id": <int>, "expires_in": <seconds optional> }
    """
    if os.environ.get('FLASK_ENV', 'development') == 'production':
        return APIResponse.forbidden("Dev token endpoint is disabled in production")

    data = request.get_json() or {}
    student_id = data.get('student_id')
    if student_id is None:
        return APIResponse.validation_error({"student_id": "student_id is required"})

    expires_in = int(data.get('expires_in', 3600))
    token = create_access_token(identity=int(student_id), expires_delta=timedelta(seconds=expires_in))
    return APIResponse.success({"access_token": token, "expires_in": expires_in}, "Dev token issued")
