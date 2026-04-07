from flask import Flask
from flask_cors import CORS

from app.config.settings import Settings
from app.routes import register_routes

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
