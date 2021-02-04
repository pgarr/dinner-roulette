from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, current_user, jwt_optional, get_current_user
from marshmallow import ValidationError

from app.blueprints.recipes import bp
from app.blueprints.recipes.errors import error_response, bad_request
from app.blueprints.recipes.helpers import paginated_recipes_jsonify, save_recipe_from_schema
from app.blueprints.recipes.schemas import recipe_schema
from app.models.recipes import StatusEnum
from app.services.recipes import get_accepted_recipes, get_user_recipes, get_recipe, init_recipe


@bp.route('/', methods=['GET'])
def connection():
    return jsonify({'message': 'API is online!'}), 200


@bp.route('/recipes', methods=['GET'])
def recipes():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    recipe_models = get_accepted_recipes(page=page, per_page=per_page)
    return paginated_recipes_jsonify(recipe_models, page, per_page, endpoint='.recipes', items_name='recipes')


@bp.route('/recipes/my', methods=['GET'])
@jwt_required
def my_recipes():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    my_models = get_user_recipes(author=current_user, page=page, per_page=per_page)
    return paginated_recipes_jsonify(my_models, page, per_page, endpoint='.my_recipes', items_name='recipes')


@bp.route('/recipes/<int:pk>', methods=['GET'])
@jwt_optional
def recipe(pk):
    recipe_model = get_recipe(pk)
    if recipe_model.status == StatusEnum.accepted or recipe_model.is_author_or_admin(get_current_user()):
        result = recipe_schema.dump(recipe_model)
        return jsonify({'recipe': result})
    else:
        return error_response(401, "Unauthorized")


@bp.route('/recipes', methods=['POST'])
@jwt_required
def create_recipe():
    if not current_user:
        return error_response(401, "Unauthorized")

    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    try:
        data = recipe_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    model = init_recipe(author=current_user)
    model = save_recipe_from_schema(data, model)
    result = recipe_schema.dump(model)
    return jsonify({"message": "Recipe will be seen for other users after administrator acceptance.",
                    "recipe": result}), 201


@bp.route('/recipes/<int:pk>', methods=['PATCH'])
@jwt_required
def update_recipe(pk):
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    recipe_model = get_recipe(pk)
    if current_user == recipe_model.author or current_user.admin:
        try:
            data = recipe_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 422
        recipe_model = save_recipe_from_schema(data, recipe_model)
        result = recipe_schema.dump(recipe_model)
        return jsonify({"message": "Changes will be seen for other users after administrator acceptance.",
                        "recipe": result}), 200
    else:
        return error_response(401)
