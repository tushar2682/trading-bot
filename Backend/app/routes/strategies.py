from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Strategy
from .. import db
import random

strategies_bp = Blueprint('strategies', __name__)

@strategies_bp.route('/', methods=['GET'])
@jwt_required()
def get_strategies():
    user_id = get_jwt_identity()
    strategies = Strategy.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'type': s.type,
        'parameters': s.parameters,
        'is_active': s.is_active,
        'created_at': s.created_at.isoformat()
    } for s in strategies]), 200

@strategies_bp.route('/<int:strategy_id>', methods=['GET'])
@jwt_required()
def get_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    
    return jsonify({
        'id': strategy.id,
        'name': strategy.name,
        'type': strategy.type,
        'parameters': strategy.parameters,
        'is_active': strategy.is_active,
        'created_at': strategy.created_at.isoformat()
    }), 200

@strategies_bp.route('/', methods=['POST'])
@jwt_required()
def create_strategy():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    strategy = Strategy(
        user_id=user_id,
        name=data['name'],
        type=data['type'],
        parameters=data.get('parameters', {})
    )
    
    db.session.add(strategy)
    db.session.commit()
    
    return jsonify({
        'id': strategy.id,
        'message': 'Strategy created successfully'
    }), 201

@strategies_bp.route('/<int:strategy_id>', methods=['PUT'])
@jwt_required()
def update_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    if 'name' in data:
        strategy.name = data['name']
    if 'type' in data:
        strategy.type = data['type']
    if 'parameters' in data:
        strategy.parameters = data['parameters']
    
    db.session.commit()
    return jsonify({'message': 'Strategy updated successfully'}), 200

@strategies_bp.route('/<int:strategy_id>', methods=['DELETE'])
@jwt_required()
def delete_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    db.session.delete(strategy)
    db.session.commit()
    return jsonify({'message': 'Strategy deleted successfully'}), 200

@strategies_bp.route('/<int:strategy_id>/activate', methods=['POST'])
@jwt_required()
def activate_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    strategy.is_active = True
    db.session.commit()
    return jsonify({'message': 'Strategy activated'}), 200

@strategies_bp.route('/<int:strategy_id>/deactivate', methods=['POST'])
@jwt_required()
def deactivate_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    strategy.is_active = False
    db.session.commit()
    return jsonify({'message': 'Strategy deactivated'}), 200

@strategies_bp.route('/<int:strategy_id>/backtest', methods=['POST'])
@jwt_required()
def backtest_strategy(strategy_id):
    user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    # Mock backtest results
    results = {
        'strategy_id': strategy.id,
        'strategy_name': strategy.name,
        'period': data.get('period', '1Y'),
        'total_return': round(random.uniform(5, 30), 2),
        'annual_return': round(random.uniform(10, 25), 2),
        'sharpe_ratio': round(random.uniform(1.2, 2.5), 2),
        'sortino_ratio': round(random.uniform(1.5, 3.0), 2),
        'max_drawdown': round(random.uniform(-15, -5), 2),
        'win_rate': round(random.uniform(50, 70), 2),
        'total_trades': random.randint(50, 200),
        'profitable_trades': random.randint(30, 140)
    }
    
    return jsonify(results), 200
