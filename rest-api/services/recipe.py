from flask import jsonify

from db import db
from models.recipe import Recipe, RecipeDetail, RecipeIngredient
from schemas.recipe import recipe_schema, recipes_schema, recipe_update_schema


class RecipeService:
    @classmethod
    def get_by_pk(cls, pk):
        recipe = Recipe.query.get(pk)
        if not recipe:
            return jsonify({'message': 'Recipe could not be found.'}), 404
        result = recipe_schema.dump(recipe)
        return jsonify(
            {'recipe': result.data})

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
        recipe_detail_model = RecipeDetail(
            link=data['detail']['link'],
            description=data['detail']['description']
        )
        recipe_model = Recipe(
            name=data['name'],
            detail=recipe_detail_model,
            ingredients=[]
        )
        for data_ingredient in data['ingredients']:
            recipe_ingredient_model = RecipeIngredient(
                name=data_ingredient['name'],
                amount=data_ingredient['amount'],
                unit=data_ingredient['unit']
            )
            recipe_model.ingredients.append(recipe_ingredient_model)
        db.session.add(recipe_model)
        db.session.commit()
        result = recipe_schema.dump(Recipe.query.get(recipe_model.id))
        return jsonify({"message": "Created new recipe.",
                        "recipe": result.data}), 201

    @classmethod
    def update_by_pk(cls, pk, json_data):
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        recipe_model = Recipe.query.get(pk)
        if not recipe_model:
            return jsonify({'message': 'Recipe could not be found.'}), 404
        data, errors = recipe_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        recipe_model.name = data['name']
        recipe_model.detail.link = data['detail']['link']
        recipe_model.detail.description = data['detail']['description']
        recipe_model.ingredients = []
        for data_ingredient in data['ingredients']:
            recipe_ingredient_model = RecipeIngredient(
                name=data_ingredient['name'],
                amount=data_ingredient['amount'],
                unit=data_ingredient['unit']
            )
            recipe_model.ingredients.append(recipe_ingredient_model)
        db.session.add(recipe_model)
        db.session.commit()
        result = recipe_schema.dump(Recipe.query.get(pk))

        return jsonify({"message": "Recipe updated.",
                        "recipe": result.data}), 200

    @classmethod
    def get_filtered(cls, ingredient):
        recipes = Recipe.query.filter(Recipe.ingredients.any(RecipeIngredient.name == ingredient)).all()
        result = recipes_schema.dump(recipes)
        return jsonify({'recipes': result.data})

    @classmethod
    def delete_by_pk(cls, pk):
        recipe = Recipe.query.get(pk)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted."}), 200
        return jsonify({'message': 'Recipe could not be found.'}), 404
