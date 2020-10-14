from flask import Blueprint, current_app
from flask_jwt_extended import JWTManager

from app.services import get_user_by_name

bp = Blueprint('api_auth', __name__)

current_app.config['JWT_SECRET_KEY'] = current_app.config['SECRET_KEY']
jwt = JWTManager(current_app)
jwt.user_loader_callback_loader(get_user_by_name)

from app.api_auth import routes
