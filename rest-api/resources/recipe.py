from flask_restful import Resource, request

from db import db
from models.ingredient import IngredientModel
from models.recipe import RecipeModel
from models.recipe_detail import RecipeDetailModel
from models.recipe_ingredient import RecipeIngredientModel


class Recipe(Resource):

    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json_with_lazy()
        return {'message': 'Recipe not found'}, 404

    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {'message': "An recipe with name '{}' already exist.".format(name)}, 400
        data = request.get_json()
        try:
            recipe = self.save_new(name, data)
        except:
            return {'message': "An error occurred during inserting recipe."}, 500
        return recipe.json_with_lazy(), 201

    def put(self, name):
        data = request.get_json()
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            # try:
                new_recipe = self.update(recipe, data)
            # except:
            #     return {'message': "An error occurred during updating recipe."}, 500
        else:
            try:
                new_recipe = self.save_new(name, data)
            except:
                return {'message': "An error occurred inserting during recipe."}, 500
        return new_recipe.json_with_lazy(), 201

    @classmethod
    def save_new(cls, name, data):
        recipe = RecipeModel(name)
        recipe_detail = RecipeDetailModel(data['detail']['link'], data['detail']['description'])
        recipe.detail = recipe_detail

        for temp_ingredient in data['ingredients']:
            name = temp_ingredient['name']
            amount = temp_ingredient['amount']
            unit = temp_ingredient['unit']
            association = cls.create_new_ingredient_association(name, amount, unit)  # TODO: kwargs
            recipe.ingredients.append(association)
        recipe.save_to_db()
        return recipe

    @classmethod
    def update(cls, recipe, data):
        # update wartości działą
        # zmiana powiązań wyrzuca "Dependency rule tried to blank-out primary key column 'recipe_ingredient.recipe_id'"
        # chyba lepiej podzielić zmianę na 3 etapy:
        # usunięcie zbędnych powiązań, aktualizacja starych, dodanie nowych
        # chyba dobrze zacząć od stworzenia prawidłowego association proxy a potem zabawa
        recipe.detail.link = data['detail']['link']
        recipe.detail.description = data['detail']['description']

        new_ingredients = []
        for temp_ingredient in data['ingredients']:
            name = temp_ingredient['name']
            amount = temp_ingredient['amount']
            unit = temp_ingredient['unit']

            for old_association in recipe.ingredients:
                if old_association.ingredient.name == name:
                    old_association.amount = amount
                    old_association.unit = unit
                    new_ingredients.append(old_association)
                    break
            else:
                association = cls.create_new_ingredient_association(name, amount, unit)  # TODO: kwargs
                new_ingredients.append(association)
        recipe.ingredients = new_ingredients
        recipe.save_to_db()
        return recipe

    @classmethod
    def create_new_ingredient_association(cls, name, amount, unit):
        ingredient = IngredientModel.find_by_name(name)
        if not ingredient:
            ingredient = IngredientModel(name)
        association = RecipeIngredientModel(amount, unit)
        association.ingredient = ingredient
        return association


class RecipeList(Resource):
    def get(self):
        return {'recipes': [recipe.json() for recipe in RecipeModel.query.all()]}
