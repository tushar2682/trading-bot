from marshmallow import Schema, fields, validate, validates, ValidationError


class OrderCreateSchema(Schema):
    """Schema for creating an order"""
    symbol = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    order_type = fields.Str(
        required=True,
        validate=validate.OneOf(['market', 'limit', 'stop', 'stop_limit'])
    )
    side = fields.Str(
        required=True,
        validate=validate.OneOf(['buy', 'sell'])
    )
    quantity = fields.Decimal(
        required=True,
        places=8,
        validate=validate.Range(min=0, min_inclusive=False)
    )
    price = fields.Decimal(places=2, allow_none=True)
    stop_price = fields.Decimal(places=2, allow_none=True)
    time_in_force = fields.Str(
        validate=validate.OneOf(['day', 'gtc', 'ioc', 'fok']),
        load_default='day'
    )

    @validates('price')
    def validate_price(self, value):
        # Validate that price is provided for limit-like orders.
        order_type = None
        # prefer context, but allow input data to contain order_type
        if isinstance(self.context, dict):
            order_type = self.context.get('order_type')
        try:
            # marshmallow provides parent data via self.context in many flows
            pass
        except Exception:
            pass

        if order_type in ['limit', 'stop_limit'] and (value is None):
            raise ValidationError('Price is required for limit orders')

class OrderSchema(Schema):
    """Schema for order response"""
    id = fields.Int(dump_only=True)
    account_id = fields.Int()
    symbol = fields.Str()
    order_type = fields.Str()
    side = fields.Str()
    quantity = fields.Decimal(places=8)
    filled_quantity = fields.Decimal(places=8)
    price = fields.Decimal(places=2)
    stop_price = fields.Decimal(places=2)
    status = fields.Str()
    time_in_force = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    filled_at = fields.DateTime(dump_only=True)