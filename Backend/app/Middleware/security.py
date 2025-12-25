from flask import request, abort

def setup_security_headers(app):
    """Setup security headers and CORS"""
    
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
        
        return response
    
    @app.before_request
    def validate_content_type():
        """Validate content type for POST/PUT requests"""
        if request.method in ['POST', 'PUT']:
            if not request.is_json:
                abort(400, description="Content-Type must be application/json")
    
    return app

