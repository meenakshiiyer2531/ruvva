"""
CareerConnect AI Flask Application
Main application file for the AI-powered career counseling service for Indian students.
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter.util import get_remote_address

import redis
from config import get_config

def create_app():
    """Application factory pattern for creating Flask app."""
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize CORS with credentials support
    CORS(app,
         origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_HEADERS'],
         supports_credentials=True,
         expose_headers=['Content-Type', 'Authorization'])
    
    # Initialize Redis connection
    try:
        redis_client = redis.from_url(app.config['REDIS_URL'])
        redis_client.ping()  # Test connection
        app.redis_client = redis_client
    except redis.ConnectionError:
        app.logger.warning("Redis connection failed. Caching will be disabled.")
        app.redis_client = None
    
    # Initialize shared Rate Limiter (disable for MVP simplicity)
    app.limiter = None  # Disable rate limiting for MVP
    # try:
    #     from utils.limiter import limiter
    #     limiter.init_app(app)
    #     app.limiter = limiter
    # except Exception as e:
    #     app.logger.warning(f"Rate limiter initialization failed: {e}. Continuing without rate limiting.")
    #     app.limiter = None
    
    # Setup logging
    setup_logging(app)
    
    # Setup authentication (JWT)
    from api.middleware.auth_middleware import setup_auth
    setup_auth(app)

    # Initialize backend integration service
    from services.backend_integration import backend_service
    backend_service.init_app(app)

    # Register error handlers
    register_error_handlers(app)
    
    # Register API blueprints
    from api.routes.profile_routes import profile_bp
    from api.routes.assessment_routes import assessment_bp
    from api.routes.career_routes import career_bp
    from api.routes.chat_routes import chat_bp
    from api.routes.learning_routes import learning_bp
    from api.routes.auth_routes import auth_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(auth_bp)
    
    # Register routes
    register_routes(app)
    
    return app

def setup_logging(app):
    """Setup application logging."""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format=app.config['LOG_FORMAT'],
        handlers=[
            logging.FileHandler(app.config['LOG_FILE']),
            logging.StreamHandler()
        ]
    )
    
    app.logger.info(f"CareerConnect AI started in {app.config['FLASK_ENV']} mode")

def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server.',
            'timestamp': datetime.utcnow().isoformat()
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication is required to access this resource.',
            'timestamp': datetime.utcnow().isoformat()
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.',
            'timestamp': datetime.utcnow().isoformat()
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'timestamp': datetime.utcnow().isoformat()
        }), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
            'timestamp': datetime.utcnow().isoformat()
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.',
            'timestamp': datetime.utcnow().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

def register_routes(app):
    """Register application routes."""
    
    @app.route('/')
    def index():
        """Welcome endpoint."""
        return jsonify({
            'message': 'Welcome to CareerConnect AI',
            'description': 'AI-powered career counseling service for Indian students',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'health': '/health',
                'api_docs': '/api/docs',
                'status': '/status'
            }
        })
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'environment': app.config['FLASK_ENV'],
            'services': {
                'redis': 'connected' if app.redis_client else 'disconnected',
                'gemini_api': 'configured' if app.config['GEMINI_API_KEY'] else 'not_configured'
            }
        }
        
        # Check Redis connection
        if app.redis_client:
            try:
                app.redis_client.ping()
                health_status['services']['redis'] = 'connected'
            except redis.ConnectionError:
                health_status['services']['redis'] = 'disconnected'
                health_status['status'] = 'degraded'
        
        # Check Gemini API key
        if not app.config['GEMINI_API_KEY']:
            health_status['status'] = 'degraded'
            health_status['services']['gemini_api'] = 'not_configured'
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        return jsonify(health_status), status_code
    
    @app.route('/status')
    def status():
        """Detailed status endpoint."""
        return jsonify({
            'application': 'CareerConnect AI',
            'version': '1.0.0',
            'environment': app.config['FLASK_ENV'],
            'uptime': 'N/A',  # Would need to track start time
            'timestamp': datetime.utcnow().isoformat(),
            'configuration': {
                'cors_origins': app.config['CORS_ORIGINS'],
                'rate_limit': app.config['RATELIMIT_DEFAULT'],
                'log_level': app.config['LOG_LEVEL'],
                'max_profile_size': app.config['MAX_PROFILE_SIZE'],
                'cache_ttl': app.config['CACHE_TTL']
            },
            'features': {
                'ai_counseling': True,
                'career_assessment': True,
                'learning_paths': True,
                'mentor_matching': True,
                'indian_education_system': True
            }
        })
    
    @app.route('/api/docs')
    def api_docs():
        """API documentation endpoint."""
        return jsonify({
            'title': 'CareerConnect AI API Documentation',
            'version': '1.0.0',
            'description': 'AI-powered career counseling API for Indian students',
            'base_url': request.base_url.rstrip('/'),
            'endpoints': {
                'health': {
                    'url': '/health',
                    'method': 'GET',
                    'description': 'Health check endpoint'
                },
                'status': {
                    'url': '/status',
                    'method': 'GET',
                    'description': 'Detailed application status'
                },
                'profile': {
                    'url': '/api/v1/profile',
                    'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                    'description': 'Student profile management'
                },
                'assessment': {
                    'url': '/api/v1/assessment',
                    'methods': ['GET', 'POST'],
                    'description': 'Career assessment and analysis'
                },
                'careers': {
                    'url': '/api/v1/careers',
                    'methods': ['GET', 'POST'],
                    'description': 'Career recommendations and information'
                },
                'chat': {
                    'url': '/api/v1/chat',
                    'methods': ['GET', 'POST'],
                    'description': 'AI chat counseling'
                },
                'learning': {
                    'url': '/api/v1/learning',
                    'methods': ['GET', 'POST'],
                    'description': 'Learning path generation'
                },
                'mentor': {
                    'url': '/api/v1/mentor',
                    'methods': ['GET', 'POST'],
                    'description': 'Mentor matching and management'
                }
            },
            'authentication': 'Bearer token required for most endpoints',
            'rate_limiting': app.config['RATELIMIT_DEFAULT'],
            'cors': {
                'origins': app.config['CORS_ORIGINS'],
                'methods': app.config['CORS_METHODS'],
                'headers': app.config['CORS_HEADERS']
            }
        })

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application
    port = app.config['FLASK_PORT']
    debug = app.config['FLASK_ENV'] == 'development'
    
    app.logger.info(f"Starting CareerConnect AI on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)