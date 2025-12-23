import logging
from flask import request, g
import time
import json

def setup_logging(app):
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/trading_bot.log'),
            logging.StreamHandler()
        ]
    )
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', str(time.time()))
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            log_request(request, response, elapsed)
        return response
    
    return app


def log_request(req, response, elapsed):
    """Log request details"""
    logger = logging.getLogger('request_logger')
    
    log_data = {
        'request_id': getattr(g, 'request_id', 'unknown'),
        'method': req.method,
        'path': req.path,
        'status': response.status_code,
        'duration_ms': round(elapsed * 1000, 2),
        'ip': req.remote_addr,
        'user_agent': req.headers.get('User-Agent', 'unknown')
    }
    
    if hasattr(req, 'user_id'):
        log_data['user_id'] = req.user_id
    
    logger.info(json.dumps(log_data))
