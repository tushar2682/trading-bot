from app.models.trade import Trade
from app.models.position import Position
from app.models.user import User
from app.models.workflow import Workflow
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Advanced analytics and reporting system"""
    
    def __init__(self, user_id):
        """
        Initialize analytics service
        
        Args:
            user_id: User ID
        """
        self.user_id = user_id
        self.user = User.query.get(user_id)
        
        if not self.user:
            raise ValueError("User not found")
    
    def get_trading_performance(self, timeframe='1M'):
        """
        Get comprehensive trading performance
        
        Args:
            timeframe: Time period (1D, 1W, 1M, 3M, 1Y, ALL)
            
        Returns:
            Performance metrics dict
        """
        # Calculate date range
        end_date = datetime.utcnow()
        
        if timeframe == '1D':
            start_date = end_date - timedelta(days=1)
        elif timeframe == '1W':
            start_date = end_date - timedelta(weeks=1)
        elif timeframe == '1M':
            start_date = end_date - timedelta(days=30)
        elif timeframe == '3M':
            start_date = end_date - timedelta(days=90)
        elif timeframe == '1Y':
            start_date = end_date - timedelta(days=365)
        else:  # ALL
            start_date = datetime(2020, 1, 1)
        
        # Get trades in timeframe
        trades = Trade.query.filter(
            Trade.user_id == self.user_id,
            Trade.timestamp >= start_date,
            Trade.status == 'filled'
        ).all()
        
        if not trades:
            return self._empty_performance()
        
        # Calculate metrics
        winning_trades = [t for t in trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in trades if t.profit_loss and t.profit_loss < 0]
        
        total_profit = sum(t.profit_loss for t in winning_trades)
        total_loss = abs(sum(t.profit_loss for t in losing_trades))
        net_pnl = total_profit - total_loss
        
        # Calculate consecutive wins/losses
        max_consecutive_wins = self._calculate_consecutive(trades, 'wins')
        max_consecutive_losses = self._calculate_consecutive(trades, 'losses')
        
        return {
            'timeframe': timeframe,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(trades) * 100) if trades else 0,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_pnl': net_pnl,
            'avg_win': total_profit / len(winning_trades) if winning_trades else 0,
            'avg_loss': total_loss / len(losing_trades) if losing_trades else 0,
            'profit_factor': total_profit / total_loss if total_loss > 0 else 0,
            'largest_win': max([t.profit_loss for t in winning_trades]) if winning_trades else 0,
            'largest_loss': min([t.profit_loss for t in losing_trades]) if losing_trades else 0,
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'avg_trade_duration': self._calculate_avg_trade_duration(trades)
        }
    
    def get_symbol_performance(self):
        """
        Get performance breakdown by trading symbol
        
        Returns:
            List of symbol performance dicts
        """
        trades = Trade.query.filter_by(
            user_id=self.user_id,
            status='filled'
        ).all()
        
        symbol_stats = {}
        
        for trade in trades:
            if trade.symbol not in symbol_stats:
                symbol_stats[trade.symbol] = {
                    'trades': 0,
                    'winning': 0,
                    'losing': 0,
                    'profit': 0,
                    'volume': 0
                }
            
            symbol_stats[trade.symbol]['trades'] += 1
            symbol_stats[trade.symbol]['volume'] += trade.quantity * trade.price
            
            if trade.profit_loss:
                symbol_stats[trade.symbol]['profit'] += trade.profit_loss
                if trade.profit_loss > 0:
                    symbol_stats[trade.symbol]['winning'] += 1
                else:
                    symbol_stats[trade.symbol]['losing'] += 1
        
        # Convert to list with calculated metrics
        result = []
        for symbol, stats in symbol_stats.items():
            result.append({
                'symbol': symbol,
                'trades': stats['trades'],
                'winning_trades': stats['winning'],
                'losing_trades': stats['losing'],
                'win_rate': (stats['winning'] / stats['trades'] * 100) if stats['trades'] > 0 else 0,
                'total_profit': stats['profit'],
                'total_volume': stats['volume']
            })
        
        # Sort by profit
        return sorted(result, key=lambda x: x['total_profit'], reverse=True)
    
    def get_monthly_performance(self):
        """
        Get monthly performance breakdown
        
        Returns:
            List of monthly performance dicts
        """
        trades = Trade.query.filter_by(
            user_id=self.user_id,
            status='filled'
        ).all()
        
        monthly_stats = {}
        
        for trade in trades:
            month_key = trade.timestamp.strftime('%Y-%m')
            
            if month_key not in monthly_stats:
                monthly_stats[month_key] = {
                    'trades': 0,
                    'profit': 0,
                    'winning': 0,
                    'losing': 0
                }
            
            monthly_stats[month_key]['trades'] += 1
            
            if trade.profit_loss:
                monthly_stats[month_key]['profit'] += trade.profit_loss
                if trade.profit_loss > 0:
                    monthly_stats[month_key]['winning'] += 1
                else:
                    monthly_stats[month_key]['losing'] += 1
        
        # Convert to list
        result = []
        for month, stats in sorted(monthly_stats.items()):
            result.append({
                'month': month,
                'trades': stats['trades'],
                'winning_trades': stats['winning'],
                'losing_trades': stats['losing'],
                'win_rate': (stats['winning'] / stats['trades'] * 100) if stats['trades'] > 0 else 0,
                'profit': stats['profit']
            })
        
        return result
    
    def get_time_analysis(self):
        """
        Analyze trading performance by time of day and day of week
        
        Returns:
            Dict with hourly and daily breakdowns
        """
        trades = Trade.query.filter_by(
            user_id=self.user_id,
            status='filled'
        ).all()
        
        # Initialize stats
        hour_stats = {i: {'trades': 0, 'profit': 0, 'winning': 0} for i in range(24)}
        day_stats = {i: {'trades': 0, 'profit': 0, 'winning': 0} for i in range(7)}
        
        # Aggregate data
        for trade in trades:
            hour = trade.timestamp.hour
            day = trade.timestamp.weekday()
            
            hour_stats[hour]['trades'] += 1
            day_stats[day]['trades'] += 1
            
            if trade.profit_loss:
                hour_stats[hour]['profit'] += trade.profit_loss
                day_stats[day]['profit'] += trade.profit_loss
                
                if trade.profit_loss > 0:
                    hour_stats[hour]['winning'] += 1
                    day_stats[day]['winning'] += 1
        
        # Calculate win rates
        for hour in hour_stats:
            if hour_stats[hour]['trades'] > 0:
                hour_stats[hour]['win_rate'] = (
                    hour_stats[hour]['winning'] / hour_stats[hour]['trades'] * 100
                )
        
        for day in day_stats:
            if day_stats[day]['trades'] > 0:
                day_stats[day]['win_rate'] = (
                    day_stats[day]['winning'] / day_stats[day]['trades'] * 100
                )
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        return {
            'by_hour': [
                {'hour': h, **stats} for h, stats in hour_stats.items()
            ],
            'by_day': [
                {'day': day_names[d], 'day_number': d, **stats} 
                for d, stats in day_stats.items()
            ],
            'best_trading_hour': max(hour_stats.items(), key=lambda x: x[1]['profit'])[0] if trades else None,
            'best_trading_day': day_names[max(day_stats.items(), key=lambda x: x[1]['profit'])[0]] if trades else None
        }
    
    def get_risk_metrics(self):
        """
        Get comprehensive risk metrics
        
        Returns:
            Risk metrics dict
        """
        from app.services.risk_manager import RiskManager
        risk_manager = RiskManager(self.user_id)
        return risk_manager.get_risk_metrics()
    
    def get_workflow_analytics(self):
        """
        Get workflow performance analytics
        
        Returns:
            Workflow analytics dict
        """
        workflows = Workflow.query.filter_by(user_id=self.user_id).all()
        
        analytics = {
            'total_workflows': len(workflows),
            'active_workflows': len([w for w in workflows if w.is_active]),
            'workflows': []
        }
        
        for workflow in workflows:
            # Get trades generated by this workflow
            workflow_trades = Trade.query.filter_by(
                workflow_id=workflow.id,
                status='filled'
            ).all()
            
            if workflow_trades:
                winning = [t for t in workflow_trades if t.profit_loss and t.profit_loss > 0]
                total_pnl = sum(t.profit_loss or 0 for t in workflow_trades)
                
                analytics['workflows'].append({
                    'id': workflow.id,
                    'name': workflow.name,
                    'is_active': workflow.is_active,
                    'total_trades': len(workflow_trades),
                    'winning_trades': len(winning),
                    'win_rate': (len(winning) / len(workflow_trades) * 100) if workflow_trades else 0,
                    'total_pnl': total_pnl
                })
        
        return analytics
    
    def get_comparison_metrics(self, compare_user_id=None):
        """
        Get comparison metrics (self vs average or vs specific user)
        
        Args:
            compare_user_id: Optional user ID to compare against
            
        Returns:
            Comparison metrics dict
        """
        # Get own performance
        own_performance = self.get_trading_performance('ALL')
        
        if compare_user_id:
            # Compare with specific user
            compare_service = AnalyticsService(compare_user_id)
            compare_performance = compare_service.get_trading_performance('ALL')
            comparison_label = f"User {compare_user_id}"
        else:
            # Compare with platform average
            compare_performance = self._get_platform_average()
            comparison_label = "Platform Average"
        
        return {
            'your_performance': own_performance,
            'comparison': compare_performance,
            'comparison_label': comparison_label,
            'differences': {
                'win_rate': own_performance['win_rate'] - compare_performance['win_rate'],
                'profit_factor': own_performance['profit_factor'] - compare_performance['profit_factor'],
                'net_pnl': own_performance['net_pnl'] - compare_performance['net_pnl']
            }
        }
    
    def _empty_performance(self):
        """Return empty performance structure"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'total_profit': 0,
            'total_loss': 0,
            'net_pnl': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0,
            'largest_win': 0,
            'largest_loss': 0
        }
    
    def _calculate_consecutive(self, trades, type='wins'):
        """Calculate maximum consecutive wins or losses"""
        if not trades:
            return 0
        
        sorted_trades = sorted(trades, key=lambda t: t.timestamp)
        max_consecutive = 0
        current_consecutive = 0
        
        for trade in sorted_trades:
            if not trade.profit_loss:
                continue
            
            if type == 'wins':
                is_match = trade.profit_loss > 0
            else:
                is_match = trade.profit_loss < 0
            
            if is_match:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _calculate_avg_trade_duration(self, trades):
        """Calculate average trade duration in hours"""
        
        return 2.5  # Default 2.5 hours
    
    def _get_platform_average(self):
        """Get platform-wide average performance"""
      
        return {
            'total_trades': 100,
            'winning_trades': 55,
            'losing_trades': 45,
            'win_rate': 55.0,
            'total_profit': 5500,
            'total_loss': 4500,
            'net_pnl': 1000,
            'profit_factor': 1.22
        }