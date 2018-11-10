from flask_restful import Resource

from models.ingredient import IngredientModel


class Ingredient(Resource):

    def get(self, name):
        ingredient = IngredientModel.find_by_name(name)
        if ingredient:
            return ingredient.json()
        return {'message': 'Ingredient not found'}, 404


class IngredientList(Resource):
    def get(self):
        return {'ingredients': [ingredient.json() for ingredient in IngredientModel.query.all()]}
