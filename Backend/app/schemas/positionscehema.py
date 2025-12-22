from marshmallow import Schema, fields


class PositionSchema(Schema):
   """Schema for position response"""
   id = fields.Int(dump_only=True)
   account_id = fields.Int()
   symbol = fields.Str()
   quantity = fields.Decimal(places=8)
   average_price = fields.Decimal(places=2)
   current_price = fields.Decimal(places=2)
   market_value = fields.Decimal(places=2)
   unrealized_pnl = fields.Decimal(places=2)
   realized_pnl = fields.Decimal(places=2)
   created_at = fields.DateTime(dump_only=True)
   updated_at = fields.DateTime(dump_only=True)
