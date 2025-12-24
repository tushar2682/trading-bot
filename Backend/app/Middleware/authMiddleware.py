from functools import wraps
from flask import request, jsonify
import jwt
import os
from datetime import datetime

def token_required(f):
    """JWT token authentication middleware"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(
                token, 
                os.getenv('JWT_SECRET_KEY', 'your-secret-key'),
                algorithms=["HS256"]
            )
            request.user_id = data['user_id']
            request.user_email = data.get('email')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def api_key_required(f):
    """API key authentication for external integrations"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key is missing'}), 401
        
        valid_key = os.getenv('API_KEY')
        if api_key != valid_key:
            return jsonify({'error': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

