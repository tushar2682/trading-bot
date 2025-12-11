from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from app import db, redis_client
from app.models.user import User
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: {email, username, password, first_name, last_name}
    """
    try:
        data = request.get_json() or {}

        # Validate required fields
        required_fields = ['email', 'username', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        # Validate password strength
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            username=data['username'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            balance=10000.0  # Starting balance
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    POST /api/auth/login
    Body: {username, password}
    """
    try:
        data = request.get_json() or {}

        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 403
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Store refresh token in Redis with expiry (seconds)
        redis_client.setex(
            f'refresh_token:{user.id}',
            int(timedelta(days=30).total_seconds()),
            refresh_token
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout
    POST /api/auth/logout
    """
    try:
        user_id = get_jwt_identity()
        jti = get_jwt()['jti']

        # Blacklist the token (store for 1 hour)
        redis_client.setex(f'blacklist:{jti}', int(timedelta(hours=1).total_seconds()), 'true')

        # Remove refresh token
        redis_client.delete(f'refresh_token:{user_id}')

        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    POST /api/auth/refresh
    """
    try:
        user_id = get_jwt_identity()
        
        # Create new access token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info
    GET /api/auth/me
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    POST /api/auth/change-password
    Body: {old_password, new_password}
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        user = User.query.get(user_id)
        
        if not user.check_password(data.get('old_password', '')):
            return jsonify({'error': 'Invalid old password'}), 400
        
        if len(data.get('new_password', '')) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
