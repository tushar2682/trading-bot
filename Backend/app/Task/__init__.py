# Backend/app/tasks/__init__.py

from .trading_task import place_order_task, check_order_status_task
from .market_task import fetch_market_data_task, analyze_market_task
from .notification_task import send_notification_task
from .maintenance import cleanup_expired_tokens_task, sync_portfolio_task

# List of all tasks for easier registration if needed
__all__ = [
    'place_order_task',
    'check_order_status_task',
    'fetch_market_data_task',
    'analyze_market_task',
    'send_notification_task',
    'cleanup_expired_tokens_task',
    'sync_portfolio_task'
]