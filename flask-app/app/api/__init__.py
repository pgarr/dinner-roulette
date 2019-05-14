from flask import Blueprint, current_app
from flask_jwt import JWT
from app.api import security

bp = Blueprint('api', __name__)

current_app.config['JWT_AUTH_URL_RULE'] = '/api/auth'  # TODO: zmienić hardcode na zależne od endpoint api
jwt = JWT(current_app, security.authenticate, security.identity)

from app.api import routes
