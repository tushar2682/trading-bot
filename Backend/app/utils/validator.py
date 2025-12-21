
import re
from .exception import ValidationError
from .constant import OrderSide, OrderType

def validate_email(email):
    """Simple regex check for email validity."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(regex, email):
        raise ValidationError("Invalid email format")
    return True

def validate_trade_request(data):
    """Validates the payload for creating a trade."""
    required_fields = ['symbol', 'side', 'quantity']
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing field: {field}")

    if data['side'] not in [OrderSide.BUY, OrderSide.SELL]:
        raise ValidationError(f"Invalid side. Must be {OrderSide.BUY} or {OrderSide.SELL}")
    
    if data.get('type') and data['type'] not in [OrderType.MARKET, OrderType.LIMIT]:
        raise ValidationError("Invalid order type")
        
    try:
        qty = float(data['quantity'])
        if qty <= 0:
            raise ValidationError("Quantity must be positive")
    except ValueError:
        raise ValidationError("Quantity must be a number")
    
    return True