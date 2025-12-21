# Backend/app/utils/constants.py

class OrderSide:
    BUY = 'BUY'
    SELL = 'SELL'

class OrderType:
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP_LOSS = 'STOP_LOSS'

class TradeStatus:
    PENDING = 'PENDING'
    FILLED = 'FILLED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class WorkflowStatus:
    IDLE = 'IDLE'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h', '1d']