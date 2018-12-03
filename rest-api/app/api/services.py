from flask import jsonify

from app import db
from app.models import Recipe, RecipeDetail, RecipeIngredient, IngredientInfo, IngredientUnitMultiplier
from app.schemas import recipe_schema, recipes_schema, ingredient_infos_schema, ingredient_info_schema


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


class IngredientInfoService:
    @classmethod
    def get_all(cls):
        ingredients = IngredientInfo.query.all()
        result = ingredient_infos_schema.dump(ingredients)
        return jsonify({'ingredients': result.data})

    @classmethod
    def get_by_pk(cls, pk):
        ingredient = IngredientInfo.query.get(pk)
        if not ingredient:
            return jsonify({'message': 'Ingredient could not be found.'}), 404
        result = ingredient_info_schema.dump(ingredient)
        return jsonify(
            {'ingredient': result.data})

    @classmethod
    def get_by_name(cls, name):
        ingredient = IngredientInfo.query.filter_by(name=name).first()
        if not ingredient:
            return jsonify({'message': 'Ingredient could not be found.'}), 404
        result = ingredient_info_schema.dump(ingredient)
        return jsonify(
            {'ingredient': result.data})

    @classmethod
    def create(cls, json_data):
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        data, errors = ingredient_info_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        ingredient_info_model = IngredientInfo(
            name=data['name'],
            calories_per_gram=data['calories_per_gram'],
            unit_multipliers=[]
        )
        for data_unit_multiplier in data['unit_multipliers']:
            ingredient_unit_multiplier_model = IngredientUnitMultiplier(
                unit=data_unit_multiplier['unit'],
                multiplier=data_unit_multiplier['multiplier']
            )
            ingredient_info_model.unit_multipliers.append(ingredient_unit_multiplier_model)
            db.session.add(ingredient_info_model)
            db.session.commit()
            result = ingredient_info_schema.dump(IngredientInfo.query.get(ingredient_info_model.id))
            return jsonify({"message": "Created new ingredient info.",
                            "ingredient info": result.data}), 201

    @classmethod
    def update_by_pk(cls, pk, json_data):
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        ingredient_info_model = IngredientInfo.query.get(pk)
        if not ingredient_info_model:
            return jsonify({'message': 'Ingredient info could not be found.'}), 404
        data, errors = ingredient_info_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        ingredient_info_model.name = data['name']
        ingredient_info_model.calories_per_gram = data['calories_per_gram']
        ingredient_info_model.unit_multipliers = []
        for data_unit_multiplier in data['unit_multipliers']:
            ingredient_unit_multiplier_model = IngredientUnitMultiplier(
                unit=data_unit_multiplier['unit'],
                multiplier=data_unit_multiplier['multiplier']
            )
            ingredient_info_model.unit_multipliers.append(ingredient_unit_multiplier_model)
        db.session.add(ingredient_info_model)
        db.session.commit()

        result = ingredient_info_schema.dump(IngredientInfo.query.get(ingredient_info_model.id))
        return jsonify({"message": "Ingredient info updated.",
                        "ingredient info": result.data}), 200

    @classmethod
    def delete_by_pk(cls, pk):
        ingredient = IngredientInfo.query.get(pk)
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return jsonify({"message": "Ingredient info deleted."}), 200
        return jsonify({'message': 'Ingredient info could not be found.'}), 404
