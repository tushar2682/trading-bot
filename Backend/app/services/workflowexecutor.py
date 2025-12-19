from app.models.position import Position
from app.models.trade import Trade
from app.models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func

class PortfolioService:
    """Handle portfolio calculations and analytics"""
    
    def get_portfolio_summary(self, user_id):
        """Get portfolio summary"""
        user = User.query.get(user_id)
        positions = Position.query.filter_by(user_id=user_id).all()
        
        # Calculate portfolio value
        positions_value = sum(p.quantity * p.current_price for p in positions)
        total_equity = user.balance + positions_value
        
        # Calculate unrealized P&L
        unrealized_pnl = sum(p.unrealized_pnl for p in positions)
        
        # Calculate realized P&L (from completed trades)
        realized_pnl = db.session.query(func.sum(Trade.profit_loss)).filter(
            Trade.user_id == user_id,
            Trade.status == 'filled',
            Trade.profit_loss != None
        ).scalar() or 0
        
        return {
            'balance': user.balance,
            'positions_value': positions_value,
            'total_equity': total_equity,
            'unrealized_pnl': unrealized_pnl,
            'realized_pnl': realized_pnl,
            'total_pnl': unrealized_pnl + realized_pnl,
            'num_positions': len(positions)
        }
    
    def get_performance(self, user_id, timeframe='1M'):
        """Get performance metrics"""
        # Calculate date range
        if timeframe == '1D':
            start_date = datetime.utcnow() - timedelta(days=1)
        elif timeframe == '1W':
            start_date = datetime.utcnow() - timedelta(weeks=1)
        elif timeframe == '1M':
            start_date = datetime.utcnow() - timedelta(days=30)
        elif timeframe == '3M':
            start_date = datetime.utcnow() - timedelta(days=90)
        elif timeframe == '1Y':
            start_date = datetime.utcnow() - timedelta(days=365)
        else:
            start_date = datetime(2020, 1, 1)
        
        # Get trades in timeframe
        trades = Trade.query.filter(
            Trade.user_id == user_id,
            Trade.timestamp >= start_date,
            Trade.status == 'filled'
        ).all()
        
        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_profit': 0,
                'total_loss': 0,
                'net_pnl': 0
            }
        
        winning_trades = [t for t in trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in trades if t.profit_loss and t.profit_loss < 0]
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(trades) * 100) if trades else 0,
            'total_profit': sum(t.profit_loss for t in winning_trades),
            'total_loss': sum(t.profit_loss for t in losing_trades),
            'net_pnl': sum(t.profit_loss or 0 for t in trades)
        }
    
    def get_analytics(self, user_id):
        """Get detailed analytics"""
        summary = self.get_portfolio_summary(user_id)
        performance = self.get_performance(user_id, 'ALL')
        
        # Get top performing symbols
        positions = Position.query.filter_by(user_id=user_id).all()
        top_positions = sorted(positions, key=lambda p: p.unrealized_pnl, reverse=True)[:5]
        
        return {
            'summary': summary,
            'performance': performance,
            'top_positions': [p.to_dict() for p in top_positions]
        }
