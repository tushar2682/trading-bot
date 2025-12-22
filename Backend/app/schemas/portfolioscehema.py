
from marshmallow import Schema

from marshmallow import fields, validate
class PortfolioSummarySchema(Schema):
    """Schema for portfolio summary"""
    total_value = fields.Decimal(places=2)
    cash_balance = fields.Decimal(places=2)
    positions_value = fields.Decimal(places=2)
    total_pnl = fields.Decimal(places=2)
    total_pnl_percent = fields.Decimal(places=2)
    day_pnl = fields.Decimal(places=2)
    day_pnl_percent = fields.Decimal(places=2)