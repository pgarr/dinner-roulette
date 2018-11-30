from flask import Flask, request
from db import db
from services.ingredient_info import IngredientInfoService
from services.recipe import RecipeService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    ingredient = request.args.get('ingredient')
    if ingredient:
        return RecipeService.get_filtered(ingredient)
    else:
        return RecipeService.get_all()


@app.route('/api/recipe/<int:pk>', methods=['GET'])
def get_recipe(pk):
    return RecipeService.get_by_pk(pk)


@app.route('/api/recipe', methods=['POST'])
def create_recipe():
    json_data = request.get_json()
    return RecipeService.create(json_data)


@app.route('/api/recipe/<int:pk>', methods=['PATCH'])
def update_recipe(pk):
    json_data = request.get_json()
    return RecipeService.update_by_pk(pk, json_data)


@app.route('/api/recipe/<int:pk>', methods=['DELETE'])
def delete_recipe(pk):
    return RecipeService.delete_by_pk(pk)


@app.route('/api/admin/ingredientinfos', methods=['GET'])
def get_ingredient_infos():
    return IngredientInfoService.get_all()


@app.route('/api/admin/ingredientinfo/<int:pk>', methods=['GET'])
def get_ingredient_info(pk):
    return IngredientInfoService.get_by_pk(pk)


@app.route('/api/admin/ingredientinfo/<string:name>', methods=['GET'])
def get_ingredient_info(name):
    return IngredientInfoService.get_by_name(name)


@app.route('/api/admin/ingredientinfo', methods=['POST'])
def create_ingredient_info():
    json_data = request.get_json()
    return IngredientInfoService.create(json_data)


@app.route('/api/admin/ingredientinfo/<int:pk>', methods=['PATCH'])
def update_ingredient_info(pk):
    json_data = request.get_json()
    return IngredientInfoService.update_by_pk(pk, json_data)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
