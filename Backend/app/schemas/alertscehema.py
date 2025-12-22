
from marshmallow import Schema

from marshmallow import fields, validate
class AlertCreateSchema(Schema):
    """Schema for creating a price alert"""
    symbol = fields.Str(required=True)
    condition = fields.Str(
        required=True,
        validate=validate.OneOf(['above', 'below'])
    )
    target_price = fields.Decimal(required=True, places=2)
    notification_type = fields.Str(
        validate=validate.OneOf(['email', 'push', 'sms']),
        missing='email'
    )

class AlertSchema(Schema):
    """Schema for alert response"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    symbol = fields.Str()
    condition = fields.Str()
    target_price = fields.Decimal(places=2)
    notification_type = fields.Str()
    is_active = fields.Bool()
    triggered_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)