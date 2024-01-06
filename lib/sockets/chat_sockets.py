from . import socketio, user_model, session, chatbot

@socketio.on("connect")
def handle_connection():
    """
    Handles a connection event from the client.
    This function is triggered when a client connects to the server via socket.io. It sets the client ID in the session and initializes the necessary objects for handling chatbot communication. It also emits the username to the client and prints a message to indicate that the connection was successful.
    Parameters:
        None
    Returns:
        None
    """
    client = chatbot.get_client()
    session["client_id"] = {
        "openai_client" : client,
        "openai_thread" : chatbot.get_thread(client=client),
    }
    user = user_model.from_json(session["user"])
    socketio.emit("Username", user.name)
    socketio.emit("assistant", session["assistant"])
    print("connected")

@socketio.on("disconnect")
def handle_disconnection():
    print("disconnected")

@socketio.on("message")
def handle_message(data):
    """
    Handle a message event from the socket.io connection.
    Parameters:
        data (Any): The data received from the message event.
    Returns:
        None
    """
    client = session["client_id"]
    chatbot.send_message(client["openai_client"], client["openai_thread"], data[0])
    response = chatbot.get_message(client["openai_client"], client["openai_thread"], data[1])
    parse_resp = chatbot.filter_messages(response)
    socketio.emit("Bot Response", parse_resp)
    print(data)