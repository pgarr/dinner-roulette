from flask import jsonify
from sqlalchemy.exc import IntegrityError

from models.recipe import Recipe
from schemas import recipe_schema, recipe_detail_schema, recipe_ingredients_schema


class RecipeService:
    @classmethod
    def get_by_pk(cls, pk):
        try:
            recipe = Recipe.query.get(pk)
        except IntegrityError:
            return jsonify({'message': 'Recipe could not be found.'}), 404
        recipe_result = recipe_schema.dump(recipe)
        recipe_detail_result = recipe_detail_schema.dump(recipe.detail.get())
        ingredients_result = recipe_ingredients_schema.dump(recipe.ingredients.all())
        return jsonify({'recipe': recipe_result, 'detail': recipe_detail_result, 'ingredients': ingredients_result})
