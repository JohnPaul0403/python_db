#imports
import json
import os

#Getting data from json
def get_secret_key():
    return get_json()["web"]["client_secret"]

def get_client_id():
    return get_json()["web"]["client_id"]

#Opening json file
def get_json():
    with open(path) as file:
        return json.load(file)

#json path
path = "lib/environments/secret_key.json"
UPLOAD_FOLDER = "temp"

#Access keys
client_id = get_client_id()
secret_key = get_secret_key()

def get_keys():
    os.environ['chat_gpt_model'] = "gpt-3.5-turbo"
    os.environ["SECRET_KEY"] = secret_key

scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

#urls
authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
redirect_uri = "http://localhost/callback"
