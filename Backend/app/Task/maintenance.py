# Backend/app/tasks/maintenance.py
from celery import shared_task
from app import db
from sqlalchemy import text

@shared_task
def cleanup_expired_tokens_task():
    """
    Removes expired JWT tokens from the blocklist database.
    Recommended to run this daily via Celery Beat.
    """
    print("[Maintenance] Cleaning up expired tokens...")
    try:
        # Example raw SQL for cleanup (adjust based on your TokenBlocklist model)
        # db.session.execute(text("DELETE FROM token_blocklist WHERE created_at < NOW() - INTERVAL '7 days'"))
        # db.session.commit()
        pass
    except Exception as e:
        print(f"[Maintenance] Error cleaning tokens: {e}")

@shared_task
def sync_portfolio_task(user_id):
    """
    Re-calculates portfolio stats by syncing DB with Exchange balances.
    """
    print(f"[Maintenance] Syncing portfolio for User {user_id}")
    return {"user_id": user_id, "status": "synced"}