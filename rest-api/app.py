from flask import Flask, request
from db import db
from services.recipe import RecipeService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'


@app.route('/recipes', methods=['GET'])
def get_recipes():
    ingredient = request.args.get('ingredient')
    if ingredient:
        return RecipeService.get_filtered(ingredient)
    else:
        return RecipeService.get_all()


@app.route('/recipe/<int:pk>', methods=['GET'])
def get_recipe(pk):
    return RecipeService.get_by_pk(pk)


@app.route('/recipe', methods=['POST'])
def new_recipe():
    json_data = request.get_json()
    return RecipeService.create(json_data)


@app.route('/recipe/<int:pk>', methods=['PATCH'])
def update_recipe(pk):
    json_data = request.get_json()
    return RecipeService.update_by_pk(pk, json_data)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
