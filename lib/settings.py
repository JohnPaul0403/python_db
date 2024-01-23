import os
from .environments import UPLOAD_FOLDER, get_keys
from dotenv import load_dotenv

get_keys()
load_dotenv()

class Config(object):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOAD_FOLDER = UPLOAD_FOLDER

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
