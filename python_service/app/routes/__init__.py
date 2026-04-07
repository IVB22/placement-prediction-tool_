from flask import Flask

from .health_route import health_bp
from .match_route import match_bp
from .history_route import history_bp

def register_routes(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(history_bp)
