# Backend/app/tasks/trading_task.py
import time
from celery import shared_task
from app import db
# from app.models import Trade, User (Import your models here)

@shared_task(bind=True, max_retries=3)
def place_order_task(self, user_id, symbol, side, quantity, order_type='MARKET', price=None):
    """
    Executes a trade order on the exchange.
    """
    try:
        print(f"[Trading] Placing {side} order for {quantity} {symbol} (User: {user_id})")
     
        time.sleep(1)
        
        # Mock Result
        trade_id = f"ord_{int(time.time())}"
        fill_price = price if price else 45000.00  # Mock price
        
        # TODO: Save Trade to Database
        # trade = Trade(user_id=user_id, symbol=symbol, ...)
        # db.session.add(trade)
        # db.session.commit()
        
        return {
            "status": "filled",
            "trade_id": trade_id,
            "price": fill_price,
            "symbol": symbol
        }

    except Exception as e:
        print(f"[Trading] Order failed: {e}")
        
        raise self.retry(exc=e, countdown=5)

@shared_task
def check_order_status_task(order_id):
    """
    Periodically checks the status of an open order.
    """
    print(f"[Trading] Checking status for Order ID: {order_id}")

    return {"order_id": order_id, "status": "closed", "filled": True}