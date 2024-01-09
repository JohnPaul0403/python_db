from flask import Flask
import os
from .routes import main
from .sockets import socketio
from .settings import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(main, url_prefix="/")

    socketio.init_app(app)
    return app