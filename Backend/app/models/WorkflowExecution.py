from app import db
from datetime import datetime


class WorkflowExecution(db.Model):
    __tablename__ = 'workflow_executions'

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    logs = db.Column(db.JSON, default=list)
    result = db.Column(db.JSON)
    error_message = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'logs': self.logs,
            'result': self.result,
            'error_message': self.error_message
        }