import os
from .environments import UPLOAD_FOLDER, get_keys

get_keys()

class Config(object):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOAD_FOLDER = UPLOAD_FOLDER

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
