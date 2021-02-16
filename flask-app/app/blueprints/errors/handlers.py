from app import db
from app.blueprints.recipes.errors import error_response as api_error_response
from app.blueprints.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return api_error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return api_error_response(500)


@bp.app_errorhandler(401)
def forbidden_error(error):
    return api_error_response(401)
