from flask import Blueprint

bp = Blueprint('api_admin', __name__)

from app.blueprints.api_admin import routes
