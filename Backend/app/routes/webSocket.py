from flask_socketio import emit, join_room, leave_room
import random
import time
from threading import Thread

def register_socketio_events(socketio):
    
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected')
        emit('connected', {
            'message': 'Connected to trading bot WebSocket',
            'timestamp': time.time()
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'Client disconnected')
    
    @socketio.on('subscribe_market')
    def handle_subscribe(data):
        symbol = data.get('symbol', '').upper()
        if symbol:
            join_room(f'market_{symbol}')
            emit('subscribed', {
                'symbol': symbol,
                'message': f'Subscribed to {symbol} market data'
            })
    
    @socketio.on('unsubscribe_market')
    def handle_unsubscribe(data):
        symbol = data.get('symbol', '').upper()
        if symbol:
            leave_room(f'market_{symbol}')
            emit('unsubscribed', {
                'symbol': symbol,
                'message': f'Unsubscribed from {symbol} market data'
            })
    
    @socketio.on('subscribe_trades')
    def handle_subscribe_trades(data):
        user_id = data.get('user_id')
        if user_id:
            join_room(f'trades_{user_id}')
            emit('subscribed_trades', {
                'message': 'Subscribed to trade updates'
            })
    
    @socketio.on('subscribe_portfolio')
    def handle_subscribe_portfolio(data):
        user_id = data.get('user_id')
        if user_id:
            join_room(f'portfolio_{user_id}')
            emit('subscribed_portfolio', {
                'message': 'Subscribed to portfolio updates'
            })
    
    def broadcast_market_data():
        symbols = ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD', 'ADAUSD']
        prices = {s: random.uniform(100, 1000) for s in symbols}
        
        while True:
            for symbol in symbols:
                # Simulate price movement
                change = random.uniform(-5, 5)
                prices[symbol] += change
                prices[symbol] = max(prices[symbol], 50)  # Minimum price
                
                socketio.emit('market_update', {
                    'symbol': symbol,
                    'price': round(prices[symbol], 2),
                    'change': round(change, 2),
                    'change_percent': round((change / prices[symbol] * 100), 2),
                    'volume': round(random.uniform(1000, 10000), 2),
                    'timestamp': time.time()
                }, room=f'market_{symbol}')
            
            time.sleep(1)
    
    def broadcast_orderbook_updates():
        symbols = ['BTCUSD', 'ETHUSD', 'BNBUSD']
        
        while True:
            for symbol in symbols:
                base_price = random.uniform(100, 200)
                
                orderbook = {
                    'symbol': symbol,
                    'bids': [[round(base_price - i * 0.1, 2), round(random.uniform(1, 10), 2)] for i in range(5)],
                    'asks': [[round(base_price + i * 0.1, 2), round(random.uniform(1, 10), 2)] for i in range(5)],
                    'timestamp': time.time()
                }
                
                socketio.emit('orderbook_update', orderbook, room=f'market_{symbol}')
            
            time.sleep(2)
    
    # Start background threads
    market_thread = Thread(target=broadcast_market_data, daemon=True)
    market_thread.start()
    
    orderbook_thread = Thread(target=broadcast_orderbook_updates, daemon=True)
    orderbook_thread.start()
