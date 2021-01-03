from flask import Blueprint, current_app
from flask_jwt_extended import JWTManager

from app.services.auth import get_user_by_name

bp = Blueprint('auth', __name__)

current_app.config['JWT_SECRET_KEY'] = current_app.config['SECRET_KEY']
jwt = JWTManager(current_app)
jwt.user_loader_callback_loader(get_user_by_name)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'is_admin': user.admin}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


from app.blueprints.auth import routes
