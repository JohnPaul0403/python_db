from . import socketio
from lib.payments import api_crud
@socketio.on("connect payment")
def handle_connection():
    """
    Handle a connection event from the socket.io connection.
    Parameters:
        None
    Returns:
        None
    """
    socketio.emit("connect payment", "Connected successfully!")

@socketio.on("payment disconnect")
def handle_disconnection():
    """
    Handle a disconnection event from the socket.io connection.
    Parameters:
        None
    Returns:
        None
    """
    socketio.emit("payment disconnect", "Disconnected successfully!")

@socketio.on("token")
def handle_token(data):
    """
    Handle a token event from the socket.io connection.
    Parameters:
        data (Any): The data received from the token event.
    Returns:
        None
    """
    print(data)
    body = {
        "source_id": data,
        "idempotency_key": "9658a52e-28c8-45d4-98f8-06882c92e736",
        "amount_money": {
            "amount": 100,
            "currency": "USD"
        }
    }
    client = api_crud.get_client()
    result = api_crud.create_payment(client, body)

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)