from flask import jsonify

from db import db
from models.ingredient_info import IngredientInfo, IngredientUnitMultiplier
from schemas.ingredient_info import ingredient_infos_schema, ingredient_info_schema


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
        ingredient_info = IngredientInfo(
            name=data['name'],
            calories_per_gram=data['calories_per_gram']
        )
        for multiplier in data['unit_multipliers']:
            ingredient_unit_multiplier = IngredientUnitMultiplier(
                unit=multiplier['unit'],
                multiplier=multiplier['multiplier']
            )
            ingredient_info.append(ingredient_unit_multiplier)
            db.session.add(ingredient_info)
            db.session.commit()
            result = ingredient_info_schema.dump(IngredientInfo.query.get(ingredient_info.id))
            return jsonify({"message": "Created new ingredient info.",
                            "ingredient info": result.data}), 201

    @classmethod
    def update_by_pk(cls, pk, json_data):
        pass  # TODO: implement
