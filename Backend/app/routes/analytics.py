from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from ..models import Trade
import random

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_analytics():
    user_id = get_jwt_identity()
    
    trades = Trade.query.filter_by(user_id=user_id, status='EXECUTED').all()
    total_trades = len(trades)
    
    analytics = {
        'total_trades': total_trades,
        'win_rate': round(random.uniform(50, 70), 2),
        'avg_profit': round(random.uniform(100, 500), 2),
        'avg_loss': round(random.uniform(-300, -50), 2),
        'profit_factor': round(random.uniform(1.2, 2.5), 2),
        'sharpe_ratio': round(random.uniform(1, 2.5), 2),
        'sortino_ratio': round(random.uniform(1.5, 3), 2),
        'max_drawdown': round(random.uniform(-15, -5), 2),
        'max_drawdown_duration': random.randint(5, 30),
        'total_pnl': round(random.uniform(1000, 10000), 2)
    }
    
    return jsonify(analytics), 200

@analytics_bp.route('/equity-curve', methods=['GET'])
@jwt_required()
def get_equity_curve():
    days = int(request.args.get('days', 30))
    
    curve = []
    value = 10000
    
    for i in range(days):
        value *= (1 + random.uniform(-0.02, 0.03))
        curve.append({
            'date': (datetime.utcnow() - timedelta(days=days-i)).isoformat(),
            'value': round(value, 2)
        })
    
    return jsonify(curve), 200

@analytics_bp.route('/risk-metrics', methods=['GET'])
@jwt_required()
def get_risk_metrics():
    metrics = {
        'var_95': round(random.uniform(-1000, -500), 2),
        'cvar_95': round(random.uniform(-1500, -1000), 2),
        'var_99': round(random.uniform(-1500, -1000), 2),
        'beta': round(random.uniform(0.8, 1.2), 2),
        'alpha': round(random.uniform(-0.5, 0.5), 2),
        'correlation_spy': round(random.uniform(0.5, 0.9), 2),
        'volatility': round(random.uniform(10, 30), 2),
        'downside_deviation': round(random.uniform(5, 15), 2)
    }
    
    return jsonify(metrics), 200

@analytics_bp.route('/trade-distribution', methods=['GET'])
@jwt_required()
def get_trade_distribution():
    distribution = {
        'by_symbol': [
            {'symbol': 'BTCUSD', 'count': random.randint(10, 50), 'pnl': round(random.uniform(-1000, 2000), 2)},
            {'symbol': 'ETHUSD', 'count': random.randint(10, 50), 'pnl': round(random.uniform(-1000, 2000), 2)},
            {'symbol': 'BNBUSD', 'count': random.randint(10, 50), 'pnl': round(random.uniform(-1000, 2000), 2)}
        ],
        'by_hour': [
            {'hour': h, 'count': random.randint(0, 10)} for h in range(24)
        ],
        'by_day': [
            {'day': d, 'count': random.randint(5, 30)} for d in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ]
    }
    
    return jsonify(distribution), 200

@analytics_bp.route('/monthly-summary', methods=['GET'])
@jwt_required()
def get_monthly_summary():
    months = []
    
    for i in range(12):
        month_date = datetime.utcnow() - timedelta(days=30*i)
        months.append({
            'month': month_date.strftime('%Y-%m'),
            'pnl': round(random.uniform(-500, 2000), 2),
            'trades': random.randint(10, 50),
            'win_rate': round(random.uniform(40, 70), 2),
            'sharpe': round(random.uniform(0.5, 2.5), 2)
        })
    
    return jsonify(months[::-1]), 200
