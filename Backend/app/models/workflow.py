from app import db
from datetime import datetime
class Workflow(db.Model):
    __tablename__ = "workflows"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    nodes = db.Column(db.JSON, nullable=False)
    connections = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    executions = db.relationship('WorkflowExecution', backref='workflow', lazy='dynamic', cascade='all, delete-orphan')
    trades= db.relationship('Trade', backref='workflow', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'nodes': self.nodes,
            'connections': self.connections,
            'is_active': self.is_active,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    