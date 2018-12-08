from flask import request
from flask_jwt import jwt_required

from app.api import bp
from app.api.services import IngredientInfoService
from app.api.services import RecipeService


@bp.route('/recipes', methods=['GET'])
def get_recipes():
    ingredient = request.args.get('ingredient')
    if ingredient:
        return RecipeService.get_filtered(ingredient)
    else:
        return RecipeService.get_all()


@bp.route('/recipe/<int:pk>', methods=['GET'])
def get_recipe(pk):
    return RecipeService.get_by_pk(pk)


@bp.route('/recipe', methods=['POST'])
def create_recipe():
    json_data = request.get_json()
    return RecipeService.create(json_data)


@bp.route('/recipe/<int:pk>', methods=['PATCH'])
@jwt_required()
def update_recipe(pk):
    json_data = request.get_json()
    return RecipeService.update_by_pk(pk, json_data)


@bp.route('/recipe/<int:pk>', methods=['DELETE'])
@jwt_required()
def delete_recipe(pk):
    return RecipeService.delete_by_pk(pk)


@bp.route('/admin/ingredientinfos', methods=['GET'])
@jwt_required()
def get_ingredient_infos():
    return IngredientInfoService.get_all()


@bp.route('/admin/ingredientinfo/<int:pk>', methods=['GET'])
@jwt_required()
def get_ingredient_info(pk):
    return IngredientInfoService.get_by_pk(pk)


@bp.route('/admin/ingredientinfo', methods=['POST'])
@jwt_required()
def create_ingredient_info():
    json_data = request.get_json()
    return IngredientInfoService.create(json_data)


@bp.route('/admin/ingredientinfo/<int:pk>', methods=['PATCH'])
@jwt_required()
def update_ingredient_info(pk):
    json_data = request.get_json()
    return IngredientInfoService.update_by_pk(pk, json_data)


@bp.route('/admin/ingredientinfo/<int:pk>', methods=['DELETE'])
@jwt_required()
def delete_ingredient_info(pk):
    return IngredientInfoService.delete_by_pk(pk)
