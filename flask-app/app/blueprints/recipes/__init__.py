from flask import Blueprint

bp = Blueprint('routes', __name__)

from app.blueprints.recipes import routes
