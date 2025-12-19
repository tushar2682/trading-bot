from app import db
from app.models.trade import Trade
from app.models.position import Position
from app.models.user import User
from datetime import datetime
import random  # For simulation

class TradingEngine:
    """Handles trade execution and position management"""
    
    def create_trade(self, user_id, symbol, side, trade_type, quantity, price=None, stop_loss=None, take_profit=None):
        """Create and execute a new trade"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Get current market price if not provided
        if not price or trade_type == 'market':
            price = self.get_current_price(symbol)
        
        # Calculate required balance
        if side == 'buy':
            required_balance = quantity * price
            if user.balance < required_balance:
                raise ValueError("Insufficient balance")
        
        # Create trade
        trade = Trade(
            user_id=user_id,
            symbol=symbol,
            side=side,
            type=trade_type,
            quantity=quantity,
            price=price,
            status='pending'
        )
        
        db.session.add(trade)
        
        # Execute trade immediately for market orders
        if trade_type == 'market':
            self.execute_trade(trade, user)
        
        db.session.commit()
        return trade
    
    def execute_trade(self, trade, user):
        """Execute a pending trade"""
        if trade.side == 'buy':
            # Deduct balance
            user.balance -= trade.quantity * trade.price
            
            # Create or update position
            position = Position.query.filter_by(
                user_id=trade.user_id,
                symbol=trade.symbol
            ).first()
            
            if position:
                # Average entry price calculation
                total_quantity = position.quantity + trade.quantity
                total_cost = (position.quantity * position.entry_price) + (trade.quantity * trade.price)
                position.entry_price = total_cost / total_quantity
                position.quantity = total_quantity
                position.current_price = trade.price
            else:
                position = Position(
                    user_id=trade.user_id,
                    symbol=trade.symbol,
                    quantity=trade.quantity,
                    entry_price=trade.price,
                    current_price=trade.price
                )
                db.session.add(position)
        
        elif trade.side == 'sell':
            position = Position.query.filter_by(
                user_id=trade.user_id,
                symbol=trade.symbol
            ).first()
            
            if not position or position.quantity < trade.quantity:
                raise ValueError("Insufficient position")
            
            # Calculate profit/loss
            trade.profit_loss = (trade.price - position.entry_price) * trade.quantity
            
            # Add to balance
            user.balance += trade.quantity * trade.price + trade.profit_loss
            
            # Update position
            position.quantity -= trade.quantity
            position.realized_pnl += trade.profit_loss
            
            if position.quantity == 0:
                db.session.delete(position)
        
        trade.status = 'filled'
        trade.filled_quantity = trade.quantity
        trade.average_price = trade.price
        
    def close_position(self, position):
        """Close an entire position"""
        return self.create_trade(
            user_id=position.user_id,
            symbol=position.symbol,
            side='sell',
            trade_type='market',
            quantity=position.quantity
        )
    
    def get_current_price(self, symbol):
        """Get current market price (simulated)"""
        # In production, fetch from exchange API
        base_prices = {
            'BTC/USDT': 43000,
            'ETH/USDT': 2280,
            'BNB/USDT': 312,
            'SOL/USDT': 98,
            'ADA/USDT': 0.58
        }
        base_price = base_prices.get(symbol, 100)
        # Add random variation
        return base_price + (random.random() - 0.5) * base_price * 0.02

