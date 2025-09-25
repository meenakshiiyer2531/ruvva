"""
Shared Flask-Limiter instance for consistent per-endpoint rate limiting
"""
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    # Create a shared limiter that will be initialized in app.py
    limiter = Limiter(key_func=get_remote_address)
except ImportError:
    # Fallback if flask-limiter is not installed
    class MockLimiter:
        def init_app(self, app):
            pass
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

    limiter = MockLimiter()
