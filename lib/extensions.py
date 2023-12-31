from flask_socketio import SocketIO
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from pip._vendor import cachecontrol
from .environments import environments as env
import os
import pathlib

socketio = SocketIO()

GOOGLE_CLIENT_ID = env.client_id
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "environments/secret_key.json")
app_id_token = id_token
app_cachecontrol = cachecontrol
my_requests = google.auth.transport.requests

flow = Flow.from_client_secrets_file(
    client_secrets_file = client_secrets_file,
    scopes = env.scopes,
    redirect_uri = env.redirect_uri
)