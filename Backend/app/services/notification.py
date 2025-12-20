from app import db
from app.models.notification import Notification
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Comprehensive notification management system"""
    
    # Notification types
    TYPE_TRADE = 'trade'
    TYPE_ALERT = 'alert'
    TYPE_SYSTEM = 'system'
    TYPE_RISK = 'risk'
    TYPE_WORKFLOW = 'workflow'
    
    @staticmethod
    def create_notification(user_id, notification_type, title, message, metadata=None):
        """
        Create a notification
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            metadata: Optional additional data
            
        Returns:
            Notification object
        """
        try:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                is_read=False
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Emit via WebSocket if available
            NotificationService._emit_websocket(user_id, notification.to_dict())
            
            logger.info(f"Notification created for user {user_id}: {title}")
            return notification
            
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def notify_trade_executed(user_id, trade):
        """
        Send trade execution notification
        
        Args:
            user_id: User ID
            trade: Trade object
        """
        title = "Trade Executed"
        message = (
            f"{trade.side.upper()} {trade.quantity} {trade.symbol} "
            f"@ ${trade.price:.2f}"
        )
        
        if trade.status == 'filled':
            message += " - Order filled"
        elif trade.status == 'partially_filled':
            message += f" - Partially filled ({trade.filled_quantity}/{trade.quantity})"
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_TRADE,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_trade_failed(user_id, trade, reason):
        """
        Send trade failure notification
        
        Args:
            user_id: User ID
            trade: Trade object
            reason: Failure reason
        """
        title = "Trade Failed"
        message = (
            f"Failed to execute {trade.side.upper()} {trade.quantity} {trade.symbol}. "
            f"Reason: {reason}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_ALERT,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_position_closed(user_id, position, pnl):
        """
        Send position closed notification
        
        Args:
            user_id: User ID
            position: Position object
            pnl: Profit/Loss amount
        """
        title = "Position Closed"
        pnl_text = f"+${pnl:.2f}" if pnl > 0 else f"-${abs(pnl):.2f}"
        emoji = "🟢" if pnl > 0 else "🔴"
        
        message = (
            f"{emoji} Closed {position.symbol} position. "
            f"Quantity: {position.quantity}, "
            f"P&L: {pnl_text}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_TRADE,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_stop_loss_triggered(user_id, position):
        """
        Send stop loss triggered notification
        
        Args:
            user_id: User ID
            position: Position object
        """
        title = "🛑 Stop Loss Triggered"
        message = (
            f"Stop loss triggered for {position.symbol}. "
            f"Current price: ${position.current_price:.2f}, "
            f"Stop loss: ${position.stop_loss:.2f}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_ALERT,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_take_profit_triggered(user_id, position):
        """
        Send take profit triggered notification
        
        Args:
            user_id: User ID
            position: Position object
        """
        title = "🎯 Take Profit Triggered"
        message = (
            f"Take profit triggered for {position.symbol}. "
            f"Current price: ${position.current_price:.2f}, "
            f"Take profit: ${position.take_profit:.2f}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_ALERT,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_workflow_completed(user_id, workflow_name, status, result=None):
        """
        Send workflow completion notification
        
        Args:
            user_id: User ID
            workflow_name: Workflow name
            status: Execution status
            result: Optional execution result
        """
        title = "Workflow Completed"
        emoji = "✅" if status == 'completed' else "❌"
        
        message = f"{emoji} Workflow '{workflow_name}' {status}"
        
        if result:
            message += f". Result: {result}"
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_WORKFLOW,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_workflow_failed(user_id, workflow_name, error):
        """
        Send workflow failure notification
        
        Args:
            user_id: User ID
            workflow_name: Workflow name
            error: Error message
        """
        title = "⚠️ Workflow Failed"
        message = (
            f"Workflow '{workflow_name}' failed. "
            f"Error: {error}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_SYSTEM,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_risk_alert(user_id, alert_type, message, severity='warning'):
        """
        Send risk management alert
        
        Args:
            user_id: User ID
            alert_type: Type of risk alert
            message: Alert message
            severity: Alert severity (warning, critical)
        """
        emoji = "⚠️" if severity == 'warning' else "🚨"
        title = f"{emoji} Risk Alert: {alert_type}"
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_RISK,
            title=title,
            message=message
        )
    
    @staticmethod
    def notify_daily_loss_limit(user_id, current_loss, limit):
        """
        Send daily loss limit alert
        
        Args:
            user_id: User ID
            current_loss: Current daily loss
            limit: Loss limit
        """
        return NotificationService.notify_risk_alert(
            user_id=user_id,
            alert_type='Daily Loss Limit',
            message=f"Daily loss (${current_loss:.2f}) approaching limit (${limit:.2f})",
            severity='warning' if current_loss < limit * 0.9 else 'critical'
        )
    
    @staticmethod
    def notify_max_drawdown(user_id, current_drawdown, max_drawdown):
        """
        Send maximum drawdown alert
        
        Args:
            user_id: User ID
            current_drawdown: Current drawdown percentage
            max_drawdown: Maximum allowed drawdown
        """
        return NotificationService.notify_risk_alert(
            user_id=user_id,
            alert_type='Maximum Drawdown',
            message=f"Drawdown ({current_drawdown:.1f}%) approaching limit ({max_drawdown:.1f}%)",
            severity='critical'
        )
    
    @staticmethod
    def notify_margin_call_risk(user_id, margin_level):
        """
        Send margin call risk alert
        
        Args:
            user_id: User ID
            margin_level: Current margin level percentage
        """
        return NotificationService.notify_risk_alert(
            user_id=user_id,
            alert_type='Margin Call Risk',
            message=f"Margin level at {margin_level:.2f}%. Risk of margin call!",
            severity='critical'
        )
    
    @staticmethod
    def notify_price_alert(user_id, symbol, current_price, target_price, condition):
        """
        Send price alert notification
        
        Args:
            user_id: User ID
            symbol: Trading symbol
            current_price: Current price
            target_price: Target/Alert price
            condition: Price condition ('above' or 'below')
        """
        title = f"🔔 Price Alert: {symbol}"
        message = (
            f"{symbol} is now {condition} ${target_price:.2f}. "
            f"Current price: ${current_price:.2f}"
        )
        
        return NotificationService.create_notification(
            user_id=user_id,
            notification_type=NotificationService.TYPE_ALERT,
            title=title,
            message=message
        )
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False, limit=50):
        """
        Get user notifications
        
        Args:
            user_id: User ID
            unread_only: Return only unread notifications
            limit: Maximum number of notifications
            
        Returns:
            List of notifications
        """
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        notifications = query.order_by(
            Notification.created_at.desc()
        ).limit(limit).all()
        
        return [n.to_dict() for n in notifications]
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """
        Mark notification as read
        
        Args:
            notification_id: Notification ID
            user_id: User ID
        """
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def mark_all_as_read(user_id):
        """
        Mark all notifications as read
        
        Args:
            user_id: User ID
        """
        Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """
        Delete notification
        
        Args:
            notification_id: Notification ID
            user_id: User ID
        """
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def get_unread_count(user_id):
        """
        Get count of unread notifications
        
        Args:
            user_id: User ID
            
        Returns:
            Count of unread notifications
        """
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
    
    @staticmethod
    def _emit_websocket(user_id, notification_data):
        """
        Emit notification via WebSocket
        
        Args:
            user_id: User ID
            notification_data: Notification data dict
        """
        try:
            from app.routes.websocket import emit_notification
            emit_notification(user_id, notification_data)
        except ImportError:
            # WebSocket module not available
            pass
        except Exception as e:
            logger.error(f"Failed to emit WebSocket notification: {str(e)}")

