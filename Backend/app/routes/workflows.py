from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.workflow import Workflow, WorkflowExecution
from app.services.workflow_executor import WorkflowExecutor
from datetime import datetime

bp = Blueprint('workflows', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_workflows():
    """
    Get all workflows for current user
    GET /api/workflows
    Query params: page, per_page
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        workflows = Workflow.query.filter_by(user_id=user_id)\
            .order_by(Workflow.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'workflows': [w.to_dict() for w in workflows.items],
            'total': workflows.total,
            'pages': workflows.pages,
            'current_page': workflows.page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_workflow():
    """
    Create a new workflow
    POST /api/workflows
    Body: {name, description, nodes, connections}
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Workflow name is required'}), 400
        
        workflow = Workflow(
            user_id=user_id,
            name=data['name'],
            description=data.get('description', ''),
            nodes=data.get('nodes', []),
            connections=data.get('connections', [])
        )
        
        db.session.add(workflow)
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow created successfully',
            'workflow': workflow.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>', methods=['GET'])
@jwt_required()
def get_workflow(workflow_id):
    """
    Get workflow by ID
    GET /api/workflows/:id
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        return jsonify(workflow.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>', methods=['PUT'])
@jwt_required()
def update_workflow(workflow_id):
    """
    Update workflow
    PUT /api/workflows/:id
    Body: {name, description, nodes, connections}
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            workflow.name = data['name']
        if 'description' in data:
            workflow.description = data['description']
        if 'nodes' in data:
            workflow.nodes = data['nodes']
        if 'connections' in data:
            workflow.connections = data['connections']
        
        workflow.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow updated successfully',
            'workflow': workflow.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>', methods=['DELETE'])
@jwt_required()
def delete_workflow(workflow_id):
    """
    Delete workflow
    DELETE /api/workflows/:id
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        db.session.delete(workflow)
        db.session.commit()
        
        return jsonify({'message': 'Workflow deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>/activate', methods=['POST'])
@jwt_required()
def activate_workflow(workflow_id):
    """
    Activate workflow
    POST /api/workflows/:id/activate
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        workflow.is_active = True
        db.session.commit()
        
        # Start workflow execution in background
        from app.tasks.trading_tasks import execute_workflow_task
        execute_workflow_task.delay(workflow_id)
        
        return jsonify({
            'message': 'Workflow activated successfully',
            'workflow': workflow.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>/deactivate', methods=['POST'])
@jwt_required()
def deactivate_workflow(workflow_id):
    """
    Deactivate workflow
    POST /api/workflows/:id/deactivate
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        workflow.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow deactivated successfully',
            'workflow': workflow.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>/execute', methods=['POST'])
@jwt_required()
def execute_workflow(workflow_id):
    """
    Execute workflow manually
    POST /api/workflows/:id/execute
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        # Execute workflow
        executor = WorkflowExecutor()
        result = executor.execute(workflow)
        
        return jsonify({
            'message': 'Workflow executed successfully',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:workflow_id>/executions', methods=['GET'])
@jwt_required()
def get_workflow_executions(workflow_id):
    """
    Get workflow execution history
    GET /api/workflows/:id/executions
    """
    try:
        user_id = get_jwt_identity()
        workflow = Workflow.query.filter_by(id=workflow_id, user_id=user_id).first()
        
        if not workflow:
            return jsonify({'error': 'Workflow not found'}), 404
        
        executions = WorkflowExecution.query.filter_by(workflow_id=workflow_id)\
            .order_by(WorkflowExecution.started_at.desc())\
            .limit(50).all()
        
        return jsonify({
            'executions': [e.to_dict() for e in executions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
