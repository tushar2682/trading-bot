from marshmallow import Schema, fields, validate


class AccountCreateSchema(Schema):
    """Schema for creating a trading account"""
    account_type = fields.Str(
        required=True,
        validate=validate.OneOf(['cash', 'margin', 'retirement'])
    )
    currency = fields.Str(
        required=True,
        validate=validate.OneOf(['USD', 'EUR', 'GBP', 'JPY'])
    )
    initial_balance = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0)
    )

class AccountSchema(Schema):
    """Schema for account response"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    account_number = fields.Str(dump_only=True)
    account_type = fields.Str()
    currency = fields.Str()
    balance = fields.Decimal(places=2)
    available_balance = fields.Decimal(places=2)
    margin_used = fields.Decimal(places=2)
    created_at = fields.DateTime(dump_only=True)
    status = fields.Str()