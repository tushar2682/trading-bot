from marshmallow import Schema, fields, validate

class WatchlistCreateSchema(Schema):
    """Schema for creating a watchlist"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    symbols = fields.List(fields.Str(), required=False)

class WatchlistSchema(Schema):
    """Schema for watchlist response"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str()
    symbols = fields.List(fields.Str())
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
