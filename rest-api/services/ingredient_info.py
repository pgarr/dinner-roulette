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
