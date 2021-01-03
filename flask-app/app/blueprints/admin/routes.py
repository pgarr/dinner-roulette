from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, current_user

from app.blueprints.admin import bp
from app.blueprints.recipes.errors import error_response
from app.blueprints.recipes.helpers import paginated_recipes_jsonify
from app.blueprints.recipes.schemas import recipe_schema, waiting_schema
from app.services.recipes import get_waiting_recipe, accept_waiting, \
    reject_waiting, get_all_pending_waiting_recipes
from app.services.search import reindex_es


@bp.route('/waiting/<int:pk>/accept', methods=['GET'])
@jwt_required
def accept_recipe(pk):
    if current_user.admin:
        waiting_model = get_waiting_recipe(pk)
        recipe_model = accept_waiting(waiting_model)
        result = recipe_schema.dump(recipe_model)
        return jsonify({"message": "Recipe accepted!",
                        "recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/waiting/<int:pk>/reject', methods=['GET'])
@jwt_required
def reject_recipe(pk):
    if current_user.admin:
        waiting_model = get_waiting_recipe(pk)
        reject_waiting(waiting_model)
        result = waiting_schema.dump(waiting_model)
        return jsonify({"message": "Recipe rejected!",
                        "rejected_recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/waiting', methods=['GET'])
@jwt_required
def waiting_recipes():  # TODO tests
    if current_user.admin:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
        waitings_models = get_all_pending_waiting_recipes(page=page, per_page=per_page)
        return paginated_recipes_jsonify(waitings_models, page, per_page, endpoint='.waiting_recipes',
                                         items_name='pending_recipes', waiting=True)


@bp.route('/search/reindex')
@jwt_required
def reindex():  # TODO tests
    if current_user.admin:
        reindex_es()
        return jsonify({'message': 'Done!'}), 200
    return error_response(401)
