from .extensions import socketio
from .views import session
from .chatbot import chatbot

@socketio.on("connect")
def handle_connection():
    session["client_id"] = {
        "openai_client" : chatbot.get_client(),
        "openai_thread" : chatbot.get_thread(chatbot.get_client()),
    }
    print("connected")

@socketio.on("disconnect")
def handle_disconnection():
    print("disconnected")

@socketio.on("message")
def handle_message(data):
    client = session["client_id"]
    chatbot.send_message(client["openai_client"], client["openai_thread"], data[0])
    response = chatbot.get_message(client["openai_client"], client["openai_thread"], data[1])
    parse_resp = chatbot.filter_messages(response)
    socketio.emit("Bot Response", parse_resp)
    print(data)