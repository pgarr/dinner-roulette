from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from app.api import bp
from app.api.errors import error_response, bad_request
from app.api.schemas import recipes_schema, recipe_schema
from app.services import get_recipe, save_recipe, init_recipe
from app.models import Recipe, RecipeIngredient


@bp.route('/', methods=['GET'])
def connection():
    return jsonify({'message': 'API is online!'}), 200


@bp.route('/recipes', methods=['GET'])
def recipes():
    recipe_models = Recipe.query.all()
    result = recipes_schema.dump(recipe_models)
    return jsonify({'recipes': result.data})


@bp.route('/recipe/<int:pk>', methods=['GET'])
def recipe(pk):
    recipe_model = get_recipe(pk)
    result = recipe_schema.dump(recipe_model)
    return jsonify(
        {'recipe': result.data})


@bp.route('/recipe', methods=['POST'])
@jwt_required()
def create_recipe():
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    data, errors = recipe_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    recipe_model = init_recipe(current_identity)
    save_recipe_from_schema(data, recipe_model)
    recipe_model = get_recipe(recipe_model.id)
    result = recipe_schema.dump(recipe_model)
    return jsonify({"message": "Created new recipe.",
                    "recipe": result.data}), 201


@bp.route('/recipe/<int:pk>', methods=['PATCH'])
@jwt_required()
def update_recipe(pk):
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    recipe_model = get_recipe(pk)
    if current_identity == recipe_model.author:
        data, errors = recipe_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        save_recipe_from_schema(data, recipe_model)
        recipe_model = get_recipe(recipe_model.id)
        result = recipe_schema.dump(recipe_model)
        return jsonify({"message": "Recipe updated.",
                        "recipe": result.data}), 200
    else:
        return error_response(401)


def save_recipe_from_schema(data, model):
    # TODO: brak danego klucza oznacza KeyError exception

    model.title = data.get('title')
    model.time = data.get('time')
    model.difficulty = data.get('difficulty')
    model.detail.link = data.get('detail').get('link')
    model.detail.preparation = data.get('detail').get('preparation')
    model.ingredients = []
    for data_ingredient in data['ingredients']:
        recipe_ingredient_model = RecipeIngredient(**data_ingredient)
        model.ingredients.append(recipe_ingredient_model)
    save_recipe(model)
