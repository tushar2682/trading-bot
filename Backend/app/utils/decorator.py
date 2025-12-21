
from functools import wraps
from flask import jsonify
from .exception import AppException
from .logger import log

def handle_exceptions(f):
    """
    Wrap routes to catch custom AppExceptions and return JSON responses.
    Prevents the server from crashing on predicted errors.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AppException as e:
            log.warning(f"Handled Exception: {e.message}")
            return jsonify(e.to_dict()), e.status_code
        except Exception as e:
            log.error(f"Unexpected Error: {str(e)}", exc_info=True)
            return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    return decorated_function

def admin_required(f):
    """
    Middleware to ensure the user has admin privileges.
    Assumes `get_jwt_identity` or `current_user` is available.
    """
    # Note: Requires flask_jwt_extended implementation in the route
    from flask_jwt_extended import get_jwt, verify_jwt_in_request
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Admins only!"}), 403
        return f(*args, **kwargs)
    return wrapper