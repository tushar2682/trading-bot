from  marshmallow import Schema, fields, validate
class QuoteSchema(Schema):
    """Schema for real-time quote"""
    symbol = fields.Str()
    bid = fields.Decimal(places=2)
    ask = fields.Decimal(places=2)
    last = fields.Decimal(places=2)
    volume = fields.Int()
    timestamp = fields.DateTime()

class CandleSchema(Schema):
    """Schema for candlestick data"""
    symbol = fields.Str()
    timestamp = fields.DateTime()
    open = fields.Decimal(places=2)
    high = fields.Decimal(places=2)
    low = fields.Decimal(places=2)
    close = fields.Decimal(places=2)
    volume = fields.Int()

