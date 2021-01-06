from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, current_user

from app.blueprints.admin import bp
from app.blueprints.recipes.errors import error_response
from app.blueprints.recipes.helpers import paginated_recipes_jsonify
from app.blueprints.recipes.schemas import recipe_schema
from app.services.recipes import get_pending_recipes, get_recipe, accept_recipe, reject_recipe
from app.services.search import reindex_es


@bp.route('/recipes/<int:pk>/accept', methods=['GET'])
@jwt_required
def accept(pk):
    if current_user.admin:
        recipe = get_recipe(pk)
        accepted_recipe = accept_recipe(recipe)
        result = recipe_schema.dump(accepted_recipe)
        return jsonify({"message": "Recipe accepted!",
                        "recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/recipes/<int:pk>/reject', methods=['GET'])
@jwt_required
def reject(pk):
    if current_user.admin:
        recipe = get_recipe(pk)
        accepted_recipe = reject_recipe(recipe)
        result = recipe_schema.dump(accepted_recipe)
        return jsonify({"message": "Recipe rejected!",
                        "recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/recipes/pending', methods=['GET'])
@jwt_required
def pending_recipes():
    if current_user.admin:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
        recipes = get_pending_recipes(page=page, per_page=per_page)
        return paginated_recipes_jsonify(recipes, page, per_page, endpoint='.pending_recipes')
    else:
        return error_response(401)

@bp.route('/search/reindex')
@jwt_required
def reindex():  # TODO tests
    if current_user.admin:
        reindex_es()
        return jsonify({'message': 'Done!'}), 200
    return error_response(401)
