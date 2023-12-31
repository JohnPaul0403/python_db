from .extensions import socketio

@socketio.on("connect")
def handle_connection():
    print("connected")