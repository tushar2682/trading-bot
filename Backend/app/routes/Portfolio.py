from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from Backend.app.models.position import Position
from ..models import Portfolio
from .. import db
import random
portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/', methods=['GET'])
@jwt_required()
def get_portfolios():
   user_id = get_jwt_identity()
    positions = Position.query.filter_by(user_id=user_id).all()
    
    total_value = sum(p.quantity * (p.current_price or p.avg_price) for p in positions)
    total_cost = sum(p.quantity * p.avg_price for p in positions)
    total_pnl = total_value - total_cost
    
    return jsonify({
        'positions': [{
            'id': p.id,
            'symbol': p.symbol,
            'quantity': p.quantity,
            'avg_price': p.avg_price,
            'current_price': p.current_price,
            'market_value': p.quantity * (p.current_price or p.avg_price),
            'cost_basis': p.quantity * p.avg_price,
            'pnl': (p.current_price - p.avg_price) * p.quantity if p.current_price else 0,
            'pnl_percent': ((p.current_price - p.avg_price) / p.avg_price * 100) if p.current_price else 0,
            'updated_at': p.updated_at.isoformat()
        } for p in positions],
        'summary': {
            'total_value': round(total_value, 2),
            'total_cost': round(total_cost, 2),
            'total_pnl': round(total_pnl, 2),
            'total_pnl_percent': round((total_pnl / total_cost * 100) if total_cost > 0 else 0, 2),
            'position_count': len(positions)
        }
    }), 200

@portfolio_bp.route('/positions/<symbol>', methods=['GET'])
@jwt_required()
def get_position(symbol):
    user_id = get_jwt_identity()
    position = Position.query.filter_by(user_id=user_id, symbol=symbol.upper()).first_or_404()
    
    return jsonify({
        'id': position.id,
        'symbol': position.symbol,
        'quantity': position.quantity,
        'avg_price': position.avg_price,
        'current_price': position.current_price,
        'market_value': position.quantity * (position.current_price or position.avg_price),
        'pnl': (position.current_price - position.avg_price) * position.quantity if position.current_price else 0,
        'updated_at': position.updated_at.isoformat()
    }), 200

@portfolio_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_performance():
    user_id = get_jwt_identity()
    
    # Mock performance data
    performance = {
        'daily_return': round(random.uniform(-2, 3), 2),
        'weekly_return': round(random.uniform(-5, 8), 2),
        'monthly_return': round(random.uniform(-8, 15), 2),
        'ytd_return': round(random.uniform(5, 35), 2),
        'total_return': round(random.uniform(10, 50), 2)
    }
    
    return jsonify(performance), 200

@portfolio_bp.route('/allocation', methods=['GET'])
@jwt_required()
def get_allocation():
    user_id = get_jwt_identity()
    positions = Position.query.filter_by(user_id=user_id).all()
    
    total_value = sum(p.quantity * (p.current_price or p.avg_price) for p in positions)
    
    allocation = [{
        'symbol': p.symbol,
        'value': p.quantity * (p.current_price or p.avg_price),
        'percentage': (p.quantity * (p.current_price or p.avg_price) / total_value * 100) if total_value > 0 else 0
    } for p in positions]
    
    return jsonify(allocation), 200