# Backend/app/tasks/market_task.py
from celery import shared_task
import random

@shared_task
def fetch_market_data_task(symbol, timeframe='1h'):
    """
    Fetches OHLCV data for a specific symbol.
    """
    print(f"[Market] Fetching {timeframe} data for {symbol}")
    
    # TODO: Fetch from Binance/Coinbase/AlphaVantage
    # Mock data
    current_price = 45000 + random.randint(-100, 100)
    
    return {
        "symbol": symbol,
        "price": current_price,
        "volume": 1200.5,
        "timestamp": "2025-12-21T09:30:00Z"
    }

@shared_task
def analyze_market_task(symbol, strategy_params):
    """
    Runs technical indicators (RSI, MACD) on fetched data.
    """
    print(f"[Market] Analyzing {symbol} with params: {strategy_params}")
    

    rsi_value = random.randint(30, 70)
    signal = "NEUTRAL"
    
    if rsi_value > 70:
        signal = "SELL"
    elif rsi_value < 30:
        signal = "BUY"
        
    return {
        "symbol": symbol,
        "rsi": rsi_value,
        "signal": signal
    }