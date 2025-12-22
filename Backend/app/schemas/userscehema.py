from marshmallow import Schema, fields, validate
class UserRegistrationSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(max=100))
    last_name = fields.Str(required=True, validate=validate.Length(max=100))
    phone = fields.Str(validate=validate.Length(max=20))

class UserLoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserProfileSchema(Schema):
    """Schema for user profile response"""
    id = fields.Int(dump_only=True)
    email = fields.Email()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    is_verified = fields.Bool()

