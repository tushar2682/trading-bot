from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
import redis
import os

# Initialize Redis client
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def rate_limit(max_requests=100, window=60):
    """
    Rate limiting middleware
    max_requests: maximum number of requests allowed
    window: time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get identifier (IP or user_id)
            identifier = getattr(request, 'user_id', None) or request.remote_addr
            key = f"rate_limit:{identifier}:{f.__name__}"
            
            try:
                current = redis_client.get(key)
                
                if current is None:
                    redis_client.setex(key, window, 1)
                elif int(current) >= max_requests:
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'retry_after': redis_client.ttl(key)
                    }), 429
                else:
                    redis_client.incr(key)
                
            except redis.RedisError:
                # If Redis fails, allow request but log error
                pass
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator