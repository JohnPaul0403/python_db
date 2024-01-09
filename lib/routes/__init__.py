import requests
from flask import Blueprint, flash, url_for, request, redirect, render_template, abort, session
from lib.extensions import os, json, GOOGLE_CLIENT_ID, flow, app_id_token, app_cachecontrol, my_requests, secure_filename, UPLOAD_FOLDER
from lib.users import auth_users
from lib.models import user_model, assistant_model, payments_models
from lib.payments import api_crud

main = Blueprint('main', __name__)

from . import auth_routes, views