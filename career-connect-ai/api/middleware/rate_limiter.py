"""
Rate limiting middleware
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from config import Config

def setup_rate_limiting(app: Flask):
    """Setup rate limiting"""
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[Config.RATELIMIT_DEFAULT],
        storage_uri=Config.RATELIMIT_STORAGE_URL
    )
    
    # Apply rate limits to specific endpoints
    limiter.limit("10 per minute")(app.view_functions.get('api.profile.create_profile'))
    limiter.limit("5 per minute")(app.view_functions.get('api.assessment.submit_riasec_assessment'))
    limiter.limit("20 per minute")(app.view_functions.get('api.chat.send_message'))
    
    return limiter
