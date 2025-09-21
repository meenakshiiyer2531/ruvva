"""
CORS configuration middleware
"""

from flask_cors import CORS
from flask import Flask
from config import Config

def setup_cors(app: Flask):
    """Setup CORS configuration"""
    CORS(app, 
         origins=Config.CORS_ORIGINS,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
