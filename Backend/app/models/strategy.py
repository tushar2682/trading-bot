from app import db
from datetime import datetime
class Strategy(db.Model):
    __tablename__ = 'strategies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    strategy_type = db.Column(db.String(50))  # rsi, macd, bollinger, custom
    parameters = db.Column(db.JSON, default={})
    code = db.Column(db.Text)
    backtest_results = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=False)
    performance_metrics = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'strategy_type': self.strategy_type,
            'parameters': self.parameters,
            'backtest_results': self.backtest_results,
            'is_active': self.is_active,
            'performance_metrics': self.performance_metrics,
            'created_at': self.created_at.isoformat()
        }
