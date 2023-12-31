from flask import Flask
import os
from .environments import environments as env
from .views import main
from .events import socketio

def create_app():
    app = Flask(__name__)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
    app.config["SECRET_KEY"] = env.secret_key
    app.config["DEBUG"] = True
    app.config["PORT"] = 80
    app.register_blueprint(main)

    socketio.init_app(app)
    return app