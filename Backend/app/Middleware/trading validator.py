from functools import wraps
from flask import request, jsonify

def validate_trade_request(f):
    """Validate trading request parameters"""
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        
        required_fields = ['symbol', 'quantity', 'order_type']
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing
            }), 400
        
        # Validate quantity
        try:
            quantity = float(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid quantity format'}), 400
        
        # Validate order type
        valid_types = ['market', 'limit', 'stop', 'stop_limit']
        if data['order_type'] not in valid_types:
            return jsonify({
                'error': 'Invalid order type',
                'valid_types': valid_types
            }), 400
        
        return f(*args, **kwargs)
    
    return decorated