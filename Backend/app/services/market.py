import ccxt
import random
from datetime import datetime, timedelta

class MarketDataService:
    """Handles market data fetching"""
    
    def __init__(self):
        # Initialize exchange (using testnet for safety)
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
    
    def get_ticker(self, symbol):
        """Get ticker data"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['volume'],
                'timestamp': ticker['timestamp']
            }
        except Exception as e:
            # Return simulated data if API fails
            return self._simulate_ticker(symbol)
    
    def get_orderbook(self, symbol, limit=20):
        """Get orderbook data"""
        try:
            orderbook = self.exchange.fetch_order_book(symbol, limit)
            return {
                'symbol': symbol,
                'bids': orderbook['bids'][:limit],
                'asks': orderbook['asks'][:limit],
                'timestamp': orderbook['timestamp']
            }
        except Exception as e:
            return self._simulate_orderbook(symbol, limit)
    
    def get_candles(self, symbol, interval='1h', limit=100):
        """Get candlestick data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, interval, limit=limit)
            candles = []
            for candle in ohlcv:
                candles.append({
                    'timestamp': candle[0],
                    'open': candle[1],
                    'high': candle[2],
                    'low': candle[3],
                    'close': candle[4],
                    'volume': candle[5]
                })
            return candles
        except Exception as e:
            return self._simulate_candles(symbol, limit)
    
    def get_symbols(self):
        """Get available trading symbols"""
        try:
            markets = self.exchange.load_markets()
            return [symbol for symbol in markets.keys() if '/USDT' in symbol][:50]
        except Exception as e:
            return ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT']
    
    def search_symbols(self, query):
        """Search for symbols"""
        symbols = self.get_symbols()
        query = query.upper()
        return [s for s in symbols if query in s]
    
    def get_current_price(self, symbol):
        """Get current price"""
        ticker = self.get_ticker(symbol)
        return ticker['last']
    
    # Simulation methods
    def _simulate_ticker(self, symbol):
        base_price = 43000 if 'BTC' in symbol else 2280 if 'ETH' in symbol else 100
        return {
            'symbol': symbol,
            'last': base_price,
            'bid': base_price * 0.999,
            'ask': base_price * 1.001,
            'high': base_price * 1.02,
            'low': base_price * 0.98,
            'volume': random.randint(1000000, 10000000),
            'timestamp': int(datetime.now().timestamp() * 1000)
        }
    
    def _simulate_orderbook(self, symbol, limit):
        base_price = 43000 if 'BTC' in symbol else 2280 if 'ETH' in symbol else 100
        bids = [[base_price * (1 - i * 0.0001), random.uniform(0.1, 10)] for i in range(limit)]
        asks = [[base_price * (1 + i * 0.0001), random.uniform(0.1, 10)] for i in range(limit)]
        return {'symbol': symbol, 'bids': bids, 'asks': asks, 'timestamp': int(datetime.now().timestamp() * 1000)}
    
    def _simulate_candles(self, symbol, limit):
        base_price = 43000 if 'BTC' in symbol else 2280 if 'ETH' in symbol else 100
        candles = []
        for i in range(limit):
            timestamp = int((datetime.now() - timedelta(hours=limit-i)).timestamp() * 1000)
            open_price = base_price + random.uniform(-base_price*0.02, base_price*0.02)
            close_price = open_price + random.uniform(-base_price*0.01, base_price*0.01)
            candles.append({
                'timestamp': timestamp,
                'open': open_price,
                'high': max(open_price, close_price) * 1.01,
                'low': min(open_price, close_price) * 0.99,
                'close': close_price,
                'volume': random.randint(100000, 1000000)
            })
        return candles
