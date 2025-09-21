"""
Shared Flask-Limiter instance for consistent per-endpoint rate limiting
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a shared limiter that will be initialized in app.py
limiter = Limiter(key_func=get_remote_address)
