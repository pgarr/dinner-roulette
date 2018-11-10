from flask_restful import Resource, request

from db import db
from models.ingredient import IngredientModel
from models.recipe import RecipeModel
from models.recipe_ingredient import RecipeIngredientModel


class Recipe(Resource):

    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {'message': "An recipe with name '{}' already exist.".format(name)}, 400

        data = request.get_json()

        recipe = RecipeModel(name)

        try:
            recipe.save_to_db()
        except:
            return {'message': "An error occurred inserting recipe."}, 500

        for temp_ingredient in data['ingredients']:
            name = temp_ingredient['name']
            ingredient = IngredientModel.find_by_name(name)
            if not ingredient:
                ingredient = IngredientModel(name)
            association = RecipeIngredientModel(amount=temp_ingredient['amount'], unit=temp_ingredient['unit'])
            association.ingredient = ingredient
            recipe.ingredients.append(association)
            db.session.commit()

        return recipe.json(), 201

class RecipeList(Resource):
    def get(self):
        return {'recipes': [recipe.lazy_json() for recipe in RecipeModel.query.all()]}
