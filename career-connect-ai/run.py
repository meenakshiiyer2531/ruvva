#!/usr/bin/env python3
"""
CareerConnect AI Application Runner
Simple script to run the Flask application with proper configuration.
"""

import os
import sys
from app import create_app

def main():
    """Main entry point for the application."""
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Using default configuration.")
        print("Copy env.example to .env and configure your settings.")
    
    # Create Flask app
    app = create_app()
    
    # Get configuration
    port = app.config['FLASK_PORT']
    debug = app.config['FLASK_ENV'] == 'development'
    
    print(f"Starting CareerConnect AI...")
    print(f"Environment: {app.config['FLASK_ENV']}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Access the application at: http://localhost:{port}")
    
    # Run the application
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nShutting down CareerConnect AI...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
