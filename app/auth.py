"""
Authentication middleware
Manage validation of API Key and JWT for protected endpoints
"""
from flask import request, jsonify
from functools import wraps
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables")

def require_api_key(f):
    """
    Decorator to require API key valid in request headers
    Header example: X-Parse-REST-API-Key: your-api-key-here
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-Parse-REST-API-Key')
        
        if not api_key:
            return jsonify({"error": "API key is missing"}), 401
        
        if api_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 403

        return f(*args, **kwargs)
    
    return decorated_function