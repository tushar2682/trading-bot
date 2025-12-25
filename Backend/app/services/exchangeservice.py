import ccxt
from app.models.api_key import ApiKey
from app.utils.encryption import encryption_service
from app.utils.exceptions import ExchangeException
from app import redis_client
import json
from datetime import timedelta

class ExchangeService:
    """Multi-exchange integration service using CCXT"""
    
    # Supported exchanges
    SUPPORTED_EXCHANGES = ['binance', 'coinbase', 'kraken', 'bybit', 'okx']
    
    def __init__(self, user_id=None):
        """
        Initialize exchange service
        
        Args:
            user_id: User ID for API key lookup
        """
        self.user_id = user_id
        self.exchanges = {}
        self.cache_timeout = 30  # seconds
    
    def get_exchange(self, exchange_name='binance', use_testnet=True):
        """
        Get or create exchange instance
        
        Args:
            exchange_name: Exchange name (binance, coinbase, etc.)
            use_testnet: Use testnet/sandbox mode
            
        Returns:
            CCXT exchange instance
            
        Raises:
            ExchangeException: If exchange creation fails
        """
        cache_key = f"{exchange_name}_{use_testnet}"
        
        # Return cached instance if exists
        if cache_key in self.exchanges:
            return self.exchanges[cache_key]
        
        # Validate exchange name
        if exchange_name not in self.SUPPORTED_EXCHANGES:
            raise ExchangeException(f"Unsupported exchange: {exchange_name}")
        
        try:
            # Get API keys from database if user_id provided
            api_key = None
            api_secret = None
            
            if self.user_id:
                api_key_record = ApiKey.query.filter_by(
                    user_id=self.user_id,
                    exchange=exchange_name,
                    is_active=True,
                    is_testnet=use_testnet
                ).first()
                
                if api_key_record:
                    api_key = encryption_service.decrypt(api_key_record.api_key)
                    api_secret = encryption_service.decrypt(api_key_record.api_secret)
            
            # Create exchange instance
            exchange_class = getattr(ccxt, exchange_name)
            
            config = {
                'enableRateLimit': True,
                'timeout': 30000,
                'options': {'defaultType': 'spot'}
            }
            
            # Add API credentials if available
            if api_key and api_secret:
                config['apiKey'] = api_key
                config['secret'] = api_secret
            
            # Configure testnet/sandbox
            if use_testnet:
                if exchange_name == 'binance':
                    config['urls'] = {
                        'api': {
                            'public': 'https://testnet.binance.vision/api',
                            'private': 'https://testnet.binance.vision/api',
                        }
                    }
                elif exchange_name == 'bybit':
                    config['urls'] = {
                        'api': {
                            'public': 'https://api-testnet.bybit.com',
                            'private': 'https://api-testnet.bybit.com',
                        }
                    }
            
            exchange = exchange_class(config)
            
            # Test connection by loading markets
            exchange.load_markets()
            
            # Cache the instance
            self.exchanges[cache_key] = exchange
            
            return exchange
            
        except ccxt.AuthenticationError as e:
            raise ExchangeException(f"Authentication failed: {str(e)}")
        except ccxt.ExchangeError as e:
            raise ExchangeException(f"Exchange error: {str(e)}")
        except Exception as e:
            raise ExchangeException(f"Failed to initialize exchange: {str(e)}")
    
    def place_order(self, symbol, side, order_type, quantity, price=None, 
                   stop_loss=None, take_profit=None, exchange_name='binance'):
        """
        Place order on exchange
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            side: 'buy' or 'sell'
            order_type: 'market', 'limit', or 'stop_loss'
            quantity: Order quantity
            price: Limit price (required for limit orders)
            stop_loss: Stop loss price
            take_profit: Take profit price
            exchange_name: Exchange name
            
        Returns:
            Order details dict
            
        Raises:
            ExchangeException: If order placement fails
        """
        try:
            exchange = self.get_exchange(exchange_name)
            
            # Validate parameters
            if side not in ['buy', 'sell']:
                raise ValueError("Side must be 'buy' or 'sell'")
            
            if order_type not in ['market', 'limit', 'stop_loss']:
                raise ValueError("Invalid order type")
            
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            # Place order based on type
            order = None
            
            if order_type == 'market':
                if side == 'buy':
                    order = exchange.create_market_buy_order(symbol, quantity)
                else:
                    order = exchange.create_market_sell_order(symbol, quantity)
                    
            elif order_type == 'limit':
                if not price:
                    raise ValueError("Price required for limit orders")
                if side == 'buy':
                    order = exchange.create_limit_buy_order(symbol, quantity, price)
                else:
                    order = exchange.create_limit_sell_order(symbol, quantity, price)
                    
            elif order_type == 'stop_loss':
                if not price:
                    raise ValueError("Price required for stop loss orders")
                params = {'stopPrice': price}
                if side == 'buy':
                    order = exchange.create_order(symbol, 'stop_loss', 'buy', quantity, price, params)
                else:
                    order = exchange.create_order(symbol, 'stop_loss', 'sell', quantity, price, params)
            
            # Add stop loss and take profit if provided
            if order and (stop_loss or take_profit):
                self._add_stop_orders(exchange, order['id'], symbol, side, quantity, stop_loss, take_profit)
            
            return self._format_order(order)
            
        except ccxt.InsufficientFunds as e:
            raise ExchangeException("Insufficient funds")
        except ccxt.InvalidOrder as e:
            raise ExchangeException(f"Invalid order: {str(e)}")
        except ccxt.ExchangeError as e:
            raise ExchangeException(f"Exchange error: {str(e)}")
        except Exception as e:
            raise ExchangeException(f"Failed to place order: {str(e)}")
    
    def cancel_order(self, order_id, symbol, exchange_name='binance'):
        """
        Cancel order
        
        Args:
            order_id: Order ID
            symbol: Trading pair
            exchange_name: Exchange name
            
        Returns:
            Cancellation result
        """
        try:
            exchange = self.get_exchange(exchange_name)
            result = exchange.cancel_order(order_id, symbol)
            return self._format_order(result)
        except Exception as e:
            raise ExchangeException(f"Failed to cancel order: {str(e)}")
    
    def get_order_status(self, order_id, symbol, exchange_name='binance'):
        """
        Get order status
        
        Args:
            order_id: Order ID
            symbol: Trading pair
            exchange_name: Exchange name
            
        Returns:
            Order status dict
        """
        try:
            exchange = self.get_exchange(exchange_name)
            order = exchange.fetch_order(order_id, symbol)
            return self._format_order(order)
        except Exception as e:
            raise ExchangeException(f"Failed to fetch order: {str(e)}")
    
    def get_balance(self, exchange_name='binance'):
        """
        Get account balance
        
        Args:
            exchange_name: Exchange name
            
        Returns:
            Balance dict
        """
        try:
            # Check cache first
            cache_key = f'balance:{self.user_id}:{exchange_name}'
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            exchange = self.get_exchange(exchange_name)
            balance = exchange.fetch_balance()
            
            result = {
                'exchange': exchange_name,
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used'],
                'timestamp': exchange.milliseconds()
            }
            
            # Cache for 30 seconds
            redis_client.setex(cache_key, self.cache_timeout, json.dumps(result))
            
            return result
            
        except Exception as e:
            raise ExchangeException(f"Failed to fetch balance: {str(e)}")
    
    def get_positions(self, exchange_name='binance'):
        """
        Get open positions (for futures/margin trading)
        
        Args:
            exchange_name: Exchange name
            
        Returns:
            List of positions
        """
        try:
            exchange = self.get_exchange(exchange_name)
            positions = exchange.fetch_positions()
            return [self._format_position(p) for p in positions if p['contracts'] > 0]
        except Exception as e:
            raise ExchangeException(f"Failed to fetch positions: {str(e)}")
    
    def get_open_orders(self, symbol=None, exchange_name='binance'):
        """
        Get open orders
        
        Args:
            symbol: Trading pair (optional, get all if None)
            exchange_name: Exchange name
            
        Returns:
            List of open orders
        """
        try:
            exchange = self.get_exchange(exchange_name)
            orders = exchange.fetch_open_orders(symbol)
            return [self._format_order(o) for o in orders]
        except Exception as e:
            raise ExchangeException(f"Failed to fetch open orders: {str(e)}")
    
    def _add_stop_orders(self, exchange, order_id, symbol, side, quantity, stop_loss, take_profit):
        """Add stop loss and take profit orders"""
        try:
            opposite_side = 'sell' if side == 'buy' else 'buy'
            
            if stop_loss:
                exchange.create_order(
                    symbol, 'stop_loss', opposite_side, quantity, stop_loss,
                    {'stopPrice': stop_loss}
                )
            
            if take_profit:
                exchange.create_order(
                    symbol, 'take_profit', opposite_side, quantity, take_profit,
                    {'stopPrice': take_profit}
                )
        except Exception as e:
            print(f"Failed to add stop orders: {str(e)}")
    
    def _format_order(self, order):
        """Format order data consistently"""
        if not order:
            return None
        
        return {
            'id': order.get('id'),
            'symbol': order.get('symbol'),
            'type': order.get('type'),
            'side': order.get('side'),
            'price': order.get('price'),
            'amount': order.get('amount'),
            'filled': order.get('filled', 0),
            'remaining': order.get('remaining', 0),
            'status': order.get('status'),
            'timestamp': order.get('timestamp'),
            'datetime': order.get('datetime'),
            'fee': order.get('fee'),
            'cost': order.get('cost'),
            'average': order.get('average')
        }
    
    def _format_position(self, position):
        """Format position data consistently"""
        return {
            'symbol': position.get('symbol'),
            'side': position.get('side'),
            'contracts': position.get('contracts'),
            'contractSize': position.get('contractSize'),
            'entryPrice': position.get('entryPrice'),
            'markPrice': position.get('markPrice'),
            'unrealizedPnl': position.get('unrealizedPnl'),
            'percentage': position.get('percentage'),
            'leverage': position.get('leverage'),
            'timestamp': position.get('timestamp')
        }

