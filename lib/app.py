from flask import Flask, render_template
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

def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return None