import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.services.market_data_service import MarketDataService
from app.services.indicator_service import IndicatorService
import logging

logger = logging.getLogger(__name__)

class BacktestService:
    """Comprehensive backtesting engine"""
    
    def __init__(self):
        self.market_service = MarketDataService()
        self.indicator_service = IndicatorService()
    
    def run_backtest(self, strategy, symbol, start_date=None, end_date=None, 
                    initial_capital=10000, commission=0.001):
        """
        Run complete backtest for a strategy
        
        Args:
            strategy: Strategy object with type and parameters
            symbol: Trading symbol
            start_date: Backtest start date
            end_date: Backtest end date
            initial_capital: Starting capital
            commission: Commission per trade (0.001 = 0.1%)
            
        Returns:
            Detailed backtest results dict
        """
        logger.info(f"Starting backtest for {strategy.name} on {symbol}")
        
        # Set date range
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=365)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Fetch historical data
        try:
            candles = self.market_service.get_candles(symbol, interval='1h', limit=2000)
        except Exception as e:
            logger.error(f"Failed to fetch candles: {str(e)}")
            return {'error': f'Failed to fetch historical data: {str(e)}'}
        
        if not candles or len(candles) < 100:
            return {'error': 'Insufficient historical data'}
        
        # Convert to DataFrame
        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Calculate indicators
        df = self._add_indicators(df, strategy)
        
        # Generate signals based on strategy type
        if strategy.strategy_type == 'rsi':
            signals = self._backtest_rsi_strategy(df, strategy.parameters)
        elif strategy.strategy_type == 'macd':
            signals = self._backtest_macd_strategy(df, strategy.parameters)
        elif strategy.strategy_type == 'bollinger':
            signals = self._backtest_bollinger_strategy(df, strategy.parameters)
        elif strategy.strategy_type == 'moving_average':
            signals = self._backtest_ma_crossover_strategy(df, strategy.parameters)
        else:
            return {'error': f'Unsupported strategy type: {strategy.strategy_type}'}
        
        # Calculate performance metrics
        results = self._calculate_performance(
            df, signals, initial_capital, commission
        )
        
        logger.info(f"Backtest completed: {results['total_trades']} trades, {results['total_return']:.2f}% return")
        
        return results
    
    def _add_indicators(self, df, strategy):
        """Add technical indicators to dataframe"""
        prices = df['close'].values.tolist()
        
        # Always add price data
        df['returns'] = df['close'].pct_change()
        
        # Add strategy-specific indicators
        if strategy.strategy_type == 'rsi':
            period = strategy.parameters.get('period', 14)
            df['rsi'] = self.indicator_service.calculate_rsi(prices, period)
            
        elif strategy.strategy_type == 'macd':
            fast = strategy.parameters.get('fast', 12)
            slow = strategy.parameters.get('slow', 26)
            signal = strategy.parameters.get('signal', 9)
            macd_data = self.indicator_service.calculate_macd(prices, fast, slow, signal)
            df['macd'] = macd_data['macd']
            df['macd_signal'] = macd_data['signal']
            df['macd_histogram'] = macd_data['histogram']
            
        elif strategy.strategy_type == 'bollinger':
            period = strategy.parameters.get('period', 20)
            std_dev = strategy.parameters.get('std_dev', 2)
            bb_data = self.indicator_service.calculate_bollinger_bands(prices, period, std_dev)
            df['bb_upper'] = bb_data['upper']
            df['bb_middle'] = bb_data['middle']
            df['bb_lower'] = bb_data['lower']
            
        elif strategy.strategy_type == 'moving_average':
            fast_period = strategy.parameters.get('fast_period', 20)
            slow_period = strategy.parameters.get('slow_period', 50)
            df['sma_fast'] = self.indicator_service.calculate_sma(prices, fast_period)
            df['sma_slow'] = self.indicator_service.calculate_sma(prices, slow_period)
        
        return df
    
    def _backtest_rsi_strategy(self, df, parameters):
        """Backtest RSI strategy"""
        oversold = parameters.get('oversold', 30)
        overbought = parameters.get('overbought', 70)
        
        signals = []
        position = None
        entry_price = 0
        
        for idx, row in df.iterrows():
            if pd.isna(row['rsi']):
                continue
            
            # Buy signal: RSI crosses below oversold
            if row['rsi'] < oversold and position is None:
                signals.append({
                    'timestamp': idx,
                    'type': 'buy',
                    'price': row['close'],
                    'rsi': row['rsi']
                })
                position = 'long'
                entry_price = row['close']
            
            # Sell signal: RSI crosses above overbought
            elif row['rsi'] > overbought and position == 'long':
                profit_pct = ((row['close'] - entry_price) / entry_price) * 100
                signals.append({
                    'timestamp': idx,
                    'type': 'sell',
                    'price': row['close'],
                    'rsi': row['rsi'],
                    'profit_pct': profit_pct
                })
                position = None
        
        return signals
    
    def _backtest_macd_strategy(self, df, parameters):
        """Backtest MACD crossover strategy"""
        signals = []
        position = None
        entry_price = 0
        prev_macd = None
        prev_signal = None
        
        for idx, row in df.iterrows():
            if pd.isna(row['macd']) or pd.isna(row['macd_signal']):
                continue
            
            # Buy signal: MACD crosses above signal line
            if prev_macd is not None and prev_signal is not None:
                if prev_macd <= prev_signal and row['macd'] > row['macd_signal'] and position is None:
                    signals.append({
                        'timestamp': idx,
                        'type': 'buy',
                        'price': row['close'],
                        'macd': row['macd'],
                        'signal': row['macd_signal']
                    })
                    position = 'long'
                    entry_price = row['close']
                
                # Sell signal: MACD crosses below signal line
                elif prev_macd >= prev_signal and row['macd'] < row['macd_signal'] and position == 'long':
                    profit_pct = ((row['close'] - entry_price) / entry_price) * 100
                    signals.append({
                        'timestamp': idx,
                        'type': 'sell',
                        'price': row['close'],
                        'macd': row['macd'],
                        'signal': row['macd_signal'],
                        'profit_pct': profit_pct
                    })
                    position = None
            
            prev_macd = row['macd']
            prev_signal = row['macd_signal']
        
        return signals
    
    def _backtest_bollinger_strategy(self, df, parameters):
        """Backtest Bollinger Bands strategy"""
        signals = []
        position = None
        entry_price = 0
        
        for idx, row in df.iterrows():
            if pd.isna(row['bb_upper']) or pd.isna(row['bb_lower']):
                continue
            
            # Buy signal: Price touches or breaks below lower band
            if row['close'] <= row['bb_lower'] and position is None:
                signals.append({
                    'timestamp': idx,
                    'type': 'buy',
                    'price': row['close'],
                    'bb_lower': row['bb_lower']
                })
                position = 'long'
                entry_price = row['close']
            
            # Sell signal: Price touches or breaks above upper band
            elif row['close'] >= row['bb_upper'] and position == 'long':
                profit_pct = ((row['close'] - entry_price) / entry_price) * 100
                signals.append({
                    'timestamp': idx,
                    'type': 'sell',
                    'price': row['close'],
                    'bb_upper': row['bb_upper'],
                    'profit_pct': profit_pct
                })
                position = None
        
        return signals
    
    def _backtest_ma_crossover_strategy(self, df, parameters):
        """Backtest Moving Average crossover strategy"""
        signals = []
        position = None
        entry_price = 0
        
        for idx, row in df.iterrows():
            if pd.isna(row['sma_fast']) or pd.isna(row['sma_slow']):
                continue
            
            # Buy signal: Fast MA crosses above Slow MA
            if row['sma_fast'] > row['sma_slow'] and position is None:
                signals.append({
                    'timestamp': idx,
                    'type': 'buy',
                    'price': row['close']
                })
                position = 'long'
                entry_price = row['close']
            
            # Sell signal: Fast MA crosses below Slow MA
            elif row['sma_fast'] < row['sma_slow'] and position == 'long':
                profit_pct = ((row['close'] - entry_price) / entry_price) * 100
                signals.append({
                    'timestamp': idx,
                    'type': 'sell',
                    'price': row['close'],
                    'profit_pct': profit_pct
                })
                position = None
        
        return signals
    
    def _calculate_performance(self, df, signals, initial_capital, commission):
        """Calculate comprehensive performance metrics"""
        if not signals:
            return self._empty_results(initial_capital)
        
        # Initialize tracking variables
        capital = initial_capital
        equity_curve = [initial_capital]
        trades = []
        position_size = 0
        entry_price = 0
        entry_capital = 0
        
        # Process all signals
        for signal in signals:
            if signal['type'] == 'buy':
                # Buy with all available capital
                entry_capital = capital
                position_size = capital / signal['price']
                entry_price = signal['price']
                # Deduct commission
                capital *= (1 - commission)
                
            elif signal['type'] == 'sell' and position_size > 0:
                # Sell position
                exit_value = position_size * signal['price']
                # Deduct commission
                exit_value *= (1 - commission)
                
                # Calculate trade P&L
                profit = exit_value - entry_capital
                profit_pct = (profit / entry_capital) * 100
                
                # Update capital
                capital = exit_value
                equity_curve.append(capital)
                
                # Record trade
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': signal['price'],
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'capital': capital
                })
                
                # Reset position
                position_size = 0
        
        if not trades:
            return self._empty_results(initial_capital)
        
        # Calculate metrics
        winning_trades = [t for t in trades if t['profit'] > 0]
        losing_trades = [t for t in trades if t['profit'] < 0]
        
        total_return = ((capital - initial_capital) / initial_capital) * 100
        
        # Maximum drawdown
        peak = initial_capital
        max_dd = 0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak
            if dd > max_dd:
                max_dd = dd
        
        # Sharpe ratio (simplified - annualized)
        returns = [t['profit_pct'] for t in trades]
        if len(returns) > 1:
            sharpe = (np.mean(returns) / np.std(returns)) * np.sqrt(252/len(returns))
        else:
            sharpe = 0
        
        # Sortino ratio (downside risk)
        downside_returns = [r for r in returns if r < 0]
        if downside_returns:
            sortino = (np.mean(returns) / np.std(downside_returns)) * np.sqrt(252/len(returns))
        else:
            sortino = 0
        
        # Profit factor
        gross_profit = sum(t['profit'] for t in winning_trades)
        gross_loss = abs(sum(t['profit'] for t in losing_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        return {
            'initial_capital': initial_capital,
            'final_capital': capital,
            'total_return': total_return,
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(trades) * 100) if trades else 0,
            'avg_win': np.mean([t['profit'] for t in winning_trades]) if winning_trades else 0,
            'avg_loss': np.mean([t['profit'] for t in losing_trades]) if losing_trades else 0,
            'avg_win_pct': np.mean([t['profit_pct'] for t in winning_trades]) if winning_trades else 0,
            'avg_loss_pct': np.mean([t['profit_pct'] for t in losing_trades]) if losing_trades else 0,
            'largest_win': max([t['profit'] for t in winning_trades]) if winning_trades else 0,
            'largest_loss': min([t['profit'] for t in losing_trades]) if losing_trades else 0,
            'max_drawdown': max_dd * 100,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'profit_factor': profit_factor,
            'expectancy': sum([t['profit'] for t in trades]) / len(trades),
            'equity_curve': equity_curve,
            'trades_sample': trades[:20]  # Return first 20 trades
        }
    
    def _empty_results(self, initial_capital):
        """Return empty results structure"""
        return {
            'initial_capital': initial_capital,
            'final_capital': initial_capital,
            'total_return': 0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'profit_factor': 0,
            'equity_curve': [initial_capital],
            'trades_sample': []
        }
