"""Technical Indicators Service"""
import numpy as np
import pandas as pd

class IndicatorService:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate RSI indicator"""
        prices = pd.Series(prices)
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50).tolist()
    
    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        prices = pd.Series(prices)
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return {
            'macd': macd.tolist(),
            'signal': signal_line.tolist(),
            'histogram': histogram.tolist()
        }
    
    @staticmethod
    def calculate_bollinger_bands(prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        prices = pd.Series(prices)
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return {
            'upper': upper_band.tolist(),
            'middle': sma.tolist(),
            'lower': lower_band.tolist()
        }
    
    @staticmethod
    def calculate_sma(prices, period=20):
        """Calculate Simple Moving Average"""
        prices = pd.Series(prices)
        return prices.rolling(window=period).mean().tolist()
    
    @staticmethod
    def calculate_ema(prices, period=20):
        """Calculate Exponential Moving Average"""
        prices = pd.Series(prices)
        return prices.ewm(span=period, adjust=False).mean().tolist()

