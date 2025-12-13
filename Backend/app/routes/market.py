from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
import random

market_bp = Blueprint('market', __name__)

@market_bp.route('/price/<symbol>', methods=['GET'])
@jwt_required()
def get_price(symbol):
    base_price = random.uniform(100, 500)
    change = random.uniform(-10, 10)
    
    return jsonify({
        'symbol': symbol.upper(),
        'price': round(base_price, 2),
        'change': round(change, 2),
        'change_percent': round((change / base_price * 100), 2),
        'volume': round(random.uniform(100000, 1000000), 2),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@market_bp.route('/quotes', methods=['POST'])
@jwt_required()
def get_quotes():
    data = request.get_json()
    symbols = data.get('symbols', [])
    
    quotes = []
    for symbol in symbols:
        base_price = random.uniform(100, 500)
        change = random.uniform(-10, 10)
        quotes.append({
            'symbol': symbol.upper(),
            'price': round(base_price, 2),
            'change': round(change, 2),
            'change_percent': round((change / base_price * 100), 2),
            'volume': round(random.uniform(100000, 1000000), 2)
        })
    
    return jsonify(quotes), 200

@market_bp.route('/orderbook/<symbol>', methods=['GET'])
@jwt_required()
def get_orderbook(symbol):
    base_price = random.uniform(100, 105)
    
    bids = [[round(base_price - i * 0.1, 2), round(random.uniform(10, 100), 2)] for i in range(10)]
    asks = [[round(base_price + i * 0.1, 2), round(random.uniform(10, 100), 2)] for i in range(10)]
    
    return jsonify({
        'symbol': symbol.upper(),
        'bids': bids,
        'asks': asks,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@market_bp.route('/candles/<symbol>', methods=['GET'])
@jwt_required()
def get_candles(symbol):
    interval = request.args.get('interval', '1h')
    limit = int(request.args.get('limit', 100))
    
    candles = []
    base_price = random.uniform(100, 200)
    
    for i in range(limit):
        open_price = base_price
        high_price = open_price + random.uniform(0, 5)
        low_price = open_price - random.uniform(0, 5)
        close_price = random.uniform(low_price, high_price)
        
        candles.append({
            'timestamp': (datetime.utcnow() - timedelta(hours=limit-i)).isoformat(),
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': round(random.uniform(1000, 10000), 2)
        })
        
        base_price = close_price
    
    return jsonify({
        'symbol': symbol.upper(),
        'interval': interval,
        'candles': candles
    }), 200

@market_bp.route('/ticker', methods=['GET'])
@jwt_required()
def get_ticker():
    symbols = ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD', 'ADAUSD']
    
    tickers = []
    for symbol in symbols:
        base_price = random.uniform(100, 1000)
        change = random.uniform(-50, 50)
        tickers.append({
            'symbol': symbol,
            'price': round(base_price, 2),
            'change': round(change, 2),
            'change_percent': round((change / base_price * 100), 2),
            'high_24h': round(base_price + random.uniform(0, 20), 2),
            'low_24h': round(base_price - random.uniform(0, 20), 2),
            'volume_24h': round(random.uniform(1000000, 10000000), 2)
        })
    
    return jsonify(tickers), 200