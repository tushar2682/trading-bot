"""Route registration helper for the `app.routes` package.

This module provides a single function `register_routes(app, socketio=None)`
that imports and registers available blueprints. Importing blueprints is
done lazily inside the function so the application factory can call it
without circular import issues.
"""
from typing import Optional
from flask import Flask


def register_routes(app: Flask, socketio: Optional[object] = None) -> None:
    """Import and register route blueprints found under `app.routes`.

    Only registers blueprints that exist; optional modules are imported
    inside try/except blocks so missing files don't break app startup.
    """
    # Required routes
    from .auth import bp as auth_bp
    from .workflows import bp as workflows_bp
    from .Trade import bp as trades_bp
    from .strategies import strategies_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(workflows_bp, url_prefix='/api/workflows')
    app.register_blueprint(trades_bp, url_prefix='/api/trades')
    app.register_blueprint(strategies_bp, url_prefix='/api/strategies')

    # Optional routes - register if present
    try:
        from .users import users_bp

        app.register_blueprint(users_bp, url_prefix='/api/users')
    except Exception:
        pass

    try:
        from .portfolio import portfolio_bp

        app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    except Exception:
        pass

    try:
        from .market import market_bp

        app.register_blueprint(market_bp, url_prefix='/api/market')
    except Exception:
        pass

    try:
        from .analytics import analytics_bp

        app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    except Exception:
        pass

    # Optional: socketio event registration
    if socketio is not None:
        try:
            from .websocket import register_socketio_events

            register_socketio_events(socketio)
        except Exception:
            pass

