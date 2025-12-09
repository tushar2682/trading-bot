from app import db
from datetime import datetime
class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))
    symbol = db.Column(db.String(20), nullable=False, index=True)
    side = db.Column(db.String(10), nullable=False)  # buy, sell
    type = db.Column(db.String(20), default='market')  # market, limit, stop_loss
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    filled_quantity = db.Column(db.Float, default=0)
    average_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, filled, partially_filled, canceled, failed
    exchange = db.Column(db.String(50), default='binance')
    exchange_order_id = db.Column(db.String(100))
    fee = db.Column(db.Float, default=0)
    profit_loss = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'symbol': self.symbol,
            'side': self.side,
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price,
            'filled_quantity': self.filled_quantity,
            'average_price': self.average_price,
            'status': self.status,
            'exchange': self.exchange,
            'exchange_order_id': self.exchange_order_id,
            'fee': self.fee,
            'profit_loss': self.profit_loss,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
