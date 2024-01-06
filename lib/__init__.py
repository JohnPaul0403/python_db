from flask import Flask
import os
from .environments import UPLOAD_FOLDER, secret_key
from .routes import main
from .sockets import socketio

def create_app():
    app = Flask(__name__)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
    app.config["SECRET_KEY"] = secret_key
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["DEBUG"] = True
    app.config["PORT"] = 80
    app.register_blueprint(main, url_prefix="/")

    socketio.init_app(app)
    return app