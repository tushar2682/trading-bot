from app.models.position import Position
from app.models.trade import Trade
from app.models.user import User
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func
import logging

import celery

logger = logging.getLogger(__name__)

class RiskManager:
    """Comprehensive risk management system"""
    
    def __init__(self, user_id, config=None):
        """
        Initialize risk manager
        
        Args:
            user_id: User ID
            config: Optional risk configuration dict
        """
        self.user_id = user_id
        self.user = User.query.get(user_id)
        
        if not self.user:
            raise ValueError("User not found")
        
        # Default risk parameters (can be overridden by config)
        self.config = config or {}
        self.max_position_size = self.config.get('max_position_size', 10000)
        self.max_open_positions = self.config.get('max_open_positions', 10)
        self.max_daily_loss = self.config.get('max_daily_loss', 1000)
        self.max_drawdown = self.config.get('max_drawdown', 0.20)  # 20%
        self.risk_per_trade = self.config.get('risk_per_trade', 0.02)  # 2%
        self.max_leverage = self.config.get('max_leverage', 10)
        self.min_risk_reward = self.config.get('min_risk_reward', 1.5)
    
    def validate_trade(self, symbol, side, quantity, price):
        """
        Comprehensive trade validation
        
        Args:
            symbol: Trading symbol
            side: 'buy' or 'sell'
            quantity: Trade quantity
            price: Trade price
            
        Returns:
            Tuple of (is_valid, message)
        """
        validations = [
            self._check_position_size_limit(quantity, price),
            self._check_max_open_positions(side),
            self._check_daily_loss_limit(),
            self._check_drawdown_limit(),
            self._check_balance(side, quantity, price),
            self._check_position_exists(symbol, side, quantity),
            self._check_correlation_limit(symbol, side)
        ]
        
        for is_valid, message in validations:
            if not is_valid:
                logger.warning(f"Trade validation failed for user {self.user_id}: {message}")
                return False, message
        
        return True, "Trade validated successfully"
    
    def _check_position_size_limit(self, quantity, price):
        """Check if position size exceeds limit"""
        position_value = quantity * price
        if position_value > self.max_position_size:
            return False, f"Position size ${position_value:.2f} exceeds limit ${self.max_position_size:.2f}"
        return True, "Position size OK"
    
    def _check_max_open_positions(self, side):
        """Check if maximum open positions reached"""
        if side == 'sell':
            return True, "Sell order OK"
        
        open_positions = Position.query.filter_by(user_id=self.user_id).count()
        if open_positions >= self.max_open_positions:
            return False, f"Maximum open positions ({self.max_open_positions}) reached"
        return True, "Open positions OK"
    
    def _check_daily_loss_limit(self):
        """Check if daily loss limit exceeded"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        daily_loss = db.session.query(func.sum(Trade.profit_loss)).filter(
            Trade.user_id == self.user_id,
            Trade.timestamp >= today,
            Trade.status == 'filled',
            Trade.profit_loss < 0
        ).scalar() or 0
        
        daily_loss = abs(daily_loss)
        
        if daily_loss >= self.max_daily_loss:
            return False, f"Daily loss limit ${self.max_daily_loss:.2f} reached (current: ${daily_loss:.2f})"
        return True, f"Daily loss OK (${daily_loss:.2f} of ${self.max_daily_loss:.2f})"
    
    def _check_drawdown_limit(self):
        """Check if maximum drawdown exceeded"""
        current_equity = self._calculate_total_equity()
        peak_equity = self._get_peak_equity()
        
        if peak_equity == 0:
            return True, "Drawdown OK"
        
        drawdown = (peak_equity - current_equity) / peak_equity
        
        if drawdown >= self.max_drawdown:
            return False, f"Maximum drawdown {self.max_drawdown*100:.1f}% reached (current: {drawdown*100:.1f}%)"
        return True, f"Drawdown OK ({drawdown*100:.1f}% of {self.max_drawdown*100:.1f}%)"
    
    def _check_balance(self, side, quantity, price):
        """Check if sufficient balance available"""
        if side == 'sell':
            return True, "Balance OK for sell"
        
        required_balance = quantity * price
        if self.user.balance < required_balance:
            return False, f"Insufficient balance (required: ${required_balance:.2f}, available: ${self.user.balance:.2f})"
        return True, "Balance sufficient"
    
    def _check_position_exists(self, symbol, side, quantity):
        """Check if position exists for sell orders"""
        if side == 'buy':
            return True, "Buy order OK"
        
        position = Position.query.filter_by(
            user_id=self.user_id,
            symbol=symbol
        ).first()
        
        if not position:
            return False, f"No position exists for {symbol}"
        
        if position.quantity < quantity:
            return False, f"Insufficient position (available: {position.quantity}, requested: {quantity})"
        
        return True, "Position exists"
    
    def _check_correlation_limit(self, symbol, side):
        """Check symbol correlation to limit concentration risk"""
        if side == 'sell':
            return True, "Correlation OK for sell"
        
        # Get base currency from symbol (e.g., BTC from BTC/USDT)
        base_currency = symbol.split('/')[0]
        
        # Count positions with same base currency
        positions = Position.query.filter_by(user_id=self.user_id).all()
        same_base_count = sum(1 for p in positions if p.symbol.startswith(base_currency))
        
        # Limit to 3 positions with same base currency
        if same_base_count >= 3:
            return False, f"Too many {base_currency} positions (limit: 3)"
        
        return True, "Correlation OK"
    
    def calculate_position_size(self, symbol, entry_price, stop_loss_price):
        """
        Calculate optimal position size based on risk per trade
        
        Args:
            symbol: Trading symbol
            entry_price: Entry price
            stop_loss_price: Stop loss price
            
        Returns:
            Optimal position size
        """
        # Ensure numeric inputs
        try:
            entry_price = float(entry_price)
            stop_loss_price = float(stop_loss_price)
        except Exception:
            logger.warning("Invalid numeric input for entry/stop prices")
            return 0

        # Basic validation
        if stop_loss_price >= entry_price or entry_price == 0:
            logger.warning(
                f"Invalid stop loss: {stop_loss_price} >= {entry_price}"
            )
            return 0

        # Calculate risk amount (% of total equity)
        total_equity = self._calculate_total_equity() or 0
        try:
            risk_amount = float(total_equity) * float(self.risk_per_trade)
        except Exception:
            risk_amount = 0

        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit == 0:
            logger.warning("Risk per unit is zero, cannot calculate position size")
            return 0

        # Calculate position size
        position_size = risk_amount / risk_per_unit

        # Apply maximum position size constraint
        try:
            max_units = float(self.max_position_size) / entry_price
        except Exception:
            max_units = 0
        position_size = min(position_size, max_units)

        # Apply balance constraint (include small fee buffer)
        try:
            available_balance = float(self.user.balance or 0)
        except Exception:
            available_balance = 0

        try:
            max_affordable = available_balance / (entry_price * 1.001)
        except Exception:
            max_affordable = 0

        position_size = min(position_size, max_affordable)

        logger.info(f"Calculated position size: {position_size} for {symbol}")
        return position_size
    
    def calculate_stop_loss(self, entry_price, side, percentage=0.02):
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price
            side: 'buy' or 'sell'
            percentage: Stop loss percentage (default 2%)
            
        Returns:
            Stop loss price
        """
        try:
            entry_price = float(entry_price)
            percentage = float(percentage)
        except Exception:
            logger.warning("Invalid numeric input to calculate_stop_loss")
            return entry_price

        if side == 'buy':
            return entry_price * (1 - percentage)
        else:
            return entry_price * (1 + percentage)
    
    def calculate_take_profit(self, entry_price, side, risk_reward_ratio=2):
        """
        Calculate take profit price based on risk/reward ratio
        
        Args:
            entry_price: Entry price
            side: 'buy' or 'sell'
            risk_reward_ratio: Risk/reward ratio (default 2:1)
            
        Returns:
            Take profit price
        """
        try:
            entry_price = float(entry_price)
            risk_reward_ratio = float(risk_reward_ratio)
        except Exception:
            logger.warning("Invalid numeric input to calculate_take_profit")
            return entry_price

        stop_loss = self.calculate_stop_loss(entry_price, side)
        try:
            risk = abs(entry_price - float(stop_loss))
        except Exception:
            return entry_price

        if side == 'buy':
            return entry_price + (risk * risk_reward_ratio)
        else:
            return entry_price - (risk * risk_reward_ratio)
    
    def check_margin_call(self):
        """
        Check if account is at risk of margin call
        
        Returns:
            Tuple of (is_at_risk, margin_level)
        """
        total_equity = self._calculate_total_equity() or 0
        margin_used = self._calculate_margin_used()

        try:
            margin_used = float(margin_used)
        except Exception:
            margin_used = 0

        if margin_used == 0:
            return False, 0

        try:
            margin_level = (total_equity / margin_used) * 100
        except Exception:
            margin_level = 0

        # Margin call at 120% level
        if margin_level < 120:
            logger.warning(f"Margin call risk for user {self.user_id}: {margin_level:.2f}%")
            return True, margin_level

        return False, margin_level
    
    def get_risk_metrics(self):
        """
        Get comprehensive risk metrics
        
        Returns:
            Dict of risk metrics
        """
        total_equity = self._calculate_total_equity() or 0
        margin_call_risk, margin_level = self.check_margin_call()

        try:
            available_balance = float(self.user.balance or 0)
        except Exception:
            available_balance = 0

        open_positions = Position.query.filter_by(user_id=self.user_id).count()

        daily_loss = self._calculate_daily_loss()
        drawdown = self._calculate_drawdown()

        return {
            'user_id': self.user_id,
            'total_equity': round(total_equity, 2),
            'available_balance': round(available_balance, 2),
            'open_positions': open_positions,
            'max_positions': self.max_open_positions,
            'daily_loss': round(daily_loss, 2),
            'max_daily_loss': self.max_daily_loss,
            'daily_loss_percent': round((daily_loss / self.max_daily_loss * 100), 2) if self.max_daily_loss > 0 else 0,
            'drawdown': round(drawdown, 4),
            'max_drawdown': self.max_drawdown,
            'drawdown_percent': round((drawdown / self.max_drawdown * 100), 2) if self.max_drawdown > 0 else 0,
            'margin_level': margin_level,
            'margin_call_risk': margin_call_risk,
            'risk_per_trade': self.risk_per_trade * 100,
            'max_position_size': self.max_position_size,
            'peak_equity': round(self._get_peak_equity(), 2)
        }
    
    def _calculate_total_equity(self):
        """Calculate total account equity"""
        positions = Position.query.filter_by(user_id=self.user_id).all()
        positions_value = 0
        for p in positions:
            try:
                qty = float(getattr(p, 'quantity', 0) or 0)
                price = float(getattr(p, 'current_price', 0) or 0)
            except Exception:
                qty = 0
                price = 0
            positions_value += qty * price

        try:
            user_balance = float(getattr(self.user, 'balance', 0) or 0)
        except Exception:
            user_balance = 0

        return user_balance + positions_value
    
    def _calculate_margin_used(self):
        """Calculate total margin used"""
        positions = Position.query.filter_by(user_id=self.user_id).all()
        total = 0
        for p in positions:
            try:
                qty = float(getattr(p, 'quantity', 0) or 0)
                entry = float(getattr(p, 'entry_price', 0) or 0)
            except Exception:
                qty = 0
                entry = 0
            total += qty * entry
        return total
    
    def _calculate_daily_loss(self):
        """Calculate today's total losses"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        daily_loss = db.session.query(func.sum(Trade.profit_loss)).filter(
            Trade.user_id == self.user_id,
            Trade.timestamp >= today,
            Trade.status == 'filled',
            Trade.profit_loss < 0
        ).scalar() or 0
        
        return abs(daily_loss)
    
    def _calculate_drawdown(self):
        """Calculate current drawdown from peak"""
        current_equity = self._calculate_total_equity()
        peak_equity = self._get_peak_equity()
        
        if peak_equity == 0:
            return 0
        
        return max(0, (peak_equity - current_equity) / peak_equity)
    
    def _get_peak_equity(self):
        """Get historical peak equity"""
        # Simplified - should track actual peak in database
        # For now, use starting balance as peak
        return max(10000, self._calculate_total_equity())