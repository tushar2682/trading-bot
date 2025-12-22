from marshmallow import Schema
from marshmallow import fields
class ErrorSchema(Schema):
    """Schema for error responses"""
    error = fields.Str()
    message = fields.Str()
    status_code = fields.Int()
    timestamp = fields.DateTime()