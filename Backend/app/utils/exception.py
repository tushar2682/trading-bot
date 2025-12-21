# Backend/app/utils/exceptions.py

class AppException(Exception):
    """Base class for all application exceptions."""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

class ValidationError(AppException):
    """Raised when input data fails validation."""
    def __init__(self, message="Invalid input data", payload=None):
        super().__init__(message, status_code=400, payload=payload)

class TradingError(AppException):
    """Raised when a trade execution fails."""
    def __init__(self, message="Trade execution failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)

class ResourceNotFound(AppException):
    """Raised when a DB record is missing."""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class AuthorizationError(AppException):
    """Raised when permission is denied."""
    def __init__(self, message="You are not authorized to perform this action"):
        super().__init__(message, status_code=403)