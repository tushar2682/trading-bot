from marshmallow import Schema, fields, validate
class TransactionSchema(Schema):
    """Schema for transaction response"""
    id = fields.Int(dump_only=True)
    account_id = fields.Int()
    transaction_type = fields.Str()
    amount = fields.Decimal(places=2)
    currency = fields.Str()
    description = fields.Str()
    reference_id = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class DepositSchema(Schema):
    """Schema for deposit request"""
    amount = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0, min_inclusive=False)
    )
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(['bank_transfer', 'card', 'crypto'])
    )

class WithdrawalSchema(Schema):
    """Schema for withdrawal request"""
    amount = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0, min_inclusive=False)
    )
    destination = fields.Str(required=True)
