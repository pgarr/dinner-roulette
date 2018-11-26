from flask import jsonify

from db import db
from models.recipe import Recipe
from models.recipe_detail import RecipeDetail
from models.recipe_ingredient import RecipeIngredient
from schemas import recipe_schema, recipes_schema


class RecipeService:
    @classmethod
    def get_by_pk(cls, pk):
        recipe = Recipe.query.get(pk)
        if not recipe:
            return jsonify({'message': 'Recipe could not be found.'}), 404
        recipe_result = recipe_schema.dump(recipe)
        return jsonify(
            {'recipe': recipe_result.data})

    @classmethod
    def get_all(cls):
        recipes = Recipe.query.all()
        result = recipes_schema.dump(recipes)
        return jsonify({'recipes': result.data})

    @classmethod
    def create(cls, json_data):
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        data, errors = recipe_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        recipe_detail = RecipeDetail(
            link=data['detail']['link'],
            description=data['detail']['description']
        )
        recipe = Recipe(
            name=data['name'],
            detail=recipe_detail,
            ingredients=[]
        )
        for ingredient in data['ingredients']:
            recipe_ingredient = RecipeIngredient(
                name=ingredient['name'],
                amount=ingredient['amount'],
                unit=ingredient['unit']
            )
            recipe.ingredients.append(recipe_ingredient)
        db.session.add(recipe)
        db.session.commit()
        result = recipe_schema.dump(Recipe.query.get(recipe.id))
        return jsonify({"message": "Created new recipe.",
                        "recipe": result.data}), 201
