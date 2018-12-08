from flask import Blueprint, current_app
from flask_jwt import JWT

bp = Blueprint('api', __name__)

from app.api import routes, services, security

jwt = JWT(current_app, security.authenticate, security.identity)
