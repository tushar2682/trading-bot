
from celery import shared_task
from flask_socketio import SocketIO

# Connect to Redis message queue to emit events from this worker process
socketio = SocketIO(message_queue='redis://localhost:6379/0')

@shared_task
def send_notification_task(user_id, type, message, payload=None):
    """
    Sends async notifications to the user.
    Types: 'info', 'success', 'warning', 'error'
    """
    print(f"[Notification] Sending {type} to User {user_id}: {message}")
    
    # 1. Emit to Frontend via SocketIO
    # We broadcast to a specific room "user_{user_id}" 
    socketio.emit('notification', {
        'type': type,
        'message': message,
        'payload': payload
    }, room=f"user_{user_id}")
    
    # 2. (Optional) Send Email or Telegram
    # if type == 'critical': send_telegram_alert(...)
    
    return "Notification sent"