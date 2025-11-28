"""
Authentication middleware
Manage validation of API Key and JWT for protected endpoints
"""
from flask import request, jsonify
from functools import wraps
import os
from dotenv import load_dotenv
from app.jwt_manager import JWTManager

# Load variables from .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables")

jwt_manager = JWTManager()

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


def require_jwt(f):
    """
    Decorator to require valid JWT in Authorization header
    Header example: X-JWT-KWY: Bearer your-jwt-token-here
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get('X-JWT-KWY')
        
        if not jwt_token:
            return jsonify({"error": "JWT token is missing"}), 401
        
        # Verify the token
        payload = jwt_manager.verify_token(jwt_token)
        
        if payload is None:
            return jsonify({"error": "Invalid or expired JWT token"}), 403
        
        request.jwt_payload = payload
        
        return f(*args, **kwargs)
    return decorated_function

def optional_jwt(f):
    """
    Decorator to optionally accept JWT in Authorization header
    Header example: X-JWT-KWY: Bearer your-jwt-token-here
    """
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get('X-JWT-KWY')
        
        if jwt_token:
            # Verify the token
            payload = jwt_manager.verify_token(jwt_token)
            
            if payload:
                request.jwt_payload = payload
        else:
            request.jwt_payload = None
            
        return f(*args, **kwargs)
    return decorated_function