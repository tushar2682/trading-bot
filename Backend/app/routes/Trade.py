from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.trade import Trade
from app.models.user import User
from app.services.trading_engine import TradingEngine
from datetime import datetime, timedelta

bp = Blueprint('trades', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_trades():
    """
    Get all trades for current user
    GET /api/trades
    Query params: page, per_page, symbol, status, start_date, end_date
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        symbol = request.args.get('symbol')
        status = request.args.get('status')
        
        query = Trade.query.filter_by(user_id=user_id)
        
        if symbol:
            query = query.filter_by(symbol=symbol)
        if status:
            query = query.filter_by(status=status)
        
        trades = query.order_by(Trade.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'trades': [t.to_dict() for t in trades.items],
            'total': trades.total,
            'pages': trades.pages,
            'current_page': trades.page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_trade():
    """
    Create a new trade
    POST /api/trades
    Body: {symbol, side, type, quantity, price, stop_loss, take_profit}
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required = ['symbol', 'side', 'type', 'quantity']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate side
        if data['side'] not in ['buy', 'sell']:
            return jsonify({'error': 'Side must be buy or sell'}), 400
        
        # Validate type
        if data['type'] not in ['market', 'limit', 'stop_loss']:
            return jsonify({'error': 'Invalid trade type'}), 400
        
        # For limit orders, price is required
        if data['type'] == 'limit' and not data.get('price'):
            return jsonify({'error': 'Price required for limit orders'}), 400
        
        # Check user balance
        user = User.query.get(user_id)
        if data['side'] == 'buy':
            required_balance = data['quantity'] * data.get('price', 0)
            if user.balance < required_balance:
                return jsonify({'error': 'Insufficient balance'}), 400
        
        # Create trade using trading engine
        engine = TradingEngine()
        trade = engine.create_trade(
            user_id=user_id,
            symbol=data['symbol'],
            side=data['side'],
            trade_type=data['type'],
            quantity=data['quantity'],
            price=data.get('price'),
            stop_loss=data.get('stop_loss'),
            take_profit=data.get('take_profit')
        )
        
        return jsonify({
            'message': 'Trade created successfully',
            'trade': trade.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:trade_id>', methods=['GET'])
@jwt_required()
def get_trade(trade_id):
    """
    Get trade by ID
    GET /api/trades/:id
    """
    try:
        user_id = get_jwt_identity()
        trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        return jsonify(trade.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:trade_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_trade(trade_id):
    """
    Cancel a pending trade
    POST /api/trades/:id/cancel
    """
    try:
        user_id = get_jwt_identity()
        trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        if trade.status not in ['pending', 'partially_filled']:
            return jsonify({'error': 'Cannot cancel this trade'}), 400
        
        trade.status = 'canceled'
        trade.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Trade canceled successfully',
            'trade': trade.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_trade_history():
    """
    Get trade history with filters
    GET /api/trades/history
    Query params: days, symbol
    """
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', 30, type=int)
        symbol = request.args.get('symbol')
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = Trade.query.filter_by(user_id=user_id)\
            .filter(Trade.timestamp >= start_date)
        
        if symbol:
            query = query.filter_by(symbol=symbol)
        
        trades = query.order_by(Trade.timestamp.desc()).all()
        
        # Calculate statistics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t.profit_loss and t.profit_loss > 0])
        total_pnl = sum(t.profit_loss or 0 for t in trades)
        
        return jsonify({
            'trades': [t.to_dict() for t in trades],
            'statistics': {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': (winning_trades / total_trades * 100) if total_trades > 0 else 0,
                'total_pnl': total_pnl
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_trade_stats():
    """
    Get trading statistics
    GET /api/trades/stats
    """
    try:
        user_id = get_jwt_identity()
        
        # Get all filled trades
        trades = Trade.query.filter_by(user_id=user_id, status='filled').all()
        
        if not trades:
            return jsonify({
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_profit': 0,
                'total_loss': 0,
                'net_pnl': 0
            }), 200
        
        winning_trades = [t for t in trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in trades if t.profit_loss and t.profit_loss < 0]
        
        return jsonify({
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(trades) * 100,
            'total_profit': sum(t.profit_loss for t in winning_trades),
            'total_loss': sum(t.profit_loss for t in losing_trades),
            'net_pnl': sum(t.profit_loss or 0 for t in trades),
            'average_win': sum(t.profit_loss for t in winning_trades) / len(winning_trades) if winning_trades else 0,
            'average_loss': sum(t.profit_loss for t in losing_trades) / len(losing_trades) if losing_trades else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

